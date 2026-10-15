"""Authenticate reviewer02 and candidate pins; optionally reproduce finite controls.

Trust the externally pinned reviewed script/manifest, Python/dependencies/OS,
and SHA256. This is no signature, sandbox, analytic proof or priority certificate.
All extraction/replay writes stay in this review's ignored private directory.
"""
import argparse,hashlib,json,os,stat,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
R=Path(__file__).absolute().parent
A=R.parents[1]
FREEZE='c58e74cd19d42ac1b867dc9add2f6c3ab9075248dcac0e19432f851ccba7509f'
ARCHIVE='291becf72ccd6345701711ab8523cf0966b042ce147e907cefdeb4bece014fd0'
PACK='0189e0ecd7bb39a1ed3899ee785cfc9f48bae7fdf386cd3002fd0a4849b70313'
HEAD='d186dea31791cd3e8acf6829e0b65d01849623b8'
PY=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python')
def need(c,label):
    if not c:raise RuntimeError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def data(p):
    need(stat.S_ISREG(p.lstat().st_mode),'nonregular '+str(p));return p.read_bytes()
def fingerprint(p,rec):
    b=data(p);need(sha(b)==rec['sha256'] and len(b)==rec['bytes'],'fingerprint '+str(p));return b
def authenticate(pin,extract=False):
    raw=data(R/'MANIFEST.json');need(sha(raw)==pin,'external review anchor');m=json.loads(raw)
    need(set(m['explicit_public_allowlist'])==set(m['files']) and 'MANIFEST.json' not in m['files'],'review self exclusion')
    for n,rec in m['files'].items():
        q=PurePosixPath(n);need(not q.is_absolute() and q.as_posix()==n and '..' not in q.parts,'review path');fingerprint(R/n,rec)
    freeze=data(A/'publication/PREPUBLICATION_FREEZE.json');need(sha(freeze)==FREEZE,'freeze');f=json.loads(freeze)
    for n,rec in f['files'].items():fingerprint(A/'publication'/n,rec)
    snapshot=json.loads(data(A/'ORIGINAL_SNAPSHOT.json'));need(snapshot['head']==HEAD and len(snapshot['files'])==28,'snapshot identity')
    for n,pin in snapshot['files'].items():
        b=data(A/'original'/n);need(sha(b)==pin,'original disk');p=subprocess.run(['git','show',HEAD+':'+n],cwd=A,capture_output=True,check=True);need(p.stdout==b,'original Git bytes')
    archive=A/'publication/rough-m-arrangements-source-verification-v1.0.zip';need(sha(data(archive))==ARCHIVE,'archive');dest=R/'private/extracted'
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();need(len(names)==len(set(names))==106,'archive membership');raw=z.read('PACKAGE_MANIFEST.json');need(sha(raw)==PACK,'package external anchor');pm=json.loads(raw);need(len(pm['files'])==105 and set(names)==set(pm['files'])|{'PACKAGE_MANIFEST.json'},'payload inventory')
        for i in z.infolist():
            q=PurePosixPath(i.filename);need(not q.is_absolute() and q.as_posix()==i.filename and '..' not in q.parts and stat.S_ISREG(i.external_attr>>16),'archive safe regular entry')
            b=z.read(i.filename)
            if i.filename!='PACKAGE_MANIFEST.json':need({'bytes':len(b),'sha256':sha(b)}==pm['files'][i.filename],'archive payload')
            if extract:
                p=dest/i.filename;p.parent.mkdir(parents=True,exist_ok=True);need(not p.is_symlink(),'extract symlink');p.write_bytes(b)
    return {'status':'PASS','review_public_files':len(m['files']),'candidate_files':14,'original_git_blobs':28,'archive_payloads':105,'pdf_pages':4}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--expected-manifest',required=True);ap.add_argument('--extract',action='store_true');ap.add_argument('--replay',action='store_true');args=ap.parse_args()
    result=authenticate(args.expected_manifest,args.extract)
    if args.replay:
        need((R/'private/extracted/PACKAGE_MANIFEST.json').exists(),'use --extract first')
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
        out=subprocess.run([str(PY),'-I','-B',str(R/'independent_checks.py')],cwd=R,env=env,capture_output=True,check=True);need(out.stdout==data(R/'INDEPENDENT_CHECKS.json'),'independent exact output');fresh=R/'private/REPLAY_AND_CHALLENGES_FRESH.json'
        p=subprocess.run([str(PY),'-I','-B',str(R/'replay_and_challenges.py'),'--output',str(fresh)],cwd=R,env=env,capture_output=True,check=True,timeout=1800)
        v=json.loads(data(fresh));need(v['status']=='PASS' and v['reviewer_negative_cases']==21 and v['actual_copied_math_boundary']['copied_math_rejected_before_execution'],'fresh replay result');result['fresh_replay']='PASS_four_modes_21_negatives_copied_math_guard'
        authenticate(args.expected_manifest)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
