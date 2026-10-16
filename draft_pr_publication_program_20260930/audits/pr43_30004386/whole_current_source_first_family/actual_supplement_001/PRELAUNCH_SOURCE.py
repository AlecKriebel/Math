"""Own final static inspection of ancillary source-only and retained failure inputs."""
from pathlib import Path
import datetime,hashlib,json,os,stat
OWN=Path.cwd().resolve(); A=OWN.parent; C=A/'reviewed_candidate'
start=datetime.datetime.now(datetime.timezone.utc).isoformat(); reads=[]; checks=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p,role):
    b=p.read_bytes(); reads.append({'path':str(p.resolve()),'bytes':len(b),'sha256':sha(b),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o'),'role':role,'entire_bytes_read':True,'executed':False});return b
def j(p,role): return json.loads(read(p,role))
def ok(v,name):
    checks.append({'name':name,'passed':bool(v)})
    if not v: raise AssertionError(name)

adv=A/'current_source_adversary_family'; am=j(adv/'SELF_MANIFEST.json','attributed pre-execution source-adversary manifest')
ok(sha((adv/'SELF_MANIFEST.json').read_bytes())=='8ffa04e6410864c7095d8c7d20bd3f635c6a0c58daf64fc4b0715b55c9afb859','exact independent source-adversary seal')
ok(am['files_count']==20 and {str(p.relative_to(adv)) for p in adv.rglob('*') if p.is_file()}=={r['path'] for r in am['files']}|{'SELF_MANIFEST.json'},'source adversary20+self exact closure')
for r in am['files']:
    b=read(adv/r['path'],'attributed source-adversary individual member; outside own authorship')
    ok(sha(b)==r['sha256'] and len(b)==r['bytes'] and stat.S_IMODE((adv/r['path']).stat().st_mode)==0o444,'source adversary individual hash/full0444 '+r['path'])
for p in (A/'root_current_prerequisites_authoring_actual_capture').rglob('*'):
    if p.is_file(): read(p,'actual ROOT prerequisite authoring completed operation at original path')
rp=j(A/'ROOT_CURRENT_PREREQUISITES_INSPECTION.json','actual ROOT prerequisite entire result')
ok(rp['status']=='PASS_ROOT_GENUINE_CURRENT_PREREQUISITES' and rp['source_adversary_manifest_sha256']==sha((adv/'SELF_MANIFEST.json').read_bytes()),'ROOT prerequisite binds source adversary')
for r in rp['complete_input_read_rows']:
    p=A.parents[2]/r['path'];b=read(p,'ROOT prerequisite individual attributed input now rechecked')
    ok(len(b)==r['bytes'] and sha(b)==r['sha256'],'ROOT prerequisite input entire identity '+r['path'])

prep=A/'current_preparation_family'; pm=j(prep/'PREPARATION_MANIFEST.json','closed source preparation manifest')
ok(pm['files_count']==38 and {str(p.relative_to(prep)) for p in prep.rglob('*') if p.is_file()}=={r['path'] for r in pm['files']}|{'PREPARATION_MANIFEST.json'},'preparation38+self exact closure')
for r in pm['files']:
    b=read(prep/r['path'],'attributed source preparation individual member')
    ok(len(b)==r['bytes'] and sha(b)==r['sha256'],'preparation individual hash '+r['path'])
builder=(prep/'prepare_current_packet.py').read_bytes(); old=(prep/'builder_before_final_tool_edit_RECONSTRUCTED_AFTER.py').read_bytes()
line=b"        'audit_relative_inner_attempt': attempt.relative_to(audit).as_posix(),\n"
ok(builder.count(line)==1 and builder.replace(line,b'',1)==old,'historical builder reconstruction exactly one known line')
op=(prep/'capture_root_builder_operation.py').read_bytes(); oldop=(prep/'operator_before_final_tool_edit_RECONSTRUCTED_AFTER.py').read_bytes()
new=b"        for key, path, prior in [('builder_unchanged_after_child', builder, source),\n                                 ('operator_unchanged_after_child', script, operator)]:\n            try:\n                record[key] = regular(path) == prior\n            except BaseException:\n                record[key] = False\n                record[key + '_read_failure'] = traceback.format_exc()\n"
old=b"        record['builder_unchanged_after_child'] = regular(builder) == source\n        record['operator_unchanged_after_child'] = regular(script) == operator\n"
ok(op.count(new)==1 and op.replace(new,old,1)==oldop,'historical operator reconstruction exact known failure-record change')

prob=A/'probability_source_family'
first=j(prob/'captures/source_inspection_capture.json','first source predicate actual capture')
corrected=j(prob/'captures/source_inspection_corrected_capture.json','corrected source predicate actual capture')
for label,cap,src in [('source_inspection',first,'captures/first_source_reconstructed_after_execution.py'),('source_inspection_corrected',corrected,'inspect_sources_and_snapshot.py')]:
    ok(cap['returncode']==0 and type(cap['child_pid']) is int,'source predicate actual process '+label)
    ok(sha(read(prob/src,'explicit original reconstructed or corrected source'))==cap['prelaunch_source_sha256'],'predicate source complete identity '+label)
    for ch in ['stdout','stderr']:
        b=read(prob/'captures'/(label+'.'+ch+'.txt'),'complete actual predicate '+ch)
        ok(len(b)==cap[ch+'_bytes'] and sha(b)==cap[ch+'_sha256'],'complete predicate stream '+label+' '+ch)
raw=json.loads((prob/'captures/source_inspection.stdout.txt').read_bytes()); fixed=json.loads((prob/'captures/source_inspection_corrected.stdout.txt').read_bytes())
ok(len(raw['checks'])==len(fixed['checks'])==44 and sum(not r['passed'] for r in raw['checks'])==1 and raw['all_finite_source_predicates_passed'] is False and all(r['passed'] for r in fixed['checks']),'one retained incorrect date predicate and44 corrected source predicates')
comp=A/'compactness_source_family'; cr=j(comp/'own_controls_actual_capture_001/CAPTURE.json','compactness actual own-controls capture')
for r in cr['FILE']:
    b=read(Path(r['path']),'compactness complete captured source/stream')
    ok(len(b)==r['bytes'] and sha(b)==r['sha256'],'compactness captured entire identity '+r['path'])
cout=json.loads((comp/'own_controls_actual_capture_001/stdout.bin').read_bytes())
ok(cr['exit_code']==0 and cout['assertions']==34621 and cout['accepted_signed_vectors']==1281,'compactness exact finite controls scoped counts')

og=j(A/'ORIGINAL_GIT_COMMANDS.json','original complete export child command index')
for r in og:
    for ch in ['stdout','stderr']:
        z=r[ch];b=read(A/'original_git_commands'/z['path'],'original export full actual child '+ch)
        ok(len(b)==z['bytes'] and sha(b)==z['sha256'],'original actual complete stream '+z['path'])
    ok(r['actual_execution'] is True and r['completed'] is True and type(r['pid']) is int and r['exit_code']==0,'original actual export process')
o={'schema':'SUPPLEMENTAL_CURRENT_SOURCE_ANCILLARY_READ_v1','started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_pid':os.getpid(),'reads':reads,'checks':checks,'all_passed':True,'foreign_execution':False,'native_git_remote_mutations':False,'scope':'Ancillary exact source-adversary, ROOT prerequisite, preparation, original/failure capture reading only. No old safety opinion is transferred to this whole-current verdict.'}
(OWN/'SUPPLEMENTAL_SOURCE_READ.json').write_text(json.dumps(o,indent=2)+'\n')
print(json.dumps({k:v for k,v in o.items() if k not in ['reads','checks']},indent=2)); print('Individual reads',len(reads),'predicates',len(checks))
