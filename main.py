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

# ─────────────────────────────────────────────────────────────
# 1. Semua grup role disimpan di dict → {option_value: [ID, …]}
# ─────────────────────────────────────────────────────────────
ROLE_GROUPS = {
    # dropdown “ras”
    "ras_dewa":        [1382008246327312424],
    "ras_iblis":       [1382008643326574622],
    "ras_naga":        [1382010013144322128],
    "ras_elemental":   [1385923115929833522],
    "ras_dwarf":       [1385922167685775401],
    "ras_human":       [1385921921677266995],

    # dropdown “ping”
    "giveaway_ping":   [1383027202970484766],
    "partnership_ping":[1383012056353210488],
    "partnership_evt": [1383671901699702864],
    "promosi_ping":    [1383366844450082817],
    "misteri_ping":    [1387340859946569808],

    # dropdown “hobi”
    "anime":           [1381930147833315398],
    "donghua":         [1381930494316515411],
    "komik":           [1381931492518662214],
    "game": [                     # <─ Pencinta Game → 4-5 role sekaligus
        1383003121416011866,
        1383003591614140477,
        1383003667178852494,
        1383003734552084531,
        1382010013144322128,      # contoh: role “gamer” umum
    ],
    "musik":           [1381931995373768744],
    "gambar":          [1381932371787386920],
    "observer":        [1381932623353610240],
}

# ─────────────────────────────────────────────────────────────
# 2. Helper dropdown generik
# ─────────────────────────────────────────────────────────────
class GenericRoleDropdown(discord.ui.Select):
    def __init__(self, placeholder: str, option_pairs: list[tuple[str, str, str | None]]):
        """option_pairs: list[(label, value, emoji)]"""
        opts = [
            discord.SelectOption(label=lab, value=val, emoji=emo)
            for lab, val, emo in option_pairs
        ]
        super().__init__(placeholder=placeholder, options=opts, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        key = self.values[0]                          # mis. "game"
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

# ─────────────────────────────────────────────────────────────
# 3. View berisi 3 dropdown
# ─────────────────────────────────────────────────────────────
class RoleMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(GenericRoleDropdown(
            "Pilih ras-mu…",
            [
                ("🔱 ras dewa",       "ras_dewa",       None),
                ("😈 ras iblis",      "ras_iblis",      None),
                ("🐉 ras naga",       "ras_naga",       None),
                ("💨 ras elemental",  "ras_elemental",  None),
                ("⛏️ ras dwarf",      "ras_dwarf",      None),
                ("🧑‍🦲 ras human",    "ras_human",      None),
            ]))

        self.add_item(GenericRoleDropdown(
            "Pilih ping…",
            [
                ("🎉 giveaway ping",       "giveaway_ping",    None),
                ("🤝 partnership ping",    "partnership_ping", None),
                ("🔔 partnership event",   "partnership_evt",  None),
                ("📣 promosi ping",        "promosi_ping",     None),
                ("❓ misteri ping",        "misteri_ping",     None),
            ]))

        self.add_item(GenericRoleDropdown(
            "Pilih hobi…",
            [
                ("🌸 pencinta anime",   "anime",    None),
                ("🔥 pencinta donghua", "donghua",  None),
                ("📖 pencinta komik",   "komik",    None),
                ("🎮 pencinta game",    "game",     None),  # ← Banyak role
                ("🎧 pencinta musik",   "musik",    None),
                ("🎨 pencinta gambar",  "gambar",   None),
                ("👀 pengamat server",  "observer", None),
            ]))

# ─────────────────────────────────────────────────────────────
# 4. Slash command /rolemenu
# ─────────────────────────────────────────────────────────────
@bot.tree.command(name="rolemenu", description="Kirim menu role")
async def rolemenu_cmd(interaction: discord.Interaction):
    if interaction.user.id not in OWNER_IDS:
        await interaction.response.send_message("❌ Kamu bukan admin.", ephemeral=True)
        return

    embed = discord.Embed(
        title="Self-Assign Roles",
        description="Klik dropdown di bawah untuk memilih role. "
                    "\n• Satu klik langsung menambah semua role yang terkait.",
        color=discord.Color.blurple()
    )
    await interaction.response.send_message(embed=embed, view=RoleMenuView())

# ─────────────────────────────────────────────────────────────
bot.run(TOKEN)
