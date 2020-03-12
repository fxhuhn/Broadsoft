from Broadsoft import XSI
from os import environ
import getpass
import argparse



"""
    Username is the full name with domain
    e.g. userid@deutschland-lan.de    
"""


if __name__ == "__main__":

    """
    TODO: Placeholder for future feature:
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    #args = parser.parse_args()

    parser.add_argument("--name", type=str, help="Username")
    parser.add_argument("--host", type=str, help="Host")
    parser.add_argument("--dir", choices=['personal', 'group','enterprise'], help="Directory")

    args = parser.parse_args()
    dir = args.dir
    print(dir)
    """

    if environ.get('USER') is None:
        USER = input('Username:')
    else:
        USER = environ.get('USER')
        print('Username:', USER)

    if environ.get('PASS') is None:
        PASS = getpass.getpass(prompt='Password: ')
    else:
        PASS = environ.get('PASS')

    x=XSI(USER,PASS)

    print('directories_personal')
    y = x.directories_personal()
    for z in y:
        print('{:40}; {:20}'.format(z['name'], z['number']))

    print('directories_group_common')
    y = x.directories_group_common()
    for z in y:
        print('{:40}; {:20}'.format(z['name'], z['number']))


    print('directories_enterprise_common')
    y = x.directories_enterprise_common()
    for z in y:
        print('{:40}; {:20}'.format(z['name'], z['number']))

    print('directories_enterprise')
    y = x.directories_enterprise()
    for z in y:
        print (list(z.values()))

    print('directories_group')
    y = x.directories_group()
    for z in y:
        print (list(z.values()))

    print('directories_call_logs_missed')
    y = x.directories_call_logs_missed()
    for z in y:
        print (list(z.values()))

    print('directories_call_logs_placed')
    y = x.directories_call_logs_placed()
    for z in y:
        print (list(z.values()))

    print('directories_call_logs_received')
    y = x.directories_call_logs_received()
    for z in y:
        print (list(z.values()))

