# HLL_CRCON_Live_topstats

A plugin for Hell Let Loose (HLL) CRCON (see : https://github.com/MarechJ/hll_rcon_tool)  
that displays and rewards top players and squads, based on their scores.

<img width="3823" height="947" alt="image" src="https://github.com/user-attachments/assets/bc740f69-b296-46f4-b9fa-21b68abb57af" />

## Features
- Select the stats and number of players you want to display
- Choose the enabled servers (ex : only on 1, 2, 3 and 7)
- Stats can be called anytime using a configurable chat command (default: `!top`).
- Stats will always be displayed to all players at game's end.
- Award VIPs at endgame : choose the duration and the number of winners.
- Endgame stats can be sent in a Discord channel.
- Available translations : english, french, spanish, german, russian, brazilian portuguese, polish and chinese.
- A multiplier bonus can be given to defense and support scores,  
  to reward first and foremost the players who play for the team  
  rather than for their individual stats.

## Observed scores

This new version (April 6, 2026) allows you to choose :  
- players/squads to be observed :  
  - commander, infantry, armor, artillery, recon  
- any available stat from `get_team_view` CRCON API endpoint can be mapped or combined

### The script comes with default (usual) settings :  

- players :
  - commander :
    - teamplay (combat + support * bonus)
  - infantry :
    - teamplay
    - offdef (offense + defense * bonus)
    - kills/deaths ratio
    - killrate
- squads :
  - infantry :
    - teamplay
    - offdef
  - armor :
    - teamplay
    - vehicles_destroyed
  - artillery :
    - teamplay
  - recon :
    - teamplay

## Install

> [!NOTE]
> The shell commands given below assume your CRCON is installed in `/root/hll_rcon_tool`.  

- Log into your CRCON host machine using SSH

- Download the tool (enter these commands, one line at a time)  
  ```shell
  cd /root/hll_rcon_tool

  wget -O https://raw.githubusercontent.com/ElGuillermo/HLL_CRCON_restart/refs/heads/main/restart.sh

  mkdir -p custom_tools

  cd /root/hll_rcon_tool/custom_tools

  wget -O https://raw.githubusercontent.com/ElGuillermo/HLL_CRCON_Live_topstats/refs/heads/main/hll_rcon_tool/custom_tools/live_topstats.py

  wget -O https://raw.githubusercontent.com/ElGuillermo/HLL_CRCON_Live_topstats/refs/heads/main/hll_rcon_tool/custom_tools/live_topstats_config.py

  wget -O https://raw.githubusercontent.com/ElGuillermo/HLL_CRCON_custom_common_translations.py/refs/heads/main/common_translations.py
  ```

- Modify CRCON files  
  Edit `/root/hll_rcon_tool/rcon/hooks.py` and add these lines :  
  (in the import part, on top of the file)  
    ```python
    import custom_tools.live_topstats as live_topstats
    ```  
  (At the very end of the file)  
    ```python
    @on_chat
    def livetopstats_onchat(rcon: Rcon, struct_log: StructuredLogLineWithMetaData):
      live_topstats.stats_on_chat_command(rcon, struct_log)

    @on_match_end
    def livetopstats_onmatchend(rcon: Rcon, struct_log: StructuredLogLineWithMetaData):
      live_topstats.stats_on_match_end(rcon, struct_log)
    ```

## Config
- Edit `/root/hll_rcon_tool/custom_tools/live_topstats_config.py` and set the parameters to fit your needs.

- Restart CRCON :
  ```shell
  cd /root/hll_rcon_tool

  sh ./restart.sh
  ```
  If you don't want to use the `restart.sh` script, you can rebuild containers and restart CRCON using Docker commands :  
  ```shell
  cd /root/hll_rcon_tool

  sudo docker compose build && sudo docker compose down && sudo docker compose up -d --remove-orphans
  ```

## Limitations
⚠️ Any change to these files requires a CRCON rebuild and restart (using the `restart.sh` script) to be taken in account :
- `/root/hll_rcon_tool/custom_tools/common_translations.py`
- `/root/hll_rcon_tool/custom_tools/live_topstats.py`
- `/root/hll_rcon_tool/custom_tools/live_topstats_config.py`
- `/root/hll_rcon_tool/rcon/hooks.py`

⚠️ This plugin requires a modification of the `/root/hll_rcon_tool/rcon/hooks.py` file, which originates from the official CRCON depot.  
If any CRCON upgrade implies updating this file, the usual upgrade procedure, as given in official CRCON instructions, will **FAIL**.  
To successfully upgrade your CRCON, you'll have to revert the changes back, then reinstall this plugin.  
To revert to the original file :  
```shell
cd /root/hll_rcon_tool
git restore rcon/hooks.py
```
