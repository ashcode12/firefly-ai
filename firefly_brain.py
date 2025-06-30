import re
from pathlib import Path

LOG_PATH = Path(__file__).parent / "firefly_log.txt"
CLASSIFIED_PATH = Path(__file__).parent / "firefly_brain_output.txt"

def classify_title(filename):
    title = filename.lower()
    if any(keyword in title for keyword in ["manual", "handbook", "guide", "tutorial"]):
        return "Guide"
    elif any(keyword in title for keyword in ["article", "paper", "study"]):
        return "Article"
    elif any(keyword in title for keyword in ["novel", "book", "story", "volume"]):
        return "Book"
    elif any(keyword in title for keyword in ["notes", "lecture", "class", "lesson"]):
        return "Note"
    elif any(keyword in title for keyword in ["resume", "cv", "portfolio"]):
        return "Personal Document"
    else:
        return "Uncategorized"

def recommend_based_on_filenames(classified_files):
    books = [entry for entry in classified_files if entry["type"] == "Book"]
    if not books:
        return "🕯️ No books found to recommend yet. Feed me more stories..."

    most_common = max(set([entry["name"].split()[0] for entry in books]), key=lambda w: sum(entry["name"].startswith(w) for entry in books))
    return f"📖 You seem to like books starting with '{most_common}'. Maybe continue exploring them?"

def read_log_and_classify():
    classified = []
    if not LOG_PATH.exists():
        print("❌ No scan log found. Run firefly_observer.py first.")
        return []

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split(" | ")
        if len(parts) != 4:
            continue

        name, size_kb, created, path = parts
        file_type = classify_title(name)
        classified.append({
            "name": name,
            "type": file_type,
            "size_kb": size_kb,
            "path": path
        })

    with open(CLASSIFIED_PATH, "w", encoding="utf-8") as out:
        for entry in classified:
            out.write(f"{entry['type']:>15} | {entry['name']:<40} | {entry['size_kb']} KB | {entry['path']}\n")

    print("🧠 Classification complete.")
    print(f"📄 Output written to: {CLASSIFIED_PATH}")
    print("\n🧙 Firefly’s recommendation:")
    print(recommend_based_on_filenames(classified))

    return classified
