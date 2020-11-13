
import discord

import os

from dotenv import load_dotenv

from discord import Game, File

from discord import Status

from discord.ext import commands

from PotionStepNode import load_potions_recipes_tree

import PotionRecipe

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX')


class PotionsHPBot:

    def __init__(self, bot_prefix, token):
        self.bot = commands.Bot(command_prefix=bot_prefix)
        self.token = token
        self.brewing_statuses = {}
        self.potions_recipes_tree = load_potions_recipes_tree()
        self.on_load()

    def on_load(self):

        @self.bot.event
        async def on_ready():
            await self.bot.change_presence(activity=Game(name="Brewing Potions"), status=Status.online)
            print(f'{self.bot.user.name} has connected to Discord!')
            print(os.path.dirname(os.path.abspath(__file__)))
            print(os.path.dirname(os.path.abspath(__file__)) + "\PotionsRecipes\Elixir_To_Induce_Euphoria.json")
            print(PotionRecipe.PotionRecipe.load_from_json(os.path.dirname(os.path.abspath(__file__)) +
                                                           "\PotionsRecipes\Elixir_To_Induce_Euphoria.json"))

        @self.bot.command(name="brew", help="Start brewing a potion!")
        async def start_brewing(ctx):
            author = ctx.author
            self.brewing_statuses[author.id] = self.potions_recipes_tree.get_root()
            await ctx.send("You started brewing! Use add, stir ,heat and wave commands for continue brewing "
                           "until you finish brewing the potion!")

        @self.bot.command(name="add", help="Add an ingredient to the cauldron!")
        async def add(ctx, *ingredient):
            ingredient = " ".join(ingredient)
            ingredient = ingredient.lower()
            if ingredient == "stir" or ingredient.startswith("stir "):
                pass
            elif ingredient.startswith("heat ") or ingredient.endswith("heat "):
                pass
            elif ingredient.startswith("wave wand"):
                pass

            author = ctx.author
            if author.id not in self.brewing_statuses.keys():
                await start_brewing(ctx)
            if self.brewing_statuses[author.id].has_child(ingredient):
                self.brewing_statuses[author.id] = self.brewing_statuses[author.id].get_child(ingredient)
                potion = self.brewing_statuses[author.id].get_info().get_potion()
                if potion is not None:
                    await ctx.send(file=File(os.path.dirname(os.path.abspath(__file__)) +
                                             "\\Images\\Potions\\cauldron.jpg")
                                   , content="Good Job! You have brewed the " + potion + " potion!")
                else:
                    await ctx.send("You have added the " + ingredient + " to the cauldron!")
            else:
                await ctx.send("You have added the " + ingredient + " to the cauldron and it blew up! "
                                                                    "Try again!")

        @self.bot.command(name="stir", help="Stir the potion in the cauldron!")
        async def stir(ctx, direction=""):
            if direction != "":
                direction = direction.lower()
                if direction != "clockwise" and direction != "anti-clockwise":
                    await ctx.send("Invalid stirring direction! Only valid stirring directions are: "
                                   "clockwise and anti-clockwise")
                    return
                direction = " " + direction
            author = ctx.author
            if author.id not in self.brewing_statuses.keys():
                await start_brewing(ctx)
            if self.brewing_statuses[author.id].has_child("stir" + direction):
                pass
            elif self.brewing_statuses[author.id].has_child("stir"):
                direction = ""
            else:
                direction = direction.lstrip()
                await ctx.send("You have stirred the potion " + direction + " in the cauldron and it blew up! "
                               "Try again!")
                return
            self.brewing_statuses[author.id] = self.brewing_statuses[author.id].get_child("stir" + direction)
            potion = self.brewing_statuses[author.id].get_info().get_potion()
            if potion is not None:
                await ctx.send("Good Job! You have brewed the " + potion + " potion!")
            else:
                direction = direction.lstrip()
                await ctx.send("You have stirred the potion " + direction + " in the cauldron!")

        @self.bot.command(name="heat", help="Set the heat of the cauldron!")
        async def heat(ctx, level=""):
            level = level.lower()
            if level != "high" and level != "medium" and level != "low":
                await ctx.send("Invalid heat level! Valid heat levels are: high, medium and low")
                return
            action = level + " heat"
            author = ctx.author
            if author.id not in self.brewing_statuses.keys():
                await start_brewing(ctx)
            if self.brewing_statuses[author.id].has_child(action):
                self.brewing_statuses[author.id] = self.brewing_statuses[author.id].get_child(action)
                potion = self.brewing_statuses[author.id].get_info().get_potion()
                if potion is not None:
                    await ctx.send("Good Job! You have brewed the " + potion + " potion!")
                else:
                    await ctx.send("You have set the cauldron's heat to " + level + "!")
            else:
                await ctx.send("You have set the cauldron's heat to " + level + " and it blew up! "
                                                                                "Try again!")

        @self.bot.command(name="wave", help="Wave the wand above the cauldron!")
        async def wave(ctx):
            action = "wave wand"
            author = ctx.author
            if author.id not in self.brewing_statuses.keys():
                await start_brewing(ctx)
            if self.brewing_statuses[author.id].has_child(action):
                self.brewing_statuses[author.id] = self.brewing_statuses[author.id].get_child(action)
                potion = self.brewing_statuses[author.id].get_info().get_potion()
                if potion is not None:
                    await ctx.send("Good Job! You have brewed the " + potion + " potion!")
                else:
                    await ctx.send("You have added the " + action + " to the cauldron!")
            else:
                await ctx.send("You have added the " + action + " to the cauldron and it blew up! "
                                                                "Try again!")

    def run(self):
        self.bot.run(self.token)


if __name__ == "__main__":
    bot = PotionsHPBot(BOT_PREFIX, TOKEN)
    bot.run()
