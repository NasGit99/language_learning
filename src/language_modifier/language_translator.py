from googletrans import Translator

async def translate_text(txt, dest) -> str:
     async with Translator() as translator:
        result = await translator.translate(txt, dest)
        return result.text
