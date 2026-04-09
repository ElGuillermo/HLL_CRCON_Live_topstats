"""
live_topstats.py

A plugin for HLL CRCON (see : https://github.com/MarechJ/hll_rcon_tool)
that displays and rewards top players

Source : https://github.com/ElGuillermo

Feel free to use/modify/distribute, as long as you keep this note in your code
"""

# Configuration (you should review/change these !)
# -----------------------------------------------------------------------------

# Translations
# Available : 0 english, 1 french,  2 spanish,
#             3 german,  4 russian, 5 brazilian portuguese,
#             6 polish,  7 chinese
LANG = 0

# Can be enabled/disabled on your different game servers
# ie : ["1"]           = enabled only on server 1
#      ["1", "2"]      = enabled on servers 1 and 2
#      ["2", "4", "5"] = enabled on servers 2, 4 and 5
ENABLE_ON_SERVERS = ["1"]

# Calling from chat
CHAT_COMMAND = "!top"


# Stats to observe
# ----------------------------------------
# Define the stats to observe for each players and squads types
# (see all available stats in example config below)
# Parameters :
#   (players & squads) "limit"                : number of top players/squads to be listed
#   (players only)     "details" (True/False) : choose to display the (team/squad first letter) before the name of the player. ex : "(Axis/C) Playername"
#   (players only)     "vip"     (True/False) : choose to give a VIP to the first VIP_WINNERS players (configure this number below)
CONFIG = {
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

# Translations
# "key" : ["english", "french", "spanish", "german", "russian", "brazilian-portuguese", "polish", "chinese"]
TRANSL = {
    # Messages, logs and Discord embeds
    "gamejustended": ["Game just ended", "Partie terminée",
                      "El juego acaba de terminar", "Spiel beendet",
                      "Игра только что закончилась", "Jogo acabou",
                      "Gra właśnie się zakończyła", "游戏刚刚结束"],
    "nostatsyet": ["No stats yet", "Pas de stats",
                   "Aún no hay estadísticas", "noch keine Statistiken",
                   "Статистики пока нет", "Sem estatísticas ainda",
                   "Brak dostępnych statystyk", "暂无统计数据"],
    "top_players": ["top players", "top joueurs", "top jugadores", "top spieler",
                    "топ игроки", "top jogadores", "top gracze", "顶级玩家"],
    "top_squads": ["top squads", "top escouades", "top patrullas", "top trupps",
                   "топ отряды", "top esquadrões", "top składy", "顶级小队"],

    # VIP ingame message
    "vip_header": ["You are in the topstats!", "Tu es dans les topstats !",
                   "¡Estás en los topstats!", "Du bist in den Topstats!",
                   "Вы попали в топ-стат!", "Você está nos topstats!",
                   "Jesteś w topstats!", "你已进入 顶级统计！"],
    "already_vip": ["Already VIP !", "Déjà VIP !", "¡Ya es VIP!", "bereits VIP !",
                    "Уже VIP!", "Já é VIP!", "Aktualnie ma VIPa!", "已经是VIP！"],
    "vip_won": ["You won a VIP until", "Tu as gagné un VIP jusqu'au",
                "Has ganado un VIP hasta el", "Du hast ein VIP gewonnen bis",
                "Вы выиграли VIP до", "Você ganhou um VIP até",
                "Wygrałeś VIP do", "你赢得了VIP，有效期至"],
    "vip_at": ["at", "à", "a las", "um",
               "в", "às", "do godziny", "于"],

    # Teams
    "allies": ["allies", "alliés", "aliados", "allierte",
               "союзники", "aliados", "alianci", "盟军"],
    "axis": ["axis", "axe", "eje", "achsenmächte",
             "ось", "eixo", "oś", "轴心"],

    # Units types
    "armycommander": ["commander", "commandant", "comandante", "kommandant",
                      "командующий", "comandante", "dowódca", "指挥官"],
    "infantry": ["infantry", "infanterie", "infantería", "infanterie",
                 "пехота", "infantaria", "piechota", "步兵"],
    "armor": ["armor", "blindés", "blindados", "panzer",
              "танки", "blindados", "czołgi", "装甲"],
    "artillery": ["artillery", "artillerie", "artillería", "artillerie",
                  "артиллерия", "artilharia", "artyleria", "火炮"],
    "recon": ["recon", "reconnaissance", "reconocimiento", "aufklärer",
              "разведка", "reconhecimento", "zwiad", "侦察"],

    "armycommander_short": ["cmd", "cdt", "cde", "kdt", "ком", "cmt", "dow", "指挥官"],
    # "infantry_short": ["inf", "inf", "inf", "inf", "пех", "inf", "pie", "步兵"],
    # "armor_short": ["arm", "bli", "bli", "pz", "тнк", "bli", "czo", "装甲"],
    # "artillery_short": ["art", "art", "art", "art", "арт", "art", "art", "火炮"],
    # "recon_short": ["rec", "rec", "rec", "aufk", "разв", "rec", "zwi", "侦察"],

    # Stats names (keys must match those in SCORE_FUNCTIONS)
    "combat": ["cmb", "cmb", "cmb", "kpf", "бой", "cmb", "wal", "战斗"],
    "offense": ["off", "off", "off", "ang", "атк", "off", "ofe", "进攻"],
    "defense": ["def", "def", "def", "ver", "обр", "def", "def", "防守"],
    "support": ["sup", "sou", "apo", "unt", "под", "sup", "wsp", "支援"],
    "kills": ["kills", "kills", "bajas", "kills", "уб.", "abates", "zab.", "击杀"],
    "deaths": ["deaths", "morts", "muertes", "tode", "см.", "mortes", "zgony", "死亡"],
    # (keys below will be used for any "player_<key>" or "squad_<key>")
    "team_kills": ["TK", "TK", "TK", "TK", "ТК", "TK", "TK", "队友击杀"],
    "vehicle_kills": ["v.kills", "kills/véhic", "bajas/veh", "fzg.kills", "уб. тех.", "abates/veí", "zab. poj.", "载具击杀"],
    "vehicles_destroyed": ["v.destr", "véhic.détru", "veh.destr.", "fzg.zen", "техн. унич", "veí.destru", "poj.znisz", "载具销毁"],
    "teamplay": ["cmb+sup", "cmb+sup", "cmb+sup", "kpf+unt", "бой+под", "cmb+sup", "wal+wsp", "团队配合"],
    "offdef": ["off+def", "off+def", "off+def", "off+def", "атк+обр", "off+def", "off+def", "攻防比"],
    "kd": ["kills/deaths", "kills/morts", "kills/deaths", "kills/tode", "уб./см.", "kills/mortes", "zab./zgony", "KD比"],
    "kpm": ["kills/min", "kills/min", "bajas/min", "kills/min", "уб./мин", "abates/min", "zab./min", "击杀/分"],
}

# Discord : embed author icon
DISCORD_EMBED_AUTHOR_ICON_URL = "https://cdn.discordapp.com/icons/316459644476456962/73a28de670af9e6569f231c9385398f3.webp?size=64"

# Bot name that will be displayed in CRCON "audit logs" and Discord embeds
BOT_NAME = "custom_tools_live_topstats"


# (End of configuration)
# -----------------------------------------------------------------------------

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import logging
import discord
from rcon.rcon import Rcon, StructuredLogLineWithMetaData
from rcon.user_config.rcon_server_settings import RconServerSettingsUserConfig
from rcon.utils import get_server_number


# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.DEBUG)


# Clan related (as set in /settings/rcon-server)
try:
    config = RconServerSettingsUserConfig.load_from_db()
    DISCORD_EMBED_AUTHOR_URL = str(config.server_url)
except Exception as error:
    logger.error("Could not retrieve DISCORD_EMBED_AUTHOR_URL from database : %s", error)
    DISCORD_EMBED_AUTHOR_URL = ""


def clean_bonus(value, name="BONUS") -> float:
    """
    Clean and validate the bonus value.
    Accepts int, float, or numeric str.
    Returns abs(value) if non-zero, otherwise 1.0 (no bonus).
    """
    # value is a number
    if isinstance(value, (int, float)):
        return abs(value) if value != 0 else 1.0

    # value may be a string
    if value is not None:
        # trying to convert to float
        try:
            converted = float(value)
            return abs(converted) if converted != 0 else 1.0

        # value couldn't be converted
        except (ValueError, TypeError):
            logger.warning(
                f"{name} has an invalid value or type ({type(value).__name__}: {value}). "
                "Falling back to default value: 1.0"
            )

    # Default fallback value (no bonus)
    return 1.0


def is_vip_for_less_than_xh(rcon: Rcon, player_id: str, vip_delay_hours: int) -> bool:
    """
    returns
    'true' if player has no VIP or a VIP that expires in less than vip_delay_hours,
    'false' if he has a VIP that expires in more than vip_delay_hours or no VIP at all.
    """
    # Get the VIP list
    try:
        actual_vips = rcon.get_vip_ids()
    except Exception as error:
        logger.error("Can't get the VIP list : %s", error)
        return False  # Consider the player as a VIP by default (giving a VIP could erase an actual -larger- VIP)

    # Check each VIP lease
    for item in actual_vips:
        if item['player_id'] == player_id and item['vip_expiration'] is not None:
            vip_expiration_output = str(item['vip_expiration'])
            vip_expiration = datetime.fromisoformat(vip_expiration_output)

            # VIP will expire in less than vip_delay_hours
            if vip_expiration < datetime.now(timezone.utc) + timedelta(hours=vip_delay_hours):
                return True

            # VIP won't expire in less than vip_delay_hours
            return False

    return True  # Player isn't in the VIP list


def give_xh_vip(rcon: Rcon, player_id: str, player_name: str, hours_awarded: int):
    """
    Gives a X hour(s) VIP
    returns a fully formatted and localized message.
    """
    combined_name = f"{player_name} (top player)"

    # Gives X hours VIP
    expiration_dt = datetime.now(timezone.utc) + timedelta(hours=hours_awarded)
    rcon.add_vip(player_id, combined_name, expiration_dt.strftime('%Y-%m-%dT%H:%M:%SZ'))

    # Local timezone
    local_tz = ZoneInfo(LOCAL_TIMEZONE)
    local_dt = expiration_dt.astimezone(local_tz)

    # Message building
    header = TRANSL['vip_header'][LANG]       # "You are in the topstats!"
    won_text = TRANSL['vip_won'][LANG]        # "You won a VIP until"
    date_str = local_dt.strftime('%d/%m/%Y')  # "01/01/2001"
    at_text = TRANSL['vip_at'][LANG]          # "at"
    time_str = local_dt.strftime('%Hh%M')     # "12h00"

    return f"{header}\n\n{won_text}\n{date_str}, {at_text} {time_str} !"


def get_player_teamplay(player: dict) -> int:
    """
    Calculates the teamplay score using combat and support stats.
    Formula: combat + (support * SUPPORT_BONUS)
    """
    combat = int(player.get("combat", 0))
    support = int(player.get("support", 0))
    support_bonus = clean_bonus(SUPPORT_BONUS, "SUPPORT_BONUS")

    return int(round(combat + (support * support_bonus)))


def get_player_offdef(player: dict) -> int:
    """
    Calculates the combined offense and defense score.
    Formula: offense + (defense * DEFENSE_BONUS)
    """
    offense = int(player.get("offense", 0))
    defense = int(player.get("defense", 0))
    defense_bonus = clean_bonus(DEFENSE_BONUS, "DEFENSE_BONUS")

    return int(round(offense + (defense * defense_bonus)))


def get_player_kd(player: dict) -> float:
    """
    Calculates the kills/deaths ratio.
    If deaths are 0, the ratio equals the number of kills.
    """
    kills = int(player.get("kills", 0))
    deaths = int(player.get("deaths", 0))

    if deaths == 0:
        return float(kills)

    return round(kills / deaths, 2)


def get_player_kpm(player: dict) -> float:
    """
    Calculates the kills per minute (KPM).
    Requires at least 1 minute of play to avoid aberrant ratios.
    """
    playtime_seconds = int(player.get("map_playtime_seconds", 0))

    # Player must have played > 5 mins
    if playtime_seconds < 300:
        return 0.0

    kills = int(player.get("kills", 0))
    if kills == 0:
        return 0.0

    playtime_min = playtime_seconds / 60

    return round(kills / playtime_min, 2)


def get_player_ranking(rcon: Rcon, server_status, api_data: dict, unit_type: str, score_func, limit: int = 3, mention_details: bool = False, give_vip: bool = False) -> list:
    """
    Extracts, ranks, and optionally triggers VIP rewards.
    """
    players_stats = []
    result = api_data.get("result", api_data)

    for side in ["allies", "axis"]:
        team_data = result.get(side, {})

        # Commander
        if unit_type == "armycommander":
            cmd = team_data.get("commander")
            if cmd:
                score = score_func(cmd)
                if score and score > 0:
                    name = cmd["name"]
                    if mention_details:
                        name = f"({TRANSL[side][LANG].capitalize()}/{TRANSL['armycommander_short'][LANG].capitalize()}) {name}"
                    players_stats.append({
                        "name": name,
                        "score": score,
                        "player_id": cmd.get("player_id"),
                        "raw_data": cmd  # Allows checkings in VIP part
                    })

        # Squads
        else:
            squads = team_data.get("squads", {})
            for s_name, s_info in squads.items():
                if s_name != "unassigned" and str(s_info.get("type")).lower() == unit_type.lower():
                    for p in s_info.get("players", []):
                        score = score_func(p)
                        if score and score > 0:
                            name = p["name"]
                            if mention_details:
                                name = f"({TRANSL[side][LANG].capitalize()}/{s_name[0].upper()}) {name}"
                            players_stats.append({
                                "name": name,
                                "score": score,
                                "player_id": p.get("player_id"),
                                "raw_data": p  # Allows checkings in VIP part
                            })

    players_stats.sort(key=lambda x: x["score"], reverse=True)

    # VIP
    if give_vip and server_status["current_players"] >= SEED_LIMIT:

        winners = players_stats[:VIP_WINNERS]
        granted_vip_hours = GRANTED_VIP_HOURS if GRANTED_VIP_HOURS > 0 else 24

        for player in winners:
            raw = player['raw_data']

            # No VIP for "entered at last second" commander
            if (
                raw.get('role') == "armycommander"
                and (
                    (int(raw.get('offense', 0)) + int(raw.get('defense', 0))) / 20 < VIP_COMMANDER_MIN_PLAYTIME_MINS
                    or int(raw.get('support', 0)) < VIP_COMMANDER_MIN_SUPPORT_SCORE
                )
            ):
                continue  # Player won't receive any message

            # Only give VIP if the player has either :
            # - no VIP at all
            # - a VIP that ends in less than granted_vip_hours
            if is_vip_for_less_than_xh(rcon, player['player_id'], granted_vip_hours):
                vip_message = give_xh_vip(rcon, player['player_id'], player['name'], granted_vip_hours)
            else:
                vip_message = f"{TRANSL['vip_header'][LANG]}\n\n{TRANSL['already_vip'][LANG]}\n"

            try:
                rcon.message_player(
                    player_id=player['player_id'],
                    message=vip_message,
                    by="custom_tools_live_topstats",
                    save_message=False
                )
            except Exception as error:
                logger.error("Ingame VIP message_player couldn't be sent : %s", error)

    # Output list
    formatted_list = []
    for p in players_stats[:limit]:
        score_val = f"{p['score']:.1f}" if isinstance(p['score'], float) else str(p['score'])
        formatted_list.append(f"{p['name']} : {score_val}")

    return formatted_list


def get_squad_teamplay(squad: dict) -> int:
    """
    Calculates combined teamplay score for a whole squad.
    Formula: combat + (support * SUPPORT_BONUS)
    """
    combat = int(squad.get("combat", 0))
    support = int(squad.get("support", 0))
    support_bonus = clean_bonus(SUPPORT_BONUS, "SUPPORT_BONUS")

    return int(round(combat + (support * support_bonus)))


def get_squad_offdef(squad: dict) -> int:
    """
    Calculates combined off/def score for a whole squad.
    Formula: offense + (defense * DEFENSE_BONUS)
    """
    offense = int(squad.get("offense", 0))
    defense = int(squad.get("defense", 0))
    defense_bonus = clean_bonus(DEFENSE_BONUS, "DEFENSE_BONUS")

    return int(round(offense + (defense * defense_bonus)))


def get_squad_kd(squad: dict) -> float:
    """
    Calculates the cumulative K/D ratio of all players in the squad.
    """
    players = squad.get("players", [])
    if not players:
        return 0.0

    total_kills = sum(int(p.get("kills", 0)) for p in players)
    total_deaths = sum(int(p.get("deaths", 0)) for p in players)

    if total_deaths == 0:
        return float(total_kills)

    return round(total_kills / total_deaths, 2)


def get_squad_kpm(squad: dict) -> float:
    """
    Calculates the squad kills/min based on cumulative kills.
    Requires at least 10 minutes of cumulated playtime to avoid aberrant ratios.
    """
    players = squad.get("players", [])
    if not players:
        return 0.0

    total_playtime_sec = sum(int(p.get("map_playtime_seconds", 0)) for p in players)
    # Players must have 10 min cumulated playtime
    if total_playtime_sec < 600:
        return 0.0

    total_kills = sum(int(p.get("kills", 0)) for p in players)
    if total_kills == 0:
        return 0.0

    kpm = total_kills / (total_playtime_sec / 60)

    return round(kpm, 2)


def get_squad_vehicles_destroyed(squad: dict) -> int:
    """
    Calculates combined vehicles_destroyed for a whole squad.
    """
    players = squad.get("players", [])
    if not players:
        return 0

    total_vehicles_destroyed = sum(int(p.get("vehicles_destroyed", 0)) for p in players)
    if total_vehicles_destroyed == 0:
        return 0

    return total_vehicles_destroyed


def get_squad_team_kills(squad: dict) -> int:
    """
    Calculates combined team_kills for a whole squad.
    """
    players = squad.get("players", [])
    if not players:
        return 0

    total_tks = sum(int(p.get("team_kills", 0)) for p in players)
    if total_tks == 0:
        return 0

    return total_tks


def get_squad_vehicle_kills(squad: dict) -> int:
    """
    Calculates combined vehicle_kills for a whole squad.
    """
    players = squad.get("players", [])
    if not players:
        return 0

    total_vehicle_kills = sum(int(p.get("vehicle_kills", 0)) for p in players)
    if total_vehicle_kills == 0:
        return 0

    return total_vehicle_kills


def get_squad_ranking(api_data: dict, unit_type: str, score_func, limit: int = 3) -> list:
    """
    Ranks squads or the Commander unit.
    """
    squads_stats = []
    result = api_data.get("result", api_data)

    for side in ["allies", "axis"]:
        team_data = result.get(side, {})

        # Commander
        if unit_type == "armycommander":
            cmd = team_data.get("commander")
            if cmd:
                # Harmonizing data structure : create an "armycommander" squad subtree
                fake_squad = {
                    "type": "armycommander",
                    "players": [cmd],
                    "offense": cmd.get("offense", 0),
                    "defense": cmd.get("defense", 0),
                    "combat": cmd.get("combat", 0),
                    "support": cmd.get("support", 0)
                }
                score = score_func(fake_squad)
                squads_stats.append({"name": f"{TRANSL[side][LANG].capitalize()}/{TRANSL['armycommander_short'][LANG].capitalize()}", "score": score})

        # Squads
        else:
            squads = team_data.get("squads", {})
            for s_name, s_info in squads.items():
                if s_name != "unassigned" and str(s_info.get("type")).lower() == unit_type.lower():
                    score = score_func(s_info)
                    if score and score > 0:
                        name = f"{TRANSL[side][LANG].capitalize()}/{s_name[0].upper()}"  # Axe/A
                        squads_stats.append({
                            "name": name,
                            "score": score
                        })

    squads_stats.sort(key=lambda x: x["score"], reverse=True)

    # Output list
    formatted_list = []
    for s in squads_stats[:limit]:
        score_val = f"{s['score']:.1f}" if isinstance(s['score'], float) else str(s['score'])
        formatted_list.append(f"{s['name']} : {score_val}")

    return formatted_list


# Functions mapping (must be declared AFTER the functions definitions)
SCORE_FUNCTIONS = {
    # (players and squads)
    # No need to create a dedicated function, as the stat is directly available from the 'get_team_view' endpoint
    "combat": lambda p: int(p.get("combat", 0)),
    "offense": lambda p: int(p.get("offense", 0)),
    "defense": lambda p: int(p.get("defense", 0)),
    "support": lambda p: int(p.get("support", 0)),
    "kills": lambda p: int(p.get("kills", 0)),
    "deaths": lambda p: int(p.get("deaths", 0)),
    # Directly calculated (no dedicated function)
    "defense_bonus": lambda p: int(int(p.get("defense", 0)) * clean_bonus(DEFENSE_BONUS, "DEFENSE_BONUS")),
    "support_bonus": lambda p: int(int(p.get("support", 0)) * clean_bonus(SUPPORT_BONUS, "SUPPORT_BONUS")),

    # (players)
    # No need to create a dedicated function, as the stat is directly available from the 'get_team_view' endpoint
    "player_team_kills": lambda p: int(p.get("team_kills", 0)),
    "player_vehicle_kills": lambda p: int(p.get("vehicle_kills", 0)),
    "player_vehicles_destroyed": lambda p: int(p.get("vehicles_destroyed", 0)),
    # These are calculated stats, provided by dedicated functions
    "player_teamplay": get_player_teamplay,                    # combat + support * support_bonus
    "player_offdef": get_player_offdef,                        # offense + defense * defense bonus
    "player_kd": get_player_kd,                                # kills / deaths
    "player_kpm": get_player_kpm,                              # kills / minute

    # (squads)
    # These are calculated stats, provided by dedicated functions
    "squad_team_kills": get_squad_team_kills,                  # cumulated team_kills
    "squad_vehicle_kills": get_squad_vehicle_kills,            # cumulated vehicle_kills
    "squad_vehicles_destroyed": get_squad_vehicles_destroyed,  # cumulated vehicles_destroyed
    "squad_teamplay": get_squad_teamplay,                      # combat + support * support_bonus
    "squad_offdef": get_squad_offdef,                          # offense + defense * defense bonus
    "squad_kd": get_squad_kd,                                  # kills / deaths
    "squad_kpm": get_squad_kpm,                                # kills / minute
}


def generate_full_report(rcon, api_data, config, is_match_end: bool = False):
    server_status = rcon.get_status()
    report_sections = []

    def process_config_category(category_key, fetch_func, main_header_key):
        cfg = config.get(category_key, {})
        category_header_added = False

        for unit_type, rankings in cfg.items():
            unit_header_added = False

            for r in rankings:
                should_grant = is_match_end and r.get("vip", False) if category_key == "players" else False

                if category_key == "players":
                    results = fetch_func(rcon, server_status, api_data, unit_type, SCORE_FUNCTIONS[r["score"]], r["limit"], r.get("details", False), should_grant)
                else:
                    results = fetch_func(api_data, unit_type, SCORE_FUNCTIONS[r["score"]], r["limit"])

                if results:
                    # "——— TOP PLAYERS ———"
                    if not category_header_added:
                        report_sections.append(f"——— {TRANSL[main_header_key][LANG].upper()} ———")
                        category_header_added = True

                    # "— INFANTRY —"
                    if not unit_header_added:
                        unit_name = TRANSL.get(unit_type.lower(), [unit_type])[LANG].upper()
                        report_sections.append(f"— {unit_name} —")
                        unit_header_added = True

                    # stat function name translation
                    # ex. "player_teamplay" or "squad_teamplay" -> use [TRANSL]["teamplay"] -> "cmb+sup"
                    raw_score_key = r['score'].lower()
                    clean_key = raw_score_key.removeprefix("player_").removeprefix("squad_")
                    translations = TRANSL.get(clean_key)
                    translated_score = translations[LANG].lower() if translations else raw_score_key

                    # Stat header
                    header = f"▒ TOP {r['limit']} ({translated_score})"

                    # Add stat section
                    report_sections.append(f"{header}\n" + "\n".join(results))

    process_config_category("players", get_player_ranking, "top_players")
    process_config_category("squads", get_squad_ranking, "top_squads")

    return "\n\n".join(report_sections)


def stats_on_chat_command(
    rcon: Rcon,
    struct_log: StructuredLogLineWithMetaData
):
    """
    Message actual top scores to the player who types the defined command in chat
    """
    # Check if script is enabled on actual server
    server_number = get_server_number()
    if server_number not in ENABLE_ON_SERVERS:
        return

    # Check log for mandatory variable
    chat_message: str|None = struct_log["sub_content"]
    if chat_message is None:
        return

    if chat_message == CHAT_COMMAND:

        # Check log for mandatory variable
        player_id: str|None = struct_log["player_id_1"]
        if player_id is None:
            return

        # Get data from RCON
        get_team_view: dict = rcon.get_team_view()

        # Process data
        report = generate_full_report(rcon, get_team_view, CONFIG, is_match_end=False)

        # Ingame message
        if not report:
            message = f"{TRANSL['nostatsyet'][LANG]}"
        else:
            message = f"{report}"

        try:
            rcon.message_player(
                player_id=player_id,
                message=message,
                by="custom_tools_live_topstats",
                save_message=False
            )
        except Exception as error:
            logger.error("Ingame message_player couldn't be sent : %s", error)


def stats_on_match_end(
    rcon: Rcon,
    struct_log: StructuredLogLineWithMetaData
):
    """
    Sends final top players in an ingame message to all the players
    Gives VIP to the top players as configured
    """
    # Check if script is enabled on actual server
    server_number = get_server_number()
    if server_number not in ENABLE_ON_SERVERS:
        return

    # Get data from RCON
    get_team_view: dict = rcon.get_team_view()

    # Process data
    report = generate_full_report(rcon, get_team_view, CONFIG, is_match_end=True)  # is_match_end=True enables VIP granting

    # Prepare ingame message and logs
    if not report:
        message = f"{TRANSL['nostatsyet'][LANG]}"
    else:
        message = f"{report}"

    # logs
    logger.info(f"{'-' * 79}\n{message}")

    # Ingame message (only if available stats)
    if report:
        try:
            rcon.message_all_players(message=message)
        except Exception as error:
            logger.error("Ingame message_all_players couldn't be sent : %s", error)

    # Discord
    server_number = int(get_server_number())
    if not DISCORD_CONFIG[server_number - 1][1]:
        return

    discord_webhook = DISCORD_CONFIG[server_number - 1][0]

    webhook = discord.SyncWebhook.from_url(discord_webhook)

    embed = discord.Embed(
        title=TRANSL['gamejustended'][LANG],
        url="",
        description=message,
        color=0xffffff
    )

    embed.set_author(
        name=BOT_NAME,
        url=DISCORD_EMBED_AUTHOR_URL,
        icon_url=DISCORD_EMBED_AUTHOR_ICON_URL
    )

    embeds = []
    embeds.append(embed)

    try:
        webhook.send(embeds=embeds, wait=True)
    except Exception as error:
        logger.error("Discord embed couldn't be sent : %s", error)
