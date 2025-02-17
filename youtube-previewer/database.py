import sqlite3
from pyet import VideoInfo

class Data:
    """
    Class used to simplify interacting with the video data cache and archive.
    """
    def __init__(self, filepath = "./instance/history.db"):
        self.file = filepath
        self.connection = sqlite3.connect(filepath)
        self.cursor = self.connection.cursor()
        self.exists_string = "SELECT exists(SELECT 1 FROM {} WHERE id='{}')"
        self.__initalize_db()

    def __initalize_db(self): 
        self.cursor.execute("PRAGMA foreign_keys = ON")
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Videos(
            id	            TEXT NOT NULL PRIMARY KEY,
            checked	        INTEGER NOT NULL,
            archive_date	TEXT,
            status	        TEXT NOT NULL,
            title	        TEXT,
            duration	    TEXT,
            upload_date	    TEXT,
            author_id	    TEXT
        ''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Authors(
            id  	TEXT NOT NULL PRIMARY KEY,
            name	TEXT NOT NULL,
            FOREIGN KEY("id") REFERENCES "Videos"("author_id")
        );''')
        self.cursor.execute('''CREATE VIEW IF NOT EXISTS Seen AS SELECT 
            id,title,duration,upload_date,author_id FROM Videos WHERE checked=1
        ''')
        self.cursor.execute('''CREATE VIEW IF NOT EXISTS New AS SELECT 
            id,title,duration,upload_date,author_id FROM Videos WHERE checked=1
        ''')
    
    def archive(self, video_id: str):
        self.cursor.execute(f"UPDATE Videos SET checked=1, archive_date=DATETIME('now') WHERE id={video_id}")

    def add(self, video: VideoInfo):
        if self.cursor.execute(self.exists_string.format('Videos',video.id)).fetchone() == (0,):
            self.cursor.execute(f"""INSERT INTO Videos(id,checked,status,title,duration,upload_date,author_id) VALUES
                ('{video.id}',0,'{video.status}','{video.title}','{video.duration}','{video.upload_date}',
                '{video.author_id}')""")
            if self.cursor.execute(self.exists_string.format('Authors',video.author_id)).fetchone() == (0,):
                self.cursor.execute(f"INSERT INTO Authors(id, name) VALUES ('{video.author_id}','{video.author}')")
            self.connection.commit()
    
    def get_saved(self):
        return self.cursor.execute("SELECT * FROM Seen").fetchall()
    
    def get_new(self):
        return self.cursor.execute("SELECT * FROM New").fetchall()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()