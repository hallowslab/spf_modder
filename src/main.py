#!/usr/bin/env python3
import re
import sys
from typing import Dict, List

from spf_utilities import setup_argparse

ADDOP = ["A", "ADD"]
REMOP = ["R", "REM", "REMOVE"]


def retrieve_spf_from_zone_file(fqdn: str) -> Dict:
    SPF_STR = re.compile(f'{fqdn}.*IN\s+TXT\s+"v=spf.*')
    zone_file_path: str = f"/var/named/{fqdn}.db"
    records: Dict = {}

    try:
        with open(zone_file_path, "r", encoding="utf-8") as file:
            for count, line in enumerate(file, start=1):
                if re.match(SPF_STR, line) and not line.startswith(";"):
                    # Extract the values after TXT and remove extra characters
                    # like spaces and new lines
                    spf_record = line.split("TXT")[1].strip(' ;\n"')
                    # Split into list
                    records[count] = spf_record.split(" ")
    except FileNotFoundError:
        print(f"Zone file not found for {fqdn}")
        return {}

    return records


def generate_new_zone(fqdn: str, modified_records: Dict) -> int:
    """
    Creates a new zone file with the extension .spfm
    should return a status code(int) to indicate if the process was successfull or not
    """
    original_zone: str = f"/var/named/{fqdn}.db"
    new_zone: str = f"/var/named/{fqdn}.spfm"
    new_content: List = []

    try:
        with open(original_zone, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if line_number in modified_records:
                    # make sure to join the list in modified_records and add apostrophes for the "string"
                    record_str = f'"{" ".join(modified_records[line_number])}"'
                    # also don't forget to add the TXT that was removed in the split
                    # and the space characters (seems to be a single tab character) before the actual record
                    new_line = line.split("TXT")[0] + "TXT\t" + record_str + "\n"
                    new_content.append(new_line)
                else:
                    new_content.append(line)
    except FileNotFoundError:
        print(f"Error: Zone file not found for {fqdn}")
        return 1

    try:
        with open(new_zone, "w", encoding="utf-8") as file:
            file.writelines(new_content)
            print(f"Wrote new zone file at: {new_zone}")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Error: Failed writing to new zone file: {e}")
        return 1
    return 0


if __name__ == "__main__":
    args = setup_argparse()
    domain = args.domain
    operation = args.operation
    original_records = retrieve_spf_from_zone_file(domain)
    supplied_records = args.records.split(",")
    new_records = {}
    status = 0

    if not original_records:
        print("Failed to retrieve SPF records. Quitting now!")
        sys.exit(1)

    # Yes I know this is horrible and not meant to be readable here is the explanation
    if operation in ADDOP:
        # creates a new dictionary with <i> as key and the values minus the last one/iteration (in this case one of the following -all|~all|...)
        # appends the new values in <supplied_records> if they are not present, this is achieved trough the sum of the previous list with the new one
        # finally append the last previous value to the list
        new_records = {
            i: original_records[i][:-1]
            + [v for v in supplied_records if v not in original_records[i]]
            + [original_records[i][-1]]
            for i in original_records
        }
    elif operation in REMOP:
        # Here it's a bit more simple it creates a dictionary with <i> as the key
        # and the it appends the values from .items() if they are not in <supplied_records>
        new_records = {
            i: [v for v in values if v not in supplied_records]
            for i, values in original_records.items()
        }
    else:
        print(f"Unkown operation: {operation}")

    if args.dry_run:
        print("We would be modifying the following contents ->")
        for i, v in new_records.items():
            print(
                f"At line:{i} , we would change to the following policy:\n===\n{v}\n===\n"
            )
    elif len(new_records) > 0:
        status = generate_new_zone(domain, new_records)

    sys.exit(status)
