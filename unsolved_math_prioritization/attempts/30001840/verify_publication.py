"""Externally pinned source-free inventory, exact patch and finite replay checks."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECTED: use python -I -S -B [ -O | -OO ] verify_publication.py PIN PACKET')
from pathlib import Path,PurePosixPath
import hashlib,json,os,stat,subprocess,tempfile,re
# Frozen inventory and pins are inserted once during publication preparation.
FILES=set(['ACCEPTANCE.md', 'PUBLICATION_SOURCE_CHECK.json', 'README.md', 'RESEARCH_LOG.md', 'audit_independent/AUDIT.md', 'audit_independent/AUDIT_MANIFEST.json', 'audit_independent/INDEPENDENT_CONTROLS.json', 'audit_independent/MUTATION_RESULTS.json', 'audit_independent/PATCH_VERIFICATION.json', 'audit_independent/PROOF_CORRECTED.md', 'audit_independent/PROPOSED.patch', 'audit_independent/PROSPECTIVE_BRIDGE.md', 'audit_independent/SOURCE_VERIFICATION.json', 'audit_independent/checks_corrected.py', 'audit_independent/corrected_public/DATASET_VERIFICATION.json', 'audit_independent/corrected_public/FINITE_CHECKS.json', 'audit_independent/corrected_public/MANIFEST.json', 'audit_independent/corrected_public/PROOF.md', 'audit_independent/corrected_public/README.md', 'audit_independent/corrected_public/SELF_AUDIT.md', 'audit_independent/corrected_public/SOURCE_AUDIT.md', 'audit_independent/corrected_public/SOURCE_MANIFEST.json', 'audit_independent/corrected_public/TURN_1.md', 'audit_independent/corrected_public/TURN_2.md', 'audit_independent/corrected_public/TURN_3.md', 'audit_independent/corrected_public/TURN_4.md', 'audit_independent/corrected_public/TURN_5.md', 'audit_independent/corrected_public/TURN_LEDGER.json', 'audit_independent/corrected_public/checks.py', 'audit_independent/independent_checks.py', 'audit_independent/independent_optimized.json', 'audit_independent/mutation_checks.py', 'audit_independent/original_controls.json', 'mutation_tests.py', 'public/DATASET_VERIFICATION.json', 'public/FINITE_CHECKS.json', 'public/MANIFEST.json', 'public/PROOF.md', 'public/README.md', 'public/SELF_AUDIT.md', 'public/SOURCE_AUDIT.md', 'public/SOURCE_MANIFEST.json', 'public/TURN_1.md', 'public/TURN_2.md', 'public/TURN_3.md', 'public/TURN_4.md', 'public/TURN_5.md', 'public/TURN_LEDGER.json', 'public/checks.py', 'verify_publication.py'])
DIRS=set(['audit_independent', 'audit_independent/corrected_public', 'public'])
PINS={'public/MANIFEST.json': '2b46f6cf67e9de36ca809237f1281d0fcc0288e03ab03c805a947a4cd5882d09', 'audit_independent/AUDIT_MANIFEST.json': '3da829514e752f70f0d3d0bd3f149afe7d7179ba48c437fd4a431f7963956745', 'audit_independent/corrected_public/MANIFEST.json': 'dc0d9046d4c873f6fb0d46d97c6dc766d41e4bfa53fe08f0e1cfeb8e0e8436ec'}

def require(ok,message):
    if not ok:raise ValueError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
    result={}
    for k,v in pairs:
        require(k not in result,'Duplicate JSON key');result[k]=v
    return result
def parse(b):return json.loads(b,object_pairs_hook=unique)
def valid_path(name):
    return isinstance(name,str) and name and '\\' not in name and not name.startswith('/') and all(p not in ('','.', '..') for p in name.split('/')) and PurePosixPath(name).as_posix()==name

def apply_patch(original,patch,target):
    source=original.splitlines(keepends=True);lines=patch.splitlines(keepends=True)
    require(lines[:2]==[('--- a/'+target+'\n').encode(),('+++ b/'+target+'\n').encode()],'Unexpected patch target')
    result=[];position=0;i=2;hunks=0
    while i<len(lines):
        match=re.fullmatch(rb'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n',lines[i]);require(match is not None,'Malformed patch hunk')
        start,old_count,new_start,new_count=map(int,match.groups());i+=1;hunks+=1
        require(start-1>=position,'Overlapping patch');result.extend(source[position:start-1]);position=start-1
        require(len(result)==new_start-1,'New patch offset mismatch');old_seen=new_seen=0
        while i<len(lines) and not lines[i].startswith(b'@@ '):
            line=lines[i];i+=1;require(line[:1] in (b' ',b'-',b'+'),'Invalid patch line')
            if line[:1] in (b' ',b'-'):
                require(position<len(source) and source[position]==line[1:],'Patch context mismatch');position+=1;old_seen+=1
            if line[:1] in (b' ',b'+'):result.append(line[1:]);new_seen+=1
        require((old_seen,new_seen)==(old_count,new_count),'Patch line count mismatch')
    require(hunks==(1 if target=='PROOF.md' else 4),'Unexpected correction count')
    result.extend(source[position:]);return b''.join(result)

def integrity(root,pin):
    require(isinstance(pin,str) and len(pin)==64 and all(c in '0123456789abcdef' for c in pin),'Malformed pin')
    require(not root.is_symlink() and root.is_dir(),'Invalid or linked root')
    files=set();dirs=set()
    def walk(directory):
        for entry in os.scandir(directory):
            p=Path(entry.path);rel=p.relative_to(root).as_posix();mode=entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                require(rel in DIRS,'Unexpected directory: '+rel);dirs.add(rel);walk(p)
            else:
                require(stat.S_ISREG(mode),'Linked or special entry: '+rel);files.add(rel)
    walk(root);require(files==FILES|{'PUBLIC_MANIFEST.json'} and dirs==DIRS,'Closed inventory mismatch')
    raw=(root/'PUBLIC_MANIFEST.json').read_bytes();require(digest(raw)==pin,'Manifest pin mismatch');manifest=parse(raw)
    require(set(manifest)=={'schema','problem_id','files'} and manifest['schema']=='genus-two-publication-v1' and manifest['problem_id']==30001840,'Manifest schema/target mismatch')
    rows=manifest['files'];require(isinstance(rows,list) and len(rows)==len(FILES),'Invalid manifest size');names=[];snapshot={}
    for row in rows:
        require(isinstance(row,dict) and set(row)=={'path','bytes','sha256'},'Invalid entry');name=row['path']
        require(valid_path(name) and name in FILES and name not in names,'Invalid/duplicate path');names.append(name)
        b=(root/name).read_bytes();require(type(row['bytes']) is int and len(b)==row['bytes'] and digest(b)==row['sha256'],'Payload mismatch: '+name);snapshot[name]=b
    require(set(names)==FILES,'Manifest allowlist mismatch')
    for name,value in PINS.items():require(digest(snapshot[name])==value,'Frozen pin mismatch: '+name)
    for name in PINS:
        parent=Path(name).parent.as_posix();child=parse(snapshot[name]);entries=child['files']
        expected={n[len(parent)+1:] for n in FILES if n.startswith(parent+'/')} - {Path(name).name}
        require(set(entries)==expected,'Nested inventory mismatch: '+name)
        for rel,row in entries.items():
            b=snapshot[parent+'/'+rel];require(len(b)==row['bytes'] and digest(b)==row['sha256'],'Nested payload mismatch: '+rel)
    patch=snapshot['audit_independent/PROPOSED.patch'];marker=b'--- a/checks.py\n'
    require(patch.count(marker)==1,'Patch boundary mismatch');first,second=patch.split(marker)
    for target,part,expanded in [('PROOF.md',first,'PROOF_CORRECTED.md'),('checks.py',marker+second,'checks_corrected.py')]:
        corrected=apply_patch(snapshot['public/'+target],part,target)
        require(corrected==snapshot['audit_independent/'+expanded]==snapshot['audit_independent/corrected_public/'+target],'Patch reconstruction mismatch: '+target)
    source=parse(snapshot['public/SOURCE_MANIFEST.json'])['sources'];audited=parse(snapshot['audit_independent/SOURCE_VERIFICATION.json'])['sources'];publication=parse(snapshot['PUBLICATION_SOURCE_CHECK.json'])['sources']
    require(len(source)==len(audited)==len(publication)==8,'Source record count')
    require(len({row['source_key'] for row in source})==8,'Duplicate source key')
    for a,b,c in zip(source,audited,publication):
        require(a['source_key']==b['source_key']==c['source_key'] and a['pdf']['sha256']==b['auditor_sha256']==c['sha256'] and a['pdf']['bytes']==b['auditor_bytes']==c['bytes'] and b['hash_and_size_match'] is True and c['matches_frozen_public_metadata'] is True,'Source metadata binding')
    return snapshot

def replay(snapshot):
    opt=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    driver='import json,runpy,sys; print(json.dumps({"optimization":sys.flags.optimize,"debug":__debug__}),file=sys.stderr); sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name="__main__")'
    env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    with tempfile.TemporaryDirectory(prefix='genus-two-publication-') as td:
        root=Path(td)
        for name,b in snapshot.items():
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        cases=[('original_output',['public/checks.py'],'public/FINITE_CHECKS.json'),('corrected_validation',['audit_independent/corrected_public/checks.py'],'public/FINITE_CHECKS.json'),('independent_validation',['audit_independent/independent_checks.py','--split'],'audit_independent/INDEPENDENT_CONTROLS.json'),('mathematical_mutations',['audit_independent/mutation_checks.py'],'audit_independent/MUTATION_RESULTS.json')]
        results={}
        for label,argv,expected in cases:
            argv[0]=str(root/argv[0]);command=[sys.executable,'-I','-S','-B',*opt,'-c',driver,*argv]
            process=subprocess.run(command,cwd=root,capture_output=True,env=env,timeout=240)
            require(process.returncode==0,label+' replay failed: '+process.stderr.decode(errors='replace'))
            require(parse(process.stderr)=={'optimization':sys.flags.optimize,'debug':sys.flags.optimize==0},'Actual child flags mismatch')
            require(process.stdout==snapshot[expected],label+' full receipt byte mismatch')
            results[label]={'status':'pass','child_optimization':sys.flags.optimize,'stdout_sha256':digest(process.stdout)}
            if label=='original_output':results[label]['acceptance_checks_active']=sys.flags.optimize==0
            if label=='mathematical_mutations':
                receipt=parse(process.stdout)
                require(receipt['summary']=={'mutants':9,'original_regular_rejected':9,'original_optimized_rejected':0,'corrected_regular_rejected':9,'corrected_optimized_rejected':9},'Mutation result mismatch')
                results[label]['nested_child_optimization_levels']=[0,1]
        return results

def main():
    require(len(sys.argv)==3,'Expected external manifest pin and packet path')
    pin=sys.argv[1];root=Path(os.path.abspath(sys.argv[2]));snapshot=integrity(root,pin)
    result={'schema':'genus-two-publication-replay-v1','problem_id':30001840,'status':'pass','python_optimization':sys.flags.optimize,'manifest_sha256':pin,'verified_payload_files':len(snapshot),'patch_replay_matches':True,'source_metadata_bound':True,'replays':replay(snapshot),'limits':'Integrity and finite controls, not a generic-image proof. Optimized original output does not validate assertions. The mutation harness tests genuine normal/-O children; source PDFs and datasets are excluded and not rehashed by portable replay.'}
    require(integrity(root,pin)==snapshot,'Input changed during replay');print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as exc:print('REJECTED: '+str(exc),file=sys.stderr);sys.exit(1)
