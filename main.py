import discord
from discord.ext import commands
from discord import ui
import os
from dotenv import load_dotenv

# Load token dan owner
load_dotenv()
TOKEN = os.getenv("TOKEN")
OWNER_IDS = [int(i.strip()) for i in os.getenv("OWNER_IDS").split(",")]

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Opsi role yang tersedia
ROLE_OPTIONS1 = [
    discord.SelectOption(label="ras dewa", value="1382008246327312424"),
    discord.SelectOption(label="ras iblis", value="1382008643326574622"),
    discord.SelectOption(label="ras naga", value="1382010013144322128"),
    discord.SelectOption(label="ras elemental", value="1385923115929833522"),
    discord.SelectOption(label="ras dwarf", value="1385922167685775401"),
    discord.SelectOption(label="ras human", value="1385921921677266995"),
]
ROLE_OPTIONS2 = [
    discord.SelectOption(label="giveaway ping", value="1383027202970484766"),
    discord.SelectOption(label="partnership ping", value="1383012056353210488"),
    discord.SelectOption(label="partnership event", value="1383671901699702864"),
    discord.SelectOption(label="promosi ping", value="1383366844450082817"),
    discord.SelectOption(label="misteri ping", value="1387340859946569808"),
]
ROLE_OPTIONS3 = [
    discord.SelectOption(label="pencinta anime", value="1381930147833315398"),
    discord.SelectOption(label="pencinta donghua", value="1381930494316515411"),
    discord.SelectOption(label="pencinta komik", value="1381931492518662214"),
    discord.SelectOption(label="pencinta game", value="1382010013144322128","1383003121416011866","1383003591614140477","1383003667178852494","1383003734552084531"),
    discord.SelectOption(label="pencinta musik", value="1381931995373768744"),
    discord.SelectOption(label="pencinta gambar", value="1381932371787386920"),
    discord.SelectOption(label="pengamat server", value="1381932623353610240"),
]



# Komponen dropdown
class RoleDropdown(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="pick your ras",
            min_values=1,
            max_values=1,
            options=ROLE_OPTIONS1,
        )
     def __init__(self):
        super().__init__(
            placeholder="pick your ping",
            min_values=1,
            max_values=1,
            options=ROLE_OPTIONS2,
        )
     def __init__(self):
        super().__init__(
            placeholder="pick your hobby",
            min_values=1,
            max_values=1,
            options=ROLE_OPTIONS3,
        )

    async def callback(self, interaction: discord.Interaction):
        role_id = int(self.values[0])  # Ambil role ID dari dropdown
        role = interaction.guild.get_role(role_id)

        if role:
            await interaction.user.add_roles(role)  # Tambahkan role ke user
            await interaction.response.send_message(
                f"✅ Role **{role.name}** berhasil diberikan!",
                ephemeral=True  # hanya user yg melihat respon ini
            )
        else:
            await interaction.response.send_message(
                "❌ Role tidak ditemukan.",
                ephemeral=True
            )


# View yang berisi dropdown
class RoleDropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Penting untuk biar gak timeout
        self.add_item(RoleDropdown())


# Ketika bot siap
@bot.event
async def on_ready():
    print(f"✅ Bot login sebagai {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Error sync command: {e}")

# Command hanya bisa dijalankan oleh OWNER_IDS
@bot.tree.command(name="rolemenu", description="Hanya admin YugenX yang dapat mengirim perintah ini")
async def rolemenu(interaction: discord.Interaction):
    if interaction.user.id not in OWNER_IDS:
        await interaction.response.send_message("❌ Kamu kan bukan admin YugenX.", ephemeral=True)
        return

    embed = discord.Embed(
        title="Choose Your Roles",
        description="Klik menu dropdown di bawah untuk memilih role.\n\n🔱ras dewa\n😈ras iblis\n🐉ras naga\n\nYour Ping\n\n🎉giveaway ping\n🤝partnership ping\n🔔partnership event\n🌸pencinta anime\n🔥pencinta donghua\n📖pencinta komik\n🎤vocaloid lovers\n🎨art lovers\n👀pengamat server\n\nYour Games\n\n💥 Free Fire\n🔪 Mobile Legends\n🚪 PUBG\n📦 Roblox",
        color=discord.Color.blurple()
    )

    await interaction.response.send_message(embed=embed, view=RoleDropdownView())


# Jalankan bot
bot.run(TOKEN)
