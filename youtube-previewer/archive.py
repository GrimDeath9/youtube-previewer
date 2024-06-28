class Archive:
    """
    Class used to simplify interacting with archive of already seen links.
    """
    def __init__(self, filepath: str):
        self.file = filepath
        self.archive = self.__read_archive()
        self.buffer = []
    
    def __enter__(self):
        return self

    def __read_archive(self) -> list[str]:
        with open(self.file, 'r') as f:
            archive = f.readlines()
            f.close()
        return [i.replace('\n', '') for i in archive]

    def add(self, id):
        self.buffer.append(id)
    
    def save(self):
        to_add = [i for i in self.buffer if i not in self.archive]
        with open(self.file, 'a') as f:
            for i in to_add:
                f.write(f'{i}\n')
            f.close()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()