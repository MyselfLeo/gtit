from node import Node

class Tree:
    """Represent a genealogical tree.

    A genealogical tree is made of a root node and multiple informations about the tree.
    """

    # Tree metadatas
    items: 'list[Node]' = []




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



    def hierarchy_to_node(self, hierarchy) -> None:
        """
        Take a generated hierarchy (as a dict, coming from the divide_into_sub_blocks method)
        and convert it into multiple nodes that will be placed in the items list.

        This method works recursively.
        """
        

    
    

    def parse(self, filepath: str) -> None:
        """
        Parse the .GED file.

        For each block of the .GED file, a Node object is created and added to the items list.
        Each item is a Node object.
        
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



    def get_stats(self) -> str:
        """Return a list of statistics from this tree, as a str."""
        # TODO: Implement this method
        pass


    def get_individuals_list(self) -> str:
        """Return a list of all individual names in this tree, as a str."""
        res: str = ""

        for item in self.items:
            if item.identifier == 'INDI':
                res += item.get_children("NAME").value + '\n'

        return res