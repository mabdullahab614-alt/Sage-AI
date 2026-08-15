"""
Code execution utility.

IMPORTANT SECURITY NOTE:
This uses a subprocess with resource limits (CPU time, memory, no network via
env stripping is NOT real network isolation) and a timeout. This is a
best-effort MVP sandbox, NOT a hard security boundary. For a real deployment,
swap this out for a proper sandbox like E2B (https://e2b.dev) or Judge0
(https://judge0.com) — both have free tiers and actually isolate execution
in a separate container/VM. The hook points to do that are marked below.
"""

import subprocess
import sys
import tempfile
import os

# `resource` is Unix-only (no such module on Windows). Import it conditionally
# so this file doesn't crash on import on Windows — we just skip the extra
# CPU/memory/process caps there and rely on the subprocess timeout instead.
IS_WINDOWS = os.name == "nt"
if not IS_WINDOWS:
    import resource

DEFAULT_TIMEOUT_SECONDS = 10
MAX_MEMORY_MB = 256
MAX_OUTPUT_CHARS = 8000


def _limit_resources():
    """Called in the child process before exec (POSIX only) — caps CPU time and memory."""
    max_mem_bytes = MAX_MEMORY_MB * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (max_mem_bytes, max_mem_bytes))
    resource.setrlimit(resource.RLIMIT_CPU, (DEFAULT_TIMEOUT_SECONDS, DEFAULT_TIMEOUT_SECONDS))
    # Prevent forking bombs / excessive subprocesses
    resource.setrlimit(resource.RLIMIT_NPROC, (32, 32))


def execute_python(code: str, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> dict:
    """
    Executes Python code in an isolated subprocess with resource limits.

    Returns:
        {"success": bool, "stdout": str, "stderr": str, "timed_out": bool}
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        script_path = f.name

    # Stripped-down environment for the child process. Windows needs a couple
    # of extra system vars beyond PATH or python.exe can fail to initialize
    # (e.g. sockets, temp dir resolution).
    if IS_WINDOWS:
        child_env = {
            "PATH": os.environ.get("PATH", ""),
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
            "TEMP": os.environ.get("TEMP", ""),
            "TMP": os.environ.get("TMP", ""),
        }
    else:
        child_env = {"PATH": os.environ.get("PATH", "")}

    try:
        # NOTE: To use a real sandbox instead, replace this subprocess.run call
        # with a call to E2B's `Sandbox.run_code()` or Judge0's submission API.
        proc = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            preexec_fn=None if IS_WINDOWS else _limit_resources,  # POSIX-only hook
            env=child_env,
        )
        stdout = proc.stdout[:MAX_OUTPUT_CHARS]
        stderr = proc.stderr[:MAX_OUTPUT_CHARS]
        return {
            "success": proc.returncode == 0,
            "stdout": stdout,
            "stderr": stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution timed out after {timeout} seconds.",
            "timed_out": True,
        }
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": f"Execution error: {e}", "timed_out": False}
    finally:
        try:
            os.unlink(script_path)
        except OSError:
            pass
