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
        input_text = ctx.input

        status, text = await util.tg.get_text_input(ctx, input_text)
        if not status:
            if isinstance(text, str):
                return text
            return "__Unknown error.__"

        detectlang = tl.detect(text)

        try:
            tekstr = tl.translate(text, dest=input_text)
        except ValueError as err:
            return ("Error: `{}`".format(str(err)))
        return "Translate from `{}` to `{}`:\n```{}```".format(detectlang.lang, input_text, tekstr.text)
