import os
import sys

from Repository import repo
from DTO import Vaccine, Supplier, Clinic, Logistic, Summary


def main(argv):
    repo.deleteifExist()
    repo.create_tables()
    load_configuration()
    load_orders()


def load_configuration():
    config = sys.argv[1]
    file = open(config, 'r')
    content = file.read()
    lines = content.split("\n")
    x = lines[0].split(",")
    v = int(x[0])
    s = int(x[1])
    c = int(x[2])
    l = int(x[3])
    total_inventory = 0
    total_demand = 0
    total_received = 0
    total_sent = 0

    i = 1
    while i < len(lines):
        p = lines[i].split(",")
        if 0 < i <= v:
            total_inventory = total_inventory + int(p[3])
            repo.vaccine.insert(Vaccine(int(p[0]), p[1], int(p[2]), int(p[3])))
        if v < i <= v + s:
            repo.supplier.insert(Supplier(int(p[0]), p[1], int(p[2])))
        if v+s < i <= v+s+c:
            total_demand = total_demand + int(p[2])
            repo.clinic.insert(Clinic(int(p[0]), p[1], int(p[2]), int(p[3])))
        if v+s+c < i <= v+s+c+l:
            total_received = total_received + int(p[2])
            total_sent = total_sent + int(p[3])
            repo.logistic.insert(Logistic(int(p[0]), p[1], int(p[2]), int(p[3])))
        i = i+1

    repo.summary.insert(Summary(total_inventory, total_demand, total_received, total_sent))


def load_orders():
    orders = sys.argv[2]
    f = open(sys.argv[3], "w")

    file = open(orders, 'r')
    content = file.read()
    lines = content.split("\n")

    counter = 0
    for line in lines:
        p = line.split(",")
        if len(p) == 3:    # Case Receive Shipment
            name = p[0]
            amount = int(p[1])
            date = p[2]

            #add line of new vaccine
            current_supplier_id = repo.supplier.findSupplierID(name)
            table = repo.vaccine.findall()
            size = len(table)
            highest_id = table[size-1][0]
            repo.vaccine.insert(Vaccine(highest_id+1, date, current_supplier_id[0], amount))

            #update count_received of logistic
            current_logistic_id = repo.supplier.findLogisticID(name)
            count_received = repo.logistic.find(current_logistic_id[0])[0]
            repo.logistic.updateReceived(current_logistic_id[0], count_received+amount)

            #update total_received of summary
            total_inventory = repo.summary.find()[0][0]
            int_total_inventory = int(total_inventory)
            total_received = repo.summary.find()[0][2]
            repo.summary.updateTotalReceived(int_total_inventory+amount, total_received+amount)
            output = repo.summary.find()[0]
            output_string = str(output).strip('()')
            f.write(output_string)
            f.write("\n")
            counter = counter + 1

        else:   # Case Send Shipment
            location = p[0]
            amount = int(p[1])

            #update demand of clinic
            demand = repo.clinic.find(location)
            int_demand = int(demand[0])
            repo.clinic.update(int_demand-amount,location)

            #update count_sent of logistic
            current_logistic_id = repo.clinic.findLogisticID(location)
            count_sent = repo.logistic.find(current_logistic_id[0])[1]
            repo.logistic.updateSent(current_logistic_id[0], count_sent+amount)

            #update lines amounts of vaccines
            table = repo.vaccine.findall()
            size = len(table)
            old_amount = amount
            for i in range(size):
                vac_amount = repo.vaccine.findall()[0][3]
                vac_id = repo.vaccine.findall()[0][0]
                if vac_amount > amount:
                    repo.vaccine.update(vac_id, vac_amount-amount)
                    break
                else:
                    repo.vaccine.delete(vac_id)
                    amount = amount-vac_amount

            #update fields of summary
            total_inventory = repo.summary.find()[0][0]
            int_total_inventory = int(total_inventory)
            total_demand = repo.summary.find()[0][1]
            int_total_demand = int(total_demand)
            total_sent = repo.summary.find()[0][3]
            int_total_sent = int(total_sent)
            repo.summary.updateElse(int_total_inventory-old_amount, int_total_demand-old_amount, int_total_sent+old_amount)
            output = repo.summary.find()[0]
            output_string = str(output).strip('()')
            f.write(output_string)
            f.write("\n")
            counter = counter + 1

    f.close()


if __name__ == '__main__':
    main(sys.argv)
