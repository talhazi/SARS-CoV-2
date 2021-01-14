# The Repository
import atexit
import os
import sqlite3
from DAO import _Vaccines, _Suppliers, _Clinics, _Logistics, _Summarys


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccine = _Vaccines(self._conn)
        self.supplier = _Suppliers(self._conn)
        self.clinic = _Clinics(self._conn)
        self.logistic = _Logistics(self._conn)
        self.summary = _Summarys(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        cursor = self._conn.cursor()
        cursor.executescript("""
        CREATE TABLE Vaccines (
            id INTEGER PRIMARY KEY,
            date DATE NOT NULL,
            supplier INTEGER REFERENCES supplier(id),
            quantity INTEGER NOT NULL
        );

        CREATE TABLE Suppliers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            logistic INTEGER REFERENCES logistic(id)
        );
        
        CREATE TABLE Clinics (
            id INTEGER PRIMARY KEY,
            location TEXT NOT NULL,
            demand INTEGER NOT NULL,
            logistic INTEGER REFERENCES logistic(id)
        );
        
        CREATE TABLE Logistics (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            count_sent INTEGER NOT NULL,
            count_received INTEGER NOT NULL
        );
        
        CREATE TABLE Summarys (
            total_inventory INTEGER NOT NULL,
            total_demand INTEGER NOT NULL,
            total_received INTEGER NOT NULL,
            total_sent INTEGER NOT NULL
        );
        
    """)

    def deleteifExist(self):
        Data_Base_Exist = os.path.isfile('database.db')
        self.__init__()


repo = _Repository()
atexit.register(repo._close)
