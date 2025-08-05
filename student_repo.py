import csv
import json


class Student:
    def __init__(self):
        self.students = {}

    # fetch data for a student
    def get_student(self, student_id):
        return self.students.get(student_id, None)

    # 1. Register a new student
    def register_student(self, student_id, name, batch):
        if student_id in self.students:
            print("Student already exists.")
            return
        self.students[student_id] = {
            "name": name,
            "batch": batch,
            "attendance": {"total_days": 0, "present_days": 0},
            "terms": {},
        }

    # 2. Add term result
    def add_term_result(self, student_id, term_name, subject_marks_dict):
        student = self.get_student(student_id)
        if not student:
            print("Student not found.")
            return 0
        student["terms"][term_name] = subject_marks_dict
        print(f"Added results for {term_name} to {student_id}.")

    # 3. Update subject mark
    def update_subject_mark(self, student_id, term, subject, new_mark):
        student = self.get_student(student_id)
        if not student:
            print("Student not found.")
            return
        if term not in student["terms"]:
            print("Term not found for update.")
            return
        if subject not in student["terms"][term]:
            print("Subject not found for update.")
            return
        student["terms"][term][subject] = new_mark
        print(f"Updated {subject} in {term} for {student_id} to {new_mark}.")

    # 4. Record attendance
    def record_attendance(self, student_id, present_days, total_days):
        student = self.get_student(student_id)
        if not student:
            print("Student not found.")
            return
        student["attendance"]["present_days"] += present_days
        student["attendance"]["total_days"] += total_days
        print(f"Attendance recorded for {student_id}.")

    # 5. Calculate average marks
    def calculate_average(self, student_id):
        student = self.get_student(student_id)
        if not student:
            return 0
        terms = student["terms"]
        print(terms)
        all_marks = []
        for term in terms.values():
            for mark in term.values():
                all_marks.append(mark)
        print(all_marks)
        if all_marks:
            average = sum(all_marks) / len(all_marks)
            return round(average, 2)
        else:
            return 0

    # 6. Attendance percentage
    def calculate_attendance_percentage(self, student_id):
        student = self.get_student(student_id)
        if not student:
            print("Student not found.")
            return 0
        attendance = student["attendance"]
        if attendance["total_days"] == 0:
            return 0
        return round((attendance["present_days"] / attendance["total_days"]) * 100, 2)

    # 7. Get topper by term
    def get_topper_by_term(self, term):
        top_student = None
        top_average = 0
        for student_id, student in self.students.items():
            if term in student["terms"]:
                average = self.calculate_average(student_id)
                if average > top_average:
                    top_average = average
                    top_student = student_id
        return top_student, top_average if top_student else (None, 0)

    # 8.rank_students_by_overall_average
    def rank_students_by_overall_average(self, batch):
        ranked_students = []
        for student_id, student in self.students.items():
            if student["batch"] == batch:
                average = self.calculate_average(student_id)
                ranked_students.append((student_id, average))
        ranked_students.sort(key=lambda x: x[1], reverse=True)
        return ranked_students

    # 9.generate_student_report
    def generate_student_report(self, student_id):
        student = self.get_student(student_id)
        if not student:
            print("Student not found.")
            return
        report = f"Report for {student['name']} (ID: {student_id})\n"
        report += f"Batch: {student['batch']}\n"
        report += "Attendance:\n"
        report += f"  Total Days: {student['attendance']['total_days']}\n"
        report += f"  Present Days: {student['attendance']['present_days']}\n"
        report += "Terms:\n"
        for term, subjects in student["terms"].items():
            report += f"  {term}:\n"
            for subject, mark in subjects.items():
                report += f"    {subject}: {mark}\n"
        print(report)

    # 10. export_data_to_json
    def export_data_to_json(self, filename):
        with open(filename, "w") as f:
            json.dump(self.students, f, indent=4)

    # 11. import_data_from_json
    def import_data_from_json(self, filename):
        try:
            with open(filename, "r") as f:
                self.students = json.load(f)
        except FileNotFoundError:
            print(f"File {filename} not found.")

    # 12. Final report
    def finalreport(self, student_id):
        student = self.get_student(student_id)
        if not student:
            print("Student not found.")
            return

        report = f"Student Report: {student['name']} ({student_id})\n"
        report += f"Batch: {student['batch']}\n"
        attendance_pct = self.calculate_attendance_percentage(student_id)
        report += f"Attendance: {attendance_pct}%\n"

        # Term averages
        for term, subjects in student["terms"].items():
            if subjects:
                avg = round(sum(subjects.values()) / len(subjects), 2)
                report += f"{term} Average: {avg}\n"

        # Overall average
        overall_avg = self.calculate_average(student_id)
        report += f"Overall Average: {overall_avg}\n"

        # Top performer for each term
        for term in student["terms"]:
            topper, avg = self.get_topper_by_term(term)
            if topper:
                report += f"Top Performer: {topper} in {term} with {avg} average\n"

        print(report)

    # 13. Export students to CSV as list of lists
    def export_students_to_csv_dict(self):
        fieldnames = [
            "Student ID",
            "Name",
            "Batch",
            "Term",
            "Subject",
            "Marks",
            "Total Days",
            "Present Days",
        ]
        rows = []
        for student_id, student in self.students.items():
            name = student["name"]
            batch = student["batch"]
            attendance = student.get("attendance", {"total_days": 0, "present_days": 0})
            terms = student.get("terms", {})
            for term_name, subjects in terms.items():
                for subject, marks in subjects.items():
                    row = {
                        "Student ID": student_id,
                        "Name": name,
                        "Batch": batch,
                        "Term": term_name,
                        "Subject": subject,
                        "Marks": marks,
                        "Total Days": attendance.get("total_days", 0),
                        "Present Days": attendance.get("present_days", 0),
                    }
                    rows.append(row)
        return rows, fieldnames

    # Write to CSV properly using DictWriter
    def table_to_list(self, filename):
        rows, fieldnames = self.export_students_to_csv_dict()
        with open(f"{filename}.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print("Exported to students_list.csv")

    def export_students_grouped_to_csv(self, filename):
        with open(f"{filename}.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "Student ID",
                    "Name",
                    "Batch",
                    "Term",
                    "Subject",
                    "Marks",
                    "Total Days",
                    "Present Days",
                ]
            )

            for student_id, student_data in self.students.items():
                name = student_data["name"]
                batch = student_data["batch"]
                total_days = student_data["attendance"]["total_days"]
                present_days = student_data["attendance"]["present_days"]
                terms = student_data["terms"]

                first_row = True
                prev_term = None
                for term, subjects in terms.items():
                    for subject, marks in subjects.items():
                        row = []

                        # Student ID, Name, Batch
                        if first_row:
                            row.extend([student_id, name, batch])
                        else:
                            row.extend(["", "", ""])

                        # Term
                        if term != prev_term:
                            row.append(term)
                            prev_term = term
                        else:
                            row.append("")

                        # Subject, Marks
                        row.extend([subject, marks])

                        # Total Days, Present Days (only once per student)
                        if first_row:
                            row.extend([total_days, present_days])
                        else:
                            row.extend(["", ""])

                        writer.writerow(row)
                        first_row = False

    # 14. Menu for user interaction
    def menu(self):
        print("1. Register a new student")
        print("2. Add term result")
        print("3. Update subject mark")
        print("4. Record attendance")
        print("5. Calculate average marks")
        print("6. Calculate attendance percentage")
        print("7. Get topper by term")
        print("8. Rank students by overall average")
        print("9. Generate student report")
        print("10. Export data to JSON")
        print("11. Import data from JSON")
        print("12. Final report")
        print("13. Export students to CSV as list of lists")
        print("14. Export students grouped to CSV")
        print("q or 0. Exit")


if __name__ == "__main__":
    system = Student()
    while True:
        system.menu()
        print("Enter your choice (1-13) or 'q' or 0 to quit:")
        choice = input("Enter your choice: ")
        if choice == "1":
            student_id = input("Enter student ID: ")
            name = input("Enter student name: ")
            batch = input("Enter student batch: ")
            system.register_student(student_id, name, batch)
        elif choice == "2":
            student_id = input("Enter student ID: ")
            term_name = input("Enter term name: ")
            number = int(input("Enter number of subjects: "))
            subjects = {}
            for _ in range(number):
                subject = input("Enter subject name: ")
                mark = float(input(f"Enter mark for {subject}: "))
                subjects[subject] = mark
            system.add_term_result(student_id, term_name, subjects)
        elif choice == "3":
            student_id = input("Enter student ID: ")
            term = input("Enter term name: ")
            subject = input("Enter subject name: ")
            new_mark = float(input("Enter new mark: "))
            system.update_subject_mark(student_id, term, subject, new_mark)
        elif choice == "4":
            student_id = input("Enter student ID: ")
            present_days = int(input("Enter number of present days: "))
            total_days = int(input("Enter number of total days: "))
            system.record_attendance(student_id, present_days, total_days)
        elif choice == "5":
            student_id = input("Enter student ID: ")
            avg = system.calculate_average(student_id)
            print(f"Average marks for {student_id}: {avg}")
        elif choice == "6":
            student_id = input("Enter student ID: ")
            percentage = system.calculate_attendance_percentage(student_id)
            print(f"Attendance percentage for {student_id}: {percentage}%")
        elif choice == "7":
            term = input("Enter term name: ")
            topper, avg = system.get_topper_by_term(term)
            if topper:
                print(f"Topper for {term}: {topper} with average {avg}")
            else:
                print("No topper found for this term.")
        elif choice == "8":
            batch = input("Enter batch: ")
            ranks = system.rank_students_by_overall_average(batch)
            print("Rankings:")
            for i, (student_id, avg) in enumerate(ranks, 1):
                print(f"{i}. {student_id} - {avg}")
        elif choice == "9":
            student_id = input("Enter student ID: ")
            system.generate_student_report(student_id)
        elif choice == "10":
            filename = input("Enter filename to export to: ")
            system.export_data_to_json(filename)
            print("Data exported.")
        elif choice == "11":
            filename = input("Enter filename to import from: ")
            system.import_data_from_json(filename)
            print("Data imported.")
        elif choice == "12":
            student_id = input("Enter student ID for final report: ")
            system.finalreport(student_id)
            print("Final report generated.")
        elif choice == "13":
            filename = input("Enter filename to export to (list format): ")
            system.table_to_list(filename)
            print("Data exported in list format.")
        elif choice == "14":
            filename = input("Enter filename to export grouped data: ")
            system.export_students_grouped_to_csv(filename)
            print("Grouped data exported.")
        elif choice.lower() == "q" or choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
