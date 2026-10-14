"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 400, 600
BOARD_SIZE = 360
CELL_SIZE = BOARD_SIZE // 3
BOARD_TOP = 100
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (245, 245, 245)
COLOR_LINE = (60, 60, 60)
COLOR_X = (200, 60, 60)
COLOR_O = (60, 100, 200)
COLOR_TEXT = (30, 30, 30)


def board_pos_to_cell(pos):
    x, y = pos
    y -= BOARD_TOP
    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        return None
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    return int(row), int(col)


def draw_board(surface, board):
    surface.fill(COLOR_BG)
    for i in range(1, 3):
        pygame.draw.line(surface, COLOR_LINE, (i * CELL_SIZE, BOARD_TOP), (i * CELL_SIZE, BOARD_TOP + BOARD_SIZE), 3)
        pygame.draw.line(surface, COLOR_LINE, (0, BOARD_TOP + i * CELL_SIZE), (BOARD_SIZE, BOARD_TOP + i * CELL_SIZE), 3)

    for r in range(3):
        for c in range(3):
            symbol = board[r][c]
            if symbol is None:
                continue
            center = (c * CELL_SIZE + CELL_SIZE // 2, BOARD_TOP + r * CELL_SIZE + CELL_SIZE // 2)
            if symbol == 'X':
                offset = CELL_SIZE // 3
                pygame.draw.line(surface, COLOR_X, (center[0]-offset, center[1]-offset), (center[0]+offset, center[1]+offset), 6)
                pygame.draw.line(surface, COLOR_X, (center[0]+offset, center[1]-offset), (center[0]-offset, center[1]+offset), 6)
            else:
                pygame.draw.circle(surface, COLOR_O, center, CELL_SIZE // 3, 6)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (180, 40, 40))
    rect = surf.get_rect(center=(surface.get_width() // 2, BOARD_TOP + BOARD_SIZE + 40))
    surface.blit(surf, rect)


# --- on-screen controls (Task 4) ---
BUTTON_Y = 530
BUTTON_H = 44
BUTTONS = {
    'first': pygame.Rect(10, BUTTON_Y, 120, BUTTON_H),
    'new_round': pygame.Rect(140, BUTTON_Y, 120, BUTTON_H),
    'reset_match': pygame.Rect(270, BUTTON_Y, 120, BUTTON_H),
}


def button_at(pos):
    for name, rect in BUTTONS.items():
        if rect.collidepoint(pos):
            return name
    return None


def draw_buttons(surface, font, first_player):
    small = pygame.font.SysFont("consolas", 15)
    labels = {
        'first': f"{first_player} starts",
        'new_round': "New round",
        'reset_match': "Reset match",
    }
    for name, rect in BUTTONS.items():
        pygame.draw.rect(surface, (225, 225, 225), rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_LINE, rect, 2, border_radius=6)
        surf = small.render(labels[name], True, COLOR_TEXT)
        surface.blit(surf, surf.get_rect(center=rect.center))
    hint = small.render("Keys: F first player | R round | M match", True, (110, 110, 110))
    surface.blit(hint, (10, BUTTON_Y + BUTTON_H + 10))
