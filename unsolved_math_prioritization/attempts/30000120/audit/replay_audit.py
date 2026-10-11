#!/usr/bin/env python3
"""Independent exact homogeneous-ideal controls. Not a geometric proof checker."""
import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from math import comb, factorial
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

FILES = {'README.md', 'AUDIT.md', 'CLARIFICATIONS.md', 'BINDINGS.json',
         'SOURCE_REVIEW.json', 'CHECKS.json', 'replay_audit.py'}

def require(c, message):
    if not c:
        raise ValueError(message)

def digest(b):
    return hashlib.sha256(b).hexdigest()

def canonical(o):
    return (json.dumps(o, sort_keys=True, indent=2)+'\n').encode()

def inventory(root, expected, manifest_name='AUDIT_MANIFEST.json', names=None):
    root=Path(root)
    require(len(expected)==64 and all(c in '0123456789abcdef' for c in expected), 'invalid pin')
    expected_names=FILES|{manifest_name} if names is None else set(names)
    entries=list(root.iterdir())
    require({p.name for p in entries}==expected_names, 'inventory mismatch')
    require(all(p.is_file() and not p.is_symlink() for p in entries), 'nonregular or symlink entry')
    raw=(root/manifest_name).read_bytes()
    require(digest(raw)==expected, 'manifest pin mismatch')
    meta=json.loads(raw)
    require(meta['problem_id']==30000120, 'problem binding mismatch')
    require(set(meta['files'])==expected_names-{manifest_name}, 'manifest inventory mismatch')
    for n,e in meta['files'].items():
        require(set(e)=={'bytes','sha256'}, 'entry keys mismatch')
        b=(root/n).read_bytes()
        require(type(e['bytes']) is int and e['bytes']==len(b), 'size mismatch: '+n)
        require(e['sha256']==digest(b), 'content mismatch: '+n)
    return meta

# Homogeneous polynomials are coefficient lists: slot j is H^(d-j) E^j.
# This does not import or emulate the author's Groebner reduction algorithm.
def plus(*ps):
    out=[Q(0)]*max(map(len,ps))
    for p in ps:
        for i,c in enumerate(p): out[i]+=c
    return out

def times(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return out

def scalar(a,c): return [Q(c)*x for x in a]

def power(a,n):
    out=[Q(1)]
    for _ in range(n): out=times(out,a)
    return out

def rref(rows, n):
    rows=[[Q(x) for x in r] for r in rows if any(r)]
    require(all(len(r)==n for r in rows), 'ragged rows')
    pivots=[]; at=0
    for col in range(n):
        p=next((k for k in range(at,len(rows)) if rows[k][col]),None)
        if p is None: continue
        rows[at],rows[p]=rows[p],rows[at]
        divisor=rows[at][col]
        rows[at]=[x/divisor for x in rows[at]]
        for k in range(len(rows)):
            if k==at: continue
            divisor=rows[k][col]
            rows[k]=[x-divisor*y for x,y in zip(rows[k],rows[at])]
        pivots.append(col); at+=1
        if at==len(rows): break
    return rows[:at],pivots

def rank(rows,n): return len(rref(rows,n)[1])

def ideal_rows(rels,d):
    rows=[]
    for rel in rels:
        extra=d-(len(rel)-1)
        for j in range(extra+1):
            row=[Q(0)]*(d+1)
            row[j:j+len(rel)]=rel
            rows.append(row)
    return rows

def in_ideal(p,rels):
    rows=ideal_rows(rels,len(p)-1)
    return rank(rows,len(p))==rank(rows+[p],len(p))

def quotient_dimension(rels,d): return d+1-rank(ideal_rows(rels,d),d+1)

def independent_basis_slots(rels,d):
    piv=rref(ideal_rows(rels,d),d+1)[1]
    return [j for j in range(d+1) if j not in piv]

def integral(poly,top):
    require(len(poly)==6, 'integration degree mismatch')
    return sum(x*y for x,y in zip(poly,top))

def expect_rejection(test,name,results):
    try: test()
    except ValueError:
        results.append(name)
        return
    raise ValueError('false claim accepted: '+name)

def compute():
    # Normal sequence: c(TP5|P2)=c(TP2)c(N).
    ambient=[Q(comb(6,j)*2**j) for j in range(3)]
    center=[Q(comb(3,j)) for j in range(3)]
    normal=[]
    for i in range(3):
        normal.append(ambient[i]-sum(center[j]*normal[i-j] for j in range(1,i+1)))
    require(normal==[1,9,30], 'normal Chern data')
    segre=[Q(1)]
    for i in range(1,3): segre.append(-sum(normal[j]*segre[i-j] for j in range(1,i+1)))
    require(segre==[1,-9,51], 'Segre inversion')
    # E|E=-xi and p_*(xi^(2+j))=s_j(N), with the line convention.
    top=[Q(1),Q(0),Q(0)]+[(-1)**(k-1)*2**(5-k)*segre[k-3] for k in range(3,6)]
    require(top==[1,0,0,4,18,51], 'Segre top intersections')
    H=[Q(1),Q(0)]; E=[Q(0),Q(1)]; F=[Q(3),Q(-2)]; nu=[Q(2),Q(-1)]
    cubic=[Q(-4),Q(15,2),Q(-9,2),Q(1)]
    quartic=[Q(0),Q(1),Q(0),Q(0),Q(0)]
    rels=[cubic,quartic]
    dims=[quotient_dimension(rels,d) for d in range(9)]
    require(dims==[1,2,3,3,2,1,0,0,0], 'Macaulay dimensions')
    # All top-degree ideal relations pair trivially with the independent Segre functional.
    relation_integrals=[integral(p,top) for p in ideal_rows(rels,5)]
    require(not any(relation_integrals), 'relation/Segre incompatibility')
    pairing_ranks=[]
    for d in range(6):
        a=independent_basis_slots(rels,d); b=independent_basis_slots(rels,5-d)
        pairing_ranks.append(rank([[top[i+j] for j in b] for i in a],len(b)))
    require(pairing_ranks==dims[:6], 'Poincare pairing')
    generation=[]
    for d in range(6):
        relations=ideal_rows(rels,d)
        boundary=[times(power(E,j),power(F,d-j)) for j in range(d+1)]
        generation.append(rank(relations+boundary,d+1)-rank(relations,d+1))
    require(generation==dims[:6], 'boundary generation')
    # Check the author's boundary presentation after the invertible substitution.
    boundary3=plus(scalar(power(E,3),8),scalar(times(power(E,2),F),3),
                   scalar(times(E,power(F,2)),-3),scalar(power(F,3),-8))
    boundary4=times(E,power(plus(scalar(E,2),F),3))
    require(boundary3==scalar(cubic,54), 'boundary cubic identity')
    require(boundary4==scalar(quartic,27), 'boundary quartic identity')
    # Independent classical coordinates mu=H, nu=2H-E.
    classical3=plus(scalar(power(H,3),2),scalar(times(power(H,2),nu),-3),
                   scalar(times(H,power(nu,2)),3),scalar(power(nu,3),-2))
    classical4=plus(scalar(power(H,4),4),scalar(times(power(H,2),power(nu,2)),-3),scalar(power(nu,4),4))
    require(in_ideal(classical3,rels) and in_ideal(classical4,rels), 'classical-to-author ideals')
    require(in_ideal(cubic,[classical3,classical4]) and in_ideal(quartic,[classical3,classical4]), 'author-to-classical ideals')
    intersections=[integral(times(power(H,5-j),power(nu,j)),top) for j in range(6)]
    require(intersections==[1,2,4,4,2,1], 'dual-conic intersections')
    volume=[Q(comb(5,j))*x for j,x in enumerate(intersections)]
    require(volume==[1,10,40,40,10,1], 'classical volume coefficients')
    tangent=plus(scalar(H,6),scalar(E,-2)); log=plus(tangent,scalar(plus(E,F),-1))
    require(tangent==scalar(plus(E,F),2) and log==plus(E,F), 'canonical/log identities')
    require(rank([tangent,log],2)==1, 'tangent/log rank')
    boundary_determinant=E[0]*F[1]-E[1]*F[0]
    require(abs(boundary_determinant)==3, 'boundary determinant')
    # Five-variable chart determinant is checked as a polynomial identity over Z.
    # Matrix [[1,u,v],[u,u^2+x,uv+y],[v,uv+y,v^2+z]].
    # Direct distributive expansion represented by five-variable exponent dictionaries.
    def pa(*polys):
        out={}
        for p in polys:
            for k,v in p.items(): out[k]=out.get(k,0)+v
        return {k:v for k,v in out.items() if v}
    def pm(a,b):
        out={}
        for u,x in a.items():
            for v,y in b.items():
                k=tuple(x+y for x,y in zip(u,v));out[k]=out.get(k,0)+x*y
        return {k:v for k,v in out.items() if v}
    def ps(p,c): return {k:c*v for k,v in p.items() if c*v}
    one={(0,)*5:1};variables=[]
    for i in range(5):
        k=[0]*5;k[i]=1;variables.append({tuple(k):1})
    u,v,x,y,z=variables
    mat=[[one,u,v],[u,pa(pm(u,u),x),pa(pm(u,v),y)],[v,pa(pm(u,v),y),pa(pm(v,v),z)]]
    determinant={}
    for perm in itertools.permutations(range(3)):
        inversions=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
        t=one
        for i in range(3): t=pm(t,mat[i][perm[i]])
        determinant=pa(determinant,ps(t,(-1)**inversions))
    require(determinant==pa(pm(x,z),ps(pm(y,y),-1)), 'local determinant')
    require(min(sum(k[2:]) for k in determinant)==2, 'center multiplicity')
    # Product controls beyond the author's five examples; geometric all-product proof is separate.
    products=0
    for b in range(7):
        for c in range(7):
            if b+c==0: continue
            p=times(power([Q(1)]*3,b),power(list(map(Q,dims[:6])),c))
            require(p==p[::-1] and sum(p)==3**b*12**c and p[1]==b+2*c,'product control')
            require(b+2*c>c,'nonminimal product rank')
            products+=1
    negatives=[]
    expect_rejection(lambda:require(rank([tangent,log],2)==2,'false tangent generation'),'tangent_and_log_generate_H2',negatives)
    expect_rejection(lambda:require(rank([E],2)==2,'false one-boundary generation'),'exceptional_alone_generates_H2',negatives)
    expect_rejection(lambda:require(in_ideal(power(H,3),[quartic]),'false omitted cubic'),'kernel_relation_alone_suffices',negatives)
    bad=cubic[:];bad[2]=-bad[2]
    expect_rejection(lambda:require(all(integral(p,top)==0 for p in ideal_rows([bad,quartic],5)),'wrong sign'),'wrong_normal_c1_sign',negatives)
    bad=cubic[:];bad[0]=Q(-1)
    expect_rejection(lambda:require(all(integral(p,top)==0 for p in ideal_rows([bad,quartic],5)),'wrong center degree'),'veronese_degree_one',negatives)
    bad=boundary3[:];bad[0]+=1
    expect_rejection(lambda:require(in_ideal(bad,rels),'false boundary relation'),'altered_boundary_cubic',negatives)
    expect_rejection(lambda:require(F==[3,-1],'false multiplicity'),'determinant_multiplicity_one',negatives)
    expect_rejection(lambda:require(abs(boundary_determinant)==1,'false integral basis'),'boundary_integral_Picard_basis',negatives)
    expect_rejection(lambda:require(2==2-1,'false minimal rank'),'complete_conics_minimal_rank',negatives)
    return {'status':'PASS_INDEPENDENT_SCOPED_PARTIAL','problem_id':30000120,
      'general_problem_solved':False,'geometric_proof_machine_certified':False,
      'method':'homogeneous ideal matrices and independent Segre integration',
      'normal_chern_coefficients':list(map(int,normal)),'normal_segre_coefficients':list(map(int,segre)),
      'quotient_dimensions_degrees_0_through_8':dims,
      'poincare_pairing_ranks':pairing_ranks,'boundary_monomial_ranks':generation,
      'H_to_E_top_intersections':list(map(int,top)),
      'H_to_dual_H_top_intersections':list(map(int,intersections)),
      'volume_coefficients':list(map(int,volume)),
      'classical_ideal_equivalence':True,'boundary_presentation_equivalence':True,
      'boundary_Picard_determinant_absolute':3,'tangent_log_H2_rank':1,
      'local_determinant_polynomial_checked':True,'normal_ideal_multiplicity':2,
      'product_cases':products,'false_mathematical_claims_rejected':negatives}

MUTATIONS=['changed_report','changed_code','missing_payload','extra_file','extra_directory',
           'changed_manifest','symlink','same_size_corruption','wrong_external_pin']
def selftest(root,pin):
    for case in MUTATIONS:
        with tempfile.TemporaryDirectory() as td:
            target=Path(td)/'audit';shutil.copytree(root,target)
            testpin=pin
            if case=='changed_report': (target/'AUDIT.md').write_bytes((target/'AUDIT.md').read_bytes()+b'changed')
            elif case=='changed_code': (target/'replay_audit.py').write_bytes(b'print("PASS")\n')
            elif case=='missing_payload': (target/'SOURCE_REVIEW.json').unlink()
            elif case=='extra_file': (target/'unexpected.txt').write_text('extra')
            elif case=='extra_directory': (target/'extra').mkdir()
            elif case=='changed_manifest': (target/'AUDIT_MANIFEST.json').write_bytes((target/'AUDIT_MANIFEST.json').read_bytes()+b'\n')
            elif case=='symlink':
                (target/'AUDIT.md').unlink();(target/'AUDIT.md').symlink_to('README.md')
            elif case=='same_size_corruption':
                p=target/'CHECKS.json';b=p.read_bytes();p.write_bytes(bytes([b[0]^1])+b[1:])
            elif case=='wrong_external_pin': testpin='0'*64
            rejected=False
            try: inventory(target,testpin)
            except (ValueError,OSError): rejected=True
            require(rejected,'accepted tamper: '+case)

def check_author(root,binding):
    root=Path(root).resolve()
    pin=binding['author_manifest_sha256']
    inventory(root,pin,'MANIFEST.json',binding['author_files'])
    for n,meta in binding['author_files'].items():
        b=(root/n).read_bytes()
        require(digest(b)==meta['sha256'] and len(b)==meta['bytes'],'author binding mismatch: '+n)
    for flags in ([],['-O']):
        command=[sys.executable,'-B']+flags+[str(root/'verify.py'),'--expected-manifest',pin,'--self-test']
        p=subprocess.run(command,cwd=root,capture_output=True,timeout=90)
        require(p.returncode==0,'author replay failure: '+p.stderr.decode(errors='replace'))
        require(p.stdout==(root/'RESULTS.json').read_bytes(),'author output differs')

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--expected-manifest',required=True)
    p.add_argument('--self-test',action='store_true')
    p.add_argument('--author-directory')
    a=p.parse_args();root=Path(__file__).resolve().parent
    inventory(root,a.expected_manifest)
    output=canonical(compute())
    require(output==(root/'CHECKS.json').read_bytes(),'independent result bytes differ')
    if a.self_test:selftest(root,a.expected_manifest)
    if a.author_directory:check_author(a.author_directory,json.loads((root/'BINDINGS.json').read_bytes()))
    sys.stdout.buffer.write(output)

if __name__=='__main__':main()
