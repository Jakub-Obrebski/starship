import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption(("Dziady cz. III"))
tile = pygame.image.load("assets/dirt.png").convert_alpha()
tile = pygame.transform.scale(tile, (64, 64))
clock = pygame.time.Clock()
running = True

while running:
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			running = False
	
	screen.fill((179, 206, 229))
	screen.blit(tile, (0, 0))
	pygame.display.flip()
	clock.tick(60)

pygame.quit()