#!/usr/bin/env python3
"""ROOT read-only family custody checks and a separately captured finite replay.

No Git, shared-control, PR or publication mutation. Writes only new ROOT evidence.
This verifies retained bodies and a finite calculation, not universal software.
"""
import ast, base64, datetime, gzip, hashlib, json, os, pathlib, subprocess, sys

A = pathlib.Path(__file__).resolve().parent
OUT = A / 'root_priority_families_01_02_custody_v02'
OUT.mkdir(exist_ok=False)
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def check(ok, msg):
    if not ok: raise RuntimeError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return json.loads(p.read_text())
def pin(p):
    check(p.is_file() and not p.is_symlink(), str(p))
    b=p.read_bytes()
    return {'path':str(p), 'bytes':len(b), 'sha256':sha(b), 'mode':p.stat().st_mode & 0o777}
def write(p, o):
    p.write_text(json.dumps(o,indent=2)+'\n'); p.chmod(0o444)
source=pin(pathlib.Path(__file__).resolve())
write(OUT/'request.json',{'UTC':now(),'actual_ROOT_PID':os.getpid(), 'source':source,
      'argv':sys.orig_argv, 'cwd':os.getcwd(), 'qualification':'Original tool caller is not separately recaptured here.'})
(OUT/'ROOT_source.py.gz').write_bytes(gzip.compress(pathlib.Path(__file__).read_bytes(),mtime=0))
families=[]
for name, manifest_name in [('priority_algorithm_01','EVIDENCE_MANIFEST.json'),('priority_effectivity_02','MANIFEST.json')]:
    root=A/name; manifest=read(root/manifest_name); entries=manifest['files']
    seen=set(); total=0
    for e in entries:
        rel=e.get('relative_path',e['path']); p=root/rel
        check(not pathlib.Path(rel).is_absolute() and '..' not in pathlib.Path(rel).parts, 'relative manifest')
        check(rel not in seen,'duplicate manifest');seen.add(rel)
        x=pin(p);check(x['bytes']==e['bytes'] and x['sha256']==e['sha256'],'body '+str(p));total+=x['bytes']
    records=[]; base=root/('native' if name.endswith('01') else 'captures')
    for d in sorted(base.iterdir()):
        check((d/'execution.json').exists(),'unfinished capture '+str(d))
        q=read(d/'request.json');s=read(d/'started.json');e=read(d/'execution.json')
        if name.endswith('01'):
            check(s['pid']==e['pid'] and e['pid']>0,'PID')
            check(q['runner_sha256']==pin(root/'run_native.py')['sha256'],'runner')
            check(datetime.datetime.fromisoformat(q['start_utc'])<=datetime.datetime.fromisoformat(s['start_utc'])<=datetime.datetime.fromisoformat(e['end_utc']),'times')
            for n in ['stdout','stderr']:
                b=(d/(n+'.bin')).read_bytes();check(len(b)==e[n+'_bytes'] and sha(b)==e[n+'_sha256'],'stream')
            records.append({'label':d.name,'actual_PID':e['pid'],'exit':e['exit_code'],'source_pin_qualification':'Runner exact; argument-source pins retrospective as disclosed by family.'})
        else:
            check(e['actual_PID']==s['actual_PID'] and e['actual_PID']>0 and e['argv']==s['argv']==q['argv'],'PID/argv')
            check(e['start_UTC']==s['start_UTC'] and datetime.datetime.fromisoformat(e['end_UTC'])>=datetime.datetime.fromisoformat(e['start_UTC']),'times')
            b=gzip.decompress((d/'capture_source.py.gz').read_bytes())
            check(sha(b)==q['capture_source']['sha256']==e['source']['sha256'],'archived runner')
            for n in ['stdout','stderr']:
                packed=(d/(n+'.gz')).read_bytes();b=gzip.decompress(packed)
                check(len(b)==e[n+'_uncompressed_bytes'] and sha(b)==e[n+'_sha256'],'stream')
                check(len(packed)==e[n+'_gzip']['bytes'] and sha(packed)==e[n+'_gzip']['sha256'],'packed stream')
            records.append({'label':d.name,'actual_PID':e['actual_PID'],'exit':e['exit_code'],'argument_sources_contemporaneous':'argument_files_at_start' in q})
    families.append({'family':name,'manifest':pin(root/manifest_name),'manifest_entries_checked':len(entries),'bound_bytes':total,'complete_native_captures':records,'report':pin(root/'REPORT.md')})

alg=A/'priority_algorithm_01'; eff=A/'priority_effectivity_02'; sources=alg/'sources'
check(pin(eff/'REPORT.md')['sha256']=='ba4eb37fa44e09d1ba08c7ec6de188bc4a3471e68d237ca06733557dfd072392','announced report')
check(pin(A/'CURRENT_CORRECTED_PROOF_v02.md')['sha256']=='d92a870709f5ce62440fa8a83313dd13790773f247e01cfb63c43c5ae8ea272a','proof')
raw=(sources/'applet-2025-main.js').read_bytes(); decoded=gzip.decompress(raw)
check(decoded==(sources/'applet-2025-main.decoded.js').read_bytes(),'archive decode')
check(sha(decoded)=='99a8209e6f54b3f24ad68b463e0a5ae83fc4487af8481b76a38271dff83644ba','historical body')
cdx=read(sources/'applet-cdx.json'); row=next(r for r in cdx[1:] if r[1]=='20250321111807')
check(base64.b32encode(hashlib.sha1(raw).digest()).decode()==row[5],'CDX raw payload digest')
headers=(sources/'applet-2025.headers').read_text()
check('memento-datetime: Fri, 21 Mar 2025 11:18:07 GMT' in headers,'Memento')
index=read(alg/'APPLET_METHOD_INDEX.json')
for file, o in index.items():
    body=(sources/file).read_bytes();check(sha(body)==o['sha256'],'method parent')
    for m in o['methods']:
        part=body[m['UTF8_start_byte']:m['UTF8_end_byte_exclusive']]
        check(sha(part)==m['method_sha256'] and part.startswith((m['method']+':function').encode()),'method body')
old=(sources/'qpa-2024-combinatorialmap.gi').read_bytes()
blob=hashlib.sha1(b'blob '+str(len(old)).encode()+b'\0'+old).hexdigest()
check(blob=='f881ef7ad6eecfce1ad2191ce47f0c6e952c70ea','2024 Git blob')
fix=read(sources/'qpa-fix-commit.json')
check(fix['sha']=='87aee76da6cec5e29ceea4c9c8fa6bfd64d9c0b7' and fix['commit']['committer']['date']=='2024-06-18T14:14:45Z','commit metadata')
check(any(x['filename']=='lib/combinatorialmap.gi' and x['sha']==blob for x in fix['files']),'commit body pointer')
release=next(x for x in read(sources/'qpa-releases.json') if x['tag_name']=='v1.36')
check(release['published_at']=='2025-05-28T19:03:21Z','release date')
versions=[]
for d in sorted((eff/'version_reads').iterdir()):
    e=read(d/'execution.json'); check(e['actual_PID']>0 and e['exit']==0,'version PID/exit')
    pdf=pathlib.Path(e['argv'][2]); p=pin(pdf)
    check(p['sha256']==e['PDF_sha256'] and p['bytes']==e['PDF_bytes'],'version PDF')
    for n in ['stdout','stderr']:check(sha(gzip.decompress((d/(n+'.gz')).read_bytes()))==e[n+'_sha256'],'version full stream')
    versions.append({'name':d.name,'actual_PID':e['actual_PID'],'PDF':p})
check(len(versions)==8,'version count')

# Run the unchanged finite control source in a separate ROOT-owned directory.
# Trace assertion lines without replacing the mathematical code or its counters.
replay=OUT/'finite_surgery_replay';replay.mkdir()
control=eff/'check_local_surgery.py'; copied=replay/control.name;copied.write_bytes(control.read_bytes());copied.chmod(0o444)
wrapper=replay/'trace_assertions.py'
wrapper.write_text('''import ast,json,pathlib,runpy,sys
p=pathlib.Path(__file__).resolve().parent/'check_local_surgery.py'
lines={n.lineno for n in ast.walk(ast.parse(p.read_text())) if isinstance(n,ast.Assert)}
count=0
def trace(frame,event,arg):
 global count
 if event=='line' and frame.f_code.co_filename==str(p) and frame.f_code.co_name in ('<module>','cycles') and frame.f_lineno in lines: count+=1
 return trace
sys.settrace(trace)
runpy.run_path(str(p),run_name='__main__')
sys.settrace(None)
print(json.dumps({'ROOT_actual_assertion_executions':count}))
if count!=177312: raise RuntimeError('Unexpected assertion count')
''');wrapper.chmod(0o444)
argv=['/opt/homebrew/bin/python3','-E','-B',str(wrapper)]
write(replay/'request.json',{'argv':argv,'cwd':str(replay),'UTC':now(),'recorder_PID':os.getpid(),'exact_control_source':pin(copied),'wrapper':pin(wrapper)})
start=now()
with (replay/'stdout.raw').open('xb') as out,(replay/'stderr.raw').open('xb') as err:
    proc=subprocess.Popen(argv,cwd=replay,stdout=out,stderr=err,start_new_session=True)
    write(replay/'started.json',{'actual_PID':proc.pid,'start_UTC':start})
    try: code=proc.wait(timeout=55)
    except BaseException:
        import signal
        os.killpg(proc.pid,signal.SIGKILL);proc.wait();raise
end=now();execution={'argv':argv,'actual_PID':proc.pid,'start_UTC':start,'end_UTC':end,'exit_code':code}
for n in ['stdout','stderr']:
    p=replay/(n+'.raw');b=p.read_bytes();packed=gzip.compress(b,mtime=0)
    (replay/(n+'.gz')).write_bytes(packed)
    execution[n]={'bytes':len(b),'sha256':sha(b),'gzip_bytes':len(packed),'gzip_sha256':sha(packed)}
    p.chmod(0o444);(replay/(n+'.gz')).chmod(0o444)
write(replay/'execution.json',execution);check(code==0,'finite replay failure')
result=read(replay/'LOCAL_SURGERY_RESULTS.json');old_result=read(eff/'LOCAL_SURGERY_RESULTS.json')
for k in ['UTC','actual_PID']: result.pop(k);old_result.pop(k)
check(result==old_result,'finite control full JSON comparison')
check(pin(control)['sha256']==pin(copied)['sha256']==result['source_sha256'],'unchanged replay')
check(b'"ROOT_actual_assertion_executions": 177312' in (replay/'stdout.raw').read_bytes(),'trace count')
final={'UTC':now(),'actual_ROOT_PID':os.getpid(),'source':source,'status':'PASS_RETAINED_TWO_FAMILY_CUSTODY_AND_EXACT_FINITE_REPLAY',
 'family_custody':families,'version_extractions':versions,'historical_archive_CDX_payload_digest_matches':True,
 'historical_applet':pin(sources/'applet-2025-main.decoded.js'),'QPA_2024_blob':blob,'QPA_release':{k:release[k] for k in ['tag_name','published_at','html_url']},
 'finite_replay':execution,'finite_checks':{'counted_predicates':177120,'chord_pairs':176800,'internal_closure_assertions':192,'actual_assertion_executions':177312},
 'limits':['Not universal certification of either public software.', 'Not proof of historical firstness or novelty of the exact certificate route.', 'Some family argument-source pins are retrospective, as disclosed.', 'Fresh priority adversary03 and ROOT disposition adjudication remain outstanding.'],
 'mathematical_acceptance':True,'priority_clearance_for_new_resolution':False,'persistent_goal_complete':False}
write(A/'ROOT_PRIORITY_FAMILIES_01_02_CUSTODY.json',final)
print(json.dumps({'status':final['status'],'family_manifest_counts':[x['manifest_entries_checked'] for x in families], 'native_capture_counts':[len(x['complete_native_captures']) for x in families],'finite_replay_PID':proc.pid,'actual_assertion_executions':177312}))
