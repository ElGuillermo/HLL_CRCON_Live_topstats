# HLL_CRCON_Live_topstats

A plugin for Hell Let Loose (HLL) CRCON (see : https://github.com/MarechJ/hll_rcon_tool)
that displays and rewards top players, based on their scores.

![375489308-67943815-da9c-41ff-988c-eaaa2e0e64c2](https://github.com/user-attachments/assets/e44d0f07-23a8-4f62-87c4-742803c8be06)

## Features
- Enable/disable the script on the different servers managed in CRCON.
- Message can be called anytime with `!top` chat command (configurable).
- Message will be displayed to all players at game's end.
- Choose to give VIPs at game's end (you can define the number of top players that will receive one, and it's duration).
- Send the report in a Discord channel.
- Available translations : english, french, spanish, german, rusian, brazilian portuguese, polish, spanish and chinese.

## Observed scores

This new version (April 6, 2024) allows you to choose :  
- players/squads to be observed :  
  commander, infantry, armo, artillery, recon  
- stats or stats combination to be calculated :  
  (any available stat from `get_team_view` CRCON API endpoint can be mapped)

The script comes with default (usual) settings :  
- players :
  - commander : combat + support
  - infantry : combat + support, offense + defense, kills/deaths ratio, killrate
- squads :
  - infantry : combat + support, offense + defense
  - armor : combat + support
  - artillery : combat + support
  - recon : combat + support

A multiplier bonus can be given to defense and support scores, if you want to reward teamplay more than individual skills.  
Doing so will ensure the teamplayers will enter the server more often than CODdies.

## Install

> [!NOTE]
> The shell commands given below assume your CRCON is installed in `/root/hll_rcon_tool`.  

- Log into your CRCON host machine using SSH and enter these commands (one line at at time) :  

- Download the tool (enter these commands, one line at a time)  
  ```shell
  cd /root/hll_rcon_tool

  wget https://raw.githubusercontent.com/ElGuillermo/HLL_CRCON_restart/refs/heads/main/restart.sh

  mkdir custom_tools

  cd /root/hll_rcon_tool/custom_tools

  wget https://raw.githubusercontent.com/ElGuillermo/HLL_CRCON_Live_topstats/refs/heads/main/hll_rcon_tool/custom_tools/live_topstats.py
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
- Edit `/root/hll_rcon_tool/custom_tools/live_topstats.py` and set the parameters to fit your needs.
- Restart CRCON :
  ```shell
  cd /root/hll_rcon_tool
  sh ./restart.sh
  ```

## Limitations
⚠️ Any change to these files requires a CRCON rebuild and restart (using the `restart.sh` script) to be taken in account :
- `/root/hll_rcon_tool/custom_tools/live_topstats.py`
- `/root/hll_rcon_tool/rcon/hooks.py`

⚠️ This plugin requires a modification of the `/root/hll_rcon_tool/rcon/hooks.py` file, which originates from the official CRCON depot.  
If any CRCON upgrade implies updating this file, the usual upgrade procedure, as given in official CRCON instructions, will **FAIL**.  
To successfully upgrade your CRCON, you'll have to revert the changes back, then reinstall this plugin.  
To revert to the original file :  
```shell
cd /root/hll_rcon_tool
git restore rcon/hooks.py
```
