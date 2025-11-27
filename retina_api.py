#!/usr/bin/env python3

import subprocess
import json

API_BASE = "https://api.result.retinabd.org"

def fetch_basic_info(roll, mobile):
    try:
        result = subprocess.run([
            'curl', '-s', '-G',
            '--data-urlencode', f'Roll={roll}',
            '--data-urlencode', f'Mobile={mobile}',
            f'{API_BASE}/basic-info'
        ], capture_output=True, text=True)
        return result.stdout
    except:
        return "Authentication failed"

def fetch_results(roll, mobile):
    try:
        result = subprocess.run([
            'curl', '-s', '-G',
            '--data-urlencode', f'Roll={roll}',
            '--data-urlencode', f'Mobile={mobile}',
            f'{API_BASE}/results'
        ], capture_output=True, text=True)
        return result.stdout
    except:
        return "Authentication failed"