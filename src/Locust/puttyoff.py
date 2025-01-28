import paramiko
import select
import sys

def ssh_connect(hostname, port, username, password):
    # Create an SSH client
    client = paramiko.SSHClient()
    
    # Automatically add the server's host key (insecure, use with caution)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Connect to the server
    client.connect(hostname, port=port, username=username, password=password)
    
    return client

def interactive_shell(client):
    # Open an interactive shell session
    shell = client.invoke_shell()
    
    # Set the shell to non-blocking mode
    shell.setblocking(0)
    
    print("Interactive SSH shell opened. Type commands or 'exit' to quit.")
    
    while True:
        # Check for user input
        if select.select([sys.stdin], [], [], 0)[0]:
            user_input = sys.stdin.readline().strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting interactive shell.")
                break
            
            # Send the command to the shell
            shell.send(user_input + "\n")
        
        # Check for output from the shell
        while True:
            if select.select([shell], [], [], 0)[0]:
                # Read the output
                output = shell.recv(1024).decode('utf-8', errors='ignore')
                if not output:
                    break
                # Print the output in real-time
                print(output, end='')
            else:
                break
    
    # Close the shell
    shell.close()

def main():
    # Server details
    hostname = 'your.server.com'
    port = 22
    username = 'your_username'
    password = 'your_password'
    
    # Connect to the server
    client = ssh_connect(hostname, port, username, password)
    
    # Enter interactive shell
    interactive_shell(client)
    
    # Close the connection
    client.close()

if __name__ == "__main__":
    main()