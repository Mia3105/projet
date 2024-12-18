import pygame
from random import randint
from sys import exit
from typing import List, Tuple

WINDOW_SIZE: Tuple[int, int] = (480, 360)
WINDOW_TITLE: str = "pygame window 11"
FPS = 12


class Actor:
    _position: pygame.Vector2
    _speed: pygame.Vector2
    _dimension: Tuple[int, int]

    def __init__(self, position: pygame.Vector2, speed: pygame.Vector2, dimension: Tuple[int, int]) -> None:
        self._position = position
        self._speed = speed
        self._dimension = dimension

    @property
    def position(self) -> pygame.Vector2:
        return self._position

    @position.setter
    def position(self, position: pygame.Vector2) -> None:
        if position.x < 0 or position.y < 0:
            raise ValueError("each position values must be zero or positive")
        self._position = position

    @property
    def speed(self) -> pygame.Vector2:
        return self._speed

    @speed.setter
    def speed(self, speed: pygame.Vector2) -> None:
        self._speed = speed

    @property
    def dimension(self) -> Tuple[int, int]:
        return self._dimension

    @dimension.setter
    def dimension(self, dimension: Tuple[int, int]) -> None:
        if dimension[0] <= 0 or dimension[1] <= 0:
            raise ValueError("each dimension value must be positive")
        self._dimension = dimension


class ActorSprite(pygame.sprite.Sprite):
    _actor: Actor
    _color: pygame.Color
    _image: pygame.Surface
    _rect: pygame.Rect

    def __init__(self, actor: Actor, color_name: str, *groups: List[pygame.sprite.Group]) -> None:
        pygame.sprite.Sprite.__init__(self, *groups)
        self._actor = actor
        self._set_color(color_name)
        self._set_image()
        self._set_rect()

    @property
    def color(self) -> pygame.Color:
        return self._color

    def _set_color(self, color_name: str) -> None:
        if color_name not in pygame.color.THECOLORS.keys():
            raise ValueError("color must be in list of pygame.Color")
        self._color = pygame.Color(color_name)

    @property
    def image(self) -> pygame.Surface:
        return self._image

    def _set_image(self) -> None:
        image: pygame.Surface = pygame.Surface(self._actor.dimension)
        image.fill(pygame.Color("black"))
        image.set_colorkey(pygame.Color("black"))
        image.set_alpha(255)
        pygame.draw.rect(image, self.color, ((0, 0), image.get_size()), 5)
        self._image = image

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    def _set_rect(self) -> None:
        rect = self.image.get_rect()
        rect.update(self._actor.position, self.image.get_size())
        self._rect = rect

    def update(self) -> None:
        pass


class ActorSpriteDrivenByMouse(ActorSprite):
    def __init__(self, actor: Actor, color_name: str, *groups: List[pygame.sprite.Group]) -> None:
        super().__init__(actor, color_name, *groups)

    def update(self):
        if pygame.mouse.get_focused():
        # https://stackoverflow.com/questions/60418322/check-if-mouse-is-outside-pygame-window
            self._rect.topleft = pygame.mouse.get_pos()
            # Update actor position to follow the mouse move
            self._rect.move_ip(self._actor.speed)
            self._rect.move_ip(1, 1)
            self._actor.position = pygame.Vector2(self.rect.topleft)


class ActorSpriteDrivenByRandom(ActorSprite):
    def __init__(self, actor: Actor, color_name: str, *groups: List[pygame.sprite.Group]) -> None:
        super().__init__(actor, color_name, *groups)

    def update(self):
        random_speed: pygame.Vector2 = pygame.Vector2(randint(-1, 1), randint(-1, 1))
        self._rect.move_ip(random_speed)
        self._actor.position = pygame.Vector2(self.rect.topleft)


class ActorSpriteDrivenBySpeed(ActorSprite):
    def __init__(self, actor: Actor, color_name: str, *groups: List[pygame.sprite.Group]) -> None:
        super().__init__(actor, color_name, *groups)

    def update(self):
        self.rect.move_ip(self._actor.speed)
        self._actor.position = pygame.Vector2(self.rect.topleft)


class App:
    __window_size: Tuple[int, int] = WINDOW_SIZE
    __window_title: str = WINDOW_TITLE
    __screen: pygame.Surface = None
    __running: bool = False
    __clock: pygame.time.Clock = pygame.time.Clock()
    __FPS: int = FPS

    __player_sprite: pygame.sprite.Group
    __actors_sprites: pygame.sprite.Group

    def __init__(self) -> None:
        pygame.init()
        self.__init_screen()
        self.__init_actors()
        self.__running = True

    def __init_screen(self) -> None:
        self.__screen = pygame.display.set_mode(self.__window_size)
        pygame.display.set_caption(self.__window_title)

    def __handle_events(self, event) -> None:
        if event.type == pygame.QUIT:
            self.__running = False
            pygame.quit()
            exit()

    def __init_actors(self) -> None:
        player: Actor = Actor(pygame.Vector2(0, 0), pygame.Vector2(1, 1), (60, 60))
        random_speed: pygame.Vector2 = pygame.Vector2(randint(-1, 1), randint(-1, 1))
        actor_00: Actor = Actor(pygame.Vector2(randint(0, 420), randint(0, 320)), random_speed, (40, 40))
        actor_01: Actor = Actor(pygame.Vector2(210, 160), pygame.Vector2(0, 0), (60, 40))
        actor_02 : Actor = Actor(pygame.Vector2(110, 90), pygame.Vector2(2, 2), (10, 150))
        self.__player_sprite = pygame.sprite.Group()
        ActorSpriteDrivenByMouse(player, "white", [self.__player_sprite])
        self.__actors_sprites = pygame.sprite.Group()
        ActorSpriteDrivenBySpeed(actor_00, "blue", [self.__actors_sprites])
        ActorSpriteDrivenByRandom(actor_01, "red", [self.__actors_sprites])
        ActorSpriteDrivenByRandom(actor_02, "cyan", [self.__actors_sprites])

    def __update_actors(self) -> None:
        self.__player_sprite.update()
        self.__actors_sprites.update()

    def __draw_screen(self) -> None:
        self.__screen.fill(pygame.color.THECOLORS["black"])

    def __draw_actors(self) -> None:
        self.__player_sprite.draw(self.__screen)
        self.__actors_sprites.draw(self.__screen)

    def execute(self) -> None:
        while self.__running:
            self.__clock.tick(self.__FPS)
            for event in pygame.event.get():
                self.__handle_events(event)
            self.__update_actors()
            self.__draw_screen()
            self.__draw_actors()
            pygame.display.flip()