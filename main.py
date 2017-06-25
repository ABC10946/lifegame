import sys
import curses
from lifegame import *


def main():
    lifegame = LifeGame("[]","__")
    main_loop_flag = True
    width = 0
    height = 0
    if len(sys.argv) == 3:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        lifegame.gen_field(width,height)

    elif len(sys.argv) == 2:
        f_name = sys.argv[1]
        file_handler = lifegame.load_field(f_name)
        if file_handler == 0:
            print("File load successful.")
            width = lifegame.width
            height = lifegame.height
        elif file_handler == -1:
            print("File not found.")
            main_loop_flag = False

    else:
        main_loop_flag = False
        print("python main.py <width> <height>")
        print("python main.py <filename>")

    screen = curses.initscr()
    screen_height,screen_width = screen.getmaxyx()
    if screen_height <= height or screen_width <= width:
        print("Window size is too small to show field. (" + str(int((screen_width-1)/2)) + "," + str(screen_height-2) + ")")
        main_loop_flag = False

    curses.noecho()
    curses.cbreak()


    if main_loop_flag:
        x = 0
        y = 1
        playFlag = False
        while True:
            screen.timeout(100)
            screen.clear()
            screen.addstr(0,0,"STEP:"+str(lifegame.output_step())+",play:"+("True" if playFlag else "False"))
            screen.addstr(1,0,"q to escape program,s to next_step,hjkl to move cursor,c to clear field,o to change cell state,w to save field")
            screen.addstr(2,0,lifegame.output_field())
            screen.addstr(y+1,x*2,"XX")
            c = screen.getch()
            if c == ord("q"):
                break
            elif c == ord("s"):
                lifegame.next_step()
            elif c == ord("h"):
                if x > 0:
                    x -= 1
            elif c == ord("j"):
                if y < lifegame.height-1:
                    y += 1
            elif c == ord("k"):
                if y > 1:
                    y -= 1
            elif c == ord("l"):
                if x < lifegame.width-1:
                    x += 1
            elif c == ord("c"):
                lifegame.clear_field()
            elif c == ord("p"):
                playFlag = False if playFlag else True
            elif c == ord("o"):
                if lifegame.get_state(x,y-1):
                    lifegame.dead(x,y-1)
                else:
                    lifegame.life(x,y-1)
            elif c == ord("w"):
                lifegame.save_field("save.dump")

            if playFlag:
                lifegame.next_step()

    curses.noecho()
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    main()
