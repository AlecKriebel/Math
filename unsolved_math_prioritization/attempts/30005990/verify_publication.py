#!/usr/bin/env python3
"""Source-free replay with an external publication-manifest anchor."""
import argparse,hashlib,json,re,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
AUTHOR='0fd5ecb3dac1b270540014c9a3b7de0c043cb0b63ba5ec3930eb5b278f15661c'
AUDIT_A='81a2839f649d7895b0eb7ecacc732b700beeefc65fbdd5fec61e5057b0ca1ffe'
AUDIT_B='62a249db9b5bbdd1dd29ef68be492f684c12ef9c37fb2d25cb13bf4337837c04'

def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
    d={}
    for k,v in pairs:
        need(k not in d,'Duplicate JSON key: '+k);d[k]=v
    return d
def readjson(p):return json.loads(p.read_bytes(),object_pairs_hook=unique)
def safe(name):
    need(isinstance(name,str) and bool(name),'Invalid path')
    p=PurePosixPath(name)
    need(not p.is_absolute() and '..' not in p.parts and str(p)==name and name!='.' and '\\' not in name,'Unsafe path: '+name)
def pin(p,meta):
    need(p.is_file() and not p.is_symlink(),'Missing or nonregular file: '+p.name)
    b=p.read_bytes();need(len(b)==meta['bytes'] and sha(b)==meta['sha256'],'Payload mismatch: '+p.name)
def anchored(p,digest):
    need(not p.is_symlink() and p.is_file(),'Missing or linked manifest')
    need(sha(p.read_bytes())==digest,'Manifest anchor mismatch: '+p.name)
    return readjson(p)
def run(script,expected,optimized=False,cwd=None,extra=()):
    result=subprocess.run([sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(script),*map(str,extra)],cwd=cwd or ROOT.parent,capture_output=True,timeout=180)
    need(result.returncode==0,'Replay failure: '+script.name+' '+result.stderr.decode(errors='replace'))
    need(not result.stderr,'Unexpected replay stderr: '+script.name)
    if expected is not None:need(result.stdout==expected,'Replay bytes differ: '+script.name)
    return json.loads(result.stdout)
def patch_reading():
    lines=(ROOT/'audit_b/reports/OPTIONAL_CLARIFICATIONS.patch').read_text().splitlines(True)
    i=0;count=0
    while i<len(lines):
        need(lines[i].startswith('--- a/'),'Invalid patch source')
        name=lines[i][6:].strip();safe(name);i+=1
        need(i<len(lines) and lines[i]=='+++ b/'+name+'\n','Invalid patch destination');i+=1
        original=(ROOT/'author'/name).read_text().splitlines(True);out=[];pos=0
        while i<len(lines) and not lines[i].startswith('--- '):
            m=re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n',lines[i]);need(m is not None,'Invalid patch hunk');i+=1
            start,old_n,new_start,new_n=map(int,m.groups());need(start-1>=pos,'Overlapping patch hunk')
            out.extend(original[pos:start-1]);pos=start-1;need(len(out)==new_start-1,'Patch target position mismatch');old_seen=new_seen=0
            while i<len(lines) and not lines[i].startswith(('@@ ','--- ')):
                line=lines[i];need(line and line[0] in ' +-','Invalid patch line');i+=1
                if line[0] in ' -':
                    need(pos<len(original) and original[pos]==line[1:],'Patch context mismatch');pos+=1;old_seen+=1
                if line[0] in ' +':out.append(line[1:]);new_seen+=1
            need((old_seen,new_seen)==(old_n,new_n),'Patch hunk length mismatch')
        out.extend(original[pos:]);need(''.join(out).encode()==(ROOT/'reading'/name).read_bytes(),'Reading copy differs from exact optional patch');count+=1
    need(count==2,'Expected exactly two clarified manuscripts')

def verify(anchor):
    manifest=anchored(ROOT/'PUBLIC_MANIFEST.json',anchor)
    need(manifest['problem_id']==30005990 and manifest['status']=='unsolved' and manifest['turns']=='5/5','Disposition mismatch')
    files=manifest['files'];need(isinstance(files,dict),'Invalid inventory')
    expected=set(files)|{'PUBLIC_MANIFEST.json'};dirs=set()
    for name in expected:
        safe(name);dirs.update(str(p) for p in PurePosixPath(name).parents if str(p)!='.')
    actual=set();actualdirs=set()
    for p in ROOT.rglob('*'):
        rel=p.relative_to(ROOT).as_posix();need(not p.is_symlink(),'Symlink member: '+rel)
        if p.is_file():actual.add(rel)
        elif p.is_dir():actualdirs.add(rel)
        else:raise ValueError('Nonregular member: '+rel)
    need(actual==expected and actualdirs==dirs,'Exact publication membership mismatch')
    for name,meta in files.items():pin(ROOT/name,meta)
    am=anchored(ROOT/'author/MANIFEST.json',AUTHOR)
    aa=anchored(ROOT/'audit_a/AUDIT_MANIFEST.json',AUDIT_A)
    ab=anchored(ROOT/'audit_b/reports/MANIFEST.json',AUDIT_B)
    seen=set()
    for rec in am['files']:
        safe(rec['path']);need(rec['path'] not in seen,'Duplicate author path');seen.add(rec['path']);pin(ROOT/'author'/rec['path'],rec)
    need(seen|{'MANIFEST.json'}=={p.name for p in (ROOT/'author').iterdir()},'Author inventory mismatch')
    for rec in aa['audit_artifacts']:safe(rec['file']);pin(ROOT/'audit_a'/rec['file'],rec)
    for rec in aa['reviewed_inputs']:pin(ROOT/'author'/rec['file'],rec)
    for rec in ab['inputs']:pin(ROOT/'author'/PurePosixPath(rec['path']).name,rec)
    for rec in ab['outputs']:
        name=rec['path'].removeprefix('boundary_frequency_30005990_second_audit/');safe(name);pin(ROOT/'audit_b'/name,rec)
    need(aa['corrective_patch_required'] is False and aa['global_spectral_attainment']=='unproved','Audit A scope mismatch')
    verdict=readjson(ROOT/'audit_b/reports/VERDICT.json')
    need(verdict['verdict']=='accept_strong_partial' and verdict['full_original_problem_status']=='unsolved' and verdict['mandatory_repairs']==[],'Audit B scope mismatch')
    pin(ROOT/'AUTHOR_FREEZE.zip',{'bytes':32339,'sha256':'c7a113b0dd87bad1e80995cf8d5d6660f13097595987e5720ec30f1dd10c1196'})
    with zipfile.ZipFile(ROOT/'AUTHOR_FREEZE.zip') as z:
        names=z.namelist();need(len(names)==14 and len(set(names))==14 and set(names)==seen|{'MANIFEST.json'},'Author archive inventory mismatch')
        for name in names:need(z.read(name)==(ROOT/'author'/name).read_bytes(),'Archive member mismatch')
    patch_reading()
    runs=[]
    for optimized in (False,True):
        a=run(ROOT/'author/check_math.py',(ROOT/'author/check_results.json').read_bytes(),optimized)
        need(a['exact_predicates']==19141 and a['status']=='PASS','Author check count mismatch')
        b=run(ROOT/'audit_a/audit_math.py',(ROOT/'audit_a/AUDIT_MATH_RESULTS.json').read_bytes(),optimized)
        need(b['status']=='pass','Audit A replay mismatch')
        c=run(ROOT/'replay/audit_b_controls.py',(ROOT/'audit_b/checks/results.json').read_bytes(),optimized)
        need(c['number_of_controls']==16 and all(v['passed'] for v in c['results'].values()),'Audit B control mismatch')
        runs.append({'optimized':optimized,'author_predicates':a['exact_predicates'],'audit_a':'pass','audit_b_controls':c['number_of_controls']})
    # Preserve the original audit B code and recreate only its authored inputs.
    with tempfile.TemporaryDirectory(prefix='boundary-frequency-original-audit-') as td:
        temp=Path(td);audit=temp/'audit';(audit/'checks').mkdir(parents=True);(audit/'frozen').mkdir();(temp/'boundary_frequency_30005990/packet').mkdir(parents=True)
        shutil.copyfile(ROOT/'audit_b/checks/independent_controls.py',audit/'checks/independent_controls.py')
        for name in ['PROOF.md','REALIZATION_APPROACHES.md']:
            for dest in [audit/'frozen'/name,temp/'boundary_frequency_30005990/packet'/name]:shutil.copyfile(ROOT/'author'/name,dest)
        run(audit/'checks/independent_controls.py',(ROOT/'audit_b/checks/results.json').read_bytes(),False,cwd=temp)
        need((audit/'checks/results.json').read_bytes()==(ROOT/'audit_b/checks/results.json').read_bytes(),'Original audit B written results differ')
    run(ROOT/'author/verify_packet.py',None,False,extra=['--replay'])
    run(ROOT/'audit_a/verify_audit.py',None,False,extra=['--packet',ROOT/'author'])
    # Audit B's historical output remains immutable after all runs.
    for name,meta in files.items():pin(ROOT/name,meta)
    return {'status':'PASS_PUBLICATION_REPLAY','problem_id':30005990,'full_target_status':'unsolved','turns':'5/5','files':len(expected),'source_contents_required':False,'original_audit_b_replayed':True,'optional_patch_verified':True,'runs':runs,'analytic_proof_certified_by_computation':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);args=ap.parse_args()
    try:
        need(re.fullmatch('[0-9a-f]{64}',args.manifest_sha256) is not None,'Invalid external anchor')
        print(json.dumps(verify(args.manifest_sha256),sort_keys=True,indent=2))
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr);return 1
    return 0
if __name__=='__main__':sys.exit(main())
