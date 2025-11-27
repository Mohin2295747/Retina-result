#!/usr/bin/env python3

import json
import sys
from datetime import datetime
from retina_api import fetch_results
from retina_data import get_all_students

# Color codes
WHITE = '\033[1;37m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
CYAN = '\033[0;36m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def compare_all(data_file):
    print("Compare Results (All Exams)")
    print()
    
    students_data = get_all_students(data_file)
    if not students_data:
        print("No students found to compare")
        return
    
    # Step 1: Collect ALL exam names from ALL students in correct order
    print("Collecting all exam names...")
    all_exam_entries = []
    exam_name_set = set()

    for student in students_data:
        results_json = fetch_results(student['roll'], student['mobile'])
        if "Authentication failed" in results_json and student['mobile2']:
            results_json = fetch_results(student['roll'], student['mobile2'])
        
        if "Authentication failed" not in results_json:
            try:
                exams = json.loads(results_json)
                # Sort by date (most recent first)
                sorted_exams = sorted(exams, key=lambda x: datetime.strptime(x.get('Date', '01/01/2000'), '%d/%m/%Y'), reverse=True)
                
                for exam in sorted_exams:
                    subject = exam.get('Subject', 'N/A')
                    date = exam.get('Date', 'N/A')
                    exam_key = (subject, date)
                    
                    if exam_key not in exam_name_set:
                        exam_name_set.add(exam_key)
                        all_exam_entries.append(exam_key)
            except:
                pass

    if not all_exam_entries:
        print("No exam data found")
        return

    # Step 2: Collect marks for all students for all exams
    print("Collecting marks for all students...")
    all_student_results = {}
    student_names = []

    for student in students_data:
        nickname = student['nickname']
        print(f"Fetching results for {nickname}...")
        student_names.append(nickname)
        
        # Initialize with all exams as absent
        student_exams = {exam[0]: 'A' for exam in all_exam_entries}
        
        results_json = fetch_results(student['roll'], student['mobile'])
        if "Authentication failed" in results_json and student['mobile2']:
            results_json = fetch_results(student['roll'], student['mobile2'])
        
        if "Authentication failed" not in results_json:
            try:
                exams = json.loads(results_json)
                # Sort by date (most recent first)
                sorted_exams = sorted(exams, key=lambda x: datetime.strptime(x.get('Date', '01/01/2000'), '%d/%m/%Y'), reverse=True)
                
                for exam in sorted_exams:
                    subject = exam.get('Subject', 'N/A')
                    mark = exam.get('Mark', 0)
                    # Update the mark for this exam
                    student_exams[subject] = mark
                    
            except Exception as e:
                print(f"Error processing results for {nickname}: {e}")
        
        all_student_results[nickname] = student_exams

    # Step 3: Display comparison table
    print("Generating comparison table...")

    # Calculate column widths
    max_exam_width = max(len(exam[0]) for exam in all_exam_entries) if all_exam_entries else 20
    max_exam_width = min(max_exam_width, 35)
    max_name_width = max(len(name) for name in student_names) if student_names else 10
    max_name_width = min(max_name_width, 15)

    # Calculate table width
    table_width = max_exam_width + 3 + (max_name_width + 3) * len(student_names) + 1
    table_width = max(table_width, 70)

    # Print table header
    print(f"{CYAN}╔{'═' * table_width}╗{NC}")
    title = 'ALL EXAMS COMPARISON (Website Order)'
    padding = (table_width - len(title)) // 2
    print(f"{CYAN}║{' ' * padding}{title}{' ' * (table_width - padding - len(title))}║{NC}")
    print(f"{CYAN}╠{'═' * max_exam_width}╬{'═' * (table_width - max_exam_width - 1)}╣{NC}")

    # Print student names header
    header = f"║ {WHITE}{'EXAM':<{max_exam_width}}{NC} ║"
    for name in student_names:
        header += f" {WHITE}{name[:max_name_width]:<{max_name_width}}{NC} ║"
    print(f"{CYAN}{header}{NC}")

    print(f"{CYAN}╠{'═' * max_exam_width}╬{'═' * (table_width - max_exam_width - 1)}╣{NC}")

    # Print exam rows
    for exam_subject, exam_date in all_exam_entries:
        exam_display = exam_subject
        if len(exam_display) > max_exam_width:
            exam_display = exam_display[:max_exam_width-3] + '...'
        
        row = f"║ {YELLOW}{exam_display:<{max_exam_width}}{NC} ║"
        
        # Find max mark for this exam
        max_mark = 0
        for name in student_names:
            mark = all_student_results[name].get(exam_subject, 'A')
            if mark != 'A':
                try:
                    mark_val = float(mark)
                    if mark_val > max_mark:
                        max_mark = mark_val
                except:
                    pass
        
        for name in student_names:
            mark = all_student_results[name].get(exam_subject, 'A')
            if mark == 'A':
                row += f" {RED}{'A':<{max_name_width}}{NC} ║"
            elif float(mark) == max_mark and max_mark > 0:
                row += f" {GREEN}{str(mark):<{max_name_width}}{NC} ║"
            else:
                row += f" {WHITE}{str(mark):<{max_name_width}}{NC} ║"
        
        print(f"{CYAN}{row}{NC}")

    print(f"{CYAN}╚{'═' * max_exam_width}╩{'═' * (table_width - max_exam_width - 1)}╝{NC}")
    print()
    print(f"{YELLOW}Legend:{NC} {GREEN}Highest Mark{NC} | {RED}A = Absent{NC}")
    print(f"{CYAN}Note: Showing {len(all_exam_entries)} exams in website order{NC}")

def compare_latest(data_file):
    print("Compare Latest X Exams")
    print()
    
    students_data = get_all_students(data_file)
    if not students_data:
        print("No students found to compare")
        return
    
    try:
        x_count = int(input("Enter number of latest exams to compare (X): "))
        if x_count < 1:
            print("Please enter a valid positive number")
            return
    except:
        print("Please enter a valid positive number")
        return
    
    # Step 1: Collect all unique exams from all students
    print("Collecting exam data from all students...")
    all_exams_set = set()

    for student in students_data:
        results_json = fetch_results(student['roll'], student['mobile'])
        if "Authentication failed" in results_json and student['mobile2']:
            results_json = fetch_results(student['roll'], student['mobile2'])
        
        if "Authentication failed" not in results_json:
            try:
                exams = json.loads(results_json)
                for exam in exams:
                    subject = exam.get('Subject', 'N/A')
                    date = exam.get('Date', 'N/A')
                    all_exams_set.add((subject, date))
            except:
                pass

    if not all_exams_set:
        print("No exam data found")
        return

    # Sort all exams by date (most recent first) and take top X
    all_exams_sorted = sorted(all_exams_set, 
                             key=lambda x: datetime.strptime(x[1], '%d/%m/%Y'), 
                             reverse=True)
    latest_x_exams = all_exams_sorted[:x_count]

    # Get just the subject names for the latest X exams
    latest_x_subjects = [exam[0] for exam in latest_x_exams]

    # Step 2: Collect marks for all students for latest X exams
    print(f"Collecting marks for latest {x_count} exams...")
    all_student_results = {}
    student_names = []

    for student in students_data:
        nickname = student['nickname']
        print(f"Fetching results for {nickname}...")
        student_names.append(nickname)
        
        # Initialize with all latest exams as absent
        student_exams = {subject: 'A' for subject in latest_x_subjects}
        
        results_json = fetch_results(student['roll'], student['mobile'])
        if "Authentication failed" in results_json and student['mobile2']:
            results_json = fetch_results(student['roll'], student['mobile2'])
        
        if "Authentication failed" not in results_json:
            try:
                exams = json.loads(results_json)
                # Sort by date (most recent first)
                sorted_exams = sorted(exams, key=lambda x: datetime.strptime(x.get('Date', '01/01/2000'), '%d/%m/%Y'), reverse=True)
                
                # Take only the latest X exams for this student
                student_latest_exams = sorted_exams[:x_count]
                
                for exam in student_latest_exams:
                    subject = exam.get('Subject', 'N/A')
                    mark = exam.get('Mark', 0)
                    # Update the mark for this exam
                    if subject in student_exams:
                        student_exams[subject] = mark
                    
            except Exception as e:
                print(f"Error processing results for {nickname}: {e}")
        
        all_student_results[nickname] = student_exams

    # Step 3: Display comparison table
    print("Generating comparison table...")

    # Calculate column widths
    max_exam_width = max(len(subject) for subject in latest_x_subjects) if latest_x_subjects else 20
    max_exam_width = min(max_exam_width, 35)
    max_name_width = max(len(name) for name in student_names) if student_names else 10
    max_name_width = min(max_name_width, 15)

    # Calculate table width
    table_width = max_exam_width + 3 + (max_name_width + 3) * len(student_names) + 1
    table_width = max(table_width, 70)

    # Print table header
    print(f"{CYAN}╔{'═' * table_width}╗{NC}")
    title = f'LATEST {x_count} EXAMS COMPARISON (Latest to Oldest)'
    padding = (table_width - len(title)) // 2
    print(f"{CYAN}║{' ' * padding}{title}{' ' * (table_width - padding - len(title))}║{NC}")
    print(f"{CYAN}╠{'═' * max_exam_width}╬{'═' * (table_width - max_exam_width - 1)}╣{NC}")

    # Print student names header
    header = f"║ {WHITE}{'EXAM':<{max_exam_width}}{NC} ║"
    for name in student_names:
        header += f" {WHITE}{name[:max_name_width]:<{max_name_width}}{NC} ║"
    print(f"{CYAN}{header}{NC}")

    print(f"{CYAN}╠{'═' * max_exam_width}╬{'═' * (table_width - max_exam_width - 1)}╣{NC}")

    # Print exam rows in latest to oldest order
    for i, subject in enumerate(latest_x_subjects, 1):
        exam_display = subject
        if len(exam_display) > max_exam_width:
            exam_display = exam_display[:max_exam_width-3] + '...'
        
        # Add numbering to show order
        numbered_display = f"{i}. {exam_display}"
        if len(numbered_display) > max_exam_width:
            numbered_display = numbered_display[:max_exam_width-3] + '...'
        
        row = f"║ {YELLOW}{numbered_display:<{max_exam_width}}{NC} ║"
        
        # Find max mark for this exam
        max_mark = 0
        for name in student_names:
            mark = all_student_results[name].get(subject, 'A')
            if mark != 'A':
                try:
                    mark_val = float(mark)
                    if mark_val > max_mark:
                        max_mark = mark_val
                except:
                    pass
        
        for name in student_names:
            mark = all_student_results[name].get(subject, 'A')
            if mark == 'A':
                row += f" {RED}{'A':<{max_name_width}}{NC} ║"
            elif float(mark) == max_mark and max_mark > 0:
                row += f" {GREEN}{str(mark):<{max_name_width}}{NC} ║"
            else:
                row += f" {WHITE}{str(mark):<{max_name_width}}{NC} ║"
        
        print(f"{CYAN}{row}{NC}")

    print(f"{CYAN}╚{'═' * max_exam_width}╩{'═' * (table_width - max_exam_width - 1)}╝{NC}")
    print()
    print(f"{YELLOW}Legend:{NC} {GREEN}Highest Mark{NC} | {RED}A = Absent{NC}")
    print(f"{CYAN}Note: Numbers indicate order (1 = Latest, {len(latest_x_subjects)} = Oldest){NC}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 retina_compare.py <function> <data_file>")
        sys.exit(1)
    
    function_name = sys.argv[1]
    data_file = sys.argv[2]
    
    if function_name == "compare_all":
        compare_all(data_file)
    elif function_name == "compare_latest":
        compare_latest(data_file)