#!/usr/bin/env python3
"""Read-only reconstruction of frozen generations; writes owned review receipts."""
import datetime,hashlib,json,os,subprocess,zipfile
from pathlib import Path,PurePosixPath
O=Path(__file__).resolve().parent;A=O.parents[1];R=A.parents[1];REPO=R.parent;P=R/'private/pr0399_package05'
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def check(root,entries):
    seen=set()
    for e in entries:
        n=e['path'];p=root/n
        require(n not in seen and not PurePosixPath(n).is_absolute() and all(q not in {'','.','..'} for q in n.split('/')),'safe unique binding')
        require(not p.is_symlink() and not any(q.is_symlink() for q in p.parents),'no symlink')
        b=p.read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'binding '+str(p));seen.add(n)
    return len(seen)
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'})
def state():
    result={}
    for label,paths in [('flat',list((REPO/'.zenodo-state').glob('*.json'))),('recursive',[p for p in (REPO/'.zenodo-state').rglob('*') if p.is_file()])]:
        entries=sorted((p.relative_to(REPO).as_posix(),p.stat().st_size,sha(p.read_bytes())) for p in paths)
        result[label]={'files':len(entries),'sha256':sha(json.dumps(entries,separators=(',',':')).encode())}
    result['branch']=git('symbolic-ref','--short','HEAD').decode().strip()
    for n in ['HEAD','index','packed-refs']:
        path=Path(git('rev-parse','--git-path',n).decode().strip());path=path if path.is_absolute() else REPO/path
        result[n]=sha(path.read_bytes()) if path.exists() else None
    return result
def main():
    results={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};H=A/'ops_doi_destination_repair_20261021';D=H/'pre_destination_binding';B=D/'ops_record_url_repair_20261021/pre_record_url_binding';N=B/'ops_identity_repair_20261021/pre_review02_binding'
    for key,root,manifest in [('current714',A,H/'MANIFEST.json'),('old356',D,D/'ops_record_url_repair_20261021/MANIFEST.json'),('old156',B,B/'ops_identity_repair_20261021/MANIFEST.json'),('original42',N,B/'publication_operations_preparation/MANIFEST.json')]:
        m=json.loads(manifest.read_bytes());results[key]={'manifest_sha256':sha(manifest.read_bytes()),'files':check(root,m['files']),'immutable_inputs':check(root,m.get('immutable_inputs',[])),'generation_root':str(root.relative_to(A)) if root!=A else '.'}
    for family in ['measure_ordinal','continuity_core','priority_source','package_adversary_01','package_adversary_02','package_adversary_03','package_adversary_04']:
        d=A/'reviews'/family;m=d/'AUTHORED_FILE_MANIFEST.json';results[family]=check(d,json.loads(m.read_bytes())['files']);require((d/'AUTHORED_FILE_MANIFEST.sha256').read_text().split()[0]==sha(m.read_bytes()),'seal checksum')
    results['preparer108']=check(A,json.loads((A/'publication_support/PREPARER_FILE_MANIFEST.json').read_bytes())['files'])
    snapshot=json.loads((A/'SOURCE_SNAPSHOT.json').read_bytes());head=snapshot['head'];parent=snapshot['comparison_base'];require(git('show','-s','--format=%P',head).decode().strip()==parent,'original parent')
    for e in snapshot['files']:
        b=(A/e['snapshot']).read_bytes();require(b==git('show',head+':'+e['repository_path']),'actual Git original');require(len(b)==e['bytes'] and sha(b)==e['sha256'],'original bytes');require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob'],'blob identity')
    results['originals_actual_git']=len(snapshot['files']);results['queue_rows']={}
    for commit in [parent,head]:
        rows=[r for r in git('show',commit+':unsolved_math_prioritization/QUEUE.md').decode().splitlines() if '| 30001179 / OWR-3392-005 |' in r];require(len(rows)==1,'one original row');results['queue_rows'][commit]=rows[0]
    pub=A/'preprint/publication';release=pub/'RELEASE_FILES.json';require(sha(release.read_bytes())=='9d9bca984bcbd5134028513db8b3294bae6f77c7994ec378053e60655af03fcb','release identity');results['release5']=check(pub,json.loads(release.read_bytes())['files'])
    with zipfile.ZipFile(pub/'free-product-tensor-core-verification.zip') as z:
        names=z.namelist();require(len(names)==82 and len(set(names))==82 and z.testzip() is None,'ZIP CRC/inventory');prefix='free-product-tensor-core-verification/';listing=json.loads(z.read(prefix+'FILES.json'));require(len(listing['files'])==81,'payload count');require(set(names)=={prefix+'FILES.json'}|{prefix+e['path'] for e in listing['files']},'ZIP manifest inventory')
        for i in z.infolist():
            require(not i.is_dir() and all(c not in {'','.','..'} for c in i.filename.split('/')) and not PurePosixPath(i.filename).is_absolute() and (i.external_attr>>16&0o170000)!=0o120000,'ZIP path/type');z.read(i).decode('utf-8')
        for e in listing['files']:
            b=z.read(prefix+e['path']);require(len(b)==e['bytes'] and sha(b)==e['sha256'],'ZIP payload')
        for e in snapshot['files']:require(z.read(prefix+e['snapshot'])==(A/e['snapshot']).read_bytes(),'ZIP original')
        require(z.read(prefix+'manuscript/main.tex')==(pub/'free-product-tensor-core.tex').read_bytes(),'archive TeX')
        extract=P/'archive'
        if not extract.exists():z.extractall(extract)
        results['archive']={'members':82,'payloads':81,'all_utf8':True,'originals':11,'tex_identical':True}
    results['root_semantic_lead_sha256']=sha((A/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').read_bytes());require(results['root_semantic_lead_sha256']=='af763826f5e22bb64887496eada7e4aaa9c944faf45db3a0c93386b9833fbe39','root semantic binding');results['clearance_exists']=(A/'ROOT_PUBLICATION_CLEARANCE.json').exists();require(not results['clearance_exists'],'no review authorization')
    now=state();baseline=O/'STATE_BASELINE.json'
    if baseline.exists():require(json.loads(baseline.read_bytes())==now,'state changed during review');results['state_preserved']=True
    else:baseline.write_text(json.dumps(now,indent=2)+'\n')
    require(now['branch']=='main','main branch');require(now['flat']=={'files':241,'sha256':'1f67238497dbd8d275232e10dcdda23a03f151480d6c853c84d6fff720f57033'},'flat saved states');require(now['recursive']=={'files':314,'sha256':'fe319e19f015bf2654598d4456551ba9a3a73b58c72738bf80fca8aa02aef5cc'},'recursive states')
    results['state']=now;(O/'INPUT_VERIFICATION.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
if __name__=='__main__':main()
