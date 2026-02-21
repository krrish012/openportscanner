import concurrent.futures
import socket
import time

target_ip = input("Enter the IP address to scan (e.g., 127.0.0.1): ")

# We define a function that takes a 'port' number as its argument
def scan_port(port):
    # This creates a socket object. 
    # AF_INET tells it to use an IPv4 address (like 127.0.0.1).
    # SOCK_STREAM tells it to use TCP (the reliable, 3-way handshake protocol).
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Tells the socket to wait 1 second for a response before giving up.
    my_socket.settimeout(0.5)

    # The function requires a tuple containing the IP (as a string) and the Port (as an integer).
    result = my_socket.connect_ex((target_ip, port))
    if result == 0:
        try:
            # Tries to look up the service name
            service = socket.getservbyport(port, "tcp")
            print(f"Port {port} is open. Service: {service}")
        except OSError:
            # If the OS doesn't know the service, it should just print this:
            print(f"Port {port} is open. Service: Unknown")
    my_socket.close()

start_time = time.time()
# Create a pool with exactly 100 workers. 
# The "with" statement ensures the pool cleans itself up when finished.
with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
    # executor.map takes two things: the function to run, and the list of numbers to feed it.
    # It automatically distributes the numbers to the available workers.
    executor.map(scan_port, range(1, 65536))
end_time = time.time()

print(f"Scan completed in {end_time - start_time:.2f} seconds.")