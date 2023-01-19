import platform
import subprocess


def ping(host: str, silent: bool = True) -> bool:
    """

    :param host: Host name. For ex: 192.168.1.1
    :param silent: No output to console mode
    :return: Returns True if host (str) responds to a ping request
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    if silent:
        return subprocess.call(command, stdout=subprocess.DEVNULL, shell=True) == 0
    return subprocess.call(command, shell=True) == 0
