"""
live_topstat_config.py

A plugin for HLL CRCON (see : https://github.com/MarechJ/hll_rcon_tool)
that displays and rewards top players

Source : https://github.com/ElGuillermo

Feel free to use/modify/distribute, as long as you keep this note in your code
"""

# Configuration (you should review/change these !)
# -----------------------------------------------------------------------------

# Translation
# Available : 0 english, 1 french, 2 german,
#             3 spanish, 4 polish, 5 brazilian portuguese,
#             6 russian, 7 chinese
LANG = 0

# Can be enabled/disabled on your different game servers
# ie : ["1"]           = enabled only on server 1
#      ["1", "2"]      = enabled on servers 1 and 2
#      ["2", "4", "5"] = enabled on servers 2, 4 and 5
ENABLE_ON_SERVERS = ["1"]

# Calling from chat
CHAT_COMMAND = "!top"

# Stats to display
# ----------------------------------------
# Define the stats to observe for each players and squads types
# (see all available stats in example config below)
# Parameters :
#   (players & squads) "limit"                : number of top players/squads to be listed
#   (players only)     "details" (True/False) : choose to display the (team/squad first letter) before the name of the player. ex : "(Axis/C) Playername"
#   (players only)     "vip"     (True/False) : choose to give a VIP to the first VIP_WINNERS players (configure this number below)
STATS_TO_DISPLAY = {
    "players": {
        "armycommander": [
            {"score": "player_teamplay", "limit": 2, "details": True, "vip": True},  # combat + support * SUPPORT_BONUS
        ],
        "infantry": [
            # {"score": "combat", "limit": 3, "details": True, "vip": False},
            # {"score": "offense", "limit": 3, "details": True, "vip": False},
            # {"score": "defense", "limit": 3, "details": True, "vip": False},
            # {"score": "defense_bonus", "limit": 3, "details": True, "vip": False},  # defense * DEFENSE_BONUS
            # {"score": "support", "limit": 3, "details": True, "vip": False},
            # {"score": "support_bonus", "limit": 3, "details": True, "vip": False},  # support * SUPPORT_BONUS
            # {"score": "kills", "limit": 3, "details": True, "vip": False},
            # {"score": "deaths", "limit": 3, "details": True, "vip": False},
            # {"score": "player_team_kills", "limit": 3, "details": True, "vip": False},
            # {"score": "player_vehicle_kills", "limit": 3, "details": True, "vip": False},
            # {"score": "player_vehicles_destroyed", "limit": 3, "details": True, "vip": False},
            {"score": "player_teamplay", "limit": 3, "details": True, "vip": True},  # combat + support * SUPPORT_BONUS
            {"score": "player_offdef", "limit": 3, "details": True, "vip": True},  # offense + defense * DEFENSE_BONUS
            {"score": "player_kd", "limit": 3, "details": True, "vip": False},  # kills / deaths
            {"score": "player_kpm", "limit": 3, "details": True, "vip": False}  # kills per minute
        ],
        "armor": [
            # add any stat using the templates above
        ],
        "artillery": [
            # add any stat using the templates above
        ],
        "recon": [
            # add any stat using the templates above
        ],
    },
    "squads": {
        "armycommander": [
            # Prefer using the "armycommander" part in "players"
        ],
        "infantry": [
            # {"score": "combat", "limit": 2},
            # {"score": "offense", "limit": 2},
            # {"score": "defense", "limit": 2},
            # {"score": "defense_bonus", "limit": 2},
            # {"score": "support", "limit": 2},
            # {"score": "support_bonus", "limit": 2},
            # {"score": "kills", "limit": 2},
            # {"score": "deaths", "limit": 2},
            # {"score": "squad_team_kills", "limit": 2},
            # {"score": "squad_vehicle_kills", "limit": 2},
            # {"score": "squad_vehicles_destroyed", "limit": 2},
            {"score": "squad_teamplay", "limit": 2},
            {"score": "squad_offdef", "limit": 2},
            # {"score": "squad_kd", "limit": 2},
            # {"score": "squad_kpm", "limit": 2},
        ],
        "armor": [
            {"score": "squad_teamplay", "limit": 2},
            {"score": "squad_vehicles_destroyed", "limit": 2},
        ],
        "artillery": [
            {"score": "squad_teamplay", "limit": 2}
        ],
        "recon": [
            {"score": "squad_teamplay", "limit": 2}
        ]
    }
}

# offdef defense bonus (offense + defense * bonus)
# ie : 1.5  = defense counts 1.5x more than offense (defense bonus)
#      1    = bonus disabled
#      0.67 = offense counts 1.5x more than defense (defense malus)
#      0.5  = offense counts 2x more than defense (defense malus)
#      0    = bonus disabled
# Any negative value will be converted to positive (ie : -1.5 -> 1.5)
DEFENSE_BONUS = 1.5

# teamplay support bonus (combat + support * bonus)
SUPPORT_BONUS = 1.5


# VIP (only given at the end of a game)
# ----------------------------------------

# Give VIP the best nth top players in each VIP-enabled subcategory ("armycommander", "infantry", "armor", "artillery", "recon") :
# 1 = gives a VIP to the top #1 player
# 2 = gives a VIP to the top #1 and #2 players
# 0 = disabled
VIP_WINNERS = 1

# Don't give a VIP to an "entered at last second" commander
VIP_COMMANDER_MIN_PLAYTIME_MINS = 20
VIP_COMMANDER_MIN_SUPPORT_SCORE = 1000

# VIPs will be given if there is at least this number of players ingame
# 0 to disable (VIP will always be given)
# Recommended : the same number as your seed limit
SEED_LIMIT = 40

# How many VIP hours awarded ?
# (If the player already has a VIP that ends AFTER this delay, VIP won't be given)
GRANTED_VIP_HOURS = 24

# VIP announce : local time
# ex : "Europe/Berlin", "Asia/Shanghai"
# Find you local timezone : https://utctime.info/timezone/
LOCAL_TIMEZONE = "Etc/UTC"


# Discord
# -------------------------------------

# Dedicated Discord's channel webhook
# (the script can run without any Discord output)
# Syntax : ["webhook url", enabled (True/False)]
DISCORD_CONFIG = [
    ["https://discord.com/api/webhooks/...", False],  # Server 1
    ["https://discord.com/api/webhooks/...", False],  # Server 2
    ["https://discord.com/api/webhooks/...", False],  # Server 3
    ["https://discord.com/api/webhooks/...", False],  # Server 4
    ["https://discord.com/api/webhooks/...", False],  # Server 5
    ["https://discord.com/api/webhooks/...", False],  # Server 6
    ["https://discord.com/api/webhooks/...", False],  # Server 7
    ["https://discord.com/api/webhooks/...", False],  # Server 8
    ["https://discord.com/api/webhooks/...", False],  # Server 9
    ["https://discord.com/api/webhooks/...", False]  # Server 10
    # (you can add lines if you manage more than 10 servers)
]


# Miscellaneous (you don't need to change these)
# -------------------------------------

# Discord : embed author icon
DISCORD_EMBED_AUTHOR_ICON_URL = "https://cdn.discordapp.com/icons/316459644476456962/73a28de670af9e6569f231c9385398f3.webp?size=64"

# Bot name that will be displayed in CRCON "audit logs" and Discord embeds
BOT_NAME = "custom_tools_live_topstats"


# (End of configuration)
# -----------------------------------------------------------------------------
