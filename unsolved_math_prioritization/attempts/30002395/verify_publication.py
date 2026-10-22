"""Externally anchored source-free replay. Authenticate this file before execution."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECTED: use python -I -S -B [-O|-OO] verify_publication.py PIN PACKET')
from pathlib import Path, PurePosixPath
import hashlib, json, os, stat, subprocess, tempfile
FILES = set(['ACCEPTANCE.md', 'README.md', 'RESEARCH_LOG.md', 'independent_audit/AUDIT.md', 'independent_audit/AUTHOR_CONTROL_REPLAY.json', 'independent_audit/CONTROL_RESULTS.json', 'independent_audit/CORRECTION.patch', 'independent_audit/MANIFEST.json', 'independent_audit/README.md', 'independent_audit/SCOPE_CONTROL_RESULTS.json', 'independent_audit/SOURCE_AUDIT.json', 'independent_audit/VERIFIER_SELF_TEST.json', 'independent_audit/corrected/AUTHOR_AUDIT.md', 'independent_audit/corrected/CONTROL_RESULTS.json', 'independent_audit/corrected/MANIFEST.json', 'independent_audit/corrected/PROOF.md', 'independent_audit/corrected/README.md', 'independent_audit/corrected/SOURCES.json', 'independent_audit/corrected/TURN_1.md', 'independent_audit/corrected/TURN_2.md', 'independent_audit/corrected/TURN_3.md', 'independent_audit/corrected/TURN_4.md', 'independent_audit/corrected/TURN_5.md', 'independent_audit/corrected/TURN_LEDGER.json', 'independent_audit/corrected/check_controls.py', 'independent_audit/corrected/verify_manifest.py', 'independent_audit/independent_controls.py', 'independent_audit/scope_controls.py', 'independent_audit/verify_audit.py', 'mutation_tests.py', 'public/AUTHOR_AUDIT.md', 'public/CONTROL_RESULTS.json', 'public/MANIFEST.json', 'public/PROOF.md', 'public/README.md', 'public/SOURCES.json', 'public/TURN_1.md', 'public/TURN_2.md', 'public/TURN_3.md', 'public/TURN_4.md', 'public/TURN_5.md', 'public/TURN_LEDGER.json', 'public/check_controls.py', 'public/verify_manifest.py', 'verify_publication.py'])
DIRS = {'public', 'independent_audit/corrected', 'independent_audit'}
PINS = {'public/MANIFEST.json': '5d4700cf4699eea9443dbd40b268839f77404cb701bb15976efdb02bb1861c3a', 'independent_audit/MANIFEST.json': '716ef72c20a216cadecbfc411a86c14b97e51a5bca1af6ea609d9cf7db5f2835', 'independent_audit/corrected/MANIFEST.json': '308b67f94f53eb43af689e4e760a3dc8856547619024011b5f9441a5d2733f53'}
def require(ok, message):
    if not ok: raise ValueError(message)
def sha(b): return hashlib.sha256(b).hexdigest()
def unique(pairs):
    d={}
    for k,v in pairs:
        require(k not in d, 'Duplicate JSON key'); d[k]=v
    return d
def parse(raw): return json.loads(raw, object_pairs_hook=unique)
def valid_path(p):
    return isinstance(p,str) and bool(p) and '\\' not in p and not p.startswith('/') and all(x not in ('','.','..') for x in p.split('/')) and PurePosixPath(p).as_posix()==p

def integrity(root, pin):
    require(isinstance(pin,str) and len(pin)==64 and all(x in '0123456789abcdef' for x in pin),'Malformed external pin')
    require(not root.is_symlink() and root.is_dir(),'Invalid or linked packet root')
    files=set();dirs=set()
    def walk(parent):
        for entry in os.scandir(parent):
            p=Path(entry.path);name=p.relative_to(root).as_posix();mode=entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                require(name in DIRS,'Unexpected directory: '+name);dirs.add(name);walk(p)
            else:
                require(stat.S_ISREG(mode),'Linked or special entry: '+name);files.add(name)
    walk(root)
    require(files==FILES|{'PUBLIC_MANIFEST.json'} and dirs==DIRS,'Closed inventory mismatch')
    raw=(root/'PUBLIC_MANIFEST.json').read_bytes();require(sha(raw)==pin,'External manifest anchor mismatch');m=parse(raw)
    require(set(m)=={'schema','problem_id','files'} and m['schema']=='dini-publication-v1' and m['problem_id']==30002395,'Wrong publication schema/target')
    require(isinstance(m['files'],list) and len(m['files'])==len(FILES),'Invalid inventory size')
    snapshot={}
    for row in m['files']:
        require(isinstance(row,dict) and set(row)=={'path','bytes','sha256'},'Invalid inventory entry')
        name=row['path'];require(valid_path(name) and name in FILES and name not in snapshot,'Invalid or duplicate path')
        b=(root/name).read_bytes();require(type(row['bytes']) is int and len(b)==row['bytes'] and sha(b)==row['sha256'],'Payload mismatch: '+name);snapshot[name]=b
    require(set(snapshot)==FILES,'Allowlist mismatch')
    for name,pinned in PINS.items():
        require(sha(snapshot[name])==pinned,'Frozen manifest anchor mismatch: '+name)
        folder=Path(name).parent.as_posix();nested=parse(snapshot[name]);rows=nested['files'];seen=set()
        require(isinstance(rows,list),'Invalid frozen list')
        for row in rows:
            require(isinstance(row,dict) and set(row)=={'path','bytes','sha256'},'Invalid frozen entry')
            rel=row['path'];require(valid_path(rel) and rel not in seen,'Invalid frozen path');seen.add(rel)
            b=snapshot[folder+'/'+rel];require(type(row['bytes']) is int and len(b)==row['bytes'] and sha(b)==row['sha256'],'Frozen payload mismatch: '+folder+'/'+rel)
        expected={n[len(folder)+1:] for n in FILES if n.startswith(folder+'/')} - {Path(name).name}
        require(seen==expected,'Frozen inventory mismatch')
    snapshot['PUBLIC_MANIFEST.json']=raw
    return snapshot

# The probe executes inside the actual child, before runpy executes the frozen file.
PROBE="import sys,json,runpy; print(json.dumps({'optimization':sys.flags.optimize,'isolated':sys.flags.isolated,'no_site':sys.flags.no_site,'no_bytecode':sys.dont_write_bytecode}),file=sys.stderr); p=sys.argv[1]; sys.argv=sys.argv[1:]; runpy.run_path(p,run_name='__main__')"
def child(root, script, args, optimization):
    command=[sys.executable,'-I','-S','-B',*(['-O']*optimization),'-c',PROBE,str(root/script),*args]
    environment={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    result=subprocess.run(command,cwd=root,env=environment,capture_output=True,timeout=300)
    require(result.returncode==0,'Child failed: '+script+' '+result.stderr.decode(errors='replace'))
    probe=parse(result.stderr);require(probe=={'optimization':optimization,'isolated':1,'no_site':1,'no_bytecode':True},'Child runtime flags mismatch')
    return parse(result.stdout),probe

def stable(value):
    if isinstance(value, dict):
        clean={}
        for k,v in value.items():
            if k.endswith('_seconds') or k=='seconds':
                require(type(v) in (int,float) and 0 <= v < float('inf'), 'Invalid measured timing')
            else: clean[k]=stable(v)
        return clean
    if isinstance(value,list):return [stable(v) for v in value]
    return value

def verify(root, pin):
    original=integrity(root,pin)
    probes={}
    with tempfile.TemporaryDirectory(prefix='dini-replay-') as temp:
        copy=Path(temp)/'packet';copy.mkdir()
        for name,raw in original.items():
            p=copy/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        integrity(copy,pin)
        opt=sys.flags.optimize
        jobs=[
            ('author','public/check_controls.py',[], 'public/CONTROL_RESULTS.json'),
            ('corrected_author','independent_audit/corrected/check_controls.py',[], 'independent_audit/corrected/CONTROL_RESULTS.json'),
            ('independent','independent_audit/independent_controls.py',['--frozen',str(copy/'public')], 'independent_audit/CONTROL_RESULTS.json'),
            ('scope','independent_audit/scope_controls.py',[], 'independent_audit/SCOPE_CONTROL_RESULTS.json'),
            ('audit_self_test','independent_audit/verify_audit.py',['--self-test'], 'independent_audit/VERIFIER_SELF_TEST.json')]
        counts={}
        for label,script,args,receipt in jobs:
            result,probes[label]=child(copy,script,args,opt)
            require(stable(result)==stable(parse(original[receipt])),label+' replay differs')
            counts[label]=result.get('total_assertions',result.get('total_checks',result.get('total_tests')))
        for label,script,args,expected in [
            ('author_manifest','public/verify_manifest.py',[],{'status':'PASS','verified_files':13}),
            ('corrected_manifest','independent_audit/corrected/verify_manifest.py',[],{'status':'PASS','verified_files':13}),
            ('audit_manifest','independent_audit/verify_audit.py',['--expected-sha256',PINS['independent_audit/MANIFEST.json']],{'status':'PASS','verified_files':25,'manifest_sha256':PINS['independent_audit/MANIFEST.json'],'external_identity_checked':True})]:
            result,probes[label]=child(copy,script,args,opt)
            require(result==expected,label+' replay differs')
        metadata=parse(original['public/SOURCES.json'])['sources']
        audited=parse(original['independent_audit/SOURCE_AUDIT.json'])['sources']
        require(len(metadata)==len(audited)==4,'Source metadata count')
        for author,audit in zip(metadata,audited):
            for key in ('key','title','bytes','sha256','pdf_pages'):
                require(author[key]==audit[key],'Source metadata mismatch: '+key)
            require(author['url']==audit['public_pdf_url'] and audit['author_metadata_match'] is True and audit['fresh_pdf_download_claim'] is False,'Source inspection scope mismatch')
        require(sha(original['independent_audit/corrected/PROOF.md'])=='282362111e1927a335e2d17943e8e85e4823a30ec40292ac352838664ea708ee','Corrected proof identity')
        require(sha(original['independent_audit/CORRECTION.patch'])=='4f240a4b7e8894135f6b776a63381415b7c1a3940d8faa7030dcefe0174ff007','Correction identity')
        require(integrity(copy,pin)==original,'Replay changed staged packet')
    require(integrity(root,pin)==original,'Replay changed original packet')
    return {'status':'pass','problem_id':30002395,'queue_status':'unsolved','turns':'5/5','python_optimization':opt,'verified_file_count':len(original),'manifest_sha256':pin,'frozen_manifests':PINS,'child_runtimes':probes,'replay_counts':counts,'frozen_child_assertions_active':opt==0,'explicit_mathematical_guards_active':True,'actual_two_file_patch_replayed':True,'historical_source_metadata_entries_checked':4,'source_pdf_bytes_rechecked':False,'unchanged':True,'limits':'Finite regression and byte checks only; infinite claims, external realization theorem and novelty are not machine-proved. Optimized runs disable the frozen author manifest assert statements. Explicit publication and mathematical guards remain active. Trusted interpreter, patch utility and OS assumed.'}
if __name__=='__main__':
    try:
        require(len(sys.argv)==3,'Expected external manifest pin and packet directory')
        print(json.dumps(verify(Path(sys.argv[2]).absolute(),sys.argv[1]),indent=2,sort_keys=True))
    except Exception as error:
        print('REJECTED: '+str(error),file=sys.stderr);raise SystemExit(1)
