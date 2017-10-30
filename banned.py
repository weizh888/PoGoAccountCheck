#!/usr/bin/python
# -*- coding: utf-8 -*-

"""banned.py - Check multiple PTC accounts ban status with Pokemon Go."""

from pgoapi import PGoApi
from pgoapi.exceptions import ServerSideRequestThrottlingException
from pgoapi.exceptions import NotLoggedInException
from pgoapi.exceptions import BannedAccountException
import time
import sys
import os
import argparse
import re


def parse_arguments(args):
    """Parse the command line arguments for the console commands.
    Args:
      args (List[str]): List of string arguments to be parsed.
    Returns:
      Namespace: Namespace with the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Pokemon Trainer Club Banned Account Checker'
    )
    parser.add_argument(
        '-f', '--file', type=str, default=None, required=True,
        help='File of accounts to check (RocketMap csv format).'
    )
    parser.add_argument(
        '-l', '--location', type=str, default="40.7127837 -74.005941",
        required=False,
        help='Location to use when checking if the accounts are banned.'
    )
    parser.add_argument(
        '-hk', '--hash-key', type=str, default=None, required=True,
        help='Key for hash server.'
    )
    return parser.parse_args(args)


def check_account(provider, username, password, location, api):
    api.set_position(location[0], location[1], 0.0)

    try:
        if not api.login(provider, username, password):
            __accountFailed(provider, username, password)
            return False
    except BannedAccountException:
        # Banned :(
        __accountBanned(provider, username, password)
        return False

    time.sleep(1)
    req = api.create_request()
    req.get_inventory()
    response = req.call()

    # For some reason occasionally api.login lets fake ptc accounts slip
    # through.. this will block em
    if type(response) is NotLoggedInException:
        __accountFailed(provider, username, password)
        return False

    if response['status_code'] == 3:
        __accountBanned(provider, username, password)
        return False
    else:
        print('{} is not banned...'.format(username))
        return True


def __accountBanned(provider, username, password):
    print('Account banned: {}.'.format(username))
    csv_format = provider + ',' + username + ',' + password
    appendFile(csv_format, 'banned.csv')


def __accountFailed(provider, username, password):
    print('Failed to login with: {}.'.format(username))
    csv_format = provider + ',' + username + ',' + password
    appendFile(csv_format, 'failed.csv')


def appendFile(text, filename):
    if os.path.exists(filename):
        f = open('./' + filename, 'a+b')
    else:
        f = open('./' + filename, 'w+b')

    f.write("%s\n" % (text))

    f.close()


def entry():
    args = parse_arguments(sys.argv[1:])
    api = PGoApi()

    prog = re.compile("^(\-?\d+\.\d+),?\s?(\-?\d+\.\d+)$")
    res = prog.match(args.location)
    if res:
        print('Using the following coordinates: {}'.format(args.location))
        position = (float(res.group(1)), float(res.group(2)), 0)
    else:
        print(('Failed to parse the supplied coordinates ({}).'
               + ' Please try again.').format(args.location))
        return

    if args.hash_key:
        print "Using hash key: {}.".format(args.hash_key)
        api.activate_hash_server(args.hash_key)

    with open(str(args.file)) as f:
        credentials = [x.strip().split(',')[0:] for x in f.readlines()]

    for provider, username, password in credentials:
        try:
            if check_account(provider, username, password, position, api):
                # Success!
                csv_format = provider + ',' + username + ',' + password
                appendFile(csv_format, 'working.csv')
        except ServerSideRequestThrottlingException:
            print('Server side throttling, waiting for 10 seconds.')
            time.sleep(10)
            check_account(provider, username, password, position, api)
        except NotLoggedInException:
            print('Could not login, waiting for 10 seconds.')
            time.sleep(10)
            check_account(provider, username, password, position, api)


entry()
