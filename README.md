# pvz-farmer

A bot to farm coins in the Zen Garden and feed the Tree of Wisdom in Plants vs. Zombies.

The Zen Garden bot:

- satisfies the plants' needs (water, fertilizer, bug spray, music)
- buys fertilizer and bug spray when they run out
- picks up coins and diamonds produced by the plants

The Tree of Wisdom bot:

- gives food to the tree
- buys more food when it runs out
- ends when there's no money for more food

The combined farmer bot farms coins in the Zen Garden, then feeds the Tree of Wisdom.

---

The following instructions are relevant for Python 3.9.0 on Windows 10, with pip in PATH. If your setup is different, adjust the instructions accordingly.

## How to install

1. Download the source distribution.
2. Navigate to its location in the terminal and run `pip install pvz-farmer-1.0.0.tar.gz`.

## How to use

Open Plants vs. Zombies in an 800x600 window.

- For the Zen Garden farmer:

  1.  Enter the Zen Garden and make sure the panel with the watering can and other tools is visible.
  2.  Run `python -m pvz_farmer.zen_farmer [-l] frames` with the following arguments:

      - _frames_—how many frames should be dedicated to picking up coins in each loop (each frame lasts about 3 seconds)

      - [optional] _-l, --log-level_—logging level: DEBUG, INFO, WARNING, ERROR, or CRITICAL; default is INFO

- For the Tree of Wisdom farmer:

  1.  Enter the Tree of Wisdom area.

  2.  Run `python -m pvz_farmer.tow_farmer [-l]` with the following arguments:

      - [optional] _-l, --log-level_—logging level: DEBUG, INFO, WARNING, ERROR, or CRITICAL; default is INFO

- For the combined bot:

  1.  Enter the Zen Garden and make sure the panel with the watering can and other tools is visible.
  2.  Run `python -m pvz_farmer.pvz_farmer [-l] frames zen-garden` with the following arguments:

      - _frames_—how many frames should be dedicated to picking up coins in each loop (each frame lasts about 3 seconds)

      - _zen-garden_—how many loops should be dedicated to the Zen Garden before moving on to the Tree of Wisdom

      - [optional] _-l, --log-level_—logging level: DEBUG, INFO, WARNING, ERROR, or CRITICAL; default is INFO

To stop any of the bots, move your mouse to the top left corner of the screen.

![screenshot](screenshots/screenshot.gif)
