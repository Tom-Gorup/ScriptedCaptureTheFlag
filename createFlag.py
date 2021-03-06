__author__ = 'tom'

import uuid
import argparse
import logging
import os
import mods.mod_createflag as create_flag_def

parser = argparse.ArgumentParser(description='Used to create flags')
parser.add_argument('-n', '--name', help='Enter name for flag', required=True)
parser.add_argument('-p', '--points', help='Enter how many points flag is worth', required=True)
parser.add_argument('-i', '--ipaddress', help='Enter the ip address of the ctfCollector', required=True)
parser.add_argument('-v', '--venomous', help='Enter if flag is venomous (1), or not (0)', action='store_true', default=0)
parser.add_argument('-u', '--justuuid', help='Enter to create just a uuid and no script', action='store_true')
parser.add_argument('-o', '--obfuscate', help='Obfuscate the flag script.', action='store_true', default=True)

#ToDo: Give option for creating Windows Executable flag

current_directory = os.getcwd()
logger = logging.getLogger('CTFcreateFlag')
hdlr = logging.FileHandler(current_directory + '/log/createFlag.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    try:
        args = vars(parser.parse_args())    # Assign arguments to args variable
    except Exception, e:
        logger.info("Call to args parser: {0}".format(e))

    try:
        flagUUID = uuid.uuid4()    # Create new uuid and assign to variable
    except Exception, e:
        logger.inf(e)

    try:
        flagname = args['name']
    except Exception, e:
        logger.info("Get flag name from args: {0}".format(e))

    try:
        ipaddress = args['ipaddress']
    except Exception, e:
        logger.info("Get ipaddress from args: {0}".format(e))

    try:
        if create_flag_def.check_if_flagname_exists(flagname):    # Check if flag name already exists, ask user for new one if does
            print "Flag name already exists, please select a new one: ",
            flagname = raw_input()
    except Exception, e:
        logger.info("Get flagname from args: {0}".format(e))
    try:
        if create_flag_def.check_if_uuid_exists(flagUUID):
            try:
                flagUUID = uuid.uuid4()    # Create new uuid and assign to variable
            except Exception, e:
                logger.info("Get new randomized UUID: {0}".format(e))
    except Exception, e:
        logger.info("Call to create_flag_def.check_if_uuid_exists: {0}".format(e))

    try:
        if not args['justuuid']:
            public_key_loc = 'keys/pub.key'    # Assign public key location to variable
            if os.path.isfile(os.path.realpath(public_key_loc)):
                try:
                    pubKey = open(public_key_loc, "r").read()    # Feed the key to variable for writing
                except Exception, e:
                    logger.info("Open public_key_loc: {0}".format(e))
                try:
                    if os.path.isfile(os.path.realpath("database/ctfCollector.db")):
                        try:
                            create_flag_def.createFlag(flagname, pubKey, flagUUID, ipaddress, args['venomous'])    # Create the new flag
                            try:
                                python_flag_name = flagname + ".py"
                                create_flag_def.obfuscate_script(python_flag_name)
                                try:
                                    create_flag_def.update_uuid_db(flagname, str(flagUUID), int(args['points']), args['venomous'])    # Update the database with the information
                                except Exception, e:
                                    logger.info("Call to create_flag_def.update_uuid_db: {0}".format(e))
                            except Exception, e:
                                logger.info("Call to create_flag_def.obfuscate_script: {0}".format(e))
                        except Exception, e:
                            logger.info("Call to create_flag_def.createFlag: {0}".format(e))
                    else:
                         logger.info("Database does not exist. Please run setup")
                except Exception, e:
                    logger.inf("Insert and obsfucate flag: {0}".format(e))
            else:
                logger.inf("Public key does not exist. Please run setup.")
        else:
            try:
                print "New Flag UUID: " + str(flagUUID)
            except Exception, e:
                logger.info("Printing new flag as string: {0}".format(e))
            try:
                create_flag_def.update_uuid_db(flagname, str(flagUUID), int(args['points']), args['venomous'])    # Update the database with the information
            except Exception, e:
                logger.info("Call to create_flag_def.update_uuid_db: {0}".format(e))
    except Exception, e:
        logger.info(e)