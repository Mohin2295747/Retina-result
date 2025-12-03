Retina Result Fetcher

<div align="center">

.github/logo/retina_logo.svg

A comprehensive result management system for Retina Medical Coaching Centre, Bangladesh

https://img.shields.io/badge/Termux-000000?style=for-the-badge&logo=termux&logoColor=white
https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge

</div>

📋 Overview

Retina Result Fetcher is a powerful command-line tool designed specifically for students of Retina Medical Coaching Centre in Bangladesh. This system allows students to easily fetch, compare, and analyze their exam results directly from the official Retina result portal using their Termux terminal on Android devices.

✨ Features

📊 Result Management

· Individual Results: View your recent 3 exams or full result history
· Student Comparison: Compare results across multiple students
· Latest Exams Analysis: Compare the latest X exams between students
· Full History: Access complete exam records with detailed statistics

🔍 Student Database

· Easy Student Addition: Add students using roll number and mobile
· Auto-Discovery: Search mode to find students by roll number range
· Multi-Mobile Support: Automatic fallback to secondary mobile numbers
· Data Refresh: Update student information from the official portal

🎨 Visual Interface

· Color-coded Output: Easy-to-read terminal interface with colors
· Formatted Tables: Beautiful comparison tables with proper alignment
· Progress Indicators: Real-time feedback during operations
· Professional UI: Box-drawing characters for clean presentation

🔄 Data Management

· JSON Storage: Structured data storage in JSON format
· Edit Capabilities: Modify existing student information
· Bulk Operations: Refresh all students or individual records
· Backup Friendly: Easy to backup and restore student data

📁 File Structure

```
Retina/
├── retina.sh              # Main controller script (Bash)
├── retina_api.py          # API interaction with Retina portal
├── retina_data.py         # Student data management
├── retina_display.py      # Result display functions
├── retina_compare.py      # Comparison utilities
├── retina_refresh.py      # Data refresh functions
├── retina_students.json   # Student database (auto-generated)
└── .github/logo/
    └── retina_logo.svg    # Retina coaching centre logo
```

🚀 Installation

Prerequisites

· Termux installed on your Android device
· Active internet connection
· Retina student credentials (roll number and registered mobile)

Step-by-Step Setup

1. Install Termux from F-Droid or Google Play Store
2. Update Termux packages:

```bash
pkg update && pkg upgrade
```

1. Install required dependencies:

```bash
pkg install python curl git
```

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Retina.git
cd Retina
```

1. Make the main script executable:

```bash
chmod +x retina.sh
```

1. Run the application:

```bash
./retina.sh
```

📖 Usage Guide

Main Menu Options

Option Description Command
1. Add New Student Add a student using roll number and mobile python3 retina_data.py add_student retina_students.json
2. Your Result (Recent 3) View your recent 3 exam results python3 retina_display.py show_my_result retina_students.json
3. Compare Results (All Exams) Compare all students across all exams python3 retina_compare.py compare_all retina_students.json
4. Compare Latest X Exams Compare latest X exams between students python3 retina_compare.py compare_latest retina_students.json
5. Other's Result View another student's recent results python3 retina_display.py show_others_result retina_students.json
6. Search Mode Find students by roll number range python3 retina_data.py search_mode retina_students.json
7. Full Result View complete exam history of a student python3 retina_display.py show_full_result retina_students.json
8. Edit Members Modify existing student information python3 retina_data.py edit_members retina_students.json
9. Refresh Student Data Update student info from Retina portal python3 retina_refresh.py refresh_all retina_students.json
0. Exit Exit the application -

🎯 Quick Start

1. First, add yourself:
   · Select option 1 from main menu
   · Enter your nickname (e.g., "John")
   · Enter your roll number (e.g., "911105")
   · Enter your registered mobile number
2. View your results:
   · Select option 2 to see your recent 3 exams
   · Select option 7 to see your complete history
3. Add friends for comparison:
   · Use option 1 to add friends manually
   · Or use option 6 (Search Mode) to find by roll range
4. Compare performance:
   · Use option 3 to compare all exams
   · Use option 4 to compare latest exams

🔧 Technical Details

API Integration

The system communicates with the official Retina result portal (api.result.retinabd.org) using:

· Authentication: Roll number + Mobile number
· Endpoints: /basic-info and /results
· Data Format: JSON responses
· Fallback: Automatic secondary mobile number support

Data Structure

Student Object:

```json
{
  "nickname": "John",
  "roll": "911105",
  "mobile": "017XXXXXXXX",
  "mobile2": "019XXXXXXXX",
  "name": "John Doe",
  "batch": "2023",
  "college": "Medical College",
  "ssc": "5.00",
  "hsc": "5.00"
}
```

Exam Result Object:

```json
{
  "Subject": "Anatomy Model Test 1",
  "Mark": "85",
  "N": "2",
  "GPAScore": "4.5",
  "Position": "15",
  "CentralPosition": "150",
  "Date": "15/01/2024"
}
```

Color Scheme

· Green: Highest marks, successful operations
· Red: Absent marks, errors
· Yellow: Exam names, warnings
· Cyan: Table borders, headers
· White: Normal text, regular marks
· Blue: Information messages

📊 Comparison Features

All Exams Comparison

· Shows every exam taken by any student
· Maintains website order (most recent first)
· Highlights highest marks in green
· Shows "A" for absent students in red

Latest X Exams Comparison

· User specifies number of latest exams
· Shows exams in chronological order (1 = latest)
· Useful for tracking recent performance trends
· Numbers indicate exam sequence

🔒 Security & Privacy

· No Data Upload: All data stays on your device
· Local Storage: Student data stored in local JSON file
· No Internet Required after initial setup (except for fetching results)
· Mobile Number Security: Numbers are stored locally only

🛠️ Advanced Usage

Direct Python Script Usage

Each module can be used independently:

```bash
# Add a student
python3 retina_data.py add_student retina_students.json

# View your results
python3 retina_display.py show_my_result retina_students.json

# Compare all students
python3 retina_compare.py compare_all retina_students.json
```

Custom Data File

Use a different data file:

```bash
./retina.sh --data custom_data.json
```

Backup Your Data

```bash
cp retina_students.json retina_students_backup.json
```

❓ Frequently Asked Questions

Q: Is this official Retina software?

A: No, this is a third-party tool created to help students access and analyze their results more easily.

Q: Do I need to pay for this?

A: No, this tool is completely free and open-source.

Q: Is my data safe?

A: Yes, all data is stored locally on your device. No information is sent to any server except the official Retina portal for authentication.

Q: What if I change my mobile number?

A: Use the "Edit Members" option to update your mobile number.

Q: Can I use this on Windows/Mac?

A: The scripts are written in Python and should work on any platform with Python 3.8+, but the main script (retina.sh) is designed for Termux/Linux.

🐛 Troubleshooting

Common Issues:

1. "Authentication failed" error
   · Check your roll number and mobile number
   · Ensure you're using the registered mobile number
   · Try using the secondary mobile number if available
2. "curl not found" error
   · Install curl: pkg install curl
3. "python3 not found" error
   · Install Python: pkg install python
4. Permission denied
   · Make script executable: chmod +x retina.sh
5. No internet connection
   · Ensure you have active internet
   · Check if Retina portal is accessible

🤝 Contributing

We welcome contributions! Here's how you can help:

1. Report Bugs: Open an issue with detailed information
2. Suggest Features: Share your ideas for improvements
3. Code Contributions: Fork the repo and submit pull requests
4. Documentation: Help improve documentation and translations

Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/Retina.git

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

· Retina Medical Coaching Centre for providing the result portal
· Termux community for the amazing Android terminal emulator
· All contributors and testers from the Retina student community

📞 Support

For support, please:

1. Check the FAQ section
2. Open an issue on GitHub
3. Contact the developer through the repository

🏥 About Retina Medical Coaching Centre

Retina is a premier medical coaching centre in Bangladesh, dedicated to helping students prepare for medical entrance examinations. With experienced faculty and comprehensive study materials, Retina has been guiding aspiring medical students for years.

---

<div align="center">

Made with ❤️ for Retina students

Disclaimer: This tool is not officially affiliated with Retina Medical Coaching Centre. Use at your own discretion.

⬆ Back to Top

</div>
