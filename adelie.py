# Adelie in PyGameZero

import pgzrun
import sys

WIDTH = 800
HEIGHT = 448

#LOGICAL_WIDTH = 48
#LOGICAL_HEIGHT = 28
LOGICAL_WIDTH = 256
LOGICAL_HEIGHT = 256

META = ""
SLIDES = []

COMMANDS = ['SIZE', 'GOTO', 'LINK', 'STOP', 'WAIT',
            'MODE', 'PICT', 'HEAD', 'TEXT', 'FILL', 'RECT']

CURRENT = 0

def draw():
  screen.fill((0, 0, 255))
  screen.draw.text("Adelie", (10, 10), fontsize=60, color="white")
  play_slide(CURRENT, screen)


def load_slides(data):
  global META, SLIDES
  in_meta = True
  slide = {}

  for line in data.split("\n"):
    if line[0:4] == 'NAME':
      if not in_meta:
        SLIDES.append(slide)
      else:
        in_meta = False
      slide = { 'name': line[5:], 'cmd': [], 'notes': [] }
    elif line[0:4] in COMMANDS:
      slide['cmd'].append(line)
    else:
      if in_meta:
        META += line.lstrip() + "\n"
      else:
        slide['notes'].append(line.lstrip())
  SLIDES.append(slide)


def scaled(x,y):
  return x * WIDTH / LOGICAL_WIDTH, y * HEIGHT / LOGICAL_HEIGHT


def play_slide(i, screen):
  global LOGICAL_WIDTH, LOGICAL_HEIGHT

  slide = SLIDES[i]
  notes = "\n".join(slide['notes'])
  print(f"Slide #{i} {slide['name']}")
  if notes:
    print(notes)

  x = 0
  y = 0

  for cmd in slide['cmd']:
    if cmd[0:4] == 'GOTO':
      x, y = [int(i, 16) for i in cmd[5:].split(',')]
    elif cmd[0:4] == 'SIZE':
      LOGICAL_WIDTH, LOGICAL_HEIGHT = [int(i, 16) for i in cmd[5:].split(',')]
    elif cmd[0:4] == 'MOVE':
      dx, dy = [int(i, 16) for i in cmd[5:].split(',')]
      x += dx
      y += dy
    elif cmd[0:4] == 'HEAD':
      screen.draw.text(cmd[5:].replace('`', "\n"), scaled(x,y), fontsize=60, color="red")
    elif cmd[0:4] == 'TEXT':
      screen.draw.text(cmd[5:].replace('`', "\n"), scaled(x,y), color="black")
    elif cmd[0:4] == 'PICT':
      screen.blit(cmd[5:], scaled(x, y))


def on_key_down(key):
  global CURRENT
  if key == keys.RIGHT:
    if CURRENT < len(SLIDES) - 1:
      CURRENT += 1
  elif key == keys.LEFT:
    if CURRENT > 0:
      CURRENT -= 1
  elif key == keys.ESCAPE:
    sys.exit(0)


if len(sys.argv) != 2:
  print(f"Usage: {sys.argv[0]} <adelie-file>")
  sys.exit(1)

with open(sys.argv[1]) as f:
  load_slides(f.read())

pgzrun.go()
