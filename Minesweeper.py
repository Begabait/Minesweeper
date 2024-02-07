import pygame
import random
from copy import copy


pygame.init()

WIDTH, HEIGHT = 931, 581
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minesweeper')
pygame.display.set_icon(pygame.image.load('icon.png'))
clock = pygame.time.Clock()
start_time = 0
generated_mines = False
N_MINES = 99

BLACK = (0, 0, 0)
LIGHT_BLUE = (32, 105, 214)
LIGHTER_BLUE = (114, 163, 237)
LIGHT_GREY = (213, 223, 232)
WHITE = (255, 255, 255)

# MINES COLORS
COLORS = {1:(18, 67, 227), 2: (5, 74, 21), 3: (196, 7, 0), 4: (7, 35, 130), 5: (99, 13, 5), 6: (5, 162, 176), 7: (196, 7, 0), 8: (196, 7, 0)}


clock_image = pygame.image.load('clock.png')
bomb_image = pygame.image.load('mine.png')
flag_image = pygame.image.load('new_flag.png')

stat_font = pygame.font.Font('stat_font.ttf', 40)
num_font = pygame.font.Font('stat_font.ttf', 30)


class Square(object):

    def __init__(self, column, line):
        self.col = column
        self.row = line
        self.covered = True
        self.mine = False
        self.num = 0
        self.flagged = False

    def draw_covered(self):
        position = pygame.mouse.get_pos()
        column = position[0] // 31
        line = position[1] // 31
        if column == self.col and line == self.row:
            color = LIGHTER_BLUE
        else:
            color = LIGHT_BLUE
        pygame.draw.rect(win, color, (self.col * 31 + 1, self.row * 31 + 1, 30, 30), 0, 2)
        if self.flagged:
            win.blit(flag_image, (self.col * 31 + 7, self.row * 31 + 6))

    def draw_open(self):
        pygame.draw.rect(win, LIGHT_GREY, (self.col * 31 + 1, self.row * 31 + 1, 30, 30))
        if not self.mine and self.num:
            text = num_font.render(str(self.num), True, COLORS[self.num])
            win.blit(text, (self.col * 31 + 16 - (text.get_width() / 2), self.row * 31 + 17 - (text.get_height() / 2)))


def generate_mines(col, row):
    untouchable = {(col-2, row-2), (col-1, row-2), (col, row-2), (col+1, row-2), (col+2, row-2),
                   (col-2, row-1), (col-1, row-1), (col, row-1), (col+1, row-1), (col+2, row-1),
                        (col-2, row), (col-1, row), (col, row), (col+1, row), (col+2, row),
                   (col-2, row+1), (col-1, row+1), (col, row+1), (col+1, row+1), (col+2, row+1),
                   (col-2, row+2), (col-1, row+2), (col, row+2), (col+1, row+2), (col+2, row+2)}

    untouchables = [30 * b + a if (0 <= a <= 29) and (0 <= b <= 15) else -1 for (a,b) in untouchable]

    population = []
    for num in range(480):
        if num not in untouchables:
            population.append(num)
    mines_list = random.sample(population, k=99)
    mines_coordinates = []
    for mine in mines_list:
        column = mine % 30
        line = mine // 30
        mines_coordinates.append([column, line])

    return mines_coordinates, True


def generate_nums(mines_list, squares_list):

    cor = [[0,0], [29,0], [0,15], [29,15]]
    top = [[x,0] for x in range(1,29)]
    bot = [[x,15] for x in range(1,29)]
    left = [[0,x] for x in range(1,15)]
    right = [[29,x] for x in range(1,15)]

    for mine in mines_list:
        if mine == [0,0]:
            squares_list[0][1].num += 1
            squares_list[1][1].num += 1
            squares_list[1][0].num += 1
        elif mine == [29,0]:
            squares_list[0][28].num += 1
            squares_list[1][28].num += 1
            squares_list[1][29].num += 1
        elif mine == [0,15]:
            squares_list[14][0].num += 1
            squares_list[14][1].num += 1
            squares_list[15][1].num += 1
        elif mine == [29,15]:
            squares_list[14][28].num += 1
            squares_list[14][29].num += 1
            squares_list[15][28].num += 1
        elif mine in top:
            squares_list[1][mine[0]-1].num += 1
            squares_list[1][mine[0]].num += 1
            squares_list[1][mine[0]+1].num += 1
            squares_list[0][mine[0]-1].num += 1
            squares_list[0][mine[0]+1].num += 1
        elif mine in bot:
            squares_list[14][mine[0] - 1].num += 1
            squares_list[14][mine[0]].num += 1
            squares_list[14][mine[0] + 1].num += 1
            squares_list[15][mine[0]-1].num += 1
            squares_list[15][mine[0]+1].num += 1
        elif mine in left:
            squares_list[mine[1]-1][1].num += 1
            squares_list[mine[1]][1].num += 1
            squares_list[mine[1]+1][1].num += 1
            squares_list[mine[1]-1][0].num += 1
            squares_list[mine[1]+1][0].num += 1
        elif mine in right:
            squares_list[mine[1]-1][28].num += 1
            squares_list[mine[1]][28].num += 1
            squares_list[mine[1]+1][28].num += 1
            squares_list[mine[1]-1][29].num += 1
            squares_list[mine[1]+1][29].num += 1
        else:
            # TOP ROW
            squares_list[mine[1]-1][mine[0]-1].num += 1
            squares_list[mine[1]-1][mine[0]].num += 1
            squares_list[mine[1]-1][mine[0]+1].num += 1
            # MIDDLE/SAME ROW
            squares_list[mine[1]][mine[0]-1].num += 1
            squares_list[mine[1]][mine[0]+1].num += 1
            # BOTTOM ROW
            squares_list[mine[1]+1][mine[0]-1].num += 1
            squares_list[mine[1]+1][mine[0]].num += 1
            squares_list[mine[1]+1][mine[0]+1].num += 1

    return squares_list


def find_neighbours(row, col):
    neighbours = set()
    if row-1 >= 0 and col-1 >= 0:
        neighbours.add((row-1,col-1))
        neighbours.add((row-1,col))
        neighbours.add((row,col-1))
    if row-1 >= 0 and col+1 <= 15:
        neighbours.add((row-1,col+1))
        neighbours.add((row-1,col))
        neighbours.add((row,col+1))
    if row+1 <= 15 and col-1 >= 0:
        neighbours.add((row+1,col-1))
        neighbours.add((row,col-1))
        neighbours.add((row+1,col))
    if row+1 <= 15 and col+1 <= 15:
        neighbours.add((row+1,col+1))
        neighbours.add((row,col+1))
        neighbours.add((row+1,col))

    return neighbours


def display_stat(over):
    pygame.draw.rect(win, LIGHT_BLUE, (717, 510, 130, 56), 0, 6)
    pygame.draw.circle(win, WHITE, (110, 538), 27.5)
    pygame.draw.circle(win, WHITE, (677, 538), 27.5)
    win.blit(clock_image, (90, 518))
    win.blit(bomb_image, (657, 518))
    if not over:
        pygame.draw.rect(win, LIGHT_BLUE, (150, 510, 130, 56), 0, 6)
        current_time = str(round((pygame.time.get_ticks() - start_time) / 1000))
        if int(current_time) > 999:
            current_time = '999'
        if start_time == 0:
            current_time = '0'
        text = stat_font.render(current_time, True, WHITE)
        win.blit(text, (215 - (text.get_width() / 2), 538 - (text.get_height() / 2)))
    if n_flagged >= 99:
        n = '0'
    else:
        n = str(99 - n_flagged)
    text = stat_font.render(n, True, WHITE)
    win.blit(text, (782 - (text.get_width() / 2), 538 - (text.get_height() / 2)))


def draw(over, won):
    if won:
        text = stat_font.render('YOU WON!', True, WHITE)
        pygame.draw.rect(win, LIGHT_BLUE, (350, 510, 231, 56), 0, 6)
        win.blit(text, (368, 515))
    elif not over:
        win.fill(BLACK)
        pygame.draw.rect(win, LIGHTER_BLUE, (0, 497, WIDTH, HEIGHT))
    else:
        text = stat_font.render('YOU LOST!', True, WHITE)
        pygame.draw.rect(win, LIGHT_BLUE, (350, 510, 231, 56), 0, 6)
        win.blit(text, (368, 515))

    for line in squares:
        for square in line:
            if square.covered:
                square.draw_covered()
            else:
                square.draw_open()


    display_stat(over)
    pygame.display.update()


# CREATION OF ALL SQUARE INSTANCES, PUN INTENDED
squares = []
for i in range(16):
    squares.append([])
    for j in range(30):
        squares[i].append(Square(j, i))

n_flagged = 0
playing = True
game_over = False
won = False
while playing:
    clock.tick(30)
    draw(game_over, won)

    if not game_over:
        if sum(1 for line in squares for square in line if not square.covered) == 381:
            won = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            break

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pygame.mouse.get_pos()[0] < 931 and pygame.mouse.get_pos()[1] < 497:
                pos = pygame.mouse.get_pos()
                col = pos[0] // 31
                row = pos[1] // 31
                if squares[row][col].mine and not squares[row][col].flagged:
                    game_over = True
                    break
                else:
                    if not squares[row][col].flagged:
                        squares[row][col].covered = False
                        # if not squares[row][col].num:
                        #     cur_neg = find_neighbours(row,col)
                        #     while True:
                        #         new_neg = set()
                        #         for i in cur_neg:
                        #             squares[i[0]][i[1]].covered = False
                        #         for i in cur_neg:
                        #             if squares[i[0]][i[1]].num == 0:
                        #                 new = find_neighbours(i[0],i[1])
                        #                 for j in new:
                        #                     if squares[j[0]][j[1]].covered:
                        #                         new_neg.add(j)
                        #         cur_neg = copy(new_neg)
                        #         if len(cur_neg) == 0:
                        #             break
                    #           TODO FINISH LOOP TO CHECK ALL WHITE SQUARES

                    if not generated_mines:
                        mines, generated_mines = generate_mines(col, row)
                        for [a,b] in mines:
                            squares[b][a].mine = True
                        start_time = pygame.time.get_ticks()
                        squares = generate_nums(mines, squares)
                        for line in squares:
                            for square in line:
                                if not square.mine:
                                    square.covered = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and pygame.mouse.get_pos()[0] < 931 and pygame.mouse.get_pos()[1] < 497:
                pos = pygame.mouse.get_pos()
                col = pos[0] // 31
                row = pos[1] // 31
                if squares[row][col].covered:
                    if squares[row][col].flagged:
                        squares[row][col].flagged = False
                        n_flagged -= 1
                    else:
                        squares[row][col].flagged = True
                        n_flagged += 1


pygame.quit()


# TODO IMPLEMENT LOGIC TO OPEN ALL EMPTY SQUARES UPON FIRST CLICK
# TODO IMPLEMENT LOGIC TO BE ABLE TO OPEN ALL EMPTY SQUARES AROUND A SATISFIED NUMBER
# TODO WIN LOGIC
# TODO STATISTICS