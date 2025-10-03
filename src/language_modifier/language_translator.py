from googletrans import Translator

async def translate_text(txt, dest) -> str:
     async with Translator() as translator:
        translation = await translator.translate(txt, dest)
        return translation.text
     
async def translate_bulk(rows, dest):
   # Created for CSV function to preserve commas in strings
   translated_text =[]
   async with Translator() as translator:
      for row in rows:
         translations = await translator.translate(row, dest)
         translated_row =[t.text for t in translations]
         translated_text.append(translated_row)
   return translated_text
