"""
Translate
Author: alanndz alanmahmud0@gmail.com
"""

from googletrans import Translator
from pyrobud import command, module, util

tl = Translator()

class Translate(module.Module):
    name: str="Translate"
    disabled: bool= False

    @command.desc("Translate")
    @command.alias("tr")
    @command.usage("[lang]", reply=True)
    async def cmd_translate(self, ctx: command.Context) -> str:
        lang = ctx.input

        if not lang:
            return "Enter lang to translate, example: `en, id`"

        text = ctx.msg.get_reply_message()
        if text.file:
            return "Is file, cant translate, please reply a message"

        detectlang = tl.detect(text)

        try:
            tekstr = tl.translate(text, dest=lang)
        except ValueError as err:
            return "Error: `{}`".format(str(err))

        return "Translate from `{}` to `{}`:\n```{}```".format(detectlang.lang, lang, tekstr.text)
