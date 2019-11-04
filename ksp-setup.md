# Setting Up KSP with kRPC

_Note: setup instructions for kRPC can be found [here](https://krpc.github.io/krpc/getting-started.html)_

1. install Kerbal Space Program via Steam (give it a run to make sure it works)
2. go to [kRPC setup](https://krpc.github.io/krpc/getting-started.html) and click on the Github link to download the .zip for the mod
3. unzip the mod into the KSP GameData folder, usually `C:\Users\you\ProgramFiles (x86)\Steam\steamapps\common\Kerbal SpaceProgram\GameData`. Make sure you unzip the contents into a folder called **krpc-0.4.8**.
4. start KSP
5. start a new game
6. you should see a window called kRPC v0.4.x. Some of the icons may be broken due to incompatible versioning.
7. Now you're ready to set up python. Get python downloaded/setup and install pip's `krpc`, `pyautogui`, and `neat-python`.
```console
$ pip3 install krpc
$ pip3 install pyautogui
$ pip3 install neat-python
```
8. create a new file in your cloned version of [David's git repo](https://github.com/Dcbaas/KSP-AI-Project) or another location on your computer that you can run from. I used PyCharm, but VS Code is a more lightweight option. Or if you can get a bash shell going on windows (or whichever OS you're using), that would probably be better.
9. the following code should get you started:
```python
import krpc

def main():
	conn = krpc.connect(name='Hello World')
	vessel = conn.space_center.active_vessel
	print(vessel.name)

if __name__ == '__main__':
	main()
```
10. make sure you have KSP running (probably best to be at the launchpad in game) and start the server from the kRPC window in the game
11. run your python file, the name 'Hello World' should show up under the server IP and ports in the game's kRPC window.
12. theoretically, the name of your vessel (AeroEquus) should print out. I was unsuccessful with this, but was able to get the rocket to launch using code from [their tutorial](https://krpc.github.io/krpc/tutorials/launch-into-orbit.html). If you're having trouble, try stopping and starting the server, making sure the name given in `krpc.connect()` is showing up in the kRPC window with your local ip (127.0.0.1).
