from screeninfo import get_monitors
import os

def get_display_resolution(primary_monitor):
    resolution = primary_monitor.width, primary_monitor.height
    return resolution

def get_available_monitors():
    return [monitor.name for monitor in get_monitors()]

def get_monitor_configuration():
    monitor_configurations = []
    for monitor in get_monitors():
        configuration = {
            'Monitor': monitor.name,
            'Position (x, y)': (monitor.x, monitor.y),
            'Size (width, height)': (monitor.width, monitor.height),
            'Is Primary': monitor.is_primary,
        }
        monitor_configurations.append(configuration)
    return monitor_configurations

def save_display_information(output_file, display_resolution, available_monitors, monitor_configurations):
    with open(output_file, 'w') as file:
        file.write("------ Display Information ------\n")
        file.write(f"Primary Monitor Resolution: {display_resolution[0]}x{display_resolution[1]}\n")
        file.write("Available Monitors:\n")
        for monitor in available_monitors:
            file.write(f" - {monitor}\n")
        file.write("\nMonitor Configurations:\n")
        for config in monitor_configurations:
            file.write(f"Monitor: {config['Monitor']}\n")
            file.write(f"Position (x, y): {config['Position (x, y)']}\n")
            file.write(f"Size (width, height): {config['Size (width, height)']}\n")
            file.write(f"Is Primary: {config['Is Primary']}\n")
            file.write('\n')

def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_directory, 'disinfo.txt')

    primary_monitor = get_monitors()[0]
    display_resolution = get_display_resolution(primary_monitor)
    available_monitors = get_available_monitors()
    monitor_configurations = get_monitor_configuration()

    save_display_information(output_file, display_resolution, available_monitors, monitor_configurations)

    print(f"Display information saved to {output_file}")

if __name__ == "__main__":
    main()