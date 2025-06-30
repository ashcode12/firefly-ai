# firefly_observer.py

import os
import string
from firefly_scanner import scan_all_drives
from firefly_persona import fire_speak

def get_user_drives():
    # Windows-only for now, we’ll add cross-platform support later
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:/"
        if os.path.exists(drive):
            drives.append(drive)
    return drives

def write_log(file_list, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            for file_path in file_list:
                f.write(file_path + "\n")
        return True
    except Exception as e:
        print(f"Error writing log: {e}")
        return False

def scan_system():
    user_dirs = get_user_drives()
    log_path = os.path.join(os.getcwd(), "firefly_log.txt")
    all_files = []

    for drive in user_dirs:
        print(f"📂 Scanning {drive} ...")
        for root, dirs, files in os.walk(drive):
            if any(skip in root.lower() for skip in ["windows", "$recycle", "program files", "appdata", "system", "temp"]):
                continue
            for file in files:
                if file.lower().endswith(('.pdf', '.epub', '.mobi', '.txt', '.docx', '.csv')):
                    full_path = os.path.join(root, file)
                    all_files.append(full_path)

    success = write_log(all_files, log_path)
    return log_path if success else None

# For CLI use
if __name__ == "__main__":
    fire_speak()
    results = scan_system()
    if results:
        print(f"\n✅ Scan complete. Log written to: {results}")
        from firefly_brain import read_log_and_classify
        read_log_and_classify()
    else:
        print("❌ Failed to write scan log.")
