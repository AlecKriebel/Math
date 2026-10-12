"""Exact flat-family packet checks, no native/remote operations.

All bodies including helper code are indexed. INDEX and READY are bound by
READY, and the literal self-excluding manifest is reserved for ROOT alone.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

BASE=Path(__file__).resolve().parent
INDEX='INDEX.json'
READY='READY.json'
SELF='SELF_MANIFEST.json'
RESERVED={INDEX,READY,SELF}
def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p):
    p=Path(p); s=p.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink==1, str(p)
    b=p.read_bytes()
    return {'name':p.name,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'full_st_mode':oct(s.st_mode),'mode_07777':format(s.st_mode & 0o7777,'04o'),'nlink':s.st_nlink}
def directory():
    s=BASE.lstat()
    assert stat.S_ISDIR(s.st_mode) and not BASE.is_symlink()
    return {'path':str(BASE),'full_st_mode':oct(s.st_mode),'mode_07777':format(s.st_mode & 0o7777,'04o')}
def json_read(name):
    return json.loads((BASE/name).read_text())
def create_json(name,body):
    data=(json.dumps(body,indent=2,sort_keys=True)+'\n').encode()
    fd=os.open(BASE/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
    try:
        os.fchmod(fd,0o444)
        off=0
        while off<len(data):
            off+=os.write(fd,data[off:])
        os.fsync(fd)
    finally:
        os.close(fd)
def topology(names):
    assert directory()['mode_07777']=='0755'
    actual={p.name for p in BASE.iterdir()}
    assert actual==set(names), (sorted(actual-set(names)),sorted(set(names)-actual))
    for name in sorted(actual):
        assert digest(BASE/name)['mode_07777']=='0444',name
def prepared(expect_manifest=False):
    index=json_read(INDEX); ready=json_read(READY)
    assert index['schema']=='pr57-endpoint-fixed-index/v1'
    assert index['original_head']=='4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29'
    assert index['directory']==directory()
    names=[d['name'] for d in index['bodies']]
    assert names==sorted(set(names)) and not set(names)&RESERVED
    assert index['reserved_names']==sorted(RESERVED)
    assert [digest(BASE/name) for name in names]==index['bodies']
    expected=names+[INDEX,READY]+([SELF] if expect_manifest else [])
    topology(expected)
    assert ready['schema']=='pr57-endpoint-ready/v1'
    assert ready['original_head']==index['original_head']
    assert ready['bindings']==[digest(BASE/n) for n in [INDEX,'REPORT.md','VERDICT.json']]
    assert ready['SELF_manifest_created'] is False
    assert ready['ROOT_helpers_executed'] is False
    assert ready['ROOT_or_math_acceptance'] is False
    return index,ready
def independent_evidence():
    controls=json_read('independent_controls.stdout.bin')
    receipt=json_read('independent_controls.CAPTURE.json')
    assert controls['check_count']==340 and controls['process_pid']==96241==receipt['executed_child_pid']
    assert controls['script_sha256']==receipt['source_sha256_before']==receipt['source_sha256_after']==digest(BASE/'controls.py')['sha256']
    assert receipt['exit_code']==0 and receipt['stdout_bytes']==18062 and receipt['stderr_bytes']==0
    for stream in ['stdout','stderr']:
        d=digest(BASE/receipt['full_'+stream+'_file'])
        assert d['bytes']==receipt[stream+'_bytes'] and d['sha256']==receipt[stream+'_sha256']
    assert digest(BASE/receipt['operator_literal_code_file'])['sha256']==receipt['operator_literal_code_sha256']
    source=json_read('source_controls_corrected.stdout.bin')
    assert source['authenticated_science_body_count']==17 and source['process_pid']==1959
    assert source['SQL_report_is_NULL'] is False and source['SQL_report_literal']=='{}'
    assert source['original_turns_used']==1 and source['original_turn_limit']==5
    for label,script,exit_code in [('source_controls','source_checks_failed_schema.py',1),('source_controls_corrected','source_checks.py',0)]:
        cap=json_read(label+'.CAPTURE.json')
        assert cap['exit_code']==exit_code and cap['source_bytes_unchanged'] is True
        assert cap['sources_before']==cap['sources_after']
        assert cap['sources_before'][0]['sha256']==digest(BASE/script)['sha256']
        for stream in ['stdout','stderr']:
            d=digest(BASE/(label+'.'+stream+'.bin')); before=cap['full_'+stream]
            assert d['sha256']==before['sha256'] and d['bytes']==before['bytes']
    assert json_read('VERDICT.json')['independent_controls_passed']==340
