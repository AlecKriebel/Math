#!/usr/bin/env python3
"""Authenticate all packet bytes and replay exact diagnostics without sources."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
PINS={'author':'10a8affedf81c5d559356b842c6d7216f88c1fb143d66dce667f62804b4d013b','audit_a':'c841f12d4ac9a7cb88229dd7477bad1c7d484b8bd6ef08e5c5723dace6686431','audit_b':'4271c2cd63ca94a71ab89bd284947464e6f917ff950c94a02d98e94a1b75d375'}
def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def patched_author(root):
    files={p.name:p.read_bytes() for p in (root/'author').iterdir()}; current=None;old=[];new=[]
    def flush():
        if old:
            before=''.join(old).encode();after=''.join(new).encode()
            require(files[current].count(before)==1,'Patch context not unique')
            files[current]=files[current].replace(before,after,1);old.clear();new.clear()
    for line in (root/'audit_a/CITATION_REFINEMENT.patch').read_text().splitlines(keepends=True):
        if line.startswith('--- a/'):flush();current=line[6:].strip()
        elif line.startswith('+++ b/') or line.startswith('@@ '):pass
        elif line.startswith('-'):old.append(line[1:])
        elif line.startswith('+'):new.append(line[1:])
        elif line.startswith(' '):old.append(line[1:]);new.append(line[1:])
        else:raise RuntimeError('Unsupported patch line')
    flush()
    files['MANIFEST.sha256']=''.join(sha(v)+'  '+k+'\n' for k,v in sorted(files.items()) if k!='MANIFEST.sha256').encode()
    return files

def validate(root,expected):
    root=Path(root).resolve(); mf=root/'PUBLIC_MANIFEST.json'
    require(not mf.is_symlink() and mf.is_file(),'Invalid public manifest path')
    raw=mf.read_bytes();require(len(expected)==64 and sha(raw)==expected,'External manifest anchor mismatch')
    m=json.loads(raw);require(m['problem_id']==30001405 and m['status']=='statement_needs_correction' and m['turns']=='1/5','Wrong disposition')
    records=m['files'];require(isinstance(records,dict) and records,'Empty manifest');dirs=set()
    for name in records:
        q=PurePosixPath(name);require(not q.is_absolute() and q.as_posix()==name and all(s not in ('','.','..') for s in q.parts),'Unsafe path')
        for parent in q.parents:
            if parent.as_posix()!='.':dirs.add(parent.as_posix())
    actual_files=set();actual_dirs=set()
    for p in root.rglob('*'):
        require(not p.is_symlink(),'Symlinks forbidden');name=p.relative_to(root).as_posix()
        if p.is_file():actual_files.add(name)
        elif p.is_dir():actual_dirs.add(name)
        else:raise RuntimeError('Nonregular path')
    require(actual_files==set(records)|{'PUBLIC_MANIFEST.json'},'File inventory mismatch')
    require(actual_dirs==dirs,'Directory inventory mismatch')
    for name,r in records.items():
        b=(root/name).read_bytes();require(len(b)==r['bytes'] and sha(b)==r['sha256'],'Byte mismatch: '+name)
    for folder,pin in PINS.items():
        raw=(root/folder/'MANIFEST.sha256').read_bytes();require(sha(raw)==pin,'Frozen acceptance anchor mismatch')
        entries={}
        for line in raw.decode().splitlines():
            h,name=line.split('  ',1);require(name not in entries,'Duplicate frozen entry');entries[name]=h
        require(set(p.name for p in (root/folder).iterdir())==set(entries)|{'MANIFEST.sha256'},'Frozen inventory mismatch')
        for name,h in entries.items():require(sha((root/folder/name).read_bytes())==h,'Frozen file mismatch')
    correct=patched_author(root);require(set(p.name for p in (root/'corrected_author').iterdir())==set(correct),'Corrected inventory mismatch')
    for name,b in correct.items():require((root/'corrected_author'/name).read_bytes()==b,'Unapproved corrected-copy change: '+name)
    status=json.loads((root/'PUBLICATION_STATUS.json').read_bytes())
    require(status['status']=='statement_needs_correction' and status['turns']=='1/5' and status['frozen_files_preserved']==24,'Status mismatch')
    require(sha(correct['MANIFEST.sha256'])==status['corrected_manifest_sha256'],'Corrected manifest mismatch')
    return m

def replay(root,expected):
    root=Path(root).resolve();m=validate(root,expected)
    import sympy
    require(sympy.__version__=='1.14.0','Use requirements.txt dependency version')
    flags=['-I','-B']+(['-O'] if sys.flags.optimize else []);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'; modes={}
    with tempfile.TemporaryDirectory(prefix='definable-quotient-replay-') as temp:
        r=Path(temp)/'packet';shutil.copytree(root,r)
        def run(relative,*args):
            p=subprocess.run([sys.executable,*flags,str(r/'hardened_runner.py'),str(r/relative),*map(str,args)],cwd=temp,env=env,capture_output=True,timeout=180)
            require(p.returncode==0,'Replay failed: '+relative+'\n'+p.stderr.decode(errors='replace'))
            marker=[json.loads(x.split('=',1)[1]) for x in p.stderr.decode().splitlines() if x.startswith('REPLAY_MODE=')]
            require(len(marker)==1 and marker[0]['optimize']==sys.flags.optimize,'Direct child optimization mode mismatch')
            modes[relative]=marker[0]
            return p.stdout
        author=run('author/verify.py');require(author==(root/'author/CHECK_RESULTS.json').read_bytes(),'Author exact output mismatch')
        require(json.loads(author)['check_count']==20 and json.loads(author)['all_passed'] is True,'Author check count/outcome')
        corrected=run('corrected_author/verify.py');require(corrected==author,'Corrected copy changes diagnostic result')
        audit_b=run('audit_b/independent_checks.py');require(audit_b==(root/'audit_b/CHECK_RESULTS.json').read_bytes(),'Audit B exact output mismatch')
        require(json.loads(audit_b)['check_count']==30 and json.loads(audit_b)['all_passed'] is True,'Audit B count/outcome')
        audit_a=json.loads(run('audit_a/audit_checks.py',r/'author'));saved_a=json.loads((root/'audit_a/AUDIT_CHECK_RESULTS.json').read_bytes())
        skipped=['corpus_byte_verification','corpus_match_count','research_exact_code_key_present','research_exact_numeric_key_present']
        for key in skipped:require(audit_a[key] is None,'Unexpected source-free dataset result')
        require({k:v for k,v in audit_a.items() if k not in skipped}=={k:v for k,v in saved_a.items() if k not in skipped},'Audit A diagnostic mismatch')
        require(len(audit_a['negative_controls'])==5 and all(c['rejected'] is True for c in audit_a['negative_controls']),'Audit A mutation controls')
        require(modes['audit_a/audit_checks.py']['nested_child_modes']==[sys.flags.optimize]*5,'Audit A nested child mode coverage')
        validate(r,expected)
    validate(root,expected)
    return {'status':'PASS','problem_id':30001405,'manifest_sha256':expected,'packet_files':len(m['files'])+1,'frozen_files_preserved':24,'author_checks':20,'author_output_byte_identical':True,'audit_b_checks':30,'audit_b_output_byte_identical':True,'audit_b_rational_witnesses':75,'audit_a_negative_controls':5,'dataset_rechecks_omitted':skipped,'source_retrieval_or_inspection_performed':False,'formal_proof_checker_run':False,'actual_child_modes':modes,'optimized':bool(sys.flags.optimize),'dependency':{'sympy':sympy.__version__},'scope':'Exact symbolic/finite-chain diagnostics, finite witnesses and byte integrity only; written mathematics and source interpretation are not formalized.'}
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--expected-manifest',required=True);ap.add_argument('--check-only',action='store_true');a=ap.parse_args();root=Path(__file__).resolve().parent
    if a.check_only:print(json.dumps({'status':'PASS_INTEGRITY','files':len(validate(root,a.expected_manifest)['files'])+1}))
    else:print(json.dumps(replay(root,a.expected_manifest),indent=2,sort_keys=True))
