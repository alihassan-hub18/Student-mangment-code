import json
import os


class Student:

  def __init__(self, student_id, name, age, grade_level, marks):
    self.student_id = student_id
    self.name = name
    self.age = int(age)
    self.grade_level = grade_level
    self.marks = float(marks)  # Percentage or GPA score
    self.status = self.calculate_status()

  def calculate_status(self):
    if self.marks >= 80:
      return "Honor Roll (A)"
    elif self.marks >= 60:
      return "Passing (B)"
    elif self.marks >= 40:
      return "Needs Improvement (C)"
    else:
      return "Failing (F)"

  def to_dict(self):
    return {
        "student_id": self.student_id,
        "name": self.name,
        "age": self.age,
        "grade_level": self.grade_level,
        "marks": self.marks,
        "status": self.status,
    }


class StudentManagementSystem:

  def __init__(self, filename="students_data.json"):
    self.filename = filename
    self.students = []
    self.load_data()

  def load_data(self):
    """Loads student records from a local JSON file."""
    if os.path.exists(self.filename):
      try:
        with open(self.filename, "r") as file:
          self.students = json.load(file)
      except json.JSONDecodeError:
        self.students = []

  def save_data(self):
    """Saves current student records to a local JSON file."""
    with open(self.filename, "w") as file:
      json.dump(self.students, file, indent=4)

  def add_student(self):
    print("\n" + "-" * 50)
    print("             REGISTER NEW STUDENT")
    print("-" * 50)
    
    # Auto-generate unique ID based on existing count
    student_id = f"STU-{len(self.students) + 101:03d}"
    
    name = input("Enter student's full name: ").strip()
    if not name:
      print("\033[91m[-] Name cannot be empty.\033[0m")
      return

    try:
      age = int(input("Enter age: "))
      if age < 5 or age > 100:
        print("\033[91m[-] Please enter a realistic age.\033[0m")
        return
    except ValueError:
      print("\033[91m[-] Invalid input for age.\033[0m")
      return

    grade_level = input("Enter grade/class level (e.g., 10th Grade, Sophomore): ").strip()

    try:
      marks = float(input("Enter overall percentage/score (0-100): "))
      if not (0 <= marks <= 100):
        print("\033[91m[-] Marks must be between 0 and 100.\033[0m")
        return
    except ValueError:
      print("\033[91m[-] Invalid input for marks.\033[0m")
      return

    new_student = Student(student_id, name, age, grade_level, marks)
    self.students.append(new_student.to_dict())
    self.save_data()

    print(f"\033[92m[+] Student registered successfully! ID Assigned: {student_id}\033[0m")
    print("-" * 50)

  def view_students(self):
    print("\n" + "=" * 80)
    print("                              STUDENT DIRECTORY")
    print("=" * 80)
    if not self.students:
      print("  (No student records found!)")
    else:
      print(f"{'ID':<10} {'Name':<20} {'Age':<6} {'Grade':<15} {'Marks':<8} {'Status'}")
      print("-" * 80)
      for s in self.students:
        print(
            f"{s['student_id']:<10} {s['name']:<20} {s['age']:<6}"
            f" {s['grade_level']:<15} {s['marks']:<7.1f}% {s['status']}"
        )
    print("=" * 80)

  def search_student(self):
    print("\n" + "-" * 50)
    query = input("Enter student ID or name to search: ").strip().lower()
    print("-" * 50)

    found = [
        s for s in self.students 
        if query in s['student_id'].lower() or query in s['name'].lower()
    ]

    if not found:
      print("\033[91m[-] No matching student records found.\033[0m")
    else:
      print(f"\033[92m[+] Found {len(found)} matching record(s):\033[0m")
      for s in found:
        print(f" -> ID: {s['student_id']} | Name: {s['name']} | Grade: {s['grade_level']} | Marks: {s['marks']}% | Status: {s['status']}")
    print("-" * 50)

  def delete_student(self):
    print("\n" + "-" * 50)
    target_id = input("Enter student ID to remove (e.g., STU-101): ").strip().upper()
    
    initial_count = len(self.students)
    self.students = [s for s in self.students if s['student_id'] != target_id]

    if len(self.students) < initial_count:
      self.save_data()
      print(f"\033[92m[+] Student ID {target_id} successfully removed from the system.\033[0m")
    else:
      print(f"\033[91m[-] Student ID {target_id} not found.\033[0m")
    print("-" * 50)


def main():
  sms = StudentManagementSystem()

  while True:
    print("\n" + "=" * 50)
    print("             STUDENT MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. View All Students")
    print("2. Register New Student")
    print("3. Search Student")
    print("4. Delete Student Record")
    print("5. Exit")
    print("=" * 50)

    choice = input("Choose an option (1-5): ").strip()

    if choice == "1":
      sms.view_students()
    elif choice == "2":
      sms.add_student()
    elif choice == "3":
      sms.search_student()
    elif choice == "4":
      sms.delete_student()
    elif choice == "5":
      print(
          "\n\033[92mSaving records securely... Exiting Student Management"
          " System. Have a great day!\033[0m\n"
      )
      break
    else:
      print("\n\033[91m[-] Invalid choice. Please select between 1 and 5.\033[0m")


if __name__ == "__main__":
  main()