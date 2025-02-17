import tomllib

class Config:
    def __init__(self, filepath):
        data = tomllib.load(open(filepath, 'rb'))
        self.input = data['read']['read']
        self.database = data['read']['archive']
        self.check = data['output']['check']
        self.removed = data['output']['check']
        self.optimize = data['display']['optimize_layout']
        self.by_month = data['display']['group_by_month']
        self.misc = data['output']['misc']
        self.keybind = data['keybinds']

    def __str__(self) -> str:
        return str(self.__dict__)
    
    def __repr__(self) -> str:
        return str(self.__dict__)