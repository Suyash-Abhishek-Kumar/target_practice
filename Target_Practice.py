import pygame
from random import randint

pygame.init()

WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Button:
    def __init__(self, screen, loc, width, name, func):
        self.screen = screen
        self.location = loc
        self.width = width
        self.bold_width = self.width + 3
        self.width_copy = width
        self.name = name
        self.name_rect = self.name.get_rect()
        self.box_rect = self.name.get_rect()
        self.name_size = self.name_rect.size
        self.box_rect.size = (self.name_size[0] + 10, self.name_size[1] + 7)
        self.name_rect.center = self.location
        self.box_rect.center = self.location
        self.function = func
        print(self.box_rect.size, self.location)

    def run(self):
        self.collision_check()
        pygame.draw.rect(self.screen, WHITE, self.box_rect, self.width)
        self.screen.blit(self.name, self.name_rect)

    def collision_check(self):
        mouse_pos = pygame.mouse.get_pos()
        if abs(mouse_pos[0] - self.location[0]) < self.box_rect.size[0] // 2 and abs(
                mouse_pos[1] - self.location[1]) < self.box_rect.size[1] // 2:
            self.width = self.bold_width
            return True
        else:
            self.width = self.width_copy
            return False


class Target:
    def __init__(self, screen, loc, size, speed):
        self.screen = screen
        self.location = loc
        self.size = size
        self.shrink_speed = (60 * speed) // self.size
        self.countdown = self.shrink_speed

    def run(self):
        pygame.draw.circle(self.screen, BLACK, self.location, self.size)
        pygame.draw.circle(self.screen, BLUE, self.location, self.size * 0.75)
        pygame.draw.circle(self.screen, RED, self.location, self.size * 0.5)
        pygame.draw.circle(self.screen, YELLOW, self.location, self.size * 0.25)
        if self.countdown == 0:
            self.size -= 1
            self.countdown = self.shrink_speed
        else:
            self.countdown -= 1

    def is_touching_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if abs(mouse_pos[0] - self.location[0]) < self.size and abs(mouse_pos[1] - self.location[1]) < self.size:
            return True
        else:
            return False

    def accuracy(self):
        mouse_pos = pygame.mouse.get_pos()
        distance = float((abs(mouse_pos[0] - self.location[0]) ** 2 + abs(mouse_pos[1] - self.location[1]) ** 2) ** 0.5)
        if distance < 0.25 * self.size:
            return 100
        elif distance < 0.5 * self.size:
            return 75
        elif distance < 0.75 * self.size:
            return 67
        else:
            return 50


class TargetPractice:
    def __init__(self):
        self.x, self.y = 750, 500
        self.screen = pygame.display.set_mode((self.x, self.y))
        pygame.display.set_caption("Target Practice")
        self.heading_font = pygame.font.Font(".\\fonts\\AstronBoyWonder.ttf", 48)
        self.regular_font = pygame.font.Font(".\\fonts\\basic_types\\Roboto-Medium.ttf", 24)
        self.targets = []
        self.buttons = {
            "Game": [
                Button(self.screen, (715, 30), 3, self.regular_font.render("Exit", False, WHITE), self.scene_switch)
            ],
            "Home": [
                Button(self.screen, (375, 250), 3, self.regular_font.render("Play", False, WHITE), self.scene_switch),
                Button(self.screen, (375, 300), 3, self.regular_font.render("Leave", False, WHITE), self.exit)
            ]
        }
        self.accuracy = 0
        self.hits = 0
        self.clicks = 0
        self.cooldown = 60 * 1
        self.scene = "Home"
        self.clock = pygame.time.Clock()

    def scene_switch(self):
        if self.scene == "Home":
            self.scene = "Game"
        else:
            self.scene = "Home"

    def exit(self): exit()

    def run_game(self):
        timer = 0
        self.instantiate_target()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for j in self.buttons[self.scene]:
                            if j.collision_check():
                                j.function()
                                continue
                        self.clicks += 1
                        for i in self.targets:
                            if i.is_touching_mouse():
                                self.calc_accuracy(i.accuracy())
                                self.targets.remove(i)
                                self.hits += 1

            self.screen.fill((110, 110, 110))

            if self.scene == "Game":
                if timer == self.cooldown:
                    timer = 0
                    self.instantiate_target()
                else:
                    timer += 1

                for i in self.targets:
                    i.run()
                    if i.size <= 0: self.targets.remove(i)
            for i in self.buttons[self.scene]:
                i.run()
            self.display_text(self.scene)
            pygame.display.update()
            self.clock.tick(60)

    def instantiate_target(self):
        size = randint(20, 50)
        location = (randint(size, self.x - size), randint(size, self.y - size))
        self.targets.append(Target(self.screen, location, size, 3))

    def calc_accuracy(self, score):
        self.accuracy = (self.accuracy * (self.clicks - 1) + score) // self.clicks
        if self.clicks > 10: self.clicks = 10

    def display_text(self, scene):
        if scene == "Home":
            heading_text = self.heading_font.render("Target Practice", False, WHITE)
            heading_text_rect = heading_text.get_rect()
            self.screen.blit(heading_text, (self.x / 2 - 140, 150), heading_text_rect)
        elif scene == "Game":
            score = self.regular_font.render("Score: {}".format(self.accuracy), False, WHITE)
            hits = self.regular_font.render("Hits: {}".format(self.hits), False, WHITE)
            score_rect = score.get_rect()
            hits_rect = hits.get_rect()
            self.screen.blit(score, score_rect)
            self.screen.blit(hits, hits_rect)


x = TargetPractice()
x.run_game()
