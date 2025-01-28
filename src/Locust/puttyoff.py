import paramiko

def ssh_connect(hostname, port, username, password):
    # Create an SSH client
    client = paramiko.SSHClient()
    
    # Automatically add the server's host key (this is insecure, see note below)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Connect to the server
    client.connect(hostname, port=port, username=username, password=password)
    
    return client

def run_commands(client, commands):
    # Open a session
    stdin, stdout, stderr = client.exec_command(commands)
    
    # Read the output and error
    output = stdout.read().decode()
    error = stderr.read().decode()
    
    # Print the output and error
    if output:
        print("Output:")
        print(output)
    if error:
        print("Error:")
        print(error)

def interactive_shell(client):
    # Open an interactive shell
    shell = client.invoke_shell()
    
    while True:
        # Get user input
        command = input("$ ")
        
        if command.lower() in ['exit', 'quit']:
            break
        
        # Send the command to the shell
        shell.send(command + "\n")
        
        # Receive the output
        while not shell.recv_ready():
            pass
        output = shell.recv(1024).decode()
        print(output, end='')
    
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
    
    # Run a set of commands
    commands = """
    echo "Running some commands..."
    ls -la
    whoami
    """
    run_commands(client, commands)
    
    # Enter interactive shell
    print("Entering interactive shell. Type 'exit' or 'quit' to exit.")
    interactive_shell(client)
    
    # Close the connection
    client.close()

if __name__ == "__main__":
    main()