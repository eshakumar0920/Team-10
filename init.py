from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.event import Event
from models.participant import Participant
