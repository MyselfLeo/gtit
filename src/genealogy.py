# This file is used to generate a proper object-oriented representation of a genealogical tree.
# A Genealogical tree is only composed of individuals; each individual has a father and a mother.

import dateutil.parser

from item import Item
from datetime import date


class Individual:
    """
    Represent an individual.
    """
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

    father: 'Individual' = None
    mother: 'Individual' = None

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
        






    def __init__(self, item: Item, generation: int = 0) -> None:
        """
        Generate this individual with the information contained in the given item.
        The item must have the 'INDI' identifier.
        """
        assert item.identifier == 'INDI', "The item must have the 'INDI' identifier."

        self.generation = generation

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



        # TODO: This code make a stack overflow: building a parent will build a child, which will build a parent, etc.



        # Look for a family where this individual is the child
        family_item = item.get_value('FAMC')
        if family_item:
            father_item = family_item.get_value('HUSB')
            mother_item = family_item.get_value('WIFE')

            # This part will generate recursively the father and the mother, building up the tree
            if father_item: self.father = Individual(father_item, self.generation + 1)
            if mother_item: self.mother = Individual(mother_item, self.generation + 1)



        # Look for families where this individual is the father or the mother
        family_items_references: 'list[str]' = item.get_children('FAMS')
        family_items: 'list[Item]' = []
        for family_item_reference in family_items_references:
            family_items.append(family_item_reference.get_value())

        # For each family, add the children to this individual
        for family_item in family_items:
            # Get the children of this family and generate them
            children_items_references: 'list[str]' = family_item.get_children('CHIL')
            for child_item_reference in children_items_references:
                child_item: Item = child_item_reference.get_value()
                self.children.append(Individual(child_item, self.generation - 1))




    
    def get_nb_ancestors(self, generation: int) -> int:
        """
        Return the number of ancestors of this individual, at the given generation.

        Args:
            generation (int): the generation offset starting from the root. Must be >= 0.

        Returns:
            The number of ancestors of this individuals in the given generation.
        """
        if generation < 0: return 0


        individual_count: int = 0
    
        if generation == 0: return 1
        elif generation == 1:
            if self.father: individual_count += 1
            if self.mother: individual_count += 1
            return individual_count

        else:
            if self.father: individual_count += self.father.get_nb_ancestors(generation - 1)
            if self.mother: individual_count += self.mother.get_nb_ancestors(generation - 1)
            return individual_count





    def get_nb_descendants(self, generation: int) -> int:
        """
        Return the number of descendants of this individual, at the given generation.
        Warning: generation must be a negative number, as we're going down in the generations.

        Args:
            generation (int): the generation offset starting from the root. Must be < 0.

        Returns:
            The number of descendants of this individual in the given generation.
        """
        if generation > 0: return 0


        if generation == 0: return 1

        elif generation == -1:
            return len(self.children)

        else:
            individual_count: int = 0
            for child in self.children:
                individual_count += child.get_nb_descendants(generation + 1)
            return individual_count





    def get_individuals_names(self, generation: int):
        """
        TODO: Docstring
        TODO: Refactor all of this
        """
        names = []

        if generation == 0: return [self.get_name_disposition()]
        elif generation == 1:
            if self.father: names += [self.father.get_name_disposition()]
            else: names += [{'top': '???', 'bottom': '???'}]
            if self.mother: names += [self.mother.get_name_disposition()]
            else: names += [{'top': '???', 'bottom': '???'}]
            return names

        else:
            if self.father: names += self.father.get_individuals_names(generation - 1)
            else:
                names += [{'top': '???', 'bottom': '???'}, {'top': '???', 'bottom': '???'}]
            if self.mother: names += self.mother.get_individuals_names(generation - 1)
            else: names += [{'top': '???', 'bottom': '???'}, {'top': '???', 'bottom': '???'}]
            
            # Check if the nb of names is the one expected
            expected_nb_names: int = 2 ** (generation)

            if len(names) != expected_nb_names:
                raise ValueError("Can't go back to this generation.")

            return names




    
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