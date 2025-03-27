#!/usr/bin/env python3
import re
from collections import defaultdict
import argparse
import sys

PATTERNS = {
    'SQL Injection': re.compile(r'.*?(union.*select|select.*from|insert into|drop table|1=1).*?', re.I),
    'XSS': re.compile(r'.*?(<script>|alert\(|onerror=|onload=).*?', re.I),
    'Path Traversal': re.compile(r'.*?(\.\./|\.\.\\|/etc/passwd).*?'),
    'Brute Force': re.compile(r'.*?(POST /wp-login|POST /admin/login).*?'),
    'LFI/RFI': re.compile(r'.*?(include\(|require\(|php://filter).*?', re.I)
}

def analyze_log(file_path):
    results = defaultdict(list)
    
    try:
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                for attack_type, pattern in PATTERNS.items():
                    if pattern.search(line):
                        results[attack_type].append((line_num, line.strip()))
                        
        return results
    
    except FileNotFoundError:
        print(f"[!] Файл {file_path} не найден")
        sys.exit(1)

def print_results(results):
    if not results:
        print("[+] Подозрительных запросов не обнаружено")
        return
        
    print("\n[!] ОБНАРУЖЕНЫ ПОДОЗРИТЕЛЬНЫЕ ЗАПРОСЫ:\n")
    for attack_type, entries in results.items():
        print(f"=== {attack_type.upper()} ===")
        for line_num, line in entries[:3]:  
            print(f"Строка {line_num}: {line[:100]}...")
        print(f"Всего найдено: {len(entries)}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Анализатор логов веб-сервера')
    parser.add_argument('file', help='Путь к файлу лога (access.log/error.log)')
    args = parser.parse_args()
    
    print(f"[*] Анализируем файл {args.file}...")
    suspicious_requests = analyze_log(args.file)
    print_results(suspicious_requests)
