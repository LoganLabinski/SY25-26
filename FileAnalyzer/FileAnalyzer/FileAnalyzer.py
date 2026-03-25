import glob

# Get all .txt files in the directory
files = glob.glob("server_dump/*.txt")

status_counts = {"OK": 0, "WARN": 0, "ERROR": 0}
status_files = {"OK": [], "WARN": [], "ERROR": []}

for file in files:
    with open(file, "r") as f:
        content = f.read()
        for status in status_counts.keys():
            if status in content:
                status_counts[status] += 1
                status_files[status].append(file)
                break

print("Status counts:")
for status, count in status_counts.items():
    print(f"{status}: {count}")

choice = input("Do you want to print file names for a specific status? (OK/WARN/ERROR, or 'n' to skip): ").strip().upper()
if choice in status_files:
    print(f"\nFiles with status {choice}:")
    for file in status_files[choice]:
        print(file)
elif choice != "N":
    print("Invalid choice. No files printed.")