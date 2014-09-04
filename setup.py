#!/usr/bin/python

import sqlite3
import os
import argparse

#ToDo: Check for crypto package installation, make recommendations

parser = argparse.ArgumentParser(description='Server listening for flags')
parser.add_argument('-l', '--loglevel', help='Logging level - followed by debug, info, or warning')

def logLevel():
    if args['loglevel'] == 'info':
        logging.basicConfig(filename='log/setup.log', level=logging.INFO, filemode='a', format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info('Log Level set to Informational')
    elif args['loglevel'] == 'debug':
        logging.basicConfig(filename='log/setup.log', level=logging.DEBUG, filemode='a', format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.debug('Log Level set to Debug')
    elif args['loglevel'] == 'warning':
        logging.basicConfig(filename='log/setup.log', level=logging.WARNING, filemode='a', format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.warning('Log Level set to Warning')

def setupDatabase(database):
    print database
    if not os.path.isfile(os.path.realpath('database/' + database)):
        conn = sqlite3.connect('database/' + database)
        logging.info("Database open: %s" % database)
        print('database open')

        conn.execute('''CREATE TABLE users_points (uname VARCHAR(32) NOT NULL, tot_points INT);''')
        conn.execute('''CREATE TABLE users_flags (uname VARCHAR(32) NOT NULL, uuid VARCHAR(37));''')
        conn.execute('''CREATE TABLE users (uname VARCHAR(32) NOT NULL, message VARCHAR(255));''')
        conn.execute('''CREATE TABLE flags (uuid VARCHAR(37) NOT NULL, points INT NOT NULL, venomous BOOLEAN DEFAULT 0);''')
        conn.execute('''CREATE TABLE users (uname VARCHAR(32) NOT NULL, password VARCHAR(32) NOT NULL);''')
        logging.info("table created in %s" % database)

        conn.commit()
        logging.info("Commit Completed")
        conn.close()
        logging.info("Connection to database closed")

def generate_RSA(bits=2048):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    from Crypto.PublicKey import RSA

    new_key = RSA.generate(bits, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")

    return private_key, public_key

if __name__ == "__main__":
    #pip install pycrypto
    #pip instlal m2crypto

    logLevel()

    setupDatabase('ctfCollector.db')
    encryption = generate_RSA()

    f = open('keys/priv.key', 'w')
    f.write(encryption[0])

    f = open('keys/pub.key', 'w')
    f.write(encryption[1])
