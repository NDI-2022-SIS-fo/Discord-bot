import os
import random
import time

import discord
import socketio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

"""
CLIENT CREATION
"""

bot = commands.Bot()
sio = socketio.AsyncClient()


@sio.event
def connect():
    print("Server is connected!")


@sio.event
def connect_error(data):
    print("Server connection failed!")


@sio.event
def disconnect():
    print("Server is disconnected!")


@bot.event
async def on_ready():
    await sio.connect('http://146.59.158.131:5500/')
    print(f"We have logged in as {bot.user}")


"""
COMMANDS
"""


@bot.slash_command(name="help",
                   description="Donne des informations à propos de ce bot")
async def helpC(interaction):
    embed = discord.Embed(title="Notre bot sur SIS-fo",
                          description="Le bot permet de se renseigner sur des définitions de termes scientifiques, de raconter différents faits divers, et de faire le lien avec le jeu créé.",
                          color=0x00ff00)
    # TODO mettre le lien de l'app
    embed.add_field(name="Lien vers le jeu", value="METTRE LE LIEN VERS LE JEU ICI")
    await interaction.response.send_message(embed=embed)


helpPages = {
    "VIH": "Le virus de l'immunodéficience humaine (VIH) est un type de virus qui attaque le système immunitaire du corps.",
    "SIDA": "Le syndrome d'immunodéficience acquise, ou sida, est dû à l'infection par le virus de l'immunodéficience humaine (VIH) qui détruit les défenses immunitaires",
    "contraception": "Ensemble des moyens employés pour rendre les rapports sexuels inféconds.",
    "TROD": "Ce simple test rapide à l'aide d'une piqûre au bout de doigt permet de détacter: VIH, hépatite C et B",
    "avortement": "Interruption d'une gestation, naturelle (fausse couche) ou provoquée",
    "pillule_lendemain": "La pilule du lendemain est une méthode contraceptive exceptionnelle qui permet d'éviter une grossesse non désirée après un rapport sexuel non ou mal protégé",
}

lienHelpPages = {
    "avortement": "https://www.ameli.fr/assure/remboursements/rembourse/contraception-ivg/ivg#:~:text=L'IVG%20instrumentale%20est%20rembours%C3%A9e,la%20dur%C3%A9e%20de%20l'hospitalisation.",
    "pillule_lendemain": "https://www.ameli.fr/assure/sante/themes/contraception-urgence/prendre-procurer-pilule-lendemain",
    "VIH": "https://www.sida-info-service.org/depistages-vih/",
    "SIDA": "https://www.sida-info-service.org/categorie/questions-frequentes/foire-aux-questions-sida/",
    "contraception": "https://www.ameli.fr/assure/sante/themes/contraception/choisir-mode-contraception#:~:text=La%20délivrance%20de%20la%20contraception,prévention%20des%20maladies%20sexuellement%20transmissibles.",
    "TROD": "https://www.sida-info-service.org/trod-ou-test-de-depistage-rapide/",
}


def infoAutocomplete(self: discord.AutocompleteContext):
    return list(helpPages.keys())


@bot.slash_command(name="info",
                   description="Donne des informations à propos d'un terme spéficique")
@discord.commands.option(name="terme", type=str, autocomplete=infoAutocomplete)
async def info_command(interaction, terme: str):
    embed = discord.Embed(title=f"Infos sur le terme \"{terme}\"", description=helpPages[terme],
                          color=0x00ff00)
    embed.add_field(name="Lien vers plus d'infos sur le sujet", value=lienHelpPages[terme])
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="signingame",
                   description="Vous fait apparaître / disparaître du jeu")
async def signingame_command(interaction):
    # await sio.emit("toggle_user", {'id': interaction.user.id, 'name': interaction.user.name})
    #
    # @sio.on('toggle_callback')
    # async def callback_user(sid, data):
    #     response = data.response
    response = random.random() > 0.5
    embed = discord.Embed(
        title=f"Vous vous êtes {'ajouté dans' if response else 'retiré de'} la liste des joueurs qui peuvent tomber dans le jeu",
        color=0x00ff00)
    await interaction.response.send_message(embed=embed, ephemeral=True)

facts = [
    "On guérit du SIDA: FAUX,Même si des trithérapies performantes existent depuis 1996, on ne guérit toujours pas du SIDA. Les trithérapies permettent de \"mieux vivre\" avec le virus mais celui-ci reste toujours présent dans l'organisme. Une infection par le VIH s'évite en utilisant un moyen de prévention adapté à ses pratiques.",
    "La pilule empêche seulement le risque de grossesse mais pas les IST Le préservatif est le SEUL moyen pour éviter la transmission des IST (Infection Sexuellement Transmissible). En effet, le préservatif permet d’éviter les contacts entre les muqueuses sexuelles et liquides sexuels des partenaires. Il évite que les spermatozoïdes remontent jusque dans l’utérus et ne puisse féconder un ovocyte et que des IST puissent se transmettre d’un partenaire à l’autre. Il est donc indispensable d’utiliser le préservatif dès le début des contacts sexuels car certaines IST se transmettent déjà lors des caresses sexuelles et non uniquement durant la pénétration!",
]


@bot.slash_command(name="fact",
                   description="Vous propose une idée reçue ou une définition d'un terme aléatoire")
async def fact_command(interaction):
    fact = random.choice(facts)
    embed = discord.Embed(
        title=f"Random fact", description=fact,
        color=0x00ff00)

    class FactView(discord.ui.View):
        @discord.ui.button(label="Je le savais déjà", style=discord.ButtonStyle.green, emoji="👍")
        async def button_callback_good(self, button, interaction_b):
            #
            # await sio.emit("user_vote_fact", {"id": interaction_b.user.id, "fact": facts.index(fact), "upvote": True})
            #
            # @sio.on('vote_fact_callback')
            # async def vote_fact_callback(sid, data):
            #
            percent = int(random.random()*100)
            await interaction_b.response.send_message(
                f"Votre vote a été pris en compte, vous êtes {percent}% des votants à le savoir", ephemeral=True)

        @discord.ui.button(label="Je le savais pas du tout", style=discord.ButtonStyle.red, emoji="👎")
        async def button_callback_bad(self, button, interaction_b):
            # await sio.emit("user_vote_fact", {"id": interaction_b.user.id, "fact": facts.index(fact), "upvote": False})
            #
            # @sio.on('vote_fact_callback')
            # async def vote_fact_callback(sid, data):
            percent = int(random.random() * 100)
            await interaction_b.response.send_message(
                f"Votre vote a été pris en compte, vous êtes {percent}% des votants à ne pas le savoir", ephemeral=True)

    await interaction.response.send_message(embed=embed, view=FactView())


"""
RUN THE BOT
"""
print("I AM ONLINE")
bot.run(TOKEN)
