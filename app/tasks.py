import subprocess


def ping(host: str, port: int = 8080) -> bool:
    """
    Ping server with telnet
    :param host: Host name
    :param port: Port num
    :return: Returns True if host (str) responds to a ping request
    """
    command = f"echo -e \x1dclose\x0d | telnet {host} {port}"
    try:
        subprocess.check_output(
            command, stderr=subprocess.DEVNULL, timeout=10, shell=True
        )
    except subprocess.CalledProcessError:
        return False
    else:
        return True
