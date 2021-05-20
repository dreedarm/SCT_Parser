#!/usr/bin/env python3

import sys
import argparse

def seq_parser(file):
    temp_dict = dict()
    temp_list = list()
    lines=file.readlines()
    magic=7 #a test in a seq file is 7 lines, if not mod7, something wrong..
    if len(lines)%magic != 0:
        sys.exit("seqfile cut short, should be mod7")
    #the utf-16 char makes this looping a bit harder, so we use x+(i) where i is next 0-6th
    for x in range(0,len(lines),magic): #loop ever "7 lines"
        #(x+0)[Test Case]
        #(x+1)Revision=0x10000
        #(x+2)Guid=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        #(x+3)Name=InstallAcpiTableFunction
        #(x+4)Order=0xFFFFFFFF
        #(x+5)Iterations=0xFFFFFFFF
        #(x+6)(utf-16 char)
        #currently only add tests that are supposed to run, should add all?
        #0xFFFFFFFF in "Iterations" means the test is NOT supposed to run
        seq_dict = {
            "name": lines[x+3][5:-1],#from after "Name=" to end (5char long)
            "guid": lines[x+2][5:-1],#from after"Guid=" to the end, (5char long)
            "Iteration": lines[x+5][11:-1],#from after "Iterations=" (11char long)
            "rev": lines[x+1][9:-1],#from after "Revision=" (9char long)
            "Order": lines[x+4][6:-1]#from after "Order=" (6char long)
        }
        temp_dict[(lines[x+2][5:-1])]=(seq_dict) #put in a dict based on guid
        
    return temp_dict


def main():

    parser = argparse.ArgumentParser(
        description='Process SCT .seq file.'
                    ' This program takes the SCT seq file, and turns it,'
                    ' int a readable version of the tests to be run.',
        epilog='usage  is seq.py <seqeunce.seq>',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'seq_file', help='Input .seq filename')

    args = parser.parse_args()

    db1 = dict() #"database 1" all test sets

    with open(args.seq_file,"r",encoding="utf-16") as f: #files are encoded in utf-16
        db1 = seq_parser(f)
    
    #print the tests names and if they run.
    for x in db1:
        #print( x, end=' : ' )
        if db1[x]['Iteration'] == '0xFFFFFFFF':
            print ( 'OFF',end=" : ")
        else:
            print ('ON ',end=' : ')
        print(db1[x]['name'])
        

main()