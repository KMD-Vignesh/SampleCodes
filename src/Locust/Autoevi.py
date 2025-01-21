import asyncio
import subprocess

async def run_continuous_polling_command(command, label):
    """
    Runs a continuous polling process and captures stdout in real-time.
    """
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        text=True
    )
    while True:
        # Read a single line of stdout
        line = await process.stdout.readline()
        if not line:
            break
        print(f"[{label}] {line.strip()}")  # Print with a label

async def run_periodic_loop_command(command, label):
    """
    Runs a periodic process that starts, pauses, and restarts.
    """
    while True:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            text=True
        )
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            print(f"[{label}] {line.strip()}")
        
        await asyncio.sleep(5)  # Pause for 5 seconds before restarting the loop

async def main():
    # Commands to execute
    continuous_command = ["cmd", "/c", "ping localhost -t"]  # Continuous polling
    periodic_command = ["cmd", "/c", "for /L %x in (1,1,10) do echo %x"]  # Looped command

    # Run both commands concurrently
    await asyncio.gather(
        run_continuous_polling_command(continuous_command, "Polling Cmd"),
        run_periodic_loop_command(periodic_command, "Periodic Cmd")
    )

if __name__ == "__main__":
    asyncio.run(main())