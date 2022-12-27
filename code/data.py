class AnswerType:
    identical = "identical"
    reversed = "reversed"
    distance_1 = "distance_1"
    distance_2 = "distance_2"
    distance_3 = "distance_3"


stimulus_category = ["male", "female"]
stimulus_names = {"male": ["Darek", "Olek", "Wojtek", "Edek", "Jacek", "Bronek", "Tomek", "Leszek"],
                  "female":  ["Hania", "Daria", "Basia", "Zuzia", "Olga", "Ada", "Fela", "Klara"]}

stimulus_types = {"male": [{"lower": "niższy niż", "higher": "wyższy niż", "type_name": "wzrost"},
                           {"lower": "młodszy niż", "higher": "starszy niż", "type_name": "wiek"},
                           {"lower": "chudszy niż", "higher": "grubszy niż", "type_name": "masa"},
                           {"lower": "wolniejszy niż", "higher": "szybszy niż", "type_name": "szybkosc"},
                           {"lower": "głupszy niż", "higher": "mądrzejszy niż", "type_name": "inteligencja"},
                           {"lower": "biedniejszy niż", "higher": "bogadszy niż", "type_name": "zamoznosc"}],
                  "female": [{"lower": "niższa niż", "higher": "wyższa niż", "type_name": "wzrost"},
                             {"lower": "młodsza niż", "higher": "starsza niż", "type_name": "wiek"},
                             {"lower": "chudsza niż", "higher": "grubsza niż", "type_name": "masa"},
                             {"lower": "wolniejsza niż", "higher": "szybsza niż", "type_name": "szybkosc"},
                             {"lower": "głupsza niż", "higher": "mądrzejsza niż", "type_name": "inteligencja"},
                             {"lower": "biedniejsza niż", "higher": "bogadsza niż", "type_name": "zamoznosc"}]}
