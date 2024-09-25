import ftplib
import os

# Function to interact with the FTP server in a simple shell-like interface
def ftp_shell(ftp):
    local_dir = os.getcwd()  # Store the current local directory
    while True:
        try:
            # Show the remote and local directory in the prompt
            prompt = f"ftp:{ftp.pwd()} (local:{local_dir})> "
            cmd = input(prompt).strip()  # Get user input for the command
            
            # Exit the shell
            if cmd.lower() in ['quit', 'exit']:
                print("Exiting FTP shell.")
                ftp.quit()  # Close FTP connection
                break

            # List files in the current directory
            elif cmd.lower() in ['ls', 'dir']:
                try:
                    ftp.retrlines('LIST')  # List remote directory contents
                except Exception as e:
                    print(f"Could not list directory: {e}")

            # Show the current directory on the FTP server
            elif cmd.lower() == 'pwd':
                try:
                    print(f"Remote directory: {ftp.pwd()}")
                except Exception as e:
                    print(f"Could not get current directory: {e}")

            # Change the local directory
            elif cmd.lower().startswith('lcd'):
                try:
                    local_directory = cmd.split()[1]
                    os.chdir(local_directory)
                    local_dir = os.getcwd()  # Update local directory
                    print(f"Changed local directory to: {local_dir}")
                except IndexError:
                    print("Usage: lcd <local_directory>")
                except FileNotFoundError:
                    print(f"Local directory not found: {local_directory}")
                except Exception as e:
                    print(f"Could not change local directory: {e}")

            # Download a file from the FTP server
            elif cmd.lower().startswith('get'):
                try:
                    filename = cmd.split()[1]
                    local_filename = os.path.join(local_dir, filename)
                    with open(local_filename, 'wb') as f:
                        ftp.retrbinary(f"RETR {filename}", f.write)
                    print(f"Downloaded {filename} to {local_filename}")
                except IndexError:
                    print("Usage: get <remote_filename>")
                except Exception as e:
                    print(f"Failed to download the file: {e}")

            # Upload a file to the FTP server
            elif cmd.lower().startswith('put'):
                try:
                    filename = cmd.split()[1]
                    with open(filename, 'rb') as f:
                        ftp.storbinary(f"STOR {filename}", f)
                    print(f"Uploaded {filename}")
                except IndexError:
                    print("Usage: put <local_filename>")
                except FileNotFoundError:
                    print(f"Local file not found: {filename}")
                except Exception as e:
                    print(f"Failed to upload the file: {e}")

            # Change the directory on the FTP server
            elif cmd.lower().startswith('cd'):
                try:
                    directory = cmd.split()[1]
                    ftp.cwd(directory)  # Change remote directory
                    print(f"Switched to directory: {directory}")
                except IndexError:
                    print("Usage: cd <remote_directory>")
                except Exception as e:
                    print(f"Failed to change directory: {e}")

            # Delete a file on the FTP server
            elif cmd.lower().startswith('delete'):
                try:
                    filename = cmd.split()[1]
                    ftp.delete(filename)  # Delete remote file
                    print(f"Deleted {filename}")
                except IndexError:
                    print("Usage: delete <remote_filename>")
                except Exception as e:
                    print(f"Failed to delete file: {e}")

            # Display help information
            elif cmd.lower() == 'help':
                print("Available commands:")
                print("  ls, dir         - List files in the current directory on the FTP server.")
                print("  cd <dir>        - Change the directory on the FTP server.")
                print("  pwd             - Display the current directory on the FTP server.")
                print("  lcd <dir>       - Change the local directory for downloads/uploads.")
                print("  get <file>      - Download a file from the FTP server.")
                print("  put <file>      - Upload a file to the FTP server.")
                print("  delete <file>   - Delete a file on the FTP server.")
                print("  quit, exit      - Exit the FTP shell.")
                print("  help            - Show this help message.")

            # Unknown command
            else:
                print(f"Unknown command: '{cmd}'")
        
        except Exception as main_exception:
            print(f"An unexpected error occurred: {main_exception}")

# Main function to start the FTP enumeration and interact with the server
def ftp_enum(target_ip):
    try:
        print(f"Connecting to FTP server at {target_ip}...")
        ftp = ftplib.FTP(target_ip)  # Connect to the FTP server
        ftp.login()  # Attempt anonymous login with a blank password
        print(f"Successfully logged into {target_ip} as anonymous.")
        ftp_shell(ftp)  # Start the interactive shell
    except Exception as e:
        print(f"Could not connect to FTP server: {e}")

# Start the process with the given target IP
ftp_enum('192.168.65.136')


