from GameInstruction import *

file = ".venv\\"

configurations = json.loads(Path(f"{file}Game Data\\gamedata.json").read_text(encoding = "utf-8"))
Maps = json.loads(Path(f"{file}Game Data\\gamemaps.json").read_text())
view_distance = (45, 15)

while True :
    os.system("cls")
    main_menu = input("   Game Name\n   Start : S\n Controls : C\n Tutorial : T\n   Quit : Q\nEnter Choice : ").lower()
    if main_menu == "s" :
        while True : 
            os.system("cls")
            string = ""
            for key in Maps.keys() :
                string += f"   Map {key} : {key}\n"
            start_menu = input(f"{string}  Campain : C\n  Reload : R\n   Back : B\nEnter Choice : ").lower()
            if start_menu in Maps.keys() :
                start_game(configurations, Maps[start_menu], view_distance)
            elif start_menu == "c" :
                for Map in Maps.values() :
                    start_game(configurations, Map, view_distance)
            elif start_menu == "r" :
                Maps = json.loads(Path(".venv\\Game Data\\gamemaps.json").read_text())
                configurtions = json.loads(Path(f"{file}Game Data\\gamedata.json").read_text(encoding = "utf-8"))
            elif start_menu == "b" :
                break
        os.system("cls")
    elif main_menu == "c" :
        while True :
            os.system("cls")
            control_menu = input(f"        KeyBinds :\n         Up : W\n        Down : S\n       Right : D\n        Left : A\nView Distance : {view_distance}\n Change View Distance : C\n        Back : B\n     Enter Choice : ").lower()
            if control_menu == "c" :
                while True :
                    os.system("cls")
                    view_distance_menu = input(f"Previous View Distance : {view_distance}\n           Back : B\n          Change : C\n        Enter Choice : ").lower()
                    if view_distance_menu == "b" :
                        break
                    elif view_distance_menu == "c" :
                        try :
                            new_x = int(input("\n     View Distance X-Axis : "))
                            new_y = int(input("     View Distance Y-Axis : "))
                            if new_x > 0 and new_y > 0 :
                                view_distance = (new_x, new_y)
                            else :
                                if new_x < 1 :
                                    new_x = 1
                                if new_y < 1:
                                    new_y = 1
                                view_distance = (new_x, new_y)
                            if new_x < 91 and new_y < 91 :
                                view_distance = (new_x, new_y)
                            else :
                                if new_x > 91 :
                                    new_x = 91
                                if new_y > 27:
                                    new_y = 27
                                view_distance = (new_x, new_y)
                        except :
                            input("Enter Digits Not Text")
                os.system("cls")
                pass
            elif control_menu == "b" :
                break
        os.system("cls")
    if main_menu == "t" :
        while True :
            os.system("cls")
            tutorial_menu = input(" Dodge bullets and reach end.\nView distance is calculated as\n number of block from postion\n of player in each direction.\n           Back : B\n       Enter Choice : ").lower()
            if tutorial_menu == "b" :
                break
    if main_menu == "q" :
        break
    
os.system("cls")
print("Thanks for playing.")