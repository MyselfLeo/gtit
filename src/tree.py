from node import Node

class Tree:
    """Represent a genealogical tree.

    A genealogical tree is made of a root node and multiple informations about the tree.
    """

    # Tree metadatas
    items: 'list[Node]' = []



    def parse_block(self, block: str) -> Node:
        """Parse the block recursively and return a Node object.
        This node object is the root of the block.

        Args:
            block (str): A block of the .GED file.

        Return:
            Node: The root of the block. This Node object has other Node objects as children.
        """

        # Create a new node
        node: Node = Node()

        # Remove last newline
        block = block.rstrip()


        # Read the first line of the block (the block information) ######################################
        line: str = block.split('\n')[0]
        line_informations = line.split(' ')
        node.level = int(line_informations[0])

        # Add the reference if it exists, and the identifier
        info = line_informations[1]

        if info[0] == info[-1] == '@':                  # first info is reference => ref + id
            node.reference = info[1:-1]
            node.identifier = line_informations[2]

        else:                                           # first info is id => id + value
            node.identifier = info
            node.value = ' '.join(line_informations[2:])

        
        # Read the other lines of the block (the block children) ########################################
        subblock: str = ""
        subblock_base_lvl: int = None


        for line in block.split('\n')[1:]:

            # Skip empty lines
            if line.rstrip() == "": continue

            line_lvl: int = int(line.split(' ')[0])

            if subblock_base_lvl == None:
                subblock_base_lvl = line_lvl
                subblock += line + '\n'

            elif line_lvl > subblock_base_lvl:
                subblock += line + '\n'

            else:
                node.add_child(self.parse_block(subblock))
                subblock = ""
                subblock_base_lvl = None


        # Return the node
        return node

        




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
            file: str = f.readlines()

        # Check for the validity of the file
        if not file[0].startswith('0 HEAD'):
            raise Exception(f"The file {filepath} is not a valid .GED file.")


        subblock: str = file[0]
        correct_stop: bool = False

        for line in file[1:]:
            # Stop parsing when the end of the file is reached
            if line.startswith('0 TRLR'):
                correct_stop = True 
                self.items.append(self.parse_block(subblock))
                break


            # Skip empty lines
            if line == '\n': continue

            line_lvl: int = int(line.split(' ')[0])

            # If the line is in a sub-block of the main block (the file), add it to the sub-block buffer
            if line_lvl > 0:
                subblock += line

            # If not, then the line is the start of a new sub-block, so add the previous sub-block to the list
            # and add the start of the new sub-block to the subblock buffer
            else:
                self.items.append(self.parse_block(subblock))
                subblock = line


        # Check if the file has been parsed correctly
        if not correct_stop:
            raise Warning(f"The file {filepath} may not have been parsed correctly.")