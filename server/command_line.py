import sys
import re
from typing import Tuple

MIN_PORT: int = 1024
MAX_PORT: int = 65535

def has_arg(index: int) -> bool:
    """Checks if there are at least `index + 1` arguments passed to the command line

    Args:
        index (int): The position of the expected argument

    Returns:
        bool: True if the argument exists

    """
    return len(sys.argv) >= (index + 1)

def get_port(index: int) -> int:
    """Gets the port at the `index` argument in the command line

    Args:
        index (int): the argument containing a port

    Returns:
        int: A valid port

    Raises:
        ValueError: Argument does not exist or port is not in the range 1024-65535
    """

    if not has_arg(index):
        raise ValueError(f'Argument [{index}] was not specified on the command line')

    port: int = int(sys.argv[index])

    if not (port > MIN_PORT and port < MAX_PORT):
        raise ValueError(f'Invalid port specified. Port must be between {MIN_PORT} and {MAX_PORT}')

    return port

def get_ip_address(index: int) -> str:
    """Gets the ip address at the `index` argument in the command line

    Args:
        index (int): the argument containing the ip address

    Returns:
        str: A valid ip address 

    Raises:
        ValueError: Argument does not exist or ip address is not in the correct format xxx.xxx.xxx.xxx
    """

    if not has_arg(index):
        raise ValueError(f'Argument [{index}] was not specified on the command line')

    ip_address: str = sys.argv[index]
    capture_group = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip_address)
    if len(capture_group) == 0:
        raise ValueError(f'Invalid ip address specified. ip address must be in the format xxx.xxx.xxx.xxx')

    return ip_address

def get_request_info(index: int):

    if not has_arg(index) or not has_arg(index + 1):
        raise ValueError(f'Arguments [{index}, {index+1}] was not specified on the command line')

    filename: str = sys.argv[index]
    method: str = sys.argv[index + 1]

    return (filename, method)