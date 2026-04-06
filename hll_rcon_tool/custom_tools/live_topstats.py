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
# ----------------------------------------

CHAT_COMMAND = "!top"


# Stats to observe
# ----------------------------------------
# Define the stats to observe for each player and squad type
# Available main categories :
#   "players", "squads"
# Available subcategories :
#       "command", "infantry", "armor", "artillery", "recon"
# Available combined stats in subcategories :
#           "teamplay" (combat score + support score * support bonus)
#           "offdef"   (offense score + defense score * defense bonus)
#           "kd"       (kills/deaths ratio)
#           "killrate" (kills/minute)
# Where :
#   (players & squads) "limit"                : number of top players/squads to be listed
#   (players only)     "details" (True/False) : choose to display the (team/squad first letter) before the name of the player. ex : "(Axis/C) Playername"
#   (players only)     "vip"     (True/False) : choose to give a VIP to the first VIP_WINNERS (see below) players
CONFIG = {
    "players": {
        "command": [
            {"score": "teamplay", "limit": 1, "details": True, "vip": True}
        ],
        "infantry": [
            # {"score": "combat", "limit": 3, "details": True, "vip": False},
            # {"score": "offense", "limit": 3, "details": True, "vip": False},
            # {"score": "defense", "limit": 3, "details": True, "vip": False},
            # {"score": "support", "limit": 3, "details": True, "vip": False},
            # {"score": "kills", "limit": 3, "details": True, "vip": False},
            # {"score": "deaths", "limit": 3, "details": True, "vip": False},
            # {"score": "team_kills", "limit": 3, "details": True, "vip": False},
            # {"score": "vehicle_kills", "limit": 3, "details": True, "vip": False},
            # {"score": "vehicles_destroyed", "limit": 3, "details": True, "vip": False},
            {"score": "teamplay", "limit": 3, "details": True, "vip": True},
            {"score": "offdef", "limit": 3, "details": True, "vip": True},
            {"score": "kd", "limit": 3, "details": True, "vip": False},
            {"score": "killrate", "limit": 3, "details": True, "vip": False}
        ]
    },
    "squads": {
        "infantry": [
            {"score": "squad_teamplay", "limit": 3},
            {"score": "squad_offdef", "limit": 3}
        ],
        "armor": [
            {"score": "squad_teamplay", "limit": 3},
            {"score": "squad_offdef", "limit": 3}
        ],
        "artillery": [
            {"score": "squad_teamplay", "limit": 3}
        ],
        "recon": [
            {"score": "squad_teamplay", "limit": 3}
        ]
    }
}

# Offense + defense score (offense + defense * bonus)
# ie : 1.5  = defense counts 1.5x more than offense (defense bonus)
#      1    = bonus disabled
#      0.67 = offense counts 1.5x more than defense (defense malus)
#      0.5  = offense counts 2x more than defense (defense malus)
#      0    = bonus disabled
# Any negative value will be converted to positive (ie : -1.5 -> 1.5)
DEFENSE_BONUS = 1.75

# Teamplay (combat + support) score (combat + support * bonus)
SUPPORT_BONUS = 1.75


# VIP (only given at the end of a game)
# ----------------------------------------

# Give VIP the best nth top players in each VIP-enabled subcategory ("command", "infantry", "armor", "artillery", "recon") :
# 1 = gives a VIP to the top #1 player
# 2 = gives a VIP to the top #1 and #2 players
# 0 = disabled
VIP_WINNERS = 1

# Avoid to give a VIP to a "entered at last second" commander
VIP_COMMANDER_MIN_PLAYTIME_MINS = 20
VIP_COMMANDER_MIN_SUPPORT_SCORE = 1000

# VIPs will be given if there is at least this number of players ingame
# 0 to disable (VIP will always be given)
# Recommended : the same number as your seed limit
SEED_LIMIT = 40

# How many VIP hours awarded ?
# (If the player already has a VIP that ends AFTER this delay, VIP won't be given)
GRANTED_VIP_HOURS = 24


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
    # (you can add more lines if you manage more than 10 servers)
]


# Translations
# -------------------------------------
# "key" : ["english", "french", "spanish", "german", "russian", "brazilian-portuguese", "polish", "chinese"]
TRANSL = {
    "nostatsyet": ["No stats yet", "Pas de stats", "Aún no hay estadísticas", "noch keine Statistiken", "Статистики пока нет", "Sem estatísticas ainda", "Brak dostępnych statystyk", "暂无统计数据"],
    "allies": ["all", "all", "aliados", "Allierte", "Союзники", "aliados", "Alianci", "盟军"],
    "axis": ["axi", "axe", "eje", "Achsenmächte", "Ось", "eixo", "Oś", "轴心国"],
    "best_players": ["Best players", "Meilleurs joueurs", "Mejores jugadores", "Beste Spieler", "Лучшие игроки", "Melhores jogadores", "Najlepsi gracze", "最佳玩家"],
    "armycommander": ["Commander", "Commandant", "Comandante", "Kommandant", "Командир", "Comandante", "Dowódca", "指挥官"],
    "infantry": ["Infantry", "Infanterie", "Infantería", "Infanterie", "Пехота", "Infantaria", "Piechota", "步兵"],
    "tankers": ["Tankers", "Tankistes", "Tanquistas", "Panzerspieler", "Танкисты", "Tanqueiros", "Czołgiści", "坦克兵"],
    "best_squads": ["Best squads", "Meilleures squads", "Mejores escuadrones", "Beste Mannschaften", "Лучшие отряды", "Melhores esquadrões", "Najlepsze jednostki", "最佳小队"],
    "offense": ["attack", "attaque", "ataque", "Angriff", "Атака", "ataque", "Ofensywa", "进攻"],
    "defense": ["defense", "défense", "defensa", "Verteidigung", "Оборона", "defesa", "Defensywa", "防守"],
    "combat": ["combat", "combat", "combate", "Kampf", "Бой", "combate", "Walka", "战斗"],
    "support": ["support", "soutien", "apoyo", "Unterstützung", "Поддержка", "suporte", "Wsparcie", "支援"],
    "ratio": ["ratio", "ratio", "proporción", "Verhältnis", "Коэффициент", "proporção", "Średnia", "比率"],
    "killrate": ["kills/min", "kills/min", "bajas/min", "Kills/min", "Убийств/мин", "abates/min", "Zabójstwa/min", "击杀率/分"],
    "vip_until": ["VIP until", "VIP jusqu'au", "VIP hasta", "VIP bis", "VIP до", "VIP até", "VIP do", "VIP有效期至"],
    "already_vip": ["Already VIP !", "Déjà VIP !", "¡Ya es VIP!", "bereits VIP !", "Уже VIP!", "Já é VIP!", "Aktualnie ma VIPa!", "已经是VIP！"],
    "gamejustended": ["Game just ended", "Partie terminée", "El juego acaba de terminar", "Spiel beendet", "Игра только что закончилась", "Jogo acabou", "Gra właśnie się zakończyła", "游戏刚刚结束"],
    "vip_at": ["at", "à", "a las", "um", "в", "às", "do godziny", "于"]
}

# VIP announce : local time
# Find you local timezone : https://utctime.info/timezone/
LOCAL_TIMEZONE = "Etc/GMT-0"
LOCAL_TIME_FORMAT = f"%d/%m/%Y {TRANSL['vip_at'][LANG]} %Hh%M (GMT)"


# Miscellaneous (you should not change these)
# -------------------------------------

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
    # CLAN_URL = str(config.discord_invite_url)
    DISCORD_EMBED_AUTHOR_URL = str(config.server_url)
except Exception as error:
    logger.error("Could not retrieve CLAN_URL and/or DISCORD_EMBED_AUTHOR_URL from database : %s", error)
    # CLAN_URL = ""
    DISCORD_EMBED_AUTHOR_URL = ""


def clean_bonus(value, name="BONUS") -> float:
    """
    Clean and validate the bonus value.
    Accepts int, float, or numeric str.
    Returns abs(value) if non-zero, otherwise 1.0.
    """
    if isinstance(value, (int, float)):
        return abs(value) if value != 0 else 1.0

    if value is not None:
        try:
            converted = float(value)
            return abs(converted) if converted != 0 else 1.0
        except (ValueError, TypeError):
            logger.warning(
                f"{name} has an invalid value or type ({type(value).__name__}: {value}). "
                "Falling back to default value: 1.0"
            )

    return 1.0


def is_vip_for_less_than_xh(rcon: Rcon, player_id: str, vip_delay_hours: int):
    """
    returns 'true' if player has no VIP or a VIP that expires in less than vip_delay_hours,
    'false' if he has a VIP that expires in more than vip_delay_hours or no VIP at all.
    """
    # Get the VIP list
    try:
        actual_vips = rcon.get_vip_ids()
    except Exception as error:
        logger.error("Can't get the VIP list : %s", error)
        return False  # Consider the player as a VIP (giving a VIP could erase an actual -larger- VIP)

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
    Gives a x hours VIP
    Returns a str that announces the VIP expiration (local) time
    """
    combined_name = f"{player_name} (top player)"

    # Gives X hours VIP
    now_plus_xh = datetime.now(timezone.utc) + timedelta(hours=hours_awarded)
    now_plus_xh_vip_formatted = now_plus_xh.strftime('%Y-%m-%dT%H:%M:%SZ')
    rcon.add_vip(player_id, combined_name, now_plus_xh_vip_formatted)

    # Returns a string giving the new expiration date in local time
    now_plus_xh_utc = now_plus_xh.replace(tzinfo=ZoneInfo("UTC"))
    now_plus_xh_local_tz = now_plus_xh_utc.astimezone(ZoneInfo(LOCAL_TIMEZONE))
    now_plus_xh_local_display = now_plus_xh_local_tz.strftime(LOCAL_TIME_FORMAT)
    return f"{TRANSL['vip_until'][LANG]}\n{str(now_plus_xh_local_display)} !"


def get_teamplay_score(player: dict) -> int:
    """
    (Players)
    Calculates the teamplay score using combat and support stats.
    Formula: combat + (support * SUPPORT_BONUS)
    """

    s_bonus = clean_bonus(SUPPORT_BONUS, "SUPPORT_BONUS")

    combat_score = int(player.get("combat", 0))
    support_score = int(player.get("support", 0))

    teamplay_score = combat_score + (support_score * s_bonus)

    return int(teamplay_score)


def get_offdef_score(player: dict) -> int:
    """
    (Players)
    Calculates the combined offense and defense score.
    Formula: offense + (defense * DEFENSE_BONUS)
    """
    d_bonus = clean_bonus(DEFENSE_BONUS, "DEFENSE_BONUS")

    offense = int(player.get("offense", 0))
    defense = int(player.get("defense", 0))

    return int(offense + (defense * d_bonus))


def get_kd_ratio_score(player: dict) -> float:
    """
    (Players)
    Calculates the kills/deaths ratio.
    If deaths are 0, the ratio equals the number of kills.
    """
    kills = int(player.get("kills", 0))
    deaths = int(player.get("deaths", 0))

    if kills == 0:
        return 0.0

    if deaths == 0:
        return float(kills)

    ratio = kills / deaths

    return round(float(ratio), 1)


def get_killrate_score(player: dict) -> float:
    """
    (Players)
    Calculates the kills per minute ratio.
    If playtime is 0, the rate equals the number of kills.
    """
    kills = int(player.get("kills", 0))
    playtime_min = int(player.get("map_playtime_seconds", 0)) / 60

    if kills == 0:
        return 0.0

    if playtime_min == 0:
        return float(kills)

    rate = kills / playtime_min

    return round(float(rate), 1)


def get_player_ranking(rcon: Rcon, server_status, api_data: dict, unit_type: str, score_func, limit: int = 3, mention_details: bool = False, give_vip: bool = False) -> list:
    """
    (Players)
    Extracts, ranks, and optionally triggers VIP rewards.
    """
    players_stats = []
    result = api_data.get("result", api_data)

    for side in ["allies", "axis"]:
        team_data = result.get(side, {})

        # Commander
        if unit_type == "command":
            cmd = team_data.get("commander")
            if cmd:
                score = score_func(cmd)
                if score and score > 0:
                    name = cmd["name"]
                    if mention_details:
                        name = f"({side.capitalize()}/CMD) {name}"
                    # On stocke l'objet complet pour la partie VIP plus bas
                    players_stats.append({
                        "name": name,
                        "score": score,
                        "player_id": cmd.get("player_id"),
                        "raw_data": cmd  # Gardé pour les checks de rôle/offense
                    })

        # Squads
        else:
            squads = team_data.get("squads", {})
            for s_name, s_info in squads.items():
                # if s_name != "unassigned" and s_info.get("type") == unit_type:
                if s_name != "unassigned" and str(s_info.get("type")).lower() == unit_type.lower():
                    for p in s_info.get("players", []):
                        score = score_func(p)
                        if score and score > 0:
                            name = p["name"]
                            if mention_details:
                                name = f"({side.capitalize()}/{s_name[0].upper()}) {name}"
                            players_stats.append({
                                "name": name,
                                "score": score,
                                "player_id": p.get("player_id"),
                                "raw_data": p  # Gardé pour les checks de rôle/offense
                            })

    players_stats.sort(key=lambda x: x["score"], reverse=True)

    # VIP
    if give_vip:
        # winners = players_stats[:limit]
        winners = players_stats[:VIP_WINNERS]
        granted_vip_hours = GRANTED_VIP_HOURS if GRANTED_VIP_HOURS > 0 else 24
        for player in winners:
            if server_status["current_players"] >= SEED_LIMIT:

                raw = player['raw_data']

                # No VIP for "entered at last second" commander
                if (
                    raw.get('role') == "armycommander"
                    and (
                        (int(raw.get('offense', 0)) + int(raw.get('defense', 0))) / 20 < VIP_COMMANDER_MIN_PLAYTIME_MINS
                        or int(raw.get('support', 0)) < VIP_COMMANDER_MIN_SUPPORT_SCORE
                    )
                ):
                    continue

                # Only give VIP if the winner has no VIP at all or a VIP that ends in less than granted_vip_hours
                if is_vip_for_less_than_xh(rcon, player['player_id'], granted_vip_hours):
                    vip_message = give_xh_vip(rcon, player['player_id'], player['name'], granted_vip_hours)
                else:
                    vip_message = f"{TRANSL['already_vip'][LANG]}\n"
                try:
                    rcon.message_player(
                        player_id=player['player_id'],
                        message=vip_message,
                        by="custom_tools_live_topstats",
                        save_message=False
                    )
                except Exception as error:
                    logger.error("Ingame VIP message_player couldn't be sent : %s", error)

    formatted_list = []
    for p in players_stats[:limit]:
        s_val = f"{p['score']:.1f}" if isinstance(p['score'], float) else str(p['score'])
        formatted_list.append(f"{p['name']} : {s_val}")

    return formatted_list


def get_squad_teamplay_score(squad: dict) -> int:
    """
    (Squads)
    Calculates combined teamplay score for a whole squad.
    """
    s_bonus = clean_bonus(SUPPORT_BONUS, "SUPPORT_BONUS")
    return int(squad.get("combat", 0) + (squad.get("support", 0) * s_bonus))


def get_squad_offdef_score(squad: dict) -> int:
    """
    (Squads)
    Calculates combined off/def score for a whole squad.
    """
    d_bonus = clean_bonus(DEFENSE_BONUS, "DEFENSE_BONUS")
    return int(squad.get("offense", 0) + (squad.get("defense", 0) * d_bonus))


def get_squad_kd_score(squad: dict) -> float:
    """
    (Squads)
    Calculates the cumulative K/D ratio of all players in the squad.
    """
    players = squad.get("players", [])
    total_kills = sum(int(p.get("kills", 0)) for p in players)
    total_deaths = sum(int(p.get("deaths", 0)) for p in players)

    if total_kills == 0:
        return 0.0
    if total_deaths == 0:
        return float(total_kills)

    return round(total_kills / total_deaths, 1)


def get_squad_killrate_score(squad: dict) -> float:
    """
    (Squads)
    Calculates the squad killrate based on cumulative kills
    divided by cumulative playtime of all members.
    """
    players = squad.get("players", [])
    if not players:
        return 0.0

    total_kills = sum(int(p.get("kills", 0)) for p in players)
    total_playtime_min = sum(int(p.get("map_playtime_seconds", 0)) for p in players) / 60

    if total_kills == 0:
        return 0.0

    if total_playtime_min == 0:
        return float(total_kills)

    rate = total_kills / total_playtime_min

    return round(float(rate), 2)  # Précision à 2 décimales car les chiffres seront plus petits


def get_squad_ranking(api_data: dict, unit_type: str, score_func, limit: int = 3) -> list:
    """
    (Squads)
    Ranks squads or the Commander unit.
    """
    squads_stats = []
    result = api_data.get("result", api_data)

    for side in ["allies", "axis"]:
        team_data = result.get(side, {})

        if unit_type == "command":
            cmd = team_data.get("commander")
            if cmd:
                # Harmonizing data structure : create a commander squad subtree
                fake_squad = {
                    "type": "command",
                    "players": [cmd],
                    "offense": cmd.get("offense", 0),
                    "defense": cmd.get("defense", 0),
                    "combat": cmd.get("combat", 0),
                    "support": cmd.get("support", 0)
                }
                score = score_func(fake_squad)
                # squads_stats.append({"name": f"({side.capitalize()}/CMD) Commander", "score": score})
                squads_stats.append({"name": f"{side.capitalize()}/CMD", "score": score})

        else:
            squads = team_data.get("squads", {})
            for s_name, s_info in squads.items():
                if s_name != "unassigned" and s_info.get("type") == unit_type:
                    score = score_func(s_info)
                    # label = f"({side.capitalize()}/{s_name[0].upper()}) {s_name.capitalize()}"
                    label = f"{side.capitalize()}/{s_name[0].upper()}"
                    squads_stats.append({"name": label, "score": score})

    squads_stats.sort(key=lambda x: x["score"], reverse=True)
    return [f"{s['name']} : {s['score']}" for s in squads_stats[:limit]]


def generate_full_report(rcon, api_data, config, is_match_end: bool = False):
    """
    Orchestrates the report.
    is_match_end: If True, allows VIP distribution based on config.
    """
    server_status = rcon.get_status()
    report_sections = []

    # Players
    player_cfg = config.get("players", {})
    for unit_type, rankings in player_cfg.items():
        for r in rankings:
            should_grant = is_match_end and r.get("vip", False)

            results = get_player_ranking(
                rcon,
                server_status,
                api_data,
                unit_type,
                SCORE_FUNCTIONS[r["score"]],
                r["limit"],
                r.get("details", False),
                should_grant
            )

            if results:
                title = f"▒ TOP {r['limit']} {unit_type.upper()} ({r['score'].upper()})"
                report_sections.append(f"{title}\n" + "\n".join(results))

    # Squads
    squad_cfg = config.get("squads", {})
    for unit_type, rankings in squad_cfg.items():
        for r in rankings:
            results = get_squad_ranking(
                api_data,
                unit_type,
                SCORE_FUNCTIONS[r["score"]],
                r["limit"]
            )
            if results:
                header = f"▒ TOP {r['limit']} {unit_type.upper()} SQUADS ({r['score'].upper()})"
                report_sections.append(header + "\n" + "\n".join(results))

    return "\n\n".join(report_sections)


# Functions mapping (must be declared AFTER the functions definitions)
SCORE_FUNCTIONS = {
    # No need to create a dedicated function, as the stat is directly available from the 'get_team_view' endpoint
    "combat": lambda p: int(p.get("combat", 0)),
    "offense": lambda p: int(p.get("offense", 0)),
    "defense": lambda p: int(p.get("defense", 0)),
    "support": lambda p: int(p.get("support", 0)),
    "kills": lambda p: int(p.get("kills", 0)),
    "deaths": lambda p: int(p.get("deaths", 0)),
    "team_kills": lambda p: int(p.get("team_kills", 0)),
    "vehicle_kills": lambda p: int(p.get("vehicle_kills", 0)),
    "vehicles_destroyed": lambda p: int(p.get("vehicles_destroyed", 0)),
    # These are calculated stats, provided by dedicated functions
    "teamplay": get_teamplay_score,              # combat + support * support_bonus
    "offdef": get_offdef_score,                  # offense + defense * defense bonus
    "kd": get_kd_ratio_score,                    # kills / deaths
    "killrate": get_killrate_score,              # kills / minute
    "squad_teamplay": get_squad_teamplay_score,  # combat + support * support_bonus
    "squad_offdef": get_squad_offdef_score,      # offense + defense * defense bonus
    "squad_kd": get_squad_kd_score,              # kills / deaths
    "squad_killrate": get_squad_killrate_score   # kills / minute
}


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

    # Check log for mandatory variables
    chat_message: str|None = struct_log["sub_content"]
    if chat_message is None:
        return

    player_id: str|None = struct_log["player_id_1"]
    if player_id is None:
        return

    # Get data from RCON
    get_team_view: dict = rcon.get_team_view()

    # Process data
    message = generate_full_report(rcon, get_team_view, CONFIG, is_match_end=False)

    if len(message) == 0:
        message = f"{TRANSL['nostatsyet'][LANG]}"

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
    message = generate_full_report(rcon, get_team_view, CONFIG, is_match_end=True)

    if len(message) == 0:
        message = f"{TRANSL['nostatsyet'][LANG]}"

    # logs
    horizontal_separator = "-" * 79
    logger.info(horizontal_separator + "\n" + message)

    # Send ingame message (only if available stats)
    if message != f"{TRANSL['nostatsyet'][LANG]}":
        try:
            rcon.message_all_players(message=message)
        except Exception as error:
            logger.error("Ingame message_all_players couldn't be sent : %s", error)

    # Discord
    # ------------------------------------------------------------------------
    # Is a webhook enabled on this server ?
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
