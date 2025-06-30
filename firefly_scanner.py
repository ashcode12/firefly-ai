import os
import platform
from datetime import datetime
from pathlib import Path

# === Configuration ===
INTERESTING_EXTENSIONS = [
    ".pdf", ".epub", ".txt", ".docx", ".md", ".html", ".mobi", ".djvu"
]

EXCLUDED_FOLDERS = [
    "Windows", "Program Files", "Program Files (x86)", "AppData", "System Volume Information",
    "node_modules", "__pycache__", "Library", "Applications", "usr", "bin", "tmp", "proc"
]

LOG_PATH = Path(__file__).parent / "firefly_log.txt"

def is_interesting(file: Path) -> bool:
    return file.suffix.lower() in INTERESTING_EXTENSIONS

def is_excluded_folder(path: Path) -> bool:
    return any(part in EXCLUDED_FOLDERS for part in path.parts)

def scan_folder(folder: Path, results: list):
    try:
        for entry in folder.iterdir():
            if entry.is_dir() and not is_excluded_folder(entry):
                scan_folder(entry, results)
            elif entry.is_file() and is_interesting(entry):
                results.append({
                    "name": entry.name,
                    "path": str(entry),
                    "size_kb": round(entry.stat().st_size / 1024, 2),
                    "created": datetime.fromtimestamp(entry.stat().st_ctime).isoformat()
                })
    except (PermissionError, FileNotFoundError):
        pass

def scan_all_drives():
    system = platform.system()
    drives = []

    if system == "Windows":
        from string import ascii_uppercase
        drives = [f"{d}:/" for d in ascii_uppercase if os.path.exists(f"{d}:/")]
    else:
        drives = ["/"] + [f"/mnt/{d}" for d in os.listdir("/mnt")]

    print("🔍 Firefly is scanning for interesting files...")
    all_results = []
    for drive in drives:
        print(f"📂 Scanning {drive} ...")
        scan_folder(Path(drive), all_results)

    write_log(all_results)
    return all_results

def write_log(results: list):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        for entry in results:
            f.write(f"{entry['name']} | {entry['size_kb']} KB | {entry['created']} | {entry['path']}\n")
