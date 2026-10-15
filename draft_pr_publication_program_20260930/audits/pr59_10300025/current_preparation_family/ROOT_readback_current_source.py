"""Separate ROOT-only readback; never creates a manifest or approval."""
import argparse
from current_custody_common import *


def main():
    p=argparse.ArgumentParser();p.add_argument('--root-only-separate-readback',action='store_true',required=True);p.parse_args()
    start=now();m=load(N/'ROOT_MANIFEST.json');need(m['literal_self_exclusion']=='ROOT_MANIFEST.json','Literal own self exclusion')
    for z in m['files']:verify_row(z)
    result=verify_current(True)
    need({z['path'] for z in m['files']}|{str(N/'ROOT_MANIFEST.json')}=={str(p) for p in N.rglob('*') if p.is_file()},'Exact closed full domain')
    need(ref(N/'ROOT_MANIFEST.json')['full_mode_07777']=='0444','Closed manifest full mode')
    print(dump({'status':'PASS_SEPARATE_CURRENT_SOURCE_READBACK_ONLY','actual_operator_pid':os.getpid(),'start_utc':start,'end_utc':now(),'manifest':ref(N/'ROOT_MANIFEST.json'),'closed_files':len(m['files'])+1,'validation':result,'native_acceptance_or_math_review_credit':False}).decode(),end='')


if __name__=='__main__':main()
