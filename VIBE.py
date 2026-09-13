"""Student Grade Calculator."""

from pathlib import Path


FILE_NAME = "student_grades.txt"


class Student:
	"""Store a student's identifying information and calculated grade."""

	def __init__(self, name, student_id, test1, test2, test3):
		self.name = name
		self.student_id = student_id
		self.test1 = test1
		self.test2 = test2
		self.test3 = test3
		self.average = (test1 + test2 + test3) / 3
		self.grade = self.calculate_grade()

	def calculate_grade(self):
		if self.average >= 90:
			return "A"
		if self.average >= 80:
			return "B"
		if self.average >= 70:
			return "C"
		if self.average >= 60:
			return "D"
		return "F"

	def to_file_line(self):
		return (
			f"{self.name}|{self.student_id}|{self.test1:.2f}|"
			f"{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}\n"
		)


def read_input(prompt):
	"""Read input and treat the escape character as a request to exit."""
	value = input(prompt)
	if value == "\x1b":
		raise KeyboardInterrupt
	return value.strip()


def get_score(test_name):
	while True:
		try:
			score = float(read_input(f"{test_name} score (0-100): "))
			if 0 <= score <= 100:
				return score
			print("Please enter a score from 0 to 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students):
	print("\nAdd Student")
	name = read_input("Student name: ")
	student_id = read_input("Student ID: ")
	if not name or not student_id:
		print("Name and student ID are required.")
		return

	student = Student(
		name,
		student_id,
		get_score("Test 1"),
		get_score("Test 2"),
		get_score("Test 3"),
	)
	students.append(student)
	print(f"Added {student.name}. Average: {student.average:.2f}, Grade: {student.grade}")


def display_students(students):
	if not students:
		print("\nNo student records found.")
		return

	print("\nStudent Records")
	print("-" * 95)
	print(
		f"{'Name':<22}{'ID':<15}{'Test 1':>10}{'Test 2':>10}"
		f"{'Test 3':>10}{'Average':>12}{'Grade':>8}"
	)
	print("-" * 95)
	for student in students:
		print(
			f"{student.name:<22.22}{student.student_id:<15.15}"
			f"{student.test1:>10.2f}{student.test2:>10.2f}"
			f"{student.test3:>10.2f}{student.average:>12.2f}"
			f"{student.grade:>8}"
		)
	print("-" * 95)


def display_statistics(students):
	if not students:
		print("\nNo student records found.")
		return

	averages = [student.average for student in students]
	highest = max(students, key=lambda student: student.average)
	lowest = min(students, key=lambda student: student.average)
	print("\nClass Statistics")
	print(f"Highest average: {highest.average:.2f} ({highest.name})")
	print(f"Lowest average:  {lowest.average:.2f} ({lowest.name})")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_student(students):
	search_name = read_input("\nEnter a student name to search: ").lower()
	matches = [student for student in students if search_name in student.name.lower()]
	if matches:
		display_students(matches)
	else:
		print(f"No students found matching '{search_name}'.")


def save_students(students, file_name=FILE_NAME):
	try:
		with Path(file_name).open("w", encoding="utf-8") as file:
			file.writelines(student.to_file_line() for student in students)
		print(f"Saved {len(students)} student record(s) to {file_name}.")
	except OSError as error:
		print(f"Could not save student records: {error}")


def load_students(file_name=FILE_NAME):
	students = []
	path = Path(file_name)
	if not path.exists():
		return students

	try:
		with path.open("r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				fields = line.rstrip("\n").split("|", 6)
				if len(fields) != 7:
					print(f"Skipping invalid record on line {line_number}.")
					continue
				name, student_id, test1, test2, test3, _average, _grade = fields
				students.append(
					Student(name, student_id, float(test1), float(test2), float(test3))
				)
	except (OSError, ValueError) as error:
		print(f"Could not load student records: {error}")
	return students


def show_menu():
	print("\nStudent Grade Calculator")
	print("1. Add student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search for a student")
	print("5. Save records")
	print("6. Exit")
	print("Press ESC to exit.")


def main():
	students = load_students()
	if students:
		print(f"Loaded {len(students)} student record(s) from {FILE_NAME}.")

	while True:
		try:
			show_menu()
			choice = read_input("Choose an option: ")
			if choice == "1":
				add_student(students)
			elif choice == "2":
				display_students(students)
			elif choice == "3":
				display_statistics(students)
			elif choice == "4":
				search_student(students)
			elif choice == "5":
				save_students(students)
			elif choice == "6":
				save_students(students)
				print("Goodbye!")
				break
			else:
				print("Please choose an option from 1 to 6, or press ESC.")
		except KeyboardInterrupt:
			print("\nExiting program.")
			save_students(students)
			break


if __name__ == "__main__":
	main()