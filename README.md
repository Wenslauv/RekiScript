## About

Reki is a script that helps you to check all decklists for Magic: the Gathering(tm) Historic Standard format on correctness.


## What is Historic Standard?

Historic Standard is a Magic: the Gathering variant format which allows any deck that was once (or currently is) standard to be played. You can pick Replenish from Urza's standard, Madness from Odyssey, Heartbeat Combo from Kamigawa, Dragonstorm from Time Spiral, Jund or Mythic from Shards of Alara, and Caw-Go/Blade from Zendikar.



## Installation

Script uses `Python v3.11` or higher.
Required modules can be found in requirements.txt



## Usage

All available standards are listed in `data/standards.json`. You can use it as is, or customise it to your needs. 

All decklists should be in `decklists/` folder in order to be found by script.

After that, just run 
```sh
python reki.py
```


#### Decklist format

Decklist should look like:

```
4 Adarkar Wastes
3 Dennick, Pious Apprentice
...
4 Deserted Beach
2 Destroy Evil

2 Disdainful Stroke
...
2 Sunfall
```

There's should be one or more empty line between main and sideboard part. No marks like `main` or `sideboard` required.
