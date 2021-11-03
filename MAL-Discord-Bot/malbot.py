# import the discord library

import os
import sys
import discord
from discord import message
from discord import embeds
from dotenv import load_dotenv
from jikanpy import AioJikan
import random
load_dotenv()

# bot connect
client = discord.Client()
# this variable stores id of an output channel, you can have many variables corresponding to different channels
out_channel = int(os.getenv('WEEBDOM'))  # add default out_channel

motor_function = [0]


@client.event
# new event
async def on_ready():
    # output_channel object holds the info of that channel, whos id is provided
    output_channel = client.get_channel(out_channel)
    # code to send message is
    await output_channel.send("> Do not fear, for I am here\n- All Might")


@client.event
async def on_message(message):
    async with AioJikan() as mal:
        output_channel = message.channel

        # To stop bot spam
        if message.content == "Za Warudo" and message.author.id == int(os.getenv("ADMIN")):
            motor_function[0] = 1
        if message.content == "Road Roller Da" and message.author.id == int(os.getenv("ADMIN")):
            motor_function[0] = 0

        input_mssg = message.content  # message.content is the string of that message
        message_list = input_mssg.split()  # split the string into a list of words
        try:
            if len(message_list) > 0:
                if message_list[0] == "mal":
                    if len(message_list) >= 3  and motor_function[0] == 0:
                        if message_list[1] == "search":
                            anime_search = ""
                            anime_page = 0
                            anime_type = "anime"
                            for i in range(2, len(message_list)):
                                if (message_list[i] == "page"):
                                    if(i < len(message_list) - 1):
                                        i += 1
                                        anime_page = int(message_list[i]) - 1
                                elif (message_list[i] in ["manga", "anime", "character", "person"]):
                                    anime_type = message_list[i]
                                else:
                                    anime_search += message_list[i] + " "
                            anime_list = await mal.search(query=anime_search,  search_type=anime_type)
                            anime_info = anime_list["results"][anime_page]
                            embed = discord.Embed(title=anime_info["title"], description=anime_info["synopsis"], color=0xffa500, url=anime_info["url"])
                            embed.set_thumbnail(url=anime_info["image_url"])
                            embed.add_field(name="Score", value=str(anime_info["score"]), inline=False)
                            embed.add_field(name="No Of Episodes", value=str(anime_info["episodes"]), inline=False)
                            embed.add_field(name="Start Date", value=str(anime_info["start_date"]), inline=True)
                            embed.add_field(name="End Date", value=str(anime_info["end_date"]), inline=True)
                            embed.set_footer(text="Requested by {}".format(message.author.display_name))
                            await output_channel.send(embed=embed)
                        elif message_list[1] == "user":
                            anime_user = await mal.user(username=message_list[2])
                            embed = discord.Embed(title="MAL Stats")
                            embed.set_author(name=anime_user["username"], url=anime_user["url"], icon_url=anime_user["image_url"])
                            embed.add_field(name="No of Anime Watched", value=str(anime_user["anime_stats"]["completed"]), inline=True)
                            embed.add_field(name="No of Episodes Watched", value=str(anime_user["anime_stats"]["episodes_watched"]), inline=True)
                            for i in range(len(anime_user["favorites"]["anime"])):
                                embed.add_field(name="Favourite Manga {}:".format(i+1), value=anime_user["favorites"]["anime"][i]["name"], inline=False)
                            embed.add_field(name="No of Manga Read", value=str(anime_user["manga_stats"]["completed"]), inline=True)
                            embed.add_field(name="No of Chapters Read", value=str(anime_user["manga_stats"]["chapters_read"]), inline=True)
                            for i in range(len(anime_user["favorites"]["manga"])):
                                embed.add_field(name="Favourite Manga {}:".format(i+1), value=anime_user["favorites"]["manga"][i]["name"], inline=False)
                            embed.set_footer(text="Requested by {}".format(message.author.display_name))
                            await output_channel.send(embed=embed)
                        elif message_list[1] == "random":
                            if message_list[2] == "anime":
                                anime_info = await mal.anime(random.randrange(0,2000,1))
                                embed = discord.Embed(title=anime_info["title"], description=anime_info["synopsis"], color=0xffa500, url=anime_info["url"])
                                embed.set_thumbnail(url=anime_info["image_url"])
                                embed.add_field(name="Score", value=str(anime_info["score"]), inline=False)
                                embed.add_field(name="No Of Episodes", value=str(anime_info["episodes"]), inline=False)
                                embed.set_footer(text="Requested by {}".format(message.author.display_name))
                                await output_channel.send(embed=embed)
                            elif message_list[2] == "manga":
                                manga_info = await mal.manga(random.randrange(0,2000,1))
                                embed = discord.Embed(title=manga_info["title"], description=manga_info["synopsis"], color=0xffa500, url=manga_info["url"])
                                embed.set_thumbnail(url=manga_info["image_url"])
                                embed.add_field(name="Score", value=str(manga_info["score"]), inline=False)
                                embed.add_field(name="No Of Chapters", value=str(manga_info["chapters"]), inline=False)
                                embed.set_footer(text="Requested by {}".format(message.author.display_name))
                                await output_channel.send(embed=embed)
        except:
            await output_channel.send("Debug Me Onii San")

# Run the client on this server
client.run(os.getenv('TOKEN'))  # add a bot token