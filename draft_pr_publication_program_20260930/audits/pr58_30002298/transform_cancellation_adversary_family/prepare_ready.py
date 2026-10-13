"""Prepare only; neither ROOT closer nor ROOT readback is invoked."""
import os
from packet import B,H,I,R,M,d,read,write_once,verify,now

assert not any((B/n).exists() for n in [I,R,M])
controls=read('controls.stdout.bin'); cap=read('controls.CAPTURE.json')
assert controls['checks_passed']==218 and controls['process_pid']==cap['child_pid']==32616
assert cap['exit_code']==0 and cap['source_unchanged'] is True
assert controls['script_sha256']==d(B/'controls.py')['sha256']==cap['source_sha256_before']==cap['source_sha256_after']
for label,source,exit_code in [('controls','controls.py',0),('slow_attempt','controls_slow_attempt.py',-15)]:
    c=read(label+'.CAPTURE.json')
    assert c['exit_code']==exit_code and c['source_unchanged'] is True
    assert c['source_sha256_before']==c['source_sha256_after']==d(B/source)['sha256']
    for stream in ['stdout','stderr']:
        desc=d(B/(label+'.'+stream+'.bin'))
        assert desc['bytes']==c[stream+'_bytes'] and desc['sha256']==c[stream+'_sha256']
source=read('source_pin.stdout.bin')
assert source['process_pid']==35105 and source['original_science_body_count']==17
assert source['script_sha256']==d(B/'source_pin.py')['sha256']
assert (B/'source_pin.stderr.bin').stat().st_size==0
names=sorted(p.name for p in B.iterdir())
for name in names: d(B/name); os.chmod(B/name,0o444)
os.chmod(B,0o755)
stamp=now()
index={'schema':'pr58-transform-fixed-index/v1','head':H,'operator':'transform_cancellation_adversary','preparer_pid':os.getpid(),'prepared_utc':stamp,'directory':{'path':str(B),'mode_07777':'0755','full_st_mode':oct(B.lstat().st_mode)},'bodies':[d(B/n) for n in names],'reserved':[I,R,M],'no_original_SOURCE_or_ROOT_credit':True}
write_once(I,index)
write_once(R,{'schema':'pr58-transform-ready/v1','head':H,'preparer_pid':os.getpid(),'prepared_utc':stamp,'bindings':[d(B/n) for n in [I,'REPORT.md','VERDICT.json']],'SELF_manifest_absent_at_handoff':True,'ROOT_helpers_unexecuted_at_handoff':True,'ROOT_or_math_acceptance':False})
verify(False)
print({'preparer_pid':os.getpid(),'utc':stamp,'bodies':len(names),'prepared_regular_files':len(names)+2,'INDEX_sha256':d(B/I)['sha256'],'READY_sha256':d(B/R)['sha256'],'SELF_absent':not (B/M).exists()})
