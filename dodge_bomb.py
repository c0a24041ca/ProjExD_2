import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT:(+5,0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def check_bound(rct:pg.Rect):
    yoko,tate = True,True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko,tate

def gameover(screen: pg.Surface) -> None:
    
    blackout = pg.Surface((WIDTH, HEIGHT))
    blackout.set_alpha(200)  
    blackout.fill((0, 0, 0))
    screen.blit(blackout, (0, 0))
    font = pg.font.Font(None, 80)
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(txt, txt_rct)

    # 左こうかとん
    left_img = pg.transform.flip(pg.image.load("fig/8.png"), False, False)
    left_img = pg.transform.rotozoom(left_img, 0, 1.0)
    left_rct = left_img.get_rect(center=(WIDTH//2 - 200, HEIGHT//2))
    screen.blit(left_img, left_rct)

    # 右こうかとん
    right_img = pg.image.load("fig/8.png")
    right_img = pg.transform.rotozoom(right_img, 0, 1.0)
    right_rct = right_img.get_rect(center=(WIDTH//2 + 200, HEIGHT//2))
    screen.blit(right_img, right_rct)

    # 画面更新 → 5秒停止
    pg.display.update()
    time.sleep(5)




def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct = bb_img.get_rect()
    kk_rct.centerx = random.randint(0,WIDTH)
    kk_rct.centery = random.randint(0,HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        #if key_lst[pg.K_UP]:
        # sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        # sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        # sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        # sum_mv[0] += 5

        for key , mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #縦方向
                sum_mv[1] += mv[1] #横方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) !=(True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
