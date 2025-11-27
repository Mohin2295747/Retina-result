#!/bin/bash

# RETINA Result Fetcher - Termux Script
# Main controller script

# Colors for UI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Configuration
DATA_FILE="retina_students.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Pretty print functions
print_header() {
    echo -e "${PURPLE}"
    echo "╔════════════════════════════════════════╗"
    echo "║        RETINA RESULT FETCHER          ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Import Python functions
add_student() {
    python3 "${SCRIPT_DIR}/retina_data.py" add_student "$DATA_FILE"
}

get_student_list() {
    python3 "${SCRIPT_DIR}/retina_data.py" get_student_list "$DATA_FILE"
}

show_my_result() {
    python3 "${SCRIPT_DIR}/retina_display.py" show_my_result "$DATA_FILE"
}

show_others_result() {
    python3 "${SCRIPT_DIR}/retina_display.py" show_others_result "$DATA_FILE"
}

show_full_result() {
    python3 "${SCRIPT_DIR}/retina_display.py" show_full_result "$DATA_FILE"
}

compare_results() {
    python3 "${SCRIPT_DIR}/retina_compare.py" compare_all "$DATA_FILE"
}

compare_latest_x_exams() {
    python3 "${SCRIPT_DIR}/retina_compare.py" compare_latest "$DATA_FILE"
}

search_mode() {
    python3 "${SCRIPT_DIR}/retina_data.py" search_mode "$DATA_FILE"
}

edit_members() {
    python3 "${SCRIPT_DIR}/retina_data.py" edit_members "$DATA_FILE"
}

refresh_all_students() {
    python3 "${SCRIPT_DIR}/retina_refresh.py" refresh_all "$DATA_FILE"
}

refresh_single_student() {
    python3 "${SCRIPT_DIR}/retina_refresh.py" refresh_single "$DATA_FILE"
}

# Initialize data file if it doesn't exist
initialize_data_file() {
    if [ ! -f "$DATA_FILE" ]; then
        echo '[]' > "$DATA_FILE"
    fi
}

refresh_student_menu() {
    while true; do
        clear
        print_header
        echo -e "${WHITE}Refresh Student Data${NC}"
        echo
        echo -e "${WHITE}1. ${GREEN}Refresh All Students${NC}"
        echo -e "${WHITE}2. ${GREEN}Refresh Single Student${NC}"
        echo -e "${WHITE}0. ${RED}Back to Main Menu${NC}"
        echo
        
        read -p "Choose option: " choice
        
        case $choice in
            1) refresh_all_students ;;
            2) refresh_single_student ;;
            0) return ;;
            *) print_error "Invalid option" ;;
        esac
        
        echo
        read -p "Press Enter to continue..."
    done
}

# Check dependencies
check_dependencies() {
    for cmd in curl python3; do
        command -v $cmd &> /dev/null || {
            print_error "$cmd is required but not installed. Install with: pkg install $cmd"
            exit 1
        }
    done
    
    # Check if Python modules exist
    for py_file in retina_data.py retina_api.py retina_display.py retina_compare.py retina_refresh.py; do
        if [ ! -f "${SCRIPT_DIR}/${py_file}" ]; then
            print_error "Missing Python file: ${py_file}"
            exit 1
        fi
    done
}

# Main menu
main_menu() {
    while true; do
        clear
        print_header
        echo -e "${WHITE}1. ${GREEN}Add New Student${NC}"
        echo -e "${WHITE}2. ${GREEN}Your Result (Recent 3)${NC}"
        echo -e "${WHITE}3. ${GREEN}Compare Results (All Exams)${NC}"
        echo -e "${WHITE}4. ${GREEN}Compare Latest X Exams${NC}"
        echo -e "${WHITE}5. ${GREEN}Other's Result${NC}"
        echo -e "${WHITE}6. ${GREEN}Search Mode${NC}"
        echo -e "${WHITE}7. ${GREEN}Full Result${NC}"
        echo -e "${WHITE}8. ${GREEN}Edit Members${NC}"
        echo -e "${WHITE}9. ${GREEN}Refresh Student Data${NC}"
        echo -e "${WHITE}0. ${RED}Exit${NC}"
        echo
        
        read -p "Choose option: " option
        
        case $option in
            1) add_student ;;
            2) show_my_result ;;
            3) compare_results ;;
            4) compare_latest_x_exams ;;
            5) show_others_result ;;
            6) search_mode ;;
            7) show_full_result ;;
            8) edit_members ;;
            9) refresh_student_menu ;;
            0) echo -e "${GREEN}Goodbye!${NC}"; exit 0 ;;
            *) print_error "Invalid option" ;;
        esac
        
        echo
        read -p "Press Enter to continue..."
    done
}

# Main execution
main() {
    check_dependencies
    initialize_data_file
    main_menu
}

# Run the script
main