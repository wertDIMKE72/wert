#создай игру "Лабиринт"!
from pygame import *
from time import *

WIN_W, WIN_H = 750, 500
RAZM = 40
#цвета
BLACK = (0, 0, 0)
GREEN = (36, 255, 10)

init()
#окно
window = display.set_mode((WIN_W,WIN_H))
display.set_caption('maze')
#класс
class Sprite():
    def __init__(self, img, x, y, w, h):
        self.image = transform.scale(image.load(img),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Area:
    def __init__(self, x = 40, y = 240, widh = 90, vusota = 200, color = None):
        self.rect = Rect(x, y, widh, vusota)
        self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        draw.rect(window, self.fill_color, self.rect)
        
    def set_text(self, text, frize=70, text_color=(0,0,0)):
        self.image = font.SysFont('freesansbold', frize).render(text, True, text_color)

    def draw(self, shift_x = 0, shift_y = 0):
        self.fill()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)  
#объекты
lab = Sprite('lab.png', 0, 0, WIN_W, WIN_H)
background = Sprite('background.jpg', 0, 0, WIN_W, WIN_H)
cyborg = Sprite('cyborg.png', 600, 350, RAZM, RAZM)
hero = Sprite('hero.png', 10, 460, RAZM, RAZM)
zoloto = Sprite('treasure.png', 650, 450, RAZM, RAZM)
knopka = Area(180, 200, 360, 70, GREEN)
#звуки
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.set_volume(8)
mixer.music.play(-1)
zvuk_vraga = mixer.Sound('kick.ogg')
zvuk_zoloto = mixer.Sound('money.ogg')
#FPS
last_time = time()
new_time = time()
#запуск игры
game = True
enemy_speed = 300
#текст
shrift = font.SysFont('freesansbold', 70)
text1 = shrift.render('Вы победили', True, BLACK)
#переменная флаг
enemy_touch = False
zoloto_touch = False
while game:
    #FPS
    last_time = new_time
    new_time = time()
    delta = new_time - last_time
    #показ изображений
    background.draw()
    lab.draw()
    zoloto.draw()    
    #прикосновение игрока охранника

    if enemy_touch:
        knopka.set_text('Вы проиграли')
        knopka.draw(10, 10)
        
    else:#движение и рисование игрока
        hero.draw()
        x = hero.rect.x
        y = hero.rect.y
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and hero.rect.y > 0:
            hero.rect.y -= 300 * delta
        if keys_pressed[K_s] and hero.rect.y < WIN_H - RAZM:
            hero.rect.y += 300 * delta  
        if keys_pressed[K_d] and hero.rect.x < WIN_W - RAZM:
            hero.rect.x += 300 * delta
        if keys_pressed[K_a] and hero.rect.x > 0:
            hero.rect.x -= 300 * delta 

        if sprite.collide_mask(hero, lab):
            hero.rect.x = x
            hero.rect.y = y
    #прикосновение игрока охранника после поражения
    if hero.rect.colliderect(zoloto.rect):
        zoloto_touch = True
        zvuk_zoloto.play()
    if zoloto_touch:
        knopka.set_text('Вы выиграли')
        knopka.draw(10, 10)
        
    else:#рисование и охранника 
        cyborg.draw()
        if hero.rect.colliderect(cyborg.rect):
            enemy_touch = True
            zvuk_vraga.play()
    cyborg.rect.x += enemy_speed * delta
    if cyborg.rect.x >= WIN_W - RAZM:
        enemy_speed = -300
    if cyborg.rect.x <= WIN_W - RAZM - 225:
        enemy_speed = 300

    #закрывание на крестик
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x, y = e.pos
            if knopka.collidepoint(x, y):
                hero.rect.x = 10
                hero.rect.y = 460
                enemy_touch = False
                
                zoloto_touch = False
    #обновление экрана
    display.update()
    