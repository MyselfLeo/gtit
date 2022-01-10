# This file is used to generate a proper object-oriented representation of a genealogical tree.
# A Genealogical tree is only composed of individuals; each individual has a father and a mother.


from item import Item


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

    birth_date: str = None
    birth_place: str = None

    death_date: str = None
    death_place: str = None

    father: 'Individual' = None
    mother: 'Individual' = None



    @staticmethod
    def separate_names(name: str) -> 'tuple(str)':
        """Tries to separate in the given name the first name and the last name.
        
        In a .GED file, the syntax is first name /last name/.
        """
        firstname: str = None
        lastname: str = None

        firstname = name.split('/')[0]
        lastname = name.split('/')[1]

        #print(firstname, '|', lastname)
        return firstname, lastname



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
            self.birth_date = birth_item.get_value('DATE')
            self.birth_place = birth_item.get_value('PLAC')

        death_item: Item = item.get_child('DEAT')
        if death_item:
            self.death_date = death_item.get_value('DATE')
            self.death_place = death_item.get_value('PLAC')

        # Look for a family where this individual is the child
        family_item = item.get_value('FAMC')
        if family_item:
            father_item = family_item.get_value('HUSB')
            mother_item = family_item.get_value('WIFE')

            # This part will generate recursively the father and the mother, building up the tree
            if father_item: self.father = Individual(father_item, self.generation + 1)
            if mother_item: self.mother = Individual(mother_item, self.generation + 1)



    
    def get_nb_individuals(self, generation: int) -> int:
        """
        Return the number of individuals in the tree, at the given generation.
        generation == 0 is the root's generation. For now, it is always one (the root individual only).
        generation == 1 is the root's parents. If the root individual has both parents, it should be 2.
        etc.

        Args:
            generation (int): the generation offset starting from the root.

        Returns:
            The number of individuals in a given generation.
        """
        individual_count: int = 0
        
        if generation == 0: return 1
        elif generation == 1:
            if self.father: individual_count += 1
            if self.mother: individual_count += 1
            return individual_count

        else:
            if self.father: individual_count += self.father.get_nb_individuals(generation - 1)
            if self.mother: individual_count += self.mother.get_nb_individuals(generation - 1)
            return individual_count




    def get_individuals_names(self, generation: int):
        """
        TODO: Docstring
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
            last: str = sep.pop()
            return {"top": ' '.join(sep), "bottom": last}