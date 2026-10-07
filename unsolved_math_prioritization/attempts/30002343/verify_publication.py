"""Externally anchored source-free replay. Authenticate this file before execution."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECTED: use python -I -S -B [-O|-OO] verify_publication.py PIN PACKET')
from pathlib import Path, PurePosixPath
import hashlib, json, os, stat, subprocess, tempfile
FILES = set(['ACCEPTANCE.md', 'README.md', 'RESEARCH_LOG.md', 'independent_audit/ACCEPTANCE_REPORT.json', 'independent_audit/AUDIT_MANIFEST.json', 'independent_audit/INDEPENDENT_AUDIT.md', 'independent_audit/INDEPENDENT_CHECK_RESULTS.json', 'independent_audit/independent_check.py', 'mutation_tests.py', 'public/AUTHOR_CHECK.md', 'public/CHECK_RESULTS.json', 'public/FROZEN_MANIFEST.json', 'public/PROOF.md', 'public/README.md', 'public/SOURCE_AUDIT.md', 'public/SOURCE_METADATA.json', 'public/TURN_LEDGER.md', 'public/check_math.py', 'verify_publication.py'])
DIRS = {'public', 'independent_audit'}
PINS = {'public/FROZEN_MANIFEST.json':'fe1428032c46c505cfa5e60dc7dd7a13b64535c2b90da8c00c83c85d95db53d8',
        'independent_audit/AUDIT_MANIFEST.json':'b3a863367d03b38370e7f119fee86bb392e937b5d7cefec82f0a891ae646ca9c'}
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
    require(set(m)=={'schema','problem_id','files'} and m['schema']=='stable-log-publication-v1' and m['problem_id']==30002343,'Wrong publication schema/target')
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
            rel=row['path'];require(valid_path(rel) and '/' not in rel and rel not in seen,'Invalid frozen path');seen.add(rel)
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

def verify(root, pin):
    original=integrity(root,pin)
    with tempfile.TemporaryDirectory(prefix='stable-log-replay-') as temp:
        copy=Path(temp)/'packet';copy.mkdir()
        for name,raw in original.items():
            p=copy/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        integrity(copy,pin)
        opt=sys.flags.optimize
        author,aprobe=child(copy,'public/check_math.py',[],opt)
        require(author==parse(original['public/CHECK_RESULTS.json']),'Author replay differs')
        check,cprobe=child(copy,'public/check_math.py',['--verify-manifest'],opt)
        require(check=={'status':'PASS','verified_files':8},'Author manifest replay differs')
        audit,iprobe=child(copy,'independent_audit/independent_check.py',['--packet',str(copy/'public')],opt)
        historical=parse(original['independent_audit/INDEPENDENT_CHECK_RESULTS.json']);historical_sources=historical.pop('source_pdf_checks')
        require(audit.pop('source_pdf_checks')==[],'Unexpected source access')
        require(audit==historical,'Independent source-free replay differs')
        metadata=parse(original['public/SOURCE_METADATA.json'])['sources']
        expected_sources=[{k:s[k] for k in ['id','title','retrieval_url','citation_url','bytes','sha256']} | {'verification':'PASS','verification_scope':'Supplied local PDF bytes; not an independent network re-download.'} for s in metadata]
        require(historical_sources==expected_sources and len(historical_sources)==6,'Historical metadata mismatch')
        acceptance=parse(original['independent_audit/ACCEPTANCE_REPORT.json'])
        require(acceptance['verdict']=='ACCEPTED_PARTIAL_NO_REQUIRED_CORRECTIONS' and acceptance['required_correction_patch'] is None and acceptance['original_changed'] is False and acceptance['mathematical_approaches']==5 and acceptance['universal_degree_five_status']=='UNRESOLVED_BY_THIS_PACKET','Acceptance scope mismatch')
        require(integrity(copy,pin)==original,'Replay changed staged packet')
    require(integrity(root,pin)==original,'Replay changed original packet')
    return {'status':'pass','problem_id':30002343,'queue_status':'unsolved','turns':'5/5','python_optimization':opt,'verified_file_count':len(original),'manifest_sha256':pin,'frozen_manifests':PINS,'child_runtimes':{'author':aprobe,'author_manifest':cprobe,'independent':iprobe},'frozen_child_assertions_active':opt==0,'independent_legacy_nested_author_runtime':'Original nested commands omit optimization and isolation flags; no separate nested runtime probe; PYTHON environment variables removed.','author_output_matches':True,'independent_output_matches_except_excluded_pdf_checks':True,'historical_source_metadata_entries_checked':6,'source_pdf_bytes_rechecked':False,'unchanged':True,'limits':'Finite regression and byte checks only; geometric dependencies and novelty are not machine-proved. Optimized runs disable frozen assert statements. Explicit publication guards remain active. Trusted interpreter/OS assumed.'}
if __name__=='__main__':
    try:
        require(len(sys.argv)==3,'Expected external manifest pin and packet directory')
        print(json.dumps(verify(Path(sys.argv[2]).absolute(),sys.argv[1]),indent=2,sort_keys=True))
    except Exception as error:
        print('REJECTED: '+str(error),file=sys.stderr);raise SystemExit(1)
