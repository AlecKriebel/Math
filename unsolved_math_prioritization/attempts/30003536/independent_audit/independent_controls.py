#!/usr/bin/env python3
"""Independent finite checks and adversarial replay of the pinned author packet.

No analytic proof is established by this program. Python standard library only.
Temporary mutations are never applied to the author packet. No network access.
"""
import argparse
import ast
import copy
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PIN = 'bd0c3dbdf92de2f92f3d31ed64033dfe16e188d1ea28ed66b069af2fad8919d6'

class Failure(Exception):
    pass

def require(ok, message):
    if not ok:
        raise Failure(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inventory(root):
    return {p.name: {'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
            for p in sorted(root.iterdir()) if p.is_file()}

# Exact a+b*sqrt(3) arithmetic. The latitude moments through degree three
# suffice for the quadratic Taylor polynomial of the field at the origin.
class Radical:
    def __init__(self,a=0,b=0):
        self.a,self.b=Q(a),Q(b)
    def __add__(self,other):
        other=promote(other)
        return Radical(self.a+other.a,self.b+other.b)
    __radd__=__add__
    def __neg__(self):return Radical(-self.a,-self.b)
    def __sub__(self,other):return self+-promote(other)
    def __rsub__(self,other):return promote(other)+-self
    def __mul__(self,other):
        other=promote(other)
        return Radical(self.a*other.a+3*self.b*other.b,self.a*other.b+self.b*other.a)
    __rmul__=__mul__
    def __eq__(self,other):
        other=promote(other)
        return self.a==other.a and self.b==other.b

def promote(x):return x if isinstance(x,Radical) else Radical(x)

def moment(indices):
    axial=indices.count(0)
    transverse=[indices.count(j) for j in range(1,8)]
    if any(n%2 for n in transverse):return Radical()
    power=Radical(1)
    for _ in range(axial):power*=Radical(0,Q(1,3))
    if sum(transverse)==2:power*=Q(2,21)
    elif sum(transverse)!=0:raise Failure('moment degree exceeds independent control')
    return power

def mathematical_checks():
    count={'latitude_taylor':0,'vector_moment':0,'three_point':0,'off_dyadic_shell_sum':0,'boundary_ratio':0}
    def check(ok,group,label):
        require(ok,label);count[group]+=1
    # Expand (x_i-y_i)*(1-2*x.y+|x|^2)^(-3/2), whose binomial
    # coefficients through order two are 1, -3/2, and 15/8.
    # This is a direct Taylor expansion, not differentiation of author code.
    c=[-moment([i]) for i in range(8)]
    linear=[[Radical(int(i==j))-3*moment([i,j]) for j in range(8)] for i in range(8)]
    second=[[[3*int(i==j)*moment([k])+3*int(i==k)*moment([j])+
               3*int(j==k)*moment([i])-15*moment([i,j,k])
               for k in range(8)] for j in range(8)] for i in range(8)]
    for j in range(8):
        check(sum((2*c[i]*linear[i][j] for i in range(8)),Radical())==0,
              'latitude_taylor','norm gradient')
        for k in range(8):
            value=sum((2*linear[i][j]*linear[i][k]+2*c[i]*second[i][j][k]
                       for i in range(8)),Radical())
            expected=Q(-8,3) if j==k==0 else Q(-4,147) if j==k else Q(0)
            check(value==expected,'latitude_taylor','full norm Hessian entry')
    check(Q(-8,3)+7*Q(-4,147)==Q(-20,7),'latitude_taylor','norm Laplacian')
    def dot(u,v):return sum((a*b for a,b in zip(u,v)),Q(0))
    def minus(u,v):return tuple(a-b for a,b in zip(u,v))
    def kernel(z,s):
        r2=dot(z,z);require(r2>0,'collision in exact kernel control')
        return tuple(v/r2**((s+1)//2) for v in z)
    points=[(Q(0),Q(0),Q(0)),(Q(1),Q(2),Q(-1)),(Q(-2),Q(1),Q(3)),(Q(3),Q(-2),Q(1)),(Q(4),Q(3),Q(2))]
    weights=[Q(1,3),Q(2,5),Q(7,11),Q(5,13),Q(3,2)]
    for s in (3,5,7,9):
        fields=[tuple(sum((weights[j]*kernel(minus(x,points[j]),s)[k]
                            for j in range(5) if j!=i),Q(0)) for k in range(3))
                for i,x in enumerate(points)]
        rhs=sum((weights[i]*weights[j]*dot(minus(points[i],points[j]),minus(points[i],points[j]))**((1-s)//2)
                 for i in range(5) for j in range(i)),Q(0))
        for a in ((Q(0),)*3,(Q(-2),Q(5),Q(7)),(Q(1,2),Q(-3,7),Q(9,11))):
            lhs=sum((weights[i]*dot(minus(x,a),fields[i]) for i,x in enumerate(points)),Q(0))
            check(lhs==rhs,'vector_moment','three dimensional antisymmetric moment')
    def permutation_sum(pts,s):
        return sum((dot(kernel(minus(pts[i],pts[(i+1)%3]),s),
                        kernel(minus(pts[i],pts[(i+2)%3]),s)) for i in range(3)),Q(0))
    for s in (3,5,7,9):
        eq=((Q(0),Q(0),Q(0)),(Q(1),Q(1),Q(0)),(Q(1),Q(0),Q(1)))
        check(permutation_sum(eq,s)==Q(3,2*2**s),'three_point','equilateral Euclidean geometry')
        for t in range(2,19):
            pts=((Q(0),)*3,(Q(1),Q(0),Q(0)),(Q(t),Q(0),Q(0)))
            check(permutation_sum(pts,s)==Q((t-1)**s-t**s+1,t**s*(t-1)**s)<0,
                  'three_point','collinear Euclidean geometry')
    for s in (2,3,4):
        for N in range(1,13):
            radii=[Q(1,2**j) for j in range(1,N+1)]
            for numerator in (1,3,5,7,11):
                for power in range(0,16):
                    r=Q(numerator,3*2**power)
                    outside=sum((r/a for a in radii if a>=r),Q(0))
                    inside=sum(((a/r)**s for a in radii if a<r),Q(0))
                    check(outside<=2 and inside<=1/(1-Q(1,2**s)),
                          'off_dyadic_shell_sum','non-dyadic evaluation radius')
    for i in range(-20,21):
        for j in range(-20,21):
            w1,w2=Q(i,40),Q(j,40)
            if w1*w1+w2*w2<=Q(1,4):
                num=1-w1;normsq=num*num+w2*w2
                check(num>0 and 9*num*num>=normsq and num*num<=normsq,
                      'boundary_ratio','closed half disk projection ratio')
    return count

def invoke(root,script,mode,args=(),cwd=None):
    flags=['-I','-B']+([mode] if mode else [])
    return subprocess.run([sys.executable,*flags,str(root/script),*map(str,args)],
                          capture_output=True,cwd=cwd,check=False)

def passed(proc,label):
    require(proc.returncode==0 and not proc.stderr,label+' did not pass cleanly')
    result=json.loads(proc.stdout);require(result['result']=='PASS',label+' wrong disposition')
    return result

def failed(proc,label):
    require(proc.returncode==2 and not proc.stderr,label+' did not fail cleanly')
    require(json.loads(proc.stdout)['result']=='FAIL',label+' wrong rejection disposition')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--packet',type=Path,required=True)
    args=ap.parse_args();root=args.packet.resolve()
    before=inventory(root)
    require(sha((root/'MANIFEST.json').read_bytes())==PIN,'external pin mismatch')
    for name in ('check_math.py','verify_packet.py','run_controls.py'):
        require(not any(isinstance(node,ast.Assert) for node in ast.walk(ast.parse((root/name).read_text()))),
                'optimization-sensitive assertion statement')
    math_counts=mathematical_checks()
    counts={'positive_replays':0,'wrong_claim_rejections':0,'malformed_claim_rejections':0,
            'integrity_rejections':0,'read_only_relocations':0,'read_only_write_denials':0}
    expected=(root/'CHECKS.expected.json').read_bytes()
    original_claims=json.loads((root/'CLAIMS.json').read_text())
    wrong=[]
    for path,value in [(('status',),'solved'),(('author_turns',),6),
        (('original_inequality_proved',),True),(('original_inequality_disproved',),True),
        (('original_inequality_disproved',),0),(('target','norm'),'one component'),
        (('target','density'),'signed smooth'),(('target','support'),'nonzero density set'),
        (('latitude','hessian_parallel'),'8/3'),(('latitude','hessian_transverse'),'4/147'),
        (('latitude','global_counterexample'),True),(('flat_model','admissible_target_density'),True),
        (('flat_model','smooth_support_boundary_layer_survives'),False)]:
        obj=copy.deepcopy(original_claims);target=obj
        for key in path[:-1]:target=target[key]
        target[path[-1]]=value;wrong.append(json.dumps(obj).encode())
    malformed=[b'{',b'[]',b'null',b'"text"',b'{"a":NaN}',b'{"a":Infinity}',
               b'{"problem_id":30003536,"problem_id":30003536}',b'\xff']
    mutants=('bad_pin','changed_payload','missing_payload','extra_directory','payload_symlink',
             'manifest_symlink','malformed_json','list_manifest','duplicate_json_key','nonfinite_json',
             'absolute_path','traversal','nested_path','duplicate_path','bool_bytes','bad_digest',
             'extra_row_key','empty_files','missing_required')
    with tempfile.TemporaryDirectory(prefix='riesz-independent-audit-') as temporary:
        tmp=Path(temporary)
        fixture=tmp/'outside';fixture.write_text('fixture\n')
        for mode in ('','-O','-OO'):
            good=invoke(root,'check_math.py',mode,cwd=tmp)
            passed(good,'original math');require(good.stdout==expected,'nonidentical math stdout')
            counts['positive_replays']+=1
            passed(invoke(root,'verify_packet.py',mode,('--expected-manifest-sha256',PIN),tmp),'original integrity')
            counts['positive_replays']+=1
            for collection,key in ((wrong,'wrong_claim_rejections'),(malformed,'malformed_claim_rejections')):
                for raw in collection:
                    fp=tmp/'claim.json';fp.write_bytes(raw)
                    failed(invoke(root,'check_math.py',mode,('--claims',fp),tmp),key)
                    counts[key]+=1
            for kind in mutants:
                clone=tmp/'mutant';shutil.copytree(root,clone)
                clone.chmod(0o755)
                for p in clone.iterdir():p.chmod(0o644)
                pin=PIN
                manifest=clone/'MANIFEST.json'
                if kind=='bad_pin':pin='0'*64
                elif kind=='changed_payload':(clone/'REPORT.md').write_bytes((clone/'REPORT.md').read_bytes()+b'\nchanged\n')
                elif kind=='missing_payload':(clone/'REPORT.md').unlink()
                elif kind=='extra_directory':(clone/'extra').mkdir()
                elif kind=='payload_symlink':(clone/'REPORT.md').unlink();(clone/'REPORT.md').symlink_to(fixture)
                elif kind=='manifest_symlink':
                    saved=tmp/'manifest-copy';saved.write_bytes(manifest.read_bytes());manifest.unlink();manifest.symlink_to(saved)
                else:
                    doc=json.loads(manifest.read_text())
                    if kind=='malformed_json':raw=b'{'
                    elif kind=='list_manifest':raw=b'[]'
                    elif kind=='duplicate_json_key':raw=b'{"format":"riesz-author-packet-v1","format":"riesz-author-packet-v1","files":[]}'
                    elif kind=='nonfinite_json':raw=b'{"format":"riesz-author-packet-v1","files":NaN}'
                    else:
                        if kind=='absolute_path':doc['files'][0]['path']='/tmp/outside'
                        elif kind=='traversal':doc['files'][0]['path']='../outside'
                        elif kind=='nested_path':doc['files'][0]['path']='nested/payload'
                        elif kind=='duplicate_path':doc['files'].append(copy.deepcopy(doc['files'][0]))
                        elif kind=='bool_bytes':doc['files'][0]['bytes']=True
                        elif kind=='bad_digest':doc['files'][0]['sha256']='G'*64
                        elif kind=='extra_row_key':doc['files'][0]['unexpected']=1
                        elif kind=='empty_files':doc['files']=[]
                        elif kind=='missing_required':
                            doc['files']=[row for row in doc['files'] if row['path']!='REPORT.md'];(clone/'REPORT.md').unlink()
                        raw=json.dumps(doc).encode()
                    manifest.write_bytes(raw);pin=sha(raw)
                failed(invoke(clone,'verify_packet.py',mode,('--expected-manifest-sha256',pin),tmp),kind)
                counts['integrity_rejections']+=1
                shutil.rmtree(clone)
            clone=tmp/'readonly';shutil.copytree(root,clone)
            frozen=inventory(clone)
            for p in clone.iterdir():p.chmod(0o444)
            clone.chmod(0o555)
            try:
                # Verify actual denied writes, not mode bits alone. This test
                # intentionally fails if run with privileges bypassing chmod.
                for path,new in ((clone/'newfile',True),(clone/'REPORT.md',False)):
                    try:
                        with path.open('ab') as out:out.write(b'write probe')
                    except PermissionError:counts['read_only_write_denials']+=1
                    else:raise Failure('read-only fixture permits writes')
                passed(invoke(clone,'verify_packet.py',mode,('--expected-manifest-sha256',PIN),tmp),'read-only relocation')
                require(inventory(clone)==frozen,'read-only payload changed')
                counts['read_only_relocations']+=1
            finally:
                clone.chmod(0o755)
                for p in clone.iterdir():p.chmod(0o644)
                shutil.rmtree(clone)
    require(inventory(root)==before,'author packet changed')
    return {'result':'PASS','problem_id':30003536,'author_manifest_sha256':PIN,
            'python_modes':['normal','-O','-OO'],'independent_mathematical_checks':math_counts,
            'independent_mathematical_check_total':sum(math_counts.values()),'replay_controls':counts,
            'author_expected_check_total':json.loads(expected)['total_checks'],
            'author_packet_unchanged':True,'source_files_copied':False,
            'analytic_proof_certified_by_computation':False,'external_writes':False,
            'read_only_fixture_test':'actual append and creation attempts rejected with PermissionError'}

if __name__=='__main__':
    try:
        output=main()
        print(json.dumps(output,indent=2,sort_keys=True))
    except (Failure,OSError,ValueError,TypeError,KeyError) as exc:
        print(json.dumps({'result':'FAIL','error':str(exc)},sort_keys=True))
        sys.exit(2)
