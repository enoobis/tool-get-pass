import psutil
import platform
import cpuinfo
import os

def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    return {
        'CPU Model': info['brand_raw'],
        'CPU Cores': psutil.cpu_count(logical=False),
        'Total Threads': psutil.cpu_count(logical=True),
        'CPU Usage (%)': psutil.cpu_percent(interval=1, percpu=True),
    }

def get_memory_info():
    virtual_memory = psutil.virtual_memory()
    return {
        'Total Memory (GB)': round(virtual_memory.total / (1024**3), 2),
        'Available Memory (GB)': round(virtual_memory.available / (1024**3), 2),
        'Used Memory (GB)': round(virtual_memory.used / (1024**3), 2),
        'Memory Usage (%)': virtual_memory.percent,
    }

def get_disk_info():
    disk_info = []
    partitions = psutil.disk_partitions(all=True)
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                'Mount Point': partition.mountpoint,
                'File System Type': partition.fstype,
                'Total Size (GB)': round(usage.total / (1024**3), 2),
                'Used Size (GB)': round(usage.used / (1024**3), 2),
                'Free Size (GB)': round(usage.free / (1024**3), 2),
                'Disk Usage (%)': usage.percent,
            })
        except PermissionError:
            # Skip inaccessible drives
            continue
    return disk_info

def get_network_info():
    interfaces = psutil.net_if_addrs()
    network_info = {}
    for interface, addresses in interfaces.items():
        address_info = []
        for address in addresses:
            address_info.append({
                'Address Family': address.family.name,
                'Address': address.address,
                'Netmask': address.netmask,
            })
        network_info[interface] = address_info
    return network_info

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        return {
            'Battery Percentage': battery.percent,
            'Power Plugged': battery.power_plugged,
        }
    return {}

def get_system_uptime():
    uptime = psutil.boot_time()
    return {
        'System Uptime (hours)': round((psutil.time.time() - uptime) / 3600, 2),
    }

def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_directory, 'info.txt')

    with open(output_file, 'w') as file:
        file.write("------ PC Information ------\n")

        system_info = {
            'System': platform.system(),
            'Release': platform.release(),
            'Version': platform.version(),
            'Machine': platform.machine(),
            'Processor': platform.processor(),
        }
        for key, value in system_info.items():
            file.write(f"{key}: {value}\n")

        cpu_info = get_cpu_info()
        memory_info = get_memory_info()
        disk_info = get_disk_info()
        network_info = get_network_info()
        battery_info = get_battery_info()
        system_uptime = get_system_uptime()

        file.write("\n------ CPU Information ------\n")
        for key, value in cpu_info.items():
            file.write(f"{key}: {value}\n")

        file.write("\n------ Memory Information ------\n")
        for key, value in memory_info.items():
            file.write(f"{key}: {value}\n")

        file.write("\n------ Disk Information ------\n")
        for disk in disk_info:
            for key, value in disk.items():
                file.write(f"{key}: {value}\n")
            file.write('\n')

        file.write("\n------ Network Information ------\n")
        for interface, addresses in network_info.items():
            file.write(f"Interface: {interface}\n")
            for address in addresses:
                for key, value in address.items():
                    file.write(f"{key}: {value}\n")
            file.write('\n')

        if battery_info:
            file.write("\n------ Battery Information ------\n")
            for key, value in battery_info.items():
                file.write(f"{key}: {value}\n")
            file.write('\n')

        file.write("\n------ System Uptime ------\n")
        for key, value in system_uptime.items():
            file.write(f"{key}: {value}\n")

        file.write("\n------ Running Processes ------\n")
        processes = psutil.process_iter(['pid', 'name', 'username'])
        for process in processes:
            try:
                info = process.info
                file.write(f"PID: {info['pid']}, Name: {info['name']}, Username: {info['username']}\n")
            except psutil.NoSuchProcess:
                continue

    print("PC information saved to pc_info.txt")

if __name__ == "__main__":
    main()
