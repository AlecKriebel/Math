"""ROOT-only absent-manifest SOURCE closure after personal full reading."""
import argparse
from current_custody_common import *


def main():
    p=argparse.ArgumentParser();p.add_argument('--root-only-close-after-full-read',action='store_true',required=True);p.parse_args()
    start=now();need(not (N/'ROOT_MANIFEST.json').exists() and not (N/'ROOT_MANIFEST.json').is_symlink(),'Literal manifest must be absent')
    result=verify_current(False)
    rows=[ref(p) for p in sorted(N.rglob('*')) if p.is_file()]
    m={'schema':'pr59-current-ROOT-source-custody/v1','actual_operator_pid':os.getpid(),'argv':__import__('sys').argv,'start_utc':start,'validation_end_utc':now(),'files':rows,'literal_self_exclusion':'ROOT_MANIFEST.json','role':'SOURCE_CUSTODY_ONLY','current_scientific_credit':0,'native_acceptance_or_merge':False,'paper_or_publication':False}
    write_new(N/'ROOT_MANIFEST.json',dump(m))
    print(dump({'status':'PASS_CURRENT_SOURCE_CLOSED_ONLY','manifest':ref(N/'ROOT_MANIFEST.json'),'closed_files':len(rows)+1,'validation':result}).decode(),end='')


if __name__=='__main__':main()
