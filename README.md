### Required packages

Go to [requirements](requirements.txt) to view the required PyPi packages.
Install packages onto your version of Python using the following terminal command (or install them manually if you're not a terminal kind of guy):
```console
pip3 install -r /path/to/KSP-AI-Project/requirements.txt
```

### How to Run

#### Required Programs
Install:
* [Kerbal Space Program](https://store.steampowered.com/app/220200/Kerbal_Space_Program/) (version 1.5.1)
* [CKAN mod manager](https://github.com/KSP-CKAN/CKAN/releases/tag/v1.26.6)
* Python 3
    * also pip

#### After Installing
1. Revert Kerbal Space Program version to 1.5.1
    1. Under the Kerbal Space Program Tab, click the gear icon
    2. In the properties menu, select “Betas”
    3. In the drop-down menu select “1.5.1 - Kerbal Space Program”
    4. Wait for Steam to update the files to 1.5.1
    5. At this point, it may be smart to launch Kerbal Space Program once to see that the game loads correctly, and then close it. 
2. Add the kRPC mod to KSP
    1. Execute the CKAN mod manager for Kerbal Space program (attached with this submission or downloaded from link above)
    2. In the search bar in CKAN search for “KRPC” and select the install checkbox on the mod that matches the description for KRPC. 
    3. Click “Apply Changes” and wait for changes to be applied and close.
3. Run Kerbal Space Program
4. Load the saved game “SHgame” (or create one with this name if you don't have it)
5. From the root folder (KSP-AI-Project) start the code using the command: 
```console
python3 src/test.py src/neat-checkpoint-338
```
6. Watch the rocket!
