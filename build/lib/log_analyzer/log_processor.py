import json
from collections import Counter
import ipaddress
import os

def process_log_files(file_paths, options):
    combined_results = {
        "text": "",
        "json": {}
    }

    for file_path in file_paths:
        if not os.path.isfile(file_path):
            print(f"Error: File {file_path} does not exist.")
            continue

        try:
            with open(file_path, 'r') as f:
                logs = f.readlines()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            continue

        if not logs:
            print(f"Warning: File {file_path} is empty.")
            continue

        try:
            # first and last timestamps
            first_log = logs[0].strip().split()
            last_log = logs[-1].strip().split()

            # Handle the case where logs might be malformed or missing
            if len(first_log) < 10 or len(last_log) < 10:
                print(f"Warning: Malformed log entries in {file_path}. Skipping file.")
                continue

            first_timestamp = float(first_log[0])
            last_timestamp = float(last_log[0])

            # Correct the duration to always be positive - if log file is written from top or bottom... access.log is for example written 
            if first_timestamp > last_timestamp:
                first_timestamp, last_timestamp = last_timestamp, first_timestamp

            parsed_logs = parse_logs(logs)
            result = analyze_logs(parsed_logs, first_timestamp, last_timestamp, options)
            combined_results['text'] += f"Results for {file_path}:\n{result['text']}\n"
            combined_results['json'][file_path] = result['json']

        except ValueError as e:
            print(f"Error processing timestamps in {file_path}: {e}")
        except Exception as e:
            print(f"Unexpected error processing {file_path}: {e}")

    return combined_results

def parse_logs(logs):
    parsed_logs = []
    for line in logs:
        parts = line.split()
        if len(parts) < 10:
            print(f"Warning: Malformed log line skipped: {line.strip()}")
            continue  # Skip malformed lines

        try:
            parsed_log = {
                'timestamp': float(parts[0]),
                'response_header_size': int(parts[1]),
                'client_ip': parts[2],
                'http_response': parts[3],
                'response_size': int(parts[4]),
                'http_method': parts[5],
                'url': parts[6],
                'username': parts[7],
                'access_type': parts[8],
                'response_type': parts[9] if len(parts) > 9 else "-"
            }
            parsed_logs.append(parsed_log)
        except ValueError as e:
            print(f"Warning: Skipping log line due to parsing error: {line.strip()} - {e}")
            continue

    return parsed_logs

def is_local_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private or ip_obj.is_loopback
    except ValueError:
        print(f"Warning: Invalid IP address encountered: {ip}")
        return False

def analyze_logs(parsed_logs, first_timestamp, last_timestamp, options):
    ip_counter = Counter()
    total_bytes = 0
    total_events = len(parsed_logs)

    total_duration_seconds = last_timestamp - first_timestamp

    if options.eps:
        if total_duration_seconds > 0:
            events_per_second = total_events / total_duration_seconds
        else:
            events_per_second = 0
        text_output = [f"Average EPS: {events_per_second:.6f}"]
        json_output = {'events_per_second': events_per_second}
    else:
        text_output = []
        json_output = {}

    # Filter logs for --mfip and --lfip
    filtered_events = 0
    for log in parsed_logs:
        ip = log['client_ip']

        # local ip filter
        if options.ignore_local_ip and is_local_ip(ip):
            continue

        filtered_events += 1
        bytes_exchanged = log['response_size']

        ip_counter[ip] += 1
        total_bytes += bytes_exchanged

    if options.mfip:
        if ip_counter:
            mf_ip, mf_count = ip_counter.most_common(1)[0]
            text_output.append(f"Most Frequent IP: {mf_ip} with {mf_count} occurrences")
            json_output['most_frequent_ip'] = {"ip": mf_ip, "count": mf_count}
        else:
            text_output.append("No IPs found to determine the most frequent IP.")
            json_output['most_frequent_ip'] = None

    if options.lfip:
        if ip_counter:
            min_count = min(ip_counter.values())
            least_frequent_ips = [ip for ip, count in ip_counter.items() if count == min_count]
            text_output.append(f"Least Frequent IPs (each seen {min_count} times): {', '.join(least_frequent_ips)}")
            json_output['least_frequent_ips'] = {"ips": least_frequent_ips, "count": min_count}
        else:
            text_output.append("No IPs found to determine the least frequent IP.")
            json_output['least_frequent_ips'] = None

    if options.bytes:
        text_output.append(f"Total Bytes Exchanged: {total_bytes}")
        json_output['total_bytes_exchanged'] = total_bytes

    return {
        "text": "\n".join(text_output),
        "json": json_output
    }
