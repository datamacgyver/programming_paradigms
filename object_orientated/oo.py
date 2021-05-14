# Okay, time for the big guns. Object oriented programming is often touted as the "correct"
# way. I'm not so sure about that but it does have its strengths. Point to note is that
# **python is an object orientated language**, many people simply don't treat it as such.
# Even Pandas has a key word argument `inplace=True` that means you don't return a new
# dataframe, you simply modify it in place. Whether you want such side effects is an
# entirely different conversation!


# In this world, you data is kept with the methods that can be applied to it, making
# your code better organised (and easier to understand...to a point...)

class Num:
    def __init__(self, n):
        self.n = n

    def add_one(self):
        self.n += 1


num = Num(1)
num.add_one()
num.add_one()
num.add_one()
num.add_one()
num.add_one()

print(num.n)

# Much to unpack here, note first the use of self in all my functions and my data, this basically says "you can find
# this in the current object"
#
# so I've created a class (an object) which is initialised with a state,
# that state being n = 1. It saves that and it becomes part of what it stores. If I want to
# modify n I call the add_one method which modifies the state of my number. The key thing here
# is that, depending on where I am in my pipeline, num is different! Compare this to the final functional
# solution where I call my function and it returns a response, there is no place where my output has a value
# that isn't the output value.

# More below































# This concept of state can trip you up as it makes thigns hard to test and debug,
# but it's also really useful (and often really badly taught IMHO). I like to present
# this as a database connection. This is useful because:
# * you don't want to make one connection per operation
# * your connection may break or timeout, requiring a catch and re-authorisation
# * you may want to use one set of connection details in several places without handing them around as arguments
from object_orientated.hidden_stuff import PostgresConnection

class Database:
    def __init__(self, address, user, password):
        self.address = address
        self.user = user
        self.password = password
        self.connection = None
        self._make_connection()

    def _make_connection(self):
        self.connection = PostgresConnection(self.address, self.user, self.password)

    def insert_into_tables(self, table, to_insert):
        insert_statement = "Insert into {table} ({values})".format(table=table, values=to_insert)
        try:
            self.connection.run(insert_statement)
        except ConnectionError:
            self._make_connection()
            self.connection.run(insert_statement)


db = Database("localhost:4321", "rob", "THX1138")
db.insert_into_tables("my_table", [1, 2, 3, 4])

# the above db object can now be given to anything that requires the functionality in the
# Database object, you don't have to create new connections for every operation and if you want to add
# new functionality you put it in Database. This is also a place to have your try/catch blocks
# to retry if your connection is closed, handily it also stores the connection data so it's easy to
# reconnect. Basically *everything to do with your database can live in this object* and if it works
# you can safely ignore what goes on inside it.



# The above example is where you should use an object no matter what paradigm you like, it simply makes
# no sense to ignore the fact that your connection has a state and that state is useful in various places.
# Many languages go all in on this way of organising code though and there are reasons for that. Lets consider
# The idea of someone that owns a farming company, how may you represent the information on their holdings?


class Farmer:
    def __init__(self, farms):
        self.farms = farms

#That's great, but what about what goes on in those farms? You could get the function to take farms, fields
# but then which farm does each field belong to? It's hard to represent that logically...or is it? Let's make
# some more objects:


class Farm:
    def __init__(self, fields):
        self.fields = fields


class Field:
    def __init__(self, area, growing_seasons):
        self.area = area
        self.growing_seasons = growing_seasons


class GrowingSeason:
    def __init__(self, crop, treatments, amount_harvested):
        self.crop = crop
        self.treatments = treatments
        self.amount_harvested = amount_harvested


# Using these four classes, I have represented the hierachy of ownership that our Farmer has, complete with some
# extra metadata along the way, such as field area_hectares. Would this be simpler using a dictionary? probably, yes but you
# wouldn't get the formal definition of the world that makes what you've done easier to document and communicate. In
# here you could also have support methods such as `get_harvest_per_acre()" in GrowingSeason or
# `get_total_harvested_by_crop()` in Farm, even `get_area_in_acres()` in field. You are adding those methods in the
# place where the data live, reducing the need for utility functions and the like.

# The above would probably also benefit from some type hints so we know what we are doing (for this kind of depth
# it really helps!):

from typing import List


class GrowingSeason:
    def __init__(self, year: int, crop: str, amount_harvested: float):
        self.year = year
        self.crop = crop
        self.amount_harvested = amount_harvested


class Field:
    def __init__(self, area: float, growing_seasons: List[GrowingSeason]):
        self.area = area
        self.growing_seasons = growing_seasons


class Farm:
    def __init__(self, fields: List[Field]):
        self.fields = fields


class Farmer:
    def __init__(self, farms: List[Farm]):
        self.farms = farms

    def print_crops(self):
        for farm in self.farms:
            for field in farm.fields:
                for season in field.growing_seasons:
                    print(season.crop)


# Now, let's create a Farmer!
seasons = [GrowingSeason(2020, "Wheat", 20512.23), GrowingSeason(2021, "Barley", 4163.58)]
fields = [Field(123, seasons)]
farms = [Farm(fields)]
farmer = Farmer(farms)

# To access a farmers farms is now simple and I can add whatever new functionality to any object I want,
# an improvement in storing this all as a nested dictionary as the methods live with the data!
farmer.print_crops()

# More below


























# The final thing I want to cover is inheritence. This is getting proper computer science now so deep breath!
# We are going to stick with farming and store some field info. The thing is that all our crops
# need the same info, it's just different each time! To help us out we will use inheritence to simplify our
# objects


class BaseField:
    def __init__(self, area_hectares, perimeter, location, soil_type):
        self.area_hectares = area_hectares
        self.perimeter = perimeter
        self.location = location
        self.soil_type = soil_type

    def get_area_in_acres(self):
        return self.area_hectares*2.47105


class CowField(BaseField):

    def __init__(self, area_hectares, perimeter, location, soil_type):
        BaseField.__init__(self, area_hectares, perimeter, location, soil_type)

    def get_max_cows_allowed(self):
        return self.area_hectares / 2


# So here I've defined a base field object, this represents the standard information that you need
# to define  field and it will be the same whenther it's a cow field, a wheat field or whatever.
# By doing this I'm establishing a common terminology and data schema for all my fields that I
# cam use in any objects that I inherit, meaning I always know what I'm gonna get.

# The second class inherits from the first, so I can access area_hectares as normal, I've also created
# a new method that is unique to cow fields, the maximum density I can safely graze at. A better implementation
# here may be an abstract class or interface class but I leave such things to the interested reader.



# It's worth noting that this particular way of using objects can quickly get really hard to maintain
# as you never really know where the bit you are using lives. This is true for most OO work, it sounds
# good on paper but it can quickly devolve to anarchy if people try to be clever or try to do *everything*
# as objects.

# This is why scala has a few benefits over java, it allows you to pick the right tools for the job and
# I reckon python is the same, you can pick your paradignm based on your needs at the time.