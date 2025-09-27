import csv
import time
import psutil
from student import Student


def current_time():
    return time.perf_counter()


def memory_usage():
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)


def load_students(filename):
    start = current_time()
    print(f"[INFO] Loading students from {filename}...")
    students = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append(Student(row["id"], row["name"], row["age"], row["grade"]))
    duration = current_time() - start
    print(f"[INFO] Loaded {len(students)} students in {duration:.6f} seconds.")
    return students, duration


def save_students(filename, students):
    start = current_time()
    print(f"[INFO] Saving {len(students)} students to {filename}...")
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "age", "grade"])
        writer.writeheader()
        for s in students:
            writer.writerow(s.to_dict())
    duration = current_time() - start
    print(f"[INFO] File {filename} saved successfully in {duration:.6f} seconds.")
    return duration


def search_students(students, name):
    print(f"[INFO] Searching for students with name containing '{name}'...")
    result = [s for s in students if name.lower() in s.name.lower()]
    print(f"[INFO] Found {len(result)} matching students.")
    return result


def sort_students(students, key="name"):
    start = current_time()
    print(f"[INFO] Sorting students by '{key}'...")
    sorted_list = sorted(students, key=lambda s: getattr(s, key))
    duration = current_time() - start
    print(f"[INFO] Sorting complete in {duration:.6f} seconds.")
    return sorted_list, duration
