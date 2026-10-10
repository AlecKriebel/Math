#!/usr/bin/env python3
"""Independent finite algebra and frozen-packet replay; standard library only.

Usage: python -I -S -B audit_controls.py AUTHOR_RELEASE [RETAINED_SOURCE_DIRECTORY]
This is not a verifier for the external quantum-topology theorems.
"""
from pathlib import Path
import copy, hashlib, json, os, shutil, subprocess, sys, tempfile

MANIFEST_SHA256 = 'abc975e091ff72d9b020f238ef4ff7884a4ce9c0ed755b34f45626c1ef74158c'
BOOTSTRAP_SHA256 = '301e0c33f5eafccb1701687ae9cfbd574496b0ef1fd357bb4c4efe728c2379fa'
SOURCE_NAMES = {'O':'ohtsuki2002.pdf','L':'le_psu_author.pdf','HL':'habiro_le_v2.pdf','LQ':'le_quantum.pdf','H':'habiro2008.pdf','L-preprint':'le_psu.pdf','HL-older':'habiro_le.pdf','BG':'beliakova_gorsky.pdf','HL-published':'habiro_le_published.pdf'}
class Rejected(Exception): pass
def need(ok,msg):
    if not ok: raise Rejected(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def pairs(items):
    result={}
    for key,value in items:
        need(key not in result,'duplicate key')
        result[key]=value
    return result
def read(p): return json.loads(p.read_text(),object_pairs_hook=pairs)
def dualadd(a,b): return (a[0]+b[0],a[1]+b[1])
def dualmul(a,b): return (a[0]*b[0],a[0]*b[1]+a[1]*b[0])
def dualpow(a,n):
    result=(1,0)
    for _ in range(n): result=dualmul(result,a)
    return result
def vector_diff(rows): return [rows[2][i]-2*rows[1][i]+rows[0][i] for i in range(len(rows[0]))]
def check_math():
    q=(1,1)
    need(dualmul(q,(1,-1))==(1,0),'inverse q')
    need(dualmul((0,1),(0,2))==(0,0),'level two ideal')
    rows=[[0,1,n,1,2*n,1] for n in (1,2,3)]
    need(vector_diff(rows)==[0]*6,'symbolic generic first jet')
    # Positive controls: arbitrary affine rank coefficients satisfy the constraint.
    positive=[]
    for a,b in [(0,0),(0,-6),(7,-11),(-13,4)]:
        values=[a+b*n for n in (1,2,3)]
        need(values[2]-2*values[1]+values[0]==0,'affine control')
        positive.append(values)
    first=dualmul(dualmul(q,dualadd((1,0),q)),(0,-3))
    need(first==(0,-6),'cancelled Poincare term')
    # This polynomial identity is finite. The report proves the all-k tail order.
    zero_terms=[]
    for k in range(2,18):
        geom=(0,0)
        for j in range(k+1): geom=dualadd(geom,dualpow(q,j))
        term=dualmul(dualpow(q,k),geom)
        for j in range(k+2,2*k+2): term=dualmul(term,(0,-j))
        need(term==(0,0),'tail control')
        zero_terms.append(k)
    values=[-n*(n*n-1) for n in (1,2,3)]
    residual=values[2]-2*values[1]+values[0]
    need(values==[0,-6,-24] and residual==-12,'actual cubic coefficients')
    later=[-n*(n*n-1) for n in (2,3,4)]
    need(later==[-6,-24,-60] and later[2]-2*later[1]+later[0]==-18,'rank one independent control')
    return {'generic_symbolic_identity':True,'positive_affine_controls':positive,'poincare_first_coefficient':first[1],'sample_tail_indices':zero_terms,'actual_first_coefficients':values,'second_difference':residual,'later_ranks_first_coefficients':later,'later_second_difference':-18}
def run(code,args=(),opt='',cwd=None,env=None):
    argv=[sys.executable,'-I','-S','-B']+([opt] if opt else [])+[str(code),*map(str,args)]
    return subprocess.run(argv,cwd=cwd,env=env,capture_output=True,timeout=30)
def writable_copy(src,dst):
    shutil.copytree(src,dst)
    for p in [dst,*dst.rglob('*')]:
        if not p.is_symlink(): p.chmod(0o700 if p.is_dir() else 0o600)
def main():
    need(len(sys.argv) in (2,3),'usage: audit_controls.py AUTHOR_RELEASE [SOURCE_DIRECTORY]')
    root=Path(sys.argv[1]).resolve()
    need(sha((root/'AUTHOR_MANIFEST.json').read_bytes())==MANIFEST_SHA256,'independent manifest pin')
    need(sha((root/'bootstrap.py').read_bytes())==BOOTSTRAP_SHA256,'independent bootstrap pin')
    m=read(root/'AUTHOR_MANIFEST.json')
    seen=set()
    for e in m['files']:
        need(e['path'] not in seen,'duplicate payload name'); seen.add(e['path'])
        p=root/'packet'/e['path'];need(not p.is_symlink() and p.is_file(),'regular payload')
        raw=p.read_bytes();need(len(raw)==e['bytes'] and sha(raw)==e['sha256'],'payload pin')
    need(seen=={p.name for p in (root/'packet').iterdir()},'inventory')
    initial={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
    modes=[]
    for opt in ('','-O','-OO'):
        result=run(root/'bootstrap.py',[root/'packet'],opt)
        need(result.returncode==0,'baseline replay '+opt+': '+result.stderr.decode())
        modes.append({'mode':opt or 'normal','stdout':json.loads(result.stdout)})
    source_results=[]
    if len(sys.argv)==3:
        sources=Path(sys.argv[2]).resolve()
        for s in read(root/'packet'/'SOURCE_METADATA.json')['sources']:
            raw=(sources/SOURCE_NAMES[s['id']]).read_bytes()
            need(len(raw)==s['bytes'] and sha(raw)==s['sha256'],'source mismatch '+s['id'])
            source_results.append({'id':s['id'],'bytes':len(raw),'sha256':sha(raw),'matches':True})
    controls=[]
    with tempfile.TemporaryDirectory(prefix='habiro-independent-audit-') as tmp:
        temp=Path(tmp)
        cases=[('wrong_rank_three','first_coefficients',[0,-6,-12]),('zero_Casson','casson_normalization',0),('wrong_rank_list','ranks',[1,2,4]),('boolean_rank','ranks',[True,2,3]),('wrong_parameter','quantum_parameter','q=1+2*x'),('wrong_forced_value','forced_rank_three',-24),('wrong_residual','second_difference',0),('boolean_problem','problem_id',True)]
        for name,key,value in cases:
            dest=temp/name;writable_copy(root,dest)
            c=read(dest/'packet'/'CERTIFICATE.json');c[key]=value
            (dest/'packet'/'CERTIFICATE.json').write_text(json.dumps(c))
            result=run(dest/'packet'/'verify.py')
            need(result.returncode!=0 and b'REJECT' in result.stderr,'semantic mutation escaped: '+name)
            controls.append({'name':name,'rejected':True})
        for name in ('duplicate_certificate_key','stale_payload','extra_payload','missing_payload','symlink_payload','manifest_hash_change','checker_hash_change'):
            dest=temp/name;writable_copy(root,dest);packet=dest/'packet'
            if name=='duplicate_certificate_key':
                p=packet/'CERTIFICATE.json';p.write_text(p.read_text().replace('{','{"schema":"duplicate",',1)); result=run(packet/'verify.py')
            else:
                if name=='stale_payload':
                    p=packet/'PROOF_AND_STATUS.md';p.write_text(p.read_text()+'\nchanged\n')
                elif name=='extra_payload': (packet/'extra.txt').write_text('extra')
                elif name=='missing_payload': (packet/'CERTIFICATE.json').unlink()
                elif name=='symlink_payload':
                    p=packet/'CERTIFICATE.json';raw=p.read_bytes();p.unlink();(dest/'target.json').write_bytes(raw);p.symlink_to(dest/'target.json')
                elif name=='manifest_hash_change':
                    p=dest/'AUTHOR_MANIFEST.json';p.write_text(p.read_text()+'\n')
                elif name=='checker_hash_change':
                    p=packet/'verify.py';p.write_text(p.read_text()+'\n# altered\n')
                result=run(dest/'bootstrap.py',[packet])
            need(result.returncode!=0 and b'REJECT' in result.stderr,'integrity mutation escaped: '+name)
            controls.append({'name':name,'rejected':True})
        hostile=temp/'hostile';hostile.mkdir();sentinel=hostile/'IMPORTED'
        for name in ('json','hashlib','pathlib','subprocess'):
            (hostile/(name+'.py')).write_text('open('+repr(str(sentinel))+',"w").write("bad")\nraise RuntimeError("hostile import")\n')
        env=dict(os.environ);env['PYTHONPATH']=str(hostile)
        result=run(root/'bootstrap.py',[root/'packet'],cwd=hostile,env=env)
        need(result.returncode==0 and not sentinel.exists(),'hostile import isolation')
    final={str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
    need(initial==final,'author originals changed')
    return {'schema':'habiro-rank-independent-audit-v1','status':'PASS','author_manifest_sha256':MANIFEST_SHA256,'author_bootstrap_sha256':BOOTSTRAP_SHA256,'payload_files_verified':len(seen),'math':check_math(),'baseline_modes':modes,'negative_controls':controls,'hostile_import_control':True,'source_checks':source_results,'author_originals_unchanged':True,'limitations':'Exact finite algebra, source-byte identities and replay controls only; not proof-assistant verification or reproof of cited topology.'}
if __name__=='__main__':
    try: print(json.dumps(main(),indent=2,sort_keys=True))
    except (Rejected,OSError,ValueError,KeyError,TypeError,IndexError,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
