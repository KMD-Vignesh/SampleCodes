import subprocess
import time

def run_process_with_dynamic_stdout():
    try:
        # Start the first process (bat file)
        process1 = subprocess.Popen(
            ["path_to_your_bat_file.bat"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Start the second process (command)
        process2 = subprocess.Popen(
            ["your_command"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        while True:
            # Check if process2 is running
            if process2.poll() is None:
                # If process2 is running, output from process2
                if process2.stdout:
                    line = process2.stdout.readline()
                    if line:
                        print(f"[Process2]: {line.strip()}")
                if process2.stderr:
                    line = process2.stderr.readline()
                    if line:
                        print(f"[Process2 Error]: {line.strip()}")
            else:
                # Otherwise, output from process1
                if process1.stdout:
                    line = process1.stdout.readline()
                    if line:
                        print(f"[Process1]: {line.strip()}")
                if process1.stderr:
                    line = process1.stderr.readline()
                    if line:
                        print(f"[Process1 Error]: {line.strip()}")

            # Exit loop if both processes are complete
            if process1.poll() is not None and process2.poll() is not None:
                break

            time.sleep(0.1)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure proper cleanup
        if process1 and process1.poll() is None:
            process1.terminate()
        if process2 and process2.poll() is None:
            process2.terminate()

if __name__ == "__main__":
    run_process_with_dynamic_stdout()
