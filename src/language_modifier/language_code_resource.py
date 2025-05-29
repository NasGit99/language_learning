import requests 
from bs4 import BeautifulSoup as bs

def create_lang_codes():
    url = "https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes"
    response = requests.get(url)
    soup = bs(response.content, 'html5lib')
    
    # Finding list of language codes for translate function

    table= soup.find('table', {'class' : 'wikitable'}, {'id' :"Table_of_all_possible_two-letter_codes"})

    lang_dict = {}

    for row in table.find_all("tr"):
        columns = row.find_all("td")
        if len(columns) >= 2:
            lang_name = columns[0].text.strip()
            lang_code = columns[1].text.strip()

            lang_dict[lang_code] = lang_name
    
    return lang_dict

def validate_codes(input_language):

    language_code_map = create_lang_codes()

    while True:
        # Looking for valid language and returning the language code
        for code, language_name in language_code_map.items():
            if input_language.lower() in language_name.lower():
                matched_code = code
                return(matched_code)
        
        input_language = input("No match found. Try another language or type exit to quit: ")   

        if input_language.lower == "exit":     
            break
        
        return None


