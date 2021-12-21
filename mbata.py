import pygame
import random

#Inisialisasi game
pygame.font.init()
pygame.mixer.init()

# Variabel Global
s_width = 650
s_height = 650
play_width = 300
play_height = 600
block_size = 30

top_left_x = (s_width - play_width) // 3
top_left_y = s_height - play_height

#sounds
sound_move = pygame.mixer.Sound("resource\sound\MOVE.wav")
sound_rotasi = pygame.mixer.Sound("resource\sound\ROTASI.wav")
sound_rowclear = pygame.mixer.Sound("resource\sound\CLEAR.wav")
sound_gameover = pygame.mixer.Sound("resource\sound\END.wav")
sound_win = pygame.mixer.Sound("resource/sound/win.wav")

# Format Shapes

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 shapes
 
class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    #methode gambar tombol
    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            font = pygame.font.Font("resource\Bodo Amat.ttf", 50)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    #cek apakah cursor di atas tombol
    def is_over(self, pos):
        #Pos adalah posisi mouse atau tuple (x,y)
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape

        #warna ditentukan oleh index dari bentuk
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions = {}):
    #membuat grid
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    #cek apakah sudah ada blok warna di grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

def convert_shape_format(shape):
    #simpan posisi '0'
    positions = []

    #rotasi
    format = shape.shape[shape.rotation % len(shape.shape)]

    #cek bentuk
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    #menghilangkan offset

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
 
    return positions

def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]

    #buat list jadi 1 dimensi
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
 
    return True

def check_lost(positions):
    #Cek jika shapes berhenti di atas layar
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    global shapes, shape_colors

    #memilih shapes random
    return Piece(5, 0, random.choice(shapes))
 
 
def draw_text_middle(text, size, color, surface, offset=0, judul = False):
    if judul == True:
        font = pygame.font.Font("resource\Sketch Wall.ttf", size)
    else:
        font = pygame.font.Font("resource\Bodo Amat.ttf", size)
    label = font.render(text, 1, color)
    
    surface.blit(label, (top_left_x + play_width/2 + 60 - (label.get_width() / 2), top_left_y + play_height/2 + offset - label.get_height()/2))

def draw_grid(surface, row, col):
    gx = top_left_x
    gy = top_left_y

    for i in range (row):
        pygame.draw.line(surface, (128,128,128), (gx, gy+ i*block_size), (gx+play_width, gy+ i*block_size))
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (gx+ j*block_size, gy), (gx+ j*block_size, gy+play_height))

def clear_rows(grid, locked):
    inc = 0
    
    #cek grid, apakah row memiliki block kosong
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            
            #posisi baris yang harus di hapus
            ind = i
            #hapus baris
            
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    #pindahkan row di atas cleared row ke bawah
    if inc > 0:
        pygame.mixer.Sound.play(sound_rowclear)
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newkey = (x, y + inc)
                locked[newkey] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface):
    #label
    font = pygame.font.Font("resource\Bodo Amat.ttf", 30)
    label = font.render('Sakwise', 1, (255,255,255))
    
    #lokasi label
    sx = top_left_x + play_width + 65
    sy = top_left_y + play_height/2 - 100
    
    #display shape selanjutnya
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    #cetak label
    surface.blit(label, (sx , sy - 60))

def draw_window(surface, grid, score):
	#menggambar windows gameplay
    surface.fill((153, 176, 176))

    #mengambar label "Game Kotak"
    pygame.font.init()
    font = pygame.font.Font("resource\Bodo Amat.ttf", 30)
    label = font.render('MBATA', 0, (250, 250, 250))
    surface.blit(label, (top_left_x + play_width/2 - label.get_width()/2, 10))

    #Cetak score
    font = pygame.font.Font("resource\Bodo Amat.ttf", 30)
    label = font.render('Bijine : ' + str(score), 1, (255,255,255))
    #lokasi label
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    #cetak label
    surface.blit(label, (sx + 10, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    #gambar border
    pygame.draw.rect(surface, (255,255,255), (top_left_x, top_left_y, play_width, play_height), 4)

    #gambar grid
    draw_grid(surface, 20, 10)

def main(win):
    #Variabel
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    game_run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.25
    score = 0
    cleared_rows= 0
    total_cleared = 0

    #game loop
    while game_run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        #Iterasi gerakan shapes
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                pygame.mixer.Sound.play(sound_move)
                current_piece.y -=1
                change_piece = True

        #events check
        for event in pygame.event.get():
            #Player quit
            if event.type == pygame.QUIT:
                game_run == False
                pygame.display.quit()
            #key press
            if event.type == pygame.KEYDOWN:
                #Gerakan shapes
                if event.key == pygame.K_LEFT:
                    pygame.mixer.Sound.play(sound_move)
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    pygame.mixer.Sound.play(sound_move)
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    pygame.mixer.Sound.play(sound_move)
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    pygame.mixer.Sound.play(sound_rotasi)
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
        #convert posisi
        shape_pos = convert_shape_format(current_piece)

        #Gambar shape
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        #shape menyentuh ground
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            #score
            cleared_rows += clear_rows(grid, locked_positions)
            total_cleared += cleared_rows
            if cleared_rows > 3:
                score += (cleared_rows * 10)*2
            else :
                score += cleared_rows * 10
            cleared_rows = 0
        #cek score
        #tambah fall speed
        if total_cleared >= 25:
            fall_speed == 0.15
        #cek win/lose condition
        if total_cleared >=50 or check_lost(locked_positions) == True:
            win.fill((0,0,0))
            draw_text_middle("UWIS BUBAR", 50, (255,255,255), win, -250)
            if total_cleared >=50:
                draw_text_middle("Bisane menang", 50, (255,255,255), win, -100)
                pygame.mixer.Sound.play(sound_win)
            else :
                draw_text_middle("Deneng Kalah", 40, (255,255,255), win, -100)
                pygame.mixer.Sound.play(sound_gameover)
            pygame.display.update()
            pygame.time.delay(1500)
            game_run = False

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()




def main_menu(win):
    run = True
    #background music
    music = pygame.mixer.music.load("resource\sound\BACKGROUND.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    #Tombol start
    start_button = button((50,168,84), top_left_x + play_width/2 - 110, top_left_y + play_height/2  - 100, 350, 150, "Mlebu")
    exit_button = button((00, 149, 237), top_left_x + play_width/2 - 110, top_left_y + play_height/2  +100 , 350, 150, "Metu")
    while run :
        win.fill((138, 43, 226))
        draw_text_middle("NUMPUK BATA", 80, (0,0,0), win, -280, True)
        start_button.draw(win, (0,0,0))
        exit_button.draw(win, (0,0,0))
        pygame.display.update()
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_over(pos):
                    main(win)
                if exit_button.is_over(pos):
                    pygame.display.quit()
            if event.type == pygame.MOUSEMOTION:
                if start_button.is_over(pos):
                    start_button.color = (50,168,84)
                elif exit_button.is_over(pos):
                    exit_button.color = (255, 0, 0) 
                else :
                    start_button.color = (00, 149, 237)
                    exit_button.color = (00, 149, 237)


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('NUMPUK BATA')
main_menu(win)  # start game
