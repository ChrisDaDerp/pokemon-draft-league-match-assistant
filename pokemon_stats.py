'''
This script will gather all the stats of Pokémon you supply it with and print out
in a table (ordered by any stat you want; default is speed) with all stats of all the Pokémon.
This will be very useful for draft leagues so you don't have to calculate the
speed of every single Pokémon you will be facing individually.
This script is up to date for up to Gen IX, as of 2023-06-11.

@Author ChrisDaDerp
'''

import requests
from math import floor
# Tabulate makes the table look nice.
from tabulate import tabulate
# Colorama allows for color printing in more terminals than ANSI escape codes.
import colorama

# Indexes of stats from the API call.
HP = 0
ATTACK = 1
DEFENSE = 2
SP_ATTACK = 3
SP_DEFENSE = 4
SPEED = 5

# Values for stat calculations.
# These values are all the maximum possible.
IV = 31
EV = 252
NATURE = 1.1
LEVEL = 100

# Formatting for printing to terminal.
RED = colorama.Fore.RED
BLUE = colorama.Fore.BLUE
BOLD = "\033[1m"
END = "\033[0m"

# Common names that may probably be typo'd because of how PokeAPI stores them.
# Also some common shorthands for Pokémon that may be entered for convenience.
# These will be assumed names and may not be what are desired. Writing the exact name will bypass the assumption.
COMMON_NAMES = {}
COMMON_NAMES["nidoran"] = "nidoran-m"
COMMON_NAMES["farfetch'd"] = "farfetchd"
COMMON_NAMES["mrmime"] = "mr-mime"
COMMON_NAMES["mr.mime"] = "mr-mime"
COMMON_NAMES["skarm"] = "skarmory"
COMMON_NAMES["deoxys"] = "deoxys-normal"
COMMON_NAMES["deoxys-n"] = "deoxys-normal"
COMMON_NAMES["deoxys-a"] = "deoxys-attack"
COMMON_NAMES["deoxys-d"] = "deoxys-defense"
COMMON_NAMES["deoxys-s"] = "deoxys-speed"
COMMON_NAMES["wormadam"] = "wormadam-plant"
COMMON_NAMES["mimejr"] = "mime-jr"
COMMON_NAMES["mime.jr"] = "mime-jr"
COMMON_NAMES["giratina"] = "giratina-origin"
COMMON_NAMES["giratina-a"] = "giratina-altered"
COMMON_NAMES["giratina-o"] = "giratina-origin"
COMMON_NAMES["shaymin"] = "shaymin-sky"
COMMON_NAMES["shaymin-l"] = "shaymin-land"
COMMON_NAMES["shaymin-s"] = "shaymin-land"
COMMON_NAMES["basculin"] = "basculin-red-striped"
COMMON_NAMES["darmanitan"] = "darmanitan-standard"
COMMON_NAMES["darm"] = "darmanitan-standard"
COMMON_NAMES["darmanitan-s"] = "darmanitan-standard"
COMMON_NAMES["darm-s"] = "darmanitan-standard"
COMMON_NAMES["darmanitan-z"] = "darmanitan-zen"
COMMON_NAMES["darm-z"] = "darmanitan-zen"
COMMON_NAMES["tornadus"] = "tornadus-therian"
COMMON_NAMES["tornadus-t"] = "tornadus-therian"
COMMON_NAMES["tornadus-i"] = "tornadus-incarnate"
COMMON_NAMES["thundurus"] = "thundurus-incarnate"
COMMON_NAMES["thundurus-i"] = "thundurus-incarnate"
COMMON_NAMES["thundurus-t"] = "thundurus-therian"
COMMON_NAMES["landorus"] = "landorus-therian"
COMMON_NAMES["landorus-t"] = "landorus-therian"
COMMON_NAMES["landot"] = "landorus-therian"
COMMON_NAMES["lando-t"] = "landorus-therian"
COMMON_NAMES["landorus-i"] = "landorus-incarnate"
COMMON_NAMES["keldeo"] = "keldeo-ordinary"
COMMON_NAMES["meloetta"] = "meloetta-aria"
COMMON_NAMES["meloetta-a"] = "meloetta-aria"
COMMON_NAMES["meloetta-p"] = "meloetta-pirouette"
COMMON_NAMES["meowstic"] = "meowstic-male"
COMMON_NAMES["pumpkaboo"] = "pumpkaboo-base"
COMMON_NAMES["gourgeist"] = "gourgeist-base"
COMMON_NAMES["zygarde"] = "zygarde-base"
COMMON_NAMES["zygarde-b"] = "zygarde-base"
COMMON_NAMES["zygarde-c"] = "zygarde-complete"
COMMON_NAMES["zygarde-10"] = "zygarde-10"
COMMON_NAMES["oricorio"] = "oricorio-baile"
COMMON_NAMES["oricorio-b"] = "oricorio-baile"
COMMON_NAMES["oricorio-pp"] = "oricorio-pom-pom"
COMMON_NAMES["oricorio-pa"] = "oricorio-pau"
COMMON_NAMES["oricorio-s"] = "oricorio-sensu"
COMMON_NAMES["lycanroc"] = "lycanroc-dusk"
COMMON_NAMES["lycanroc-d"] = "lycanroc-dusk"
COMMON_NAMES["lycanroc-md"] = "lycanroc-midday"
COMMON_NAMES["lycanroc-mn"] = "lycanroc-midnight"
COMMON_NAMES["wishiwashi"] = "wishiwashi-school"
COMMON_NAMES["type:null"] = "type-null"
COMMON_NAMES["type_null"] = "type-null"
COMMON_NAMES["typenull"] = "type-null"
COMMON_NAMES["minior"] = "minior-core"
COMMON_NAMES["minior-c"] = "minior-core"
COMMON_NAMES["minior-m"] = "minior-meteor"
COMMON_NAMES["mimikyu"] = "mimikyu-disguised"
COMMON_NAMES["necrozma-dusk"] = "necrozma-dusk-mane"
COMMON_NAMES["necrozma-dawn"] = "necrozma-dawn-wings"
COMMON_NAMES["rattata-a"] = "rattata-alola"
COMMON_NAMES["raticate-a"] = "raticate-alola"
COMMON_NAMES["raichu-a"] = "raichu-alola"
COMMON_NAMES["sandshrew-a"] = "sandshrew-alola"
COMMON_NAMES["sandslash-a"] = "sandslash-alola"
COMMON_NAMES["vulpix-a"] = "vulpix-alola"
COMMON_NAMES["nintales-a"] = "ninetales-alola"
COMMON_NAMES["diglett-a"] = "diglett-alola"
COMMON_NAMES["dugtrio-a"] = "dugtrio-alola"
COMMON_NAMES["meowth-a"] = "meowth-alola"
COMMON_NAMES["persian-a"] = "persian-alola"
COMMON_NAMES["geodude-a"] = "geodude-alola"
COMMON_NAMES["graveler-a"] = "graveler-alola"
COMMON_NAMES["golem-a"] = "golem-alola"
COMMON_NAMES["grimer-a"] = "grimer-alola"
COMMON_NAMES["muk-a"] = "muk-alola"
COMMON_NAMES["exeggutor-a"] = "exeggutor-alola"
COMMON_NAMES["marowak-a"] = "marowak-alola"
COMMON_NAMES["tapukoko"] = "tapu-koko"
COMMON_NAMES["koko"] = "tapu-koko"
COMMON_NAMES["tapulele"] = "tapu-lele"
COMMON_NAMES["lele"] = "tapu-lele"
COMMON_NAMES["tapubulu"] = "tapu-bulu"
COMMON_NAMES["bulu"] = "tapu-bulu"
COMMON_NAMES["tapufini"] = "tapu-fini"
COMMON_NAMES["fini"] = "tapu-fini"
COMMON_NAMES["toxtricity"] = "toxtricity-amped"
COMMON_NAMES["zigzagoon-g"] = "zigzagoon-galar"
COMMON_NAMES["linoone-g"] = "linoone-galar"
COMMON_NAMES["meowth-g"] = "meowth-galar"
COMMON_NAMES["ponyta-g"] = "ponyta-galar"
COMMON_NAMES["rapidash-g"] = "rapidash-galar"
COMMON_NAMES["slowpoke-g"] = "slowpoke-galar"
COMMON_NAMES["slowbro-g"] = "slowbro-galar"
COMMON_NAMES["slowking-g"] = "slowking-galar"
COMMON_NAMES["corsola-g"] = "corsola-galar"
COMMON_NAMES["farfetch'd-g"] = "farfetchd-galar"
COMMON_NAMES["farfetchd-g"] = "farfetched-galar"
COMMON_NAMES["sirfetch'd"] = "sirfetchd"
COMMON_NAMES["weezing-g"] = "weezing-galar"
COMMON_NAMES["mrmime-g"] = "mr-mime-galar"
COMMON_NAMES["mr.mime-g"] = "mr-mime-galar"
COMMON_NAMES["mrrime"] = "mr-rime"
COMMON_NAMES["mr.rime"] = "mr-rime"
COMMON_NAMES["darumaka-g"] = "darumaka-galar"
COMMON_NAMES["darmanitan-g"] = "darmanitan-galar-standard"
COMMON_NAMES["darm-g"] = "darmanitan-galar-standard"
COMMON_NAMES["darmanitan-g-s"] = "darmanitan-galar-standard"
COMMON_NAMES["darm-g-s"] = "darmanitan-galar-standard"
COMMON_NAMES["darmanitan-g-z"] = "darmanitan-galar-zen"
COMMON_NAMES["darm-g-z"] = "darmanitan-galar-zen"
COMMON_NAMES["yamask-g"] = "yamask-galar"
COMMON_NAMES["stunfisk-g"] = "stunfisk-galar"
COMMON_NAMES["eiscue"] = "eiscue-ice"
COMMON_NAMES["eiscue-n"] = "eiscue-noice"
COMMON_NAMES["indeedee"] = "indeedee-male"
COMMON_NAMES["indeedee-m"] = "indeedee-male"
COMMON_NAMES["indeedee-f"] = "indeedee-female"
COMMON_NAMES["morpeko"] = "morpeko-full-belly"
COMMON_NAMES["morpeko-f"] = "morpeko-full-belly"
COMMON_NAMES["morpeko-h"] = "morpeko-hangry"
COMMON_NAMES["pult"] = "dragapult"
COMMON_NAMES["urshifu"] = "urshifu-single-strike"
COMMON_NAMES["urshifu-s"] = "urshifu-single-strike"
COMMON_NAMES["urshifu-ss"] = "urshifu-single-strike"
COMMON_NAMES["urshifu-r"] = "urshifu-single-strike"
COMMON_NAMES["urshifu-rs"] = "urshifu-single-strike"
COMMON_NAMES["eleki"] = "regieleki"
COMMON_NAMES["leki"] = "regieleki"
COMMON_NAMES["drago"] = "regidrago"
COMMON_NAMES["articuno-g"] = "articuno-galar"
COMMON_NAMES["zapdos-g"] = "zapdos-galar"
COMMON_NAMES["moltres-g"] = "moltres-galar"
# I can't find how the Paldean Tauros forms are stored on PokeAPI so I am excluding them.
COMMON_NAMES["wooper-p"] = "wooper-paldea"
COMMON_NAMES["palafin-h"] = "palafin-hero"
COMMON_NAMES["greattusk"] = "great-tusk"
COMMON_NAMES["tusk"] = "great-tusk"
COMMON_NAMES["screamtail"] = "scream-tail"
COMMON_NAMES["brutebonnet"] = "brute-bonnet"
COMMON_NAMES["fluttermane"] = "flutter-mane"
COMMON_NAMES["mane"] = "flutter-mane"
COMMON_NAMES["slitherwing"] = "slither-wing"
COMMON_NAMES["sandyshocks"] = "sandy-shocks"
COMMON_NAMES["irontreads"] = "iron-treads"
COMMON_NAMES["treads"] = "iron-treads"
COMMON_NAMES["ironbundle"] = "iron-bundle"
COMMON_NAMES["bundle"] = "iron-bundle"
COMMON_NAMES["ironhands"] = "iron-hands"
COMMON_NAMES["hands"] = "iron-hands"
COMMON_NAMES["ironjugulis"] = "iron-jugulis"
COMMON_NAMES["jugulis"] = "iron-jugulis"
COMMON_NAMES["ironmoth"] = "iron-moth"
COMMON_NAMES["moth"] = "iron-moth"
COMMON_NAMES["ironthorns"] = "iron-thorns"
COMMON_NAMES["thorns"] = "iron-thorns"
COMMON_NAMES["wochien"] = "wo-chien"
COMMON_NAMES["chienpao"] = "chien-pao"
COMMON_NAMES["tinglu"] = "ting-lu"
COMMON_NAMES["chiyu"] = "chi-yu"
COMMON_NAMES["roaringmoon"] = "roaring-moon"
COMMON_NAMES["moon"] = "roaring-moon"
COMMON_NAMES["ironvaliant"] = "iron-valiant"
COMMON_NAMES["valiant"] = "iron-valiant"
COMMON_NAMES["walkingwake"] = "walking-wake"
COMMON_NAMES["wake"] = "walking-wake"
COMMON_NAMES["ironleaves"] = "iron-leaves"
COMMON_NAMES["leaves"] = "iron-leaves"


class Pokemon:
    '''
    Pokémon object to track name and stats.
    Stores base stats, calculated stats, and Choice Scarfed speed stat.
    Can also make Pokémon names print pretty in the table.
    Change what stats will be compared when ordering the table by changing self.__compare_stat.
    '''
    def __init__(self, name, is_my_team):
        self.__name = name.lower()
        # Replaces name with assumed name to avoid errors from mistakes.
        if name.lower() in COMMON_NAMES:
            self.__name = COMMON_NAMES[name]

        pokemon = requests.get("https://pokeapi.co/api/v2/pokemon/" + self.__name.lower())
        # If the API returns data, the Pokemon object is made.
        if self.__name != "" and pokemon.status_code == 200:
            self.__pokemon = pokemon.json()
            self.__is_valid = True
            self.__base_hp = self.__get_base_stat(HP)
            self.__base_attack = self.__get_base_stat(ATTACK)
            self.__base_defense = self.__get_base_stat(DEFENSE)
            self.__base_sp_attack = self.__get_base_stat(SP_ATTACK)
            self.__base_sp_defense = self.__get_base_stat(SP_DEFENSE)
            self.__base_speed = self.__get_base_stat(SPEED)

            self.__hp = self.__calculate_hp()
            self.__attack = self.__calculate_stat(self.__base_attack)
            self.__defense = self.__calculate_stat(self.__base_defense)
            self.__sp_attack = self.__calculate_stat(self.__base_sp_attack)
            self.__sp_defense = self.__calculate_stat(self.__base_sp_defense)
            self.__speed = self.__calculate_stat(self.__base_speed)
            self.__scarf = self.__calculate_scarf()

            # This is what stat will be used to compare Pokémon to sort the table.
            self.__compare_stat = self.__speed

            self.__pretty_name = self.__parse_name(self.__name)

            # For setting text color for printing to terminal.
            if is_my_team: 
                self.__text_color = RED
            else:
                self.__text_color = BLUE

        # If the API does not return data, the Pokemon object is flagged as invalid.
        else:
            self.__is_valid = False
            if self.__name == "":
                print(RED + BOLD + "No Pokémon was entered. Continuing.")
            else:
                link = 'https://pokeapi.co/'
                print(RED + BOLD + "ERROR: '" + self.__name + "' was not found when consulting PokeAPI (" + 
                            link + END + RED + 
                            "). Check for a typo, or if the Pokémon has alternate forms." + END)

    def __parse_name(self, name):
        '''
        Makes the Pokémon's name look pretty instead of in all lowercase.
        For example, "Landorus-Therian" instead of "landorus-therian" or "Roaring Moon" instead of "roaring-moon".
        '''
        # Names with special characters.
        if name == "mime-jr":
            return "Mime Jr."
        elif name == "mr-mime":
            return "Mr. Mime"
        elif name == "farfetchd":
            return "Farfetch'd"
        elif name == "sirfetchd":
            return "Sirfetch'd"
        elif name == "flabebe":
            return "Flabébé"
        elif name == "type-null":
            return "Type: Null"
        elif name == "mr-rime":
            return "Mr. Rime"
    
        # Names without anything special.
        if len(name.split("-")) == 1:
            return (name[0].upper()) + name[1:]
        
        # All Pokémon with alternate forms.
        hyphenated_names = ["ho-oh", "porygon-z", "wo-chien", "chi-yu", "chien-pao", "ting-lu"]
        alternate_forms = ["nidoran", "tauros", "castform", "kyogre", "groudon", "deoxys", "burmy", "wormadam", "cherrim", "rotom", "dialga", "palkia", "giratina",
                           "shaymin", "basculin", "darmanitan", "tornadus", "thundurus", "landorus", "enamorus", "kyruem", "keldeo", "meloetta", "greninja", "aegislash",
                           "pumpkaboo", "gourgeist", "zygarde", "hoopa", "lycanroc", "jangmo-o", "hakamo-o", "kommo-o" "wishiwashi", "minior", "necrozma", "toxtricity",
                           "eiscue", "zacian", "zamazenta", "eternatus", "urhsifu", "calyrex", "palafin", "gimmighoul"]
        region_names = ["mega", "alola", "galar", "hisui", "paldea"]
        
        # Names with multiple parts and/or without special characters.
        pretty_name = ""
        i = 1
        for part in name.split("-"):
            pretty_name += (part[0].upper()) + part[1:]
            if i < len(name.split("-")):
                if name in hyphenated_names:
                    pretty_name += "-"
                else:
                    found = False
                    for form in alternate_forms:
                        if form in name:
                            pretty_name += "-"
                            found = True
                    if not found:
                        for region in region_names:
                            if region in name:
                                pretty_name += "-"
                                found = True
                    if not found:
                        pretty_name += " "
            i += 1
        return pretty_name


    def __get_base_stat(self, stat):
        '''Gets base stat from PokeAPI and sets it.'''
        return int(self.__pokemon["stats"][stat]["base_stat"])
    
    def __calculate_hp(self):
        '''Calculates the HP the Pokémon will have at level LEVEL based on the HP formula.'''
        # Shedinja always has 1 HP, which technically goes against the HP formula.
        if self.__name == "shedinja":
            return 1
        
        # HP calculation formula.
        return floor((2 * self.__base_hp + IV + floor(EV/4)) * LEVEL / 100 + LEVEL + 10)


    def __calculate_stat(self, base_stat):
        '''
        Sets the actual stat that the Pokémon will have at level LEVEL based on the standard stat formula.
        Note that it is impossible to have all of these stats at once due to how natures and EVs work.
        '''
        # Pokémon stat calculation formula. Cannot be used for HP as it uses a different formula.
        return floor(floor((2 * base_stat + IV + floor(EV/4)) * LEVEL / 100 + 5) * NATURE)
    
    def __calculate_scarf(self):
        '''Calculates the speed of a Pokémon holding a Choice Scarf.'''
        return floor(self.__speed * 1.5)

    
    def get_pokemon_list(self):
        '''Returns list of all Pokémon stats, plus scarfed speed stat.'''
        return [self.__text_color +
                self.__pretty_name,
                BOLD + str(self.__hp) + END + self.__text_color + " / " + str(self.__base_hp),
                BOLD + str(self.__attack) + END + self.__text_color + " / " + str(self.__base_attack),
                BOLD + str(self.__defense) + END + self.__text_color + " / " + str(self.__base_defense),
                BOLD + str(self.__sp_attack) + END + self.__text_color + " / " + str(self.__base_sp_attack),
                BOLD + str(self.__sp_defense) + END + self.__text_color + " / " + str(self.__base_sp_defense),
                BOLD + str(self.__speed) + END + self.__text_color + " / " + str(self.__base_speed),
                BOLD + str(self.__scarf) +
                END]
    
    def is_valid(self):
        '''A Pokémon is valid if it was found in the PokeAPI database.
        Otherwise there was no data returned for it and it cannot be used.
        '''
        return self.__is_valid

    def __eq__(self, other):
        return self.__compare_stat == other.__compare_stat and self.__compare_stat == other.__compare_stat

    def __lt__(self, other):
        return self.__compare_stat < other.__compare_stat


def parse_team(pokemon_list, is_my_team):
    '''Creates a team of Pokemon objects.'''
    team = {}
    pokemon_list = pokemon_list.replace(" ", "").split(",")
    for pokemon in pokemon_list:
        team[pokemon] = Pokemon(pokemon, is_my_team)
    return team


def compare_teams(my_team, opponent_team):
    '''Creates a list of Pokemon from both teams and sorts them by stat.'''
    every_pokemon = []
    for pokemon in my_team:
        if my_team[pokemon].is_valid():
            every_pokemon.append(my_team[pokemon])
    for pokemon in opponent_team:
        if opponent_team[pokemon].is_valid():
            every_pokemon.append(opponent_team[pokemon])
    
    return sorted(every_pokemon, reverse=True)


def print_pokemon_list(sorted_pokemon_list):
    '''Prints the Pokémon and the selected stat in order and in a clearly legible way.'''
    # Error handler, so an empty table isn't printed.
    if len(sorted_pokemon_list) == 0:
        print(RED + BOLD + "ERROR: No valid Pokémon were provided. Please try again.")
        return

    # A table of all valid Pokémon will be printed.
    header = ["Pokémon", "HP", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed", "Scarfed Speed"]
    pokemon_stats_list = []
    for i in range(0, len(sorted_pokemon_list)):
        pokemon_stats_list.append(sorted_pokemon_list[i].get_pokemon_list())
        
    print(RED + BOLD +
          "NOTE: It is impossible for a Pokémon to have all of these stats at once due to how natures and EVs work." +
          END)
    table = tabulate(pokemon_stats_list, headers=header, tablefmt="psql")
    print(table)
    
        
def main():
    mine, opponent = True, False
    my_team = parse_team(input("Write the names of the Pokémon on" + RED + " your team" + END + ", separated by comma: "), mine)
    opponent_team = parse_team(input("Write the names of the Pokémon on" + BLUE + " your opponent's team" + END + ", separated by comma: "), opponent)
    sorted_pokemon_list = compare_teams(my_team, opponent_team)

    print_pokemon_list(sorted_pokemon_list)
    input("Press any key to exit...")


if __name__ == "__main__":
    main()