__author__ = 'tom'

import uuid
import argparse
import logging
import mods.mod_createflag as create_flag_def

parser = argparse.ArgumentParser(description='Used to create flags')
parser.add_argument('-n', '--name', help='Enter name for flag', required=True)
parser.add_argument('-p', '--points', help='Enter how many points flag is worth', required=True)
parser.add_argument('-i', '--ipaddress', help='Enter the ip address of the ctfCollector', required=True)
parser.add_argument('-v', '--venomous', help='Enter if flag is venomous (1), or not (0)', action='store_true')
parser.add_argument('-u', '--justuuid', help='Enter to create just a uuid and no script', action='store_true')

#ToDo: Add randomized encoded function for 'Poisoned Flags'

current_directory = os.getcwd()
logger = logging.getLogger('ctfCollector')
hdlr = logging.FileHandler(current_directory + '/log/setup.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    try:
        args = vars(parser.parse_args())    # Assign arguments to args variable
    except Exception, e:
        logger.inf(e)

    try:
        flagUUID = uuid.uuid4()    # Create new uuid and assign to variable
    except Exception, e:
        logger.inf(e)

    try:
        flagname = args['name']
    except Exception, e:
        logger.inf(e)

    try:
        ipaddress = args['ipaddress']
    except Exception, e:
        logger.inf(e)

    if create_flag_def.check_if_flagname_exists(flagname):    # Check if flag name already exists, ask user for new one if does
        print "Flag name already exists, please select a new one: ",
        flagname = raw_input()

    if create_flag_def.check_if_uuid_exists(flagUUID):
        flagUUID = uuid.uuid4()    # Create new uuid and assign to variable

    if not args['justuuid']:
        public_key_loc = 'keys/pub.key'    # Assign public key location to variable
        pubKey = open(public_key_loc, "r").read()    # Feed the key to variable for writing
        create_flag_def.createFlag(flagname, pubKey, flagUUID, ipaddress)    # Create the new flag
        create_flag_def.update_uuid_db(flagname, str(flagUUID), int(args['points']), args['venomous'])    # Update the database with the information
    else:
        print "New Flag UUID: " + str(flagUUID)
        create_flag_def.update_uuid_db(flagname, str(flagUUID), int(args['points']), args['venomous'])    # Update the database with the information
