import subprocess


# ---------------- CPU MONITOR ----------------
def get_cpu_usage():

    result = subprocess.run(
        ["top", "-bn1"],
        capture_output=True,
        text=True
    )

    for line in result.stdout.split("\n"):
        if "%Cpu(s)" in line:

            parts = line.split(",")

            user = parts[0].split()[1]
            system = parts[1].split()[0]
            idle = parts[3].split()[0]

            return user, system, idle

    return "0", "0", "0"


# ---------------- PROCESS MONITOR ----------------
def get_process_info():

    result = subprocess.run(
        ["ps", "aux"],
        capture_output=True,
        text=True
    )

    lines = result.stdout.strip().split("\n")[1:]

    process_list = []

    for line in lines:

        parts = line.split(None, 10)

        if len(parts) >= 11:

            user = parts[0]
            pid = parts[1]
            cpu = float(parts[2])
            mem = float(parts[3])
            command = parts[10]

            process_list.append({
                "pid": pid,
                "cpu": cpu,
                "mem": mem,
                "command": command
            })

    total = len(process_list)

    top_cpu = sorted(
        process_list,
        key=lambda x: x["cpu"],
        reverse=True
    )[:5]

    top_mem = sorted(
        process_list,
        key=lambda x: x["mem"],
        reverse=True
    )[:5]

    return total, top_cpu, top_mem


# ---------------- MAIN ----------------
def main():

    print("\n===== SYSTEM MONITOR =====\n")

    # CPU
    user, system, idle = get_cpu_usage()

    print("CPU Usage:")
    print(f"User   : {user}%")
    print(f"System : {system}%")
    print(f"Idle   : {idle}%\n")


    # Processes
    total, top_cpu, top_mem = get_process_info()

    print("Process Monitoring:")
    print(f"Total Processes: {total}\n")


    print("Top 5 Processes by CPU:")
    for p in top_cpu:
        print(f"{p['pid']} | {p['command']} | CPU: {p['cpu']}%")

    print("\nTop 5 Processes by Memory:")
    for p in top_mem:
        print(f"{p['pid']} | {p['command']} | MEM: {p['mem']}%")


if __name__ == "__main__":
    main()
