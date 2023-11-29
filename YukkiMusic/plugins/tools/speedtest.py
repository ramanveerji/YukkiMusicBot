#
# Copyright (C) 2023-2024 by YukkiOwner@Github, < https://github.com/YukkiOwner >.
#
# This file is part of < https://github.com/YukkiOwner/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/YukkiOwner/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import speedtest
from pyrogram import filters
from strings import get_command
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS

# Commands
SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        
        # Running Download SpeedTest
        m = m.edit("Running Download SpeedTest")
        download_speed = test.download()
        
        # Running Upload SpeedTest
        m = m.edit("Running Upload SpeedTest")
        upload_speed = test.upload()
        
        # Sharing SpeedTest Results
        test.results.share()
        result = test.results.dict()
        m = m.edit("Sharing SpeedTest Results")
        
        # Add upload and download speed to the result dictionary
        result['download_speed'] = download_speed
        result['upload_speed'] = upload_speed
        
    except Exception as e:
        return m.edit(e)
    return result


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("Running Speed test")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    
    # Add upload and download speed to the output
    output = f"""**Speedtest Results**
    

<u>**Server:**</u>
**__Name:__** {result['server']['name']}
**__Country:__** {result['server']['country']}, {result['server']['cc']}
**__Sponsor:__** {result['server']['sponsor']}
**__Latency:__** {result['server']['latency']}  
**__Ping:__** {result['ping']}
  
<u>**Speeds:**</u>
**__Download Speed:__** {result['download_speed'] / 1024 / 1024:.2f} Mbps
**__Upload Speed:__** {result['upload_speed'] / 1024 / 1024:.2f} Mbps"""

    msg = await app.send_message(
        chat_id=message.chat.id, 
        text=output
    )
    await m.delete()

