
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





def list(ged_data: GEDData, individuals: bool) -> None:
    """List elements from the GEDData."""
    
    if individuals:
        individual_list: 'list[Item]' = ged_data.get_items('INDI')

        txt: str = ""

        for i, individual in enumerate(individual_list):
            txt += "%-8i %-30s %-20s\n" % (i, individual.get_value('NAME').replace('/', ''), individual.get_child('BIRT').get_value('DATE'))

        print("%-8s %-30s %-20s" % ("id", "name", "birth date"))
        print(txt)





def tree(ged_data: GEDData, root_name: str, depth: int) -> None:
    """Draw a tree from the GEDData."""

    if root_name == "":
        print("No root specified. Please specify a root with the -r option.")
        exit(1)

    root: list[Item] = ged_data.find_items('INDI', {"NAME": root_name})

    if len(root) == 0:
        print("Could not find the individual with the name '" + root_name + "'.")
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
        
    exit(0)






def main():
    parser = argparse.ArgumentParser()
    # Add the arguments
    parser.add_argument("mode", help="The mode of the program. Available modes: " + ", ".join(AVAILABLE_MODES), default="tree")
    parser.add_argument("-r", "--root", help="The root of the tree to draw. Must be the name of an individual from the .GED file.", default="")
    parser.add_argument("-d", "--depth", help="The depth of the tree to draw. Must be an integer. Default: 2", type=int, default=2)
    parser.add_argument("-i", "--individuals", help="Only show information about individuals", action="store_true")
    parser.add_argument("path", help="Path to the .GED file")

    args = parser.parse_args()


    # Check if the mode is valid
    if args.mode not in AVAILABLE_MODES:
        print("Invalid mode: " + args.mode)
        exit(1)

    # Load the GED file
    ged_data: GEDData = GEDData()
    ged_data.parse(args.path)


    # Act depending on the mode
    if args.mode == "list":
        list(ged_data, args.individuals)
        exit(0)


    elif args.mode == "tree":
        tree(ged_data, args.root, args.depth)
        exit(0)


    elif args.mode == "stats":
        pass
        exit(0)
        




if __name__ == "__main__":
    main()