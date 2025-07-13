from src.controller import MinesweeperAI

def main():
    ai = MinesweeperAI()
    ai.run()

if __name__ == "__main__":
    main()

# 843 lines of code in total
# Project Directory Structure
# main.py
# src
# ├── controller.py   <- controls game logic
# ├── core            <- core classes like board and cell
# │   └── board.py
# │   └── cell.py
# ├── vision          <- image processing and display
# │   ├── img_proc.py
# │   └── display.py
# ├── algorithms      <- algorithms to solve the game
# │   ├── solver.py (controls the others)
# │   ├── basic.py
# │   ├── set.py
# │   └── constraint.py
# └── util            <- utility classes
#     ├── logger.py
#     ├── time.py
#     └── settings.py
