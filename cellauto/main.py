import core
from cellauto.grids import life, ant, multi_ant

def main():
    lg = life.LifeGrid(10, 10)
    ag = ant.AntGrid(40, 80)
    mag = multi_ant.MultiAntGrid(40, 80)

    with core.GridWin() as disp:
        disp.add_game(mag)
        disp.run_prog()

if __name__ == '__main__':
    main()
