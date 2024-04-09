class archiver:
    """
    Class used to simplify interacting with archive.
    """
    def __init__(self, filepath: str):
        self.file = filepath
        self.archive = self.__readFile()
        self.to_add = []

    def __readFile(self):
        with open(self.file, 'r') as f:
            archive = f.readlines()
            f.close()
        return [i.split("\n")[0] for i in archive]

    def add(self, id):
        if id not in self.archive:
            self.toAdd.append(id)
    
    def save(self, file = "archive.txt"):
        to_add = [i for i in self.to_add if i not in self.archive]
        with open(file, 'a') as f:
            for i in to_add:
                f.write(f"{i}\n")
            f.close()