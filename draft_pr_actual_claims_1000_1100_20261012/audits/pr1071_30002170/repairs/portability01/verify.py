"""Resolve immutable custody and independently verify closed archive/native input."""
import collections, hashlib, json, os, struct, subprocess, sys, zipfile, zlib
sys.dont_write_bytecode=True
from datetime import datetime,timezone
from pathlib import Path
D=Path(__file__).resolve().parent;A=D.parents[1];P=A/'NEWpreprint_v1_0';S=D/'scratch';R=A/'repairs/case_alias01';T=A/'finalization/terminal_admin_20261015';Q=A/'reviews/package_03';ZIP='PR1071_preprint_v1_0_support.zip'
def now():return datetime.now(timezone.utc).isoformat()
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def read(p):return json.loads(p.read_text())
def dump(p,o):
    tmp=p.with_name(p.name+'.verify-tmp');tmp.write_text(json.dumps(o,indent=2)+'\n');os.replace(tmp,p)
def pin(p,n):
    b=p.read_bytes();return {'path':str(n),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def matches(p,r):
    if not p.is_file() or p.is_symlink():return False
    b=p.read_bytes();return len(b)==r.get('bytes',r.get('size')) and hashlib.sha256(b).hexdigest()==r['sha256']
index=collections.defaultdict(list)
for p in sorted(A.rglob('*')):
    if p.is_file() and not p.is_symlink() and S not in p.parents:
        r=pin(p,'');index[(r['bytes'],r['sha256'])].append(p)
def resolve(preferred,r):
    if matches(preferred,r):return preferred
    candidates=index[(r.get('bytes',r.get('size')),r['sha256'])]
    need(bool(candidates),'Unresolved exact pin '+str(preferred)+' '+str(r))
    p=candidates[0];need(matches(p,r),'Content resolver failed');return p
def locator(p):
    try:return str(p.relative_to(A))
    except ValueError:return str(p)
hist=read(R/'HISTORICAL_STAGE_RESOLUTION.json');old=read(T/'HISTORICAL_STAGE_RESOLUTION.json')['records'];resolved=[]
need(len(hist['records'])==len(old)==2788 and len(hist['additional_terminal_rows'])==1558,'Original historical row counts')
for i,(r,b) in enumerate(zip(hist['records'],old)):
    need(r['prior_row_index']==i and r['prior_resolution_path']==b['resolved_path'],'Historical ordering/old locator')
    for key in ['stage','captured_path','bytes','sha256']:need(r[key]==b[key],'Original history value '+key)
    p=resolve(A/r['resolved_path'],r);resolved.append({**r,'portability_resolution_path':locator(p),'exact_bytes_rehashed':True})
sets=[('terminal_immediate_inputs',T/'BASELINE_INPUT_PINS.json','records'),('preparation_204',P/'FROZEN_INPUTS.json','records'),('preparation_92',P/'INPUT_OUTPUT_PINS.json','records'),('repair_492_before',A/'repairs/package01/BASELINE_INPUT_PINS.json','records'),('repair_34_outputs',A/'repairs/package01/OUTPUT_PINS.json','records'),('repair_270_current',A/'repairs/package01/CURRENT_OUTPUT_PINS.json','records'),('repair_480_unchanged',A/'repairs/package01/PROTECTED_UNCHANGED.json','unchanged_records'),('whole01_25_outputs',A/'reviews/package_01/OUTPUT_PINS.json','files'),('whole02_25_outputs',A/'reviews/package_02/OUTPUT_PINS.json','files'),('whole02_569_inputs',A/'reviews/package_02/INPUT_PINS.json','files')]
counts={}
for stage,path,key in sets:
    source=read(path)[key];rr=[r for r in hist['records'] if r['stage']==stage];need(len(source)==len(rr),'Stage count '+stage)
    for b,r in zip(source,rr):need((b['path'],b['bytes'],b['sha256'])==(r['captured_path'],r['bytes'],r['sha256']),'Original stage source '+stage)
    counts[stage]=len(rr)
for name in ['OUTPUT_PINS.json','CURRENT_AUDIT_PINS.json','CURRENT_CANDIDATE_PINS.json','PROTECTED_UNCHANGED.json']:
    source=read(T/name)['records'];rr=[r for r in hist['additional_terminal_rows'] if r['stage']==name];need(len(source)==len(rr),'Terminal additional stage count')
    for b,r in zip(source,rr):
        need((b['path'],b['bytes'],b['sha256'])==(r['captured_path'],r['bytes'],r['sha256']),'Terminal additional source')
        p=resolve(A/r['resolved_path'],r);resolved.append({**r,'portability_resolution_path':locator(p),'exact_bytes_rehashed':True})
dump(D/'HISTORICAL_STAGE_RESOLUTION.json',{'utc':now(),'status':'PASS','original2788_values_and_order_preserved':True,'additional1558_values_and_order_preserved':True,'stage_counts':counts,'records':resolved})
latest=[]
for source,base,key in [(R/'BASELINE_INPUT_PINS.json',A,'records'),(R/'PROTECTED_UNCHANGED.json',A,'records'),(R/'CURRENT_CANDIDATE_PINS.json',P,'records'),(R/'CURRENT_AUDIT_PINS.json',A,'records'),(R/'OUTPUT_PINS.json',R,'records'),(R/'CORE_PROTECTED_IDENTITIES.json',A,'records'),(Q/'FROZEN_INPUTS.json',A,'rows'),(Q/'OUTPUT_PINS.json',Q,'records'),(Q/'EXTERNAL_INPUT_PINS.json',Path('/'),'records')]:
    source_rows=read(source)[key]
    for i,r in enumerate(source_rows):
        p=resolve(base/r['path'],r)
        latest.append({'source_manifest':locator(source),'row_index':i,'captured_path':r['path'],'bytes':r.get('bytes',r.get('size')),'sha256':r['sha256'],'resolved_path':locator(p)})
dump(D/'PRIOR_LATEST_INPUT_OUTPUT_PIN_RESOLUTION.json',{'utc':now(),'status':'PASS','records':latest,'meaning':'All case-repair and whole03 input/output/current/protected pins resolved to exact before/current bytes, without rewriting historical manifests.'})
oldmap=read(D/'before/NEWpreprint_v1_0/INPUT_COPY_MAP.json')['copies'];copies=read(P/'INPUT_COPY_MAP.json')['copies'];need(len(oldmap)==128 and len(copies)==140 and copies[:128]==oldmap,'Original128 copy rows/order')
copyrows=[]
for r in copies:
    src=A/r.get('source_snapshot',r['original_path']);dst=P/r['package_copy']
    need(matches(src,r) and matches(dst,r) and src.read_bytes()==dst.read_bytes(),'Source/copy identity '+r['package_copy'])
    copyrows.append({**r,'actual_source':locator(src),'actual_byte_equality':True})
dump(D/'COPY_EQUALITY_RECHECK.json',{'utc':now(),'status':'PASS','original128_values_order_unchanged':True,'records':copyrows})
omissions=[]
for name in ['WHOLE01_COPY_EXCLUSIONS.json','WHOLE02_COPY_EXCLUSIONS.json','CASE_ALIAS_COPY_EXCLUSIONS.json','PORTABILITY_COPY_EXCLUSIONS.json']:
    for r in read(P/name)['records']:
        proposed=A/r['path']
        if not proposed.exists():proposed=A.parents[1]/r['path']
        path=resolve(proposed,r);omissions.append({'ledger':name,**r,'resolved_path':locator(path),'exact_rehashed':True})
dump(D/'INDIVIDUAL_OMISSIONS_RECHECK.json',{'utc':now(),'status':'PASS','records':omissions,'omitted_program_replay_claim':False})
entry=read(D/'BASELINE_INPUT_PINS.json')['rows'];befores={r['original_path']:r for r in read(D/'BEFORE_PINS.json')['rows']};changes=[];protected=[]
need(len(entry)==763 and len(befores)==9,'Entry/permitted counts')
for r in entry:
    p=A/r['path']
    if r['path'] in befores:
        b=befores[r['path']];need(matches(A/b['before_snapshot'],r),'Entry before changed '+r['path'])
        changes.append({'path':r['path'],'before':r,'before_bytes_path_relative_to_audit':b['before_snapshot'],'after':pin(p,r['path'])})
    else:need(matches(p,r),'Unpermitted old input changed '+r['path']);protected.append(r)
newpaths=[str(f.relative_to(A)) for f in sorted(A.rglob('*')) if f.is_file() and not f.is_symlink() and D not in f.parents and str(f.relative_to(A)) not in {r['path'] for r in entry}]
need(len(newpaths)==16 and all(n.startswith('NEWpreprint_v1_0/') for n in newpaths),'Unexpected new audit path')
dump(D/'CHANGE_INVENTORY.json',{'utc':now(),'authorized_existing_changes':changes,'all_new_paths_outside_effort':newpaths})
dump(D/'PROTECTED_UNCHANGED.json',{'utc':now(),'records':protected})
submitted=read(A/'SUBMITTED_PINS.json');need(len(submitted['files'])==9 and submitted['head_oid']=='fc37aa5169a0fe6adae0a254c9ee6c1531a2911f','Submitted identity')
for r in submitted['files']:need(matches(A/r['snapshot_path'],r),'Original submitted bytes')
ag=read(P/'FROZEN_INPUTS.json')['workspace_AGENTS'];need(matches(Path(ag['path']),ag),'AGENTS changed')
native=read(A/'publication/zenodo-deposit.json');metadata=read(P/'metadata.json')
need(set(native)=={'metadata','files'} and native['metadata']==metadata==read(P/'metadata_wrapped.json')['metadata']==read(P/'deposit.json')['metadata'],'Native metadata exact equality')
need(native['files']==[{'path':'../NEWpreprint_v1_0/paper.pdf','name':'paper.pdf'},{'path':'../NEWpreprint_v1_0/'+ZIP,'name':ZIP}],'Native unchanged selected files')
oldbinding=read(D/'before/NEWpreprint_v1_0/UPLOAD_BINDINGS.json');binding=read(P/'UPLOAD_BINDINGS.json');adjusted=json.loads(json.dumps(oldbinding))
for k in ('bytes','sha256'):adjusted['archive'][k]=binding['archive'][k]
adjusted['manifest_sha256']=binding['manifest_sha256'];need(adjusted==binding,'More than three necessary binding scalars changed')
paper=pin(P/'paper.pdf','paper.pdf');tex=pin(P/'paper.tex','paper.tex')
need(paper['bytes']==93113 and paper['sha256']=='33b90a4d846db58ea93efd453c13455fbeb3a29dcaa3e4cc49a68c0a8ebdff5b','PDF identity')
need(tex['sha256']=='4ffbe0d65609213fd91aecf675661ff278e4e1bd5037db8836f1291f5bdc1d78','TeX identity')

# Reconstruct independently from the explicit manifest, close it, THEN compare.
m=read(P/'PACKAGE_MANIFEST.json');names=sorted([r['path'] for r in m['members']]+['PACKAGE_MANIFEST.json']);closed=S/'independent-closed.zip'
with zipfile.ZipFile(closed,'w',allowZip64=False) as independent:
    for n in names:
        header=zipfile.ZipInfo(n,(2026,10,14,0,0,0));header.create_system=3;header.external_attr=(0o100644<<16)
        independent.writestr(header,(P/n).read_bytes(),compress_type=zipfile.ZIP_STORED)
need(closed.read_bytes()==(P/ZIP).read_bytes(),'Closed ZIP bytes differ')
data=(P/ZIP).read_bytes();ziprows=[]
with zipfile.ZipFile(P/ZIP) as z:
    need(z.namelist()==names and z.testzip() is None,'ZIP names/CRC')
    for info in z.infolist():
        payload=(P/info.filename).read_bytes();crc=zlib.crc32(payload)&0xffffffff
        need(z.read(info.filename)==payload and info.CRC==crc,'ZIP payload/CRC')
        need(info.compress_type==0 and info.create_system==3 and info.external_attr==0o100644<<16 and info.date_time==(2026,10,14,0,0,0),'ZIP central attributes')
        h=struct.unpack_from('<IHHHHHIIIHH',data,info.header_offset);sig,version,flag,compression,dostime,dosdate,localcrc,csize,size,nlen,xlen=h
        need(sig==0x04034b50 and flag==0 and compression==0 and localcrc==crc and csize==size==len(payload) and xlen==0,'ZIP local header')
        namebytes=data[info.header_offset+30:info.header_offset+30+nlen];need(namebytes.decode()==info.filename,'ZIP local name')
        start=info.header_offset+30+nlen+xlen;need(data[start:start+size]==payload,'ZIP local raw payload')
        need(dostime==0 and dosdate==((2026-1980)<<9 | 10<<5 |14),'ZIP raw timestamp')
        ziprows.append({'path':info.filename,'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest(),'CRC32':crc,'local_header_checked':True,'central_header_checked':True})
need(data[-22:-18]==b'PK\x05\x06' and struct.unpack_from('<H',data,len(data)-2)[0]==0,'ZIP terminal EOCD/comment')
dump(D/'INDEPENDENT_CLOSED_ZIP.json',{'utc':now(),'status':'PASS','archive':pin(P/ZIP,ZIP),'reconstruction':pin(closed,'scratch/independent-closed.zip'),'comparison_after_close':True,'members':ziprows,'member_count':len(names),'CRC_testzip':None,'headers_payloads_CRC_and_EOCD_checked':True})
nativecommands=[]
tool=Path('/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py')
for py in ('3.11','3.14'):
    for optimized in (False,True):
        argv=['/opt/homebrew/bin/python'+py,'-B',*(['-O'] if optimized else []),str(tool),'check',str(A.resolve()/'publication/zenodo-deposit.json')]
        proc=subprocess.run(argv,capture_output=True,text=True,cwd=S,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        need(proc.returncode==0 and proc.stderr=='','Native local check')
        summary=json.loads(proc.stdout);expected=[{'name':'paper.pdf','size':paper['bytes'],'sha256':paper['sha256']},{'name':ZIP,'size':(P/ZIP).stat().st_size,'sha256':pin(P/ZIP,ZIP)['sha256']}]
        need(summary['files']==expected,'Native actual asset selection')
        nativecommands.append({'utc':now(),'argv':argv,'cwd':str(S),'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'only_local_check':True})
dump(D/'NATIVE_REPOSITORY_LOCAL_CHECK.json',{'utc':now(),'status':'PASS','tool':pin(tool,str(tool)),'dispatch_evidence':'run() lines406-412 load/validate local manifest/files and return check summary before local_state/token/client/network branches at413-415.','commands':nativecommands,'native_manifest':pin(A/'publication/zenodo-deposit.json','publication/zenodo-deposit.json'),'metadata_objects_equal':True})
controls=[]
for tag in ['py311_normal','py311_optimized','py314_normal','py314_optimized']:
    c=read(D/('CONTROLS_'+tag+'.json'));rr=read(D/('COMMANDS_'+tag+'.json'));g=read(D/('GUARDS_'+tag+'.json'))
    need(c['status']=='PASS' and len(rr)==c['actual_commands']==89 and len(g['faults'])==1431,'Complete controls')
    need(all((r['returncode']==r['expected_returncode'] if r['expected_returncode']>=0 else r['returncode']!=0) for r in rr),'Actual command expectation')
    need(all(f['accepted']==f['expected_accepted'] for f in g['faults']),'Actual guard expectation')
    controls.append({'tag':tag,'runtime':c['runtime'],'optimized':c['wrapper_optimized'],'commands':len(rr),'expected_zero_exits':sum(r['expected_returncode']==0 for r in rr),'expected_rejections':sum(r['expected_returncode']==-1 for r in rr),'expected_sentinel_exit91':sum(r['expected_returncode']==91 for r in rr),'guard_controls':len(g['faults']),'guard_accepted_controls':sum(f['accepted'] for f in g['faults']),'coverage':c['coverage']})
with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+now()+' — 90%: all four actual runtime/mode suites passed; 356 commands,5724 guard cases plus source controls, closed ZIP headers/payloads/CRC, all4346 original historical references, newer pin stages,140 source/copy pairs,72 omissions,763 entry inputs and four actual native LOCAL checks validated. Final inventories/seal remain. No whole04/readiness authority.\n')
summary={'utc':now(),'status':'PASS','controls':controls,'actual_support_commands':356,'actual_native_local_commands':4,'guard_controls':5724,'historical_rows':len(resolved),'newer_prior_pin_rows':len(latest),'entry_inputs':len(entry),'existing_changes':len(changes),'protected_unchanged':len(protected),'new_candidate_paths':len(newpaths),'copy_pairs':len(copyrows),'omissions':len(omissions),'archive':pin(P/ZIP,ZIP),'paper':paper,'tex':tex,'native_exact':True,'root_adoption_then_new_complete_whole04_required':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032}
dump(D/'FINAL_VERIFICATION.json',summary);print(json.dumps(summary,indent=2))
