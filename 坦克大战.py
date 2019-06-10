#coding:utf-8
import pygame,sys,time
from pygame.locals import *
from random import randint

class TankeMain():

    pygame.init() #pygame模块初始化
    width=600
    height=500
    # 我方炮弹
    my_missile_list = []
    #开始游戏的方法
    def startGame(self):
        #设置或创建一个窗口
        screem=pygame.display.set_mode((TankeMain.width,TankeMain.height),RESIZABLE,32)
        #设置标题
        pygame.display.set_caption("坦克大战")

        # 我方坦克
        my_tank=My_Tank(screem)
        my_missile=my_tank.fire(screem)
        enemy_list=[]
        for i in range(1,6):
            enemy_list.append(Enemy_Tank(screem))

        while True:
            #设置背景色
            screem.fill((0,0,0))

            my_tank.display()
            my_tank.move()
            for missile in TankeMain.my_missile_list:
                if missile.live:
                    missile.display()
                    missile.move()
                else:
                    TankeMain.my_missile_list.remove(missile)
            for enemy in enemy_list:
                enemy.display()
                enemy.enemy_random_move()
            # 显示字体
            for i, text in enumerate(self.wirte_text(), 0):
                screem.blit(text, (2, 5 + (20 * i)))
            self.get_event(my_tank,screem)
            #设置重置
            time.sleep(0.05)
            pygame.display.update()

    #关闭游戏的方法
    def stopGame(self):
        sys.exit()

    # 窗口显示字体
    def wirte_text(self):
        font=pygame.font.SysFont("华文宋体",20)
        text_sf1=font.render("敌方坦克为：5",True,(255,0,0))
        text_sf2 = font.render("我方炮弹数为：%d"%len(TankeMain.my_missile_list), True, (255, 0, 0))
        return text_sf1,text_sf2

    # 获取事件
    def get_event(self,my_tank,screem):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.stopGame()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    my_tank.direction = "L"
                    my_tank.status=True
                if event.key == K_RIGHT or event.key == K_d:
                    my_tank.direction = "R"
                    my_tank.status=True
                if event.key == K_UP or event.key == K_w:
                    my_tank.direction = "U"
                    my_tank.status=True
                if event.key == K_DOWN or event.key == K_s:
                    my_tank.direction = "D"
                    my_tank.status=True
                if event.key == K_SPACE:
                    TankeMain.my_missile_list.append(my_tank.fire(screem))
                if event.key == K_ESCAPE:
                    self.stopGame()
            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                    my_tank.status = False


# 所有对象的父类
class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

# 坦克类
class Tank(BaseItem):
    # 定义类属性，所有坦克高度和宽度一样
    width=50
    height=50
    def __init__(self,screem,left,top):
        super().__init__()
        self.screem=screem#坦克在移动或显示过程中需要用到当前屏幕
        self.direction="D"#坦克的方向，默认方向往下
        self.speed=5#坦克的速度
        self.status = False  # 坦克初始状态是停止的
        self.images={}#坦克的所有图片
        self.images["L"]=pygame.image.load("images/tankL.gif")
        self.images["R"]=pygame.image.load("images/tankR.gif")
        self.images["U"]=pygame.image.load("images/tankU.gif")
        self.images["D"]=pygame.image.load("images/tankD.gif")
        self.image=self.images[self.direction]#坦克的图片由方向决定
        self.rect=self.image.get_rect()
        self.rect.left=left
        self.rect.top=top
        self.live=True#决定坦克是否消灭了
    # 坦克显示方法
    def display(self):
        self.image=self.images[self.direction]#由方向决定图片
        self.screem.blit(self.image,self.rect)
    # 坦克移动方法
    def move(self):
        if self.status:
            if self.direction == "L":
                if self.rect.left > 0:
                    self.rect.left -=self.speed
                else:
                    self.rect.left = 0
            elif self.direction == "R":
                if self.rect.right < TankeMain.width:
                    self.rect.right += self.speed
                else:
                    self.rect.right = TankeMain.width
            elif self.direction == "U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.rect.top = 0
            elif self.direction == "D":
                if self.rect.bottom <TankeMain.height:
                    self.rect.bottom += self.speed
                else:
                    self.rect.bottom = TankeMain.height
    # 坦克开火方法
    def fire(self):
        pass

# 我方坦克
class My_Tank(Tank):
    def __init__(self,screem):
        super().__init__(screem,270,300)
    # 重写我方坦克开火方法
    def fire(self,screem):
        my_missile=Missile(screem,self)
        return my_missile





# 敌方坦克
class Enemy_Tank(Tank):
    def __init__(self,screem):
        super().__init__(screem,randint(1,5)*100,200)
        self.step=6#定义敌方坦克每走6步，更改一个状态
        self.get_random_direction()

    def get_random_direction(self):
        r = randint(0, 4)
        if r == 4:
            self.status = False
        elif r == 0:
            self.direction = "L"
            self.status = True
        elif r == 1:
            self.direction = "R"
            self.status = True
        elif r == 2:
            self.direction = "U"
            self.status = True
        elif r == 3:
            self.direction = "D"
            self.status = True

    def enemy_random_move(self):
        if self.live:
            if self.step == 0:
                self.get_random_direction()
                self.step = 6
            else:
                self.move()
                self.step -= 1

# 炮弹类
class Missile(BaseItem):
    width = 12
    height = 12
    def __init__(self,screem,my_tank):
        super().__init__();
        self.screem = screem  # 炮弹在移动或显示过程中需要用到当前屏幕
        self.direction = my_tank.direction  # 炮弹的方向由坦克决定
        self.speed = 12  # 炮弹的速度
        self.fire_status = False #开火的状态,初始是不连续的
        self.images = {}  # 坦克的所有图片
        self.images["L"] = pygame.image.load("images/missileL.gif")
        self.images["R"] = pygame.image.load("images/missileR.gif")
        self.images["U"] = pygame.image.load("images/missileU.gif")
        self.images["D"] = pygame.image.load("images/missileD.gif")
        self.image = self.images[self.direction]  # 炮弹的图片由方向决定
        self.rect = self.image.get_rect()
        self.rect.left = my_tank.rect.left + (my_tank.width-self.width)//2
        self.rect.top = my_tank.rect.top + (my_tank.height-self.height)//2
        self.live = True  # 决定坦克是否消灭了
    # 炮弹显示的方法
    def display(self):
        if self.live:
            self.image = self.images[self.direction]  # 由方向决定图片
            self.screem.blit(self.image, self.rect)

    # 炮弹移动的方法
    def move(self):
        if self.live:
            if self.direction == "L":
                if self.rect.left > 0:
                    self.rect.left -= self.speed
                else:
                    self.live = False
            elif self.direction == "R":
                if self.rect.right < TankeMain.width:
                    self.rect.right += self.speed
                else:
                    self.live = False
            elif self.direction == "U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.live = False
            elif self.direction == "D":
                if self.rect.bottom < TankeMain.height:
                    self.rect.bottom += self.speed
                else:
                    self.live = False


game=TankeMain()
game.startGame()








