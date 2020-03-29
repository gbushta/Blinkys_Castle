# Castle Sprites test
# With and animated Blinky Snake
# Adding Button A and B into the mix
#
import board
import displayio
import digitalio
import adafruit_imageload
from adafruit_gizmo import tft_gizmo

display = tft_gizmo.TFT_Gizmo()

button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(pull=digitalio.Pull.DOWN)
button_b = digitalio.DigitalInOut(board.BUTTON_B)
button_b.switch_to_input(pull=digitalio.Pull.DOWN)

displayHeight = 240
displayWidth = 240
blinky_counter = 0

bg_color = displayio.Bitmap(64, 64, 64)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000
bg_sprite = displayio.TileGrid(bg_color, pixel_shader=color_palette, x=0, y=0)

# Load the sprite sheet (bitmap)
sprite_sheet, palette = adafruit_imageload.load("/castle_sprite_sheet.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

sprite_sheet2, palette2 = adafruit_imageload.load("/blinky_sheet.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

sprite_tran_color = 0x00FF00
blinky_tran_color = 0x00FF00

for i, color in enumerate(palette):
    if color == sprite_tran_color:
        palette.make_transparent(i)
        break
for i, color in enumerate(palette2):
    if color == blinky_tran_color:
        palette2.make_transparent(i)
        break

# Create the sprite TileGrid
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16,
                            default_tile = 0)
sprite2 = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16,
                            default_tile = 1)
blinky = displayio.TileGrid(sprite_sheet2, pixel_shader=palette2,
                            width = 1,
                            height = 1,
                            tile_width = 22,
                            tile_height = 16,
                            default_tile = 0)

# Create the castle TileGrid
castle = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 7,
                            height = 7,
                            tile_width = 16,
                            tile_height = 16)

# Create a Group to hold the sprite and add it
sprite_group = displayio.Group()
sprite_group.append(sprite)
sprite_group.append(sprite2)
sprite_group.append(blinky)

# Create a Group to hold the castle and add it
castle_group = displayio.Group(scale=2)
castle_group.append(castle)

# Create a Group to hold the sprite and castle
group = displayio.Group()

# Add the sprite and castle to the group
group.append(bg_sprite)
group.append(castle_group)
group.append(sprite_group)

castle.x = 4
castle.y = 4
# Castle tile assignments
# corners
castle[0, 0] = 3  # upper left
castle[6, 0] = 5  # upper right
castle[0, 6] = 9  # lower left
castle[6, 6] = 11 # lower right
# top / bottom walls
for x in range(1, 6):
    castle[x, 0] = 4  # top
    castle[x, 6] = 10 # bottom
# left/ right walls
for y in range(1, 6):
    castle[0, y] = 6 # left
    castle[6, y] = 8 # right
# floor
for x in range(1, 6):
    for y in range(1, 6):
        castle[x, y] = 7 # floor
castle[0, 3] = 7
castle[6, 3] = 7

# put the sprite somewhere in the castle
sprite.x = 110
sprite.y = 70

sprite2[0] = 1
sprite2.x = 150
sprite2.y = 150

blinky.x = 50
blinky.y = 110
blinky_walk = [0,1,2,1]
blinky_walk2 = [3,4,5,4]
which_blinky = -1
going_right = True

# Add the Group to the Display
display.show(group)

while True:
    blinky_counter += 1
    if blinky_counter == 8000:
        blinky_counter = 0
        which_blinky += 1
        if which_blinky > len(blinky_walk) - 1:
            which_blinky = 0
        # Now I have to check for button presses A or B to
        # see which direction Blinky is facing.  Button A
        # is facing right. Button B is facing left.
        #
        # OMG I forgot to add if A and B are pressed
        # Just do nothing, or stay in place?
        if button_a.value and button_b.value:
            if going_right:
                which_blinky = 0
                blinky[0] = blinky_walk[which_blinky]
            else:
                which_blinky = 0
                blinky[0] = blinky_walk2[which_blinky]
        elif button_a.value:
            going_right = True
            blinky[0] = blinky_walk[which_blinky]
            blinky.x += 3
            if blinky.x > 190:
                blinky.x = 190
        elif button_b.value:
            going_right = False
            blinky[0] = blinky_walk2[which_blinky]
            blinky.x -= 3
            if blinky.x < 50:
                blinky.x = 50
        else:
            if going_right:
                which_blinky = 0
                blinky[0] = blinky_walk[which_blinky]
            else:
                which_blinky = 0
                blinky[0] = blinky_walk2[which_blinky]