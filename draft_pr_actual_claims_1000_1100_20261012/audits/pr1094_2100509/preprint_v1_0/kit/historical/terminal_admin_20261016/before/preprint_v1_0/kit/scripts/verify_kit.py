import argparse
import json
import sys
sys.dont_write_bytecode=True
from safety import verify_payload, binding_check

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--binding');parser.add_argument('--require-binding',action='store_true');args=parser.parse_args()
    data=verify_payload()
    print(json.dumps({'status':'PASS','payload_files':len(data['records']),
                      'binding':binding_check(args.binding,args.require_binding)},sort_keys=True))
if __name__=='__main__': main()
