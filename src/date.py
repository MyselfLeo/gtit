from enum import Enum




class Date:
    """This class is used to represent a date associated to an event in a .GED file.

    Dates are not only restricted to day/month/year:
    - An event can be between 2 known dates;
    - An event can last between 2 known dates;
    - An event can be before or after a known date;
    - An event can have an approximated date;

    This class can represents all of that.
    """

    MONTHS_STR: Enum = Enum("MONTHS", "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC")
    CIRCA_TOKENS: 'list[str]' = ["ABT", "CAL", "EST"]

    day: int
    month: int
    year: int

    other_day: int
    other_month: int
    other_year: int

    is_before: bool = False
    is_after: bool = False
    is_between: bool = False
    is_from_to: bool = False
    is_circa: bool = False


    def __init__(date_str: str) -> None:
        """Instanciate the Date and parse the date_str"""
        tokens: list[str] = date_str.split(' ')

        for token in tokens:
            if token in Date.CIRCA_TOKENS: is_circa = True