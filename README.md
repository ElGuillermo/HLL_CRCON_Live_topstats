# HLL_CRCON_Live_topstats

Unofficial plugin for the Hell Let Loose (HLL) [CRCON](https://github.com/MarechJ/hll_rcon_tool)

### Displays and rewards top players and squads, based on their stats.

![HLL_CRCON_Live_topstats](https://github.com/user-attachments/assets/bc740f69-b296-46f4-b9fa-21b68abb57af)

---

## Features
- Select the stats and number of players you want to display
- Choose the enabled servers (ex : only on 1, 2, 3 and 7)
- Stats can be called anytime using a configurable chat command (default: `!top`).
- Stats will always be displayed to all players at game's end.
- Award VIPs at endgame : choose the duration and the number of winners.
- Endgame stats can be sent in a Discord channel.
- A multiplier bonus can be given to defense and support scores,  
  to reward first and foremost the players who play for the team  
  rather than for their individual stats.
- Available translations : english, french, spanish, german, russian, brazilian portuguese, polish and chinese.

### Observed scores

This new version (April 6, 2026) allows you to choose :  
- players/squads to be observed :  
  - commander, infantry, armor, artillery, recon  
- any available stat from `get_team_view` CRCON API endpoint can be mapped or combined

### The script comes with default (usual) settings :  
```
- Top players
└ commander
  └ teamplay (combat + support * bonus)
└ infantry
  └ teamplay
  └ offdef (offense + defense * bonus)
  └ kills/deaths ratio
  └ killrate

- Top squads
└ infantry
  └ teamplay
  └ offdef
└ armor
  └ teamplay
  └ vehicles_destroyed
└ artillery
  └ teamplay
└ recon
  └ teamplay
```

---

> [!IMPORTANT]
> - The shell commands given below assume your CRCON is installed in `/root/hll_rcon_tool`  
>   You may have installed your CRCON in a different folder.  
>   If so, you'll have to adapt the commands below accordingly.
>
> - Always copy/paste/execute commands :warning: one line at a time :warning:

## Installation

### 1/3 - Log into your CRCON host machine using SSH

- See [this guide](https://github.com/MarechJ/hll_rcon_tool/wiki/Troubleshooting-&-Help-‐-Common-procedures-‐-How-to-enter-a-SSH-terminal) if you need help to do it.

### 2/3 - Download files

- Copy/paste/execute these commands :  
  ```shell
  cd /root/hll_rcon_tool

  wget -N https://raw.githubusercontent.com/ElGuillermo/HLL_CRCON_restart/refs/heads/main/restart.sh

  mkdir -p custom_tools

  cd /root/hll_rcon_tool/custom_tools

  wget -N https://raw.githubusercontent.com/ElGuillermo/HLL_CRCON_custom_common_translations.py/refs/heads/main/common_translations.py

  wget -N https://raw.githubusercontent.com/ElGuillermo/HLL_CRCON_Live_topstats/refs/heads/main/hll_rcon_tool/custom_tools/live_topstats.py

  wget -N https://raw.githubusercontent.com/ElGuillermo/HLL_CRCON_Live_topstats/refs/heads/main/hll_rcon_tool/custom_tools/live_topstats_config.py
  ```

### 3/3 - Edit `/root/hll_rcon_tool/rcon/hooks.py`

- Add these parts :  
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

---

## Configuration

### 1/2 - Edit `/root/hll_rcon_tool/custom_tools/live_topstats_config.py`

- Set the parameters to fit your needs (see inner comments for guidance).

### 2/2 - Rebuild and restart CRCON Docker containers

- Copy/paste/execute these commands :  
  ```shell
  cd /root/hll_rcon_tool
  
  sh ./restart.sh
  ```

> [!TIP]
> 
>  If you don't want to use the `restart.sh` script :  
>  - Copy/paste/execute these commands :  
>  ```shell
>  cd /root/hll_rcon_tool
>
>  sudo docker compose build && sudo docker compose down && sudo docker compose up -d --remove-orphans
>  ```

---

## Maintenance

### Disable this plugin

- Revert the changes made in [Installation 3/3](#33---edit-roothll_rcon_toolrconhookspy)

--

### Modify code or settings

:exclamation: Any change to these files requires to rebuild and restart CRCON Docker containers (same procedure as in [Configuration 2/2](#22---rebuild-and-restart-crcon-docker-containers)) : 
- `/root/hll_rcon_tool/rcon/hooks.py`
- `/root/hll_rcon_tool/custom_tools/common_translations.py`
- `/root/hll_rcon_tool/custom_tools/live_topstats.py`
- `/root/hll_rcon_tool/custom_tools/live_topstats_config.py`

--

### Upgrade CRCON

This plugin requires a modification of original CRCON file(s).  
:exclamation: If any CRCON update contains a new version of this file(s), the usual CRCON upgrade procedure will **FAIL**.

#### Restore the original CRCON file(s)

- Copy/paste/execute these commands : 
  ```shell
  cd /root/hll_rcon_tool
  
  cp rcon/hooks.py rcon/hooks.py.backup
  
  git restore rcon/hooks.py
  ```

#### Upgrade

- Follow the official upgrade instructions given in the new CRCON version announcement.
- Don't restart CRCON Docker containers yet (don't execute `docker compose up -d`).

#### Reapply changes

- copy/paste the changes from  
  `/root/hll_rcon_tool/rcon/hooks.py.backup`  
  into  
  `/root/hll_rcon_tool/rcon/hooks.py`
- Rebuild and restart CRCON Docker containers (same procedure as in [Configuration 2/2](#22---rebuild-and-restart-crcon-docker-containers)).
- If anything works as intended, you can delete the backup file :
  - Copy/paste/execute these commands :  
    ```
    cd /root/hll_rcon_tool
  
    rm rcon/hooks.py.backup
    ```
