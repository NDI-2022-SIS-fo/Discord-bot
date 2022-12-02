import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

"""
CLIENT CREATION
"""

bot = commands.Bot()


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


"""
COMMANDS
"""


@bot.slash_command(name="help",
                   description="Donne des informations à propos de ce bot")
async def helpC(interaction):
    embed = discord.Embed(title="Notre bot sur SIS-fo", description="ECRIRE LA DESCRIPTION", color=0x00ff00)
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

lienhelpPages = {
    "avortement": "https://www.ameli.fr/assure/remboursements/rembourse/contraception-ivg/ivg#:~:text=L'IVG%20instrumentale%20est%20rembours%C3%A9e,la%20dur%C3%A9e%20de%20l'hospitalisation.",
    "pillule_lendemain": "https://www.ameli.fr/assure/sante/themes/contraception-urgence/prendre-procurer-pilule-lendemain",
    "VIH": "https://www.sida-info-service.org/depistages-vih/",
    "SIDA": "https://www.sida-info-service.org/categorie/questions-frequentes/foire-aux-questions-sida/",
    "contraception": "ameli.fr/assure/sante/themes/contraception/choisir-mode-contraception#:~:text=La%20délivrance%20de%20la%20contraception,prévention%20des%20maladies%20sexuellement%20transmissibles.",
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
    embed.add_field(name="Lien vers le SIS pour plus d'infos", value=f"https://www.sida-info-service.org/?s={terme}")
    await interaction.response.send_message(embed=embed)


@bot.slash_command(name="signingame",
                   description="Vous fait apparaître / disparaître du jeu")
async def signingame_command(interaction):
    # TODO FAIRE REQUETE BACK POUR TOGGLE LE JOUEUR DE LA BDD
    # RECOIT UN BOOL QUI DIT SI AJOUT OU SUPPRESSION BDD
    response = random.random() > .5
    embed = discord.Embed(
        title=f"Vous vous êtes {'ajouté dans' if response else 'retiré de'} la liste des joueurs qui peuvent tomber dans le jeu",
        color=0x00ff00)
    await interaction.response.send_message(embed=embed, ephemeral=True)


facts = [
    "On guérit du SIDA: FAUX,Même si des trithérapies performantes existent depuis 1996, on ne guérit toujours pas du SIDA. Les trithérapies permettent de \"mieux vivre\" avec le virus mais celui-ci reste toujours présent dans l'organisme. Une infection par le VIH s'évite en utilisant un moyen de prévention adapté à ses pratiques.",
    "Le préservatif empêche seulement le risque de grossesse mais pas les IST Le préservatif est le SEUL moyen pour éviter la transmission des IST (Infection Sexuellement Transmissible). En effet, le préservatif permet d’éviter les contacts entre les muqueuses sexuelles et liquides sexuels des partenaires. Il évite que les spermatozoïdes remontent jusque dans l’utérus et ne puisse féconder un ovocyte et que des IST puissent se transmettre d’un partenaire à l’autre. Il est donc indispensable d’utiliser le préservatif dès le début des contacts sexuels car certaines IST se transmettent déjà lors des caresses sexuelles et non uniquement durant la pénétration!",
]


class FactView(discord.ui.View):
    @discord.ui.button(label="Je le savais déjà", style=discord.ButtonStyle.green, emoji="👍")
    async def button_callback_good(self, button, interaction):
        # ENVOYER BON VOTE BDD ET RETOURNER POURCENTAGE POSITIF
        percent = int(random.random() * 100)
        await interaction.response.send_message(
            f"Votre vote a été pris en compte, vous êtes {percent}% des votants à le savoir", ephemeral=True)

    @discord.ui.button(label="Je le savais pas du tout", style=discord.ButtonStyle.red, emoji="👎")
    async def button_callback_bad(self, button, interaction):
        # ENVOYER PAS BON VOTE BDD ET RETOURNER POURCENTAGE NEGATIF
        percent = int(random.random() * 100)
        await interaction.response.send_message(
            f"Votre vote a été pris en compte, vous êtes {percent}% des votants à ne pas le savoir", ephemeral=True)


@bot.slash_command(name="fact",
                   description="Vous propose une idée reçue ou une définition d'un terme aléatoire")
async def fact_command(interaction):
    fact = random.choice(facts)
    embed = discord.Embed(
        title=f"Random fact", description=fact,
        color=0x00ff00)
    await interaction.response.send_message(embed=embed, view=FactView())


"""
RUN THE BOT
"""
print("I AM ONLINE")
bot.run(TOKEN)
