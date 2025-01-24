import subprocess
import psutil
import time
import threading

# Function to recursively terminate a process and its children
def terminate_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)  # Get all child processes
        for child in children:
            print(f"Terminating child process: {child.pid}")
            child.terminate()  # Terminate each child process
        print(f"Terminating parent process: {parent.pid}")
        parent.terminate()  # Terminate the parent process
    except psutil.NoSuchProcess:
        print(f"Process {pid} no longer exists.")
    except Exception as e:
        print(f"Failed to terminate process {pid}. Error: {e}")

# Function to read and print output from a stream
def file_watcher_log(stream):
    for line in stream:
        print(line.strip())

# Start the file watcher process
file_watcher_process = subprocess.Popen(
    r'python "src\scb(file_watcher\file_watcher_handler.py" local',
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
    text=True,
    cwd=r"C:\Users\8213636\OneDrive - Standard Chartered Bank\Documents\Projects\utilities"
)

# Wait for the process to start
time.sleep(5)

# Start threads to read stdout and stderr
stdout_thread = threading.Thread(target=file_watcher_log, args=(file_watcher_process.stdout,))
stderr_thread = threading.Thread(target=file_watcher_log, args=(file_watcher_process.stderr,))
stdout_thread.start()
stderr_thread.start()

# Simulate some work
time.sleep(10)  # Replace with your actual logic

# Terminate the file watcher process and all its child processes
print("Terminating file watcher process and its children...")
terminate_process_tree(file_watcher_process.pid)

# Wait for the threads to finish
stdout_thread.join()
stderr_thread.join()

print("File watcher process and all child processes terminated.")