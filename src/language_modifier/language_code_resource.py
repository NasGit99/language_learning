from googletrans import LANGUAGES

def create_lang_codes():
    lang_dict = {}

    for code, name in LANGUAGES.items():
        lang_dict[code] = name

    return lang_dict

def validate_codes():

    language_code_map = create_lang_codes()

    while True:
        input_language = input("Type the language you are searching for or type exit to leave")

        if input_language.lower() == "exit":
            print("Exiting language search.")
            return None

        # Looking for valid language and returning the language code
        for code, language_name in language_code_map.items():
            if input_language.lower() in language_name.lower():
                return code
        
        print("No match found. Try another language or type 'exit' to quit.")


