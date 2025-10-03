from googletrans import Translator

async def translate_text(txt, dest) -> str:
     async with Translator() as translator:
        if len(txt) > 10000:
            raise ValueError("Max length is 10000 characters")
        translation = await translator.translate(txt, dest)
        return translation.text
     
async def translate_bulk(rows, dest):
   # Created for CSV function to preserve commas in strings
   translated_text =[]
   async with Translator() as translator:
      # Current CSV row limit to limit api requests
      if len(rows) > 100:
         raise ValueError("Max length is 100 rows")
      for row in rows:
         translations = await translator.translate(row, dest)
         translated_row =[t.text for t in translations]
         translated_text.append(translated_row)
   return translated_text
