# This project requires the 'members' and 'message_content' privileged intents to function.

# region (Import and Config)

import datetime
import random

import discord
from discord import app_commands
from discord.ui import Select, View
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)
bot.remove_command('help')

# colors

RED = "\033[1;31m"
CYAN = "\033[1;36m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
BLUE = "\033[1;34m"
GREEN = "\033[0;32m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"


# endregion (Import and Config)

# region (Events)

@bot.event  # Main
async def on_ready():
    now = datetime.datetime.now()
    now = now.strftime("%H:%M:%S")
    print(f'I am {bot.user} (ID: {bot.user.id})')
    print("Agora são " + now)
    print('------')

    await bot.change_presence(activity=discord.Game(name="?help"))

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    guild = bot.get_guild(0)

    if (message.guild == guild):

        if "Oi Bot" in message.content:
            await message.channel.send(f"Oi {message.author.mention}")

    await bot.process_commands(message)


# endregion (Events)

# region (Utility Commands)

@bot.command(name="hello")
async def send_hello(ctx):
    nome = ctx.author.mention

    resposta = "ola, " + nome

    await ctx.send(resposta)


@bot.command(name="ge")  # Develop
async def getemoji(ctx, emoji):
    print(emoji)


@bot.command(name="say", aliases=['s'])
async def say(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)


@bot.command(aliases=['m'])
async def math(ctx, n1: float = 0, signal: str = "+", n2: float = 0):
    match signal:
        case "+":
            resposta = n1 + n2
            await ctx.send(f"{n1} + {n2} = {resposta}")

        case "-":
            resposta = n1 - n2
            await ctx.send(f"{n1} - {n2} = {resposta}")

        case "*":
            resposta = n1 * n2
            await ctx.send(f"{n1} * {n2} = {resposta}")

        case "/":
            resposta = n1 / n2
            await ctx.send(f"{n1} / {n2} = {resposta}")

        case _:
            await ctx.send(f"'{signal}' não é um sinal válido")


@bot.command(aliases=['c'])
async def clear(ctx, quantidade=100):
    if ctx.author.guild_permissions.ban_members:
        if quantidade <= 200:
            if quantidade >= 2:
                await ctx.channel.purge(limit=quantidade)
                await ctx.send(f"**{quantidade} mensagens foram apagadas com susseso!**")
            else:
                await ctx.send(f"**A quantidade não pode ser menor que 2**")
        else:
            await ctx.send(f"**{quantidade} é um numero muito grande!**")
    else:
        await ctx.send("**Você não possui permisão para usar este comando!**")


@bot.command()
async def roll(ctx, n=1, d=6):
    if n <= 100:
        if d >= 0:
            value_list = []
            total = 0

            while n >= 1:
                value = random.randint(1, d)

                value_list.append(value)

                n -= 1

            # for -> 0,...
            for x in value_list:
                total = total + x

            value_list = str(value_list).replace(",", " +")

            await ctx.send(f"`{value_list}` = `{total}`")

        else:
            await ctx.send(f"Não pode ter numeros negativos ou igual a 0 nos campos")

    else:
        await ctx.send(f"A quantidade de rolls não pode ser maior que 100")


# endregion (Utility Commands)

# region (Help)

@bot.command(aliases=['h'])
async def help(ctx, command=None):
    embed = discord.Embed(title="?help", color=0x00d1ce)
    embed.set_thumbnail(url=bot.user.avatar.url)

    match command:

        case None:
            embed.description = "Use `?help <nome do comando>` para ver mais detalhes do comando"

            embed.add_field(name="Utilitários", value="`?math` `?clear` `?roll`", inline=True)

        case "math":
            embed.description = (
                '''math (m): realiza um cálculo
**Sintaxe: ?math <1° numero> <Sinal> <2° numero>**'''
            )

        case "clear":
            embed.description = (
                '''clear (c): Apaga a quantidade de mensagens fornecidas 
**Sintaxe: ?clear <numero de mensagens>**'''
            )

        case "roll":
            embed.description = (
                '''roll : sorteia um numero
**Sintaxe: ?roll <quantidade de vezes> <numero máximo>**'''
            )

    await ctx.reply(embed=embed)


# region (Extras)

@bot.command()
async def hum(ctx):
    await ctx.send(
        '''⣞⢽⢪⢣⢣⢣⢫⡺⡵⣝⡮⣗
⠸⡸⠜⠕⠕⠁⢁⢇⢏⢽⢺⣪⡳⡝⣎⣏⢯⢞⡿⣟⣷⣳⢯⡷⣽⢽⢯⣳⣫⠇
⠀⠀⢀⢀⢄⢬⢪⡪⡎⣆⡈⠚⠜⠕⠇⠗⠝⢕⢯⢫⣞⣯⣿⣻⡽⣏⢗⣗⠏⠀
⠀⠪⡪⡪⣪⢪⢺⢸⢢⢓⢆⢤⢀⠀⠀⠀⠀⠈⢊⢞⡾⣿⡯⣏⢮⠷⠁
⠀⠀⠀⠈⠊⠆⡃⠕⢕⢇⢇⢇⢇⢇⢏⢎⢎⢆⢄⠀⢑⣽⣿⢝⠲⠉⠀
⠀⠀⠀⠀⠀⡿⠂⠠⠀⡇⢇⠕⢈⣀⠀⠁⠡⠣⡣⡫⣂⣿⠯⢪⠰⠂
⠀⠀⠀⠀⡦⡙⡂⢀⢤⢣⠣⡈⣾⡃⠠⠄⠀⡄⢱⣌⣶⢏⢊⠂
⠀⠀⠀⠀⢝⡲⣜⡮⡏⢎⢌⢂⠙⠢⠐⢀⢘⢵⣽⣿⡿⠁⠁
⠀⠀⠀⠀⠨⣺⡺⡕⡕⡱⡑⡆⡕⡅⡕⡜⡼⢽⡻⠏⠀
⠀⠀⠀⠀⣼⣳⣫⣾⣵⣗⡵⡱⡡⢣⢑⢕⢜⢕⡝⠀
⠀⠀⠀⣴⣿⣾⣿⣿⣿⡿⡽⡑⢌⠪⡢⡣⣣⡟⠀
⠀⠀⠀⡟⡾⣿⢿⢿⢵⣽⣾⣼⣘⢸⢸⣞⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠁⠇⠡⠩⡫⢿⣝⡻⡮⣒⢽⠋
''')


@bot.command()
async def wa(ctx):
    embed = discord.Embed(title="Zero Two",
                          description="Darling in the FranXX \n 1053 <:Kakera_Fake:1023657041761423391> \n React with any emoji to claim!",
                          color=0xff7b00)
    user = bot.get_user(432610292342587392)
    embed.set_author(name=user.name, icon_url=user.avatar.url)
    embed.set_image(url="https://mudae.net/uploads/2706259/FDrlwr_nab6woZb5SdAg~Fexte63.png")
    await ctx.send(embed=embed)
    await ctx.message.delete()


# endregion (Extras)

# region (/) commands

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World!")


@bot.tree.command(name="say")
@app_commands.describe(mensagem="Mensagem para o Bot falar")
async def say(interaction: discord.Interaction, mensagem: str):
    await interaction.response.send_message(mensagem)

# endregion (/) commands

# region (Exemplos)

# region Button

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Send Message", style=discord.ButtonStyle.grey)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Hello World!")

    @discord.ui.button(label="Edit Message", style=discord.ButtonStyle.green)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Essa mensagem foi editada")

    @discord.ui.button(label="Edited Embed 1", style=discord.ButtonStyle.blurple)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Esse é um embed de teste", color=0x00d1ce)
        # embed.set_author(name= bot.user.name, icon_url = bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.description = (
            '''
  embed 1
  '''
        )

        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Edited Embed 2", style=discord.ButtonStyle.blurple)
    async def menu4(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Esse é um embed de teste", color=0x00d1ce)
        # embed.set_author(name= bot.user.name, icon_url = bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.description = (
            '''
  embed 2
  '''
        )

        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Quit", style=discord.ButtonStyle.red)
    async def menu5(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.menu1.disabled = True  # set button.disabled to True to disable the button 1
        self.menu2.disabled = True  # set button.disabled to True to disable the button 2
        self.menu3.disabled = True  # set button.disabled to True to disable the button 3
        self.menu4.disabled = True  # set button.disabled to True to disable the button 4
        self.menu5.disabled = True  # set button.disabled to True to disable the button 5
        await interaction.response.edit_message(content="Bye bye", view=self)


@bot.command()  # Ex
async def menu(ctx):
    view = Menu()
    view.add_item(discord.ui.Button(label="URL", style=discord.ButtonStyle.link, url="https://youtu.be/82d9s8D6XE4",
                                    emoji="<:Platinum_Coin:1023735775218647141>"))
    await ctx.reply("Ola esse é o menu", view=view)


# endregion Button

# region Select

class MySelect(View):

    @discord.ui.select(
        placeholder="escolha uma opção",
        options=[
            discord.SelectOption(label="Embed editado", value="1", description="Este é um embed editado", emoji="1️⃣"),
            discord.SelectOption(label="Mensagem editada", value="2", description="Esta é uma mensagem editada",
                                 emoji="2️⃣"),
            discord.SelectOption(label="Mensagem normal", value="3", description="Esta é uma mensagem normal",
                                 emoji="3️⃣")
        ]
    )
    async def select_callback(self, interaction, select):
        select.disabled = True
        if select.values[0] == "1":
            embed = discord.Embed(title="Esse é um embed de teste", color=0x00d1ce)
            # embed.set_author(name= bot.user.name, icon_url = bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.description = (
                '''
embed 1
'''
            )
            await interaction.response.edit_message(embed=embed)

        if select.values[0] == "2":
            await interaction.response.edit_message(content="mensagem editada")
        if select.values[0] == "3":
            await interaction.response.send_message("Hello World!")


@bot.command()  # Ex
async def selectmenu(ctx):
    view = MySelect()
    await ctx.send("Ola esse é um Select Menu", view=view)


# endregion Select

# region Modal

class MyModal(discord.ui.Modal, title="Example Modal"):
    answer = discord.ui.TextInput(label="Should you subscribe to Digiwind", style=discord.TextStyle.short,
                                  placeholder="Yes?", default="Yes/No", required=False, max_length=6)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.title, description=f"**{self.answer.label}**\n{self.answer}",
                              color=discord.Colour.blue())
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)


@bot.tree.command(name="modal", description="An example modal")
async def modal(interaction: discord.Interaction):
    await interaction.response.send_modal(MyModal())


# endregion Modal

# endregion (Exemplos)

# region (Token)

with open('..\TOKEN.txt', 'r') as f:
    f_contents = f.readline()
    bot.run(f_contents)

# endregion

if exit:
    print(f"{RESET}{BOLD}Desligando...")
