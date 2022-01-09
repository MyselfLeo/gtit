import sys
from geddata import GEDData
from item import Item
from genealogy import Individual
from tree_drawer import *



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
        geddata = GEDData()
        geddata.parse(arguments[-1])

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
            individual_list: 'list[Item]' = geddata.get_items('INDI')

            txt: str = ""

            for i, individual in enumerate(individual_list):
                txt += "%-8i %-30s %-20s\n" % (i, individual.get_value('NAME').replace('/', ''), individual.get_child('BIRT').get_value('DATE'))

            print("%-8s %-30s %-20s" % ("id", "name", "birth date"))
            print(txt)




    if mode == "tree":
        name: str = arguments[1]
        filepath: str = arguments[2]

        root: list[Item] = geddata.find_items('INDI', {"NAME": name})

        if len(root) == 0:
            print("ERROR: Could not find the individual with the name '" + name + "'.")
            return

        root = Individual(root[0])
        tree: str = draw(root, 150)
        print('\n\n')
        print(tree)
        print('\n\n')

        



if __name__ == "__main__":
    main()