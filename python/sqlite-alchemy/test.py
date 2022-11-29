from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
import bcrypt

Base = declarative_base()

class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location_id = Column(Integer, nullable=False) #FK
    #location FK

class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    #paths FK

    def check_paths(self, cmd):
        selected = None
        for path in paths:
            if (path.matches(cmd)):
                selected = path
        return selected

class Path(Base):
    __tablename__ = "path"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    source_location_id = Column(Integer, nullable=False) #FK
    destination_location_id = Column(Integer, nullable=False) #FK
    verbs = Column(String, nullable=False)
    nouns = Column(String, nullable=False)

    def matches(self, cmd):
        regex = f"{verbs}\s+{nouns}"
        return regex.matches(cmd) # incomplete sudo code

def create_all(engine):
    Base.metadata.create_all(engine)

class GateService:

    session = None
    player = None

    def __init__(self, database):
        # Establish connection the auth database file and create and missing tables
        engine = create_engine(f"sqlite:///{database}")
        create(engine)

        # Establish a Session with this database connection
        SessionMaker = sessionmaker()
        SessionMaker.configure(bind=engine)
        self.session = SessionMaker()
        self.__load_game_state()

    def __load_game_state(self):
        self.player = self.session.query(Player).filter(Player.id == 0).one_or_none()

    def __check_path(self, cmd: str):
        path = self.player.location.check_paths(cmd)
        if (path != None):
            self.player.location_id = path.destination_location_id
            # persist player to DB
            self.__load_game_state()

    def __look(self):
        return self.player.location.description

    def process_command(self, cmd: str):
        if (cmd == "look"):
            return self.__look()
        else:
            return __check_path(cmd)

    #def drop_user(self, username, password):

    def close(self):
        self.session.close()

gateService = GateService()
def game_loop():
    while True:
        # TODO: not sure about this...
        clear_screen()
        gateService.process_command("look")
        cmd = prompt()
        gateService.process_command(cmd)
    gateService.close()
