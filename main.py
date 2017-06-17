import sys
import copy
import curses
import pickle

class LifeGame():
    def __init__(self):
        self.step = 0
        self.field = []

    def gen_field(self,width,height):
        self.width = width
        self.height = height
        self.field = [[False for x in range(width)] for y in range(height)]
        self.zero_field = copy.deepcopy(self.field)
        self.field_ = copy.deepcopy(self.field)

    def life(self,x_pos,y_pos):
        self.field[y_pos][x_pos] = True

    def dead(self,x_pos,y_pos):
        self.field[y_pos][x_pos] = False

    def get_state(self,x_pos,y_pos):
        return self.field[y_pos][x_pos]

    def count_around_life(self,x_pos,y_pos):
        around_life_count = 0
        for y_delta in range(-1,2):
            for x_delta in range(-1,2):
                if (y_delta != 0 or x_delta != 0) and x_pos+x_delta >= 0 and y_pos+y_delta >= 0 and x_pos+x_delta < self.width and y_pos+y_delta < self.height:
                    if self.field[y_pos+y_delta][x_pos+x_delta]:
                        around_life_count += 1

        return around_life_count


    def next_step(self):
        self.step += 1
        around_life_count = 0
        for y in range(self.height):
            for x in range(self.width):
                around_life_count = self.count_around_life(x,y)

                if around_life_count == 3:
                    self.field_[y][x] = True

                elif around_life_count == 2:
                    if self.field[y][x]:
                        self.field_[y][x] = True
                    else:
                        self.field_[y][x] = False

                elif around_life_count >= 4 or around_life_count <= 1:
                    self.field_[y][x] = False

        self.field = copy.deepcopy(self.field_)
        self.field_ = copy.deepcopy(self.zero_field)

    def output_field(self):
        return "\n".join(["".join([str(int(x)) for x in y]) for y in self.field])

    def output_count_life_field(self):
        print("COUNT LIFE FIELD")
        count_life_field = [list([0 for x in range(self.width)]) for y in range(self.height)]
        for y in range(1,self.height-1):
            for x in range(1,self.width-1):
                count_life_field[y][x] = self.count_around_life(x,y)

        return "\n".join(["".join([str(int(x)) for x in y]) for y in count_life_field])

    def output_step(self):
        return self.step

    def clear_field(self):
        self.field = copy.deepcopy(self.zero_field)

    def save_field(self,filename):
        f = open(filename,"wb")
        pickle.dump(self.field,f)
        f.close()
        return 0

    def load_field(self,filename):
        try:
            f = open(filename,"rb")
            temp_field = pickle.load(f)
            temp_field_width = len(temp_field[0])
            temp_field_height = len(temp_field)

            self.gen_field(temp_field_width,temp_field_height)
            self.field = temp_field

        except FileNotFoundError:
            return -1


def main():
    lifegame = LifeGame()
    main_loop_flag = True
    width = 0
    height = 0
    if len(sys.argv) == 3:
        lifegame = LifeGame()
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        lifegame.gen_field(width,height)

    elif len(sys.argv) == 2:
        f_name = sys.argv[1]
        file_handler = lifegame.load_field(f_name)
        if file_handler == 0:
            print("File load successful.")
        elif file_handler == -1:
            print("File not found.")
            main_loop_flag = False

    else:
        main_loop_flag = False
        print("python main.py <width> <height>")
        print("python main.py <filename>")

    if main_loop_flag:

        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        x = 0
        y = 0
        playFlag = False
        while True:
            screen.timeout(100)
            screen.clear()
            screen.addstr(0,0,"STEP:"+str(lifegame.output_step())+",play:"+("True" if playFlag else "False"))
            screen.addstr(1,0,lifegame.output_field())
            screen.addstr(y+1,x,"x")
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
                if y > 0:
                    y -= 1
            elif c == ord("l"):
                if x < lifegame.width-1:
                    x += 1
            elif c == ord("c"):
                lifegame.clear_field()
            elif c == ord("p"):
                playFlag = False if playFlag else True
            elif c == ord("o"):
                if lifegame.get_state(x,y):
                    lifegame.dead(x,y)
                else:
                    lifegame.life(x,y)
            elif c == ord("w"):
                lifegame.save_field("save.dump")

            if playFlag:
                lifegame.next_step()

        curses.noecho()
        curses.echo()
        curses.endwin()

if __name__ == "__main__":
    main()
