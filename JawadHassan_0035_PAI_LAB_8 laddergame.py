"""
Name: Jawad Hassan
Pai
2230-0035
bs ai
Resizable Cinematic Snakes & Ladders
Fully dynamic window size with scaling tokens, snakes, ladders, dice, and UI.
Requires: pygame, numpy
"""

import pygame, sys, random, numpy as np, colorsys

# ---------------- Configuration ----------------
BOARD_CELLS = 10
MARGIN_BOTTOM_RATIO = 0.2  # Bottom UI height fraction
FPS = 60
ANIM_STEPS_PER_CELL = 12
NUM_LADDERS = 3
NUM_SNAKES = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 230)
PLAYER_COLORS = [(50, 120, 255), (230, 60, 90)]
LADDER_COLOR = (180, 140, 50)
SNAKE_COLOR = (220, 50, 50)
CONFETTI_COLORS = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]

# ---------------- Pygame Init ----------------
pygame.init()
try: pygame.mixer.init()
except: print("Warning: sound disabled")

# ---------------- Sounds ----------------
def generate_tone(freq=440,length_ms=200,vol=0.3,samplerate=44100):
    if not pygame.mixer.get_init(): return None
    t = np.linspace(0,length_ms/1000,int(samplerate*length_ms/1000),endpoint=False)
    wave = np.sin(2*np.pi*freq*t)*vol
    audio = np.int16(wave*32767)
    return pygame.sndarray.make_sound(np.stack([audio,audio],axis=-1))

DICE_SOUND = generate_tone(800,150)
LADDER_SOUND = generate_tone(1000,200)
SNAKE_SOUND = generate_tone(400,200)
WIN_SOUND = generate_tone(1200,500)

# ---------------- Helpers ----------------
def hsv_to_rgb(h, s, v):
    r,g,b = colorsys.hsv_to_rgb(h/360,s,v)
    return int(r*255), int(g*255), int(b*255)

# ---------------- Confetti ----------------
class Confetti:
    def __init__(self): self.particles=[]
    def spawn(self,num,x_range,y_range):
        for _ in range(num):
            x=random.randint(*x_range)
            y=random.randint(*y_range)
            dx=random.uniform(-3,3); dy=random.uniform(-6,-1)
            color=random.choice(CONFETTI_COLORS)
            self.particles.append({"x":x,"y":y,"dx":dx,"dy":dy,"color":color,"life":random.randint(30,60)})
    def update_draw(self,screen):
        for p in self.particles:
            p["x"]+=p["dx"]; p["y"]+=p["dy"]; p["life"]-=1
            pygame.draw.circle(screen,p["color"],(int(p["x"]),int(p["y"])),3)
        self.particles=[p for p in self.particles if p["life"]>0]
confetti=Confetti()

# ---------------- Dice ----------------
class Dice:
    def __init__(self,pos,size):
        self.value=1
        self.rolling=False
        self.roll_frames=0
        self.pos=pos
        self.size=size
        self.angle=0
    def start_roll(self):
        self.rolling=True; self.roll_frames=15
        if DICE_SOUND: DICE_SOUND.play()
    def update(self):
        if self.rolling:
            self.roll_frames-=1
            self.value=random.randint(1,6)
            self.angle+=30
            if self.roll_frames<=0: self.rolling=False
    def draw(self,screen):
        surf=pygame.Surface((self.size,self.size),pygame.SRCALPHA)
        pygame.draw.rect(surf,(255,255,255),[0,0,self.size,self.size],border_radius=8)
        font_size = max(12,int(self.size*0.6))
        font = pygame.font.SysFont(None,font_size,bold=True)
        text_surf = font.render(str(self.value),True,BLACK)
        rect = text_surf.get_rect(center=(self.size//2,self.size//2))
        surf.blit(text_surf, rect)
        rotated=pygame.transform.rotate(surf,self.angle)
        rect=rotated.get_rect(center=self.pos)
        screen.blit(rotated,rect)

# ---------------- Game ----------------
class SnLGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((800,1000), pygame.RESIZABLE)
        pygame.display.set_caption("Resizable Snakes & Ladders")
        self.clock = pygame.time.Clock()
        self.reset_game()
        self.ask_ladder_placement = True
        self.placing_ladder = False
        self.ladder_clicks = []
        self.update_sizes()

    # ---------------- Resizing ----------------
    def update_sizes(self):
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = self.screen.get_size()
        self.MARGIN_BOTTOM = int(self.WINDOW_HEIGHT*0.2)
        self.board_height = self.WINDOW_HEIGHT - self.MARGIN_BOTTOM
        self.board_width = self.WINDOW_WIDTH
        self.cell = min(self.board_width, self.board_height) // BOARD_CELLS
        self.token_radius = int(self.cell*0.4)
        # Buttons
        self.roll_rect = pygame.Rect(20, self.WINDOW_HEIGHT - self.MARGIN_BOTTOM + 30, 150, 50)
        self.restart_rect = pygame.Rect(200, self.WINDOW_HEIGHT - self.MARGIN_BOTTOM + 30, 150, 50)
        self.yes_rect = pygame.Rect(self.WINDOW_WIDTH // 2 - 150, self.WINDOW_HEIGHT // 2, 120, 50)
        self.no_rect = pygame.Rect(self.WINDOW_WIDTH // 2 + 30, self.WINDOW_HEIGHT // 2, 120, 50)
        self.dice = Dice((self.WINDOW_WIDTH - 120, self.WINDOW_HEIGHT - self.MARGIN_BOTTOM + 70), size=int(self.cell*0.8))

    # ---------------- Helpers ----------------
    def square_to_xy(self, square):
        s = max(1,min(100,square))
        n = s-1
        row = n // BOARD_CELLS
        col = n % BOARD_CELLS
        if row % 2 == 1: col = BOARD_CELLS-1-col
        x = col*self.cell + self.cell//2
        y = (BOARD_CELLS-1-row)*self.cell + self.cell//2
        return x, y

    def draw_text(self,surf,text,size,x,y,color=BLACK,bold=False,center=True):
        font = pygame.font.SysFont(None,size,bold=bold)
        surf_text = font.render(str(text),True,color)
        rect = surf_text.get_rect()
        rect.center = (x,y) if center else (x,y)
        surf.blit(surf_text,rect)

    # ---------------- Game state ----------------
    def reset_game(self):
        self.players=[{"pos":1},{"pos":1}]
        self.current=0
        self.last_roll=None
        self.animating=False
        self.anim_path=[]
        self.anim_player=None
        self.msg=f"Player 1's turn"
        self.winner=None
        self.LADDERS={}
        self.SNAKES={}
        self.placing_ladder=False
        self.ladder_clicks=[]
        self.set_random_snakes()

    def set_random_snakes(self):
        placed=0
        while placed<NUM_SNAKES:
            start=random.randint(2,99)
            end=random.randint(1,start-1)
            if start in self.LADDERS or start in self.SNAKES or end in self.LADDERS.values() or end in self.SNAKES.values(): continue
            self.SNAKES[start]=end
            placed+=1

    # ---------------- Drawing ----------------
    def draw_board(self):
        for s in range(1,101):
            x, y = self.square_to_xy(s)
            hue = (s-1)*3.6
            color = hsv_to_rgb(hue, 0.6, 0.9)
            rect = pygame.Rect(x - self.cell//2, y - self.cell//2, self.cell, self.cell)
            pygame.draw.rect(self.screen, color, rect)
        # Draw numbers
        for s in range(1, 101):
            x, y = self.square_to_xy(s)
            self.draw_text(self.screen, s, max(12,int(self.cell*0.3)), x, y-15, BLACK)
        # Draw ladders
        for a,b in self.LADDERS.items():
            x1,y1=self.square_to_xy(a)
            x2,y2=self.square_to_xy(b)
            pygame.draw.line(self.screen,LADDER_COLOR,(x1,y1),(x2,y2), max(4,int(self.cell*0.08)))
            pygame.draw.circle(self.screen,LADDER_COLOR,(x1,y1), max(3,int(self.cell*0.06)))
        # Draw snakes
        for a,b in self.SNAKES.items():
            x1,y1=self.square_to_xy(a)
            x2,y2=self.square_to_xy(b)
            points=[(x1,y1)]
            for t in range(1,6):
                midx = x1 + (x2-x1)*t/6 + random.randint(-self.cell//15,self.cell//15)
                midy = y1 + (y2-y1)*t/6 + random.randint(-self.cell//15,self.cell//15)
                points.append((midx,midy))
            points.append((x2,y2))
            pygame.draw.lines(self.screen,SNAKE_COLOR,False,points, max(4,int(self.cell*0.08)))
            pygame.draw.circle(self.screen,SNAKE_COLOR,(x1,y1), max(5,int(self.cell*0.12)))

    def draw_tokens(self):
        for i,p in enumerate(self.players):
            x=p.get("pos_x",self.square_to_xy(p["pos"])[0])
            y=p.get("pos_y",self.square_to_xy(p["pos"])[1])
            offset_x = -self.token_radius if i==0 else self.token_radius
            glow_color=PLAYER_COLORS[i]
            pygame.draw.circle(self.screen,glow_color,(int(x+offset_x*0.2),int(y)),self.token_radius+int(self.cell*0.1))
            pygame.draw.circle(self.screen,WHITE,(int(x+offset_x*0.2),int(y)),self.token_radius)
            pygame.draw.circle(self.screen,glow_color,(int(x+offset_x*0.2),int(y)),self.token_radius-int(self.cell*0.1),2)
            self.draw_text(self.screen,str(i+1), max(12,int(self.cell*0.3)), int(x+offset_x*0.2), int(y), PLAYER_COLORS[i], bold=True)

    def draw_ui(self):
        panel_rect=pygame.Rect(0,self.WINDOW_HEIGHT-self.MARGIN_BOTTOM,self.WINDOW_WIDTH,self.MARGIN_BOTTOM)
        pygame.draw.rect(self.screen,(220,220,230),panel_rect)
        mouse_pos=pygame.mouse.get_pos()
        if self.ask_ladder_placement:
            pygame.draw.rect(self.screen,BUTTON_COLOR,self.yes_rect,border_radius=8)
            pygame.draw.rect(self.screen,BUTTON_COLOR,self.no_rect,border_radius=8)
            self.draw_text(self.screen,"YES", max(12,int(self.cell*0.3)),self.yes_rect.centerx,self.yes_rect.centery,WHITE,bold=True)
            self.draw_text(self.screen,"NO", max(12,int(self.cell*0.3)),self.no_rect.centerx,self.no_rect.centery,WHITE,bold=True)
            self.draw_text(self.screen,"Place ladders manually?", max(14,int(self.cell*0.35)),self.WINDOW_WIDTH//2,self.WINDOW_HEIGHT//2-60,BLACK,bold=True)
        else:
            roll_color=BUTTON_HOVER if self.roll_rect.collidepoint(mouse_pos) else BUTTON_COLOR
            restart_color=BUTTON_HOVER if self.restart_rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(self.screen,roll_color,self.roll_rect,border_radius=8)
            pygame.draw.rect(self.screen,restart_color,self.restart_rect,border_radius=8)
            self.draw_text(self.screen,"ROLL DICE", max(12,int(self.cell*0.3)),self.roll_rect.centerx,self.roll_rect.centery,WHITE,bold=True)
            self.draw_text(self.screen,"Restart", max(12,int(self.cell*0.3)),self.restart_rect.centerx,self.restart_rect.centery,WHITE,bold=True)
            self.draw_text(self.screen,f"Last roll: {self.last_roll if self.last_roll else '-'}", max(12,int(self.cell*0.3)), 450,self.WINDOW_HEIGHT-self.MARGIN_BOTTOM+35,center=False)
            self.draw_text(self.screen,f"Turn: Player {self.current+1}", max(12,int(self.cell*0.3)), 450,self.WINDOW_HEIGHT-self.MARGIN_BOTTOM+70,center=False)
            self.draw_text(self.screen,self.msg, max(12,int(self.cell*0.3)), 450,self.WINDOW_HEIGHT-self.MARGIN_BOTTOM+110,center=False)
            self.dice.draw(self.screen)
        confetti.update_draw(self.screen)

    # ---------------- Game Logic ----------------
    def roll_and_move(self):
        if self.animating or self.winner: return
        self.dice.start_roll()
        roll=random.randint(1,6)
        self.last_roll=roll
        player=self.players[self.current]
        start=player["pos"]
        tentative=start+roll
        if tentative>100: tentative=start

        path_squares=[sq for sq in range(start+1,tentative+1)]
        pixel_path=[]
        prev_sq=start
        for sq in path_squares:
            x1,y1=self.square_to_xy(prev_sq)
            x2,y2=self.square_to_xy(sq)
            for t in range(1,ANIM_STEPS_PER_CELL+1):
                fx = x1 + (x2-x1)*(t/ANIM_STEPS_PER_CELL)
                fy = y1 + (y2-y1)*(t/ANIM_STEPS_PER_CELL)
                pixel_path.append((fx,fy,sq))
            prev_sq=sq

        land_sq=tentative
        final_sq=self.LADDERS.get(tentative,self.SNAKES.get(tentative,tentative))
        if final_sq!=land_sq:
            x1,y1=self.square_to_xy(land_sq)
            x2,y2=self.square_to_xy(final_sq)
            steps=ANIM_STEPS_PER_CELL*abs(final_sq-land_sq)
            for t in range(1,steps+1):
                fx=x1+(x2-x1)*(t/steps)
                fy=y1+(y2-y1)*(t/steps)
                pixel_path.append((fx,fy,final_sq))
            if final_sq in self.LADDERS and LADDER_SOUND: LADDER_SOUND.play()
            elif final_sq in self.SNAKES and SNAKE_SOUND: SNAKE_SOUND.play()

        self.animating=True
        self.anim_path=pixel_path
        self.anim_player=self.current
        self._pending_final_pos=final_sq
        self.msg=f"Player {self.current+1} rolled {roll}"

    def update_animation(self):
        self.dice.update()
        if not self.animating or not self.anim_path:
            if self.animating:
                self.players[self.anim_player]["pos"]=self._pending_final_pos
                self.players[self.anim_player].pop("pos_x",None)
                self.players[self.anim_player].pop("pos_y",None)
                if self.players[self.anim_player]["pos"]==100:
                    self.winner=self.anim_player
                    self.msg=f"Player {self.winner+1} wins! 🎉"
                    if WIN_SOUND: WIN_SOUND.play()
                    confetti.spawn(150,(0,self.WINDOW_WIDTH),(0,self.WINDOW_HEIGHT))
                else:
                    self.current=1-self.current
                    self.msg=f"Player {self.current+1}'s turn"
                self.animating=False
            return
        fx,fy,sq=self.anim_path.pop(0)
        self.players[self.anim_player]["pos_x"]=fx
        self.players[self.anim_player]["pos_y"]=fy
        self.players[self.anim_player]["pos"]=sq

    # ---------------- Click Handling ----------------
    def handle_click(self,pos):
        if self.ask_ladder_placement:
            if self.yes_rect.collidepoint(pos):
                self.placing_ladder=True
                self.ask_ladder_placement=False
                self.msg="Click two squares for each ladder"
            elif self.no_rect.collidepoint(pos):
                self.placing_ladder=False
                self.ask_ladder_placement=False
            return

        if self.winner and self.restart_rect.collidepoint(pos):
            self.reset_game(); return
        if self.animating: return
        if self.placing_ladder:
            for s in range(1,101):
                x,y=self.square_to_xy(s)
                rect=pygame.Rect(x-self.cell//2,y-self.cell//2,self.cell,self.cell)
                if rect.collidepoint(pos):
                    self.ladder_clicks.append(s)
                    if len(self.ladder_clicks)==2:
                        start,end=sorted(self.ladder_clicks)
                        if start in self.LADDERS or start in self.SNAKES or end in self.LADDERS.values() or end in self.SNAKES.values():
                            self.msg="Invalid ladder placement!"
                        else:
                            self.LADDERS[start]=end
                            self.msg=f"Ladder placed: {start}->{end}"
                        self.ladder_clicks=[]
                        if len(self.LADDERS)>=NUM_LADDERS: self.placing_ladder=False
                    return
        if self.roll_rect.collidepoint(pos): self.roll_and_move()
        elif self.restart_rect.collidepoint(pos): self.reset_game()

    # ---------------- Main Loop ----------------
    def run(self):
        while True:
            self.clock.tick(FPS)
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                    self.update_sizes()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.roll_and_move()
                    elif event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
            # Update animation
            if self.animating:
                self.update_animation()
            # Draw everything
            self.screen.fill((245,245,250))
            self.draw_board()
            self.draw_tokens()
            self.draw_ui()
            pygame.display.flip()

# ---------------- Run ----------------
if __name__=="__main__":
    game=SnLGame()
    game.run()
