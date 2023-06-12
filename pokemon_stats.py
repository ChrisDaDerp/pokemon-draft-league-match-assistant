'''
This script will gather all the stats of Pokémon you supply it with and print out
in a table (ordered by any stat you want; default is speed) with all stats of all the Pokémon.
This will be very useful for draft leagues so you don't have to calculate the
speed of every single Pokémon you will be facing individually.

@Author ChrisDaDerp
'''

import requests
from math import floor
# Tabulate makes the table look nice.
from tabulate import tabulate

# Indexes of stats from the API call.
HP = 0
ATTACK = 1
DEFENSE = 2
SP_ATTACK = 3
SP_DEFENSE = 4
SPEED = 5

# Values for stat calculations.
IV = 31
EV = 252
NATURE = 1.1
LEVEL = 100

# Formatting for printing to terminal.
RED = "\u001b[31m"
BLUE = "\u001b[34m"
BOLD = "\033[1m"
END = "\033[0m"


class Pokemon:
    '''
    Pokémon object to track name and stats.
    Stores base stats, calculated stats, and Choice Scarfed speed stat.
    Can also make Pokémon names print pretty in the table.
    Change what stats will be compared when ordering the table by changing self.__compare_stat.
    '''
    def __init__(self, name, is_my_team):
        self.__name = name.lower()

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
                print(RED + BOLD + "No Pokémon were entered. Continuing.")
            else:
                link = 'https://pokeapi.co/'
                print(RED + BOLD + "ERROR: '" + self.__name + "' was not found when consulting PokeAPI (" + 
                            link + END + RED + 
                            "). Check for a typo, or if the Pokémon has alternate forms. (E.g. 'landorus' should either be 'landorus-incarnate' or 'landorus-therian'.)" + END)

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
        alternate_forms = ["tauros", "castform", "kyogre", "groudon", "deoxys", "burmy", "wormadam", "cherrim", "rotom", "dialga", "palkia", "giratina",
                           "shaymin", "basculin", "darmanitan", "tornadus", "thundurus", "landorus", "enamorus", "kyruem", "meloetta", "greninja", "aegislash",
                           "pumpkaboo", "gourgeist", "zygarde", "hoopa", "lycanroc", "wishiwashi", "minior", "necrozma", "toxtricity", "eiscue", "zacian",
                           "zamazenta", "eternatus", "urhsifu", "calyrex", "palafin", "gimmighoul"]
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


if __name__ == "__main__":
    main()