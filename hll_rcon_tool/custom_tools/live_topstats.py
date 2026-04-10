"""
live_topstats.py

A plugin for HLL CRCON (see : https://github.com/MarechJ/hll_rcon_tool)
that displays and rewards top players

Source : https://github.com/ElGuillermo

Feel free to use/modify/distribute, as long as you keep this note in your code
"""

from datetime import datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo
import logging
import os
import discord
from rcon.rcon import Rcon, StructuredLogLineWithMetaData
from rcon.user_config.rcon_server_settings import RconServerSettingsUserConfig
from rcon.utils import get_server_number

import custom_tools.live_topstats_config as live_topstats_config
from custom_tools.common_translations import TRANSL


# Setup logger
os.makedirs('/logs', exist_ok=True)
logger = logging.getLogger('live_topstats_standalone')
logger.setLevel(logging.INFO)
logger.propagate = False
if not logger.handlers:
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
    file_handler = logging.FileHandler('/logs/custom_tools_live_topstats.log', mode='a', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


# Clan related (as set in CRCON user interface, in http://<ip>:8010/settings/others/crcon)
try:
    rcon_server_settings_userconfig = RconServerSettingsUserConfig.load_from_db()
    DISCORD_EMBED_AUTHOR_URL = str(rcon_server_settings_userconfig.server_url)
except Exception as error:
    logger.error("Could not retrieve DISCORD_EMBED_AUTHOR_URL from database : %s", error)
    DISCORD_EMBED_AUTHOR_URL = "https://github.com/ElGuillermo/HLL_CRCON_Live_topstats"


def sanitize_to_int(value: Any, default: int = 0, min_val: int = 0, max_val: int|None = None) -> int:
    """
    Converts 'value' to a positive integer (truncating decimals).
    Returns 'default' :
    - if conversion isn't possible.
    - if 'value' is out of min-max range
    Returns 'value' (int) if converted
    """
    try:
        clean_val = int(float(value))
        if clean_val < min_val:
            logger.warning(f"Invalid value in config ('%s' is too low, min allowed is '%s'), using default value : %s", value, min_val, default)
            return default
        if max_val is not None and clean_val > max_val:
            logger.warning(f"Invalid value in config ('%s' is too high, max allowed is '%s'), using default value : %s", value, max_val, default)
            return default
        return clean_val
    except (ValueError, TypeError):
        logger.warning(f"Invalid value in config ('%s' is not a valid number), using default value : %s", value, default)
        return default


# Check config
num_langs = len(next(iter(TRANSL.values())))
live_topstats_config.LANG = sanitize_to_int(live_topstats_config.LANG, default=0, max_val=num_langs - 1)
live_topstats_config.VIP_COMMANDER_MIN_PLAYTIME_MINS = sanitize_to_int(live_topstats_config.VIP_COMMANDER_MIN_PLAYTIME_MINS, default=20, min_val=0)
live_topstats_config.VIP_COMMANDER_MIN_SUPPORT_SCORE = sanitize_to_int(live_topstats_config.VIP_COMMANDER_MIN_SUPPORT_SCORE, default=1000, min_val=0)
live_topstats_config.VIP_WINNERS = sanitize_to_int(live_topstats_config.VIP_WINNERS, default=0, min_val=0, max_val=100)
live_topstats_config.SEED_LIMIT = sanitize_to_int(live_topstats_config.SEED_LIMIT, default=40, min_val=0, max_val=100)
live_topstats_config.GRANTED_VIP_HOURS = sanitize_to_int(live_topstats_config.GRANTED_VIP_HOURS, default=24, min_val=0)


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
    local_tz = ZoneInfo(live_topstats_config.LOCAL_TIMEZONE)
    local_dt = expiration_dt.astimezone(local_tz)

    # Message building
    header = TRANSL['vip_header'][live_topstats_config.LANG]       # "You are in the topstats!"
    won_text = TRANSL['vip_won'][live_topstats_config.LANG]        # "You won a VIP until"
    date_str = local_dt.strftime('%d/%m/%Y')  # "01/01/2001"
    at_text = TRANSL['vip_at'][live_topstats_config.LANG]          # "at"
    time_str = local_dt.strftime('%Hh%M')     # "12h00"

    return f"{header}\n\n{won_text}\n{date_str}, {at_text} {time_str} !"


def get_player_teamplay(player: dict) -> int:
    """
    Calculates the teamplay score using combat and support stats.
    Formula: combat + (support * SUPPORT_BONUS)
    """
    combat = int(player.get("combat", 0))
    support = int(player.get("support", 0))
    support_bonus = clean_bonus(live_topstats_config.SUPPORT_BONUS, "SUPPORT_BONUS")

    return int(round(combat + (support * support_bonus)))


def get_player_offdef(player: dict) -> int:
    """
    Calculates the combined offense and defense score.
    Formula: offense + (defense * DEFENSE_BONUS)
    """
    offense = int(player.get("offense", 0))
    defense = int(player.get("defense", 0))
    defense_bonus = clean_bonus(live_topstats_config.DEFENSE_BONUS, "DEFENSE_BONUS")

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
                    name = cmd["name"][:30]  # [:30] avoids line returns
                    if mention_details:
                        name = f"({TRANSL[side+'_short'][live_topstats_config.LANG].capitalize()}/{TRANSL['armycommander_short'][live_topstats_config.LANG].capitalize()}) {name[:20]}"  # [:20] avoids line returns
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
                            name = p["name"][:30]
                            if mention_details:
                                name = f"({TRANSL[side+'_short'][live_topstats_config.LANG].capitalize()}/{s_name[0].upper()}) {name[:20]}"
                            players_stats.append({
                                "name": name,
                                "score": score,
                                "player_id": p.get("player_id"),
                                "raw_data": p
                            })

    players_stats.sort(key=lambda x: x["score"], reverse=True)

    # VIP
    if (give_vip
        and server_status["current_players"] >= live_topstats_config.SEED_LIMIT
        and live_topstats_config.VIP_WINNERS > 0
        and live_topstats_config.GRANTED_VIP_HOURS > 0
    ):
        winners = players_stats[:live_topstats_config.VIP_WINNERS]

        for player in winners:
            raw = player['raw_data']

            # No VIP for "entered at last second" commander
            if (
                raw.get('role') == "armycommander"
                and (
                    (int(raw.get('offense', 0)) + int(raw.get('defense', 0))) / 20 < live_topstats_config.VIP_COMMANDER_MIN_PLAYTIME_MINS
                    or int(raw.get('support', 0)) < live_topstats_config.VIP_COMMANDER_MIN_SUPPORT_SCORE
                )
            ):
                continue  # Player won't receive any message

            # Only give VIP if the player has either :
            # - no VIP at all
            # - a VIP that ends in less than GRANTED_VIP_HOURS
            if is_vip_for_less_than_xh(rcon, player['player_id'], live_topstats_config.GRANTED_VIP_HOURS):
                vip_message = give_xh_vip(rcon, player['player_id'], player['name'], live_topstats_config.GRANTED_VIP_HOURS)
            else:
                vip_message = f"{TRANSL['vip_header'][live_topstats_config.LANG]}\n\n{TRANSL['already_vip'][live_topstats_config.LANG]}\n"

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
    support_bonus = clean_bonus(live_topstats_config.SUPPORT_BONUS, "SUPPORT_BONUS")

    return int(round(combat + (support * support_bonus)))


def get_squad_offdef(squad: dict) -> int:
    """
    Calculates combined off/def score for a whole squad.
    Formula: offense + (defense * DEFENSE_BONUS)
    """
    offense = int(squad.get("offense", 0))
    defense = int(squad.get("defense", 0))
    defense_bonus = clean_bonus(live_topstats_config.DEFENSE_BONUS, "DEFENSE_BONUS")

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
                squads_stats.append({"name": f"{TRANSL[side][live_topstats_config.LANG].capitalize()}/{TRANSL['armycommander_short'][live_topstats_config.LANG].capitalize()}", "score": score})

        # Squads
        else:
            squads = team_data.get("squads", {})
            for s_name, s_info in squads.items():
                if s_name != "unassigned" and str(s_info.get("type")).lower() == unit_type.lower():
                    score = score_func(s_info)
                    if score and score > 0:
                        name = f"{TRANSL[side][live_topstats_config.LANG].capitalize()}/{s_name[0].upper()}"
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
    "defense_bonus": lambda p: int(int(p.get("defense", 0)) * clean_bonus(live_topstats_config.DEFENSE_BONUS, "DEFENSE_BONUS")),
    "support_bonus": lambda p: int(int(p.get("support", 0)) * clean_bonus(live_topstats_config.SUPPORT_BONUS, "SUPPORT_BONUS")),

    # (players)
    "player_team_kills": lambda p: int(p.get("team_kills", 0)),
    "player_vehicle_kills": lambda p: int(p.get("vehicle_kills", 0)),
    "player_vehicles_destroyed": lambda p: int(p.get("vehicles_destroyed", 0)),
    # These are calculated stats, provided by dedicated functions
    "player_teamplay": get_player_teamplay,                    # combat + support * support_bonus
    "player_offdef": get_player_offdef,                        # offense + defense * defense bonus
    "player_kd": get_player_kd,                                # kills / deaths
    "player_kpm": get_player_kpm,                              # kills / minute

    # (squads)
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
        category_lines = []

        for unit_type, rankings in cfg.items():
            valid_results = []
            for r in rankings:
                should_grant = is_match_end and r.get("vip", False) if category_key == "players" else False
                if category_key == "players":
                    data = fetch_func(rcon, server_status, api_data, unit_type, SCORE_FUNCTIONS[r["score"]], r["limit"], r.get("details", False), should_grant)
                else:
                    data = fetch_func(api_data, unit_type, SCORE_FUNCTIONS[r["score"]], r["limit"])
                if data:
                    valid_results.append((r, data))

            if valid_results:
                if not category_header_added:
                    title = TRANSL[main_header_key][live_topstats_config.LANG].upper()
                    category_lines.append(f"— {title} —")
                    category_header_added = True

                unit_name = TRANSL.get(unit_type.lower(), [unit_type])[live_topstats_config.LANG].capitalize()
                category_lines.append(f"└ {unit_name}")

                for i, (r, results) in enumerate(valid_results):
                    raw_score_key = r['score'].lower()
                    clean_key = raw_score_key.removeprefix("player_").removeprefix("squad_")
                    translations = TRANSL.get(clean_key)
                    stat_label = translations[live_topstats_config.LANG].capitalize() if translations else clean_key.capitalize()

                    is_last_stat = (i == len(valid_results) - 1)
                    # branch = " └" if is_last_stat else " ├"
                    branch = " ├" if is_last_stat else " ├"
                    # branch = " ┌" if is_last_stat else " ┌"

                    category_lines.append(f"{branch} {stat_label}")

                    # pipe = "  ·" if is_last_stat else " │ ·"
                    pipe = " │ ·" if is_last_stat else " │ ·"
                    for line in results:
                        category_lines.append(f"{pipe} {line}")

        return category_lines

    player_lines = process_config_category("players", get_player_ranking, "top_players")
    squad_lines = process_config_category("squads", get_squad_ranking, "top_squads")

    if player_lines:
        report_sections.append("\n".join(player_lines))
    if squad_lines:
        report_sections.append("\n".join(squad_lines))

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
    if server_number not in live_topstats_config.ENABLE_ON_SERVERS:
        return

    # Check log for mandatory variable
    chat_message: str|None = struct_log["sub_content"]
    if chat_message is None:
        return

    if chat_message == live_topstats_config.CHAT_COMMAND:

        # Check log for mandatory variable
        player_id: str|None = struct_log["player_id_1"]
        if player_id is None:
            return

        # Get data from RCON
        get_team_view: dict = rcon.get_team_view()

        # Process data
        report = generate_full_report(rcon, get_team_view, live_topstats_config.STATS_TO_DISPLAY, is_match_end=False)

        # Ingame message
        if not report:
            message = f"{TRANSL['nostatsyet'][live_topstats_config.LANG]}"
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
    if server_number not in live_topstats_config.ENABLE_ON_SERVERS:
        return

    # Get data from RCON
    get_team_view: dict = rcon.get_team_view()

    # Process data
    report = generate_full_report(rcon, get_team_view, live_topstats_config.STATS_TO_DISPLAY, is_match_end=True)  # is_match_end=True enables VIP granting

    # Prepare ingame message and logs
    if not report:
        message = f"{TRANSL['nostatsyet'][live_topstats_config.LANG]}"
    else:
        message = f"{report}"

    # logs
    logger.info(f"\n{message}")

    # Ingame message (only if available stats)
    if report:
        try:
            rcon.message_all_players(message=message)
        except Exception as error:
            logger.error("Ingame message_all_players couldn't be sent : %s", error)

    # Discord
    server_number = int(get_server_number())
    if not live_topstats_config.DISCORD_CONFIG[server_number - 1][1]:
        return

    discord_webhook = live_topstats_config.DISCORD_CONFIG[server_number - 1][0]

    webhook = discord.SyncWebhook.from_url(discord_webhook)

    embed = discord.Embed(
        title=TRANSL['gamejustended'][live_topstats_config.LANG],
        url="",
        description=message,
        color=0xffffff
    )

    embed.set_author(
        name=live_topstats_config.BOT_NAME,
        url=DISCORD_EMBED_AUTHOR_URL,
        icon_url=live_topstats_config.DISCORD_EMBED_AUTHOR_ICON_URL
    )

    embeds = []
    embeds.append(embed)

    try:
        webhook.send(embeds=embeds, wait=True)
    except Exception as error:
        logger.error("Discord embed couldn't be sent : %s", error)
