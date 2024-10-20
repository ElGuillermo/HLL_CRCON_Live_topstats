# HLL_CRCON_Topstats

A plugin for HLL CRCON (see : https://github.com/MarechJ/hll_rcon_tool)
that displays and rewards top players, based on their scores.

![375489308-67943815-da9c-41ff-988c-eaaa2e0e64c2](https://github.com/user-attachments/assets/e44d0f07-23a8-4f62-87c4-742803c8be06)

## Description
A plugin for HLL CRCON (see : https://github.com/MarechJ/hll_rcon_tool)
that displays and rewards top players, based on their scores.

The message may be called from `!top` chat command
or displayed at game's end.
VIPs will only be given at match's end.

Score values are agregated to reward the teamplay over the individual skills.
In hope the players who play for their team will enter the server more often
than the ones who play solo / never defend / don't earn support points.

There are 3 scores observed :
- (players and squads) offense * (defense * defense bonus)
- (players and squads) combat + (support * support bonus)
- (players only) kills / deaths ratio
- (players only) kills / min ratio

Only the players that enter the top of the two first scores can be rewarded with VIP.

As 'offense' and 'defense' values are based on the time the player spend on map
(20 points per minute), 'defense' value can be multiplied for a bonus.
So if two players spend the same time in game, the defender will be rewarded
before the one that mostly attacks.
It's a multiplicated value, so players will have to do both to enter the top,
thus avoiding to grant VIP to those that stay purposely at HQ the whole game.

Same for 'combat' and 'support' : commanders, officers, supports, engineers
and medics are rewarded as the ones who build and consolidate the teamplay.
So support value can be multiplied for a bonus.

Tankers don't get any VIP, as they (normally) have a huge combat score
and would easily get a VIP on each game.

## Installation
- Create `custom_tools` folder in CRCON's root (`/root/hll_rcon_tool/`) ;
- Copy `hooks_custom_topstats.py` in `/root/hll_rcon_tool/custom_tools/` ;
- Copy `restart.sh` in CRCON's root (`/root/hll_rcon_tool/`) ;
- Edit `/root/hll_rcon_tool/hooks.py` and add these lines:
  - in the import part, on top of the file
    ```python
    import custom_tools.hooks_custom_topstats as hooks_custom_topstats
    ```
  - At the very end of the file
    ```python
    @on_chat
    def topstats_onchat(rcon: Rcon, struct_log: StructuredLogLineWithMetaData):
        hooks_custom_topstats.stats_on_chat_command(rcon, struct_log)

    @on_match_end
    def topstats_onmatchend(rcon: Rcon, struct_log: StructuredLogLineWithMetaData):
        hooks_custom_topstats.stats_on_match_end(rcon, struct_log)
    ```
- Restart CRCON :
  ```shell
  cd /root/hll_rcon_tool
  sh ./restart.sh
  ```
Any change to the `/root/hll_rcon_tool/custom_tools/hooks_custom_topstats.py` or the `/root/hll_rcon_tool/hooks.py` file will need a CRCON restart with the above commands to be taken in account.