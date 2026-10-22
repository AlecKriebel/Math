#!/usr/bin/env python3
"""Strict portable delivery/replay checks; not a proof of continuum observability."""
from pathlib import Path, PurePosixPath
import hashlib,json,os,stat,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent
PINS={
 'advection_control_30003759/MANIFEST.json':'d60b749ef5914027eed0e03da99de7e712e52a755f18c4d243ee3f6251cdb1f1',
 'advection_control_30003759_independent_audit/MANIFEST.json':'0569538896249e31268cbe7379794b7dcfeef60749ad3176f6b8e3e78aaf3a9d',
 'ADVECTION_CONTROL_30003759_SAFE_FREEZE.zip':'d6686eca2815c676f65d76bc552a2d41c9b8080dd6bca844c7d0a4815d231b26',
 'ADVECTION_CONTROL_30003759_INDEPENDENT_AUDIT_SAFE_FREEZE.zip':'049be719e3b491a4a38b60d03c172fca05c64c7c4486645d7394d04bbf0bfb0f',
}

def require(p,label):
    if not p:raise ValueError(label)

def digest(b):return hashlib.sha256(b).hexdigest()

def pathcheck(s):
    require(isinstance(s,str) and bool(s),'Nonempty path required')
    p=PurePosixPath(s)
    require(not p.is_absolute() and '..' not in p.parts and '.' not in p.parts and str(p)==s,'Unsafe path')
    return p

def regular(p):
    require(stat.S_ISREG(p.lstat().st_mode),'Regular file required: '+str(p))
    return p.read_bytes()

def closed(root,manifest_name):
    require(not root.is_symlink(),'Root symlink')
    m=json.loads(regular(root/manifest_name));rows=m['files'];paths=[r['path'] for r in rows]
    require(len(paths)==len(set(paths)),'Duplicate path')
    for s in paths:pathcheck(s);require(s!=manifest_name,'Manifest self-inclusion')
    expected={manifest_name,*paths};dirs={p.as_posix() for s in expected for p in PurePosixPath(s).parents if str(p)!='.'}
    actual=set();actual_dirs=set()
    for p in root.rglob('*'):
        mode=p.lstat().st_mode;rel=p.relative_to(root).as_posix()
        if stat.S_ISREG(mode):actual.add(rel)
        elif stat.S_ISDIR(mode):actual_dirs.add(rel)
        else:raise ValueError('Symlink or special file rejected: '+rel)
    require(actual==expected,'Closed file set mismatch')
    require(actual_dirs==dirs,'Unexpected directory')
    for r in rows:
        b=regular(root/r['path']);require(len(b)==r['bytes'] and digest(b)==r['sha256'],'Hash/size mismatch: '+r['path'])
    return rows

def archive_check(name,folder):
    expected={p.relative_to(ROOT/folder).as_posix() for p in (ROOT/folder).rglob('*') if p.is_file()}
    seen=set()
    with zipfile.ZipFile(ROOT/name) as z:
        for i in z.infolist():
            require(not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16),'Unsafe ZIP entry')
            s=i.filename.removeprefix(folder+'/');pathcheck(s)
            require(s not in seen and s in expected,'Duplicate/unlisted ZIP entry');seen.add(s)
            require(z.read(i)==regular(ROOT/folder/s),'ZIP payload mismatch')
    require(seen==expected,'ZIP closed file set mismatch')
    return len(seen)

def run(relative,opt=False,cwd=None):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    args=[sys.executable]+(['-O'] if opt else [])+[str(ROOT/relative)]
    return subprocess.check_output(args,cwd=cwd or ROOT,env=env,stderr=subprocess.STDOUT)

def main():
    rows=closed(ROOT,'PUBLICATION_MANIFEST.json')
    for p,h in PINS.items():require(digest(regular(ROOT/p))==h,'Pinned freeze mismatch: '+p)
    author='advection_control_30003759';audit='advection_control_30003759_independent_audit'
    closed(ROOT/author,'MANIFEST.json');closed(ROOT/audit,'MANIFEST.json')
    count=archive_check('ADVECTION_CONTROL_30003759_SAFE_FREEZE.zip',author)+archive_check('ADVECTION_CONTROL_30003759_INDEPENDENT_AUDIT_SAFE_FREEZE.zip',audit)
    status=json.loads(regular(ROOT/'PUBLICATION_STATUS.json'))
    require(status['overall_status']=='unsolved' and status['turns']=='1/5','Overall disposition changed')
    require(status['publication_disposition']=='qualified_prior_preprint_threshold_finding','Qualification changed')
    require(status['author_unqualified_resolution_audit']=='REVISE_REQUIRED','Audit override changed')
    require(status['positive_critical_endpoint']=='OPEN: boundedness at T=2L/M','Positive endpoint changed')
    require(status['negative_critical_endpoint']=='vanishing cost as epsilon tends to zero','Negative endpoint changed')
    require(status['verified_cost']=='L2(0,L) initial unit ball; L2(0,T) left Dirichlet control','Cost scope changed')
    require(status['review_type']=='independent AI mathematical proof review; not human peer review or formal verification','Review type changed')
    require(status['no_further_campaign_scope']=='Infimum-only research stopping decision; does not resolve the positive endpoint','Stopping scope changed')
    require(status['infimum_subproblem']['classification']=='prior_resolution_preprint','Subproblem class changed')
    require(status['infimum_subproblem']['positive_drift']=='2L/M' and status['infimum_subproblem']['negative_drift']=='(2+2sqrt(2))L/abs(M)','Thresholds changed')
    require(status['novelty']=='No new full solution or priority claim','Novelty changed')
    verdict=json.loads(regular(ROOT/audit/'AUDIT_VERDICT.json'))
    require(verdict['verdict']=='REVISE_REQUIRED' and verdict['recommended_queue']['status']=='unsolved','Audit gate mismatch')
    for opt in (False,True):
        require(run(author+'/code/verify.py',opt)==regular(ROOT/author/'CHECK_RESULTS.json'),'Author replay mismatch')
        require(run(audit+'/independent_verify.py',opt)==regular(ROOT/audit/'independent_results.json'),'Independent replay mismatch')
        require(json.loads(run(author+'/code/check_manifest.py',opt))['status']=='PASS','Author manifest replay')
        integrity=json.loads(run(audit+'/verify_integrity.py',opt))
        require(all(v['status']=='PASS' for v in integrity.values()),'Strict historical replay')
        require(run(audit+'/integrity_negative_controls.py',opt)==regular(ROOT/audit/'integrity_negative_results.json'),'Integrity controls mismatch')
    # Ensure replay did not add or modify delivery files.
    closed(ROOT,'PUBLICATION_MANIFEST.json')
    print(json.dumps({'result':'PASS','problem_id':'30003759','status':'unsolved','turns':'1/5','positive_critical_endpoint':'OPEN','frozen_files_preserved':count,'archives_preserved':2,'packet_files':len(rows)+1,'normal_and_optimized':True,'author_replay_byte_equal':True,'independent_replay_byte_equal':True,'historical_integrity_controls':6,'scope':'Qualified prior-preprint infimum thresholds and negative endpoint; no full solution or formal verification.','publication_manifest_sha256':digest(regular(ROOT/'PUBLICATION_MANIFEST.json'))},indent=2,sort_keys=True))

if __name__=='__main__':main()
