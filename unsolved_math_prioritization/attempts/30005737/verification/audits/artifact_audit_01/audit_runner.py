#!/usr/bin/env python3
"""Independent original-packet audit. Standard library only; never writes source.
Every process's raw output and receipt are persisted before outcome validation.
"""
from pathlib import Path
import base64, collections, copy, datetime, hashlib, importlib.util, io, json, os
import shutil, struct, subprocess, sys, zipfile

BASE=Path(__file__).resolve().parent
PARENT=BASE.parent
TMP=BASE/'private_tmp'
PACKET=TMP/'packet'
RUNS=TMP/'runs'
EXPECTED_MANIFEST='1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c'
EXPECTED_NATIVE='b27d5dbb0f92c0ab330bf44891ec4467f7d8c593cef610196cbd82d4cc6d5298'
PYTHON=sys.executable
ENV={'PATH':'/opt/homebrew/bin:/usr/bin:/bin','TMPDIR':str(TMP),'LC_ALL':'C','LANG':'C'}
RECEIPTS=[]
OBS=[]

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def write_json(p,o): p.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def journal(p,o):
    with p.open('a') as f:
        f.write(json.dumps(o,sort_keys=True)+'\n'); f.flush(); os.fsync(f.fileno())
def log(message,percent):
    with (BASE/'RESEARCH_LOG.md').open('a') as f:
        f.write('- '+now()+' — '+message+' Audit completion estimate: '+str(percent)+'%.\n'); f.flush(); os.fsync(f.fileno())
def require(x,m):
    if not x: raise RuntimeError(m)
def run(label,args,cwd=PACKET,extra_env=None,timeout=45):
    env=dict(ENV); env.update(extra_env or {})
    start=now()
    p=subprocess.run([PYTHON,*args],cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
    end=now()
    # Persist original byte streams and receipt immediately; do not infer pass/fail first.
    (RUNS/(label+'.stdout')).write_bytes(p.stdout)
    (RUNS/(label+'.stderr')).write_bytes(p.stderr)
    receipt={'label':label,'start_utc':start,'end_utc':end,'returncode':p.returncode,
      'argv':['python',*[str(a).replace(str(BASE),'<audit>').replace(str(PARENT),'<audit-parent>') for a in args]],
      'cwd':str(cwd.relative_to(BASE)),'environment_keys':sorted(env),
      'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),
      'stderr_bytes':len(p.stderr),'stderr_sha256':sha(p.stderr),
      'raw_stdout':'private_tmp/runs/'+label+'.stdout','raw_stderr':'private_tmp/runs/'+label+'.stderr'}
    journal(BASE/'PROCESS_RECEIPTS.jsonl',receipt); RECEIPTS.append(receipt)
    return p

def observe(label,p,expected,detail,exact=None):
    row={'label':label,'expected':expected,'observed':'accept' if p.returncode==0 else 'reject',
         'returncode':p.returncode,'detail':detail,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)}
    if exact is not None: row['stdout_matches_frozen_bytes']=p.stdout==exact
    if p.returncode: row['last_stderr_line']=p.stderr.decode('utf8','replace').strip().splitlines()[-1].replace(str(BASE),'<audit>') if p.stderr else ''
    journal(BASE/'OBSERVATIONS.jsonl',row); OBS.append(row)
    return row

def reset():
    if PACKET.exists(): shutil.rmtree(PACKET)
    PACKET.mkdir(parents=True)
    for name,b in ORIGINAL.items():
        f=PACKET/name; f.parent.mkdir(parents=True,exist_ok=True); f.write_bytes(b)

def publication_refresh():
    m=json.loads((PACKET/'PUBLICATION_MANIFEST.json').read_bytes())
    for e in m['files']:
        b=(PACKET/e['path']).read_bytes(); e['bytes']=len(b); e['sha256']=sha(b)
    write_json(PACKET/'PUBLICATION_MANIFEST.json',m)

def zip_rebuild(payloads=None,infos=None,comment=b'',tail=b''):
    payloads=payloads or {i.filename:(PACKET/'authored'/i.filename).read_bytes() for i in ZINFOS}
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w') as z:
        z.comment=comment
        for i in infos or ZINFOS:
            z.writestr(copy.copy(i),payloads[i.filename])
    (PACKET/'AUTHOR_CANDIDATE.zip').write_bytes(out.getvalue()+tail)

def author_refresh():
    m=json.loads((PACKET/'authored/MANIFEST.json').read_bytes())
    for e in m['files']:
        b=(PACKET/'authored'/e['path']).read_bytes(); e['bytes']=len(b);e['sha256']=sha(b)
    write_json(PACKET/'authored/MANIFEST.json',m)
    zip_rebuild(); publication_refresh()

def case(label,mutation,expected,detail,optimized=False):
    reset(); mutation()
    args=['-I','-S','-B']+(['-O'] if optimized else [])+['verify_publication.py']
    p=run(label,args); row=observe(label,p,expected,detail)
    require(row['observed']==expected,'Unexpected outcome for '+label)
    return p

TMP.mkdir(exist_ok=True);RUNS.mkdir(exist_ok=True)
mb=(PARENT/'SOURCE_MANIFEST.json').read_bytes()
require(sha(mb)==EXPECTED_MANIFEST,'External source manifest mismatch')
sm=json.loads(mb)
ORIGINAL={}
pins=[]
for e in sm['files']:
    f=PARENT/'source'/e['path']; b=f.read_bytes()
    require(f.is_file() and not f.is_symlink() and len(b)==e['bytes'] and sha(b)==e['sha256'],'External source mismatch '+e['path'])
    require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob'],'Git blob mismatch')
    ORIGINAL[e['path']]=b
    pins.append({'path':e['path'],'bytes':len(b),'sha256':sha(b),'git_blob':e['git_blob'],'git_mode':e['git_mode']})
require(len(ORIGINAL)==18 and sum(map(len,ORIGINAL.values()))==91564,'Unexpected source inventory')
nb=(PARENT/'private_native/canonical_pair.json').read_bytes()
require(len(nb)==3524 and sha(nb)==EXPECTED_NATIVE,'Native pair mismatch')
write_json(BASE/'AUTHENTICATION.json',{'timestamp_utc':now(),'source_head':sm['original_head'],'external_manifest_sha256':sha(mb),'files':pins,'file_count':18,'total_bytes':91564,'native_pair':{'bytes':3524,'sha256':sha(nb)},'original_effort':'1/5'})
log('Reauthenticated all 18 source files and complete native pair. Both original Python files and all manifests were read completely before any original-code execution. Standard-library CPython runtime available; earlier ENOSPC and Xcode-license failures retained separately.',20)

# Lossless ZIP metadata inventory. No extraction or normalization of names.
zb=ORIGINAL['AUTHOR_CANDIDATE.zip']
zf=zipfile.ZipFile(io.BytesIO(zb));ZINFOS=zf.infolist()
eocd=zb.rfind(b'PK\x05\x06');endrec=struct.unpack_from('<4s4H2LH',zb,eocd)
cd_offset=endrec[6]; cd_size=endrec[5]
central_pos=cd_offset;members=[]
for info in ZINFOS:
    require(zb[central_pos:central_pos+4]==b'PK\x01\x02','Central signature')
    nlen,xlen,clen=struct.unpack_from('<3H',zb,central_pos+28)
    central=zb[central_pos:central_pos+46+nlen+xlen+clen]
    rawname=zb[central_pos+46:central_pos+46+nlen]
    local=info.header_offset
    require(zb[local:local+4]==b'PK\x03\x04','Local signature')
    ln,lx=struct.unpack_from('<2H',zb,local+26)
    local_header=zb[local:local+30+ln+lx]
    compressed=zb[local+30+ln+lx:local+30+ln+lx+info.compress_size]
    payload=zf.read(info)
    authored=ORIGINAL.get('authored/'+info.filename)
    members.append({'filename':info.filename,'raw_central_name_base64':base64.b64encode(rawname).decode(),
      'central_record_base64':base64.b64encode(central).decode(),'local_header_base64':base64.b64encode(local_header).decode(),
      'date_time':list(info.date_time),'compression':info.compress_type,'compressed_bytes':info.compress_size,
      'compressed_sha256':sha(compressed),'payload_bytes':len(payload),'payload_sha256':sha(payload),
      'CRC32_hex':format(info.CRC,'08x'),'flag_bits':info.flag_bits,'create_system':info.create_system,
      'create_version':info.create_version,'extract_version':info.extract_version,'external_attr':info.external_attr,
      'internal_attr':info.internal_attr,'volume':info.volume,'header_offset':info.header_offset,
      'extra_base64':base64.b64encode(info.extra).decode(),'comment_base64':base64.b64encode(info.comment).decode(),
      'byte_identical_to_authored':authored==payload,'is_directory':info.is_dir()})
    central_pos+=len(central)
write_json(BASE/'ZIP_INVENTORY.json',{'archive_bytes':len(zb),'archive_sha256':sha(zb),'members':members,
 'member_count':len(members),'central_directory_offset':cd_offset,'central_directory_bytes':cd_size,
 'eocd_and_trailing_base64':base64.b64encode(zb[eocd:]).decode(),'archive_comment_base64':base64.b64encode(zf.comment).decode(),
 'full_archive_preserved':'private_tmp/packet/AUTHOR_CANDIDATE.zip; source/AUTHOR_CANDIDATE.zip remains authoritative',
 'all_members_byte_identical_to_authored':all(m['byte_identical_to_authored'] for m in members),
 'all_members_regular_mode_100644':all((i.external_attr>>16)==0o100644 for i in ZINFOS),
 'central_records_exactly_partition_directory':central_pos==cd_offset+cd_size})
require(len(members)==9 and all(m['byte_identical_to_authored'] for m in members),'ZIP preservation failure')
reset()
frozen=ORIGINAL['authored/CHECK_RESULTS.json']
for opt in (False,True):
    tag='optimized' if opt else 'normal';flags=['-I','-S','-B']+(['-O'] if opt else [])
    p=run('checker_'+tag,flags+['authored/check_algebra.py'])
    observe('checker_'+tag,p,'accept','Unmodified original checker in private copied original packet',frozen)
    require(p.returncode==0 and p.stdout==frozen and p.stderr==b'','Original checker reproduction failed')
    probe=run('flags_'+tag,flags+['-c','import sys,json;print(json.dumps({"version":sys.version,"flags":str(sys.flags),"optimize":sys.flags.optimize,"assertions_active":__debug__}))'])
    require(probe.returncode==0,'Flags probe failed')
    write_json(BASE/('FLAGS_'+tag.upper()+'.json'),json.loads(probe.stdout))
    p=run('verifier_'+tag,flags+['verify_publication.py'])
    observe('verifier_'+tag,p,'accept','Unmodified original publication verifier in private copied original packet')
    require(p.returncode==0 and p.stderr==b'','Original verifier reproduction failed')
log('Original checker and publication verifier reproduced successfully in genuine normal and optimized processes. Each checker stdout is exactly the frozen 966 bytes. Original ZIP all nine members and complete metadata inventoried; source preservation holds.',45)

# Count exact kinds of conditions without changing original source bytes.
trace_code="""import collections,importlib.util,json,sys
s=importlib.util.spec_from_file_location('original','authored/check_algebra.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
c=collections.Counter();old=m.require
def counted(x,msg):
 c[msg]+=1
 return old(x,msg)
m.require=counted
r=m.main()
print(json.dumps({'flags':str(sys.flags),'checks':r['checks'],'condition_messages':dict(c),'unique_condition_messages':len(c)},sort_keys=True,indent=2))
"""
p=run('condition_attribution',['-I','-S','-B','-c',trace_code])
require(p.returncode==0,'Attribution failed')
write_json(BASE/'CONDITION_ATTRIBUTION.json',json.loads(p.stdout))

# Test explicit negative algebra and exception behavior in both actual process modes.
bad_code="""import importlib.util,json,sys
s=importlib.util.spec_from_file_location('original','authored/check_algebra.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
errors={}
try: m.require(False,'deliberate false condition')
except RuntimeError as e: errors['require']=str(e)
try: m.verify_pa('R_identity',3,m.sl2,lambda x,y:m.sl2(x,y))
except RuntimeError as e: errors['R_identity']=str(e)
print(json.dumps({'flags':str(sys.flags),'errors':errors},sort_keys=True))
if len(errors)!=2: raise RuntimeError('negative controls were accepted')
"""
for opt in (False,True):
    label='algebra_negative_'+('optimized' if opt else 'normal')
    p=run(label,['-I','-S','-B']+(['-O'] if opt else [])+['-c',bad_code])
    observe(label,p,'accept','Harness succeeded only if original require(False) and PA2-invalid R=I both raised RuntimeError')
    require(p.returncode==0,'Negative algebra control failed')
    write_json(BASE/(label.upper()+'.json'),json.loads(p.stdout))

# Corruptions with unchanged manifests: independent digest boundary must reject.
def size_tamper(): (PACKET/'authored/PROOF.md').write_bytes(ORIGINAL['authored/PROOF.md']+b'X')
def hash_tamper():
    b=ORIGINAL['authored/PROOF.md'];(PACKET/'authored/PROOF.md').write_bytes(b'X'+b[1:])
def extra_file(): (PACKET/'EXTRA.txt').write_bytes(b'extra')
def missing_file(): (PACKET/'authored/PROOF.md').unlink()
def pub_duplicate():
    m=json.loads(ORIGINAL['PUBLICATION_MANIFEST.json']);m['files'].append(copy.deepcopy(m['files'][0]));write_json(PACKET/'PUBLICATION_MANIFEST.json',m)
def pub_unsafe():
    m=json.loads(ORIGINAL['PUBLICATION_MANIFEST.json']);m['files'][0]['path']='../ACCEPTANCE_REPORT.md';write_json(PACKET/'PUBLICATION_MANIFEST.json',m)
def invalid_json(): (PACKET/'PUBLICATION_MANIFEST.json').write_bytes(b'{invalid')
for opt in (False,True):
    for name,fn in [('size',size_tamper),('hash',hash_tamper),('extra',extra_file),('missing',missing_file),('duplicate_path',pub_duplicate),('unsafe_path',pub_unsafe),('invalid_json',invalid_json)]:
        case('corrupt_'+name+('_O' if opt else ''),fn,'reject','Unchanged external/public payload hashes except mutation under test',opt)

# Self-describing manifest schema and file-type boundaries.
def pub_metadata():
    m=json.loads(ORIGINAL['PUBLICATION_MANIFEST.json']);m.update(problem_id=-1,rank=-1,status='formally_proved',turns='999/5',original_archive_contains_audits=True);write_json(PACKET/'PUBLICATION_MANIFEST.json',m)
def duplicate_json_key():
    raw=ORIGINAL['PUBLICATION_MANIFEST.json'];(PACKET/'PUBLICATION_MANIFEST.json').write_bytes(b'{"files":[],"problem_id":-1,'+raw.lstrip()[1:])
def cache_payload():
    d=PACKET/'__pycache__';d.mkdir();(d/'not_bytecode.txt').write_bytes(b'unlisted arbitrary payload')
def symlink_proof():
    out=TMP/'proof_reference.md';out.write_bytes(ORIGINAL['authored/PROOF.md']);(PACKET/'authored/PROOF.md').unlink();(PACKET/'authored/PROOF.md').symlink_to(out)
def dangling_symlink(): (PACKET/'DANGLING').symlink_to(TMP/'does_not_exist')
for label,fn,detail in [
 ('accepted_wrong_metadata',pub_metadata,'Problem identity/status/turns and archive-audit metadata are not semantically checked'),
 ('accepted_duplicate_json_key',duplicate_json_key,'json.loads accepts duplicate object keys, retaining final value'),
 ('accepted_nonbytecode_cache_file',cache_payload,'Any file below a __pycache__ path component is ignored, not only bytecode'),
 ('accepted_external_symlink',symlink_proof,'Matching proof bytes may be read through an external symlink; regular-file requirement absent'),
 ('accepted_dangling_symlink',dangling_symlink,'A dangling symlink is not is_file and is ignored')]:
    case(label,fn,'accept',detail)

# Deeper ZIP checks, with outer hashes deliberately refreshed, remain independent of payload byte checks.
def zip_payload_bad():
    payload={i.filename:(PACKET/'authored'/i.filename).read_bytes() for i in ZINFOS};payload['PROOF.md']=b'wrong';zip_rebuild(payload);publication_refresh()
def zip_missing(): zip_rebuild(infos=ZINFOS[:-1]);publication_refresh()
def zip_extra():
    zip_rebuild()
    with zipfile.ZipFile(PACKET/'AUTHOR_CANDIDATE.zip','a') as z:z.writestr('EXTRA.txt',b'x')
    publication_refresh()
def zip_duplicate():
    zip_rebuild()
    with zipfile.ZipFile(PACKET/'AUTHOR_CANDIDATE.zip','a') as z:z.writestr(ZINFOS[0].filename,(PACKET/'authored'/ZINFOS[0].filename).read_bytes())
    publication_refresh()
def zip_traversal():
    payload={i.filename:(PACKET/'authored'/i.filename).read_bytes() for i in ZINFOS};infos=[copy.copy(i) for i in ZINFOS];old=infos[0].filename;infos[0].filename='../'+old;payload[infos[0].filename]=payload.pop(old);zip_rebuild(payload,infos);publication_refresh()
def zip_symlink_mode():
    infos=[copy.copy(i) for i in ZINFOS];infos[0].external_attr=(0o120777<<16);zip_rebuild(infos=infos);publication_refresh()
def zip_extra_metadata(): zip_rebuild(comment=b'changed archive metadata',tail=b'nonzip trailing bytes');publication_refresh()
for label,fn,outcome,detail in [
 ('zip_wrong_payload',zip_payload_bad,'reject','Outer ZIP digest refreshed; member bytes differ from original authored file'),
 ('zip_missing_member',zip_missing,'reject','Outer ZIP digest refreshed; eight members'),
 ('zip_extra_member',zip_extra,'reject','Outer ZIP digest refreshed; ten members'),
 ('zip_duplicate_member',zip_duplicate,'reject','Outer ZIP digest refreshed; duplicate name and ten entries'),
 ('zip_traversal_member',zip_traversal,'reject','Outer ZIP digest refreshed; archive name is outside fixed original-name set'),
 ('accepted_zip_symlink_metadata',zip_symlink_mode,'accept','After outer rehash, original verifier checks member contents but ignores Unix ZIP file mode'),
 ('accepted_zip_comment_trailer',zip_extra_metadata,'accept','After outer rehash, member payload equality does not pin complete original archive metadata/trailer')]:
    case(label,fn,outcome,detail)

# Original manifest has weaker list/path validation than publication manifest.
def original_duplicate():
    m=json.loads(ORIGINAL['authored/MANIFEST.json']);m['files'].append(copy.deepcopy(m['files'][0]));write_json(PACKET/'authored/MANIFEST.json',m);zip_rebuild();publication_refresh()
def original_traversal():
    m=json.loads(ORIGINAL['authored/MANIFEST.json']);entry=next(e for e in m['files'] if e['path']=='PROOF.md');entry['path']='../authored/PROOF.md';write_json(PACKET/'authored/MANIFEST.json',m)
    payload={i.filename:(PACKET/'authored'/i.filename).read_bytes() for i in ZINFOS};infos=[copy.copy(i) for i in ZINFOS]
    for i in infos:
        if i.filename=='PROOF.md':i.filename='../authored/PROOF.md'
    payload['../authored/PROOF.md']=payload.pop('PROOF.md');zip_rebuild(payload,infos);publication_refresh()
def false_proof(): (PACKET/'authored/PROOF.md').write_bytes(b'# False proof control\nEvery complex Lie algebra is semisimple. No proof.\n');author_refresh()
def frozen_tamper():
    b=ORIGINAL['authored/CHECK_RESULTS.json'].replace(b'2896',b'2895');(PACKET/'authored/CHECK_RESULTS.json').write_bytes(b);author_refresh()
def checker_stub():
    b=ORIGINAL['authored/CHECK_RESULTS.json'];code=b'import sys\nsys.stdout.buffer.write('+repr(b).encode()+b')\n';(PACKET/'authored/check_algebra.py').write_bytes(code);author_refresh()
def stub_scope_bad():
    b=ORIGINAL['authored/CHECK_RESULTS.json'].replace(b'2896',b'2895');(PACKET/'authored/CHECK_RESULTS.json').write_bytes(b);(PACKET/'authored/check_algebra.py').write_bytes(b'import sys\nsys.stdout.buffer.write('+repr(b).encode()+b')\n');author_refresh()
for label,fn,outcome,detail in [
 ('accepted_original_manifest_duplicate',original_duplicate,'accept','Unique original names remain eight but list contains nine entries; no duplicate-entry check'),
 ('accepted_original_manifest_traversal',original_traversal,'accept','Original manifest and matching archive can use ../authored/PROOF.md; only publication paths have unsafe-path test'),
 ('accepted_false_proof_rehashed',false_proof,'accept','All internal hashes refreshed; verifier never reads mathematical prose for truth'),
 ('frozen_result_mismatch',frozen_tamper,'reject','Original checker output differs from internally repinned frozen output'),
 ('accepted_checker_stub_rehashed',checker_stub,'accept','All internal hashes refreshed; a stub printing frozen bytes passes self-attestation'),
 ('stub_wrong_scope_count',stub_scope_bad,'reject','Even mutually consistent stub/frozen JSON must report literal checks=2896')]:
    case(label,fn,outcome,detail)
log('Completed integrity, parser, ZIP, file-type, frozen-output, and semantic negative controls. All accepted mutations are explicitly recorded; accepted repinned packets do not match external authenticated source. Finite diagnostics are not global proof certificates.',80)

# Record actual child flags using a benign sitecustomize; preserve original code bytes.
reset();site=TMP/'flag_site';site.mkdir(exist_ok=True);flaglog=TMP/'child_flags.jsonl'
(site/'sitecustomize.py').write_text("import sys,json,os\nwith open(os.environ['AUDIT_FLAGS_LOG'],'a') as f:f.write(json.dumps({'optimize':sys.flags.optimize,'flags':str(sys.flags),'argv':[os.path.basename(a) for a in sys.argv]})+'\\n')\n")
write_json(BASE/'SITE_FLAGS_RECORDER_SOURCE.json',{'source':(site/'sitecustomize.py').read_text(),'purpose':'Benign independent process-flag observation; no original-code change'})
for setting in ('baseline','hostile_optimization'):
    if flaglog.exists():flaglog.unlink()
    extra={'PYTHONPATH':str(site),'AUDIT_FLAGS_LOG':str(flaglog),'PYTHONDONTWRITEBYTECODE':'1'}
    if setting=='hostile_optimization':extra['PYTHONOPTIMIZE']='2'
    p=run('verifier_childflags_'+setting,['-I','-S','-B','verify_publication.py'],extra_env=extra)
    row=observe('verifier_childflags_'+setting,p,'accept','Outer isolated interpreter ignores Python environment, original verifier children do not use -I or -S')
    require(p.returncode==0,'Flag observation verifier failed')
    rows=[json.loads(x) for x in flaglog.read_text().splitlines()]
    write_json(BASE/('CHILD_FLAGS_'+setting.upper()+'.json'),{'children':rows,'parent_flags':['-I','-S','-B'],'PYTHONOPTIMIZE':extra.get('PYTHONOPTIMIZE'),'expected_child_optimize':[0,1] if setting=='baseline' else [2,2]})
    require([r['optimize'] for r in rows]==([0,1] if setting=='baseline' else [2,2]),'Unexpected real child optimization flags')

# A controlled import override demonstrates the original subprocess trust boundary.
reset();spoof=TMP/'spoof_site';spoof.mkdir(exist_ok=True)
(spoof/'sitecustomize.py').write_text("import os,sys\nif os.path.basename(sys.argv[0])=='check_algebra.py':\n sys.stdout.buffer.write("+repr(frozen)+")\n sys.stdout.buffer.flush()\n os._exit(0)\n")
write_json(BASE/'SITE_SPOOF_SOURCE.json',{'source':(spoof/'sitecustomize.py').read_text(),'purpose':'Deliberate hostile PYTHONPATH control; exits before the original checker executes'})
p=run('accepted_hostile_sitecustomize',['-I','-S','-B','verify_publication.py'],extra_env={'PYTHONPATH':str(spoof),'PYTHONDONTWRITEBYTECODE':'1'})
observe('accepted_hostile_sitecustomize',p,'accept','Unmodified original packet, but child Python environment supplies frozen stdout and exits before checker code')
require(p.returncode==0,'Expected hostile-environment false acceptance did not occur')

# Restore a private exact packet, then verify both copy and untouched original source bytes.
reset();after=[]
for name,b in ORIGINAL.items():
    source=(PARENT/'source'/name).read_bytes();copied=(PACKET/name).read_bytes()
    after.append({'path':name,'source_matches_authenticated':source==b,'private_copy_matches_authenticated':copied==b,'sha256':sha(source)})
write_json(BASE/'FINAL_PRESERVATION.json',{'timestamp_utc':now(),'files':after,'original_zip_sha256':sha((PACKET/'AUTHOR_CANDIDATE.zip').read_bytes()),'all_exact':all(x['source_matches_authenticated'] and x['private_copy_matches_authenticated'] for x in after)})
require(all(x['source_matches_authenticated'] and x['private_copy_matches_authenticated'] for x in after),'Source preservation failed')
write_json(BASE/'SUMMARY.json',{'timestamp_utc':now(),'processes':len(RECEIPTS),'observations':len(OBS),'accepted_mutations':[x['label'] for x in OBS if x['observed']=='accept' and x['label'].startswith('accepted_')],'outcomes_all_as_predicted':all(x['expected']==x['observed'] for x in OBS),'original_effort':'1/5','scope':'Validation only; no publication, priority, formal-proof or global-mathematical-proof certification'})
log('All planned original-code reproduction and mutation controls completed. Preserved source and final private original packet match all 18 external pins. Detailed artifact report remains to be written; no Git or remote mutation occurred.',90)
print(json.dumps({'completed':True,'processes':len(RECEIPTS),'observations':len(OBS),'source_preserved':True},sort_keys=True))
