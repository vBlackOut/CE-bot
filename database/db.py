from playhouse.sqlcipher_ext import *
import os, sys
from playhouse.sqlcipher_ext import SqlCipherDatabase
import yaml

with open("config.yml", 'r') as stream:
    Configuration = yaml.safe_load(stream)

db = SqlCipherDatabase('database/bank.db', passphrase=Configuration['passphraseSQL'])

class Bank(Model):
    description = CharField()
    date = DateField()
    price = IntegerField()

    class Meta:
        database = db # This model uses the "bank.db" database.

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bank.db')

if os.path.isfile(dir_path) is False:
    print("Create New database...")
    Bank.create_table()
