from scapy.all import sniff, IP, TCP, Raw
import socket
import time

# Target IP to monitor
target_ip = "192.168.65.136"

# Log file to store captured packets
log_file = "network_log.txt"

# DNS cache dictionary
dns_cache = {}

# Function to get the domain name for a given IP address using DNS cache
def get_domain(ip_address):
    # Check if IP address is in the cache
    if ip_address in dns_cache:
        return dns_cache[ip_address]
    
    # Perform DNS lookup and cache the result
    try:
        domain = socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        domain = "Unknown Domain"
    
    # Store the result in the cache
    dns_cache[ip_address] = domain
    
    return domain

# Define a callback function to process captured packets
def packet_callback(packet):
    # Filter for IP packets only
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        # Log packets where target IP is either source or destination
        if src_ip == target_ip or dst_ip == target_ip:
            with open(log_file, "a") as f:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                
                # Get domain names for source and destination IPs using DNS cache
                src_domain = get_domain(src_ip)
                dst_domain = get_domain(dst_ip)
                
                # Create a log entry with domain names
                log_entry = f"[{timestamp}] {src_ip} ({src_domain}) -> {dst_ip} ({dst_domain})\n"
                f.write(log_entry)
                print(log_entry)

                # Check if it contains a Raw layer (which holds the payload)
                if packet.haslayer(Raw):
                    payload = packet[Raw].load
                    # Check if the payload contains HTTP data (e.g., HTTP GET/POST)
                    if b"HTTP" in payload:
                        try:
                            http_log_entry = f"[{timestamp}] HTTP data: {payload.decode(errors='ignore')}\n"
                            f.write(http_log_entry)
                            print(http_log_entry)
                        except:
                            pass

# Function to start sniffing packets
def start_sniffing(interface):
    print(f"[*] Starting packet sniffing on {interface}")
    # Start sniffing on the specified interface and call packet_callback for each packet
    sniff(iface=interface, prn=packet_callback, store=False)

if __name__ == "__main__":
    # Define the network interface to sniff on
    interface = 'eth0'  # Change this to your network interface, e.g., 'ens33'
    start_sniffing(interface)
