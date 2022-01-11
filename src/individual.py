# This file is used to generate a proper object-oriented representation of a genealogical tree.
# A Genealogical tree is only composed of individuals; each individual has a father and a mother.

import dateutil.parser

from item import Item
from datetime import date


class Individual:
    """
    Represent an individual.
    """
    id: int = 0
    generation: int = 0

    first_name: str = None # In the form first name /last name/
    last_name: str = None
    surname: str = None
    given_name: str = None

    sex: str = None

    birth_date: date = None
    birth_place: str = None

    death_date: date = None
    death_place: str = None

    # father_reference, mother_reference and children_references are used after the creation of the Individual
    # by the geddata parser to link it to the other individual objects.

    father_reference: str = None
    mother_reference: str = None

    father: 'Individual' = None
    mother: 'Individual' = None

    children_references: 'list[str]' = []
    children: 'list[Individual]' = []



    @staticmethod
    def separate_names(name: str) -> 'tuple(str)':
        """Tries to separate in the given name the first name and the last name.
        
        In a .GED file, the syntax is first name /last name/.
        """
        firstname: str = None
        lastname: str = None

        firstname = name.split('/')[0]
        lastname = name.split('/')[1]

        return firstname, lastname


    
    @staticmethod
    def parse_date(date_str: str) -> date:
        """Tries to parse the given date (as a string) into the most precise date object possible."""

        # Parse using dateutil
        try:
            return dateutil.parser.parse(date_str)
        except:
            # If the date can't be parsed, we expect that only the year is provided
            return date(int(date_str[-4:]), 1, 1)

    
    

    def get_name_disposition(self) -> 'list[str]':
        """Return a list of 2 str representing how the name of this
        individual should be displayed in a 2 line way.

        If this individual has both firstname and lastname, the syntax is firstname then lastname.
        If not, display every "word" of the name on top except the last.
        """
        if self.first_name != "" and self.last_name != "":
            return {"top": self.first_name, "bottom": self.last_name}

        else:
            sep: list[str] = self.first_name.split(' ')
            middle = len(sep) // 2
            return {"top": ' '.join(sep[0:middle]), "bottom": ' '.join(sep[middle:])}
        






    def __init__(self, item: Item) -> None:
        """
        Generate this individual with the information contained in the given item.
        The item must have the 'INDI' identifier.
        """
        assert item.identifier == 'INDI', "The item must have the 'INDI' identifier."


        self.id = item.reference.replace('@', '')[1:]

        self._raw_name = item.get_value('NAME')
        self.first_name, self.last_name = Individual.separate_names(self._raw_name)
        self.surname = item.get_value('SURN')
        self.given_name = item.get_value('GIVN')

        self.sex = item.get_value('SEX')

        birth_item: Item = item.get_child('BIRT')
        if birth_item:
            self.birth_date = Individual.parse_date(birth_item.get_value('DATE'))
            self.birth_place = birth_item.get_value('PLAC')

        death_item: Item = item.get_child('DEAT')
        if death_item:
            self.death_date = Individual.parse_date(death_item.get_value('DATE'))
            self.death_place = death_item.get_value('PLAC')



        # Look for a family where this individual is the child
        family_item = item.get_value('FAMC')
        if family_item:
            self.father_reference = family_item.get_child('HUSB').value # Get the reference string to the father
            self.mother_reference = family_item.get_child('HUSB').value # Get the reference string to the father



        # Look for families where this individual is the father or the mother
        family_items_references: 'list[str]' = item.get_children('FAMS')
        family_items: 'list[Item]' = []
        for family_item_reference in family_items_references:
            family_items.append(family_item_reference.get_value())


        # For each family, add the children reference to this individual
        for family_item in family_items:
            # Add each child reference to this individual
            children_items_references: 'list[str]' = family_item.get_children('CHIL')

            for child_item_reference in children_items_references:
                self.children_references += child_item_reference.value





    
    def get_ancestors(self, generation: int) -> 'list[Individual]':
        """
        Return the list of ancestors of this Individual at the given generation.

        Args:
            generation (int): the generation offset starting from the root. Must be >= 0. get_descendants will be called otherwise.

        Returns:
            List of every ancestors of this Individual at the given generation.
        """
        if generation < 0: return self.get_descendants(generation)

        ancestors: list[Individual] = []
    
        if generation == 0: return []
        elif generation == 1:
            if self.father: ancestors.append(self.father)
            if self.mother: ancestors.append(self.mother)
            return ancestors

        else:
            if self.father: ancestors += self.father.get_ancestors(generation - 1)
            if self.mother: ancestors += self.mother.get_ancestors(generation - 1)
            return ancestors





    def get_descendants(self, generation: int) -> 'list[Individual]':
        """
        Return the list of ancestors of this Individual at the given generation.

        Args:
            generation (int): the generation offset starting from the root. Must be < 0. get_ancestors will be called otherwise.

        Returns:
            List of every descendants of this Individual at the given generation.
        """
        if generation > 0: return self.get_ancestors(generation)

        if generation == 0: return []
        elif generation == -1:
            return self.children

        else:
            descendants: list[Individual] = []
            for child in self.children:
                descendants += child.get_descendants(generation + 1)
            return descendants