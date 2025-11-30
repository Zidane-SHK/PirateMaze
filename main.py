import pygame
import sys
import time

# importing from the other files
from config import NODES, ADJACENCY_LIST, START_NODE, MISSION_CHECKPOINTS
from visualizer import Visualizer
from algorithm import a_star_search

# animation speed
FPS = 60
MOVE_DELAY = 500 # 500in milisecond before moving onto the next

def solve_mission():
  full_path = []
  current_start = START_NODE

	print(".....Starting Mission calculations.....")

  for target in MISSION_CHECKPOINTS:
    # moving to a mission target ( cannonball 1 , cannon 1 ,..)
    print(f"Calculating segment: {current_start} -> {target}")

    # pushing it far enough to not be able to retrace ( adding a history log )
    segment_path = a_star_search(current_start, target, ADJACENCY_LIST, NODES)

    if not segment_path:
      print(f"Error: No path was found from {current_start} to {target}. Try again")
      return []

		# to avoid copying an already existing connected node
    if full_path:
      full_path.extend(segment_path[1:])
    else:
      full_path.extend(segment_path)

		current_start = target

	print(".....Mission calculated succesfully.....")
	return full_path


def main():

	# initializing the visualizer , loads up the ship image
	viz = Visualizer()
	clock = pygame.time.Clock()

	#running algorithm
	calculated_path = solve_mission()

	# animation setup
	patg_index = 0
	last_move_time = pygame.time.get.ticks()

	# game loop
	running = True
	while running:
		current_time = pygames.time.get.ticks()

		# use of controls ( keyboard / mouse )
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				# resetting animation wheb needed
				if event.key == pygame.K_r:
					path_index = 0

		# animation logic , moving luke to the next node 
		if path_index < len(calculated_path) - 1:
			if current_time - last_move_time > MOVE_DELAY:
				path_index += 1
				last_move_time = current_time

		# id of the current node Luke is on
		current_node_id = calculated_path[path_index] if calculated_path else START_NODE

		# drawing program

		# background ship
		viz.draw_background()

		# invisible graph ( for debugging )
		viz.draw_graph(NODES, ADJACENCY_LIST)

		# solution path
		viz.draw_path_line(calculated_path, NODES)

		# lethal luke at the current position
		viz.draw_player(current_node_id, NODES)

		# updating display
		pygame.display.flip()
		clock.tick(FPS)

	pygame.quit()
	sys.exist()

if __name__ == "__main__":
	main()
	
