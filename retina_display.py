#!/usr/bin/env python3

import json
import sys
from datetime import datetime
from retina_api import fetch_basic_info, fetch_results
from retina_data import get_student_by_index, get_all_students

# Color codes
WHITE = '\033[1;37m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
CYAN = '\033[0;36m'
NC = '\033[0m'

def display_basic_info(student):
    print(f"{CYAN}========= STUDENT INFO ========={NC}")
    print(f"{WHITE}Nickname:    {GREEN}{student['nickname']}{NC}")
    print(f"{WHITE}Name:        {GREEN}{student['name']}{NC}")
    print(f"{WHITE}Roll:        {GREEN}{student['roll']}{NC}")
    print(f"{WHITE}Batch:       {GREEN}{student['batch']}{NC}")
    print(f"{WHITE}College:     {GREEN}{student['college']}{NC}")
    print(f"{WHITE}SSC GPA:     {GREEN}{student.get('ssc', '')}{NC}")
    print(f"{WHITE}HSC GPA:     {GREEN}{student.get('hsc', '')}{NC}")
    print(f"{WHITE}Mobile:      {GREEN}{student['mobile']}{NC}")
    if student['mobile2']:
        print(f"{WHITE}Mobile (2):  {GREEN}{student['mobile2']}{NC}")
    print()

def display_recent_three_results(results_json):
    print(f"{CYAN}========= RECENT 3 EXAM RESULTS ========={NC}")
    
    try:
        data = json.loads(results_json)
        # Sort by date (most recent first) and take first 3
        sorted_exams = sorted(data, key=lambda x: datetime.strptime(x.get('Date', '01/01/2000'), '%d/%m/%Y'), reverse=True)
        recent_three = sorted_exams[:3]
        
        for i, exam in enumerate(reversed(recent_three), 1):
            subject = exam.get('Subject', 'N/A')
            mark = exam.get('Mark', 0)
            negative = exam.get('N', 0)
            gpa_score = exam.get('GPAScore', 'N/A')
            position = exam.get('Position', 'N/A')
            central_pos = exam.get('CentralPosition', 'N/A')
            
            print(f"{WHITE}{i}. {YELLOW}{subject}{NC}")
            print(f"{WHITE}   Mark:        {GREEN}{mark}{NC}")
            if negative and float(negative) > 0:
                print(f"{WHITE}   Negative:    {RED}{negative}{NC}")
            if gpa_score and gpa_score != 'N/A':
                print(f"{WHITE}   GPA Score:   {GREEN}{gpa_score}{NC}")
            print(f"{WHITE}   Position:    {GREEN}{position}{NC}")
            if central_pos and central_pos != 'N/A':
                print(f"{WHITE}   Central Rank:{GREEN}{central_pos}{NC}")
            print()
            
    except Exception as e:
        print(f"{RED}Error displaying results: {str(e)}{NC}")

def display_all_results(results_json):
    print(f"{CYAN}========= ALL EXAM RESULTS ========={NC}")
    
    try:
        data = json.loads(results_json)
        # Sort by date (most recent first)
        sorted_exams = sorted(data, key=lambda x: datetime.strptime(x.get('Date', '01/01/2000'), '%d/%m/%Y'), reverse=True)
        
        for i, exam in enumerate(reversed(sorted_exams), 1):
            subject = exam.get('Subject', 'N/A')
            mark = exam.get('Mark', 0)
            negative = exam.get('N', 0)
            gpa_score = exam.get('GPAScore', 'N/A')
            position = exam.get('Position', 'N/A')
            central_pos = exam.get('CentralPosition', 'N/A')
            
            print(f"{WHITE}{i}. {YELLOW}{subject}{NC}")
            print(f"{WHITE}   Mark:        {GREEN}{mark}{NC}")
            if negative and float(negative) > 0:
                print(f"{WHITE}   Negative:    {RED}{negative}{NC}")
            if gpa_score and gpa_score != 'N/A':
                print(f"{WHITE}   GPA Score:   {GREEN}{gpa_score}{NC}")
            print(f"{WHITE}   Position:    {GREEN}{position}{NC}")
            if central_pos and central_pos != 'N/A':
                print(f"{WHITE}   Central Rank:{GREEN}{central_pos}{NC}")
            print()
            
    except Exception as e:
        print(f"{RED}Error displaying results: {str(e)}{NC}")

def show_my_result(data_file):
    print("Your Result (Recent 3 Exams)")
    print()
    
    students = get_all_students(data_file)
    if not students:
        print("No students found. Please add yourself first.")
        return
    
    # Get the first student
    student = students[0]
    
    print(f"Automatically fetching results for {student['nickname']}...")
    
    # Try primary mobile first
    results = fetch_results(student['roll'], student['mobile'])
    
    if "Authentication failed" in results:
        if student['mobile2']:
            print("Primary mobile failed, trying alternative...")
            results = fetch_results(student['roll'], student['mobile2'])
        else:
            print("Authentication failed with provided mobile number")
            return
    
    if "Authentication failed" in results:
        print("Authentication failed with both mobile numbers")
        return
    
    # Get updated basic info for display
    basic_info = fetch_basic_info(student['roll'], student['mobile'])
    if "Authentication failed" in basic_info and student['mobile2']:
        basic_info = fetch_basic_info(student['roll'], student['mobile2'])
    
    try:
        data = json.loads(basic_info)
        student['batch'] = data.get('Batch', student['batch'])
        student['college'] = data.get('College', student['college'])
    except:
        pass
    
    display_basic_info(student)
    display_recent_three_results(results)

def show_others_result(data_file):
    print("Other's Result")
    print()
    
    students = get_all_students(data_file)
    if not students:
        print("No students found.")
        return
    
    print("Select student:")
    for i, student in enumerate(students, 1):
        print(f"{i}. {student['nickname']} (Roll: {student['roll']})")
    print("0. Cancel")
    
    try:
        choice = int(input("Choose: "))
        if choice == 0:
            return
        if choice < 1 or choice > len(students):
            print("Invalid selection")
            return
    except:
        print("Invalid selection")
        return
    
    student = students[choice-1]
    
    print(f"Fetching results for {student['nickname']}...")
    
    results = fetch_results(student['roll'], student['mobile'])
    if "Authentication failed" in results and student['mobile2']:
        results = fetch_results(student['roll'], student['mobile2'])
    
    if "Authentication failed" in results:
        print("Authentication failed")
        return
    
    # Get updated basic info
    basic_info = fetch_basic_info(student['roll'], student['mobile'])
    if "Authentication failed" in basic_info and student['mobile2']:
        basic_info = fetch_basic_info(student['roll'], student['mobile2'])
    
    try:
        data = json.loads(basic_info)
        student['batch'] = data.get('Batch', student['batch'])
        student['college'] = data.get('College', student['college'])
    except:
        pass
    
    display_basic_info(student)
    display_recent_three_results(results)

def show_full_result(data_file):
    print("Full Result")
    print()
    
    students = get_all_students(data_file)
    if not students:
        print("No students found.")
        return
    
    print("Select student:")
    for i, student in enumerate(students, 1):
        print(f"{i}. {student['nickname']} (Roll: {student['roll']})")
    print("0. Cancel")
    
    try:
        choice = int(input("Choose: "))
        if choice == 0:
            return
        if choice < 1 or choice > len(students):
            print("Invalid selection")
            return
    except:
        print("Invalid selection")
        return
    
    student = students[choice-1]
    
    print(f"Fetching all results for {student['nickname']}...")
    
    results = fetch_results(student['roll'], student['mobile'])
    if "Authentication failed" in results and student['mobile2']:
        results = fetch_results(student['roll'], student['mobile2'])
    
    if "Authentication failed" in results:
        print("Authentication failed")
        return
    
    # Get updated basic info
    basic_info = fetch_basic_info(student['roll'], student['mobile'])
    if "Authentication failed" in basic_info and student['mobile2']:
        basic_info = fetch_basic_info(student['roll'], student['mobile2'])
    
    try:
        data = json.loads(basic_info)
        student['batch'] = data.get('Batch', student['batch'])
        student['college'] = data.get('College', student['college'])
    except:
        pass
    
    display_basic_info(student)
    display_all_results(results)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 retina_display.py <function> <data_file>")
        sys.exit(1)
    
    function_name = sys.argv[1]
    data_file = sys.argv[2]
    
    if function_name == "show_my_result":
        show_my_result(data_file)
    elif function_name == "show_others_result":
        show_others_result(data_file)
    elif function_name == "show_full_result":
        show_full_result(data_file)