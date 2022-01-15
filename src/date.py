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

    MONTHS_TOKENS: 'list[str]' = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    MONTH_NAMES: 'list[str]' = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    CIRCA_TOKENS: 'list[str]' = ["ABT", "CAL", "EST"]

    day: str = None
    month: int = None
    year: str = None

    other_day: str = None
    other_month: int = None
    other_year: str = None

    is_before: bool = False
    is_after: bool = False
    is_between: bool = False
    is_from_to: bool = False
    is_circa: bool = False


    def __init__(self, date_str: str) -> None:
        """Instanciate the Date and parse the date_str"""

        if not date_str: return

        first_year_list: list[str] = []
        second_year_list: list[str] = []

        is_second_year: bool = False

        # Parse date_str
        words: list[str] = date_str.split(' ')
        for word in words:
            if word == '': continue

            if word in Date.CIRCA_TOKENS: self.is_circa = True

            elif word == "TO" and self.is_from_to: is_second_year = True
            elif word == "AND" and self.is_between: is_second_year = True
            elif word == "FROM": self.is_from_to = True
            elif word == "BETWEEN": self.is_between = True
            elif word == "BEF": self.is_before = True
            elif word == "AFT": self.is_after = True

            elif is_second_year: second_year_list.append(word)
            else: first_year_list.append(word)
        
        
        # Register date information
        if len(first_year_list) == 3: # The date is complete
            self.day = first_year_list[0]
            self.month = self.MONTHS_TOKENS.index(first_year_list[1])
            self.year = first_year_list[2]

        if len(first_year_list) == 2: # Could be day/month or month/year (day/year is absurd)

            # Is day/month, as the month is the last value
            if first_year_list[1] in self.MONTHS_TOKENS:
                self.day = first_year_list[0]
                self.month = self.MONTHS_TOKENS.index(first_year_list[1])

            # Is month/year
            else:
                self.month = self.MONTHS_TOKENS.index(first_year_list[0])
                self.year = first_year_list[1]
        
        elif len(first_year_list) == 1: # Only the year
            self.year = first_year_list[0]



        # Register date information
        if len(second_year_list) == 3: # The date is complete
            self.other_day = second_year_list[0]
            self.other_month = self.MONTHS_TOKENS.index(second_year_list[1])
            self.other_year = second_year_list[2]

        if len(second_year_list) == 2: # Could be day/month or month/year (day/year is absurd)

            # Is day/month, as the month is the last value
            if second_year_list[1] in self.MONTHS_TOKENS:
                self.other_day = second_year_list[0]
                self.other_month = self.MONTHS_TOKENS.index(second_year_list[1])

            # Is month/year
            else:
                self.other_month = self.MONTHS_TOKENS.index(second_year_list[0])
                self.other_year = second_year_list[1]
        
        elif len(second_year_list) == 1: # Only the year
            self.other_year = second_year_list[0]



    
    def __str__(self) -> str:
        """Represent the date as a str"""
        
        res: list[str] = []

        if self.is_circa: res.append("appr.")

        if self.is_after: res.append("after")
        elif self.is_before: res.append("before")
        elif self.is_between: res.append("between")
        elif self.is_from_to: res.append("from")

        if self.day: res.append(self.day)
        if self.month: res.append(self.MONTH_NAMES[self.month])
        if self.year: res.append(self.year)

        if self.is_between: res.append("and")
        elif self.is_from_to: res.append("to")

        if self.other_day: res.append(self.other_day)
        if self.other_month: res.append(self.MONTH_NAMES[self.other_month])
        if self.other_year: res.append(self.other_year)

        if len(res) > 0:
            res[0] = res[0].capitalize()
            return ' '.join(res)
        return ''