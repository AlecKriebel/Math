#!/usr/bin/env python3
"""Replay independent finite, optimization, and frozen-input adversarial controls."""
import argparse, ast, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

def require(ok,message):
    if not ok: raise RuntimeError(message)

def invoke(script,args=(),flags=(),cwd=None):
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    r=subprocess.run([sys.executable,*flags,str(script),*map(str,args)],capture_output=True,text=True,cwd=cwd,env=env)
    return r

def tail(r):return (r.stderr.strip().splitlines() or [''])[ -1]
def update_sums(root):
    lines=[]
    for p in sorted(root.iterdir()):
        if p.is_file() and p.name!='SHA256SUMS':lines.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name)
    (root/'SHA256SUMS').write_text('\n'.join(lines)+'\n')

def mutate(root,kind):
    proof=root/'TURN_5_COMPACTNESS.md';manifest=root/'AUTHOR_MANIFEST.json'
    if kind=='proof_byte': proof.write_bytes(proof.read_bytes()+b'\n')
    elif kind=='proof_truncate':proof.write_bytes(proof.read_bytes()[:-11])
    elif kind=='missing_file':proof.unlink()
    elif kind=='extra_file':(root/'unexpected.txt').write_text('unexpected')
    elif kind=='symlink_file':proof.unlink();proof.symlink_to('README.md')
    elif kind=='checksum_byte':(root/'SHA256SUMS').write_bytes((root/'SHA256SUMS').read_bytes()+b'\n')
    elif kind=='manifest_duplicate_key':manifest.write_text(manifest.read_text().replace('"problem_id": 30001518,','"problem_id": 30001518, "problem_id": 1,'))
    else:
        m=json.loads(manifest.read_text())
        if kind=='manifest_bytes':m['files'][0]['bytes']+=1
        elif kind=='manifest_hash':m['files'][0]['sha256']='0'*64
        elif kind=='manifest_duplicate_path':m['files'].append(dict(m['files'][0]))
        elif kind=='manifest_traversal':m['files'][0]['path']='../outside'
        elif kind=='manifest_absolute':m['files'][0]['path']='/tmp/outside'
        elif kind=='coordinated_proof_and_rehash':
            proof.write_bytes(proof.read_bytes()+b'\nDeliberate false control: this proves perfection for every bounded body.\n')
            for row in m['files']:
                if row['path']==proof.name:
                    b=proof.read_bytes();row['bytes']=len(b);row['sha256']=hashlib.sha256(b).hexdigest()
        else:raise RuntimeError('unknown mutation')
        manifest.write_text(json.dumps(m,indent=2)+'\n');update_sums(root)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--archive',type=Path)
    ap.add_argument('--source-dir',type=Path);ap.add_argument('--corpus-dir',type=Path);a=ap.parse_args()
    author=a.author.resolve();own=Path(__file__).resolve().parent; archive=a.archive.resolve() if a.archive else None
    anchor_args=[author]+(['--archive',archive] if archive else [])
    anchored=invoke(own/'check_frozen_author.py',anchor_args);require(anchored.returncode==0,'frozen author not authentic')
    replay_args=[]
    for flag,path in [('--source-dir',a.source_dir),('--corpus-dir',a.corpus_dir)]:
        if path is not None:replay_args += [flag,path.resolve()]
    author_replay=invoke(author/'replay.py',replay_args);require(author_replay.returncode==0,'author replay failed')
    positives=[];independent_result=None;modes=[(),('-O',),('-OO',)]
    for mode in modes:
        r=invoke(own/'independent_verify.py',flags=mode);require(r.returncode==0,'independent exact controls failed')
        d=json.loads(r.stdout); require(d['optimization']==len(''.join(mode).replace('-','')),'optimization mode not active')
        comp=dict(d);comp.pop('optimization')
        if independent_result is None:independent_result=comp
        else:require(comp==independent_result,'optimized independent results changed')
        positives.append({'flags':list(mode),'active_optimization':d['optimization'],'checks':d['checks'],'exit_code':r.returncode})
    mutants=[]
    for mode in modes:
        for label in ['defect_factor','jacobian','all_retro','exit_position']:
            r=invoke(own/'independent_verify.py',['--mutant',label],mode)
            require(r.returncode!=0,'faulty independent control accepted')
            mutants.append({'variant':label,'flags':list(mode),'exit_code':r.returncode,'error_tail':tail(r)})
    author_optimized=[]
    for mode in modes[1:]:
        for script in ['verify.py','replay.py']:
            r=invoke(author/script,flags=mode);require(r.returncode!=0,'author optimized mode unexpectedly accepted')
            author_optimized.append({'script':script,'flags':list(mode),'exit_code':r.returncode,'error_tail':tail(r)})
    corrupted=[];self_consistency=None;relocated=None;external_negative=None
    labels=['proof_byte','proof_truncate','missing_file','extra_file','symlink_file','checksum_byte','manifest_duplicate_key','manifest_bytes','manifest_hash','manifest_duplicate_path','manifest_traversal','manifest_absolute','coordinated_proof_and_rehash']
    with tempfile.TemporaryDirectory(prefix='retro-audit-') as td:
        temp=Path(td)
        p=temp/'relocated'/'packet';p.parent.mkdir();shutil.copytree(author,p)
        r=invoke(p/'replay.py',cwd=temp);require(r.returncode==0,'relocated author replay failed');relocated=json.loads(r.stdout)
        for label in labels:
            p=temp/label;shutil.copytree(author,p);mutate(p,label)
            for mode in modes:
                r=invoke(own/'check_frozen_author.py',[p],mode)
                require(r.returncode!=0,'corrupt author packet accepted')
                corrupted.append({'mutation':label,'flags':list(mode),'exit_code':r.returncode,'error_tail':tail(r)})
            if label=='coordinated_proof_and_rehash':
                r=invoke(p/'replay.py');require(r.returncode==0,'self-consistency limitation control changed')
                self_consistency={'author_replay_exit_code':r.returncode,'author_self_consistency_accepts_coordinated_rehash':True,
                    'audit_external_anchor_rejects':True,'meaning':'Author replay checks internal consistency and finite controls, not authenticity or arbitrary proof prose.'}
        if archive:
            bad=temp/'corrupt.zip';b=archive.read_bytes();bad.write_bytes(b[:-1])
            r=invoke(own/'check_frozen_author.py',[author,'--archive',bad]);require(r.returncode!=0,'truncated archive accepted')
            corrupted.append({'mutation':'archive_truncate','flags':[],'exit_code':r.returncode,'error_tail':tail(r)})
        if a.source_dir:
            src=temp/'pdfs';shutil.copytree(a.source_dir,src,ignore=shutil.ignore_patterns('*.txt','*.png'))
            md=json.loads((author/'SOURCE_METADATA.json').read_text());f=src/md['pdfs'][0]['filename'];f.write_bytes(f.read_bytes()[:-1])
            r=invoke(author/'replay.py',['--source-dir',src]);require(r.returncode!=0,'corrupt source accepted')
            external_negative={'mutation':'source_pdf_truncate','exit_code':r.returncode,'error_tail':tail(r)}
    for script in ['independent_verify.py','check_frozen_author.py','run_audit.py']:
        tree=ast.parse((own/script).read_text())
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)),'audit script relies on stripped assert')
    # The exact author anchor is checked again after every test.
    r=invoke(own/'check_frozen_author.py',anchor_args);require(r.returncode==0,'author freeze changed during audit')
    output={'schema':'independent-retroreflector-audit-controls-v1','problem_id':30001518,'status':'PASS_SCOPED_AUDIT_CONTROLS',
        'anchored_author':json.loads(anchored.stdout),'author_replay':json.loads(author_replay.stdout),
        'independent_controls':independent_result,'genuine_optimization_runs':positives,
        'independent_faults_rejected':mutants,'author_optimization_rejections':author_optimized,
        'corruptions_rejected':corrupted,'external_source_negative':external_negative,
        'relocated_author_replay':relocated,'self_consistency_limitation_control':self_consistency,
        'audit_scripts_contain_no_assert_statements':True,'author_freeze_unchanged':True,'full_problem_solved':False}
    print(json.dumps(output,indent=2,sort_keys=True))

if __name__=='__main__': main()
