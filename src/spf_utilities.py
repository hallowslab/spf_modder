from typing import Dict
from argparse import Namespace, ArgumentParser, Action


class StoreUpper(Action):
    """
    Just a really simple action that converts the stored value from the <operation> argument to upper case
    this way the operations are case insensitive and will work with any variation EX: a|AdD|ReMoVe|REMove|r
    """

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    def _to_upper(self, values):
        if values is None:
            raise ValueError("You need to supply a value")
        if isinstance(values, str):
            return values.upper()
        elif isinstance(values, list):
            raise ValueError("Multiple values not supported")
        raise TypeError("Invalid type for values. Must be string or list.")

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, self._to_upper(values))


def setup_argparse() -> Namespace:
    parser = ArgumentParser(
        description="Adds or removes spf records, trough the creation of a new zone file",
        prog="spf_modder",
        epilog="The end",
    )
    parser.add_argument("domain", type=str, help="Domain to be modified")
    parser.add_argument(
        "operation",
        type=str,
        help="Add or Remove (A/R|a/r|add/remove|Add/Remove)",
        action=StoreUpper,
    )
    parser.add_argument(
        "records",
        type=str,
        help='Record(s) to be added or removed(string separated by commas "+ip4:...,")',
    )
    parser.add_argument(
        "-rd",
        "--remove-duplicates",
        type=bool,
        action="store_true",
        help="Removes duplicate mechanisms from the records"
    )
    parser.add_argument(
        "-dry",
        "--dry-run",
        action="store_true",
        default=False,
        help="Does not execute, only logs changes",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    args: Namespace = parser.parse_args()
    return args


def remove_duplicate_entries(records_dict: Dict) -> Dict:
    """
    Removes duplicate entries using a dictionary plus list comprehension, the logic is as follows:
    We are creating a new dictionary, copying the keys over since they should not be modified
    then we enumerate the list so that for each value we have a corresponding index
    and if we already have an equal occurence in the list up to that index it's a duplicate entry
    """
    new_dict = {
        index_key: [
            value
            for index, value in enumerate(records_dict[index_key])
            if value not in records_dict[index_key][:index]
        ]
        for index_key in records_dict.keys()
    }
    return new_dict
