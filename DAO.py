from DTO import Vaccine, Supplier, Clinic, Logistic


class _Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccines): # we use it
        self._conn.execute("""
        INSERT INTO Vaccines VALUES (?,?,?,?)""", [vaccines.id, vaccines.date, vaccines.supplier, vaccines.quantity])

    def update(self, id, quantity): # we use it
        self._conn.execute("""UPDATE Vaccines SET quantity=(?) WHERE id=(?)""", [quantity, id])

    def delete(self, id): # we use it
        self._conn.execute("""DELETE FROM Vaccines WHERE id=(?)""", [id])

    def find(self): # we use it
        c = self._conn.cursor()
        c.execute("""
                SELECT id FROM Vaccines ORDER BY DATE 
            """)
        return c.fetchone()

    def findall(self): # we use it
        c = self._conn.cursor()
        c.execute("""SELECT * FROM Vaccines ORDER BY DATE asc""")
        return c.fetchall()


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier): # we use it
        self._conn.execute("""
        INSERT INTO Suppliers VALUES (?,?,?) """, [supplier.id, supplier.name, supplier.logistic])

    def findSupplierID(self, name): # we use it
        c = self._conn.cursor()
        c.execute("""
                SELECT id FROM Suppliers WHERE name = ?
            """, [name])
        return c.fetchone()

    def findLogisticID(self, name): # we use it
        c = self._conn.cursor()
        c.execute("""
                SELECT logistic FROM Suppliers WHERE name = ?
            """, [name])
        return c.fetchone()


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinics): # we use it
        self._conn.execute("""
            INSERT INTO Clinics VALUES (?, ?, ?,?)
        """, [clinics.id, clinics.location, clinics.demand, clinics.logistic])

    def find(self, location): # we use it
        c = self._conn.cursor()
        c.execute("""
                SELECT demand FROM Clinics WHERE location = ?
            """, [location])
        return c.fetchone()

    def findLogisticID(self, location):  # we use it
        c = self._conn.cursor()
        c.execute("""
                SELECT logistic FROM Clinics WHERE location = ?
            """, [location])
        return c.fetchone()

    def update(self, demand,location):  # we use it
        self._conn.execute("""UPDATE Clinics SET demand=(?) WHERE location=(?)""", [demand,location])


class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic): # we use it
        self._conn.execute("""
                INSERT INTO Logistics VALUES (?, ?, ?, ?)
        """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])


    def find(self, id): # we use it
        c = self._conn.cursor()
        c.execute("""
                SELECT count_received, count_sent FROM Logistics WHERE id = ?
            """, [id])
        return c.fetchone()

    def updateReceived(self, logistics, count_received): # we use it
        self._conn.execute("""UPDATE Logistics SET count_received=(?) WHERE id=(?)""", [count_received, logistics])


    def updateSent(self, logistics, count_sent): # we use it
        self._conn.execute("""UPDATE Logistics SET count_sent=(?) WHERE id=(?)""", [count_sent, logistics])


class _Summarys:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, summary): # we use it
        self._conn.execute("""
            INSERT INTO Summarys VALUES (?, ?, ?, ?)
        """, [summary.total_inventory, summary.total_demand, summary.total_received, summary.total_sent])

    def updateTotalReceived(self, total_inventory, total_received):
        self._conn.execute("""UPDATE Summarys SET total_inventory=(?), total_received=(?) WHERE total_inventory != -1""", [total_inventory, total_received])

    def updateElse(self, total_inventory, total_demand, total_sent):
        self._conn.execute("""UPDATE Summarys SET total_inventory=(?), total_demand=(?), total_sent=(?) WHERE total_inventory != -1""", [total_inventory, total_demand, total_sent])

    def find(self): # we use it
        c = self._conn.cursor()
        c.execute("""SELECT * FROM Summarys""")
        return c.fetchall()

