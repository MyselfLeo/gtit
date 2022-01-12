import re
import os
import argparse
from sys import exit
from geddata import GEDData
from item import Item
from individual import Individual
from graphic_tree import *



AVAILABLE_MODES = ["list", "stats", "tree"]






def list(ged_data: GEDData, regex: str, remove_artifacts: bool) -> None:
    """Print a list of individuals from the GEDData.
    
    TODO: Docstring
    """
    
    # Get a list of every individual
    individual_list: 'list[Item]' = ged_data.get_items('INDI')

    # Sort the list of individuals by reference id (reference = @I13@, reference id = 13)
    individual_list.sort(key=lambda x: int(x.reference.replace('@', '')[1:]))


    print("%-10s %-50s %-20s" % ("reference", "name", "birth date"))

    for individual in individual_list:

        # Skip the name if it doesn't match the regex
        if regex is not None:
            if re.match(regex, individual.get_value('NAME')) is None:
                continue


        reference: int = int(individual.reference.replace('@', '')[1:])

        name: str = individual.get_value('NAME')
        if remove_artifacts:
            name = name.replace("/", "")
            name = name.replace("_", " ")

        birth: str = ""
        try: birth = individual.get_child('BIRT').get_value('DATE')
        except: pass

        print("%-10i %-50s %-20s" % (reference, name, birth))







def tree(ged_data: GEDData, name: str, depth: int, remove_artifacts: bool, downward: bool) -> None:
    """Draw a tree from the GEDData."""

    root: list[Individual] = ged_data.find_individual(name)

    if len(root) == 0:
        print("Could not find the individual with the name '" + name + "'.")
        print(f"You can list the individuals with the 'gtit.py list -i {ged_data.filepath}' mode.")
        exit(1)

    root = root[0]


    used_depth: int = depth
    graphic_tree: GraphicTree = GraphicTree()

    
    #while used_depth >= 0:
        #try:
    graphic_tree.draw(root, used_depth)
            #break

        #except: used_depth -= 1


    if used_depth == -1:
        print("Could not draw the tree. Verify your arguments.")
        exit(1)






def load_ged_file(path: str) -> GEDData:
    """Load a GED file and return a GEDData object."""

    print("Loading GED file...")
    ged_data: GEDData = GEDData()
    ged_data.parse(path)
    print()

    return ged_data






def main():
    parser = argparse.ArgumentParser()
    # Add the arguments
    parser.add_argument("mode", help="The mode of the program. Available modes: " + ", ".join(AVAILABLE_MODES), default="tree")
    parser.add_argument("-n", "--name", help="A Regular expression to filter the name of the individuals.", default=None)
    parser.add_argument("-a", "--removeartifacts", help="Whether the display must remove artifacts in the individual names (like / or _).", default=False, action="store_true")
    parser.add_argument("-d", "--depth", help="The depth of the tree to draw. Must be an integer. Default: 2", type=int, default=2)
    parser.add_argument("--downward", help="Whether to display a downward tree from the root (its children) instead of a upward tree (its parents).", default=False, action="store_true")
    parser.add_argument("path", help="Path to the .GED file")

    args = parser.parse_args()


    # Check if the mode is valid
    if args.mode not in AVAILABLE_MODES:
        print("Invalid mode: " + args.mode)
        exit(1)


    # Act depending on the mode
    if args.mode == "list":

        ged_data: GEDData = load_ged_file(args.path)
        list(ged_data, args.name, args.removeartifacts)
        exit(0)


    elif args.mode == "tree":

        # Check arguments before loading the .GED file
        if args.name == None:
            print("No root specified. Please specify the name of the root individual using the -n/--name option.")
            exit(1)

        ged_data: GEDData = load_ged_file(args.path)
        tree(ged_data, args.name, args.depth, args.removeartifacts, args.downward)
        exit(0)
        




if __name__ == "__main__":
    main()