#!/usr/bin/env python3
"""Exact, bounded checks. This is not a formal proof of the all-genus target."""
from fractions import Fraction as F
from itertools import product, combinations
from math import isqrt
from pathlib import Path
import argparse, hashlib, json, re, tempfile, shutil

ASSERTIONS = 0

def check(condition, message):
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        raise AssertionError(message)

def det(a):
    a = [[F(x) for x in row] for row in a]
    r = F(1)
    for j in range(len(a)):
        p = next((i for i in range(j, len(a)) if a[i][j]), None)
        if p is None:
            return F(0)
        if p != j:
            a[j], a[p] = a[p], a[j]
            r = -r
        pivot = a[j][j]
        r *= pivot
        for i in range(j+1, len(a)):
            ratio = a[i][j]/pivot
            for k in range(j+1, len(a)):
                a[i][k] -= ratio*a[j][k]
    return r

def spd(q):
    n = len(q)
    return (n > 0 and all(len(row) == n for row in q)
            and all(q[i][j] == q[j][i] for i in range(n) for j in range(n))
            and all(det([row[:k] for row in q[:k]]) > 0 for k in range(1,n+1)))

def qvalue(q, v):
    return sum(F(v[i])*q[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))

def outer(v):
    return [[F(x)*y for y in v] for x in v]

def unit(n,i):
    return tuple(int(i==j) for j in range(n))

def fs_coedges(n):
    return [(2,)+(-1,)*(n-1)]+[unit(n,i) for i in range(1,n)]

def fs_metric(n):
    return [[F(n,4) if i==j==0 else F(1) if i==j else F(1,2) if i==0 or j==0 else F(0)
             for j in range(n)] for i in range(n)]

def certify(q, coedges, lam):
    n=len(q); lam=F(lam)
    if lam<=0 or not spd(q):
        raise ValueError('positive definiteness or lower bound missing')
    lower=[[F(q[i][j])-(lam if i==j else 0) for j in range(n)] for i in range(n)]
    if not spd(lower):
        raise ValueError('strict rational spectral lower bound invalid')
    if not all(qvalue(q,v)==1 for v in coedges):
        raise ValueError('coedge equality failed')
    reciprocal=1/lam
    bound=isqrt(reciprocal.numerator//reciprocal.denominator)
    points=0; minimum=None
    for z in product(range(-bound,bound+1), repeat=n):
        if not any(z): continue
        points+=1
        value=qvalue(q,z)
        if minimum is None or value<minimum: minimum=value
        if value<1:
            raise ValueError('short vector: '+str(z))
    return {'rank':n,'lambda':str(lam),'box_bound':bound,'nonzero_points':points,'minimum_in_box':str(minimum)}

def connected(n, edges, vertices=None):
    vertices=set(range(n)) if vertices is None else set(vertices)
    if not vertices: return False
    seen={min(vertices)}
    while True:
        old=len(seen)
        for a,b in edges:
            if a in vertices and b in vertices:
                if a in seen: seen.add(b)
                if b in seen: seen.add(a)
        if len(seen)==old: return seen==vertices

def cut_mask(edges, subset):
    return sum(1<<i for i,(a,b) in enumerate(edges) if ((a in subset)!=(b in subset)))

def graph_analysis(n, edges):
    if not connected(n,edges): raise ValueError('graph must be connected')
    code={cut_mask(edges,{i for i in range(n) if s>>i&1}) for s in range(1<<n)}
    bridges={i for i in range(len(edges)) if not connected(n,edges[:i]+edges[i+1:])}
    bridge_mask=sum(1<<i for i in bridges)
    check({i for i in range(len(edges)) if (1<<i) in code}==bridges,'singleton cut normalization')
    code0={c & ~bridge_mask for c in code}
    check(code0 <= code,'subtracting singleton bridge words must stay in cut code')
    check(all(c.bit_count()!=1 for c in code0),'reduced code has no singleton')
    bad_words={c for c in code0 if c.bit_count() in (2,3)}
    bad_bonds=set()
    for s in range(1,1<<n):
        shore={i for i in range(n) if s>>i&1}
        other=set(range(n))-shore
        c=cut_mask(edges,shore)
        if c.bit_count() in (2,3) and connected(n,edges,shore) and connected(n,edges,other):
            bad_bonds.add(c)
    check(bad_words==bad_bonds,'short cut words and small bonds differ')
    check(len(code)==1<<(n-1),'connected cut code dimension')
    check(len(code0)*(1<<len(bridges))==len(code),'integral bridge factorization')
    positive=not bad_words
    code_min=min((c.bit_count() for c in code0 if c),default=None)
    return {'vertices':n,'edges':len(edges),'bridges':len(bridges),'cut_code_size':len(code),
            'reduced_min_weight':code_min,'small_bonds':len(bad_bonds),'extends_in_restricted_class':positive}

def verify_math():
    # Universal identities are proved in RESEARCH.md; these checks exercise instances.
    fs=[]
    for n in range(2,9):
        coedges=fs_coedges(n);q=fs_metric(n)
        check(abs(det(coedges))==2,'FS determinant')
        check(det(q)==F(1,4) and spd(q),'FS metric determinant or SPD')
        check(all(qvalue(q,v)==1 for v in coedges),'FS coedge equalities')
        for omitted in range(n):
            rows=[v for j,v in enumerate(coedges) if j!=omitted]
            rows.append(unit(n,0))
            check(abs(det(rows))==1,'proper FS coedge face not primitive')
        total=[[F(0) for _ in range(n)] for _ in range(n)]
        values=[]
        for signs in product((-1,1),repeat=n):
            w=(signs[0],)+tuple((signs[j]-signs[0])//2 for j in range(1,n))
            check(any(w),'sign vector unexpectedly zero')
            o=outer(w)
            for i in range(n):
                for j in range(n): total[i][j]+=o[i][j]
            values.append(qvalue(q,w))
        expected=[[sum(outer(v)[i][j] for v in coedges)/4 for j in range(n)] for i in range(n)]
        check(all(total[i][j]/(1<<n)==expected[i][j] for i in range(n) for j in range(n)), 'dual averaging identity')
        check(all(v==F(n,4) for v in values),'Euclidean half-coset values')
        check((F(n,4)<1)==(n in (2,3)),'FS threshold')
        fs.append({'n':n,'coedge_index':2,'half_coset_value':str(F(n,4)), 'perfect_extension':n>=4})
    finite_certificates={}
    finite_certificates['FS4']=certify(fs_metric(4),fs_coedges(4),F(1,16))
    u=(1,0);v=(0,1);plus=(1,1);minus=(1,-1);a=(2,-1)
    qplus=[[F(1),F(-1,2)],[F(-1,2),F(1)]]
    qminus=[[F(1),F(1,2)],[F(1,2),F(1)]]
    qsecond=[[F(1),F(3,2)],[F(3,2),F(3)]]
    finite_certificates['overlap_plus']=certify(qplus,[u,v,plus],F(1,4))
    finite_certificates['overlap_minus_and_subdivision_C1']=certify(qminus,[u,v,minus],F(1,4))
    finite_certificates['subdivision_C2']=certify(qsecond,[a,u,minus],F(1,8))
    check(all(outer(plus)[i][j]+outer(minus)[i][j]==2*outer(u)[i][j]+2*outer(v)[i][j]
              for i in range(2) for j in range(2)),'parallelogram identity')
    check(all((outer(a)[i][j]+outer(v)[i][j])/2==outer(u)[i][j]+outer(minus)[i][j]
              for i in range(2) for j in range(2)),'subdivision ray identity')
    # Two passing systems cannot be mistaken for a passing union.
    rejected=[]
    for name,q,rays,lam in [
        ('FS2 candidate has short vectors',fs_metric(2),fs_coedges(2),F(1,16)),
        ('FS3 candidate has short vectors',fs_metric(3),fs_coedges(3),F(1,16)),
        ('overlap union fails',qplus,[u,v,plus,minus],F(1,4)),
        ('wrong lower bound fails',qplus,[u,v,plus],F(2)),
        ('nonsymmetric matrix fails',[[F(1),F(0)],[F(1),F(1)]],[u,v],F(1,4)),
        ('mutated FS4 coedge fails',fs_metric(4),fs_coedges(4)+[(1,0,0,1)],F(1,16))]:
        try: certify(q,rays,lam)
        except ValueError: rejected.append(name)
        else: raise AssertionError('negative control accepted: '+name)
    counts={}; positives={}; total_graphs=0
    for n in range(1,6):
        possible=list(combinations(range(n),2)); count=positive=0
        for bits in range(1<<len(possible)):
            edges=[e for i,e in enumerate(possible) if bits>>i&1]
            if not connected(n,edges): continue
            result=graph_analysis(n,edges); count+=1;positive+=result['extends_in_restricted_class']
        counts[str(n)]=count;positives[str(n)]=positive;total_graphs+=count
    check(counts=={'1':1,'2':1,'3':4,'4':38,'5':728},'labelled graph enumeration counts')
    fixtures={}
    for n in range(1,13):
        result=graph_analysis(2,[(0,1)]*n)
        check(result['extends_in_restricted_class']==(n not in (2,3)),'FS multigraph classification')
        fixtures['FS'+str(n)]=result
    k5=list(combinations(range(5),2))
    fixtures['K5']=graph_analysis(5,k5)
    check(fixtures['K5']['extends_in_restricted_class'] and fixtures['K5']['reduced_min_weight']==4,'K5 expected positive')
    fixtures['K5_with_bridge_and_loop']=graph_analysis(6,k5+[(4,5),(2,2)])
    check(fixtures['K5_with_bridge_and_loop']['extends_in_restricted_class'],'bridge/loop should not obstruct')
    fixtures['two_triangles_wedge']=graph_analysis(5,[(0,1),(1,2),(2,0),(0,3),(3,4),(4,0)])
    check(not fixtures['two_triangles_wedge']['extends_in_restricted_class'],'small bonds should obstruct wedge')
    return {'scope':'Bounded exact checks, not a formal proof or a complete admissible-cover enumeration.',
            'fs_checks':fs,'finite_certificates':finite_certificates,
            'connected_labelled_simple_graphs_by_vertices':counts,
            'extending_graphs_in_restricted_class_by_vertices':positives,
            'total_graphs':total_graphs,'fixtures':fixtures,
            'mathematical_negative_controls_rejected':rejected,
            'assertions':ASSERTIONS}

EXPECTED_FILES={'README.md','RESEARCH.md','RESEARCH_LOG.md','STATUS.json','SOURCE_VERIFICATION.json',
                'PRIOR_ATTEMPT_CHECK.md','verify.py','verification_results.json'}

def verify_manifest(root):
    manifest_path=root/'MANIFEST.json'
    if manifest_path.is_symlink(): raise ValueError('manifest symlink')
    data=json.loads(manifest_path.read_text())
    if set(data)!={'schema','files'} or data['schema']!='prym-safe-manifest-v1':
        raise ValueError('manifest schema')
    records=data['files']
    if not isinstance(records,list): raise ValueError('manifest records not list')
    names=[]
    for r in records:
        if set(r)!={'path','bytes','sha256'}: raise ValueError('record schema')
        p=r['path']; names.append(p)
        if not isinstance(p,str) or p not in EXPECTED_FILES: raise ValueError('unapproved or unsafe path')
        if type(r['bytes']) is not int or r['bytes']<0: raise ValueError('invalid byte count')
        if not isinstance(r['sha256'],str) or re.fullmatch('[0-9a-f]{64}',r['sha256']) is None:
            raise ValueError('invalid hash')
        target=root/p
        if target.is_symlink() or not target.is_file(): raise ValueError('nonregular file')
        b=target.read_bytes()
        if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:
            raise ValueError('file integrity mismatch: '+p)
    if len(set(names))!=len(names) or set(names)!=EXPECTED_FILES: raise ValueError('manifest file set')
    actual={p.name for p in root.iterdir()}
    if actual!=EXPECTED_FILES|{'MANIFEST.json'}: raise ValueError('unexpected or missing object')
    status=json.loads((root/'STATUS.json').read_text())
    if status['problem_id']!='30002653' or status['outcome']!='unsolved' or status['approach_families_completed']!=5:
        raise ValueError('status guard')
    return hashlib.sha256(manifest_path.read_bytes()).hexdigest()

def integrity_negative_controls(root):
    rejected=[]
    mutations={
      'changed_byte':lambda p:(p/'RESEARCH.md').write_bytes((p/'RESEARCH.md').read_bytes()+b'\n'),
      'extra_file':lambda p:(p/'source.pdf').write_bytes(b'not allowed'),
      'missing_file':lambda p:(p/'README.md').unlink(),
      'symlink':lambda p:((p/'README.md').unlink(),(p/'README.md').symlink_to('RESEARCH.md')),
    }
    def change_record(p,kind):
        m=json.loads((p/'MANIFEST.json').read_text())
        if kind=='path_traversal':m['files'][0]['path']='../RESEARCH.md'
        elif kind=='duplicate_record':m['files'].append(m['files'][0])
        elif kind=='boolean_size':m['files'][0]['bytes']=True
        elif kind=='wrong_hash':m['files'][0]['sha256']='0'*64
        (p/'MANIFEST.json').write_text(json.dumps(m))
    for k in ('path_traversal','duplicate_record','boolean_size','wrong_hash'):
        mutations[k]=lambda p,k=k:change_record(p,k)
    for name,mutation in mutations.items():
        with tempfile.TemporaryDirectory(prefix='prym-negative-') as d:
            p=Path(d)/'packet';shutil.copytree(root,p)
            mutation(p)
            try:verify_manifest(p)
            except (ValueError,FileNotFoundError):rejected.append(name)
            else:raise AssertionError('integrity negative accepted: '+name)
    return rejected

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write-results',action='store_true')
    parser.add_argument('--skip-manifest',action='store_true')
    args=parser.parse_args();root=Path(__file__).resolve().parent
    result=verify_math()
    if args.write_results:
        (root/'verification_results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        saved=json.loads((root/'verification_results.json').read_text())
        if result!=saved:raise AssertionError('mathematical replay differs from saved result')
    output={'mathematical_checks':'PASS','assertions':ASSERTIONS,'total_graphs':result['total_graphs']}
    if not args.skip_manifest:
        output['manifest_sha256']=verify_manifest(root)
        output['integrity_negative_controls_rejected']=integrity_negative_controls(root)
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
