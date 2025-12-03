import math
import heapq

def get_euclidean_distance(node_a, node_b, coords):
    """
    Calculates the straight-line distance between two nodes (Heuristic).
    Formula: sqrt((x2 - x1)^2 + (y2 - y1)^2)
    """
    x1, y1 = coords[node_a]
    x2, y2 = coords[node_b]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def reconstruct_path(came_from, current):
    """
    Backtracks from the Goal to the Start using the 'came_from' dictionary
    to build the clean final path.
    """
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    # The path is currently Goal -> Start, so we reverse it
    return total_path[::-1]

def a_star_search(start_node, goal_node, graph, coords):
    """
    Executes A* Search logic.
    
    Args:
        start_node (str): ID of starting node
        goal_node (str): ID of target node
        graph (dict): Adjacency list {'node': [('neighbor', cost)]}
        coords (dict): Coordinate list {'node': (x, y)}
        
    Returns:
        list: The sequence of nodes representing the shortest path.
    """
    
    # Priority Queue stores tuples: (f_score, current_node)
    # f_score = g_score (actual cost) + h_score (heuristic estimate)
    open_set = []
    heapq.heappush(open_set, (0, start_node))
    
    # Keeps track of where we came from to rebuild path later
    came_from = {}
    
    # g_score: Cost of getting from Start to current node
    # Default to infinity for all nodes except start
    g_score = {node: float('inf') for node in coords}
    g_score[start_node] = 0
    
    # f_score: g_score + heuristic cost to goal
    f_score = {node: float('inf') for node in coords}
    f_score[start_node] = get_euclidean_distance(start_node, goal_node, coords)

    # Set to keep track of items in the priority queue (for lookup speed)
    open_set_hash = {start_node}

    while open_set:
        # Pop the node with the lowest f_score
        current = heapq.heappop(open_set)[1]
        open_set_hash.remove(current)

        # 1. Check if we reached the goal
        if current == goal_node:
            return reconstruct_path(came_from, current)

        # 2. Explore Neighbors
        # graph[current] gives us a list of neighbors: [('neighbor_id', weight), ...]
        if current in graph:
            for neighbor, weight in graph[current]:
                # Calculate tentative g_score (Current cost + distance to neighbor)
                tentative_g_score = g_score[current] + weight

                # If this path to neighbor is better than any previous one, record it!
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    
                    # Calculate f_score (Actual cost + Heuristic)
                    h_score = get_euclidean_distance(neighbor, goal_node, coords)
                    f_score[neighbor] = tentative_g_score + h_score
                    
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)

    # If we get here, no path was found
    print(f"No path found from {start_node} to {goal_node}")
    return []