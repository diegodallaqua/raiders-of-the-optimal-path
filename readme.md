# Search Algorithms Simulation Project with Pygame
This project was developed as part of the Artificial Intelligence Fundamentals course in the Computer Science program at UTFPR. Its main goal is to simulate and compare classic search algorithms in an interactive visual environment using the `pygame` library.

## Features
- Graphical interface with simulated environment
- Real-time visualization of the agent's movement
- Implementation of the following algorithms:
  - Depth-First Search (DFS)
  - Breadth-First Search (BFS)
  - Greedy Search
  - A* Search
- Performance comparison between the algorithms
- Detection and collection of treasures on the map
- Evaluation of path cost and number of expanded nodes

## Folder Structure
```
raiders_of_the_lost_ark/
├── main.py # Main file that runs the simulation
├── assets/ # Images used for characters and textures
│ └── images/
├── utils/ # Support modules
│ ├── map_generator.py # Map generation and drawing function
│ ├── movement.py # Agent movement logic
│ ├── search_algorithms.py # Search algorithms implementations
│ └── components/ # Interface components like menus and pop-ups
```

## How to Run
1. Make sure Python is installed (version 3.7+ recommended).
2. Install pygame:
```bash
pip install pygame
```
3. Navigate to the project folder and run:
```bash
python main.py
```

## Demonstration
The interface displays the map, objects (agent, treasures, walls), and a sidebar menu with buttons to activate the algorithms. After execution, the route, total cost, and number of collected treasures are shown.
![alt text](assets/images/demonstration_image.png)

## Authors
Developed by Diego Lucas Hattori Dallaqua.

## License
This project is for academic purposes only.