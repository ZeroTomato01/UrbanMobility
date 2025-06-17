from Models.User import User
from Models.Scooter import Scooter
from Validate import Validate
from Utils import Utility
from InitDB import InitDB
import sqlite3
import hashlib


class SeedDB:

    @staticmethod
    def Reset_db():
        InitDB.Del_userdb()
        InitDB.Del_scooterdb()
        InitDB.Del_travellerdb()
        InitDB.Del_logdb()
        InitDB.Init_userdb()
        InitDB.Init_scooterdb()
        InitDB.Init_travellerdb()
        InitDB.Init_logdb()
        InitDB.Init_SAdb()
        InitDB.Init_dummyusers()
        InitDB.Init_dummyscooters()
        InitDB.Init_dummytravellers()