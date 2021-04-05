from Scripts.Un_Freeze_Arabic import Un_Freeze
from Scripts.CharmapCreator import BMFont_to_Charmap
from Scripts.Fit_in_box import fit
from time import sleep
from PIL import Image
import keyboard
import pygame

##################يجب ان يكون للخط صورة واحدة

def type_in_box(text, font_size, box_width, box_height, px_per_line, charmap, border_thick, newline, newpage, display, char_border = False, from_Right = False,
                x = 0, y = 0, sleep_time = 0, frames = 1, box_style = 0):
    X, Y = x, y
    if newpage: pages = text.split(newpage)
    else: pages = [text]
    if newline: splited_pages = [page.split(newline) for page in pages]
    else: splited_pages = [pages]
    
    for page in splited_pages:
        conversation(0, 0, box_width + border_thick * 2, box_height + border_thick * 2, 0, (255, 255, 255), border_thick, frames, box_style, display)
        for line in page:
            if from_Right: x = box_width
            for char in line:
                if char not in charmap: continue
                char_x, char_y, char_width, char_height = charmap[char][0], charmap[char][1], charmap[char][2], charmap[char][3]
                char_xoffset, char_yoffset, char_xadvance = charmap[char][4], charmap[char][5], charmap[char][6]
                if char_width > box_width: continue

                img = Image.open(img_directory)
                croped_img = img.crop((char_x, char_y, char_x+char_width, char_y+char_height))
                py_img = pygame.image.fromstring(croped_img.tobytes(), croped_img.size, croped_img.mode)

                if from_Right: x -= char_width
                display.blit(py_img, (x + char_xoffset, y + char_yoffset))
                if char_border:
                    pygame.draw.rect(display, (0, 255, 0), (x, y, char_width, font_size), 1)
                    pygame.draw.rect(display, (255, 0, 0), (x + char_xoffset, y + char_yoffset, char_width, char_height), 1)
                if from_Right: x -= char_xadvance
                else: x += char_width + char_xadvance
                
                pygame.display.update()
                sleep(sleep_time)
            y += font_size + px_per_line
            x = X
        y = Y
        keyboard.wait("enter")

def conversation(x, y, width, height, box_color, border_color, border_thick, frames, box_style, display):
    if box_style == 0:
        h = height
        for i in range(frames):
            w = width * (i + 1) / frames
            x = width / 2 - w / 2 
            pygame.draw.rect(display, box_color, (x, y, w, h))
            pygame.draw.rect(display, border_color, (x, y, w, h), border_thick)
            pygame.display.update()
            sleep(0.005)
    elif box_style == 1:
        for i in range(frames):
            w = width * (i + 1) / frames
            h = height * (i + 1) / frames
            x = width / 2 - w / 2 
            y = height / 2 - h / 2 
            pygame.draw.rect(display, box_color, (x, y, w, h))
            pygame.draw.rect(display, border_color, (x, y, w, h), border_thick)
            pygame.display.update()
            sleep(0.005)
    elif box_style == 2:
        x, w = width / 2, 0
        for i in range(frames):
            h = height * (i + 1) / frames
            y = height / 2 - h / 2
            pygame.draw.rect(display, box_color, (x, y, w, h))
            pygame.draw.rect(display, border_color, (x, y, w, h), border_thick)
            pygame.display.update()
            sleep(0.0025)
        h = height
        for i in range(frames):
            w = width * (i + 1) / frames
            x = width / 2 - w / 2 
            pygame.draw.rect(display, box_color, (x, y, w, h))
            pygame.draw.rect(display, border_color, (x, y, w, h), border_thick)
            pygame.display.update()
            sleep(0.0025)

def fit_advance(text, box_width, box_height, px_per_line, border_thick, fnt_directory, img_directory,
                newline = '', newpage = '', before_command = '', after_command = '', from_Right = False, sleep_time = 0, frames = 1, box_style = 0):
    keyboard.on_press_key("F3", lambda _: pygame.image.save(textbox, "screenshot.png"))

    charmap = BMFont_to_Charmap(fnt_directory)
    
    font_size = charmap['height']
    lines_num = int(box_height / (font_size * 2 + px_per_line) * 2)
    fitted_text = fit(Un_Freeze(text), charmap, box_width, lines_num, newline, newpage, before_command, after_command)
    
    print_text = fitted_text
    if newpage: print_text = print_text.replace(newpage, '\n\n')
    if newline: print_text = print_text.replace(newline, '\n')
    print('\n' + print_text)
    
    pygame.init()
    pygame.display.set_caption('Fit in box (Advanced)')
    textbox = pygame.display.set_mode((box_width + border_thick * 2, box_height + border_thick * 2))

    type_in_box(fitted_text, font_size, box_width, box_height, px_per_line, charmap, border_thick, newline, newpage, textbox, False, from_Right,
                border_thick, border_thick, sleep_time, frames, box_style)

    while True:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                quit()

print('\nPress enter to see the next page.')
print('Press F3 to save an image.')
print('-----------------------------------')

#fnt_directory, img_directory = r'tests\BMFontXml\chinese.fnt', r'tests\BMFontXml\Arabic_0.png'
#fit_advance('السلام عليكم ورحمة الله تعالى وبركاته', 400, 160, 10, 10, fnt_directory, img_directory, '\n', '\n\n', '[', ']', True)

#fnt_directory, img_directory = r'tests\The Legend of Zelda A Link to the Past\table.txt', r'tests\The Legend of Zelda A Link to the Past\unknown.png'
#text = 'Long ago, in the[gr] beautiful kingdom of hyrule surrounded by mountains and forests...'
#fit_advance(text, 180, 65, 5, 10, fnt_directory, img_directory, '[br]', '[page]', '[', ']', False, 0.03, 100, 2)

text = 'خط الميترويد يحييكم'
fnt_directory, img_directory = r'tests\Mitroid\font.fiba', r'tests\Mitroid\unknown.png'
fit_advance(text, 180, 65, 5, 10, fnt_directory, img_directory, '[br]', '[page]', '[', ']', True, 0.03, 100, 2)