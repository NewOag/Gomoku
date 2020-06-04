import pygame
from pygame.locals import *
from GameMap import *


class Button():
    def __init__(self, screen, text, x, y, color, enable):
        self.screen = screen
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT
        self.button_color = color
        self.text_color = (255, 255, 255)
        self.enable = enable
        self.font = pygame.font.SysFont(None, BUTTON_HEIGHT * 2 // 3)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topleft = (x, y)  # 重新标定Rect的原点坐标（或者起点）
        self.text = text
        self.init_msg()

    def init_msg(self):  # 按钮的颜色及文字
        if self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
            # render的参数（文本，抗锯齿，颜色，背景）,并且返回一个新的Surface,即为msg_image
        else:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
        self.msg_image_rect = self.msg_image.get_rect()#获得msg_image的矩形区域并赋值给一个新变量
        self.msg_image_rect.center = self.rect.center#让文本的center与按钮的center一致

    def draw(self):#绘制按钮
        if self.enable:
            self.screen.fill(self.button_color[0], self.rect)#用纯色填充整个按钮(color,rect,special_flags=0),并返回被填充的Surface
        else:
            self.screen.fill(self.button_color[1], self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)#将文字Surface和纯色按钮Surface绘制在同一个Surface中


class StartButton(Button):
    def __init__(self, screen, text, x, y):
        super().__init__(screen, text, x, y, [(26, 173, 25), (158, 217, 157)], True)#调用父类的初始化方法

    def click(self, game):
        if self.enable:
            game.start()
            game.winner = None
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
            self.enable = False
            return True
        return False

    def unclick(self):
        if not self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
            self.enable = True


class GiveupButton(Button):
    def __init__(self, screen, text, x, y):
        super().__init__(screen, text, x, y, [(230, 67, 64), (236, 139, 137)], False)

    def click(self, game):#返回跟enable相同的布尔值
        if self.enable:
            game.is_play = False
            if game.winner is None:
                game.winner = game.map.reverseTurn(game.player)
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
            self.enable = False
            return True
        return False

    def unclick(self):#返回跟enable相反的布尔值
        if not self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
            self.enable = True


class Game():
    def __init__(self, caption):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])#初始化窗口或屏幕进行显示
        pygame.display.set_caption(caption)#设置窗口标题
        self.clock = pygame.time.Clock()#创建一个时钟（用来帮助跟踪时间）
        self.buttons = []#按钮list？？？？？？？？？？
        self.buttons.append(StartButton(self.screen, 'Start', MAP_WIDTH + 30, 15))#添加开始按钮
        self.buttons.append(GiveupButton(self.screen, 'Giveup', MAP_WIDTH + 30, BUTTON_HEIGHT + 45))#添加结束按钮
        self.is_play = False
        self.map = Map(CHESS_LEN, CHESS_LEN)#实例化一个棋盘，参数是线条数而非实际大小
        self.player = MAP_ENTRY_TYPE.MAP_PLAYER_ONE#定义玩家？？？？？？？？？
        self.action = None
        self.winner = None

    def start(self):
        self.is_play = True#更改游戏状态
        self.player = MAP_ENTRY_TYPE.MAP_PLAYER_ONE#定义玩家？？？？？？？？？
        self.map.reset()#调用map类的函数清空棋盘

    def play(self):
        self.clock.tick(60)#最高60帧？？？？？？？
        light_yellow = (247, 238, 214)#定义一种颜色
        pygame.draw.rect(self.screen, light_yellow, pygame.Rect(0, 0, MAP_WIDTH, SCREEN_HEIGHT))#绘制棋盘的底色矩形
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(MAP_WIDTH, 0, INFO_WIDTH, SCREEN_HEIGHT))#绘制棋盘右侧的底色矩形

        for button in self.buttons:#画出按钮
            button.draw()

        if self.is_play and not self.isOver():
            if self.action is not None:
                self.checkClick(self.action[0], self.action[1])#下棋并轮到对方下
                self.action = None

            if not self.isOver():
                self.changeMouseShow()

        if self.isOver():
            self.showWinner()

        self.map.drawBackground(self.screen)
        self.map.drawChess(self.screen)

    def changeMouseShow(self):
        map_x, map_y = pygame.mouse.get_pos()#获取鼠标的坐标
        x, y = self.map.MapPosToIndex(map_x, map_y)#鼠标坐标变为行列序号
        if self.map.isInMap(map_x, map_y) and self.map.isEmpty(x, y):
            pygame.mouse.set_visible(False)
            light_red = (213, 90, 107)
            pos, radius = (map_x, map_y), CHESS_RADIUS
            pygame.draw.circle(self.screen, light_red, pos, radius)
        else:
            pygame.mouse.set_visible(True)

    def checkClick(self, x, y, isAI=False):
        self.map.click(x, y, self.player)#落子
        self.player = self.map.reverseTurn(self.player)#轮到对方下棋

    def mouseClick(self, map_x, map_y):
        if self.is_play and self.map.isInMap(map_x, map_y) and not self.isOver():
            x, y = self.map.MapPosToIndex(map_x, map_y)
            if self.map.isEmpty(x, y):
                self.action = (x, y)

    def isOver(self):
        return self.winner is not None

    def showWinner(self):
        def showFont(screen, text, location_x, locaiton_y, height):
            font = pygame.font.SysFont(None, height)
            font_image = font.render(text, True, (0, 0, 255), (255, 255, 255))
            font_image_rect = font_image.get_rect()
            font_image_rect.x = location_x
            font_image_rect.y = locaiton_y
            screen.blit(font_image, font_image_rect)

        if self.winner == MAP_ENTRY_TYPE.MAP_PLAYER_ONE:
            str = 'Winner is White'
        else:
            str = 'Winner is Black'
        showFont(self.screen, str, MAP_WIDTH + 25, SCREEN_HEIGHT - 60, 30)
        pygame.mouse.set_visible(True)

    def click_button(self, button):
        if button.click(self):
            for tmp in self.buttons:
                if tmp != button:
                    tmp.unclick()

    def check_buttons(self, mouse_x, mouse_y):
        for button in self.buttons:
            if button.rect.collidepoint(mouse_x, mouse_y):
                self.click_button(button)
                break


game = Game(" Gomoku " + GAME_VERSION)
while True:
    game.play()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            game.mouseClick(mouse_x, mouse_y)
            game.check_buttons(mouse_x, mouse_y)
