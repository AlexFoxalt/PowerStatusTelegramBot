import subprocess


def ping(host: str, port: int = 8080) -> bool:
    command = f"echo -e \x1dclose\x0d | telnet {host} {port}"
    try:
        subprocess.check_output(
            command, stderr=subprocess.DEVNULL, timeout=10, shell=True
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False
    else:
        return True
