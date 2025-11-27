#!/usr/bin/env python3

import json
import sys
import re
from retina_api import fetch_basic_info, fetch_results

def add_student(data_file):
    print("Adding New Student")
    print()
    
    nickname = input("Enter nickname: ")
    roll = input("Enter roll number: ")
    mobile = input("Enter mobile number: ")
    
    print("Fetching student information...")
    
    basic_info = fetch_basic_info(roll, mobile)
    
    if "Authentication failed" in basic_info:
        print("Authentication failed with provided credentials")
        return
    
    # Extract all fields from the API response
    try:
        data = json.loads(basic_info)
        name = data.get('Name', '')
        mobile2 = data.get('Mobile2', '')
        batch = data.get('Batch', '')
        college = data.get('College', '')
        ssc = data.get('SSC', '')
        hsc = data.get('HSC', '')
    except:
        # If JSON parsing fails, try regex extraction
        name_match = re.search(r'Name[^:]*:\s*\"([^\"]+)\"', basic_info)
        name = name_match.group(1) if name_match else ''
        
        mobile2_match = re.search(r'Mobile2[^:]*:\s*\"?([0-9]+)\"?', basic_info)
        mobile2 = mobile2_match.group(1) if mobile2_match else ''
        
        batch_match = re.search(r'Batch[^:]*:\s*\"([^\"]+)\"', basic_info)
        batch = batch_match.group(1) if batch_match else ''
        
        college_match = re.search(r'College[^:]*:\s*\"([^\"]+)\"', basic_info)
        college = college_match.group(1) if college_match else ''
        
        ssc_match = re.search(r'SSC[^:]*:\s*([0-9.]+)', basic_info)
        ssc = ssc_match.group(1) if ssc_match else ''
        
        hsc_match = re.search(r'HSC[^:]*:\s*([0-9.]+)', basic_info)
        hsc = hsc_match.group(1) if hsc_match else ''
    
    if not name:
        print("Could not fetch student information")
        return
    
    print("Student information fetched successfully!")
    
    # Add to data file
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
    except:
        data = []
    
    new_student = {
        'nickname': nickname,
        'roll': roll,
        'mobile': mobile,
        'mobile2': mobile2,
        'name': name,
        'batch': batch,
        'college': college,
        'ssc': ssc,
        'hsc': hsc
    }
    data.append(new_student)
    
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Student '{nickname}' added successfully!")
    
    if mobile2:
        print(f"Alternative mobile number found: {mobile2}")

def get_student_list(data_file):
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        for i, student in enumerate(data, 1):
            print(f"{i}. {student['nickname']} (Roll: {student['roll']})")
    except:
        print('')

def get_student_by_index(data_file, index):
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        if index <= len(data):
            student = data[index-1]
            return student
    except:
        pass
    return None

def get_all_students(data_file):
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
        return data
    except:
        return []

def search_mode(data_file):
    print("Search Mode")
    print()
    
    search_mobile = input("Enter mobile number: ")
    roll_prefix = input("Enter roll prefix (e.g., 911): ")
    start_range = int(input("Enter start range (e.g., 105): "))
    end_range = int(input("Enter end range (e.g., 999): "))
    
    print(f"Searching from roll {roll_prefix}{start_range} to {roll_prefix}{end_range}...")
    
    found = False
    for i in range(start_range, end_range + 1):
        roll = f"{roll_prefix}{i:03d}"
        print(f"Trying roll: {roll}", end='\r')
        
        basic_info = fetch_basic_info(roll, search_mobile)
        
        if "Authentication failed" not in basic_info:
            print(f"\nFound matching roll: {roll}")
            found = True
            
            # Extract student data
            try:
                data = json.loads(basic_info)
                name = data.get('Name', '')
                mobile2 = data.get('Mobile2', '')
                batch = data.get('Batch', '')
                college = data.get('College', '')
                ssc = data.get('SSC', '')
                hsc = data.get('HSC', '')
            except:
                name_match = re.search(r'Name[^:]*:\s*\"([^\"]+)\"', basic_info)
                name = name_match.group(1) if name_match else ''
                
                mobile2_match = re.search(r'Mobile2[^:]*:\s*\"?([0-9]+)\"?', basic_info)
                mobile2 = mobile2_match.group(1) if mobile2_match else ''
                
                batch_match = re.search(r'Batch[^:]*:\s*\"([^\"]+)\"', basic_info)
                batch = batch_match.group(1) if batch_match else ''
                
                college_match = re.search(r'College[^:]*:\s*\"([^\"]+)\"', basic_info)
                college = college_match.group(1) if college_match else ''
                
                ssc_match = re.search(r'SSC[^:]*:\s*([0-9.]+)', basic_info)
                ssc = ssc_match.group(1) if ssc_match else ''
                
                hsc_match = re.search(r'HSC[^:]*:\s*([0-9.]+)', basic_info)
                hsc = hsc_match.group(1) if hsc_match else ''
            
            print(f"Name: {name}")
            print(f"Roll: {roll}")
            print(f"Batch: {batch}")
            print(f"College: {college}")
            print(f"SSC GPA: {ssc}")
            print(f"HSC GPA: {hsc}")
            
            add_choice = input("Add this student? (y/n): ").lower()
            if add_choice == 'y':
                nickname = input("Enter nickname (press enter to use full name): ").strip()
                if not nickname:
                    nickname = name
                
                try:
                    with open(data_file, 'r') as f:
                        data = json.load(f)
                except:
                    data = []
                
                new_student = {
                    'nickname': nickname,
                    'roll': roll,
                    'mobile': search_mobile,
                    'mobile2': mobile2,
                    'name': name,
                    'batch': batch,
                    'college': college,
                    'ssc': ssc,
                    'hsc': hsc
                }
                data.append(new_student)
                
                with open(data_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                print("Student added successfully!")
            break
    
    if not found:
        print("\nNo matching student found in the specified range.")

def edit_members(data_file):
    print("Edit Members")
    print()
    
    students = get_all_students(data_file)
    if not students:
        print("No students found to edit.")
        return
    
    print("Select student to edit:")
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
    
    old_student = students[choice-1]
    
    print(f"\nEditing: {old_student['nickname']} (Roll: {old_student['roll']})")
    print()
    
    nickname = input(f"Enter new nickname [{old_student['nickname']}]: ").strip()
    roll = input(f"Enter new roll [{old_student['roll']}]: ").strip()
    mobile = input(f"Enter new mobile [{old_student['mobile']}]: ").strip()
    
    if not nickname:
        nickname = old_student['nickname']
    if not roll:
        roll = old_student['roll']
    if not mobile:
        mobile = old_student['mobile']
    
    print("Re-fetching student information...")
    basic_info = fetch_basic_info(roll, mobile)
    
    if "Authentication failed" in basic_info:
        print("Could not verify new credentials. Keeping old basic info.")
        name = old_student['name']
        mobile2 = old_student['mobile2']
        ssc = old_student.get('ssc', '')
        hsc = old_student.get('hsc', '')
        batch = ''
        college = ''
    else:
        try:
            data = json.loads(basic_info)
            name = data.get('Name', old_student['name'])
            mobile2 = data.get('Mobile2', old_student['mobile2'])
            batch = data.get('Batch', '')
            college = data.get('College', '')
            ssc = data.get('SSC', old_student.get('ssc', ''))
            hsc = data.get('HSC', old_student.get('hsc', ''))
        except:
            name = old_student['name']
            mobile2 = old_student['mobile2']
            ssc = old_student.get('ssc', '')
            hsc = old_student.get('hsc', '')
            batch = ''
            college = ''
    
    students[choice-1] = {
        'nickname': nickname,
        'roll': roll,
        'mobile': mobile,
        'mobile2': mobile2,
        'name': name,
        'batch': batch,
        'college': college,
        'ssc': ssc,
        'hsc': hsc
    }
    
    with open(data_file, 'w') as f:
        json.dump(students, f, indent=2)
    
    print("Student information updated successfully!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 retina_data.py <function> <data_file>")
        sys.exit(1)
    
    function_name = sys.argv[1]
    data_file = sys.argv[2]
    
    if function_name == "add_student":
        add_student(data_file)
    elif function_name == "get_student_list":
        get_student_list(data_file)
    elif function_name == "search_mode":
        search_mode(data_file)
    elif function_name == "edit_members":
        edit_members(data_file)