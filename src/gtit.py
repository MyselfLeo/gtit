import re
import os
import argparse
from geddata import GEDData
from item import Item
from genealogy import Individual
from tree_drawer import *



AVAILABLE_MODES = ["list", "stats", "tree"]




def terminal_width() -> int:
    """Return the width of the terminal."""
    DEFAULT_WIDTH: int = 80

    try: return os.get_terminal_size().columns
    except: return DEFAULT_WIDTH





def list(ged_data: GEDData, regex: str, remove_artifacts: bool) -> None:
    """Print a list of individuals from the GEDData.
    
    TODO: Docstring
    """
    
    # Get a list of every individual
    individual_list: 'list[Item]' = ged_data.get_items('INDI')

    # Sort the list of individuals by name
    individual_list.sort(key=lambda x: x.get_value('NAME'))


    print("%-10s %-50s %-20s" % ("id", "name", "birth date"))

    for i, individual in enumerate(individual_list):

        # Skip the name if it doesn't match the regex
        if regex is not None:
            if re.match(regex, individual.get_value('NAME')) is None:
                continue


        birth: str = ""
        try: birth = individual.get_child('BIRT').get_value('DATE')
        except: pass

        name: str = individual.get_value('NAME')

        if remove_artifacts:
            name = name.replace("/", "")
            name = name.replace("_", " ")

        print("%-10i %-50s %-20s" % (i, name, birth))







def tree(ged_data: GEDData, name: str, depth: int, remove_artifacts: bool) -> None:
    """Draw a tree from the GEDData."""

    root: list[Item] = ged_data.find_individual('INDI', name)

    if len(root) == 0:
        print("Could not find the individual with the name '" + name + "'.")
        print(f"You can list the individuals with the 'gtit.py list -i {ged_data.filepath}' mode.")
        exit(1)

    root = Individual(root[0])


    used_depth: int = depth
    tree: str = ""

    while used_depth >= 0:
        try:
            tree = draw(root, used_depth, terminal_width())
            
            if used_depth != depth:
                print("[WARN] Could not draw the tree with the specified depth. The tree was drawn with a depth of " + str(used_depth) + ".")

            print('\n\n')
            print(tree)
            print('\n\n')

            break

        except: used_depth -= 1


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
        tree(ged_data, args.name, args.depth, args.removeartifacts)
        exit(0)
        




if __name__ == "__main__":
    main()