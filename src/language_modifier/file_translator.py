from translate import Translator
import requests 

def translate_text (txt, language) -> str:
    translator= Translator(to_lang=language)
    translation = translator.translate(txt)
    
    return(translation)



