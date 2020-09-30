"""
Module which can hold multiple input validators
validating input user and responses.
"""


def validate_input_number(min, rank, max):
    return (min <= rank <= max)
