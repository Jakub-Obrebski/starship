import pygame
import sys
import math
import random

pygame.init()

WIDTH, HEIGHT = 960, 640
TILE = 32
FPS = 60

C_BG        = (15,  12,  30)
C_GROUND    = (38,  32,  60)
C_GROUND2   = (50,  42,  75)
C_STONE     = (90,  80, 120)
C_STONE2    = (110, 98, 140)
C_RUIN      = (70,  60,  95)
C_RUIN2     = (85,  73, 110)
C_SAND      = (180, 155, 110)
C_SAND2     = (200, 175, 130)
C_STAR_DIM  = (180, 160, 220)
C_STAR_BRT  = (240, 220, 255)
C_GLOW      = (130, 100, 200)
C_ARTIFACT  = (255, 210,  80)
C_ARTIFACT2 = (255, 170,  40)
C_PLAYER    = (220, 180, 255)
C_PLAYER2   = (180, 130, 230)
C_UI_BG     = (20,  16,  38, 210)
C_UI_BORDER = (130, 100, 200)
C_WHITE     = (255, 255, 255)
C_CREAM     = (240, 230, 210)
C_PINK      = (255, 180, 200)
C_TEAL      = (100, 220, 200)
C_ORANGE    = (255, 160,  80)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("✦ STARSHIP ✦  Archaeologist on Kepler-7b")
clock = pygame.time.Clock()

font_big   = pygame.font.SysFont("notosans", 28, bold=True)
font_med   = pygame.font.SysFont("notosans", 18)
font_small = pygame.font.SysFont("notosans", 14)
font_tiny  = pygame.font.SysFont("notosans", 11)

RAW_MAP = [
	"1111111111111111111111111111111111",
	"1000000000000000100000000001000001",
	"1002000030000002000000300000000001",
	"1000002000000000000000000002000001",
	"1030000000222200000300000000030001",
	"1000000002000200003000000000000001",
	"1000300002000200000000400000000001",
	"1000000002222200030000000000003001",
	"1000000000000000000000000020000001",
	"1033000000003000000040000000000001",
	"1000000000000000000000000000000001",
	"1000020000000000300000000000030001",
	"1000000000400000000000030000000001",
	"1000300000000000000020000000000001",
	"1022200000003000000000000400000001",
	"1000000000000000000000000000003001",
	"1000040000000030000000000000000001",
	"1000000000000000000000020000000001",
	"1111111111111111111111111111111111",
]

MAP_ROWS = len(RAW_MAP)
MAP_COLS = len(RAW_MAP[0])
MAP_W = MAP_COLS * TILE
MAP_H = MAP_ROWS * TILE

tile_map = []
artifact_positions = []
for r, row in enumerate(RAW_MAP):
	tile_row = []
	for c, ch in enumerate(row):
		tile_row.append(int(ch))
		if ch == '4':
			artifact_positions.append([c, r])
	tile_map.append(tile_row)

stars = [(random.randint(0, MAP_W), random.randint(0, MAP_H),
		  random.choice([1, 1, 1, 2]),
		  random.uniform(0.3, 1.0)) for _ in range(220)]

ARTIFACT_DATA = [
	{
		"name": "Kryształowy Zapis",
		"icon": "💎",
		"desc": [
			"Półprzezroczysty kryształ pokryty",
			"nieznanym pismem. Wibruje lekko",
			"w twoich rękach jakby chciał coś",
			"powiedzieć...",
			"",
			"[ Zapis #1 z 6 odnaleziony ]"
		],
		"lore": "Nieznana cywilizacja istniała tu 4000 lat temu."
	},
	{
		"name": "Mapa Gwiezdna",
		"icon": "🗺",
		"desc": [
			"Metalowa płyta z wyrytą mapą",
			"układu gwiezdnego. Jedno słońce",
			"jest zakreślone — Twoje słońce.",
			"Znali Ziemię.",
			"",
			"[ Zapis #2 z 6 odnaleziony ]"
		],
		"lore": "Znali drogę do Ziemi zanim my znaleźliśmy kosmos."
	},
	{
		"name": "Figurka Strażnika",
		"icon": "🗿",
		"desc": [
			"Mała figurka humanoidalnej",
			"istoty z czterema oczami.",
			"Na podstawie napis:",
			"»Ci co zostają, strzegą«",
			"",
			"[ Zapis #3 z 6 odnaleziony ]"
		],
		"lore": "Może nadal tu są. Tylko czekają."
	},
	{
		"name": "Nasienie Rośliny",
		"icon": "🌱",
		"desc": [
			"Idealnie zachowane nasienie",
			"rośliny której nie ma już na",
			"tej planecie. W środku — ciepło.",
			"Wciąż żywe.",
			"",
			"[ Zapis #4 z 6 odnaleziony ]"
		],
		"lore": "Życie szuka drogi nawet przez tysiąclecia."
	},
	{
		"name": "Dziennik Podróżnika",
		"icon": "📖",
		"desc": [
			"Ostatnia strona dziennika.",
			"»Opuszczamy planetę. Niech",
			"ten kto to czyta wie:  byliśmy",
			"tu, kochaliśmy tu, żyliśmy.«",
			"",
			"[ Zapis #5 z 6 odnaleziony ]"
		],
		"lore": "Odeszli dobrowolnie. Ale dokąd?"
	},
	{
		"name": "Kula Pamięci",
		"icon": "🔮",
		"desc": [
			"Dotykasz kuli i widzisz:",
			"miasto, śmiech, dzieci bawiące",
			"się pod fioletowym niebem.",
			"Ta planeta żyła. Naprawdę żyła.",
			"",
			"[ Zapis #6 z 6 - KOMPLETNY! ]"
		],
		"lore": "KONIEC: Przekazujesz znaleziska na Ziemię. Ich historia żyje dalej."
	},
]

player = pygame.Rect(3 * TILE, 2 * TILE, 22, 22)
player_speed = 3
camera_x, camera_y = 0, 0
collected = []
active_dialog = None
dialog_timer = 0
show_intro = True
intro_alpha = 255
game_won = False
tick = 0

def draw_pixel_char(surf, x, y, facing, t):
	bob = math.sin(t * 0.08) * 1.5
	y += bob
	pygame.draw.rect(surf, C_PLAYER2, (x-4, y-2, 8, 10))
	pygame.draw.rect(surf, C_PLAYER,  (x-3, y-1, 6,  8))
	pygame.draw.rect(surf, C_CREAM,   (x-4, y-11,9, 9))
	ex = x-2 if facing >= 0 else x-1
	pygame.draw.rect(surf, C_BG, (ex, y-8, 2, 2))
	pygame.draw.rect(surf, C_BG, (ex+3, y-8, 2, 2))
	pygame.draw.rect(surf, C_ORANGE,  (x-5, y-12,11, 4))
	pygame.draw.rect(surf, C_TEAL,    (x-2, y-13, 6, 3))
	leg = int(math.sin(t * 0.15) * 3) if True else 0
	pygame.draw.rect(surf, C_PLAYER2, (x-4, y+7, 3, 5+leg))
	pygame.draw.rect(surf, C_PLAYER2, (x+1, y+7, 3, 5-leg))

def tile_color(t, r, c):
	checker = (r + c) % 2
	if t == 0:  return C_GROUND  if checker else C_GROUND2
	if t == 1:  return C_STONE   if checker else C_STONE2
	if t == 2:  return C_RUIN    if checker else C_RUIN2
	if t == 3:  return C_SAND    if checker else C_SAND2
	if t == 4:  return C_GROUND  if checker else C_GROUND2
	return C_GROUND

def is_solid(col, row):
	if row < 0 or row >= MAP_ROWS or col < 0 or col >= MAP_COLS:
		return True
	return tile_map[row][col] == 1

def move_player(dx, dy):
	global player
	new = player.move(dx, 0)
	cols = [new.left // TILE, new.right // TILE]
	rows = [new.top  // TILE, new.bottom // TILE]
	if not any(is_solid(c, r) for c in cols for r in rows):
		player = new
	new = player.move(0, dy)
	cols = [new.left // TILE, new.right // TILE]
	rows = [new.top  // TILE, new.bottom // TILE]
	if not any(is_solid(c, r) for c in cols for r in rows):
		player = new

def draw_text_box(surf, lines, x, y, w, padding=10):
	lh = font_small.get_linesize()
	h  = len(lines) * lh + padding * 2
	box = pygame.Surface((w, h), pygame.SRCALPHA)
	box.fill((20, 16, 38, 220))
	pygame.draw.rect(box, C_UI_BORDER, (0, 0, w, h), 2)
	surf.blit(box, (x, y))
	for i, line in enumerate(lines):
		col = C_ARTIFACT if line.startswith("[") else C_CREAM
		surf.blit(font_small.render(line, True, col), (x+padding, y+padding+i*lh))
	return h

def draw_hud(surf):
	hud = pygame.Surface((WIDTH, 36), pygame.SRCALPHA)
	hud.fill((20, 16, 38, 200))
	surf.blit(hud, (0, 0))
	t = font_med.render("✦ STARSHIP ✦", True, C_STAR_BRT)
	surf.blit(t, (WIDTH//2 - t.get_width()//2, 8))
	a = font_small.render(f"artefakty: {len(collected)}/{len(artifact_positions)}", True, C_ARTIFACT)
	surf.blit(a, (12, 10))
	ctrl = font_tiny.render("WSAD / strzałki - ruch    SPACJA - zbierz    ESC - wyjście", True, C_STAR_DIM)
	surf.blit(ctrl, (WIDTH - ctrl.get_width() - 10, 22))

def draw_glow(surf, x, y, r, color, alpha=60):
	gsurf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
	pygame.draw.circle(gsurf, (*color, alpha), (r, r), r)
	surf.blit(gsurf, (x - r, y - r), special_flags=pygame.BLEND_ALPHA_SDL2)

def draw_intro(surf, alpha):
	overlay = pygame.Surface((WIDTH, HEIGHT))
	overlay.fill(C_BG)
	overlay.set_alpha(alpha)
	surf.blit(overlay, (0, 0))
	if alpha < 200:
		return
	lines = [
		("✦ STARSHIP ✦", font_big, C_STAR_BRT),
		("Archaeologist on Kepler-7b", font_med, C_CREAM),
		("", None, None),
		("Rok 2387. Twój statek ląduje na opuszczonej planecie.", font_small, C_STAR_DIM),
		("Skanery wykryły ślady dawnej cywilizacji.", font_small, C_STAR_DIM),
		("Twoją misją jest odnalezienie 6 artefaktów", font_small, C_STAR_DIM),
		("i poznanie historii tych, którzy tu żyli.", font_small, C_STAR_DIM),
		("", None, None),
		("[ naciśnij dowolny klawisz aby zacząć ]", font_small, C_ARTIFACT),
	]
	total_h = sum(l[1].get_linesize() if l[1] else 12 for l in lines)
	y = HEIGHT // 2 - total_h // 2
	for text, font, color in lines:
		if font is None:
			y += 12
			continue
		r = font.render(text, True, color)
		surf.blit(r, (WIDTH // 2 - r.get_width() // 2, y))
		y += font.get_linesize() + 2

def draw_win(surf):
	overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
	overlay.fill((10, 8, 20, 210))
	surf.blit(overlay, (0, 0))
	lines = [
		("✦ MISJA UKOŃCZONA ✦", font_big,   C_ARTIFACT),
		("", None, None),
		("Zebrałaś wszystkie 6 artefaktów.", font_med,   C_CREAM),
		("Historia cywilizacji Kepler-7b", font_small, C_STAR_DIM),
		("zostanie przekazana na Ziemię.", font_small, C_STAR_DIM),
		("", None, None),
		("Ich pamięć żyje dzięki Tobie. 🌸", font_med,   C_PINK),
		("", None, None),
		("[ ESC aby wyjść ]", font_small, C_STAR_DIM),
	]
	y = HEIGHT // 2 - 100
	for text, font, color in lines:
		if font is None:
			y += 14
			continue
		r = font.render(text, True, color)
		surf.blit(r, (WIDTH // 2 - r.get_width() // 2, y))
		y += font.get_linesize() + 4

facing = 1

while True:
	dt = clock.tick(FPS)
	tick += 1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit(); sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit(); sys.exit()
			if show_intro:
				show_intro = False
				intro_alpha = 0
				continue
			if active_dialog is not None:
				active_dialog = None
				dialog_timer  = 0
				continue
			if event.key == pygame.K_SPACE and not game_won:
				px, py = player.centerx // TILE, player.centery // TILE
				for i, (ac, ar) in enumerate(artifact_positions):
					if i in collected:
						continue
					if abs(ac - px) <= 1 and abs(ar - py) <= 1:
						collected.append(i)
						tile_map[ar][ac] = 0
						idx = min(i, len(ARTIFACT_DATA) - 1)
						active_dialog = idx
						if len(collected) == len(artifact_positions):
							game_won = True
						break

	if not show_intro and active_dialog is None and not game_won:
		keys = pygame.key.get_pressed()
		dx = dy = 0
		if keys[pygame.K_LEFT]  or keys[pygame.K_a]: dx -= player_speed; facing = -1
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += player_speed; facing =  1
		if keys[pygame.K_UP]    or keys[pygame.K_w]: dy -= player_speed
		if keys[pygame.K_DOWN]  or keys[pygame.K_s]: dy += player_speed
		if dx and dy:
			dx = int(dx * 0.707)
			dy = int(dy * 0.707)
		move_player(dx, dy)

	target_cx = player.centerx - WIDTH  // 2
	target_cy = player.centery - HEIGHT // 2
	target_cx = max(0, min(target_cx, MAP_W - WIDTH))
	target_cy = max(0, min(target_cy, MAP_H - HEIGHT))
	camera_x += (target_cx - camera_x) * 0.12
	camera_y += (target_cy - camera_y) * 0.12
	cx, cy = int(camera_x), int(camera_y)

	screen.fill(C_BG)

	star_pulse = math.sin(tick * 0.02)
	for sx, sy, sr, sb in stars:
		brt = int(sb * (200 + 55 * star_pulse))
		col = (min(255, brt + 20), min(255, brt), min(255, brt + 40))
		pygame.draw.circle(screen, col, (sx - cx, sy - cy), sr)

	start_c = max(0, cx // TILE)
	end_c   = min(MAP_COLS, start_c + WIDTH  // TILE + 2)
	start_r = max(0, cy // TILE)
	end_r   = min(MAP_ROWS, start_r + HEIGHT // TILE + 2)

	for r in range(start_r, end_r):
		for c in range(start_c, end_c):
			t = tile_map[r][c]
			color = tile_color(t, r, c)
			rx = c * TILE - cx
			ry = r * TILE - cy
			pygame.draw.rect(screen, color, (rx, ry, TILE, TILE))
			if t == 2:
				pygame.draw.rect(screen, C_RUIN2, (rx+2, ry+2, TILE-4, 3))
				pygame.draw.rect(screen, C_RUIN2, (rx+2, ry+TILE-5, TILE-4, 3))

	for i, (ac, ar) in enumerate(artifact_positions):
		if i in collected:
			continue
		ax = ac * TILE + TILE // 2 - cx
		ay = ar * TILE + TILE // 2 - cy
		glow_r = 20 + int(5 * math.sin(tick * 0.05 + i))
		draw_glow(screen, ax, ay, glow_r, C_ARTIFACT, 80)
		size = 7 + int(2 * math.sin(tick * 0.07 + i * 1.3))
		pygame.draw.polygon(screen, C_ARTIFACT2, [
			(ax,       ay - size),
			(ax + size, ay),
			(ax,       ay + size),
			(ax - size, ay),
		])
		pygame.draw.polygon(screen, C_ARTIFACT, [
			(ax,         ay - size + 2),
			(ax + size - 2, ay),
			(ax,         ay + size - 2),
			(ax - size + 2, ay),
		])
		near_px = abs((ac * TILE + TILE//2) - player.centerx) < 3 * TILE
		near_py = abs((ar * TILE + TILE//2) - player.centery) < 3 * TILE
		if near_px and near_py:
			label = font_tiny.render("[ SPACJA ]", True, C_ARTIFACT)
			screen.blit(label, (ax - label.get_width()//2, ay - size - 16))

	draw_pixel_char(screen,
			player.centerx - cx,
			player.centery - cy,
			facing, tick)

	draw_hud(screen)

	if active_dialog is not None:
		d = ARTIFACT_DATA[active_dialog]
		box_w = 380
		lines = [f"✦ {d['name']} ✦", ""] + d["desc"] + ["", "[ naciśnij dowolny klawisz ]"]
		draw_text_box(screen, lines,
				WIDTH // 2 - box_w // 2,
				HEIGHT - 220,
				box_w)

	if show_intro:
		draw_intro(screen, intro_alpha)
	elif intro_alpha > 0:
		draw_intro(screen, intro_alpha)
		intro_alpha = max(0, intro_alpha - 12)

	if game_won and active_dialog is None:
		draw_win(screen)

	pygame.display.flip()