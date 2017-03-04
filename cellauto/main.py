import core
from cellauto.grids import life, ant

def main():
    lg = life.LifeGrid(10, 10)
    ag = ant.AntGrid(30, 30, 20, 20)

    with core.GridWin() as disp:
        disp.add_game(ag)
        disp.run_prog()

if __name__ == '__main__':
    main()
