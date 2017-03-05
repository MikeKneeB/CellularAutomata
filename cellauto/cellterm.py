#!/usr/bin/python

from cellauto.displays import terminal

def main():
    with terminal.TermWin() as disp:
        disp.run_prog()

if __name__ == '__main__':
    main()
