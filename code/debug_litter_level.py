"""One-off debug: dump raw Whisker API litter-level fields for each LR4.

Run:  python debug_litter_level.py > ..\debug_litter_output.txt
Credentials come from WHISKER_USERNAME / WHISKER_PASSWORD env vars
(same as litter_robot_v1.py). Safe to delete after use.
"""
import asyncio
import json
import os
import sys
from datetime import datetime


async def main() -> None:
    from pylitterbot import Account

    username = os.environ.get("WHISKER_USERNAME")
    password = os.environ.get("WHISKER_PASSWORD")
    if not (username and password):
        sys.exit("Set WHISKER_USERNAME / WHISKER_PASSWORD env vars first.")

    account = Account()
    try:
        await account.connect(username=username, password=password, load_robots=True)
        print(f"# Raw litter-level debug dump — {datetime.now():%Y-%m-%d %H:%M:%S}")
        for robot in account.robots:
            print(f"\n=== {robot.name} ({robot.serial}) ===")
            data = getattr(robot, "_data", {}) or {}
            keys = [
                "litterLevel", "litterLevelPercentage", "litterLevelState",
                "robotStatus", "DFILevelPercent", "isDFIFull",
                "odometerCleanCycles", "sensorHealth", "litterLevelStateOriginal",
            ]
            for k in keys:
                if k in data:
                    print(f"  {k:26s} = {data[k]!r}")
            # Library-computed views of the same data
            print(f"  {'litter_level (property)':26s} = {robot.litter_level!r}")
            try:
                print(f"  {'litter_level_calculated':26s} = {robot.litter_level_calculated!r}")
            except Exception as exc:
                print(f"  litter_level_calculated    = <error: {exc}>")
            # Full raw payload for reference
            print("\n  -- full raw _data --")
            print(json.dumps(data, indent=2, default=str))
    finally:
        await account.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
