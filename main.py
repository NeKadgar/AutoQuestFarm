from Base.SharkEye import SharkEye
from Base.WowWindow import WowWindow
from Path.PlayerDirection import record_points, move_to_point
from AddonData.WorldData import WorldData
from DB.Location import Location
from Base.ScriptInterpreter import ScriptInterpreter
from Base.utils import pretty_print
from Base.TelegramCore import TelegramCore

MENU_TEXT = '''
    Menu:
    1. Start
    2. Show all points on map by name
    3. Record new points
    4. Set NPC spawn polygon
    5. Setup Telegram
    0. Exit
    '''


if __name__ == "__main__":
    print('''
                    //World of Warcraft\\\\
    Hi, it's me, Pablo. From now we going to getting huge in this game.
    We at war
    We at war with terrorism, racism
    But most of all we at war with ourselves
    💀 👹 😈 🐸 💀 👹 😈 🐸 💀 👹 😈 🐸 💀 👹 😈 🐸 💀 👹 😈 🐸 
    Put a gun against his head, pulled my trigger, now he's dead
    🦋 🦋 🦋 🦋 🦋 🦋 🦋 🦋 🦋 🦋 🦋 🦋 🦋 🦋 🦋 🦋 🦋
    ''')
    session_name = str(input("Session name: "))
    WorldData.set_funcs(set_target=SharkEye.set_target, attack=SharkEye.attack, find_target=SharkEye.find_target,
                        move_to_point=move_to_point)
    while True:
        print(MENU_TEXT)
        f = str(input("Option: "))
        if f == "1":
            ScriptInterpreter.load_script("Human")
            WowWindow.set_focus()
            ScriptInterpreter.start()
        elif f == "2":
            pretty_print(Location.locations)
            Location.show_points_on_map(int(input("Location id: ")))
        elif f == "3":
            record_points()  # press ctrl to stop
        elif f == "4":
            pretty_print(Location.locations)
            Location.set_polygon(int(input("Location id: ")))  # set point mouse button 2, save right mouse button
        elif f == "5":
            TelegramCore.setup(session_name)
        elif f == "0":
            break
    print("Goodbye")
