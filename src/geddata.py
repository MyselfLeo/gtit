import re
from item import Item
from individual import Individual

class GEDData:
    """Represent all the informations contained in a .GED file.

    The parsing of the .GED file is done in 3 steps:
    - Divide the file into items (Families, Individuals, etc.)
    - From the list of items, create a list of Individual objects.
    - Link the individuals with their parents and children.

    Creating on-the-fly the Individual objects was not possible, as it was causing
    problem linking the individuals with their parents and children. We need to have a list
    of every Individuals in the form of objects.
    """

    filepath: str = ''                      # File path
    individuals: 'list[Individual]' = []    # List of every individuals present in the .GED file

    _items: 'list[Item]' = []               # GEDData items
    _item_references = {}                   # Reference dictionary for items
    _individual_references = {}             # Reference dictionary for Individual objects




    @staticmethod
    def divide_into_sub_blocks(block: str):
        """Take given block and divide it into a hierarchy in the
        form of a dictionary.
        """
        block_lvl: int = int(block[0])
        sub_blocks = {}
        first_line = block.split('\n')[0]
        sub_block: str = ""

        for line in block.split('\n')[1:]:

            # Skips empty lines
            if line == '': continue

            line_lvl: int = int(line.split(' ')[0])

            if line_lvl > block_lvl:
                sub_block += line + '\n'

            else:
                sub_blocks[first_line] = sub_block
                sub_block = ""
                first_line = line

        sub_blocks[first_line] = sub_block

        for key in sub_blocks:
            if not sub_blocks[key] == '':
                sub_blocks[key] = GEDData.divide_into_sub_blocks(sub_blocks[key])

        return sub_blocks


    @staticmethod
    def hierarchy_to_items(hierarchy) -> 'list[Item]':
        """
        Take a generated hierarchy (as a dict, coming from the divide_into_sub_blocks method)
        and convert it into multiple items.

        This method works recursively.
        """
        items: list[Item] = []


        for key in hierarchy:
            item: Item = Item()

            # Get information about the item from the key
            item_values: list[str] = key.split(' ')
            if len(item_values) < 3:
                item_values += [''] * (3 - len(item_values))

            item.level = int(item_values[0])

            if item_values[1][0] == item_values[1][-1] == '@': # If the first information is a reference, this item wont have a value
                item.reference = item_values[1]
                item.identifier = item_values[2]

            else:                                              # Else, the item has an identifier and a value
                item.identifier = item_values[1]
                item.value = ' '.join(item_values[2:])

            # Get the children of the item, if any (children are in the hierarchy[key] dict)
            if hierarchy[key] != '':
                item.children = Item.hierarchy_to_items(hierarchy[key])

            items.append(item)

        return items




    def generate_items(self, hierarchy) -> None:
        """Take the hierarchy and generate the items."""

        # Generate the list of items
        self._items = Item.hierarchy_to_items(hierarchy)

        # Reference the items
        for item in self._items:
            if item.reference != '':
                self._references[item.reference] = item

        # Link references
        for item in self._items:
            item.link_references(self._references)
        
        
    



    def generate_individuals(self) -> None:
        """Generate the individuals from the list of items."""

        for item in self._items:
            if item.identifier == 'INDI':
                indi: Individual = Individual(item)                     # Create the individual
                self._individual_references[f"@I{indi.id}@"] = indi     # Reference this individual in the _individual_references dict
                self.individuals.append(indi)                           # Add this individual to the list of individuals
        
        # For each individual of the list, link the parents and children
        for indi in self.individuals:
            if indi.father_reference: indi.father = self._individual_references[indi.father_reference]
            if indi.mother_reference: indi.mother = self._individual_references[indi.mother_reference]

            for child_reference in indi.child_references:
                indi.children.append(self._individual_references[child_reference])





    

    def parse(self, filepath: str) -> None:
        """
        Parse the .GED file.

        For each block of the .GED file, a Item object is created and added to the items list.
        Each item is a Item object.
        
        Args:
            filepath (str): The path of the .GED file.

        Raise:
            FileNotFoundError: If the filepath is not valid.
            Exception: If the file does not look like a .GED file.
            Warning: If the file does not look valid, but parsing is not stopped.
        """

        self.filepath = filepath

        # Open the file
        with open(self.filepath, 'r', encoding = 'utf-8-sig') as f:
            file: str = f.read()

        # Check for the validity of the file
        if not file.startswith('0 HEAD'):
            raise Exception(f"The file {self.filepath} is not a valid .GED file.")


        # Generate the items
        hierarchy: dict = GEDData.divide_into_sub_blocks(file)   
        self.generate_items(self, hierarchy)

        # Generate the individuals
        self.generate_individuals()



        











    
    def get_items(self, item_id: str) -> 'list[Item]':
        """Return a list of items with the given identifier."""
        return [item for item in self._items if item.identifier == item_id]






    def find_individual(self, item_id: str, searched_name: str) -> 'list[Item]':
        """Return every individual with the given name."""

        items: 'list[Item]' = self.get_items(item_id)
        returned_items: 'list[Item]' = []

        for item in items:

            # Check both raw name and formatted name
            if re.search(searched_name, item.get_value('NAME')):
                returned_items.append(item)
            elif re.search(searched_name, item.get_value('NAME', True)):
                returned_items.append(item)


        return returned_items