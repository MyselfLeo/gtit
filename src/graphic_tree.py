# The only goal of this file is to generate a graphical view of a genealogical tree.

from enum import Enum
from individual import Individual


class LINE_SYMBOLS(Enum):
    HOR = '═'
    VER = '║'
    DIAG_L = '╗'
    DIAG_R = '╔'
    DIAG_L_B = '╚'
    DIAG_R_B = '╝'
    BRANCH_DOWN = '╦'
    BRANCH_UP = '╩'



class LineTransition:
    """
    TODO: Docstring
    """
    is_downward: bool

    nb_source_points: int
    nb_target_points: int

    # This dictionary stores in key the id of the source_point and in value
    # the list of points where it is headed to.
    # Example: if the source point 0 needs to be linked to target points 2 and 3,
    # the dict will be {0: [2, 3]}
    transition_dict: dict


    def generate_parent_transition(self, list_of_sources: 'list[Individual]') -> None:
        """
            Generate the transition_dict for the transition between list_of_sources' generation and list_of_sources' generation + 1.
        """
        self.nb_source_points = len(list_of_sources)
        self.transition_dict = {}

        list_of_targets: list[Individual] = []

        for i, source_indi in enumerate(list_of_sources):
            self.transition_dict[i] = []
            
            if source_indi.father:
                if not source_indi.father in list_of_targets: list_of_targets.append(source_indi.father)
                self.transition_dict[i] += [list_of_targets.index(source_indi.father)]
            
            if source_indi.mother:
                if not source_indi.mother in list_of_targets: list_of_targets.append(source_indi.mother)
                self.transition_dict[i] += [list_of_targets.index(source_indi.mother)]



    def generate_child_transition(self, list_of_sources: 'list[Individual]') -> None:
        """
            Generate the transition_dict for the transition between list_of_sources' generation and list_of_sources' generation - 1.
        """
        self.nb_source_points = len(list_of_sources)
        self.transition_dict = {}

        list_of_targets: list[Individual] = []

        for i, source_indi in enumerate(list_of_sources):
            self.transition_dict[i] = []
            
            for child in source_indi.children:
                if child not in list_of_targets: list_of_targets.append(child)
                self.transition_dict[i] += [list_of_targets.index(child)]



    def draw_lines():
        """TODO"""
        pass



    '''
    def connecting_lines(source_points: 'list[int]', target_points: 'list[list[int]]', width: int, height: int = 5) -> str:
    """Return a string of multiple lines representing lines coming from source_points and going
    to target_points.
    A source point can target multiple points: if so, the line will split at middle height.
    """
    lines: list[list[str]] = [[" "] * width for _ in range(height)]
    turn_height: int = height // 2

    # Draw the upward lines, from height = 0 to height = turn_height
    for lvl in range(turn_height):
        for point in source_points:
            lines[lvl][point] = LINE_SYMBOLS.VER.value

    
    # Draw the turning line. The turning line is the line where the upward line turn and go to there target point position.
    for i, point in enumerate(source_points):
        # Check if the line turns or split
        split = False
        if len(target_points[i]) > 1:
            if (target_points[i][0] < source_points[i] and target_points[i][1] > source_points[i]):
                split = True
            elif (target_points[i][0] > source_points[i] and target_points[i][1] < source_points[i]):
                split = True


        if split:
            lines[turn_height][point] = LINE_SYMBOLS.BRANCH_DOWN.value
        elif target_points[i][0] < source_points[i]:
            lines[turn_height][point] = LINE_SYMBOLS.DIAG_L.value
        elif target_points[i][0] > source_points[i]:
            lines[turn_height][point] = LINE_SYMBOLS.DIAG_R.value
        else:
            lines[turn_height][point] = LINE_SYMBOLS.VER.value
        

        # Draw the horizontal line to the target point
        for target_point in target_points[i]:
            # point: current x position
            # target_point: target x position

            if target_point < point:
                # The line goes to the left
                for j in range(point - 1, target_point, -1):
                    lines[turn_height][j] = LINE_SYMBOLS.HOR.value

                lines[turn_height][target_point] = LINE_SYMBOLS.DIAG_L_B.value
                # Check if this line comes from a split
                if len(target_points[i]) > 1:
                    other_point: int = target_points[i][1] if target_points[i][0] == target_point else target_points[i][0]
                    if other_point < target_point:
                        lines[turn_height][other_point] = LINE_SYMBOLS.BRANCH_UP.value


            elif target_point > point:
                # The line goes to the right
                for j in range(point + 1, target_point):
                    lines[turn_height][j] = LINE_SYMBOLS.HOR.value 

                lines[turn_height][target_point] = LINE_SYMBOLS.DIAG_R_B.value
                # Check if this line comes from a split
                if len(target_points[i]) > 1:
                    other_point: int = target_points[i][1] if target_points[i][0] == target_point else target_points[i][0]
                    if other_point > target_point:
                        lines[turn_height][other_point] = LINE_SYMBOLS.BRANCH_UP.value

        
        # Draw the upward lines, from height = 0 to height = turn_height
    for lvl in range(turn_height + 1, height):
        for points in target_points:
            for point in points:
                lines[lvl][point] = LINE_SYMBOLS.VER.value
    '''








class GraphicTree:
    """Class used to store and compute data related to the graphic representation in terminal of the genealogical tree.
    """

    root: Individual = None         # Root of the given tree. The root is the person from which the tree is generated.
    width: int = 0                  # Width of the terminal, in characters















def get_spaced_points(nb_points: int, width: int) -> 'list[int]':
    """Return a list of position in the x coordinate corresponding to points evenly spaced in the width space.
    """
    # Compute the space between each point
    space: int = width // (nb_points + 1)

    # Generate the list of points
    points: 'list[int]' = []
    for i in range(0, nb_points):
        points.append(space * (i + 1))

    return points



def words_line(words: 'list[str]', width: int, centers: 'list[int]') -> str:
    """Returns a line made of the given words placed according to the given centers.
    Args:
        words (list[str]): The words to put in the line.
        width (int): The width of the line, in chars.
        centers (list[int]): The position of the center of each word.
    """

    assert len(words) == len(centers), "The number of words and the number of centers must be the same."

    line = [" "] * width

    # Place each word in the line
    for i, w in enumerate(words):
        offset: int = len(w) // 2

        for j, c in enumerate(w):
            # Replace '_' by a space
            if c == '_': c = ' '
            line[centers[i] - offset + j] = c

    return ''.join(line)




def name_line(names: 'list[dict]', width: int, centers: 'list[int]') -> str:
    """Return a 2 line string displaying firstname and lastname
    of each person in names, evenly spaced.
    """

    assert len(names) == len(centers), f"The number of names {len(names)} and the number of centers {len(centers)} must be the same."

    first_names: list[str] = []
    last_names: list[str] = []
    for n in names:
        first_names.append(n['top'])
        last_names.append(n['bottom'])

    return words_line(first_names, width, centers) + '\n' + words_line(last_names, width, centers)




def connecting_lines(source_points: 'list[int]', target_points: 'list[list[int]]', width: int, height: int = 5) -> str:
    """Return a string of multiple lines representing lines coming from source_points and going
    to target_points.
    A source point can target multiple points: if so, the line will split at middle height.
    """
    lines: list[list[str]] = [[" "] * width for _ in range(height)]
    turn_height: int = height // 2

    # Draw the upward lines, from height = 0 to height = turn_height
    for lvl in range(turn_height):
        for point in source_points:
            lines[lvl][point] = LINE_SYMBOLS.VER.value

    
    # Draw the turning line. The turning line is the line where the upward line turn and go to there target point position.
    for i, point in enumerate(source_points):
        # Check if the line turns or split
        split = False
        if len(target_points[i]) > 1:
            if (target_points[i][0] < source_points[i] and target_points[i][1] > source_points[i]):
                split = True
            elif (target_points[i][0] > source_points[i] and target_points[i][1] < source_points[i]):
                split = True


        if split:
            lines[turn_height][point] = LINE_SYMBOLS.BRANCH_DOWN.value
        elif target_points[i][0] < source_points[i]:
            lines[turn_height][point] = LINE_SYMBOLS.DIAG_L.value
        elif target_points[i][0] > source_points[i]:
            lines[turn_height][point] = LINE_SYMBOLS.DIAG_R.value
        else:
            lines[turn_height][point] = LINE_SYMBOLS.VER.value
        

        # Draw the horizontal line to the target point
        for target_point in target_points[i]:
            # point: current x position
            # target_point: target x position

            if target_point < point:
                # The line goes to the left
                for j in range(point - 1, target_point, -1):
                    lines[turn_height][j] = LINE_SYMBOLS.HOR.value

                lines[turn_height][target_point] = LINE_SYMBOLS.DIAG_L_B.value
                # Check if this line comes from a split
                if len(target_points[i]) > 1:
                    other_point: int = target_points[i][1] if target_points[i][0] == target_point else target_points[i][0]
                    if other_point < target_point:
                        lines[turn_height][other_point] = LINE_SYMBOLS.BRANCH_UP.value


            elif target_point > point:
                # The line goes to the right
                for j in range(point + 1, target_point):
                    lines[turn_height][j] = LINE_SYMBOLS.HOR.value 

                lines[turn_height][target_point] = LINE_SYMBOLS.DIAG_R_B.value
                # Check if this line comes from a split
                if len(target_points[i]) > 1:
                    other_point: int = target_points[i][1] if target_points[i][0] == target_point else target_points[i][0]
                    if other_point > target_point:
                        lines[turn_height][other_point] = LINE_SYMBOLS.BRANCH_UP.value

        
        # Draw the upward lines, from height = 0 to height = turn_height
    for lvl in range(turn_height + 1, height):
        for points in target_points:
            for point in points:
                lines[lvl][point] = LINE_SYMBOLS.VER.value

    
    # Join the lines
    txt = ""
    for i in range(height - 1, 0, -1):
        txt += ''.join(lines[i]) + "\n"
    
    return txt
    






def draw_upward(root: Individual, depth: int, width: int) -> str:
    """Draw the genealogical tree starting of the given Individual root and
    going up in the generations (parents).

    Args:
        root (Individual): The root of the tree.
        width (int): The width of the tree, in chars.

    Returns:
        str: The tree as a string.
    """
    
    lines = []

    # Add d layers
    for d in range(depth):

        source_centers: list[int] = get_spaced_points(2 ** d, width)
        flat_target_points: list[int] = get_spaced_points(2 ** (d + 1), width)
        target_points: list[list[int]] = [flat_target_points[i:i + 2] for i in range(0, len(flat_target_points), 2)]
        
        source_names: list[dict] = root.get_individuals_names(d)
        lines.append(name_line(source_names, width, source_centers))
        lines.append(connecting_lines(source_centers, target_points, width).rstrip())

    # Add the final layers, the names of the d generation

    source_centers: list[int] = get_spaced_points(2 ** depth, width)
    source_names: list[dict] = root.get_individuals_names(depth)

    lines.append(name_line(source_names, width, source_centers))

    
    # Reverse the line list
    lines.reverse()
    # Return the lines, as string
    return '\n'.join(lines)




def draw_downward(root: Individual, depth: int, width: int) -> str:
    """Draw the genealogical tree starting of the given Individual root and
    going down in the generations (children).

    Args:
        root (Individual): The root of the tree.
        width (int): The width of the tree, in chars.

    Returns:
        str: The tree as a string.
    """
    
    lines = []

    # Add d layers
    for d in range(depth):

        source_centers: list[int] = get_spaced_points(2 ** d, width)
        flat_target_points: list[int] = get_spaced_points(2 ** (d + 1), width)
        target_points: list[list[int]] = [flat_target_points[i:i + 2] for i in range(0, len(flat_target_points), 2)]
        
        source_names: list[dict] = root.get_individuals_names(d)
        lines.append(name_line(source_names, width, source_centers))
        lines.append(connecting_lines(source_centers, target_points, width).rstrip())

    # Add the final layers, the names of the d generation

    source_centers: list[int] = get_spaced_points(2 ** depth, width)
    source_names: list[dict] = root.get_individuals_names(depth)

    lines.append(name_line(source_names, width, source_centers))

    
    # Reverse the line list
    lines.reverse()
    # Return the lines, as string
    return '\n'.join(lines)