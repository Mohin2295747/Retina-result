#!/usr/bin/env python3

import json
import sys
import re
from retina_api import fetch_basic_info

def refresh_all_students(data_file):
    print("Refreshing All Students Basic Info")
    print()
    
    try:
        with open(data_file, 'r') as f:
            students = json.load(f)
    except:
        print("Error loading student data")
        return
    
    if not students:
        print("No students found to refresh.")
        return
    
    print(f"Found {len(students)} students to refresh.")
    print()
    
    updated_count = 0
    failed_count = 0
    
    for i, student in enumerate(students, 1):
        print(f"Refreshing {i}/{len(students)}: {student['nickname']} (Roll: {student['roll']})")
        
        # Try primary mobile first
        basic_info = fetch_basic_info(student['roll'], student['mobile'])
        
        if "Authentication failed" in basic_info:
            if student['mobile2']:
                print(f"  Primary mobile failed, trying alternative...")
                basic_info = fetch_basic_info(student['roll'], student['mobile2'])
            else:
                print(f"  {RED}Authentication failed with both mobile numbers{NC}")
                failed_count += 1
                continue
        
        if "Authentication failed" in basic_info:
            print(f"  {RED}Authentication failed with both mobile numbers{NC}")
            failed_count += 1
            continue
        
        # Extract updated information
        try:
            data = json.loads(basic_info)
            name = data.get('Name', student['name'])
            mobile2 = data.get('Mobile2', student['mobile2'])
            batch = data.get('Batch', student['batch'])
            college = data.get('College', student['college'])
            ssc = data.get('SSC', student.get('ssc', ''))
            hsc = data.get('HSC', student.get('hsc', ''))
        except:
            # If JSON parsing fails, try regex extraction
            name_match = re.search(r'Name[^:]*:\s*\"([^\"]+)\"', basic_info)
            name = name_match.group(1) if name_match else student['name']
            
            mobile2_match = re.search(r'Mobile2[^:]*:\s*\"?([0-9]+)\"?', basic_info)
            mobile2 = mobile2_match.group(1) if mobile2_match else student['mobile2']
            
            batch_match = re.search(r'Batch[^:]*:\s*\"([^\"]+)\"', basic_info)
            batch = batch_match.group(1) if batch_match else student['batch']
            
            college_match = re.search(r'College[^:]*:\s*\"([^\"]+)\"', basic_info)
            college = college_match.group(1) if college_match else student['college']
            
            ssc_match = re.search(r'SSC[^:]*:\s*([0-9.]+)', basic_info)
            ssc = ssc_match.group(1) if ssc_match else student.get('ssc', '')
            
            hsc_match = re.search(r'HSC[^:]*:\s*([0-9.]+)', basic_info)
            hsc = hsc_match.group(1) if hsc_match else student.get('hsc', '')
        
        # Update student data
        student['name'] = name
        student['mobile2'] = mobile2
        student['batch'] = batch
        student['college'] = college
        student['ssc'] = ssc
        student['hsc'] = hsc
        
        print(f"  {GREEN}✓ Updated: {name}{NC}")
        updated_count += 1
    
    # Save updated data
    try:
        with open(data_file, 'w') as f:
            json.dump(students, f, indent=2)
        
        print()
        print(f"{GREEN}Refresh completed!{NC}")
        print(f"Successfully updated: {updated_count} students")
        if failed_count > 0:
            print(f"Failed to update: {failed_count} students")
        
    except Exception as e:
        print(f"{RED}Error saving updated data: {e}{NC}")

def refresh_single_student(data_file):
    print("Refresh Single Student Basic Info")
    print()
    
    try:
        with open(data_file, 'r') as f:
            students = json.load(f)
    except:
        print("Error loading student data")
        return
    
    if not students:
        print("No students found.")
        return
    
    print("Select student to refresh:")
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
    
    print(f"Refreshing: {student['nickname']} (Roll: {student['roll']})")
    print()
    
    # Try primary mobile first
    basic_info = fetch_basic_info(student['roll'], student['mobile'])
    
    if "Authentication failed" in basic_info:
        if student['mobile2']:
            print("Primary mobile failed, trying alternative...")
            basic_info = fetch_basic_info(student['roll'], student['mobile2'])
        else:
            print("Authentication failed with provided mobile numbers")
            return
    
    if "Authentication failed" in basic_info:
        print("Authentication failed with both mobile numbers")
        return
    
    # Extract updated information
    try:
        data = json.loads(basic_info)
        old_name = student['name']
        name = data.get('Name', student['name'])
        mobile2 = data.get('Mobile2', student['mobile2'])
        batch = data.get('Batch', student['batch'])
        college = data.get('College', student['college'])
        ssc = data.get('SSC', student.get('ssc', ''))
        hsc = data.get('HSC', student.get('hsc', ''))
    except:
        # If JSON parsing fails, try regex extraction
        name_match = re.search(r'Name[^:]*:\s*\"([^\"]+)\"', basic_info)
        old_name = student['name']
        name = name_match.group(1) if name_match else student['name']
        
        mobile2_match = re.search(r'Mobile2[^:]*:\s*\"?([0-9]+)\"?', basic_info)
        mobile2 = mobile2_match.group(1) if mobile2_match else student['mobile2']
        
        batch_match = re.search(r'Batch[^:]*:\s*\"([^\"]+)\"', basic_info)
        batch = batch_match.group(1) if batch_match else student['batch']
        
        college_match = re.search(r'College[^:]*:\s*\"([^\"]+)\"', basic_info)
        college = college_match.group(1) if college_match else student['college']
        
        ssc_match = re.search(r'SSC[^:]*:\s*([0-9.]+)', basic_info)
        ssc = ssc_match.group(1) if ssc_match else student.get('ssc', '')
        
        hsc_match = re.search(r'HSC[^:]*:\s*([0-9.]+)', basic_info)
        hsc = hsc_match.group(1) if hsc_match else student.get('hsc', '')
    
    # Update student data
    student['name'] = name
    student['mobile2'] = mobile2
    student['batch'] = batch
    student['college'] = college
    student['ssc'] = ssc
    student['hsc'] = hsc
    
    # Save updated data
    try:
        with open(data_file, 'w') as f:
            json.dump(students, f, indent=2)
        
        print(f"{GREEN}Student information updated successfully!{NC}")
        print()
        print(f"Name: {old_name} → {name}")
        if student['mobile2'] != mobile2:
            print(f"Mobile2: {student['mobile2']} → {mobile2}")
        if student['batch'] != batch:
            print(f"Batch: {student['batch']} → {batch}")
        if student['college'] != college:
            print(f"College: {student['college']} → {college}")
        if student.get('ssc', '') != ssc:
            print(f"SSC: {student.get('ssc', '')} → {ssc}")
        if student.get('hsc', '') != hsc:
            print(f"HSC: {student.get('hsc', '')} → {hsc}")
        
    except Exception as e:
        print(f"{RED}Error saving updated data: {e}{NC}")

# Color codes for terminal output
RED = '\033[0;31m'
GREEN = '\033[0;32m'
NC = '\033[0m'

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 retina_refresh.py <function> <data_file>")
        sys.exit(1)
    
    function_name = sys.argv[1]
    data_file = sys.argv[2]
    
    if function_name == "refresh_all":
        refresh_all_students(data_file)
    elif function_name == "refresh_single":
        refresh_single_student(data_file)