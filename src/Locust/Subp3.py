import subprocess

def run_process_with_dynamic_stdout():
    # Paths to your files
    pytest_automation_file = "test\\automation.py"
    pytest_html_report = "test\\pytest_report.html"
    output_command = "--capture=tee-sys --tb=no"

    # Start the first process (.bat file)
    process1 = subprocess.Popen(
        ["test\\file_watcher.bat"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    )

    # Start the second process (pytest command)
    process2 = subprocess.Popen(
        f"pytest -v {pytest_automation_file} --html={pytest_html_report} --self-contained-html {output_command}",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    )

    try:
        # Use a loop to handle output in real-time for both processes
        while True:
            # Check process1's output
            if process1.poll() is None:  # Process is still running
                if process1.stdout:
                    for line in iter(process1.stdout.readline, ''):
                        print(f"[Process1]: {line.strip()}")  # Print process1's stdout in real-time
                if process1.stderr:
                    for line in iter(process1.stderr.readline, ''):
                        print(f"[Process1 Error]: {line.strip()}")  # Print process1's stderr

            # Check process2's output
            if process2.poll() is None:  # Process is still running
                if process2.stdout:
                    for line in iter(process2.stdout.readline, ''):
                        print(f"[Process2]: {line.strip()}")  # Print process2's stdout in real-time
                if process2.stderr:
                    for line in iter(process2.stderr.readline, ''):
                        print(f"[Process2 Error]: {line.strip()}")  # Print process2's stderr

            # Exit when both processes finish
            if process1.poll() is not None and process2.poll() is not None:
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure both processes are terminated if still running
        if process1 and process1.poll() is None:
            process1.terminate()
        if process2 and process2.poll() is None:
            process2.terminate()

if __name__ == "__main__":
    run_process_with_dynamic_stdout()
