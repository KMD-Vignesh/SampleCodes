import subprocess
import time

def run_process_with_dynamic_stdout():
    # Paths to your files
    pytest_automation_file = "test\\automation.py"
    pytest_html_report = "test\\pytest_report.html"
    output_command = "--capture=tee-sys --tb=no"

    # Start the first process (your .bat file)
    process1 = subprocess.Popen(
        ["test\\file_watcher.bat"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True  # Ensure `shell=True` for Windows bat files
    )

    # Start the second process (pytest command)
    process2 = subprocess.Popen(
        f"pytest -v {pytest_automation_file} --html={pytest_html_report} --self-contained-html {output_command}",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True  # Required for string commands
    )

    try:
        while True:
            # Poll each process to check their status
            process1_status = process1.poll()
            process2_status = process2.poll()

            # Log output from process1 (if running)
            if process1_status is None and process1.stdout:
                line = process1.stdout.readline()
                if line:
                    print(f"[Process1]: {line.strip()}")
            
            # Log error output from process1
            if process1.stderr:
                error = process1.stderr.readline()
                if error:
                    print(f"[Process1 Error]: {error.strip()}")

            # Log output from process2 (if running)
            if process2_status is None and process2.stdout:
                line = process2.stdout.readline()
                if line:
                    print(f"[Process2]: {line.strip()}")
            
            # Log error output from process2
            if process2.stderr:
                error = process2.stderr.readline()
                if error:
                    print(f"[Process2 Error]: {error.strip()}")

            # Exit the loop if both processes are done
            if process1_status is not None and process2_status is not None:
                break

            # Small delay to avoid overloading the CPU
            time.sleep(0.1)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up processes
        if process1 and process1.poll() is None:
            process1.terminate()
        if process2 and process2.poll() is None:
            process2.terminate()

if __name__ == "__main__":
    run_process_with_dynamic_stdout()
