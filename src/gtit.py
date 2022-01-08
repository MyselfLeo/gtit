import sys
from tree import Tree



AVAILABLE_MODES = ["list", "stats", "tree"]



def usage():
    print("USAGE: gtit.py <MODE> <OPTIONS> <ged_file_path>")
    print("MODES:")
    print("    list         Return a list of every element in the tree (individual, family, etc.)")
    print("    stats        Return a list of statistics about the tree")
    print("    tree         Display the tree.")
    print("")
    print("OPTIONS:")
    print("    -i           Only show information about individuals")
    print("    -f           Only show information about families")


def main():
    arguments = sys.argv[1:]

    if len(arguments) == 0:
        print("ERROR: No arguments provided.\n")
        usage()
        return

    mode = arguments[0]
    if not mode in AVAILABLE_MODES:
        print("ERROR: Invalid mode.\n")
        usage()
        return



    # Load the .GED file
    try:
        tree = Tree()
        tree.parse(arguments[-1])

    except Exception as e:
        print("ERROR: Could not load file.")
        print("       " + str(e))
        return



    if mode == "list":
        options: str = []
        filepath: str = ""

        # Get the options
        for arg in arguments[1:]:
            if arg.startswith('-'):
                for c in arg[1:]: options.append(c)
            else: filepath = arg


        # Act depending on the options
        if 'i' in options:
            print(f"INDIVIDUALS IN {filepath}:")
            print(tree.get_individuals_list())

        # Act depending on the options
        if 'f' in options:
            print(f"FAMILIES IN {filepath}:")
            print(tree.get_families_list())




if __name__ == "__main__":
    main()