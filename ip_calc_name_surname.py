def main():
    """
    None -> None
    The main func of program
    """
    raw_address = input()
    print("IP address:", get_ip_from_raw_address(raw_address))
    print("Network Address:", get_network_address_from_raw_address(raw_address))
    print("Broadcast Address:", get_broadcast_address_from_raw_address(raw_address))
    print("Binary Subnet Mask:", get_binary_mask_from_raw_address(raw_address))
    print("Number of usable Hosts:", get_number_of_usable_hosts_from_raw_address(raw_address))


def get_ip_from_raw_address(raw_address):
    """
    str -> str
    This func returns ip adress
    """
    vals = raw_address.split("/")
    try:
        int(vals[1])
    except TypeError:
        return None

    return vals[0]


def get_network_address_from_raw_address(raw_address):
    """
    This func returns network adress from ip
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
    This func returns broadcast address
    """
    ip_bin, mask_bin = get_ip_and_mask(raw_address)

    address_bin = bin((~int(mask_bin, 2)) | int(ip_bin, 2))
    ip_bin_arr = []
    address_bin = address_bin[2::]

    temp_val = ''

    for pos in range(len(address_bin)):
        if pos % 8 == 0:
            ip_bin_arr.append(temp_val)
            temp_val = ''
        else:
            temp_val += address_bin[pos]

    address_ready = ""

    for elem in ip_bin_arr:
        address_ready += str(int(elem, 2))
        address_ready += '.'

    return address_ready[:-1:]


def get_binary_mask_from_raw_address(raw_address):
    """
    This func returns binary mask
    """
    ip_bin, mask_bin = get_ip_and_mask(raw_address)

    mask_bin = mask_bin[2::]

    ready_mask = ""
    for pos in range(len(mask_bin)):
        if pos % 8 == 0 and pos != 0:
            ready_mask += '.'
        ready_mask += mask_bin[pos]

    return ready_mask


def get_number_of_usable_hosts_from_raw_address(raw_address):
    """
    This func returns max num of usable hosts
    """
    ip, mask = raw_address.split("/")
    mask = int(mask)

    max_num = 2 ^ (32 - mask) - 2

    return max_num


"""def get_first_usable_ip_address_from_raw_address(raw_address):
    adress_network = get_network_address_from_raw_address(raw_address)

    ip_arr = adress_network.split('.')
    ip_bin, mask_bin = get_ip_and_mask(raw_address)

    mask_now = bin(int(mask_bin, 2) + 1)
    
    ip_network_bin = ''
    for elem in ip_arr:
        """


def get_ip_and_mask(raw_address):
    """
    This func returns binary ip and mask
    """
    ip, mask = raw_address.split("/")
    mask = int(mask)

    ip_parts = ip.split(".")

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


main()