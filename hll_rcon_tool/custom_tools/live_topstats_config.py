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

# Display on matchend ?
DISPLAY_ON_MATCHEND = True

# Chat command
CHAT_COMMAND = "!top"

# Stats to display
# ----------------------------------------
# Define the stats to observe for each players and squads types
#   (see all available stats in example config below)
# Parameters :
#   (players & squads) "display"              : number of top players/squads to be listed
#   (players only)     "details" (True/False) : choose to display the (team/squad first letter) before the name of the player. ex : "(Axis/C) Playername"
#   (players only)     "vip_winners"          : give a VIP to this number of top players (up to 'display' number above)
STATS_TO_DISPLAY = {
    "players": {
        "armycommander": [
            {"score": "player_teamplay", "display": 2, "details": True, "vip_winners": 1},             # combat + support * SUPPORT_BONUS
        ],
        "infantry": [
            # {"score": "combat", "display": 3, "details": True, "vip_winners": 0},
            # {"score": "offense", "display": 3, "details": True, "vip_winners": 0},
            # {"score": "defense", "display": 3, "details": True, "vip_winners": 0},
            # {"score": "defense_bonus", "display": 3, "details": True, "vip_winners": 0},             # defense * DEFENSE_BONUS
            # {"score": "support", "display": 3, "details": True, "vip_winners": 0},
            # {"score": "support_bonus", "display": 3, "details": True, "vip_winners": 0},             # support * SUPPORT_BONUS
            # {"score": "kills", "display": 3, "details": True, "vip_winners": 0},
            # {"score": "deaths", "display": 3, "details": True, "vip_winners": 0},
            # {"score": "player_team_kills", "display": 3, "details": True, "vip_winners": 0},
            # {"score": "player_vehicle_kills", "display": 3, "details": True, "vip_winners": 0},
            # {"score": "player_vehicles_destroyed", "display": 3, "details": True, "vip_winners": 0},
            {"score": "player_teamplay", "display": 3, "details": True, "vip_winners": 3},             # combat + support * SUPPORT_BONUS
            {"score": "player_offdef", "display": 3, "details": True, "vip_winners": 3},               # offense + defense * DEFENSE_BONUS
            {"score": "player_kd", "display": 3, "details": True, "vip_winners": 0},                   # kills / deaths
            {"score": "player_kpm", "display": 3, "details": True, "vip_winners": 0}                   # kills per minute
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
            # {"score": "combat", "display": 2},
            # {"score": "offense", "display": 2},
            # {"score": "defense", "display": 2},
            # {"score": "defense_bonus", "display": 2},
            # {"score": "support", "display": 2},
            # {"score": "support_bonus", "display": 2},
            # {"score": "kills", "display": 2},
            # {"score": "deaths", "display": 2},
            # {"score": "squad_team_kills", "display": 2},
            # {"score": "squad_vehicle_kills", "display": 2},
            # {"score": "squad_vehicles_destroyed", "display": 2},
            {"score": "squad_teamplay", "display": 2},
            {"score": "squad_offdef", "display": 2},
            # {"score": "squad_kd", "display": 2},
            # {"score": "squad_kpm", "display": 2},
        ],
        "armor": [
            {"score": "squad_teamplay", "display": 2},
            {"score": "squad_vehicles_destroyed", "display": 2},
        ],
        "artillery": [
            {"score": "squad_teamplay", "display": 2}
        ],
        "recon": [
            {"score": "squad_teamplay", "display": 2}
        ]
    }
}

# offdef defense bonus (offense + defense * bonus)
# ie : 1.5  = defense counts 1.5x more than offense (defense bonus)
#      1    = bonus disabled
#      0.67 = offense counts 1.5x more than defense (defense malus)
#      0.5  = offense counts 2x more than defense (defense malus)
#      0    = bonus disabled
# Any negative value will be considered as positive (ie : -1.5 -> 1.5)
DEFENSE_BONUS = 1.5

# teamplay support bonus (combat + support * bonus)
SUPPORT_BONUS = 1.5


# VIP (only given to players at the end of a game)
# ----------------------------------------

# Don't give a VIP to an "entered at last second" commander
VIP_COMMANDER_MIN_PLAYTIME_MINS = 20
VIP_COMMANDER_MIN_SUPPORT_SCORE = 1000

# Give VIP if there is at least this number of players ingame
# 0 = disabled (VIP will always be given)
# Recommended : the same number as your seed limit
SEED_LIMIT = 40

# How many VIP hours should be given ?
# (If the player already has a VIP that ends AFTER this delay, VIP won't be given)
GRANTED_VIP_HOURS = 24

# VIP message : local time in expiration date/hour
# Find you local timezone : https://utctime.info/timezone/
# ie : "Europe/Berlin"
#      "Asia/Shanghai"
# default : "Etc/UTC"
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
