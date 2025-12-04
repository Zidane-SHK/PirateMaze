import math
import heapq

def get_euclidean_distance(node_a, node_b, coords):
    """Standard Euclidean Heuristic (h1)."""
    if node_a not in coords or node_b not in coords:
        # Safety check for missing coordinates
        return float('inf')
    x1, y1 = coords[node_a]
    x2, y2 = coords[node_b]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def get_distance_to_human_path(current_node, human_path_list, coords):
    """
    Human Bias Heuristic (h2).
    Calculates the minimum distance from the current node to ANY node 
    in the human solution list.
    """
    if not human_path_list:
        return 0
    
    min_dist = float('inf')
    
    # Find the closest point in the human solution to our current position
    for path_node in human_path_list:
        dist = get_euclidean_distance(current_node, path_node, coords)
        if dist < min_dist:
            min_dist = dist
            
    return min_dist

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path[::-1]

def a_star_search(start_node, goal_node, graph, coords, human_path=None):
    """
    A* Search with Dual Heuristics:
    f(n) = g(n) + h_goal(n) + (W * h_human(n))
    """
    
    open_set = []
    heapq.heappush(open_set, (0, start_node))
    
    came_from = {}
    
    # g_score: Cost from start
    g_score = {node: float('inf') for node in coords}
    g_score[start_node] = 0
    
    # f_score: Total estimated cost
    f_score = {node: float('inf') for node in coords}
    
    # --- HEURISTIC CONFIGURATION ---
    # Weight for Human Path Bias. 
    # 2.5 gives a very strong bias towards the human path.
    HUMAN_BIAS_WEIGHT = 2.5 
    
    # Initial H calc
    h1 = get_euclidean_distance(start_node, goal_node, coords)
    h2 = get_distance_to_human_path(start_node, human_path, coords)
    f_score[start_node] = h1 + (HUMAN_BIAS_WEIGHT * h2)

    open_set_hash = {start_node}

    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current not in open_set_hash:
            continue
        open_set_hash.remove(current)

        if current == goal_node:
            return reconstruct_path(came_from, current)

        if current in graph:
            for neighbor, weight in graph[current]:
                
                # Prevent immediate backtracking (ladder bounce)
                if current in came_from and neighbor == came_from[current]:
                    continue

                tentative_g_score = g_score[current] + weight

                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    
                    # --- DUAL HEURISTIC CALCULATION ---
                    h1_goal = get_euclidean_distance(neighbor, goal_node, coords)
                    h2_human = get_distance_to_human_path(neighbor, human_path, coords)
                    
                    # Final Score
                    f_score[neighbor] = tentative_g_score + h1_goal + (HUMAN_BIAS_WEIGHT * h2_human)
                    
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)

    print(f"No path found from {start_node} to {goal_node}")
    return []