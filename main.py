import socket
import concurrent.futures
import pyfiglet
from colorama import Fore
import colorama
import os

def check_ip_port(ip, port):
    """
    Check if a given IP and port combination is active.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            return ip, port, True
        else:
            return ip, port, False
    except socket.error:
        return ip, port, False

def check_ips(ip_port_list):
    """
    Check a list of IP and port combinations.
    """
    active_ips = []
    inactive_ips = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(lambda x: check_ip_port(x[0], x[1]), ip_port_list)

        for ip, port, is_active in results:
            if is_active:
                active_ips.append(f"{ip}:{port}")
            else:
                inactive_ips.append(f"{ip}:{port}")

    return active_ips, inactive_ips

def save_to_file(filename, ip_list):
    """
    Save a list of IPs to a file.
    """
    with open(filename, 'w') as f:
        for ip in ip_list:
            f.write(f"{ip}\n")

def read_ip_port_from_file(filename):
    """
    Read IP addresses and ports from a file.
    """
    ip_port_list = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(':')
                if len(parts) == 2:
                    ip = parts[0]
                    try:
                        port = int(parts[1])
                        ip_port_list.append((ip, port))
                    except ValueError:
                        print(f"Invalid port number in line: {line}")
                else:
                    print(f"Invalid format in line: {line}")
    return ip_port_list
    
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')
    
print(colorama.Fore.RED)
pyfiglet.print_figlet("Asylum")


def main():
    print(colorama.Fore.RESET)
    input_file = input("Enter IP List==> ")

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    ip_port_list = read_ip_port_from_file(input_file)

    if not ip_port_list:
        print("No valid IP:port combinations found in the file.")
        return

    print("Checking IP and ports...")
    active_ips, inactive_ips = check_ips(ip_port_list)

    save_to_file('active_ips.txt', active_ips)
    save_to_file('inactive_ips.txt', inactive_ips)
    print(colorama.Fore.GREEN)
    print("\nActive IPs:")
    print(colorama.Fore.RESET)
    for ip in active_ips:
        print(f"  - {ip}")
    print(colorama.Fore.RED)
    print("\nInactive IPs:")
    print(colorama.Fore.RESET)
    for ip in inactive_ips:
        print(f"  - {ip}")

    print("\nActive IPs saved in 'active_ips.txt'")
    print("Inactive IPs saved in 'inactive_ips.txt'")

if __name__ == "__main__":
    main()