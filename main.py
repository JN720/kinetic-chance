import pygame, sys
import pygame.locals
import game

pygame.init()
DISPLAY = pygame.display.set_mode((800, 450), flags = pygame.SCALED)
pygame.display.set_caption('Kinetic Chance')

players = []
spells = []

pause = False
running = True
game_running = False

def collision(player, spell):
  if ((spell.x > player.x and spell.x < player.x + game.PS * 2) or (spell.x + spell.dx > player.x and spell.x + spell.dx < player.x + game.PS * 2)) and ((spell.y > player.y and spell.y < player.y + game.PS * 2) or (spell.y + spell.dy > player.y and spell.y + spell.dy < player.y + game.PS * 2)):
    return True
  if ((player.x > spell.x and player.x < spell.x + spell.dx) or (player.x + player.x + game.PS * 2 > spell.x and player.x + player.x + game.PS * 2 < spell.x + spell.dx)) and ((player.y > spell.y and player.y < spell.y + spell.dy) or (player.y + game.PS * 2 > spell.y and player.y + game.PS * 2 < spell.y + spell.dy)):
    return True
  return False

font = pygame.font.SysFont('dejavusans', 30)
sfont = pygame.font.SysFont('dejavusans', 20)

p1moves = list(game.MOVES.keys())

p2moves = list(game.MOVES.keys())

while running:
  DISPLAY.fill((40, 40, 40))

  for event in pygame.event.get():
    if event.type == pygame.locals.QUIT:
      running = False
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_s and not game_running:
      game_running = True
      players = [game.Player(200, 4, p1moves, (0, 0, 255), 0, 80, 280),
          game.Player(200, 4, p2moves, (255, 0, 0), 1, 720, 280)]
      spells = []
    if pause and event.type == pygame.KEYDOWN and event.key == pygame.K_p and game_running:
      pause = False
    elif not pause and event.type == pygame.KEYDOWN and event.key == pygame.K_p and game_running:
      pause = True
      
  if game_running:
    #text display
    DISPLAY.blit(font.render(players[0].moveset[players[0].selmove] + ' ' + str(int(players[0].lit)), True, (255, 255, 255)), (30, 30))
    DISPLAY.blit(font.render(str(int(players[1].lit)) + ' ' + players[1].moveset[players[1].selmove], True, (255, 255, 255)), (600, 30))
    DISPLAY.blit(sfont.render(players[0].moveset[0] if players[0].selmove == len(players[0].moveset) - 1 else players[0].moveset[players[0].selmove + 1], True, (150, 150, 150)), (150, 80))
    DISPLAY.blit(sfont.render(players[0].moveset[-1] if players[0].selmove == 0 else players[0].moveset[players[0].selmove - 1], True, (150, 150, 150)), (10, 80))
    DISPLAY.blit(sfont.render(players[1].moveset[0] if players[1].selmove == len(players[1].moveset) - 1 else players[1].moveset[players[1].selmove + 1], True, (150, 150, 150)), (670, 80))
    DISPLAY.blit(sfont.render(players[1].moveset[-1] if players[1].selmove == 0 else players[1].moveset[players[1].selmove - 1], True, (150, 150, 150)), (500, 80))

    if pause:
      DISPLAY.blit(font.render('Press P to Unpause', True, (255, 255, 255)), (350, 150))
      for i in range(len(players)):
        if not players[i].alive:
          continue
        else:
          players[i].render(DISPLAY)
      for j in range(len(spells)):
        spells[j].render(DISPLAY)
    else:
      alive = 0
      for i in range(len(players)):
        if not players[i].alive:
          continue
        alive += 1
        players[i].tick()
        newspell = players[i].autocast()
        if newspell != None:
          spells.append(newspell)
          spells[-1].owner = i
        players[i].render(DISPLAY)
        keys = pygame.key.get_pressed()
        for k in range(len(keys)):
          if keys[k] and pygame.key.name(k) in players[i].controls and players[i].stun == 0:
            newspell = players[i].control(pygame.key.name(k))
            if newspell != None:
              spells.append(newspell)
              spells[-1].owner = i
        for j in range(len(spells)):
            if spells[j] == -1:
                continue
            if i != spells[j].owner:
                if collision(players[i], spells[j]):
                    players[i].trigger(spells[j])
                    spells[j] = -1
            elif spells[j].movetype == 1:
                spells[j].init(players[i].dir, players[i].x, players[i].y)
      for i in range(len(spells)):
        if spells[i] == -1:
          continue
        spells[i].render(DISPLAY)
        if spells[i].tick():
          spells[i] = -1
      while -1 in spells:
        spells.remove(-1)
      if alive == 1:
        game_running = False
  else:
    DISPLAY.blit(font.render('Press S to Start', True, (255, 255, 255)), (300, 200))
  pygame.display.update()
  pygame.time.Clock().tick(60)
