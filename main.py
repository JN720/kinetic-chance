import pygame, sys
import pygame.locals
import game
from random import randint

pygame.init()
DISPLAY = pygame.display.set_mode((800, 450), flags = pygame.SCALED)
pygame.display.set_caption('Kinetic Chance')

players = []
spells = []

colors = [
  (0, 0, 0), #black
  (120, 40, 20), #dark brown
  (180, 180, 180), #grey
  (100, 100, 155),  #light blue
  (155, 100, 100), #light red
  (255, 100, 0) #elusive orange
  ]

map_names = ['The Void', 'Classic', 'Divided']
backgrounds = [(40, 40, 40), (30, 30, 0), (110, 110, 110)]
#one list per map
#each list contains lists of length 6 with terrain attributes
#x, y, xsize, ysize, color id, antipermeability
terrains = [
  [],
  [
    [0, 0, 100, 450, 3, 0],
    [700, 0, 100, 450, 4, 0],
    [300, 0, 200, 100, 0, 3],
    [300, 350, 200, 100, 0, 3],
    [180, 100, 50, 250, 1, 2],
    [570, 100, 50, 250, 1, 2],
  ],
  [
    [0, 0, 800, 40, 0, 3],
    [0, 410, 800, 40, 0, 3],
    [0, 40, 100, 100, 0, 3],
    [0, 310, 100, 100, 0, 3],
    [700, 40, 100, 100, 0, 3],
    [700, 310, 100, 100, 0, 3],
    [200, 125, 400, 15, 2, 2],
    [200, 310, 400, 15, 2, 2],
    [100, 125, 100, 15, 5, 1],
    [100, 310, 100, 15, 5, 1],
    [600, 125, 100, 15, 5, 1],
    [600, 310, 100, 15, 5, 1]
  ]
]
map = 0

mode = 0
mode_names = ['Classic', 'Freeplay', 'Random', 'Draft']
mode_descriptions = [
  'A simple mode with 4 moves and standard stats',
  'A high-stat mode where every move is accessible',
  'A mode with randomized moves',
  'A competitive mode where moves are drafted'
]

pause = False
running = True
game_running = False
drafting = False
winner = -1

def collision(player, spell):
  if ((spell.x > player.x and spell.x < player.x + game.PS * 2) or (spell.x + spell.dx > player.x and spell.x + spell.dx < player.x + game.PS * 2)) and ((spell.y > player.y and spell.y < player.y + game.PS * 2) or (spell.y + spell.dy > player.y and spell.y + spell.dy < player.y + game.PS * 2)):
    return True
  if ((player.x > spell.x and player.x < spell.x + spell.dx) or (player.x + game.PS * 2 > spell.x and player.x + game.PS * 2 < spell.x + spell.dx)) and ((player.y > spell.y and player.y < spell.y + spell.dy) or (player.y + game.PS * 2 > spell.y and player.y + game.PS * 2 < spell.y + spell.dy)):
    return True
  return False

def render_terrain():
  for rect in terrains[map]:
    pygame.draw.rect(DISPLAY, colors[rect[4]], pygame.Rect(*rect[0:4]))

def terrain_collision(r):
  x = r.x + r.mx
  y = r.y + r.my
  for t in terrains[map]:
    #check if projectile/player can phase through
    if r.perm >= t[5]:
      continue
    #rectangle collision
    if ((x > t[0] and x < t[0] + t[2]) or (x + r.dx > t[0] and x + r.dx < t[0] + t[2])) and ((y > t[1] and y < t[1] + t[3]) or (y + r.dy > t[1] and y + r.dy < t[1] + t[3])):
      return True
    if ((t[0] > x and t[0] < x + r.dx) or (t[0] + t[2] > x and t[0] + t[2] < x + r.dx)) and ((t[1] > r.y and t[1] < y + r.dy) or (t[1] + t[3] > y and t[1] + t[3] < y + r.dy)):
      return True
  return False

def terrain_collision_x(r):
  x = r.x + r.mx
  y = r.y
  for t in terrains[map]:
    #check if projectile/player can phase through
    if r.perm >= t[5]:
      continue
    #rectangle collision
    if ((x > t[0] and x < t[0] + t[2]) or (x + r.dx > t[0] and x + r.dx < t[0] + t[2])) and ((y > t[1] and y < t[1] + t[3]) or (y + r.dy > t[1] and y + r.dy < t[1] + t[3])):
      return True
    if ((t[0] > x and t[0] < x + r.dx) or (t[0] + t[2] > x and t[0] + t[2] < x + r.dx)) and ((t[1] > r.y and t[1] < y + r.dy) or (t[1] + t[3] > y and t[1] + t[3] < y + r.dy)):
      return True
  return False

def terrain_collision_y(r):
  x = r.x
  y = r.y + r.my
  for t in terrains[map]:
    #check if projectile/player can phase through
    if r.perm >= t[5]:
      continue
    #rectangle collision
    if ((x > t[0] and x < t[0] + t[2]) or (x + r.dx > t[0] and x + r.dx < t[0] + t[2])) and ((y > t[1] and y < t[1] + t[3]) or (y + r.dy > t[1] and y + r.dy < t[1] + t[3])):
      return True
    if ((t[0] > x and t[0] < x + r.dx) or (t[0] + t[2] > x and t[0] + t[2] < x + r.dx)) and ((t[1] > r.y and t[1] < y + r.dy) or (t[1] + t[3] > y and t[1] + t[3] < y + r.dy)):
      return True
  return False

font = pygame.font.SysFont('dejavusans', 30)
sfont = pygame.font.SysFont('dejavusans', 20)

p1moves = list(game.MOVES.keys())
p2moves = list(game.MOVES.keys())

while running:
  DISPLAY.fill(backgrounds[map])
  render_terrain()
  for event in pygame.event.get():
    if event.type == pygame.locals.QUIT:
      running = False
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN and event.key == pygame.K_g and not game_running:
      #classic
      if mode == 0:
        p1moves = ['sword', 'heal', 'fireball', 'superstrike']
        p2moves = ['sword', 'heal', 'fireball', 'superstrike']
        players = [
          game.Player(200, 3, p1moves, (0, 0, 255), 0, 80, 205),
          game.Player(200, 3, p2moves, (255, 0, 0), 1, 720, 205)]
      #frenzy
      elif mode == 1:
        p1moves = list(game.MOVES.keys())
        p2moves = list(game.MOVES.keys())
        players = [
          game.Player(500, 4, p1moves, (0, 0, 255), 0, 80, 205, mr = 0.6),
          game.Player(500, 4, p2moves, (255, 0, 0), 1, 720, 205, mr = 0.6)]
      #random
      elif mode == 2:
        moves = list(game.MOVES.keys())
        p1moves = []
        p2moves = []
        for i in range(6):
          p1moves.append(moves[randint(0, len(moves) - 1)])
          p2moves.append(moves[randint(0, len(moves) - 1)])
          players = [
            game.Player(300, 3, p1moves, (0, 0, 255), 0, 80, 205),
            game.Player(300, 3, p2moves, (255, 0, 0), 1, 720, 205)
          ]
      game_running = True
      spells = []
      
        
    if pause and event.type == pygame.KEYDOWN and event.key == pygame.K_p and game_running:
      pause = False
    elif not pause and event.type == pygame.KEYDOWN and event.key == pygame.K_p and game_running:
      pause = True
    #arrow keys for map selection
    if not game_running and event.type == pygame.KEYDOWN and event.key == pygame.K_a and map > 0:
      map -= 1
    elif not game_running and event.type == pygame.KEYDOWN and event.key == pygame.K_d and map < len(map_names) - 1:
      map += 1
    if not game_running and event.type == pygame.KEYDOWN and event.key == pygame.K_w and mode > 0:
      mode -= 1
    elif not game_running and event.type == pygame.KEYDOWN and event.key == pygame.K_s and mode < len(mode_names) - 1:
      mode += 1
      
  if game_running:
    #text display
    DISPLAY.blit(font.render(players[0].moveset[players[0].selmove] + ' ' + str(int(players[0].lit)), True, (255, 255, 255)), (30, 30))
    DISPLAY.blit(font.render(str(int(players[1].lit)) + ' ' + players[1].moveset[players[1].selmove], True, (255, 255, 255)), (600, 30))
    DISPLAY.blit(sfont.render(players[0].moveset[0] if players[0].selmove == len(players[0].moveset) - 1 else players[0].moveset[players[0].selmove + 1], True, (150, 150, 150)), (150, 80))
    DISPLAY.blit(sfont.render(players[0].moveset[-1] if players[0].selmove == 0 else players[0].moveset[players[0].selmove - 1], True, (150, 150, 150)), (10, 80))
    DISPLAY.blit(sfont.render(players[1].moveset[0] if players[1].selmove == len(players[1].moveset) - 1 else players[1].moveset[players[1].selmove + 1], True, (150, 150, 150)), (670, 80))
    DISPLAY.blit(sfont.render(players[1].moveset[-1] if players[1].selmove == 0 else players[1].moveset[players[1].selmove - 1], True, (150, 150, 150)), (500, 80))

    if pause:
      #display unpause and render players and spells during pause
      DISPLAY.blit(font.render('Press P to Unpause', True, (255, 255, 255)), (350, 150))
      for i in range(len(players)):
        if not players[i].alive:
          continue
        else:
          players[i].render(DISPLAY)
      for j in range(len(spells)):
        spells[j].render(DISPLAY)
    else:
      #counting alive players
      alive = 0
      for i in range(len(players)):
        if not players[i].alive:
          continue
        alive += 1
        #if only 1 player is alive, declare the winner
        winner = i
        #handle player logic and casting
        players[i].tick()
        newspell = players[i].autocast()
        if newspell != None:
          spells.append(newspell)
          spells[-1].owner = i
        #rendering and controls
        players[i].render(DISPLAY)
        keys = pygame.key.get_pressed()
        for k in range(len(keys)):
          #disable if stunned
          if keys[k] and pygame.key.name(k) in players[i].controls and players[i].stun == 0:
            newspell = players[i].control(pygame.key.name(k))
            if newspell != None:
              spells.append(newspell)
              spells[-1].owner = i
        #apply movement
        if terrain_collision_x(players[i]) and not terrain_collision_y(players[i]):
          players[i].mx = 0
          players[i].move()
        elif terrain_collision_y(players[i]) and not terrain_collision_x(players[i]):
          players[i].my = 0
          players[i].move()
        if terrain_collision(players[i]):
          players[i].mx = 0
          players[i].my = 0
        else:
          players[i].move()
        #handle spell logic
        for j in range(len(spells)):
            if spells[j] == -1:
                continue
            if i != spells[j].owner:
                #spell interaction on players
                if collision(players[i], spells[j]):
                    players[i].trigger(spells[j])
                    spells[j] = -1
            elif spells[j].movetype == 1:
                spells[j].init(players[i].dir, players[i].x, players[i].y)
      #mark ended spells to be deleted and remove them
      for i in range(len(spells)):
        if spells[i] == -1:
          continue
        spells[i].render(DISPLAY)
        if spells[i].tick() or terrain_collision(spells[i]):
          spells[i] = -1
      while -1 in spells:
        spells.remove(-1)
      #win condition
      if alive == 1:
        game_running = False
  elif drafting:
    pass
  else:
    DISPLAY.blit(font.render('Press G to Start', True, (255, 255, 255)), (300, 200))
    DISPLAY.blit(font.render('Use A and D to Change Map', True, (150, 150, 150)), (220, 100))
    DISPLAY.blit(font.render('Use W and S to Change Mode', True, (150, 150, 150)), (210, 150))
    #display last game's winner
    if winner > -1:
      DISPLAY.blit(font.render('Player ' + str(winner + 1) + ' Wins!', True, (255, 255, 0)), (300, 300))
    #display map names
    for i in range(len(map_names)):
      DISPLAY.blit(font.render(map_names[i], True, (255, 255, 255) if map == i else (150, 150, 150)), ((i * 150) + 10, 20))
    for i in range(len(mode_names)):
      DISPLAY.blit(font.render(mode_names[i], True, (255, 255, 255) if mode == i else (150, 150, 150)), (((i * 150) + 10, 400)))
    DISPLAY.blit(sfont.render(mode_descriptions[mode], True, (255, 255, 255)), (10, 350))
  #render map (this applies regardless of if the game runs)
  pygame.display.update()
  pygame.time.Clock().tick(60)
