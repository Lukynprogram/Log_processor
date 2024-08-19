import argparse
import json
from log_analyzer.log_processor import process_log_files

def main():
    parser = argparse.ArgumentParser(description="Log Analyzer Tool")
    parser.add_argument('input', nargs='+', help='Path to one or more input log files')
    parser.add_argument('--output', help='Path to save output (either text or JSON)')
    parser.add_argument('--format', choices=['txt', 'json'], default='txt', help='Output format: txt or json')
    parser.add_argument('--mfip', action='store_true', help='Most frequent IP')
    parser.add_argument('--lfip', action='store_true', help='Least frequent IP')
    parser.add_argument('--eps', action='store_true', help='Events per second')
    parser.add_argument('--bytes', action='store_true', help='Total bytes exchanged')
    parser.add_argument('--ignore-local-ip', action='store_true', help='Ignore local IP addresses (Class A, B, C, and localhost)')

    args = parser.parse_args()
    results = process_log_files(args.input, args)

    # Handle the output based on the format and output arguments
    if args.output:
        if args.format == 'txt':
            with open(args.output, 'w') as f:
                f.write(results['text'])
        elif args.format == 'json':
            with open(args.output, 'w') as f:
                json.dump(results['json'], f, indent=4)
    else:
        if args.format == 'txt':
            print(results['text'])
        elif args.format == 'json':
            print(json.dumps(results['json'], indent=4))

if __name__ == "__main__":
    main()
