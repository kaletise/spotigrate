import json
import os


class Config:
    def __init__(self, file, default={}, auto_init=True,
                 indent=4, sort_keys=True):
        self.file = file
        self.default = default
        self.data = {}
        self.indent = indent
        self.sort_keys = sort_keys
        self.first_init = False
        if auto_init:
            self.init()

    def init(self):
        if os.path.isfile(self.file):
            self.load()
        else:
            self.first_init = True
            self.data = self.default
            self.save()

    def get(self, key):
        if key in self.data.keys():
            return self.data[key]
        if key in self.default.keys():
            return self.default[key]

    def set(self, key, value):
        self.data[key] = value

    def save(self):
        with open(self.file, 'w') as file:
            file.write(json.dumps(
                self.data, indent=self.indent, sort_keys=self.sort_keys
            ))

    def load(self):
        if not os.path.isfile(self.file):
            return False
        try:
            with open(self.file) as file:
                self.data = json.load(file)
        except json.decoder.JSONDecodeError:
            return False
