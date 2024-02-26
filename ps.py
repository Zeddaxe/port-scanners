import argparse
import socket
import threading
from concurrent.futures import ThreadPoolExecutor

def scan_port(port):
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set timeout for connection attempt
        s.settimeout(1)
        # Attempt to connect to the target IP address and port
        result = s.connect_ex((target_ip, port))
        if result == 0:
            # If port is open, attempt to get service/version information
            service_info = socket.getservbyport(port)
            print(f"Port {port} ({service_info}): OPEN")
        s.close()
    except Exception as e:
        print(f"Error occurred while scanning port {port}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-threaded port scanner with service/version detection")
    parser.add_argument("-t", "--target", help="Target IP address", required=True)
    parser.add_argument("-p", "--all-ports", help="Scan all ports", action="store_true")
    args = parser.parse_args()

    target_ip = args.target
    num_threads = 100  # Number of threads to use for scanning (adjust as needed)

    print(f"Wait just Starting f'kin port scan on {target_ip}...")

    # Create a ThreadPoolExecutor with the specified number of threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        if args.all_ports:
            # Scan all ports (1-65535)
            for port in range(1, 65536):
                executor.submit(scan_port, port)
        else:
            # Scan well-known ports (1-1024)
            for port in range(1, 1025):
                executor.submit(scan_port, port)

    print("Port scan complete.")
