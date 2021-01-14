# Data Transfer Objects:
class Vaccine:
    def __init__(self, id, date, supplier, quantity):
        self.id = id
        self.date = date
        self.supplier = supplier
        self.quantity = quantity


class Supplier:
    def __init__(self, id, name, logistic):
        self.id = id
        self.name = name
        self.logistic = logistic


class Clinic:
    def __init__(self, id, location, demand, logistic):
        self.id = id
        self.location = location
        self.demand = demand
        self.logistic = logistic


class Logistic:
    def __init__(self, id, name, count_sent, count_received):
        self.id = id
        self.name = name
        self.count_sent = count_sent
        self.count_received = count_received


class Summary:
    def __init__(self, total_inventory, total_demand, total_received, total_sent):
        self.total_inventory = total_inventory
        self.total_demand = total_demand
        self.total_received = total_received
        self.total_sent = total_sent
