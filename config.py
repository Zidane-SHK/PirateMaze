"""
Purpose: Defines the ship's graph structure for A* pathfinding algorithm
Scenario: Help Lethal Luke collect 4 cannonballs and load all cannons to reach the finish

Constraints:
- Luke can only carry one cannonball at a time
- Cannot climb over barrels or retrace steps
- Must collect all 4 cannonballs before reaching finish
"""

# ===== SCREEN SETTINGS =====
# Display dimensions for visualization (portrait orientation for ship image)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1200
FPS = 60

# ===== NODE COORDINATES =====
# All 50 nodes mapped to (x, y) pixel position on the screen
# Coordinates scaled to fit within SCREEN_WIDTH x SCREEN_HEIGHT
# Based on the complete labeled graph image with ship layout
# Y-axis: 0 (top of screen) to SCREEN_HEIGHT (bottom of screen)
# X-axis: 0 (left of screen) to SCREEN_WIDTH (right of screen)


# ===== GRAPH STRUCTURE =====
# Adjacency list: node -> [(neighbor, edge_weight), ...]
# Edge weights (1, 2, or 3) represent movement cost between nodes
# All 50 nodes with complete connections based on the graph overlay

COORDS = {
    # Node ID : (x, y) coordinates
    # Deck 0 (Bottom Deck)
    '1': (448, 1104),

    # Deck 1
    '2': (327, 1020),
    '3': (552, 1013),
    '4': (606, 988),
    '5': (702, 1012),

    # Deck 2
    '6': (488, 927),
    '7': (679, 922),
    '8': (796, 921),
    '9': (845, 917),
    '10': (362, 924),
    '11': (319, 911),
    '12': (225, 921),

    # Deck 3
    '13': (153, 839),
    '14': (285, 842),
    '15': (437, 842),
    '16': (577, 838),
    '17': (652, 826),
    '18': (743, 836),
    '19': (839, 833),
    '20': (920, 790),
    '21': (327, 809),

    # Deck 4
    '22': (188, 745),
    '23': (324, 729),
    '24': (456, 731),
    '25': (604, 731),
    '26': (670, 740),
    '27': (775, 726),
    '37': (108, 699),

    # Deck 5
    '28': (793, 632),
    '29': (877, 581),
    '30': (719, 618),
    '31': (628, 627),
    '32': (596, 626),
    '33': (416, 627),
    '34': (451, 600),
    '35': (351, 633),
    '36': (212, 630),

    # Deck 6
    '38': (234, 539),
    '39': (416, 536),
    '40': (529, 533),
    '41': (579, 531),
    '42': (683, 538),
    '43': (745, 525),

    # Deck 7
    '44': (778, 442),
    '45': (571, 445),
    '46': (478, 425),
    '47': (383, 445),
    '48': (249, 425),

    # Deck 8 (Top Deck)
    '49': (348, 343),
    '50': (665, 340),
   
}

# --- 2. ADJACENCY LIST (The Graph) ---
# Defines valid paths. If a connection is missing here, the pirate cannot walk there.
# Format: 'Node_ID': [('Neighbor_ID', cost), ...]
GRAPH = {
    # Deck 0
    '1': [('2', 1), ('3', 1)],
    
    # Deck 1
    '2': [('1', 1), ('3', 2), ('10', 1)],
    '3': [('1', 1), ('2', 2), ('4', 1),],
    '4': [('3', 1), ('5', 3), ('7', 1), ('6',3)],
    '5': [('4', 3), ('8', 1)],
    
    # Deck 2
    '6': [('4', 3), ('16', 3), ('10', 2)],
    '7': [('4', 1), ('18', 3)],
    '8': [('5', 1), ('9', 1), ('18', 3)],
    '9': [('19', 3), ('8', 1)],
    '10': [('6', 2), ('11', 1)],
    '11': [('10',1)],
    '12': [('13', 1), ('14', 1)],
    
    # Deck 3
    '13': [('12', 1), ('22',1)],
    '14': [('12', 1), ('21', 1)],
    '15': [('21', 2), ('16', 2)],
    '16': [('6', 3), ('15', 2), ('17',3)],
    '17': [('18', 1), ('16', 3)],
    '18': [('8', 3), ('17', 1), ('19', 2)],
    '19': [('9', 3), ('18', 2), ('20', 3)],
    '20': [('19', 3), ('27', 1)],
    '21': [('14', 1), ('15', 2), ('24', 3),('23',1),('22',3)],
    
    # Deck 4
    '22': [('13', 1), ('21', 3), ('23', 2), ('37', 1)],
    '23': [('35', 2), ('22', 2), ('21', 1)],
    '24': [('21', 3), ('25', 3)],
    '25': [('26', 1), ('24', 3)],
    '26': [('27', 2), ('25',1))],
    '27': [('28', 2), ('26', 2), ('20', 1)],
    '37': [('22', 1), ('36', 1)],
  
    # Deck 5
    '28': [('29',_), ('27', 2), ('30', 1)],
    '29': [('28', ), ('43', 1)],
    '30': [('28', 1), ('31', 1)],
    '31': [('32',_), ('30', 1), ('42', 3)],
    '32': [('34', 1), ('31',_)],
    '33': [('35', 1), ('34', 2)],
    '34': [('39', 3), ('33', 2), ('32', 1), ('41', 2),('40', 1)],
    '35': [('36', 2), ('33', 1), ('23', 2)],
    '36': [('37', 1), ('35', 2), ('38', 2)],
    
    # Deck 6
    '38': [('36', 2), ('39', 2)],
    '39': [('34', 3), ('38', 2)],
    '40': [('34', 1), ('41', _)],
    '41': [('42', 2), ('34', 2), ('40', _)],
    '42': [('43', 2), ('41', 2), ('31', 3)],
    '43': [('42', 2), ('29', 1)],
    
    # Deck 7
    '44': [('50', 1), ('45', 1)],
    '45': [('46', 1), ('44', 1)],
    '46': [('49', 2), ('50', 3), ('45', 1), ('47', 1)],
    '47': [('46', 1), ('48', 1)],
    '48': [('49', 3), ('47', 1)],
    
    # Deck 8 (Top)
    '49': [('46', 2), ('48', 3)],  # FINISH node (black)
    '50': [('44', 1), ('46', 3)],  # START node (green)
}

CANNONBALL_NODES = [
    '4',   # Gray node on Deck 1
    '21',  # Gray node on Deck 3
    '34',  # Gray node on Deck 5
    '46',  # Gray node on Deck 7
]
# Reverse mapping: node to deck level
NODE_TO_DECK = {}
for deck, nodes in DECK_LEVELS.items():
    for node in nodes:
        NODE_TO_DECK[node] = deck


def get_all_nodes():
    """Returns a list of all node IDs in the graph."""
    return list(COORDS.keys())

def get_cannonball_count():
    """Returns the number of cannonballs available."""
    return len(CANNONBALL_NODES)

def is_cannonball_node(node):
    """Check if a given node contains a cannonball."""
    return node in CANNONBALL_NODES

def get_node_type(node):
    """
    Returns the type of node for visualization purposes.
    Types: 'start', 'finish', 'cannonball', 'regular'
    """
    if node == START_NODE:
        return 'start'
    elif node == FINISH_NODE:
        return 'finish'
    elif node in CANNONBALL_NODES:
        return 'cannonball'
    else:
        return 'regular'

def get_deck_level(node):
    """Returns the deck level (0-8) for a given node."""
    return NODE_TO_DECK.get(node, -1)

def get_nodes_on_deck(deck_num):
    """Returns a list of all nodes on a specific deck."""
    return DECK_LEVELS.get(deck_num, [])

def validate_graph():
    """
    Validates that the graph structure is consistent.
    Checks for:
    - All nodes in GRAPH exist in COORDS
    - All neighbor references are valid
    - Bidirectional edges have matching weights (optional check)
    """
    errors = []
    
    # Check all graph nodes exist in coordinates
    for node in GRAPH:
        if node not in COORDS:
            errors.append(f"Node '{node}' in GRAPH but not in COORDS")
    
    # Check all neighbors exist
    for node, neighbors in GRAPH.items():
        for neighbor, weight in neighbors:
            if neighbor not in COORDS:
                errors.append(f"Neighbor '{neighbor}' of '{node}' not in COORDS")
            if neighbor not in GRAPH:
                errors.append(f"Neighbor '{neighbor}' of '{node}' not in GRAPH")
    
    # Check special nodes exist
    if START_NODE not in COORDS:
        errors.append(f"START_NODE '{START_NODE}' not in COORDS")
    if FINISH_NODE not in COORDS:
        errors.append(f"FINISH_NODE '{FINISH_NODE}' not in COORDS")
    
    for i, cannon_node in enumerate(CANNONBALL_NODES):
        if cannon_node not in COORDS:
            errors.append(f"CANNONBALL_NODES[{i}] '{cannon_node}' not in COORDS")
    
    if errors:
        print("Graph validation errors found:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("Graph validation successful!")
        print(f"Total nodes: {len(COORDS)}")
        print(f"Total edges: {sum(len(neighbors) for neighbors in GRAPH.values())}")
        print(f"Start: Node {START_NODE} (Deck {get_deck_level(START_NODE)})")
        print(f"Finish: Node {FINISH_NODE} (Deck {get_deck_level(FINISH_NODE)})")
        print(f"Cannonballs: {CANNONBALL_NODES}")
        return True

def print_graph_summary():
    """Prints a summary of the graph structure."""
    print("=" * 60)
    print("CANNON CHALLENGE - GRAPH SUMMARY")
    print("=" * 60)
    print(f"Total Nodes: {len(COORDS)}")
    print(f"Total Connections: {sum(len(neighbors) for neighbors in GRAPH.values())}")
    print(f"\nStart Node: {START_NODE} (Green, Deck {get_deck_level(START_NODE)})")
    print(f"Finish Node: {FINISH_NODE} (Black, Deck {get_deck_level(FINISH_NODE)})")
    print(f"\nCannonball Locations:")
    for i, node in enumerate(CANNONBALL_NODES, 1):
        print(f"  Cannonball {i}: Node {node} (Gray, Deck {get_deck_level(node)})")
    print(f"\nNodes per Deck:")
    for deck in range(9):
        nodes = get_nodes_on_deck(deck)
        print(f"  Deck {deck}: {len(nodes)} nodes - {nodes}")
    print("=" * 60)

# Run validation if this file is executed directly
if __name__ == "__main__":
    print_graph_summary()
    print()
    validate_graph()
