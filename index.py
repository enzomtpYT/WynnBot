import asyncio, time, os, pycord, requests, json
from corkus import Corkus
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
# Define all variables
preconf = open('./config.json')
config = json.load(preconf)

def RoundRectangle(w, h, r):
    image = Image.new("RGBA", (w, h), (30,30,30,0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, w, h), fill=(30,30,30), radius=r)
    return image

def PB(w, h, r, p):
    image = Image.new("RGB", (w, h), (30,30,30))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, w, h), fill=(70, 91, 80), radius=r)
    draw.rounded_rectangle((0, 0, w*p/100, h), fill=(142, 195, 100), radius=r)
    return image

def TotalPlayer(p, c):
    # Rectangle
    m = RoundRectangle(2560, 1080, 200)
    # Prepare to draw + init font
    draw = ImageDraw.Draw(m)
    font = ImageFont.truetype("Ubuntu-Regular.ttf", 86)
    font2 = ImageFont.truetype("Ubuntu-Regular.ttf", 42)
    # [Rank] Username (Class) Draw
    draw.text((650, 100),f"[{str(p.tag).replace('PlayerTag.','')}] {p.username} ({c.display_name})",(255,255,255),font=font)
    # Guild Name
    if p.guild:
        draw.text((650, 210),f"Guild: {str(p.guild.name)}",(255,255,255),font=font2)
    else :
        draw.text((650, 210),"Guild: None",(255,255,255),font=font2)
    # Last Online
    draw.text((650, 260),f"Last Online: {p.last_online.strftime('%m/%d/%Y, %H:%M:%S')}",(255,255,255),font=font2)
    # Playtime
    draw.text((650, 312),f"Playtime: {round(p.playtime.hours(4.7),2)}h",(255,255,255),font=font2)
    # Level Draw
    draw.text((2200, 364),"lvl"+str(c.combat.level),(255,255,255),font=font)
    # Skin Draw
    img_data = requests.get(f'https://visage.surgeplay.com/bust/350/{str(p.uuid)}').content
    with open('temp.png', 'wb') as handler:
        handler.write(img_data)
    m.paste(Image.open("temp.png"), (150, 100), Image.open("temp.png"))

    # Books draw

    # Strenght
    m.paste(Image.open("assets/strength_book.png").resize((16 * 12, 17 * 12), resample=Image.NEAREST), (150, 500), Image.open("assets/strength_book.png").resize((16 * 12, 17 * 12), resample=Image.NEAREST))
    draw.text((220, 692),str(c.skill_points.strength),(255,255,255),font=font2)
    
    # Check Online
    if p.online:
        draw.ellipse((525, 100, 625, 200), fill=(0, 255, 0))
    else:
        draw.ellipse((525, 100, 625, 200), fill=(255, 0, 0))
    m.paste(PB(2260, 42, 50, c.combat.level_progress), (150, 460))
    m = m.resize((2560 // 2, 1080 // 2), resample=Image.LANCZOS)
    m.show()

async def SearchPlayer(ign, index=0):
    async with Corkus() as corkus:
        p = await corkus.player.get(ign)
        c = p.characters[index]
        if p.guild:
            TotalPlayer(p, c)
            c.skill_points.strength
        else:
            TotalPlayer(p, c)

async def main():
    await SearchPlayer("DiamaXV", 0)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())