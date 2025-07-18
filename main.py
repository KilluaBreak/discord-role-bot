import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
OWNER_IDS = {int(i) for i in os.getenv("OWNER_IDS").split(",")}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

ROLE_GROUPS = {
    "ras_dewa": [1382008246327312424],
    "ras_iblis": [1382008643326574622],
    "ras_naga": [1382010013144322128],
    "ras_elemental": [1385923115929833522],
    "ras_dwarf": [1385922167685775401],
    "ras_human": [1385921921677266995],
    "giveaway_ping": [1383027202970484766],
    "partnership_ping": [1383012056353210488],
    "partnership_event": [1383671901699702864],
    "promosi_ping": [1383366844450082817],
    "anime": [1381930147833315398],
    "donghua": [1381930494316515411],
    "komik": [1381931492518662214],
    "vocaloid": [1381931995373768744],
    "art": [1381932371787386920],
    "pengamat": [1381932623353610240],
    "free fire": [1383003121416011866],
    "PUBG": [1383003667178852494],
    "mobile legend": [1383003591614140477],
    "Valorant": [1387784579431272558],
    "minecraft": [1387784434278990046],
    "roblox": [1383003734552084531],
}

class GenericRoleDropdown(discord.ui.Select):
    def __init__(self, placeholder: str, option_pairs: list[tuple[str, str, str | None]]):
        opts = [
            discord.SelectOption(label=lab, value=val, emoji=emo)
            for lab, val, emo in option_pairs
        ]
        super().__init__(placeholder=placeholder, options=opts, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        key = self.values[0]
        role_ids = ROLE_GROUPS.get(key, [])
        roles = [interaction.guild.get_role(rid) for rid in role_ids if interaction.guild.get_role(rid)]

        if not roles:
            await interaction.response.send_message("❌ Role tidak ditemukan.", ephemeral=True)
            return

        try:
            await interaction.user.add_roles(*roles, reason="Self-assign")
            role_names = ", ".join(r.name for r in roles)
            await interaction.response.send_message(f"✅ Ditambahkan: {role_names}", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Bot kurang izin `Manage Roles`.", ephemeral=True)

class RoleMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GenericRoleDropdown(
            "click for pick your ras...",
            [
                ("🔱 Ras Dewa", "ras_dewa", None),
                ("😈 Ras Iblis", "ras_iblis", None),
                ("🐉 Ras Naga", "ras_naga", None),
                ("💨 Ras Elemental", "ras_elemental", None),
                ("⛏️ Ras Dwarf", "ras_dwarf", None),
                ("🧑‍🦲 Ras Human", "ras_human", None),
            ]))

class PingMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GenericRoleDropdown(
            "click for pick your ping...",
            [
                ("🎉 Giveaway Ping", "giveaway_ping", None),
                ("🤝 Partnership Ping", "partnership_ping", None),
                ("🔔 Partnership Event", "partnership_event", None),
                ("📣 Promosi Ping", "promosi_ping", None),
            ]))

class HobiMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GenericRoleDropdown(
            "click for pick your hobbie...",
            [
                ("🌸 Pencinta Anime", "anime", None),
                ("🔥 Pencinta Donghua", "donghua", None),
                ("📖 Pencinta Komik", "komik", None),
                ("🎧 Pencinta Musik", "vocaloid", None),
                ("🎨 Pencinta Gambar", "art", None),
                ("👀 Pengamat Server", "pengamat", None),
            ]))

class GameMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GenericRoleDropdown(
            "click for pick your game...",
            [
                ("💥 Free Fire", "free fire", None),
                ("🚪 PUBG", "PUBG", None),
                ("⚔️ Mobile Legends", "mobile legend", None),
                ("🔪 Valorant", "Valorant", None),
                ("🎧 Minecraft", "minecraft", None),
                ("📦 Roblox", "roblox", None),
            ]))

@bot.command(name="rolemenu")
async def rolemenu_cmd(ctx: commands.Context):
    if ctx.author.id not in OWNER_IDS:
        await ctx.send("❌ Kamu bukan admin.")
        return

    embed_color = discord.Color.from_str("#7542f5")

    embeds = [
        discord.Embed(title="Role Ras", description="pilih role yang kamu inginkan untuk di tunjukan ke Yulovers lainnya\n\n<@&1382008246327312424>\n<@&1382008643326574622>\n<@&1382010013144322128>\n<@&1385923115929833522>\n<@&1385922167685775401>\n<@&1385921921677266995>", color=embed_color).set_image(url="https://files.catbox.moe/7d3sj0.png"),
        discord.Embed(title="Role Ping", description="pilih role yang kamu inginkan untuk di tunjukan ke Yulovers lainnya\n\n<@&1383012056353210488>\n<@&1383671901699702864>\n<@&1383027202970484766>\n<@&1383371960733663242>", color=embed_color).set_image(url="https://files.catbox.moe/mueci9.png"),
        discord.Embed(title="Role Hobi", description="pilih role yang kamu inginkan untuk di tunjukan ke Yulovers lainnya\n\n<@&1381930147833315398>\n<@&1381930494316515411>\n<@&1381931492518662214>\n<@&1381931995373768744>\n<@&1381932371787386920>\n<@&1381932623353610240>", color=embed_color).set_image(url="https://files.catbox.moe/r2vry2.png"),
        discord.Embed(title="Role Games", description="pilih role yang kamu inginkan untuk di tunjukan ke Yulovers lainnya\n\n<@&1383003121416011866>\n<@&1383003667178852494>\n<@&1383003591614140477>\n<@&1387784579431272558>\n<@&1387784434278990046>\n<@&1383003734552084531>", color=embed_color).set_image(url="https://files.catbox.moe/ww7puf.png")
    ]

    await ctx.send(embed=embeds[0], view=RoleMenuView())
    await ctx.send(embed=embeds[1], view=PingMenuView())
    await ctx.send(embed=embeds[2], view=HobiMenuView())
    await ctx.send(embed=embeds[3], view=GameMenuView())

bot.run(TOKEN)
