"""
ip_calc_yevhen_pankevuch.py
This module calculates many values from ip
"""

import re


def main():
    """
    None -> None
    The main func of program
    """
    raw_address = input()

    pat = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}$")
    check_pref = pat.match(raw_address)

    if not check_pref:
        print("Invalid form (missing prefix or not enough nums)")
    else:
        try:
            print("IP address:", get_ip_from_raw_address(raw_address))
            print("Network Address:", get_network_address_from_raw_address(raw_address))
            print("Broadcast Address:", get_broadcast_address_from_raw_address(raw_address))
            print("Binary Subnet Mask:", get_binary_mask_from_raw_address(raw_address))
            print("Number of usable hosts:",\
                  get_number_of_usable_hosts_from_raw_address(raw_address))
            print("First usable host IP:",\
                  get_first_usable_ip_address_from_raw_address(raw_address))
            print("Penultimate usable host IP:",\
                  get_penultimate_usable_ip_address_from_raw_address(raw_address))
            print("IP class:", get_ip_class_from_raw_address(raw_address))
            print("IP type private:", check_private_ip_address_from_raw_address(raw_address))
        except TypeError:
            print("Error")
        except IndexError:
            print("Error")


def get_ip_from_raw_address(raw_address):
    """
    str -> str
    This func returns ip adress or None in errors
    >>> get_ip_from_raw_address("1.1.1.1/10")
    '1.1.1.1'
    >>> get_ip_from_raw_address("34.34.10.20/10")
    '34.34.10.20'
    """
    vals = raw_address.split("/")
    try:
        int(vals[1])
    except TypeError:
        return None
    except IndexError:
        return None

    return vals[0]


def get_network_address_from_raw_address(raw_address):
    """
    srt -> str
    This func returns network address from ip
    >>> get_network_address_from_raw_address("91.124.230.205/30")
    '91.124.230.204'
    >>> get_network_address_from_raw_address("192.168.0.3/24")
    '192.168.0.0'
    """

    ip_bin, mask_bin = get_ip_and_mask(raw_address)

    address_bin = bin(int(mask_bin, 2) & int(ip_bin, 2))
    ip_bin_arr = []
    address_bin = address_bin[2::]
    if len(address_bin) < 32:
        address_bin = ('0' * (32 - len(address_bin))) + address_bin

    temp_val = ''

    for pos in range(len(address_bin)):
        if pos % 8 == 0 and pos != 0:
            ip_bin_arr.append(temp_val)
            temp_val = ''
        temp_val += address_bin[pos]

    ip_bin_arr.append(temp_val)
    address_ready = ""

    for elem in ip_bin_arr:
        address_ready += str(int(elem, 2))
        address_ready += '.'

    return address_ready[:-1:]


def get_broadcast_address_from_raw_address(raw_address):
    """
    str -> str
    This func returns broadcast address
    >>> get_broadcast_address_from_raw_address("91.124.230.205/30")
    '91.124.230.207'
    >>> get_broadcast_address_from_raw_address("192.168.0.3/24")
    '192.168.0.255'
    """
    ip_bin, mask_bin = get_ip_and_mask(raw_address)

    not_mask = ""

    for elem in mask_bin[2::]:
        if elem == "0":
            not_mask += "1"
        else:
            not_mask += "0"

    address_bin = bin(int(not_mask, 2) | int(ip_bin, 2))
    ip_bin_arr = []
    address_bin = address_bin[2::]

    address_bin = "0" * (32 - len(address_bin)) + address_bin

    temp_val = ''

    for pos in range(len(address_bin)):
        if pos % 8 == 0 and pos != 0:
            ip_bin_arr.append(temp_val)
            temp_val = ''
        temp_val += address_bin[pos]
    ip_bin_arr.append(temp_val)

    address_ready = ""

    for elem in ip_bin_arr:
        address_ready += str(int(elem, 2))
        address_ready += '.'

    return address_ready[:-1:]


def get_binary_mask_from_raw_address(raw_address):
    """
    str -> str
    This func returns binary mask
    >>> get_binary_mask_from_raw_address("91.124.230.205/30")
    '11111111.11111111.11111111.11111100'
    >>> get_binary_mask_from_raw_address("192.168.0.3/24")
    '11111111.11111111.11111111.00000000'
    """
    ip_bin, mask_bin = get_ip_and_mask(raw_address)

    ip_bin = ip_bin * 1

    mask_bin = mask_bin[2::]

    ready_mask = ""
    for pos in range(len(mask_bin)):
        if pos % 8 == 0 and pos != 0:
            ready_mask += '.'
        ready_mask += mask_bin[pos]

    return ready_mask


def get_number_of_usable_hosts_from_raw_address(raw_address):
    """
    str -> int
    This func returns max num of usable hosts
    >>> get_number_of_usable_hosts_from_raw_address("91.124.230.205/30")
    2
    >>> get_number_of_usable_hosts_from_raw_address("192.168.0.3/24")
    254
    """
    ip_address, mask = raw_address.split("/")
    ip_address = ip_address * 1
    mask = int(mask)

    max_num = (2 ** (32 - mask)) - 2

    return max_num


def get_ip_class_from_raw_address(raw_address):
    """
    str -> str
    This func returns class of IP address
    >>> get_ip_class_from_raw_address("91.124.230.205/30")
    'A'
    >>> get_ip_class_from_raw_address("192.168.0.3/24")
    'C'
    """
    ip_address, mask = get_norm_mask_and_ip(raw_address)
    mask = mask * 1

    ip_arr = ip_address.split(".")

    ip_class = int(ip_arr[0])

    if 1 <= ip_class <= 126:
        return "A"
    if 128 <= ip_class <= 191:
        return "В"
    if 192 <= ip_class <= 223:
        return "C"
    if 224 <= ip_class <= 239:
        return "D"
    if 240 <= ip_class <= 247:
        return "E"
    return None


def get_first_usable_ip_address_from_raw_address(raw_address):
    """
    str -> str
    This func returns first usable host ip address
    >>> get_first_usable_ip_address_from_raw_address("91.124.230.205/30")
    '91.124.230.205'
    >>> get_first_usable_ip_address_from_raw_address("192.168.0.3/24")
    '192.168.0.1'
    """
    if get_number_of_usable_hosts_from_raw_address(raw_address) > 0:
        ip_address = get_network_address_from_raw_address(raw_address)

        ip_arr = ip_address.split(".")
        ip_host_bit = int(ip_arr[3]) + 1

        ip_first_host = str(ip_arr[0]) + "." +\
                        str(ip_arr[1]) + "." + str(ip_arr[2]) + "." + str(ip_host_bit)

        return ip_first_host
    return None


def get_penultimate_usable_ip_address_from_raw_address(raw_address):
    """
    str -> str
    This func returns penultimate usable host ip address
    >>> get_penultimate_usable_ip_address_from_raw_address("91.124.230.205/30")
    '91.124.230.205'
    >>> get_penultimate_usable_ip_address_from_raw_address("192.168.0.3/24")
    '192.168.0.253'
    """
    if get_number_of_usable_hosts_from_raw_address(raw_address) > 1:
        ip_address = get_broadcast_address_from_raw_address(raw_address)

        ip_arr = ip_address.split(".")
        ip_host_bit = int(ip_arr[3]) - 2

        ip_prelast_host = str(ip_arr[0]) + "." +\
                          str(ip_arr[1]) + "." + str(ip_arr[2]) + "." + str(ip_host_bit)

        return ip_prelast_host
    return None


def check_private_ip_address_from_raw_address(raw_address):
    """
    str -> bool
    Returns True if IP address is private, else False
    >>> check_private_ip_address_from_raw_address("91.124.230.205/30")
    False
    >>> check_private_ip_address_from_raw_address("192.168.0.3/24")
    True
    """
    ip_address, mask = get_norm_mask_and_ip(raw_address)
    mask = mask * 1

    ip_arr = ip_address.split(".")
    ip_type = int(ip_arr[0])

    example_list = [10, 127, 172, 192]
    if ip_type in example_list:
        return True
    return False


def get_ip_and_mask(raw_address):
    """
    str -> (str, str)
    This func returns binary ip and mask
    >>> get_ip_and_mask("91.124.230.205/30")
    ('0b01011011011111001110011011001101', '0b11111111111111111111111111111100')
    >>> get_ip_and_mask("192.168.0.3/24")
    ('0b11000000101010000000000000000011', '0b11111111111111111111111100000000')
    """
    ip_address, mask = raw_address.split("/")
    mask = int(mask)

    ip_parts = ip_address.split(".")

    mask_bin = '0b'
    mask_bin += '1' * mask
    mask_bin += '0' * (32 - mask)

    ip_bin = '0b'

    for elem in ip_parts:
        temp_val = bin(int(elem))[2::]
        if len(temp_val) < 8:
            ip_bin += '0' * (8 - len(temp_val))
        ip_bin += temp_val

    return ip_bin, mask_bin


def get_norm_mask_and_ip(raw_address):
    """
    str -> (str, str)
    This func returns normal ip and mask
    >>> get_norm_mask_and_ip("91.124.230.205/30")
    ('91.124.230.205', '30')
    >>> get_norm_mask_and_ip("192.168.0.3/24")
    ('192.168.0.3', '24')
    """
    ip_address, mask = raw_address.split("/")
    return ip_address, mask


if __name__ == "__main__":
    main()
