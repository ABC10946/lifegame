import copy
import pickle

class LifeGame():
    def __init__(self,life_cell_char,dead_cell_char):
        self.step = 0
        self.field = []
        self.life_cell_char = life_cell_char
        self.dead_cell_char = dead_cell_char

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
        return "\n".join(["".join([(self.life_cell_char if x else self.dead_cell_char) for x in y]) for y in self.field])

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
            return 0

        except FileNotFoundError:
            return -1
