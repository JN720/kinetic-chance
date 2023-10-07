import pygame
import random

PS = 20

class Player():
  def __init__(self, hp, spd, moveset, color, control, x = 0, y = 0, mr = 0.3):
    self.hp = hp
    self.maxhp = hp
    self.base_spd = spd
    self.moveset = moveset
    self.selmove = 0
    self.color = color
    self.x = x
    self.y = y
    self.mx = 0
    self.my = 0
    self.dx = PS * 2
    self.dy = PS * 2
    self.mana = 0
    self.lit = 0
    self.streak = 0
    self.dir = 0
    self.ecds = [0, 0, 0] #poison burn regen
    self.effs = [0, 0, 0]
    self.shield = 0
    self.scd = 0
    self.stun = 0
    self.alive = True
    self.castcd = 0
    self.selcd = 0
    self.castseq = []
    self.delays = []
    self.perm = 1
    self.mr = mr
    #right left down up streak lit cast
    if control == 0:
      self.controls = ['d', 'a', 's', 'w', 'q', 'e', 'f', 'c', 'x'] 
    elif control == 1:
      self.controls = ['l', 'j', 'k', 'i', 'u', 'o', ';', '.', ',']
    elif control == 2:
      self.controls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
  def render(self, display):
    if self.effs[0] > 0:
      pygame.draw.circle(display, (0, 150, 0, 0), (self.x + PS, self.y + PS), PS + 5, 3)
    if self.effs[1] > 0:
      pygame.draw.circle(display, (255, 100, 0, 0), (self.x + PS, self.y + PS), PS + 7, 3)
    if self.effs[2] > 0:
      pygame.draw.circle(display, (150, 0, 0, 0), (self.x + PS, self.y + PS), PS + 9, 3)
    if self.stun > 0:
      pygame.draw.circle(display, (0, 0, 150, 0), (self.x + PS, self.y + PS), PS + 11, 3)
    pygame.draw.rect(display, self.color, pygame.Rect(self.x, self.y, PS * 2, PS * 2))
    pygame.draw.rect(display, (0, 255, 0), pygame.Rect(self.x - (PS * 0.5), self.y - 20, self.hp * PS * 3 / self.maxhp, 8))
    pygame.draw.rect(display, (100, 100, 255), pygame.Rect(self.x - (PS * 0.5), self.y - 12, self.mana * PS * 1.5 / 50, 8))
    if self.shield > 0:
      pygame.draw.rect(display, (100, 100, 255), pygame.Rect(self.x, self.y, PS * 2, PS * 2), self.shield // 8)
    if self.streak > 0:
      pygame.draw.circle(display, (255, 255, 255), (self.x + PS, self.y + PS), self.streak * 3)
  def trigger(self, move):
    if move.damage > 0:
      if self.shield >= move.damage:
        self.shield -= move.damage
      elif self.shield > 0:
        self.hp -= move.damage - self.shield
        self.shield = 0
      else:
        self.hp -= move.damage
    if move.heal > 0:
      self.hp += move.heal
    if move.cleanse > 0:
      for i in range(2):
        self.effs[i] -= move.cleanse
        if self.effs[i] < 0:
          self.effs[i] = 0
    if move.poison > self.effs[0]:
      self.effs[0] = move.poison
      self.ecds[0] = 100
    if move.burn > self.effs[1]:
      self.effs[1] = move.burn
      self.ecds[1] = 50
    if move.regen > self.effs[2]:
      self.effs[2] = move.regen
      self.ecds[2] = 100
    if move.stun > self.stun:
      self.stun = move.stun
    if move.shield > self.shield:
      self.shield = move.shield
  def control(self, key):
    #movement
    if key == self.controls[0]:
      self.mx = self.base_spd
      self.dir = 0
    elif key == self.controls[1]:
      self.mx = -self.base_spd
      self.dir = 1
    elif key == self.controls[2]:
      self.my = self.base_spd
      self.dir = 2
    elif key == self.controls[3]:
      self.my = -self.base_spd
      self.dir = 3
    #movement readjustment
    if self.x < 0:
      self.x = 0
    if self.y < 0:
      self.y = 0
    if self.x > 800 - (PS * 2):
      self.x = 800 - (PS * 2)
    if self.y > 450 - (PS * 2):
      self.y = 450 - (PS * 2)
    #streak
    elif key == self.controls[4]:
      if self.scd == 0 and self.mana > 20:
        if random.randint(0, 1):
          self.streak += 1
        else:
          self.streak = 0
        self.scd = 15
        self.mana -= 20
    #literacy
    elif key == self.controls[5]:
      if self.mana > 1:
        self.mana -= 1
        self.lit += 0.2
    #cast
    elif key == self.controls[6] and self.castcd == 0:
      cost = MOVES[self.moveset[self.selmove]].cost
      if self.streak >= cost:
        self.streak -= cost
      elif self.lit >= cost * 15:
        self.lit -= cost * 15
      else: 
        return
      if MOVES[self.moveset[self.selmove]].movetype == 0:
        self.trigger(MOVES[self.moveset[self.selmove]])
      elif MOVES[self.moveset[self.selmove]].movetype == 3:
        aseq, adelays = MOVES[self.moveset[self.selmove]].copy()
        for i in aseq:
          self.castseq.append(i)
        for i in adelays:
          self.delays.append(i)
      else:
        base = MOVES[self.moveset[self.selmove]]
        move = base.copy()
        move.init(self.dir, self.x, self.y)
        return move
      self.castcd = 20
    #select
    elif key == self.controls[7] and self.selcd == 0:
      self.selmove += 1
      if self.selmove >= len(self.moveset):
        self.selmove = 0
      self.selcd = 10
    elif key == self.controls[8] and self.selcd == 0:
      self.selmove -= 1
      if self.selmove < 0:
        self.selmove = len(self.moveset) - 1
      self.selcd = 10
  def autocast(self):
    if self.castseq:
      if self.delays[0] > 0:
        self.delays[0] -= 1
      else:
        rmove = self.castseq[0]
        if len(self.castseq) == 1:
          self.castseq = []
          self.delays = []
        else:
          self.castseq = self.castseq[1:]
          self.delays = self.delays[1:]
        if rmove.movetype > 0:
          rmove.init(self.dir, self.x, self.y)
          return rmove
        else:
          self.trigger(rmove)
        
  def tick(self):
    #cd's
    if self.castcd > 0:
      self.castcd -= 1
    if self.selcd > 0:
      self.selcd -= 1
    #mana and streak
    self.mana += self.mr
    if self.mana > 100:
      self.mana = 100
    if self.scd > 0:
      self.scd -= 1
    #stun
    if self.stun > 0:
      self.stun -= 1
    #poison burn regen
    for i in range(len(self.ecds)):
      if self.ecds[i] == 0:
        if self.effs[i] > 0:
          self.effs[i] -= 1
          if i != 1:
            self.ecds[i] = 100
          else:
            self.ecds[i] = 50
          if i != 2:
            self.hp -= 10
          else:
            self.hp += 10
      else:
        self.ecds[i] -= 1
    #hp checks
    if self.hp > self.maxhp:
      self.hp = self.maxhp
    if self.hp <= 0:
      self.alive = False
      
  def move(self):
    self.x += self.mx
    self.y += self.my
    self.mx = 0
    self.my = 0

#damage, heal, poison, burn, stun, shield, regen
class Move():
  def __init__(self, cost = 1, damage = 0, heal = 0, poison = 0, burn = 0, stun = 0, shield = 0, regen = 0, cleanse = 0):
    self.cost = cost
    self.damage = damage
    self.heal = heal
    self.poison = poison
    self.burn = burn
    self.stun = stun
    self.shield = shield
    self.regen = regen
    self.cleanse = cleanse
    self.x = 0
    self.y = 0
    self.dir = 0
    self.owner = -1
    self.alive = False
    self.movetype = 0
  def copy(self):
    rmove = Move()
    rmove.cost = self.cost
    rmove.damage = self.damage
    rmove.heal = self.heal
    rmove.poison = self.poison
    rmove.burn = self.burn
    rmove.stun = self.stun
    rmove.shield = self.shield
    rmove.regen = self.regen
    rmove.cleanse = self.cleanse
    return rmove
    
class Melee(Move):
  def __init__(self, xsize, ysize, color, lifetime, cost = 1, damage = 0, heal = 0, poison = 0, burn = 0, stun = 0, shield = 0, regen = 0, cleanse = 0, perm = 1):
    super().__init__(cost, damage, heal, poison, burn, stun, shield, regen, cleanse)
    self.xsize = xsize
    self.ysize = ysize
    self.dx = xsize
    self.dy = ysize
    self.mx = 0
    self.my = 0
    self.color = color
    self.movetype = 1
    self.lifetime = lifetime
    self.perm = perm
  def copy(self):
    rmove = Melee(0, 0, 0, 0, damage = self.damage)
    rmove.cost = self.cost
    rmove.damage = self.damage
    rmove.heal = self.heal
    rmove.poison = self.poison
    rmove.burn = self.burn
    rmove.stun = self.stun
    rmove.shield = self.shield
    rmove.regen = self.regen
    rmove.cleanse = self.cleanse
    rmove.xsize = self.xsize
    rmove.ysize = self.ysize
    rmove.color = self.color
    rmove.lifetime = self.lifetime
    rmove.perm = self.perm
    return rmove
  def render(self, display):
      pygame.draw.rect(display, self.color, pygame.Rect(self.x, self.y, self.dx, self.dy))
  def tick(self): #returns whether to delete
    self.lifetime -= 1
    if self.lifetime == 0:
      return True
    return False
  def init(self, dir, x, y):
    self.dir = dir
    if self.dir == 0:
      self.dx = self.xsize
      self.dy = self.ysize
      self.x = x + 15
      self.y = y + 15 - (self.dy / 2)
    elif self.dir == 1:
      self.dx = self.xsize
      self.dy = self.ysize
      self.x = x + 15 - self.dx
      self.y = y + 15 - (self.dy / 2)
    elif self.dir == 2:
      self.dx = self.ysize
      self.dy = self.xsize
      self.y = y + 15
      self.x = x + 15 - (self.dx / 2)
    elif self.dir == 3:
      self.dx = self.ysize
      self.dy = self.xsize
      self.y = y + 15 - self.dy
      self.x = x + 15 - (self.dx / 2)

    
class Projectile(Melee):
  def __init__(self, speed, xsize, ysize, color, lifetime, cost = 1, damage = 0, heal = 0, poison = 0, burn = 0, stun = 0, shield = 0, regen = 0, cleanse = 0, spread = 0, perm = 1):
    super().__init__(xsize, ysize, color, lifetime, cost, damage, heal, poison, burn, stun, shield, regen, cleanse, perm)
    self.spread = spread
    self.speed = speed
    self.alive = True
    self.movetype = 2
  def copy(self):
    rmove = Projectile(0, 0, 0, 0, 0)
    rmove.spread = self.spread
    rmove.speed = self.speed
    rmove.cost = self.cost
    rmove.damage = self.damage
    rmove.heal = self.heal
    rmove.poison = self.poison
    rmove.burn = self.burn
    rmove.stun = self.stun
    rmove.shield = self.shield
    rmove.regen = self.regen
    rmove.cleanse = self.cleanse
    rmove.xsize = self.xsize
    rmove.ysize = self.ysize
    rmove.color = self.color
    rmove.lifetime = self.lifetime
    rmove.perm = self.perm
    return rmove
  def tick(self):
    if self.dir == 0:
      self.x += self.speed
      self.y += self.spread
    elif self.dir == 1:
      self.x -= self.speed
      self.y += self.spread
    elif self.dir == 2:
      self.y += self.speed
      self.x += self.spread
    elif self.dir == 3:
      self.y -= self.speed
      self.x += self.spread
    return super().tick()
  def init(self, dir, x, y):
    super().init(dir, x, y)
    self.spread = random.randint(-self.spread, self.spread)

    
class MultiSpecial():
  def __init__(self, move = None, cost = 1, repeat = 1, delays = [0], specid = 0):
    self.cost = cost
    self.delays = delays
    self.movetype = 3
    self.repeat = repeat
    self.specid = specid
    self.move = move
  def copy(self):
    seq = []
    for i in range(self.repeat):
      if self.specid == 0:
        seq.append(self.move.copy())
      elif self.specid == 1: #arrow
        r = random.randint(0, 4)
        amove = Projectile(3, 20, 6, (100, 50, 0), 120)
        if r == 1:
          amove.damage = 10
          amove.speed = 6
        elif r == 2:
          amove.damage = 30
          amove.speed = 9
          amove.perm = 2
        elif r == 3:
          amove.damage = 50
          amove.stun = 60
          amove.speed = 12
          amove.perm = 2
        seq.append(amove)
    return seq, self.delays

#trigger: cost, attributes
#melee: xsize, ysize, color, lifetime, cost attributes
#projectile: speed, xsize, ysize, color, lifetime, cost, attributes
#multispec: move, cost, repeat, delays, specid

acc_thrown_sword = Projectile(6, 40, 6, (200, 200, 200), 60, 1, damage = 10)
thrown_sword = Projectile(6, 40, 6, (200, 200, 200), 60, 1, damage = 10, spread = 1)

MOVES = {
  #1 streak
  'sword' : Melee(40, 6, (200, 200, 200), 60, 1, damage = 10),
  'flare' : Projectile(5, 15, 15, (255, 100, 0), 180, 1, burn = 1, perm = 0),
  #2 streak
  'heal' : Move(2, heal = 20, cleanse = 1),
  'regenerate' : Move(2, regen = 4),
  'shield' : Move(2, shield = 40),
  'intoxicate' : Projectile(4, 15, 6, (0, 150, 0), 60, 2, damage = 10, poison = 3),
  'zap' : Projectile(15, 5, 50, (0, 0, 255), 10, 2, damage = 20, stun = 60, perm = 3),
  'arrow' : MultiSpecial(cost = 2, specid = 1),
  'multisword' : MultiSpecial(acc_thrown_sword.copy(), 2, 3, [0, 10, 10]),
  #3 streak
  'cannon' : Projectile(8, 25, 25, (0, 0, 0), 300, 3, damage = 50, perm = 2),
  'fireball' : Projectile(6, 30, 20, (255, 100, 0), 180, 3, damage = 30, burn = 4, perm = 2),
  'asian slap' : Melee(40, 40, (255, 255, 0), 20, 3, damage = 30, stun = 120),
  'blade flurry' : MultiSpecial(thrown_sword.copy(), 3, 8, [0, 8, 8, 8, 8, 8, 8, 8]),
  'micronuke' : Projectile(5, 25, 20, (200, 200, 0), 300, 3, damage = 30, poison = 3, burn = 2, perm = 2),
  #4 streak
  'mega shield' : Move(4, shield = 100),
  'mega heal' : Move(4, heal = 100, cleanse = 4),
  'superstrike' : Projectile(12, 8, 70, (230, 230, 230), 180, 4, damage = 85, perm = 3),
  'volley' : MultiSpecial(cost = 4, repeat = 4, delays = [0, 8, 8, 8], specid = 1),
  'blade storm' : MultiSpecial(thrown_sword.copy(), 4, 12, [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]),
  'asphyxiate' : Projectile(3, 20, 8, (0, 120, 0), 240, 4, poison = 14),
  'milinuke' : Projectile(4, 30, 24, (180, 180, 0), 300, 4, damage = 50, poison = 5, burn = 3, stun = 30, perm = 2),
  #5 streak
  'parry this' : Projectile(14, 10, 10, (30, 30, 30), 300, 5, damage = 140)
}