from firefly_scanner import scan_all_drives
from firefly_persona import fire_speak

if __name__ == "__main__":
    fire_speak()
    results = scan_all_drives()
    print(f"\n✅ Scan complete. {len(results)} files found.")
