import pygame
import sys
import random
import os
from pygame.locals import *
import configparser

WINDOWWIDTH = 1000
WINDOWHEIGHT = 600
GAME_TITLE = "ANIMAL RACING BET"

ANIWIDTH = 60
ANIHEIGHT = 40
ANISPEED = 1
ANIMAXSPEED = 1
ANI_LEFT = 100
ANI_TOP = 200
RACETRACK_LENGTH = 800
ANI_MAXDISTANCE = RACETRACK_LENGTH - ANIWIDTH

LANE_DISTANCE = 60

RACETRACK_THICK = 6
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
LIGHTRED = (255, 100, 100)
SHADOW = (192, 192, 192)

CENTER = "center"
CONFIG_PATH = 'config/profiles.ini'
CONFIG_ISEXIST = 1
CONFIG_PROFILES = 0

pygame.init()


FPS = 60
fpsClock = pygame.time.Clock()


GAMEICON = pygame.image.load('res/img/icon.png')
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption(GAME_TITLE)
pygame.display.set_icon(GAMEICON)

BGMENUIMG = pygame.image.load('res/img/bgmenu.png')
BGGAMEIMG = []
for i in range(0, 4):
    BGGAMEIMG.append(pygame.image.load('res/img/gamebg'+ str(i) + '.png'))
BGGAMEINDEX = 0

STORE_BG = pygame.image.load('res/img/storebg.png')
MINIGAMEIMG = pygame.image.load('res/img/minigamebg.png')

ANIMAL_IMG = []
for i in range(0, 5):
    A = []
    for j in range(0, 6):
        A.append(pygame.image.load('res/img/ani'+ str(i) + str(j) +'.png'))
    ANIMAL_IMG.append(A)

ITEM_IMG = {
    "quickspells": pygame.image.load('res/img/quickspells.png'),
    "slowspells": pygame.image.load('res/img/slowspells.png'),
    "turnbackspells": pygame.image.load('res/img/turnbackspells.png'),
    "stopspells": pygame.image.load('res/img/stopspells.png'),
    "endtpspells": pygame.image.load('res/img/endtpspells.png'),
    "begintpspells": pygame.image.load('res/img/begintpspells.png'),
    "randomtpspells": pygame.image.load('res/img/randomtpspells.png')
}

WHEEL_IMG = pygame.image.load('res/img/wheel.png')
ARROW_IMG = pygame.image.load('res/img/arrow.png')

SCISSORS_IMG = pygame.image.load('res/img/scissors.png')
ROCK_IMG = pygame.image.load('res/img/rock.png')
PAPER_IMG = pygame.image.load('res/img/paper.png')

profile = []
profile_choiced = 0
profile_str = ""

_sound_library = {}
isSoundOn = 0
isMusicOn = 0

class MenuScene():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = BGMENUIMG
        self.font_size = 40
        self.profile_choiced = profile_choiced
        self.headingText = Text(GAME_TITLE, 'consolas', 60, (CENTER, 50), BLUE)
        self.playButton = Text('PLAY', 'consolas', self.font_size, (710, 250), RED)
        self.storeButton = Text('STORE', 'consolas', self.font_size, (700, 300), RED)
        self.minigameButton = Text('MINIGAME', 'consolas', self.font_size, (665, 350), RED)
        self.optionsButton = Text('OPTIONS', 'consolas', self.font_size, (680, 400), RED)
        self.changeProfileButton = Text('LOG OUT', 'consolas', self.font_size, (680, 450), RED)
        self.exitButton = Text('EXIT', 'consolas', self.font_size, (710, 500), RED)
        self.welcomeTx = Text('Welcome ', 'consolas', 20, (780, 570), GREEN)

        self.info_list = ["Người chơi: ", "Số trận thắng: ", "Số trận thua: "]
        self.infoMsb = MessageBox(self.info_list, 700, 230)
        self.isInfo = 0
    def draw(self):
        DISPLAYSURF.blit(self.img, (self.x, self.y))
        self.headingText.draw()
        self.playButton.draw()
        self.storeButton.draw() 
        self.minigameButton.draw()
        self.optionsButton.draw()
        self.changeProfileButton.draw()
        self.exitButton.draw()
        self.welcomeTx.draw()
        if self.isInfo:
            self.infoMsb.draw()
    def update(self):
        self.playButton.update(WHITE if self.playButton.isUpdate == 1 else RED, 'PLAY')
        self.storeButton.update(WHITE if self.storeButton.isUpdate == 1 else RED, 'STORE')
        self.minigameButton.update(WHITE if self.minigameButton.isUpdate == 1 else RED, 'MINIGAME')
        self.optionsButton.update(WHITE if self.optionsButton.isUpdate == 1 else RED, 'OPTIONS')
        self.changeProfileButton.update(WHITE if self.changeProfileButton.isUpdate == 1 else RED, 'LOG OUT')
        self.exitButton.update(WHITE if self.exitButton.isUpdate == 1 else RED, 'EXIT')
        self.playButton.isUpdate = self.playButton.isMouseOver(pygame.mouse.get_pos())
        self.storeButton.isUpdate = self.storeButton.isMouseOver(pygame.mouse.get_pos())
        self.minigameButton.isUpdate = self.minigameButton.isMouseOver(pygame.mouse.get_pos())
        self.optionsButton.isUpdate = self.optionsButton.isMouseOver(pygame.mouse.get_pos())
        self.changeProfileButton.isUpdate = self.changeProfileButton.isMouseOver(pygame.mouse.get_pos())
        self.exitButton.isUpdate = self.exitButton.isMouseOver(pygame.mouse.get_pos())
        self.profile_choiced = profile_choiced
        self.welcomeTx.isUpdate = self.welcomeTx.isMouseOver(pygame.mouse.get_pos())
        self.welcomeTx.update(WHITE if self.welcomeTx.isUpdate == 1 else GREEN, 'Welcome ' + config[profile_str]["name"] + "!")
        
        self.info_list = ["Người chơi: " + config[profile_str]["name"], "Số trận thắng: " + config[profile_str]["wins"], "Số trận thua: " + config[profile_str]["loses"]]

        self.infoMsb.okBtn.hovered = self.infoMsb.okBtn.isMouseOver(pygame.mouse.get_pos())
        self.infoMsb.update()
    def handle_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            play_sound("res/sound/tick.wav")
            pos = event.pos
            if self.playButton.isMouseOver(pos):
                global scene
                scene = scenes["Game"]
                scene.isReset = 1
            if self.changeProfileButton.isMouseOver(pos):
                scene = scenes["Profile"]
                scene.isReset = 1
            if self.storeButton.isMouseOver(pos):
                scene = scenes["Store"]
                scene.isReset = 1
            if self.minigameButton.isMouseOver(pos):
                scene = scenes["Minigame"]
                scene.isReset = 1
            if self.optionsButton.isMouseOver(pos):
                scene = scenes["Options"]
            if self.exitButton.isMouseOver(pos):
                pygame.quit()
                sys.exit()
            if self.welcomeTx.isMouseOver(pos):
                self.infoMsb = MessageBox(self.info_list, 700, 230)
                self.isInfo = 1
            if self.infoMsb.okBtn.isMouseOver(pos) and self.isInfo:
                self.isInfo = 0

class ProfileScene():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = BGMENUIMG
        self.font_size = 25
        self.isReset = 1
        self.headingText = Text(GAME_TITLE, 'consolas', 60, (CENTER, 50), BLUE)
        self.selectProfile = Text('====== LOGIN ======', 'consolas', self.font_size, (610, 230), RED)
        self.doneButton = Text('LOGIN', 'consolas', self.font_size, (710, 395), RED)
        self.newProfileButton = Text('SIGN UP', 'consolas', self.font_size, (700, 490), RED)
        self.rect = pygame.Rect(590, 260, 300, 175)

        self.usernameInp = InputBox(600, 270, 280, 50, "USERNAME")
        self.passwordInp = InputBox(600, 330, 280, 50, "PASSWORD", True)
        self.passwordInp.active = 0
        self.isReset = 0

        self.errorMsb = MessageBox(["Tài khoản hoặc mật khẩu không đúng", "Vui lòng thử lại"], 600, 200)
        self.isError = 0

    def reset(self):
        self.passwordInp.text = ""
        self.passwordInp.active = 0
        self.isReset = 0
        self.isError = 0

    def draw(self):
        DISPLAYSURF.blit(self.img, (self.x, self.y))
        self.headingText.draw()
        self.selectProfile.draw()
        self.doneButton.draw() 
        self.newProfileButton.draw()
        pygame.draw.rect(DISPLAYSURF, WHITE, self.rect, 2)

        self.usernameInp.draw(DISPLAYSURF)
        self.passwordInp.draw(DISPLAYSURF)

        if self.isError:
            self.errorMsb.draw()
    def update(self):
        if self.isReset:
            self.reset()
        self.doneButton.update(WHITE if self.doneButton.isUpdate == 1 else RED, 'LOGIN')
        self.newProfileButton.update(WHITE if self.newProfileButton.isUpdate == 1 else RED, 'SIGN UP')
        self.doneButton.isUpdate = self.doneButton.isMouseOver(pygame.mouse.get_pos())
        self.newProfileButton.isUpdate = self.newProfileButton.isMouseOver(pygame.mouse.get_pos())

        self.usernameInp.update()
        self.passwordInp.update()

        self.errorMsb.okBtn.hovered = self.errorMsb.okBtn.isMouseOver(pygame.mouse.get_pos())
        self.errorMsb.update()

    def handle_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            play_sound("res/sound/tick.wav")
            pos = event.pos
            if self.doneButton.isMouseOver(pos):
                global scene, profile_choiced, profile_str
                if int(config["PROFILE"]["profiles"]) != 0:
                    for i in range(1, int(config["PROFILE"]["profiles"]) + 1):
                        if self.usernameInp.text == config["profile" + str(i)]["name"] and self.passwordInp.text == config["profile" + str(i)]["pass"]:
                            profile_choiced = i
                            profile_str = "profile" + str(profile_choiced)
                            scene = scenes["Menu"]
                    if profile_choiced == 0:
                        self.isError = 1
            if self.newProfileButton.isMouseOver(pos):
                scene = scenes["NewProfile"]
                scene.isReset = 1

            if self.errorMsb.okBtn.isMouseOver(pos) and self.isError:
                self.isError = 0
        self.usernameInp.handle_event(event)
        self.passwordInp.handle_event(event)

class NewProfileScene():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = BGMENUIMG
        self.font_size = 25

        self.isReset = 1
        self.headingText = Text(GAME_TITLE, 'consolas', 60, (CENTER, 50), BLUE)
        self.selectProfile = Text('===== SIGN UP =====', 'consolas', self.font_size, (610, 230), RED)
        self.doneButton = Text('SIGN UP', 'consolas', self.font_size, (700, 455), RED)
        self.backButton = Text('BACK', 'consolas', self.font_size, (720, 500), RED)
        self.rect = pygame.Rect(590, 260, 300, 230)

        self.usernameInp = InputBox(600, 270, 280, 50, "USERNAME")
        self.passwordInp = InputBox(600, 330, 280, 50, "PASSWORD", True)
        self.confirmpasswordInp = InputBox(600, 390, 280, 50, "CONFIRM PASSWORD", True)
        self.passwordInp.active = 0
        self.confirmpasswordInp.active = 0
        self.isReset = 0
    
        self.error_list = ["Mật khẩu xác nhận không trùng khớp", "Vui lòng thử lại"]
        self.errorMsb = MessageBox(self.error_list, 600, 200)
        self.isError = 0
    def reset(self):
        self.usernameInp = InputBox(600, 270, 280, 50, "USERNAME")
        self.passwordInp = InputBox(600, 330, 280, 50, "PASSWORD", True)
        self.confirmpasswordInp = InputBox(600, 390, 280, 50, "CONFIRM PASSWORD", True)
        self.passwordInp.active = 0
        self.confirmpasswordInp.active = 0
        self.isReset = 0
        self.isError = 0
        self.error_list = ["Mật khẩu xác nhận không trùng khớp", "Vui lòng thử lại"]

    def draw(self):
        DISPLAYSURF.blit(self.img, (self.x, self.y))
        self.headingText.draw()
        self.selectProfile.draw()
        self.doneButton.draw()
        if int(config["PROFILE"]["profiles"]) != 0:
            self.backButton.draw()

        pygame.draw.rect(DISPLAYSURF, WHITE, self.rect, 2)
        self.usernameInp.draw(DISPLAYSURF)
        self.passwordInp.draw(DISPLAYSURF)
        self.confirmpasswordInp.draw(DISPLAYSURF)

        if self.isError:
            self.errorMsb.draw()
    def update(self):
        if self.isReset:
            self.reset()

        self.doneButton.update(WHITE if self.doneButton.isUpdate == 1 else RED, 'SIGN UP')
        self.backButton.update(WHITE if self.backButton.isUpdate == 1 else RED, 'BACK')
        self.doneButton.isUpdate = self.doneButton.isMouseOver(pygame.mouse.get_pos())
        self.backButton.isUpdate = self.backButton.isMouseOver(pygame.mouse.get_pos())

        self.usernameInp.update()
        self.passwordInp.update()
        self.confirmpasswordInp.update()

        self.errorMsb.okBtn.hovered = self.errorMsb.okBtn.isMouseOver(pygame.mouse.get_pos())
        self.errorMsb.update()
    def handle_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            play_sound("res/sound/tick.wav")
            pos = event.pos
            if self.doneButton.isMouseOver(pos):
                global scene
                if self.usernameInp.text != "" and self.passwordInp.text != "" and self.confirmpasswordInp.text != "":
                    if self.passwordInp.text == self.confirmpasswordInp.text:
                        isDuplicate = 0
                        for i in range(1, int(config["PROFILE"]["profiles"]) + 1):
                            if self.usernameInp.text == config["profile" + str(i)]["name"]:
                                isDuplicate = 1
                        if not isDuplicate:
                            config["PROFILE"]["profiles"] = str(int(config["PROFILE"]["profiles"]) + 1)
                            profile_str = "profile" + str(config["PROFILE"]["profiles"])
                            config.add_section(profile_str)
                            config[profile_str]["name"] = self.usernameInp.text
                            config[profile_str]["pass"] = self.passwordInp.text
                            config[profile_str]["coin"] = '500'
                            config[profile_str]["quickspells"] = '0'
                            config[profile_str]["slowspells"] = '0'
                            config[profile_str]["turnbackspells"] = '0'
                            config[profile_str]["stopspells"] = '0'
                            config[profile_str]["endtpspells"] = '0'
                            config[profile_str]["begintpspells"] = '0'
                            config[profile_str]["randomtpspells"] = '0'
                            config[profile_str]["wins"] = '0'
                            config[profile_str]["loses"] = '0'
                            profileUpdate()
                            scene = scenes["Profile"]
                            scene.isReset = 1
                            scene.usernameInp.text = self.usernameInp.text
                        else:
                            self.error_list[0] = "Tài khoản đã tồn tại"
                            self.errorMsb = MessageBox(self.error_list, 600, 200)
                            self.isError = 1
                    else:
                        self.error_list[0] = "Mật khẩu xác nhận không trùng khớp"
                        self.errorMsb = MessageBox(self.error_list, 600, 200)
                        self.isError = 1
            if self.backButton.isMouseOver(pos):
                scene = scenes["Profile"]
                scene.isReset = 1

            if self.errorMsb.okBtn.isMouseOver(pos) and self.isError:
                self.isError = 0
        self.usernameInp.handle_event(event)
        self.passwordInp.handle_event(event)
        self.confirmpasswordInp.handle_event(event)

class OptionsScene():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = MINIGAMEIMG
        self.font_size = 25

        self.isReset = 1
        self.doneButton = Text('DONE', 'consolas', self.font_size, (480, 550), RED)
        self.bggameText = Text("GAME BACKGROUND", 'consolas', 20, (200, 10), BLACK)
        self.bgrect = pygame.Rect(170, 30, 660, 420)
        self.soundandmusicText = Text("MUSIC & SOUND", 'consolas', 20, (200, 460), BLACK)
        self.soundrect = pygame.Rect(170, 480, 660, 50)
        self.musicText = Text("MUSIC:", 'consolas', 20, (190, 500), BLACK)
        self.music = Text("ON", 'consolas', 20, (290, 500), BLACK)
        self.soundText = Text("SOUND:", 'consolas', 20, (510, 500), BLACK)
        self.sound = Text("ON", 'consolas', 20, (600, 500), BLACK)

        self.gamebg = []
        for i in range(0, 4):
            self.gamebg.append(pygame.transform.scale(BGGAMEIMG[i], (300, 180)))
        self.gamebg_rect = [
            self.gamebg[0].get_rect(x = 190, y = 50),
            self.gamebg[1].get_rect(x = 510, y = 50),
            self.gamebg[2].get_rect(x = 190, y = 250),
            self.gamebg[3].get_rect(x = 510, y = 250)
        ]

    def draw(self):
        DISPLAYSURF.blit(self.img, (self.x, self.y))

        for i in range(0, 4):
            DISPLAYSURF.blit(self.gamebg[i], self.gamebg_rect[i])
            if self.gamebg_rect[i].collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(DISPLAYSURF, BLUE, self.gamebg_rect[i], 5)

        pygame.draw.rect(DISPLAYSURF, RED, self.gamebg_rect[BGGAMEINDEX], 5)
        self.bggameText.draw()
        self.soundandmusicText.draw()
        self.musicText.draw()
        self.soundText.draw()
        self.music.draw()
        self.sound.draw()
        self.doneButton.draw()

        pygame.draw.rect(DISPLAYSURF, BLACK, self.bgrect, 2)
        pygame.draw.rect(DISPLAYSURF, BLACK, self.soundrect, 2)

    def update(self):
        self.doneButton.update(WHITE if self.doneButton.isUpdate == 1 else RED, 'DONE')
        self.doneButton.isUpdate = self.doneButton.isMouseOver(pygame.mouse.get_pos())

        self.music.isUpdate = self.music.isMouseOver(pygame.mouse.get_pos())
        self.music.update(WHITE if self.music.isUpdate == 1 else RED, 'ON' if isMusicOn else 'OFF')
        self.sound.isUpdate = self.sound.isMouseOver(pygame.mouse.get_pos())
        self.sound.update(WHITE if self.sound.isUpdate == 1 else RED, 'ON' if isSoundOn else 'OFF')

    def handle_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            play_sound("res/sound/tick.wav")
            pos = event.pos
            if self.doneButton.isMouseOver(pos):
                global scene
                scene = scenes["Menu"]
                scene.isReset = 1
            if self.music.isMouseOver(pos):
                global isMusicOn
                isMusicOn = not isMusicOn
                gameMusic.sound.set_volume(isMusicOn)
            if self.sound.isMouseOver(pos):
                global isSoundOn
                isSoundOn = not isSoundOn
            for i in range(0, 4):
                if self.gamebg_rect[i].collidepoint(pos):
                    global BGGAMEINDEX
                    BGGAMEINDEX = i
class GameScene():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.text_color = BLACK
        self.spells_textcolor = BLACK
        self.isReset = 0
        self.isResetRound = 0
        self.img = BGGAMEIMG[BGGAMEINDEX]
        self.racetrack = RaceTrack()
        self.item_appear_ticks = 6000 #miliseconds
        self.player = Player()

        self.helpButton = Button("?", 880, 10, 40, 40)
        self.backButton = Button("►", 930, 10, 40, 40)

        self.topborderrect = pygame.Rect(int((WINDOWWIDTH - 700)/2), -6, 700, 125)
        self.topborderrect1 = pygame.Rect(int((WINDOWWIDTH - 700)/2) + 140, -6, 200, 125)

        self.round_tx = Text("ROUND", "consolas", 30, (350, 10), self.text_color)
        
        self.playeranibg_rect = pygame.Rect(int((WINDOWWIDTH - 700)/2), 0, 700, 119)
        self.playeranibg_sur = pygame.Surface((self.playeranibg_rect.w, self.playeranibg_rect.h), pygame.SRCALPHA)   # per-pixel alpha
        self.playeranibg_sur.fill((255, 255, 255, 192))

        self.help_list = ["Nhập số coins, ấn OK và chọn nhân vật để cá cược", "Nhấp dùng bùa trực tiếp trên thanh công cụ", "Out game giữa chừng sẽ mất tiền cược"]
        self.helpMsb = MessageBox(self.help_list, 700, 230)
        self.isHelp = 0

        self.gameplayMusic = Sound("res/sound/gameplay.mp3")

    def reset(self):
        if self.isReset:
            self.round = 1
            self.bonus = 0
            self.isReset = 0
        if self.isResetRound:
            self.round += 1
            self.bonus += 10 if self.round < 5 else 20
            self.isResetRound = 0

        self.img = BGGAMEIMG[BGGAMEINDEX]
        self.coins_reward = 0
        self.player.coinbetted = 0
        self.player.choice = 6
        self.anicur1st = 6
        self.isRacing = 0
        self.isBetted = 0
        self.top_count = 0
        self.isOver = 0
        self.ani = []
        self.top_text = []
        self.item_appear_time = 0
        self.start_ticks = 0
        self.end_ticks = 0
        self.headertext = Text("Nhập số coins muốn cược", "consolas", 40, (CENTER, 150), WHITE)
        self.coin_tx = Text("Coins: " + config[profile_str]["coin"], "consolas", 20, (500, 20), self.text_color)
        self.coinbetted_tx = Text("Coins Betted: 0", "consolas", 20, (650, 20), self.text_color)

        self.round_num = Text(str(self.round) + "/5", "consolas", 55, (348, 40), self.text_color)
        self.bonus_tx = Text("Bonus: +" + str(self.bonus) + "%", "consolas", 25, (315, 90), self.text_color)

        self.itemCreate()

        self.coinbettedinp = InputBox(350, 194, 180, 54)
        self.okButton = Button("OK", 540, 194, 54, 54)

        for x in range(0, 6):
            self.ani.append(Animal(ANIMAL_IMG[self.round - 1][x], ANI_LEFT, ANI_TOP + LANE_DISTANCE * x, x))
            self.top_text.append(Text("0", "consolas", 40, (910, ANI_TOP + LANE_DISTANCE * x), WHITE))

        self.playeranitop_tx = Text("TOP: ", "consolas", 25, (175, 90), self.text_color)

        self.isCongrat = 0
        self.congratList = ["Chúc mừng", "Bạn nhận được "]        
        self.congratMsb = MessageBox(self.congratList, 430, 180)
        self.isUpdateCongratMsb = 0
        self.isHelp = 0

    def itemCreate(self):
        self.QuickSpellsItem = QuickSpellsItem(500, 50)
        self.SlowSpellsItem = SlowSpellsItem(550, 50)
        self.TurnBackSpellsItem = TurnBackSpellsItem(600, 50)
        self.StopSpellsItem = StopSpellsItem(650, 50)
        self.EndTPSpellsItem = EndTPSpellsItem(700, 50)
        self.BeginTPSpellsItem = BeginTPSpellsItem(750, 50)
        self.RandomTPSpellsItem = RandomTPSpellsItem(800, 50)

        self.QuickSpellsItem_Tx = Text("0", "consolas", 20, (515, 95), self.spells_textcolor)
        self.SlowSpellsItem_Tx = Text("0", "consolas", 20, (565, 95), self.spells_textcolor)
        self.TurnBackSpellsItem_Tx = Text("0", "consolas", 20, (615, 95), self.spells_textcolor)
        self.StopSpellsItem_Tx = Text("0", "consolas", 20, (665, 95), self.spells_textcolor)
        self.EndTPSpellsItem_Tx = Text("0", "consolas", 20, (715, 95), self.spells_textcolor)
        self.BeginTPSpellsItem_Tx = Text("0", "consolas", 20, (765, 95), self.spells_textcolor)
        self.RandomTPSpellsItem_Tx = Text("0", "consolas", 20, (815, 95), self.spells_textcolor)

    def itemDraw(self):
        self.QuickSpellsItem.draw()
        self.SlowSpellsItem.draw()
        self.TurnBackSpellsItem.draw()
        self.StopSpellsItem.draw()
        self.EndTPSpellsItem.draw()
        self.BeginTPSpellsItem.draw()
        self.RandomTPSpellsItem.draw()

        self.QuickSpellsItem_Tx.draw()
        self.SlowSpellsItem_Tx.draw()
        self.TurnBackSpellsItem_Tx.draw()
        self.StopSpellsItem_Tx.draw()
        self.EndTPSpellsItem_Tx.draw()
        self.BeginTPSpellsItem_Tx.draw()
        self.RandomTPSpellsItem_Tx.draw()

    def draw(self):
        DISPLAYSURF.blit(self.img, (self.x, self.y))
        self.racetrack.draw()                 
        DISPLAYSURF.blit(self.playeranibg_sur, self.playeranibg_rect)
        pygame.draw.rect(DISPLAYSURF, BLUE, self.topborderrect, 6)
        pygame.draw.rect(DISPLAYSURF, BLUE, self.topborderrect1, 6)  
        self.round_tx.draw()
        self.round_num.draw()
        self.bonus_tx.draw()
        self.playeranitop_tx.draw()
        if self.isRacing:
            DISPLAYSURF.blit(ANIMAL_IMG[self.round - 1][self.player.choice], (190, 30))

        self.headertext.draw()
        self.coin_tx.draw()
        self.coinbetted_tx.draw()
        self.itemDraw()

        if self.isBetted == 0:
            self.coinbettedinp.draw(DISPLAYSURF)
            self.okButton.draw(DISPLAYSURF)

        if self.isCongrat:
            self.congratMsb.draw()

        for x in range(0, 6):
            self.ani[x].draw()
            self.top_text[x].draw()

        self.helpButton.draw(DISPLAYSURF)
        self.backButton.draw(DISPLAYSURF)

        if self.isHelp:
            self.helpMsb.draw()
    def update(self):
        # reset hinh anh khi bat dau
        if self.isReset or self.isResetRound:
            self.reset()

        self.itemUpdate()
        self.coinbettedinp.update()
        self.coinbetted_tx.update(self.text_color, "Coins cược: " + str(self.player.coinbetted))
        self.coin_tx.update(self.text_color, "Coins: " + config[profile_str]["coin"])

        self.round_num.update(self.text_color, str(self.round) + "/5")
        self.bonus_tx.update(self.text_color, "Bonus: +" + str(self.bonus) + "%")

        self.okButton.hovered = self.okButton.isMouseOver(pygame.mouse.get_pos())
        self.okButton.update()

        if self.isBetted:
            self.headertext.update(WHITE, "Click để chọn nhân vật", CENTER, 150)

        # update hinh anh khi dang dua
        if self.isRacing:
            self.headertext.update(WHITE, "", CENTER, 150)
            self.playeranitop_tx.update(self.text_color, "TOP: " + str(self.ani[self.player.choice].current_top))
            self.itemHandle()
            self.aniCurrentTop()
            for x in range(0, 6):
                self.ani[x].update()
                self.top_text[x].update(WHITE, str(self.ani[x].current_top))
                self.anicur1st = x if self.ani[x].current_top == (self.top_count + 1) else self.anicur1st

        # kiem tra tro choi ket thuc
        for ani in self.ani:
            if (ani.distance >= ANI_MAXDISTANCE) and (ani.top == 0):
                self.top_count += 1
                ani.top = self.top_count
        if self.top_count >= 6 and not self.isOver:
            self.gameplayMusic.stop()
            print("Xe ban chon duoc top", self.ani[self.player.choice].top)
            self.GameOver()
            if self.ani[self.player.choice].top > 3:
                self.congratList[0] = "Oh! No"
                self.congratList[1] = "Bạn đã thất bại!"
                play_sound("res/sound/condolatory.wav")
            else:
                self.congratList[1] = "Bạn nhận được " + str(self.coins_reward) + " coins"
                play_sound("res/sound/congratulation.mp3")
            self.congratMsb = MessageBox(self.congratList, 430, 180)
            self.isRacing = 0
            self.isCongrat = 1
            self.isOver = 1

        self.congratMsb.okBtn.hovered = self.congratMsb.okBtn.isMouseOver(pygame.mouse.get_pos())
        self.congratMsb.update()
        self.helpMsb.okBtn.hovered = self.helpMsb.okBtn.isMouseOver(pygame.mouse.get_pos())
        self.helpMsb.update()

        self.helpButton.hovered = self.helpButton.isMouseOver(pygame.mouse.get_pos())
        self.helpButton.update()
        self.backButton.hovered = self.backButton.isMouseOver(pygame.mouse.get_pos())
        self.backButton.update()

        if self.isOver:
            for x in range(0, 6):
                self.ani[x].update()

    def itemUpdate(self):
        self.QuickSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["quickspells"])
        self.SlowSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["slowspells"])
        self.TurnBackSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["turnbackspells"])
        self.StopSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["stopspells"])
        self.EndTPSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["endtpspells"])
        self.BeginTPSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["begintpspells"])
        self.RandomTPSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["randomtpspells"])

    def GameOver(self):
        if self.ani[self.player.choice].top == 1:
            self.coins_reward = int((3 + 2 * self.bonus / 100) * self.player.coinbetted)
            config[profile_str]["coin"] = str(int(config[profile_str]["coin"]) + self.coins_reward)
            config[profile_str]["loses"] = str(int(config[profile_str]["loses"]) - 1)
            config[profile_str]["wins"] = str(int(config[profile_str]["wins"]) + 1)
        elif self.ani[self.player.choice].top == 2:
            self.coins_reward = int((2 + 1 * self.bonus / 100) * self.player.coinbetted)
            config[profile_str]["coin"] = str(int(config[profile_str]["coin"]) + self.coins_reward)
            config[profile_str]["loses"] = str(int(config[profile_str]["loses"]) - 1)
            config[profile_str]["wins"] = str(int(config[profile_str]["wins"]) + 1)
        elif self.ani[self.player.choice].top == 3:   
            self.coins_reward = int((1.5 + 0.5 * self.bonus / 100) * self.player.coinbetted)
            config[profile_str]["coin"] = str(int(config[profile_str]["coin"]) + self.coins_reward)
            config[profile_str]["loses"] = str(int(config[profile_str]["loses"]) - 1)
            config[profile_str]["wins"] = str(int(config[profile_str]["wins"]) + 1)
        profileUpdate()

    def aniCurrentTop(self):
        for i in range(0, 6):
            self.ani[i].current_top = 1
            for j in range(0, 6):
                if self.ani[i].distance < self.ani[j].distance:
                    self.ani[i].current_top += 1
                if self.ani[i].distance >= ANI_MAXDISTANCE:
                    self.ani[i].current_top = self.ani[i].top
    def itemHandle(self):
        self.end_ticks = pygame.time.get_ticks()
        # print((self.end_ticks - self.start_ticks) // self.item_appear_ticks)
        if ((self.end_ticks - self.start_ticks) // self.item_appear_ticks) == (self.item_appear_time + 1):
            print(self.start_ticks, self.end_ticks)
            self.item_appear_time += 1
            for x in range(0, 6):
                if self.ani[x].x + 140 < (ANI_LEFT + ANI_MAXDISTANCE):
                    self.ani[x].randomItem()
    def handle_event(self, event):
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                global scene
                scene = scenes["Menu"]
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            play_sound("res/sound/tick.wav")
            pos = event.pos
            for ani in self.ani:
                if ani.rect.collidepoint(pos) and self.player.choice == 6 and self.isBetted == 1:
                    self.player.choice = ani.number
                    self.start_ticks = pygame.time.get_ticks() if self.isRacing == 0 else self.start_ticks
                    self.isRacing = 1
                    self.headertext.update(WHITE, "")
                    gameMusic.sound.set_volume(0)
                    self.gameplayMusic.play()
                    self.gameplayMusic.sound.set_volume(isMusicOn)
            if self.okButton.isMouseOver(pos):
                if self.coinbettedinp.text.isnumeric():
                    if 10 <= int(self.coinbettedinp.text) <= int(config[profile_str]["coin"]):
                        self.player.coinbetted = int(self.coinbettedinp.text)
                        config[profile_str]["coin"] = str(int(config[profile_str]["coin"]) - self.player.coinbetted)
                        config[profile_str]["loses"] = str(int(config[profile_str]["loses"]) + 1)
                        profileUpdate()
                        self.isBetted = 1
            if self.backButton.isMouseOver(pos):
                self.gameplayMusic.stop()
                gameMusic.sound.set_volume(isMusicOn)
                scene = scenes["Menu"]

            if self.QuickSpellsItem.isMouseOver(pos) and self.isRacing and not self.ani[self.player.choice].isFinish and int(config[profile_str]["quickspells"]) > 0:
                self.ani[self.player.choice].item = QuickSpellsItem(self.ani[self.player.choice].x, self.ani[self.player.choice].y)
                config[profile_str]["quickspells"] = str(int(config[profile_str]["quickspells"]) - 1)
                profileUpdate()
            
            if self.EndTPSpellsItem.isMouseOver(pos) and self.isRacing and not self.ani[self.player.choice].isFinish and int(config[profile_str]["endtpspells"]) > 0:
                self.ani[self.player.choice].item = EndTPSpellsItem(self.ani[self.player.choice].x, self.ani[self.player.choice].y)
                config[profile_str]["endtpspells"] = str(int(config[profile_str]["endtpspells"]) - 1)
                profileUpdate()

            if self.SlowSpellsItem.isMouseOver(pos) and self.isRacing and self.ani[self.player.choice] != self.ani[self.anicur1st] and not self.ani[self.player.choice].isFinish and int(config[profile_str]["slowspells"]) > 0:
                self.ani[self.anicur1st].item = SlowSpellsItem(self.ani[self.anicur1st].x, self.ani[self.anicur1st].y)
                config[profile_str]["slowspells"] = str(int(config[profile_str]["slowspells"]) - 1)
                profileUpdate()
              
            if self.TurnBackSpellsItem.isMouseOver(pos) and self.isRacing and self.ani[self.player.choice] != self.ani[self.anicur1st] and not self.ani[self.player.choice].isFinish and int(config[profile_str]["turnbackspells"]) > 0:
                self.ani[self.anicur1st].item = TurnBackSpellsItem(self.ani[self.anicur1st].x, self.ani[self.anicur1st].y)
                config[profile_str]["turnbackspells"] = str(int(config[profile_str]["turnbackspells"]) - 1)
                profileUpdate()

            if self.StopSpellsItem.isMouseOver(pos) and self.isRacing and self.ani[self.player.choice] != self.ani[self.anicur1st] and not self.ani[self.player.choice].isFinish and int(config[profile_str]["stopspells"]) > 0:
                self.ani[self.anicur1st].item = StopSpellsItem(self.ani[self.anicur1st].x, self.ani[self.anicur1st].y)
                config[profile_str]["stopspells"] = str(int(config[profile_str]["stopspells"]) - 1)
                profileUpdate()
            
            if self.BeginTPSpellsItem.isMouseOver(pos) and self.isRacing and self.ani[self.player.choice] != self.ani[self.anicur1st] and not self.ani[self.player.choice].isFinish and int(config[profile_str]["begintpspells"]) > 0:
                self.ani[self.anicur1st].item = BeginTPSpellsItem(self.ani[self.anicur1st].x, self.ani[self.anicur1st].y)
                config[profile_str]["begintpspells"] = str(int(config[profile_str]["begintpspells"]) - 1)
                profileUpdate()

            if self.RandomTPSpellsItem.isMouseOver(pos) and self.isRacing and not self.ani[self.player.choice].isFinish and int(config[profile_str]["randomtpspells"]) > 0:
                for ani in self.ani:
                    ani.item = RandomTPSpellsItem(ani.x, ani.y)
                config[profile_str]["randomtpspells"] = str(int(config[profile_str]["randomtpspells"]) - 1)
                profileUpdate()

            if self.congratMsb.okBtn.isMouseOver(pos) and self.isCongrat:
                self.isCongrat = 0
                if self.round < 5:
                    self.isResetRound = 1
                else:
                    self.isReset = 1
                gameMusic.sound.set_volume(isMusicOn)
            if self.helpButton.isMouseOver(pos):
                self.isHelp = 1
            if self.helpMsb.okBtn.isMouseOver(pos) and self.helpMsb:
                self.isHelp = 0
        self.coinbettedinp.handle_event(event)
        
class StoreScene():
    def __init__(self):
        self.img = STORE_BG
        self.wheel_img = WHEEL_IMG
        self.arrow_img = ARROW_IMG
        self.isReset = 1
        self.text_color = WHITE
        self.item_dict = {
            'QuickSpellsItem': 7,
            'SlowSpellsItem': 6,
            'TurnBackSpellsItem': 5,
            'StopSpellsItem': 4,
            'BeginTPSpellsItem': 3,
            'EndTPSpellsItem': 2,
            'RandomTPSpellsItem': 1,
            'LostTurn': 0
        }

        self.helpButton = Button("?", 880, 10, 40, 40)
        self.backButton = Button("►", 930, 10, 40, 40)

        self.helpMsb = MessageBox(["Click vào vòng quay để quay", "Mất 500 coins mỗi lần quay"], 400, 200)

        self.QuickSpellsItem = QuickSpellsItem(200, 150)
        self.SlowSpellsItem = SlowSpellsItem(200, 200)
        self.TurnBackSpellsItem = TurnBackSpellsItem(200, 250)
        self.StopSpellsItem = StopSpellsItem(200, 300)
        self.EndTPSpellsItem = EndTPSpellsItem(200, 350)
        self.BeginTPSpellsItem = BeginTPSpellsItem(200, 400)
        self.RandomTPSpellsItem = RandomTPSpellsItem(200, 450)

        self.spinning_sound = Sound("res/sound/spinning.mp3")

    def reset(self):
        self.coin_tx = Text("Coins: " + config[profile_str]["coin"], "consolas", 20, (CENTER, 20), WHITE)
        self.angle = 0
        self.speed = 15
        self.isRotate = 0
        self.isReset = 0
        self.item = 0
        self.isCongrat = 0
        self.isHelp = 0
        self.random_angle = random.randint(-20, 20)
        self.congratList = ["Chúc mừng", ""]        
        self.congratMsb = MessageBox(self.congratList, 600, 180)
        self.isUpdateCongratMsb = 0

        self.QuickSpellsItem_Tx = Text("0", "consolas", 20, (250, 160), self.text_color)
        self.SlowSpellsItem_Tx = Text("0", "consolas", 20, (250, 210), self.text_color)
        self.TurnBackSpellsItem_Tx = Text("0", "consolas", 20, (250, 260), self.text_color)
        self.StopSpellsItem_Tx = Text("0", "consolas", 20, (250, 310), self.text_color)
        self.EndTPSpellsItem_Tx = Text("0", "consolas", 20, (250, 360), self.text_color)
        self.BeginTPSpellsItem_Tx = Text("0", "consolas", 20, (250, 410), self.text_color)
        self.RandomTPSpellsItem_Tx = Text("0", "consolas", 20, (250, 460), self.text_color)

    def draw(self):
        DISPLAYSURF.blit(self.img, (0, 0))
        DISPLAYSURF.blit(self.surf, self.new_rect)
        DISPLAYSURF.blit(self.arrow_img, (780, 273))

        self.QuickSpellsItem.draw()
        self.SlowSpellsItem.draw()
        self.TurnBackSpellsItem.draw()
        self.StopSpellsItem.draw()
        self.EndTPSpellsItem.draw()
        self.BeginTPSpellsItem.draw()
        self.RandomTPSpellsItem.draw()

        self.QuickSpellsItem_Tx.draw()
        self.SlowSpellsItem_Tx.draw()
        self.TurnBackSpellsItem_Tx.draw()
        self.StopSpellsItem_Tx.draw()
        self.EndTPSpellsItem_Tx.draw()
        self.BeginTPSpellsItem_Tx.draw()
        self.RandomTPSpellsItem_Tx.draw()

        self.helpButton.draw(DISPLAYSURF)
        self.backButton.draw(DISPLAYSURF)
        self.coin_tx.draw()
        if self.isHelp:
            self.helpMsb.draw()
        if self.isCongrat:
            self.congratMsb.draw()
    def update(self):
        if self.isReset:
            self.reset()

        self.itemUpdate()

        self.helpMsb.okBtn.hovered = self.helpMsb.okBtn.isMouseOver(pygame.mouse.get_pos())
        self.helpMsb.update()

        self.helpButton.hovered = self.helpButton.isMouseOver(pygame.mouse.get_pos())
        self.helpButton.update()
        self.backButton.hovered = self.backButton.isMouseOver(pygame.mouse.get_pos())
        self.backButton.update()
        self.coin_tx.update(WHITE, "Coins: " + config[profile_str]["coin"])

        if self.isRotate == 1:
            self.speed = 10 if (self.angle >= 360 * 4) else self.speed
            self.speed = 5 if (self.angle >= 360 * 5) else self.speed
            self.speed = 3 if (self.angle >= 360 * 6) else self.speed
            self.speed = 1 if (self.angle >= 360 * 6 + self.item_dict[self.item] * 45 - 90) else self.speed
            self.speed = 0 if (self.angle >= 360 * 6 + self.item_dict[self.item] * 45 + self.random_angle) else self.speed
            self.angle += self.speed
        if self.speed == 0:
            self.isRotate = 0
            if self.isUpdateCongratMsb == 0:
                self.itemUpdateConfig()
                self.spinning_sound.stop()
                if self.item == 'LostTurn':
                    play_sound("res/sound/condolatory.wav")
                    self.congratList[0] = "Oh! No"
                    self.congratList[1] = "Bạn vừa quay vào ô Mất Lượt"
                else:
                    play_sound("res/sound/congratulation.mp3")
                    self.congratList[1] = "Bạn nhận được " + self.itemName()

                self.congratMsb = MessageBox(self.congratList, 430, 180)
                self.isUpdateCongratMsb = 1
                self.isCongrat = 1

        self.congratMsb.okBtn.hovered = self.congratMsb.okBtn.isMouseOver(pygame.mouse.get_pos())
        self.congratMsb.update()

        self.picture = pygame.transform.scale(self.wheel_img, (400, 400))   
        self.surf = pygame.transform.rotate(self.picture, self.angle - 31)
        self.new_rect = self.surf.get_rect(center = self.picture.get_rect(center = (600, 300)).center) 
    def itemUpdate(self):
        self.QuickSpellsItem_Tx.update(self.text_color, config[profile_str]["quickspells"])
        self.SlowSpellsItem_Tx.update(self.text_color, config[profile_str]["slowspells"])
        self.TurnBackSpellsItem_Tx.update(self.text_color, config[profile_str]["turnbackspells"])
        self.StopSpellsItem_Tx.update(self.text_color, config[profile_str]["stopspells"])
        self.EndTPSpellsItem_Tx.update(self.text_color, config[profile_str]["endtpspells"])
        self.BeginTPSpellsItem_Tx.update(self.text_color, config[profile_str]["begintpspells"])
        self.RandomTPSpellsItem_Tx.update(self.text_color, config[profile_str]["randomtpspells"])

    def itemUpdateConfig(self):
        if self.item == 'QuickSpellsItem':
            config[profile_str]["quickspells"] = str(int(config[profile_str]["quickspells"]) + 1)
        elif self.item == 'SlowSpellsItem':
            config[profile_str]["slowspells"] = str(int(config[profile_str]["slowspells"]) + 1)
        elif self.item == 'TurnBackSpellsItem':
            config[profile_str]["turnbackspells"] = str(int(config[profile_str]["turnbackspells"]) + 1)
        elif self.item == 'StopSpellsItem':
            config[profile_str]["stopspells"] = str(int(config[profile_str]["stopspells"]) + 1)
        elif self.item == 'EndTPSpellsItem':
            config[profile_str]["endtpspells"] = str(int(config[profile_str]["endtpspells"]) + 1)
        elif self.item == 'BeginTPSpellsItem':
            config[profile_str]["begintpspells"] = str(int(config[profile_str]["begintpspells"]) + 1)
        elif self.item == 'RandomTPSpellsItem':
            config[profile_str]["randomtpspells"] = str(int(config[profile_str]["randomtpspells"]) + 1)
        profileUpdate()

    def itemName(self):
        if self.item == 'QuickSpellsItem':
            return "Bùa nhanh"
        elif self.item == 'SlowSpellsItem':
            return "Bùa chậm"
        elif self.item == 'TurnBackSpellsItem':
            return "Bùa quay lại"
        elif self.item == 'StopSpellsItem':
            return "Bùa đứng yên"
        elif self.item == 'EndTPSpellsItem':
            return "Bùa về đích"
        elif self.item == 'BeginTPSpellsItem':
            return "Bùa về vạch xuất phát"
        elif self.item == 'RandomTPSpellsItem':
            return "Bùa dịch chuyển"

    def randomItem(self):
        self.item_random = random.randint(1, 200)
        if 1 <= self.item_random <= 40:
            self.item = 'QuickSpellsItem'
        elif 41 <= self.item_random <= 80:
            self.item = 'SlowSpellsItem'
        elif 81 <= self.item_random <= 100:
            self.item = 'StopSpellsItem'
        elif 101 <= self.item_random <= 120:
            self.item = 'TurnBackSpellsItem'
        elif self.item_random == 121:
            self.item = 'BeginTPSpellsItem'
        elif self.item_random == 122:
            self.item = 'EndTPSpellsItem'
        elif 123 <= self.item_random <= 140:
            self.item = 'RandomTPSpellsItem'
        elif 141 <= self.item_random <= 200:
            self.item = 'LostTurn'
        print(self.item)

    def handle_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                self.isReset = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            play_sound("res/sound/tick.wav")
            pos = event.pos
            if self.new_rect.collidepoint(pos) and self.angle == 0 and self.isHelp == 0:
                if 500 <= int(config[profile_str]["coin"]):
                    config[profile_str]["coin"] = str(int(config[profile_str]["coin"]) - 500)
                    with open(CONFIG_PATH, 'w') as configfile:
                        config.write(configfile)
                    self.randomItem()
                    self.isRotate = 1
                    gameMusic.sound.set_volume(0)
                    self.spinning_sound.play()
                    self.spinning_sound.sound.set_volume(isSoundOn)
            if self.backButton.isMouseOver(pos):
                self.spinning_sound.stop()
                gameMusic.sound.set_volume(isMusicOn)
                global scene
                scene = scenes["Menu"]
            if self.helpButton.isMouseOver(pos):
                self.isHelp = 1
            if self.helpMsb.okBtn.isMouseOver(pos) and self.isHelp:
                self.isHelp = 0        
            if self.congratMsb.okBtn.isMouseOver(pos) and self.isCongrat:
                self.isCongrat = 0
                self.isReset = 1
                gameMusic.sound.set_volume(isMusicOn)

class MinigameScene():
    def __init__(self):
        self.img = MINIGAMEIMG
        self.wheel_img = WHEEL_IMG
        self.arrow_img = ARROW_IMG
        self.isReset = 1
        self.spells_textcolor = BLACK
        self.helpButton = Button("?", 880, 10, 40, 40)
        self.backButton = Button("►", 930, 10, 40, 40)

        self.helpMsb = MessageBox(["========= HELP =========", "Click vào hình ảnh kéo, búa, bao bên trái để chọn", "Khi thắng 3 lần liên tiếp bạn sẽ nhận được 300 coins", "và 30% tỉ lệ nhận được bùa ngẫu nhiên"], 800, 230)

        self.scissors_img = SCISSORS_IMG
        self.rock_img = ROCK_IMG
        self.paper_img = PAPER_IMG

        self.scissors = pygame.transform.rotate(pygame.transform.scale(self.scissors_img, (150, 150)), -90)
        self.rock = pygame.transform.rotate(pygame.transform.scale(self.rock_img, (150, 150)), -90)
        self.paper = pygame.transform.rotate(pygame.transform.scale(self.paper_img, (150, 150)), -90)

        self.scissors_rect = self.scissors.get_rect(x = 100, y = 50)
        self.rock_rect = self.scissors.get_rect(x = 100, y = 225)
        self.paper_rect = self.scissors.get_rect(x = 100, y = 400)

    def reset(self):
        self.coin_tx = Text("Coins: " + config[profile_str]["coin"], "consolas", 20, (300, 20), BLACK)
        self.isReset = 0
        self.isCongrat = 0
        self.isHelp = 0
        self.congratList = ["CHÚC MỪNG", "Bạn vừa nhận được 300 coins"]        
        self.congratMsb = MessageBox(self.congratList, 430, 180)
        self.isUpdateCongratMsb = 0

        self.isChoose = 0
        self.isBotChoose = 0
        self.isFinish = 0

        self.player_choice = 0

        self.winner_tx = Text("", "consolas", 40, (300, 420), RED)
        self.reward_count_tx = Text("░ ░ ░", "consolas", 60, (425, 100), RED)
        self.reward_count = 0
        self.itemCreate()

    def itemCreate(self):
        self.QuickSpellsItem = QuickSpellsItem(500, 10)
        self.SlowSpellsItem = SlowSpellsItem(550, 10)
        self.TurnBackSpellsItem = TurnBackSpellsItem(600, 10)
        self.StopSpellsItem = StopSpellsItem(650, 10)
        self.EndTPSpellsItem = EndTPSpellsItem(700, 10)
        self.BeginTPSpellsItem = BeginTPSpellsItem(750, 10)
        self.RandomTPSpellsItem = RandomTPSpellsItem(800, 10)

        self.QuickSpellsItem_Tx = Text("0", "consolas", 20, (515, 55), self.spells_textcolor)
        self.SlowSpellsItem_Tx = Text("0", "consolas", 20, (565, 55), self.spells_textcolor)
        self.TurnBackSpellsItem_Tx = Text("0", "consolas", 20, (615, 55), self.spells_textcolor)
        self.StopSpellsItem_Tx = Text("0", "consolas", 20, (665, 55), self.spells_textcolor)
        self.EndTPSpellsItem_Tx = Text("0", "consolas", 20, (715, 55), self.spells_textcolor)
        self.BeginTPSpellsItem_Tx = Text("0", "consolas", 20, (765, 55), self.spells_textcolor)
        self.RandomTPSpellsItem_Tx = Text("0", "consolas", 20, (815, 55), self.spells_textcolor)

    def itemDraw(self):
        self.QuickSpellsItem.draw()
        self.SlowSpellsItem.draw()
        self.TurnBackSpellsItem.draw()
        self.StopSpellsItem.draw()
        self.EndTPSpellsItem.draw()
        self.BeginTPSpellsItem.draw()
        self.RandomTPSpellsItem.draw()

        self.QuickSpellsItem_Tx.draw()
        self.SlowSpellsItem_Tx.draw()
        self.TurnBackSpellsItem_Tx.draw()
        self.StopSpellsItem_Tx.draw()
        self.EndTPSpellsItem_Tx.draw()
        self.BeginTPSpellsItem_Tx.draw()
        self.RandomTPSpellsItem_Tx.draw()

    def draw(self):
        DISPLAYSURF.blit(self.img, (0, 0))

        self.helpButton.draw(DISPLAYSURF)
        self.backButton.draw(DISPLAYSURF)
        self.coin_tx.draw()

        DISPLAYSURF.blit(self.scissors, (100, 50))
        DISPLAYSURF.blit(self.rock, (100, 225))
        DISPLAYSURF.blit(self.paper, (100, 400))

        self.itemDraw()

        if self.isChoose:
            DISPLAYSURF.blit(pygame.transform.rotate(self.player, -90), (300, 200))
        if self.isBotChoose:
            DISPLAYSURF.blit(pygame.transform.rotate(self.bot, 90), (600, 200))
        if self.isBotChoose:
            self.winner_tx.draw()

        self.reward_count_tx.draw()

        if self.isCongrat:
            self.congratMsb.draw()
        if self.isHelp:
            self.helpMsb.draw()

    def update(self):
        if self.isReset:
            self.reset()

        if self.isChoose and not self.isBotChoose:
            self.isBotChoose = 1
            self.bot_rand = random.randint(1, 3)
            self.bot = self.scissors_img if self.bot_rand == 1 else (self.rock_img if self.bot_rand == 2 else self.paper_img)

            if self.bot_rand - self.player_choice in [1, -2]:
                self.winner_tx.update(RED, "BOT WIN")
                self.reward_count = 0
            elif self.bot_rand - self.player_choice in [-1, 2]:
               self.winner_tx.update(RED, "PLAYER WIN")
               self.reward_count += 1
            else:
                self.winner_tx.update(RED, "DRAW")

        if self.reward_count == 3 and not self.isFinish:
            self.isCongrat = 1
            self.isFinish = 1
            config[profile_str]["coin"] = str(int(config[profile_str]["coin"]) + 300)
            if random.randint(1, 10) <= 3:
                self.randomItem()
                self.congratList.append("và " + self.itemName())
                self.itemUpdateConfig()

            self.congratMsb = MessageBox(self.congratList, 430, 200)
            gameMusic.sound.set_volume(0)
            play_sound("res/sound/congratulation.mp3")

        self.reward_count_tx.update(RED, "░ ░ ░" if self.reward_count == 0 else ("█ ░ ░" if self.reward_count == 1 else ("█ █ ░" if self.reward_count == 2 else ("█ █ █"))))

        self.helpMsb.okBtn.hovered = self.helpMsb.okBtn.isMouseOver(pygame.mouse.get_pos())
        self.helpMsb.update()

        self.helpButton.hovered = self.helpButton.isMouseOver(pygame.mouse.get_pos())
        self.helpButton.update()
        self.backButton.hovered = self.backButton.isMouseOver(pygame.mouse.get_pos())
        self.backButton.update()
        self.coin_tx.update(BLACK, "Coins: " + config[profile_str]["coin"])

        self.congratMsb.okBtn.hovered = self.congratMsb.okBtn.isMouseOver(pygame.mouse.get_pos())
        self.congratMsb.update()

        self.itemUpdate()

    def itemUpdateConfig(self):
        if self.item == 'QuickSpellsItem':
            config[profile_str]["quickspells"] = str(int(config[profile_str]["quickspells"]) + 1)
        elif self.item == 'SlowSpellsItem':
            config[profile_str]["slowspells"] = str(int(config[profile_str]["slowspells"]) + 1)
        elif self.item == 'TurnBackSpellsItem':
            config[profile_str]["turnbackspells"] = str(int(config[profile_str]["turnbackspells"]) + 1)
        elif self.item == 'StopSpellsItem':
            config[profile_str]["stopspells"] = str(int(config[profile_str]["stopspells"]) + 1)
        elif self.item == 'EndTPSpellsItem':
            config[profile_str]["endtpspells"] = str(int(config[profile_str]["endtpspells"]) + 1)
        elif self.item == 'BeginTPSpellsItem':
            config[profile_str]["begintpspells"] = str(int(config[profile_str]["begintpspells"]) + 1)
        elif self.item == 'RandomTPSpellsItem':
            config[profile_str]["randomtpspells"] = str(int(config[profile_str]["randomtpspells"]) + 1)
        profileUpdate()

    def itemName(self):
        if self.item == 'QuickSpellsItem':
            return "Bùa nhanh"
        elif self.item == 'SlowSpellsItem':
            return "Bùa chậm"
        elif self.item == 'TurnBackSpellsItem':
            return "Bùa quay lại"
        elif self.item == 'StopSpellsItem':
            return "Bùa đứng yên"
        elif self.item == 'EndTPSpellsItem':
            return "Bùa về đích"
        elif self.item == 'BeginTPSpellsItem':
            return "Bùa về vạch xuất phát"
        elif self.item == 'RandomTPSpellsItem':
            return "Bùa dịch chuyển"

    def randomItem(self):
        self.item_random = random.randint(1, 100)
        if 1 <= self.item_random <= 35:
            self.item = 'QuickSpellsItem'
        elif 36 <= self.item_random <= 70:
            self.item = 'SlowSpellsItem'
        elif 71 <= self.item_random <= 80:
            self.item = 'StopSpellsItem'
        elif 81 <= self.item_random <= 90:
            self.item = 'TurnBackSpellsItem'
        elif self.item_random == 91:
            self.item = 'BeginTPSpellsItem'
        elif self.item_random == 92:
            self.item = 'EndTPSpellsItem'
        elif 93 <= self.item_random <= 100:
            self.item = 'RandomTPSpellsItem'
        print(self.item)

    def itemUpdate(self):
        self.QuickSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["quickspells"])
        self.SlowSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["slowspells"])
        self.TurnBackSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["turnbackspells"])
        self.StopSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["stopspells"])
        self.EndTPSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["endtpspells"])
        self.BeginTPSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["begintpspells"])
        self.RandomTPSpellsItem_Tx.update(self.spells_textcolor, config[profile_str]["randomtpspells"])


    def handle_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                self.isReset = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            play_sound("res/sound/tick.wav")
            pos = event.pos
            if self.backButton.isMouseOver(pos):
                global scene
                scene = scenes["Menu"]
            if self.helpButton.isMouseOver(pos):
                self.isHelp = 1
            if self.helpMsb.okBtn.isMouseOver(pos) and self.isHelp:
                self.isHelp = 0         
            if self.congratMsb.okBtn.isMouseOver(pos) and self.isCongrat:
                self.isCongrat = 0
                self.isReset = 1
                gameMusic.sound.set_volume(isMusicOn)
            if not self.isHelp and not self.isCongrat:
                if self.scissors_rect.collidepoint(pos):
                    self.isBotChoose = 0
                    self.player = self.scissors_img
                    self.player_choice = 1
                    self.isChoose = 1
                if self.paper_rect.collidepoint(pos):
                    self.isBotChoose = 0
                    self.player = self.paper_img
                    self.player_choice = 3
                    self.isChoose = 1
                if self.rock_rect.collidepoint(pos):
                    self.isBotChoose = 0
                    self.player = self.rock_img
                    self.player_choice = 2
                    self.isChoose = 1

class Animal():
    def __init__(self, img, x, y, number):
        self.width = ANIWIDTH
        self.height = ANIHEIGHT
        self.x = x
        self.y = y
        self.speed = ANISPEED
        self.maxspeed = ANIMAXSPEED
        self.distance = 0
        self.top = 0
        self.isFinish = 0
        self.current_top = 1
        self.number = number
        self.img = img
        self.item = Item(ITEM_IMG["quickspells"], 880, 10)
        self.direction = 1
        self.rect = self.img.get_rect(x = self.x, y = self.y)
        self.jumphigh = 0
        self.isfalldown = 0

    def draw(self):
        if self.direction == 1:
            DISPLAYSURF.blit(self.img, self.rect)
        else:
            DISPLAYSURF.blit(pygame.transform.flip(self.img, True, False), self.rect)

        self.item.draw()
    def update(self):
        self.speed = random.randint(0, ANIMAXSPEED) #random toc do

        self.direction = 1
        #update bua
        if self.item.isPicked == 1:
            self.item.effect(self)

        self.item.update()

        #update hinh anh
        if self.distance < ANI_MAXDISTANCE:
            self.x += self.speed * self.direction
            self.distance += self.speed * self.direction
        else:
            self.x = ANI_MAXDISTANCE + ANI_LEFT
            self.isFinish = 1

        self.rect.x = self.x
        self.rect.y = self.y

        #kiem tra nhat bua
        if self.isItemPicked():
            self.onItemPicked()

        if self.isFinish and self.top <= 3:
            self.celebration()
    def celebration(self):
        if self.isfalldown:
            self.y += 1
            self.jumphigh -= 1
        else:
            self.y -= 1
            self.jumphigh += 1
        if self.jumphigh >= 15:
            self.isfalldown = 1
        if self.jumphigh <= -5:
            self.isfalldown = 0

    def isItemPicked(self):
        return self.item.rect.colliderect(self.rect)

    def onItemPicked(self):
        self.item.isPicked = 1
        play_sound(self.item.sound_path)

    def randomItem(self):
        self.item_random = random.randint(1,100)
        if 1 <= self.item_random <= 35:
            self.item = QuickSpellsItem(self.x + 100, self.y)
        elif 36 <= self.item_random <= 70:
            self.item = SlowSpellsItem(self.x + 100, self.y)
        elif 71 <= self.item_random <= 82:
            self.item = StopSpellsItem(self.x + 100, self.y)
        elif 83 <= self.item_random <= 88:
            self.item = TurnBackSpellsItem(self.x + 100, self.y)
        elif self.item_random == 89:
            self.item = BeginTPSpellsItem(self.x + 100, self.y)
        elif self.item_random == 90:
            self.item = EndTPSpellsItem(self.x + 100, self.y)
        elif 91 <= self.item_random <= 100:
            self.item = RandomTPSpellsItem(self.x + 100, self.y)

class Item():
    def __init__(self, img, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.img = img
        self.isPicked = 0
        self.rect = self.img.get_rect(x = self.x, y = self.y)

    def draw(self):
        DISPLAYSURF.blit(self.img, self.rect)
    def update(self):
        if self.isPicked:
            self.x = 880
            self.y = 10
            self.rect.x = self.x
            self.rect.y = self.y
        else:
            self.rect.x = self.x
            self.rect.y = self.y

    def isMouseOver(self, pos):
        return self.rect.collidepoint(pos)

class Player():
    def __init__(self):
        self.choice = 6
        self.coinbetted = 0     

class QuickSpellsItem(Item):
    def __init__(self, x, y):
        super(QuickSpellsItem, self).__init__(ITEM_IMG["quickspells"], x, y)
        self.time = 1000 #miliseconds
        self.start_ticks = 0
        self.end_ticks = 0
        self.sound_path = "res/sound/quickspells.mp3"
    def effect(self, ani):
        if (self.end_ticks - self.start_ticks < self.time):
            self.start_ticks = pygame.time.get_ticks() if self.start_ticks == 0 else self.start_ticks
            self.end_ticks = pygame.time.get_ticks()
            ani.speed += ANISPEED
        else:
            self.start_ticks = 0
            self.end_ticks = 0     
            self.isPicked = 0

class SlowSpellsItem(Item):
    def __init__(self, x, y):
        super(SlowSpellsItem, self).__init__(ITEM_IMG["slowspells"], x, y)
        self.time = 1500 #miliseconds
        self.start_ticks = 0
        self.end_ticks = 0
        self.sound_path = "res/sound/slowspells.flac"
    def effect(self, ani):
        if (self.end_ticks - self.start_ticks < self.time):
            self.start_ticks = pygame.time.get_ticks() if self.start_ticks == 0 else self.start_ticks
            self.end_ticks = pygame.time.get_ticks()
            ani.speed = 0 if (random.randint(1, 10) < 9) else 1
            # ani.speed -= 1
        else:
            self.start_ticks = 0
            self.end_ticks = 0     
            self.isPicked = 0
        
class TurnBackSpellsItem(Item):
    def __init__(self, x, y):
        super(TurnBackSpellsItem, self).__init__(ITEM_IMG["turnbackspells"], x, y)
        self.time = 1000 #miliseconds
        self.start_ticks = 0
        self.end_ticks = 0
        self.sound_path = "res/sound/quickspells.mp3"
    def effect(self, ani):
        if (self.end_ticks - self.start_ticks < self.time):
            self.start_ticks = pygame.time.get_ticks() if self.start_ticks == 0 else self.start_ticks
            self.end_ticks = pygame.time.get_ticks()
            ani.direction = -1
        else:
            self.start_ticks = 0
            self.end_ticks = 0   
            self.isPicked = 0
            ani.direction = 1

class StopSpellsItem(Item):
    def __init__(self, x, y):
        super(StopSpellsItem, self).__init__(ITEM_IMG["stopspells"], x, y)
        self.time = 1000 #miliseconds
        self.start_ticks = 0
        self.end_ticks = 0
        self.sound_path = "res/sound/stopspells.wav"
    def effect(self, ani):
        if (self.end_ticks - self.start_ticks < self.time):
            self.start_ticks = pygame.time.get_ticks() if self.start_ticks == 0 else self.start_ticks
            self.end_ticks = pygame.time.get_ticks()
            ani.speed = 0
        else:
            self.start_ticks = 0
            self.end_ticks = 0     
            self.isPicked = 0

class EndTPSpellsItem(Item):
    def __init__(self, x, y):
        super(EndTPSpellsItem, self).__init__(ITEM_IMG["endtpspells"], x, y)
        self.sound_path = "res/sound/teleportspells.wav"
    def effect(self, ani):
        ani.speed = ANI_MAXDISTANCE + ANI_LEFT - ani.x
        self.update()
        self.isPicked = 0  

class BeginTPSpellsItem(Item):
    def __init__(self, x, y):
        super(BeginTPSpellsItem, self).__init__(ITEM_IMG["begintpspells"], x, y)
        self.sound_path = "res/sound/teleportspells.wav"
    def effect(self, ani):
        ani.speed = ANI_LEFT - ani.x
        self.update()
        self.isPicked = 0 

class RandomTPSpellsItem(Item):
    def __init__(self, x, y):
        super(RandomTPSpellsItem, self).__init__(ITEM_IMG["randomtpspells"], x, y)
        self.sound_path = "res/sound/teleportspells.wav"
    def effect(self, ani):
        ani.speed = ANI_LEFT - ani.x + random.randint(0, ANI_MAXDISTANCE)
        self.update()
        self.isPicked = 0  
        
class RaceTrack():
    def __init__(self):
        self.thick = RACETRACK_THICK
        self.top = ANI_TOP - self.thick - 7
        self.left = ANI_LEFT - self.thick
        self.height = LANE_DISTANCE
        self.width = RACETRACK_LENGTH
        self.rect_height = self.width + 2 * self.thick
        self.rect_width = self.thick + 6 * self.height
        self.linecolor = GREEN
        self.bgcolor = WHITE

    def draw(self):
        self.s = pygame.Surface((self.rect_height, self.rect_width), pygame.SRCALPHA)   # per-pixel alpha
        self.s.fill((255,255,255,128))                         # notice the alpha value in the color
        DISPLAYSURF.blit(self.s, (self.left, self.top))
        # pygame.draw.rect(DISPLAYSURF, self.bgcolor, (self.left, self.top, self.rect_height, self.rect_width))  # khung chu nhat
        pygame.draw.rect(DISPLAYSURF, self.linecolor, (self.left, self.top, self.thick, self.rect_width))  # canh left
        pygame.draw.rect(DISPLAYSURF, self.linecolor, (self.left + self.rect_height - self.thick, self.top, self.thick, self.rect_width))  # canh phai
        pygame.draw.rect(DISPLAYSURF, self.linecolor, (self.left, self.top, self.rect_height, self.thick))  # canh top
        pygame.draw.rect(DISPLAYSURF, self.linecolor, (self.left, self.top + self.rect_width-self.thick, self.rect_height, self.thick))  # canh duoi
        pygame.draw.rect(DISPLAYSURF, self.linecolor, (self.left + self.thick, self.top + self.height, self.width, self.thick))  # 1
        pygame.draw.rect(DISPLAYSURF, self.linecolor, (self.left + self.thick, self.top + self.height*2, self.width, self.thick))  # 2
        pygame.draw.rect(DISPLAYSURF, self.linecolor, (self.left + self.thick, self.top + self.height*3, self.width, self.thick))  # 3
        pygame.draw.rect(DISPLAYSURF, self.linecolor, (self.left + self.thick, self.top + self.height*4, self.width, self.thick))  # 4
        pygame.draw.rect(DISPLAYSURF, self.linecolor, (self.left + self.thick, self.top + self.height*5, self.width, self.thick))  # 5

class Text():
    def __init__(self, text, font_name, size, pos, color):
        self.text = text
        self.font_name = font_name
        self.size = size
        self.color = color
        self.isUpdate = 0
        self.font = pygame.font.SysFont(self.font_name, self.size)
        self.surface = self.font.render(self.text, True, self.color)
        self.surfaceSize = self.surface.get_size()
        self.x = int((WINDOWWIDTH - self.surfaceSize[0])/2) if (pos[0] == CENTER) else pos[0]
        self.y = int((WINDOWHEIGHT - self.surfaceSize[1])/2) if (pos[1] == CENTER) else pos[1]
        self.rect = self.surface.get_rect(x = self.x, y = self.y)
        
    def draw(self):
        DISPLAYSURF.blit(self.surface, self.rect)
    def update(self, color, text, x = -1, y = -1):
        self.rect.x = self.x = self.x if x == -1 else (int((WINDOWWIDTH - self.surfaceSize[0])/2) if (x == CENTER) else x)
        self.rect.y = self.y = self.y if y == -1 else (int((WINDOWWIDTH - self.surfaceSize[0])/2) if (y == CENTER) else y)
        self.rect = self.surface.get_rect(x = self.x, y = self.y)
        self.color = color
        self.text = text
        self.surface = self.font.render(self.text, True, self.color)
        self.surfaceSize = self.surface.get_size()
    def isMouseOver(self, pos):
        return self.rect.collidepoint(pos)

class InputBox():
    def __init__(self, x, y, w, h, hidden_content = "", isPassword = False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.text = ""
        self.active = 1
        self.font = pygame.font.SysFont("consolas", 30)
        self.hidden_content = hidden_content
        self.txt_surface = self.font.render(self.text + ("█" if self.active else ""), True, BLACK)
        self.allow = 1
        self.isPassword = isPassword
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            self.active = self.isMouseOver(pos)
        if event.type == pygame.KEYDOWN:
            play_sound("res/sound/gun.wav")
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.allow:
                        self.text += event.unicode

    def update(self):
        self.allow = 1 if max(self.rect.w, self.txt_surface.get_width() + 50) == self.rect.w else 0
        if len(self.text) > 0:
            self.txt_surface = self.font.render(((len(self.text) * '●') if self.isPassword else self.text) + ("█" if self.active else ""), True, BLACK)
        else:
            self.txt_surface = self.font.render(("█" if self.active else self.hidden_content), True, (BLACK if self.active else SHADOW))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        self.text_size = self.txt_surface.get_size()
        screen.blit(self.txt_surface, (int(self.rect.x + (self.rect.w - self.text_size[0]) / 2), int(self.rect.y + (self.rect.h - self.text_size[1]) / 2)))

    def isMouseOver(self, pos):
        return self.rect.collidepoint(pos)

class MessageBox():
    def __init__(self, text, w, h, font_size = 25):
        self.text = text
        self.image_normal = pygame.Surface((w, h))
        self.image_normal.fill(WHITE)
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont('consolas', font_size)
        i = 0
        for tx in self.text:
            i += 1
            text_image = self.font.render(tx, True, BLUE)
            text_rect = text_image.get_rect(centerx = int(w / 2), y = 30 * i)
            self.image_normal.blit(text_image, text_rect)

        self.rect.topleft = (int((WINDOWWIDTH - w) / 2), int((WINDOWHEIGHT - h) / 2))
        self.rect = pygame.Rect(int((WINDOWWIDTH - w) / 2), int((WINDOWHEIGHT - h) / 2), w, h)  
        self.okBtn = Button("OK", int((WINDOWWIDTH - 50) / 2), self.rect.y + self.rect.h - 60, 50, 40)
    def draw(self):
        DISPLAYSURF.blit(self.image, self.rect)
        pygame.draw.rect(DISPLAYSURF, BLUE, self.rect, 5)
        self.okBtn.draw(DISPLAYSURF)
    def update(self):
        self.okBtn.hovered = self.okBtn.isMouseOver(pygame.mouse.get_pos())
        self.okBtn.update()

class Button():
    def __init__(self, text, x = 0, y = 0, width = 100, height = 50):
        self.text = text
        self.image_normal = pygame.Surface((width, height))
        self.image_normal.fill(YELLOW)
        self.image_hovered = pygame.Surface((width, height))
        self.image_hovered.fill(RED)
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        font = pygame.font.SysFont('consolas', 35)
        text_image = font.render(text, True, BLUE)
        text_rect = text_image.get_rect(center = self.rect.center)
        self.image_normal.blit(text_image, text_rect)
        self.image_hovered.blit(text_image, text_rect)

        self.rect.topleft = (x, y)

        self.hovered = False

    def update(self):
        if self.hovered:
            self.image = self.image_hovered
        else:
            self.image = self.image_normal

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        pygame.draw.rect(DISPLAYSURF, BLUE, self.rect, 3)

    def isMouseOver(self, pos):
        return self.rect.collidepoint(pos)

class Sound():
    def __init__(self, path):
        self.canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        self.sound = pygame.mixer.Sound(self.canonicalized_path)
    def play(self, loops = -1):
        self.sound.play(loops)
    def stop(self):
        self.sound.stop()

def profileUpdate():
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)

def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    sound.play()
    sound.set_volume(isSoundOn)

config = configparser.ConfigParser()
config.read(CONFIG_PATH)
try:
    config['PROFILE']['profiles']
except Exception as e:
    CONFIG_ISEXIST = 0
    config.add_section('PROFILE')
    config['PROFILE']['profiles'] = '0'
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)
else:
    CONFIG_ISEXIST = 1
    CONFIG_PROFILES = int(config['PROFILE']['profiles'])

profiles = 0 if (CONFIG_ISEXIST == 0 or CONFIG_PROFILES == 0) else CONFIG_PROFILES

scenes = {
    "Profile": ProfileScene(),
    "NewProfile": NewProfileScene(),
    "Menu": MenuScene(),
    "Game": GameScene(),
    "Store": StoreScene(),
    "Minigame": MinigameScene(),
    "Options": OptionsScene()
}


gameMusic = Sound("res/sound/gamemusic.mp3")
gameMusic.play(-1)
gameMusic.sound.set_volume(isMusicOn)
scene = scenes["NewProfile"] if (profiles == 0) else scenes["Profile"]



def main():
    while True:
        for event in pygame.event.get():
            scene.handle_event(event)
        scene.update()
        scene.draw()

        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()

#Update 22h 03/01/2021
#Thêm bùa vào minigame: 30% tỉ lệ xuất hiện khi thắng liên tục ba lần
#Sửa số tiền mất cho vòng quay cửa hàng thành 500
#Hiệu ứng nhảy lên nhảy xuống khi về đích và nằm trong top 3 của nhân vật
#Đổi tên mục CHANGE PROFILE thành LOG OUT
#Thêm mục OPTIONS cho phép chọn nền Game và bật tắt nhạc/âm thanh
#Thêm điều kiện tài khoản đã tồn tại khi SIGN UP
#Thêm icon
#Thêm thông báo hiển thị thắng/thua khi ấn vào dòng Welcome... ở Menu