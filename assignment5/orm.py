from peewee import *
from datetime import date
import json

database = PostgresqlDatabase('flightsskewed', user='vagrant', password='vagrant', host='127.0.0.1')
    # database = PostgresqlDatabase('flightsskewed', **{'user': 'vagrant', 'password': 'vagrant'})`


class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Airports(BaseModel):
    airportid = CharField(primary_key=True)
    city = CharField(null=True)
    name = CharField(null=True)
    total2011 = IntegerField(null=True)
    total2012 = IntegerField(null=True)

    class Meta:
        table_name = 'airports'

class Airlines(BaseModel):
    airlineid = CharField(primary_key=True)
    hub = ForeignKeyField(column_name='hub', field='airportid', model=Airports, null=True)
    name = CharField(null=True)

    class Meta:
        table_name = 'airlines'

class Customers(BaseModel):
    birthdate = DateField(null=True)
    customerid = CharField(primary_key=True)
    frequentflieron = ForeignKeyField(column_name='frequentflieron', field='airlineid', model=Airlines, null=True)
    name = CharField(null=True)

    class Meta:
        table_name = 'customers'

class Flights(BaseModel):
    airlineid = ForeignKeyField(column_name='airlineid', field='airlineid', model=Airlines, null=True)
    dest = ForeignKeyField(column_name='dest', field='airportid', model=Airports, null=True)
    flightid = CharField(primary_key=True)
    local_arrival_time = TimeField(null=True)
    local_departing_time = TimeField(null=True)
    source = ForeignKeyField(backref='airports_source_set', column_name='source', field='airportid', model=Airports, null=True)

    class Meta:
        table_name = 'flights'

class Flewon(BaseModel):
    customerid = ForeignKeyField(column_name='customerid', field='customerid', model=Customers, null=True)
    flightdate = DateField(null=True)
    flightid = ForeignKeyField(column_name='flightid', field='flightid', model=Flights, null=True)

    class Meta:
        table_name = 'flewon'

def runORM(jsonFile): 

    with open(jsonFile) as f:
        for line in f:
            data = json.loads(line) 

     # check newcustomer exist 
            if 'newcustomer' in data: 
                cusData = data['newcustomer']

                existed = (Customers
                .select()
                .where(Customers.customerid == cusData['customerid'])
                .count())

                # if not such customer 
                if existed == 0: 
                     # count # of frequentflieron does not have a match in the airlines table
                    noairlines = (Airlines
                                    .select()
                                    .where(Airlines.name == cusData['frequentflieron'])
                                    .count())

                    # if the frequentflieron does not have a match in the airlines table
                    if noairlines == 0:
                            print("Error424")
                            exit()

                    # if the frequentflieron have a match in the airlines table
                    else: 
                        # change name to id 
                        idnum = (Airlines
                                    .select(Airlines.airlineid)
                                    .where(Airlines.name == cusData['frequentflieron']))
                        
                        # add new customer
                        Customers.create(birthdate = cusData['birthdate'],
                                        customerid = cusData['customerid'],
                                        frequentflieron = idnum, 
                                        name = cusData['name'])
                
                # if customer already exist then exit and print Error424
                else: 
                    print("Error424")
                    exit()

            elif 'flightinfo' in data: 
 
                fliData = data['flightinfo']
 
                 # check whether customerid exist 
                for customer in fliData['customers']: 
                    cusdata = customer 
                    existed = (Customers
                                .select()
                                .where(Customers.customerid == cusdata['customerid'])
                                .count())

                    # if no customer there => add it to customer table
                    if existed == 0: 
                         noairlines = (Airlines.select().where(Airlines.airlineid == cusdata['frequentflieron']).count())

                         # if no such frequentflieron => Error 424 + exist 
                         if noairlines == (0,):
                                print("Error424")
                                exit()

                        # create new customer into table 
                         else: 
                            Customers.create(birthdate = cusdata['birthdate'],
                                            customerid = cusdata['customerid'],
                                            frequentflieron = cusdata['frequentflieron'], 
                                            name = cusdata['name'])

                    # create new flewon into table
                    Flewon.create(customerid = cusdata['customerid'],
                                    flightdate = fliData['flightdate'],
                                    flightid = fliData['flightid'])
                    
                        
                                



            

bob = Customers(name="bob", customerid='cust1010', birthdate='1960-01-15', frequentflieron='SW')
bob

bwi = Airports(airportid='PET', city='Takoma', name='Pete', total2011=2, total2012=4)
bwi
    
for port in Airports.select().order_by(Airports.name):
    print (port.name)




