import asyncio, time, os, pycord, requests, json
from corkus import Corkus
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from cairosvg import svg2png
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

def TotalPlayer(PG, username, lvl, classe, rank, uuid, online, last, playtime, guild):
    # Rectangle
    m = RoundRectangle(2560, 1080, 200)
    # Prepare to draw + init font
    draw = ImageDraw.Draw(m)
    font = ImageFont.truetype("Ubuntu-Regular.ttf", 86)
    font2 = ImageFont.truetype("Ubuntu-Regular.ttf", 42)
    # [Rank] Username (Class) Draw
    draw.text((650, 100),f"[{rank}] {username} ({classe})",(255,255,255),font=font)
    # Guild Name
    draw.text((650, 210),f"Guild: {guild}",(255,255,255),font=font2)
    # Last Online
    draw.text((650, 260),f"Last Online: {last.strftime('%m/%d/%Y, %H:%M:%S')}",(255,255,255),font=font2)
    # Playtime
    draw.text((650, 312),f"Playtime: {round(playtime.hours(4.7),2)}h",(255,255,255),font=font2)
    # Level Draw
    draw.text((2200, 364),"lvl"+str(lvl),(255,255,255),font=font)
    # Skin Draw
    img_data = requests.get(f'https://visage.surgeplay.com/bust/350/{uuid}').content
    with open('temp.png', 'wb') as handler:
        handler.write(img_data)
    m.paste(Image.open("temp.png"), (150, 100), Image.open("temp.png"))

    # Books draw

    # Strenght
    img_data = requests.get('https://cdn.wynncraft.com/nextgen/skill/strength_book.svg').content
    svg2png(url=img_data, write_to="temp.png")
    m.paste(Image.open("temp.png"), (150, 500), Image.open("temp.png"))
    
    # Check Online
    if online:
        draw.ellipse((525, 100, 625, 200), fill=(0, 255, 0))
    else:
        draw.ellipse((525, 100, 625, 200), fill=(255, 0, 0))
    m.paste(PB(2260, 42, 50, PG), (150, 460))
    m = m.resize((2560 // 2, 1080 // 2), resample=Image.LANCZOS)
    m.show()
    # Rectangle
    m = RoundRectangle(2560, 1080, 200)
    # Prepare to draw + init font
    draw = ImageDraw.Draw(m)
    font = ImageFont.truetype("Ubuntu-Regular.ttf", 86)
    font2 = ImageFont.truetype("Ubuntu-Regular.ttf", 42)
    # [Rank] Username (Class) Draw
    draw.text((650, 100),f"[{rank}] {username} ({classe})",(255,255,255),font=font)
    # Guild Name
    draw.text((650, 210),f"Guild: {guild}",(255,255,255),font=font2)
    # Last Online
    draw.text((650, 260),f"Last Online: {last.strftime('%m/%d/%Y, %H:%M:%S')}",(255,255,255),font=font2)
    # Playtime
    draw.text((650, 312),f"Playtime: {round(playtime.hours(4.7),2)}h",(255,255,255),font=font2)
    # Level Draw
    draw.text((2200, 364),"lvl"+str(lvl),(255,255,255),font=font)
    # Skin Draw
    img_data = requests.get(f'https://visage.surgeplay.com/bust/350/{uuid}').content
    with open('temp.png', 'wb') as handler:
        handler.write(img_data)
    m.paste(Image.open("temp.png"), (150, 100), Image.open("temp.png"))
    # Check Online
    if online:
        draw.ellipse((525, 100, 625, 200), fill=(0, 255, 0))
    else:
        draw.ellipse((525, 100, 625, 200), fill=(255, 0, 0))
    m.paste(PB(2260, 42, 50, PG), (150, 460))
    m = m.resize((2560 // 2, 1080 // 2), resample=Image.LANCZOS)
    m.show()

async def SearchPlayer(ign, index=0):
    async with Corkus() as corkus:
        p = await corkus.player.get(ign)
        c = p.characters[index]
        if p.guild:
            TotalPlayer(c.combat.level_progress, p.username, c.combat.level, c.display_name, str(p.tag).replace('PlayerTag.',''), str(p.uuid), p.online, p.last_online, p.playtime, p.guild.name)
        else:
            TotalPlayer(c.combat.level_progress, p.username, c.combat.level, c.display_name, str(p.tag).replace('PlayerTag.',''), str(p.uuid), p.online, p.last_online, p.playtime, "None")

async def main():
    await SearchPlayer("DiamaXV", 0)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())