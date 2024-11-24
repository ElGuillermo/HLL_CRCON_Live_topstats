# HLL_CRCON_Live_topstats

A plugin for Hell Let Loose (HLL) CRCON (see : https://github.com/MarechJ/hll_rcon_tool)
that displays and rewards top players, based on their scores.

![375489308-67943815-da9c-41ff-988c-eaaa2e0e64c2](https://github.com/user-attachments/assets/e44d0f07-23a8-4f62-87c4-742803c8be06)

## Features
- can be called anytime with `!top` chat command (configurable)  
- will be displayed to all players at game's end.  
- You can choose to give VIPs at game's end (you can define the number of top players that will receive one, and it's duration).

## Observed scores

- (top players will earn a VIP at game's end)
    - commanders
        - combat + (support * bonus)
    - infantry players
        - offense * (defense * bonus)
        - combat + (support * bonus)
- (for info only - no VIPs given)
    - infantry players
        - kills / deaths
        - kills / minute
    - infantry squads
        - offense * (defense * bonus)
        - combat + (support * bonus)
    - armor squads
        - offense * (defense * bonus)
        - combat + (support * bonus)

A multiplication bonus can be given to defense and support scores, if you want to reward teamplay more than individual skills.  
Doing so will ensure the teamplayers will enter the server more often than CODdies.

Tankers don't get any VIP, as they usually have a huge combat score and would easily get a VIP on each game.

Players must gain offense AND defense points to enter the top, thus to avoid giving VIPs to those who purposely stay AFK in HQs.

## Install

> [!NOTE]
> The shell commands given below assume your CRCON is installed in `/root/hll_rcon_tool`.  
> You may have installed your CRCON in a different folder.  
>   
> Some Ubuntu Linux distributions disable the `root` user and `/root` folder by default.  
> In these, your default user is `ubuntu`, using the `/home/ubuntu` folder.  
> You should then find your CRCON in `/home/ubuntu/hll_rcon_tool`.  
>   
> If so, you'll have to adapt the commands below accordingly.

- Log into your CRCON host machine using SSH and enter these commands (one line at at time) :  

  First part  
  If you already have installed any other "custom tools" from ElGuillermo, you can skip this part.  
  (though it's always a good idea to redownload the files, as they could have been updated)
  ```shell
  cd /root/hll_rcon_tool
  wget https://raw.githubusercontent.com/ElGuillermo/HLL_CRCON_restart/refs/heads/main/restart.sh
  mkdir custom_tools
  ```
  Second part
  ```shell
  cd /root/hll_rcon_tool/custom_tools
  wget https://raw.githubusercontent.com/ElGuillermo/HLL_CRCON_Live_topstats/refs/heads/main/hll_rcon_tool/custom_tools/live_topstats.py
  ```
- Edit `/root/hll_rcon_tool/rcon/hooks.py` and add these lines :
  - in the import part, on top of the file
    ```python
    import custom_tools.live_topstats as live_topstats
    ```
  - At the very end of the file
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
If any CRCON upgrade implies updating this file, the usual upgrade procedure, as given in official CRCON instructions, will ==FAIL==.  
To successfully upgrade your CRCON, you'll have to revert the changes back, then reinstall this plugin.  
To revert to the original file :  
```shell
cd /root/hll_rcon_tool
git restore rcon/hooks.py
```
