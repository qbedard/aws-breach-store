import sys
import argparse
import re
import json

parser = argparse.ArgumentParser()

parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()

try:
    raw_data = open(args.file, 'r')
except FileNotFoundError:
    sys.exit('File was not found.')

email_format = r"(([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+))"
password_format = r"(.+)\r"
line_format = re.compile(
    r"^" + email_format + r"\:" + password_format + r"\s*$")

parsed_list = []
for line in raw_data:
    match = line_format.match(line)
    if match is not None:
        email, username, domain, password = match.groups()
        parsed_list.append({
            'email': email,
            'username': username,
            'domain': domain,
            'password': password})
    else:
        print('Line does not match format: ', line)

with open('parsed_data.json', 'wb') as out_file:
    for item in parsed_list:
        out_file.write("{ \"index\": {\"_index\": \"identity\", \"_type\": \"login\"}}\n")
        json.dump(item, out_file, ensure_ascii=False)
        out_file.write('\n')
