from node import Node

class Tree:
    """Represent a genealogical tree.

    A genealogical tree is made of a root node and multiple informations about the tree.
    """

    # Tree metadatas
    items: 'list[Node]' = []

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



    def hierarchy_to_nodes(self, hierarchy) -> 'list[Node]':
        """
        Take a generated hierarchy (as a dict, coming from the divide_into_sub_blocks method)
        and convert it into multiple nodes.

        This method works recursively.
        """
        nodes: list[Node] = []


        for key in hierarchy:
            node: Node = Node()

            # Get information about the node from the key
            node_values: list[str] = key.split(' ')
            if len(node_values) < 3:
                node_values += [''] * (3 - len(node_values))

            node.level = int(node_values[0])

            if node_values[1][0] == node_values[1][-1] == '@': # If the first information is a reference, this node wont have a value
                node.reference = node_values[1]
                node.identifier = node_values[2]

            else:                                              # Else, the node has an identifier and a value
                node.identifier = node_values[1]
                node.value = node_values[2]

            # Get the children of the node, if any (children are in the hierarchy[key] dict)
            if hierarchy[key] != '':
                node.children = self.hierarchy_to_nodes(hierarchy[key])

            nodes.append(node)


        return nodes
        


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
        self.items = self.hierarchy_to_nodes(hierachy)

        # Find references
        self.find_references()

        # Link references
        for item in self.items:
            item.link_references(self.references)



    def get_stats(self) -> str:
        """Return a list of statistics from this tree, as a str."""
        # TODO: Implement this method
        pass


    def get_individuals_list(self) -> str:
        """Return a list of all individual names in this tree, as a str."""
        res: str = ""

        for item in self.items:
            if item.identifier == 'INDI':
                res += item.get_children("NAME").get_value() + '\n'

        return res.rstrip()


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
                    if isinstance(child_item.get_real_value(), Node):
                        nb_children += child_item.get_real_value().identifier == 'CHIL'

                # Get each children node that is a HUSB or a WIFE node
                for child_item in item.children:
                    if child_item.identifier in ['HUSB', 'WIFE']:
                        individual: Node = child_item._referenced_node

                        res += f"{individual.get_value('NAME')}, "

                res += f"{nb_children} children\n"

        return res.rstrip()