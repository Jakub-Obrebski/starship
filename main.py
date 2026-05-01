import pygame

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption(("Dziady cz. III"))
tile = pygame.image.load("assets/dirt.png").convert_alpha()
tile = pygame.transform.scale(tile, (64, 64))
clock = pygame.time.Clock()
running = True

while running:
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			running = False
		elif e.type == pygame.KEYDOWN:
			print(f"Key {pygame.key.name(e.key)} pressed")
			if e.key == pygame.K_ESCAPE:
				print("Hotkey Exit!")
				running = False
		elif e.type == pygame.KEYUP:
			print(f"Key {pygame.key.name(e.key)} released")
	
	screen.fill((179, 206, 229))
	screen.blit(tile, (0, 0))
	pygame.display.flip()
	clock.tick(60)

pygame.quit()