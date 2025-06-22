from datetime import timedelta, datetime
from argparse import ArgumentParser, ArgumentTypeError
from os import path, access, W_OK

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ArgumentTypeError(f'Invalid date: {date_str}. Please use YYYY-MM-DD format and make sure dates exist')
    
def main():
    parser = ArgumentParser(description="Generate a custom date wordlist")
    parser.add_argument('--start','-s', help='Start date in YYYY-MM-DD format', required=True, type=validate_date)
    parser.add_argument('--end','-e', help='End date in YYYY-MM-DD format', type=validate_date, default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument('--format','-f', help="Output format: (YYYYMMDD, DDMMYYYY, MMDDYYYY) or use -sep/--separator to add custom separator", choices=['YYYYMMDD', 'DDMMYYYY', 'MMDDYYYY'], required=True)
    parser.add_argument('output_file', help='Output file name')
    parser.add_argument('--separator','-sep', help='Seperator for date fields in output', default='')
    args = parser.parse_args()

    if args.start > args.end:
        parser.error('-start/-s must be before -end/-e date')

    if path.exists(args.output_file):
        if input(f"{args.output_file} already exists. Overwrite? (y/n) ").lower() == 'n':
            exit()

    if not access(args.output_file, W_OK):
        parser.error(f"Cannot write to {args.output_file}. Insufficient permissions")

    startDate = args.start
    endDate = args.end
    oneDay = timedelta(days=1)

    match args.format:
        case 'YYYYMMDD':
            output_format = f"%Y{args.separator}%m{args.separator}%d"
        case 'DDMMYYYY': 
            output_format =  f"%d{args.separator}%m{args.separator}%Y"
        case 'MMDDYYYY':
            output_format =  f"%m{args.separator}%d{args.separator}%Y"


    with open(args.output_file, 'w') as file:
        currentDate = startDate
        while currentDate <= endDate:
            file.write(currentDate.strftime(output_format) + '\n')
            currentDate += oneDay

if __name__ == '__main__':
    main()
