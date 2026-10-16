#!/usr/bin/env python3
"""Verify fresh priority packet custody and reproduce its exact finite controls.

All writes are new ROOT evidence; no public, Git, shared-control or family write.
"""
import datetime, gzip, hashlib, json, os, pathlib, subprocess, sys
A=pathlib.Path(__file__).resolve().parent
F=A/'priority_adversary_03'; O=A/'root_priority_adversary_03_reproduction'
O.mkdir(exist_ok=False)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def check(b,s):
    if not b:raise RuntimeError(s)
def read(p):return json.loads(p.read_text())
def pin(p):
    check(p.is_file() and not p.is_symlink(),str(p));b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':sha(b),'mode':p.stat().st_mode & 0o777}
def write(p,o):p.write_text(json.dumps(o,indent=2)+'\n');p.chmod(0o444)
source=pin(pathlib.Path(__file__).resolve())
write(O/'request.json',{'UTC':now(),'ROOT_actual_PID':os.getpid(),'argv':sys.orig_argv,'source':source})
(O/'ROOT_source.py.gz').write_bytes(gzip.compress(pathlib.Path(__file__).read_bytes(),mtime=0))
check(pin(F/'REPORT.md')['sha256']=='56626722bf915a8b77866343fe07f155384998cc52e7d3c9022032e1da268257','announced report')
manifest=read(F/'MANIFEST.json');seen=set()
for x in manifest:
    rel=pathlib.Path(x['path']);check(not rel.is_absolute() and '..' not in rel.parts and str(rel) not in seen,'manifest path')
    seen.add(str(rel));r=pin(F/rel);check(r['sha256']==x['sha256'] and r['bytes']==x['bytes'],'manifest body')
captures=[];sources=0
for d in sorted((F/'captures').iterdir()):
    q=read(d/'request.json');s=read(d/'started.json');e=read(d/'execution.json')
    check(s['pid']==e['pid'] and e['pid']>0 and s['start_utc']==e['start_utc'],'PID/start')
    check(datetime.datetime.fromisoformat(e['end_utc'])>=datetime.datetime.fromisoformat(e['start_utc']),'time')
    b=gzip.decompress((d/'recorder_source.py.gz').read_bytes());check(sha(b)==q['recorder_sha256'],'recorder')
    for n in ['stdout','stderr']:
        b=gzip.decompress((d/(n+'.gz')).read_bytes());check(sha(b)==e[n+'_sha256'] and len(b)==e[n+'_bytes'],'full stream')
    for x in q['sources']:
        b=gzip.decompress((d/x['archive']).read_bytes());check(len(b)==x['bytes'] and sha(b)==x['sha256'],'archived actual source');sources+=1
    captures.append({'label':d.name,'argv':q['argv'],'actual_PID':e['pid'],'start_UTC':e['start_utc'],'end_UTC':e['end_utc'],'exit':e['exit_code']})
for p in (F/'sources').glob('*.receipt.json'):
    r=read(p)
    if 'failure' in r:continue
    b=(F/'sources'/p.name.removesuffix('.receipt.json')).read_bytes()
    check(sha(b)==r['sha256'] and len(b)==r['bytes'],'fresh HTTP body receipt')
check(len(captures)==21 and sources==44,'packet cardinality')
prior=A/'priority_algorithm_01'/'sources'
check((F/'sources'/'qpa_fix.gi').read_bytes()==(F/'sources'/'qpa_v136.gi').read_bytes()==(prior/'qpa-2024-combinatorialmap.gi').read_bytes(),'independent June2024/release bodies')
check((F/'sources'/'applet_2025.gz').read_bytes()==(prior/'applet-2025-main.js').read_bytes(),'independent raw historical body')
rows=read(F/'APPLET_RESULTS_v03.json');check([len(x['results']) for x in rows]==[19,30],'replay rows')
check(not any('error' in r for x in rows for r in x['results']),'replay caught errors')

def run(label,argv,inputs):
    d=O/label;d.mkdir();input_pins=[pin(p) for p in inputs]
    write(d/'request.json',{'UTC':now(),'argv':argv,'cwd':'/Users/alec/Documents/Math','recorder_PID':os.getpid(),'input_pins':input_pins})
    for i,p in enumerate(inputs):(d/('input_%02d.gz'%i)).write_bytes(gzip.compress(p.read_bytes(),mtime=0))
    start=now()
    with (d/'stdout.raw').open('xb') as out,(d/'stderr.raw').open('xb') as err:
        child=subprocess.Popen(argv,cwd='/Users/alec/Documents/Math',stdout=out,stderr=err,start_new_session=True)
        write(d/'started.json',{'actual_PID':child.pid,'start_UTC':start})
        try:code=child.wait(timeout=55)
        except BaseException:
            import signal
            os.killpg(child.pid,signal.SIGKILL);child.wait();raise
    e={'actual_PID':child.pid,'argv':argv,'start_UTC':start,'end_UTC':now(),'exit_code':code}
    for n in ['stdout','stderr']:
        p=d/(n+'.raw');b=p.read_bytes();z=gzip.compress(b,mtime=0);(d/(n+'.gz')).write_bytes(z)
        e[n]={'bytes':len(b),'sha256':sha(b),'gzip_bytes':len(z),'gzip_sha256':sha(z)}
        p.chmod(0o444);(d/(n+'.gz')).chmod(0o444)
    write(d/'execution.json',e);check(code==0,'native replay failure '+label)
    check(input_pins==[pin(p) for p in inputs],'input drift '+label)
    return e

# Exact source copies change only their output directory through __file__/__dirname.
P=O/'controls';P.mkdir();(P/'sources').mkdir()
for name in ['check_primary_arf.js','qpa_occurrence_control.py']:
    p=P/name;p.write_bytes((F/name).read_bytes());p.chmod(0o444)
p=P/'sources'/'applet_2025.gz';p.write_bytes((F/'sources'/'applet_2025.gz').read_bytes());p.chmod(0o444)
arp=run('exact_arf_replay',['/opt/homebrew/bin/node',str(P/'check_primary_arf.js')],[P/'check_primary_arf.js',p,prior/'string-main.js'])
check(read(P/'ARF_CONTROLS.json')==read(F/'ARF_CONTROLS.json'),'whole Arf output')
check(sum(x['gauss_sum_checks'] for x in read(P/'ARF_CONTROLS.json'))==896,'896 checks')
occ=run('exact_occurrence_replay',['/opt/homebrew/bin/python3','-E','-B',str(P/'qpa_occurrence_control.py')],[P/'qpa_occurrence_control.py'])
check(read(P/'QPA_OCCURRENCE_RESULTS.json')==read(F/'QPA_OCCURRENCE_RESULTS.json'),'whole occurrence output')
check(pin(F/'check_primary_arf.js')['sha256']==pin(P/'check_primary_arf.js')['sha256'] and pin(F/'qpa_occurrence_control.py')['sha256']==pin(P/'qpa_occurrence_control.py')['sha256'],'unchanged source copies')
r={'UTC':now(),'actual_ROOT_PID':os.getpid(),'source':source,'status':'PASS_FRESH_PRIORITY_ADVERSARY_CUSTODY_AND_EXACT_CONTROL_REPRODUCTION',
 'manifest':pin(F/'MANIFEST.json'),'manifest_entries':len(manifest),'report':pin(F/'REPORT.md'),'captures':captures,'archived_actual_sources':sources,
 'independent_prior_body_matches':True,'historical_and_current_finite_replay_rows':[19,30],'ROOT_actual_replays':[arp,occ],
 'ROOT_Arf_Gauss_sum_checks':896,'QPA_control_scope':'Exact finite permutation translation; no GAP runtime or complete QPA implementation certification.',
 'limits':['896 Arf checks cover dimension4 only.', 'Full all-input numerical software correctness not certified.', 'Specific certificate/correction novelty remains unknown.', 'ROOT disposition adjudication remains separate.'],
 'paper_or_merge_or_publication_cleared':False,'persistent_goal_complete':False}
write(A/'ROOT_FRESH_PRIORITY_ADVERSARY_REPRODUCTION.json',r)
print(json.dumps({'status':r['status'],'manifest_entries':len(manifest),'native_captures':len(captures),'Arf_checks':896,'replay_PIDs':[arp['actual_PID'],occ['actual_PID']]}))
