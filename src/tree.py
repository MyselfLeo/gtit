from item import Item

class GEDData:
    """Represent all the informations contained in a .GED file.

    Like a .GED file, it is composed of a succession of items (Individuals, Families, Notes, etc.) that
    are linked together.

    This class can then generate a genealogical tree, starting from an Individual Item and making its way up
    in the generations.
    """

    # Tree items
    items: 'list[Item]' = []

    # Reference dictionary
    references = {}




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
                sub_blocks[key] = Tree.divide_into_sub_blocks(sub_blocks[key])

        return sub_blocks



    def hierarchy_to_items(self, hierarchy) -> 'list[Item]':
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
                item.value = item_values[2]

            # Get the children of the item, if any (children are in the hierarchy[key] dict)
            if hierarchy[key] != '':
                item.children = self.hierarchy_to_items(hierarchy[key])

            items.append(item)


        return items
        


    def find_references(self) -> None:
        """
        Iterate over each of the item of the tree and find references.
        """

        for item in self.items:
            if item.reference != '':
                self.references[item.reference] = item
        
    
    

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


        # Open the file
        with open(filepath, 'r', encoding = 'utf-8-sig') as f:
            file: str = f.read()

        # Check for the validity of the file
        if not file.startswith('0 HEAD'):
            raise Exception(f"The file {filepath} is not a valid .GED file.")


        hierachy: dict = Tree.divide_into_sub_blocks(file)
        self.items = self.hierarchy_to_items(hierachy)

        # Find references
        self.find_references()

        # Link references
        for item in self.items:
            item.link_references(self.references)


    
    def get_items(self, item_id: str) -> 'list[Item]':
        """Return a list of items with the given identifier."""
        return [item for item in self.items if item.identifier == item_id]







'''
    def get_stats(self) -> str:
        """Return a list of statistics from this tree, as a str."""
        # TODO: Implement this method
        pass


    def get_individuals_list(self) -> str:
        """Return a list of all individual names in this tree, as a str."""
        res: str = ""

        for item in self.items:
            if item.identifier == 'INDI':
                res += str(item) + '\n'

        return res



    def get_families_list(self) -> str:
        """Return a list of all family in this tree, as a str.
        Families are identified by the name of the husband and the name of the wife.
        """

        res: str = ""

        for item in self.items:
            if item.identifier == 'FAM':

                # Count the number of children
                nb_children: int = 0
                for child_item in item.children:
                    if isinstance(child_item.get_value(), Item):
                        nb_children += child_item.get_value().identifier == 'CHIL'

                # Get each children item that is a HUSB or a WIFE item
                for child_item in item.children:
                    if child_item.identifier in ['HUSB', 'WIFE']:
                        individual: Item = child_item._referenced_item

                        res += f"{individual.get_value('NAME')}, "

                res += f"{nb_children} children\n"

        return res
'''