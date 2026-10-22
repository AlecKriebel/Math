"""Metadata-only hash/delta verification. No helper/control execution or live operations."""
import copy,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).resolve().parent
PREP=BASE.parent/'preparation_01'
def need(v,m):
    if type(v)is not bool or not v:raise RuntimeError(m)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def read(p):
    need(p.resolve()==p,'canonical file')
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        a=os.fstat(fd);need(stat.S_ISREG(a.st_mode) and stat.S_IMODE(a.st_mode)==0o444,'ordinary0444 file')
        b=os.read(fd,4_000_001);z=os.fstat(fd)
        need((a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)==(z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns,z.st_ctime_ns) and len(b)==a.st_size,'stable full read')
        return b
    finally:os.close(fd)
def main():
    raw=read(PREP/'SOURCE_MANIFEST.json');need(pin(raw)=={'bytes':2052,'sha256':'619ad9a85be48e6323c5643eeefc22ed7bfda4a8e1efbebe46d080ebbec0e765'},'new manifest')
    sealraw=read(PREP/'PREPARATION_SEAL.json');need(pin(sealraw)=={'bytes':736,'sha256':'bf354e173d3a21763a1a93110baa2c02e9f865f9ecfbb53039afcb84d74a39da'},'new seal')
    current=json.loads(raw);seal=json.loads(sealraw);initial=json.loads(read(BASE/'CONTROL_RESULT.json'))
    oldpins={r['path']:{k:r[k] for k in ('bytes','sha256')} for r in initial['finite_source_pins']}
    rows=current['files'];need(len(rows)==8 and len({r['path'] for r in rows})==8,'exact eight paths')
    actual={};delta=[]
    for row in rows:
        b=read(PREP/row['path']);p=pin(b)
        need(p=={k:row[k] for k in ('bytes','sha256')},'new payload pin')
        actual[row['path']]=p
        if p!=oldpins[row['path']]:delta.append(row['path'])
    need(sum(x['bytes'] for x in actual.values())==current['total_bytes']==80788,'new eight total')
    need(delta==['SOURCE_PREPARATION_RECORD.json','RESEARCH_LOG.md'],'only two metadata payloads changed')
    recordraw=read(PREP/'SOURCE_PREPARATION_RECORD.json');record=json.loads(recordraw)
    need(pin(recordraw)=={'bytes':4458,'sha256':'c6aa0faa72fe34ff9adcc629b3d2eddc12ba3d16c3dfec41767fde328fbd7d0c'},'record pin')
    need('research_goal_active' not in record and record['research_work_continues_under_user_authorization']is True
      and record['goal_API_status']=='blocked_inherited_not_modified','exact lifecycle correction')
    reconstructed=copy.deepcopy(record);del reconstructed['research_work_continues_under_user_authorization'];del reconstructed['goal_API_status'];reconstructed['research_goal_active']=True
    need(pin(enc(reconstructed))==oldpins['SOURCE_PREPARATION_RECORD.json'],'reconstruct exact historical4375 record')
    log=read(PREP/'RESEARCH_LOG.md');need(pin(log)=={'bytes':1665,'sha256':'51a9e475ce0621a8a4e0b67ec5203870c6315b69a925e826a2a6b9776e2ce469'},'log pin')
    need(pin(log[:1037])==oldpins['RESEARCH_LOG.md'],'exact historical1037 log prefix')
    need(b'disclosure-only metadata clarification' in log[1037:] and b'no tests rerun' in log[1037:].lower(),'append explicitly disclosure only')
    oldm=copy.deepcopy(current);oldm['UTC']='2026-10-17T22:37:30.324507+00:00';oldm['total_bytes']=80077
    for row in oldm['files']:
        row.update(oldpins[row['path']])
    need(pin(enc(oldm))=={'bytes':2052,'sha256':'685af682af841e6e38856d1ff7dfff78cf3cc02737593eff5ddd7f57cf01fe45'},'reconstruct exact original manifest with only pins/total/date updates')
    olds=copy.deepcopy(seal);olds['UTC']='2026-10-17T22:37:30.324507+00:00';olds['selected_bytes']=80077
    olds['manifest'].update({'bytes':2052,'sha256':'685af682af841e6e38856d1ff7dfff78cf3cc02737593eff5ddd7f57cf01fe45'})
    need(pin(enc(olds))=={'bytes':736,'sha256':'e3890404fa107018bae9520014695bac42babf4db495aace4bb726242b308f81'},'reconstruct exact original seal')
    need(actual['status_only_intake_after_pr212.py']=={'bytes':24760,'sha256':'0292388c3722d04cb2c11108d409c14759b61a370b0478fbbef41c92e19349eb'}
      and actual['offline_source_controls.py']==oldpins['offline_source_controls.py']
      and actual['OFFLINE_SOURCE_CONTROLS_RESULT.json']==oldpins['OFFLINE_SOURCE_CONTROLS_RESULT.json'],'helper/producer116 source/evidence unchanged')
    report=read(BASE/'REPORT.md');priorseal=read(BASE/'EXTERNAL_SEAL.json')
    need(pin(report)=={'bytes':8173,'sha256':'7852b3e5062124e7a05f65fde2d21dfe7376779e1dd7f38af971c4105bc5c49f'}
      and pin(priorseal)=={'bytes':576,'sha256':'af0bf9be61302c855eb0d642ec97d8d058df6ad808da5eb3a1c0b120a13e07e1'},'initial independent review unchanged')
    result={'schema':'after212-independent-metadata-delta-verification-v1','exact_two_payload_delta':delta,
      'new_source_manifest':pin(raw),'new_source_seal':pin(sealraw),'new_payload_count':8,'new_payload_bytes':80788,
      'all_final_payload_pins_modes_verified':actual,'historical_record_log_manifest_seal_exactly_reconstructed':True,
      'helper_and116_and133_test_evidence_unchanged':True,'tests_rerun':False,'new_source_or_intake_execution':False,
      'mandatory_findings':[],'source_only_recommendation_unchanged_with_new_metadata_qualification':True}
    b=enc(result);fd=os.open(BASE/'METADATA_DELTA_RESULT_01.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
    try:need(os.write(fd,b)==len(b),'full result');os.fsync(fd)
    finally:os.close(fd)
    print(json.dumps({'result':pin(b),'metadata_only':True,'helper_or_controls_executed':False}))
if __name__=='__main__':main()
