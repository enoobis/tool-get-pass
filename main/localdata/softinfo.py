import pkg_resources
import subprocess
import os

def get_installed_packages():
    installed_packages = []
    for package in pkg_resources.working_set:
        installed_packages.append({
            'Package Name': package.project_name,
            'Version': package.version,
        })
    return installed_packages

def get_pip_list():
    try:
        # Get the output of 'pip list' command
        result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
        pip_list_output = result.stdout.strip()
        return pip_list_output
    except Exception as e:
        print(f"Error while getting pip list: {e}")
        return ''

def main():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_directory, 'software_info.txt')

    installed_packages = get_installed_packages()
    pip_list_output = get_pip_list()

    with open(output_file, 'w') as file:
        file.write("------ Installed Packages ------\n")
        for package in installed_packages:
            file.write(f"{package['Package Name']} ({package['Version']})\n")

        file.write("\n------ pip list Output ------\n")
        file.write(pip_list_output)

    print(f"Software information saved to {output_file}")

if __name__ == "__main__":
    main()