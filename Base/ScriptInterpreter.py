import os
import json


class ScriptInterpreter(object):
    script = None

    @classmethod
    def load_script(cls, race):
        path_to_script = os.path.abspath("DB/scripts/script.json")
        print(path_to_script)
        with open(path_to_script) as file:
            cls.script = json.load(file)[race]
