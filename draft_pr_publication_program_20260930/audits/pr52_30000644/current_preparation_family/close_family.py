#!/usr/bin/env python3
"""Unexecuted ROOT-only SOURCE; closes only this current private packet."""
from datetime import datetime,timezone
from pathlib import Path
import argparse,json,os
from closure_common import HERE,SELF,bind,inspect,load,require,sha

def completed_private_readback():
    cap=load(HERE/'READBACK_CAPTURE.json')
    require(cap['schema']=='pr52-current-private-compact-readback-capture/v1','literal complete compact capture')
    require(cap['exit_code']==0 and cap['sources_unchanged_after'] is True,'actual completed private readback')
    require(cap['argv']==['/usr/bin/python3','-B',str(HERE/'readback_current.py'),'--child'],'actual literal readback argv')
    require(cap['cwd']==str(HERE) and cap['child_pid']==13627 and cap['operator_pid']==13626,'actual literal readback cwd/PIDs')
    require(datetime.fromisoformat(cap['utc_start'])<=datetime.fromisoformat(cap['utc_end']),'actual readback interval')
    require(cap['ROOT_or_production_execution'] is False,'readback was private preparation only')
    for row in cap['sources_and_operator_prelaunch']:
        body=row['full_prelaunch_utf8'].encode()
        require(len(body)==row['bytes'] and sha(body)==row['sha256'],'complete compact prelaunch input')
        require(Path(row['path']).read_bytes()==body,'private readback source body remained unchanged')
        require(row['mode']=='0644','dated private prelaunch source mode')
    for stream in ('stdout','stderr'):
        body=cap[stream]['full_utf8'].encode()
        require(len(body)==cap[stream]['bytes'] and sha(body)==cap[stream]['sha256'],'complete compact stream')
    require(cap['stderr']['full_utf8']=='','complete empty private readback stderr')
    value=json.loads(cap['stdout']['full_utf8'])
    require(value==cap['stdout_typed'] and value['actual_pid']==cap['child_pid'],'typed complete actual readback stdout')
    require(value['integrity_checks']==1564 and value['science_files']==39 and value['external_full_body_rows']==273,'actual bounded readback result')
    require(value['completed_builder_child_pid']==10798 and value['new_mathematical_verdict'] is False,'actual builder and no borrowed math verdict')
    return cap
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expected-index-sha256',required=True)
    parser.add_argument('--expected-ready-sha256',required=True)
    parser.add_argument('--after-preparer-exit',required=True,action='store_true')
    args=parser.parse_args()
    require(HERE.name=='current_preparation_family' and HERE.parent.name=='pr52_30000644','exact private current family')
    require(args.after_preparer_exit and not (HERE/SELF).exists(),'absent-only ROOT closure after preparer exit')
    require(bind(HERE/'INDEX.json')['sha256']==args.expected_index_sha256,'ROOT-pinned whole index')
    require(bind(HERE/'READY.json')['sha256']==args.expected_ready_sha256,'ROOT-pinned whole READY')
    completed_private_readback()
    result=inspect(False)
    rows=[bind(p,True) for p in sorted(HERE.rglob('*')) if p.is_file()]
    value={'schema':'pr52-current-lean-self-closure/v1','utc':datetime.now(timezone.utc).isoformat(),
           'closure_operator_pid':os.getpid(),'family':str(HERE),'files':rows,
           'index_sha256':args.expected_index_sha256,'ready_sha256':args.expected_ready_sha256,
           'inspection':result,'manifest_excludes_only_itself':SELF,
           'ROOT_personal_read_attestation':False,'native_acceptance':False,
           'new_independent_mathematical_verdict':False,'production_or_publication_authority':False,
           'scope':'Self-only SOURCE custody. ROOT caller and actual completion are independently captured after this child returns.'}
    body=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
    os.chmod(HERE,0o755)
    try:
        fd=os.open(str(HERE/SELF),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
        with os.fdopen(fd,'wb') as stream:
            stream.write(body);stream.flush();os.fchmod(stream.fileno(),0o444);os.fsync(stream.fileno())
    finally:os.chmod(HERE,0o555)
    inspect(True)
    print(json.dumps({'status':'CLOSED_CURRENT_SOURCE_ONLY','manifest':bind(HERE/SELF,True),
                      'payload_files':len(rows),'science_files':39,'production_authority':False},sort_keys=True))
if __name__=='__main__':main()
