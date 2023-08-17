import asyncio, time, os, pycord, requests
from corkus import Corkus
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

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

def Total(PG, username, lvl, classe, rank, uuid, online, last, playtime):
    # Rectangle
    m = RoundRectangle(2560, 1080, 200)
    # Prepare to draw + init font
    draw = ImageDraw.Draw(m)
    font = ImageFont.truetype("Ubuntu-Regular.ttf", 86)
    font2 = ImageFont.truetype("Ubuntu-Regular.ttf", 42)
    # [Rank] Username (Class) Draw
    draw.text((650, 100),f"[{rank}] {username} ({classe})",(255,255,255),font=font)
    # Last Online
    draw.text((650, 200),f"Last Online: {last.strftime('%m/%d/%Y, %H:%M:%S')}",(255,255,255),font=font2)
    # Playtime
    draw.text((650, 242),f"Playtime: {playtime.hours(4.7)}h",(255,255,255),font=font2)
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

async def main():
    async with Corkus() as corkus:

        player = await corkus.player.get("enzomtp")
        print(f"username: {player.username}, {player.rank}")
        character = player.best_character
        print(f"best character: {character.display_name} ({character.combat.level}lv)")
        print(player.uuid)
        Total(character.combat.level_progress, player.username, character.combat.level, character.display_name, str(player.tag).replace('PlayerTag.',''), str(player.uuid), player.online, player.last_online, player.playtime)

        if player.guild:
            guild = await player.guild.fetch()
            print(f"guild: {player.guild.name} {guild.level}lv ({len(guild.members)} members)")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())