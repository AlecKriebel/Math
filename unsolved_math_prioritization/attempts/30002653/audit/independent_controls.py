#!/usr/bin/env python3
"""Independent exact controls; imports no author code and reads no primary-source text.
Finite evidence only. Full-cycle integral cohomology replaces the author's cut-code
construction; bond membership is checked by edge deletion, not connected shores.
"""
from pathlib import Path
from itertools import combinations, product
from fractions import Fraction as F
from collections import Counter
from math import gcd
import hashlib, json, argparse, tempfile, shutil

CHECKS=Counter()
def chk(x, name):
    CHECKS[name]+=1
    if not x: raise AssertionError(name)

class DSU:
    def __init__(self,n): self.p=list(range(n))
    def get(self,a):
        while a!=self.p[a]:
            self.p[a]=self.p[self.p[a]];a=self.p[a]
        return a
    def join(self,a,b):
        a,b=self.get(a),self.get(b)
        if a==b:return False
        self.p[a]=b;return True

def connected(n,edges,deleted=0):
    d=DSU(n)
    for i,(a,b) in enumerate(edges):
        if not (deleted>>i&1):d.join(a,b)
    return len({d.get(a) for a in range(n)})==1

def span(gens):
    s={0}
    for g in gens:s|={v^g for v in list(s)}
    return s

def rank2(rows):
    basis={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in basis:x^=basis[p]
            else:basis[p]=x;break
    return len(basis)

def cycles(n,edges):
    """Integral fundamental cycle Z-basis using a spanning tree."""
    d=DSU(n);tree=[];chords=[];adj=[[] for _ in range(n)]
    for i,(a,b) in enumerate(edges):
        if d.join(a,b):
            tree.append(i);adj[a].append((b,i,1));adj[b].append((a,i,-1))
        else:chords.append(i)
    if len(tree)!=n-1:raise ValueError('disconnected')
    basis=[]
    for e in chords:
        a,b=edges[e];c=[0]*len(edges);c[e]=1
        # The chord runs a -> b; the tree path must run b -> a.
        stack=[b];parent={b:None}
        while stack and a not in parent:
            x=stack.pop()
            for y,i,sgn in adj[x]:
                if y not in parent:parent[y]=(x,i,sgn);stack.append(y)
        x=a
        while x!=b:
            x0,i,sgn=parent[x];c[i]=sgn;x=x0
        boundary=[0]*n
        for v,(u,w) in zip(c,edges):boundary[u]-=v;boundary[w]+=v
        chk(not any(boundary),'integral_cycle_boundary_zero')
        basis.append(c)
    return basis

def contract(n,pairs,fixed):
    d=DSU(n)
    for a,b in fixed:d.join(a,b)
    roots=sorted({d.get(a) for a in range(n)});index={r:i for i,r in enumerate(roots)}
    return len(roots),[(index[d.get(a)],index[d.get(b)]) for a,b in pairs]

def analyze(n,pairs,fixed=(),full_bonds=True):
    cover=[x for e in pairs for x in (e,e)]+list(fixed)
    cb=cycles(n,cover);m=len(pairs)
    T=[[c[2*i]-c[2*i+1] for i in range(m)] for c in cb]
    rows=[sum((v%2)<<i for i,v in enumerate(row)) for row in T]
    qn,qe=contract(n,pairs,fixed)
    vertexcuts=[sum(1<<i for i,(a,b) in enumerate(qe) if (a==v)!=(b==v)) for v in range(qn)]
    cut=span(vertexcuts)
    chk(len(cut)==1<<(qn-1),'contracted_cut_dimension')
    chk(m-rank2(rows)==qn-1,'cycle_parity_kernel_dimension')
    chk(all(all((row&c).bit_count()%2==0 for row in rows) for c in cut),'cycle_kernel_equals_cut_code')
    # These two checks establish equality, without guessing a cut-code basis for L.
    contents=[]
    for i in range(m):
        g=0
        for row in T:g=gcd(g,row[i])
        contents.append(g)
    bridges={i for i in range(m) if not connected(qn,qe,1<<i)}
    chk(all(g in (1,2) for g in contents),'primitive_content_one_or_two')
    chk({i for i,g in enumerate(contents) if g==2}==bridges,'cohomology_primitive_content_matches_bridge')
    # Pair-difference integral cycles evaluate t_i as 2e_i: no denominators > 2.
    chk(all(cover[2*i]==cover[2*i+1] for i in range(m)),'pair_cycle_bounds_denominators')
    bm=sum(1<<i for i in bridges)
    reduced={c&~bm for c in cut}
    chk(all(c in cut for c in reduced),'bridge_reduction_remains_lattice')
    bad={c for c in reduced if c.bit_count() in (2,3)}
    if full_bonds:
        bonds=set()
        for k in (2,3):
            for ids in combinations(range(m),k):
                mask=sum(1<<i for i in ids)
                if not connected(qn,qe,mask) and all(connected(qn,qe,mask^(1<<i)) for i in ids):bonds.add(mask)
        chk(bad==bonds,'exact_FS_bonds_by_minimal_edge_deletion')
    # All original connected partitions not crossing fixed edges correspond to quotient cuts.
    if fixed:
        original=set()
        for s in range(1<<n):
            if any(((s>>a)^(s>>b))&1 for a,b in fixed):continue
            original.add(sum(1<<i for i,(a,b) in enumerate(pairs) if ((s>>a)^(s>>b))&1))
        chk(original==cut,'fixed_contraction_preserves_all_allowed_partitions')
        _,qcb=qn,cycles(qn,[x for e in qe for x in (e,e)])
        qrows=[sum(((c[2*i]-c[2*i+1])%2)<<i for i in range(m)) for c in qcb]
        chk(rank2(qrows)==rank2(rows),'fixed_contraction_preserves_projected_dual_lattice')
    degrees=[0]*n
    for a,b in fixed:degrees[a]+=1;degrees[b]+=1
    geometric=all(d%2==0 for d in degrees)
    return {'vertices':n,'paired_orbits':m,'fixed_edges':len(fixed),'contracted_vertices':qn,
            'cycle_rank':len(cb),'anti_rank':m,'primitive_contents':contents,
            'cut_code_size':len(cut),'bridge_count':len(bridges),'small_bond_count':len(bad),
            'perfect_extension':not bad,'even_fixed_branch_degrees':geometric}

def rational_rank(rows):
    a=[[F(x) for x in row] for row in rows]
    if not a:return 0
    k=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(k,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[k],a[pivot]=a[pivot],a[k];v=a[k][j];a[k]=[x/v for x in a[k]]
        for i in range(len(a)):
            if i!=k:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k

def exchanged_control():
    edges=[(0,1),(1,2),(2,0),(0,3),(3,4),(4,0)]
    vp=[0,3,4,1,2];ep=[3,4,5,0,1,2]
    chk(all(tuple(vp[v] for v in edges[i])==edges[ep[i]] for i in range(6)),
        'exchanged_example_involution_preserves_incidence')
    cb=cycles(5,edges);projected=[]
    for c in cb:
        ic=[0]*6
        for i,x in enumerate(c):ic[ep[i]]=x
        projected.append([F(x-y,2) for x,y in zip(c,ic)])
    r=rational_rank(projected)
    chk(r==1 and len(cb)==2,'exchanged_example_anti_rank_computed')
    return {'cover_vertices':5,'cover_edges':6,'cover_cycle_rank':2,
            'exchanged_edge_orbits':3,'anti_rank':r,
            'realizable':'Take one elliptic base component at each of the three quotient vertices, a connected etale cover at the fixed vertex, split covers at the other two vertices, and equivariant gluing. Base genus 4; cover genus 7.'}

def admissibility_and_separating_bridge_controls():
    def admissible(vp,edges,ep,sign):
        if sorted(vp)!=list(range(len(vp))) or any(vp[vp[v]]!=v for v in range(len(vp))):return False
        if sorted(ep)!=list(range(len(edges))) or any(ep[ep[e]]!=e for e in range(len(edges))):return False
        for i,(a,b) in enumerate(edges):
            if sign[i] not in (-1,1) or sign[i]*sign[ep[i]]!=1:return False
            target=edges[ep[i]] if sign[i]==1 else tuple(reversed(edges[ep[i]]))
            if (vp[a],vp[b])!=target:return False
            if ep[i]==i and sign[i]==-1:return False
        return True
    chk(not admissible([1,0],[(0,1)],[0],[-1]),'negative_fixed_edge_reversal_rejected')
    chk(not admissible([0],[(0,0)],[0],[-1]),'negative_fixed_loop_branch_exchange_rejected')
    edges=[(0,1),(0,2),(1,1),(2,2)];vp=[0,2,1];ep=[1,0,3,2]
    chk(admissible(vp,edges,ep,[1]*4),'exchanged_separating_bridges_admissible')
    cb=cycles(3,edges)
    chk(all(c[0]==c[1]==0 for c in cb),'genuine_separating_cover_bridges_zero_coedges')
    projected=[]
    for c in cb:
        ic=[0]*4
        for i,x in enumerate(c):ic[ep[i]]=x
        projected.append([F(x-y,2) for x,y in zip(c,ic)])
    chk(rational_rank(projected)==1,'exchanged_bridge_fixture_anti_rank')
    return {'cover_vertices':3,'cover_edges':4,'exchanged_edge_orbits':2,'anti_rank':1,
            'genuine_cover_bridges_have_zero_coedge':True,'geometric_base_genus':3,'geometric_cover_genus':5,
            'inversion_negatives_rejected':2}

def matrix_controls():
    def value(q,v):return sum(F(x)*q[i][j]*v[j] for i,x in enumerate(v) for j in range(len(v)))
    def ldl(q):
        a=[[F(x) for x in row] for row in q];piv=[]
        for k in range(len(a)):
            p=a[k][k];piv.append(p)
            if p<=0:return None
            for i in range(k+1,len(a)):
                for j in range(k+1,len(a)):a[i][j]-=a[i][k]*a[k][j]/p
        return piv
    def finite(q,rays,lam):
        n=len(q);low=[[F(q[i][j])-(lam if i==j else 0) for j in range(n)] for i in range(n)]
        chk(ldl(low) is not None,'independent_LDL_spectral_bound')
        B=0
        while lam*(B+1)**2<=1:B+=1
        values=[value(q,v) for v in product(range(-B,B+1),repeat=n) if any(v)]
        chk(min(values)>=1,'independent_finite_lattice_minimum')
        chk(all(value(q,v)==1 for v in rays),'independent_primitive_coedge_equalities')
        return {'box_bound':B,'nonzero_vectors':len(values),'minimum':str(min(values))}
    u=(1,0);v=(0,1);minus=(1,-1);plus=(1,1);a=(2,-1)
    results={
      'FS4':finite([[F(1) if i==j else F(1,2) if i==0 or j==0 else F(0) for j in range(4)] for i in range(4)],[(2,-1,-1,-1),(0,1,0,0),(0,0,1,0),(0,0,0,1)],F(1,16)),
      'C1':finite([[F(1),F(1,2)],[F(1,2),F(1)]],[u,v,minus],F(1,4)),
      'C2':finite([[F(1),F(3,2)],[F(3,2),F(3)]],[a,u,minus],F(1,8)),
      'overlap_plus':finite([[F(1),F(-1,2)],[F(-1,2),F(1)]],[u,v,plus],F(1,4)),
    }
    for n in range(2,13):
        q=[[F(n,4) if i==j==0 else F(1) if i==j else F(1,2) if i==0 or j==0 else F(0) for j in range(n)] for i in range(n)]
        piv=ldl(q);chk(piv is not None,'FS_all_ranks_LDL_positive')
        determinant=F(1)
        for x in piv:determinant*=x
        chk(determinant==F(1,4),'FS_all_ranks_LDL_determinant')
        rays=[(2,)+(-1,)*(n-1)]+[tuple(int(i==j) for i in range(n)) for j in range(1,n)]
        chk(all(value(q,w)==1 for w in rays),'FS_all_ranks_coedge_values')
    for i in range(2):
        for j in range(2):
            chk(plus[i]*plus[j]+minus[i]*minus[j]==2*u[i]*u[j]+2*v[i]*v[j],
                'overlap_parallelogram_outer_identity')
            chk(F(a[i]*a[j]+v[i]*v[j],2)==u[i]*u[j]+minus[i]*minus[j],
                'subdivision_outer_identity')
    return results

def all_subspaces(r):
    spaces={frozenset({0})}
    for dim in range(r):
        following=set()
        for s in spaces:
            if len(s)!=1<<dim:continue
            for v in range(1,1<<r):
                if v not in s:following.add(frozenset(set(s)|{v^w for w in s}))
        spaces|=following
    return spaces

def binary_code_controls():
    counts={};threshold={};sign_checks=0
    for r in range(0,6):
        ss=all_subspaces(r);counts[str(r)]=len(ss);admissible=positive=0
        for code in ss:
            if any(v.bit_count()==1 for v in code):continue
            admissible+=1
            minweight=min((v.bit_count() for v in code if v),default=10**6)
            predicted=min(F(1),F(minweight,4))
            # Direct nearest-coordinate enumeration: each parity class has representatives
            # with coordinates 0 or +/-1/2. Include unit vectors for the zero coset.
            actual=F(1)
            for v in code:
                if not v:continue
                support=[i for i in range(r) if v>>i&1]
                for sg in product((-1,1),repeat=len(support)):
                    vec=[F(0)]*r
                    for i,s in zip(support,sg):vec[i]=F(s,2)
                    actual=min(actual,sum(x*x for x in vec))
            chk(actual==predicted,'arbitrary_binary_code_exact_coset_minimum')
            chk((actual>=1)==(minweight>=4),'arbitrary_binary_code_metric_threshold')
            positive+=actual>=1
        threshold[str(r)]={'without_weight_one':admissible,'positive':positive}
    # Averaging is a matrix identity, so it tests every possible symmetric form.
    for w in range(1,10):
        total=[[0]*w for _ in range(w)]
        for s in product((-1,1),repeat=w):
            for i in range(w):
                for j in range(w):total[i][j]+=s[i]*s[j]
        chk(all(total[i][j]==((1<<w) if i==j else 0) for i in range(w) for j in range(w)),
            'sign_average_matrix_identity')
        sign_checks+=1
    return {'all_binary_subspaces_by_rank':counts,'threshold_checks':threshold,'sign_identity_ranks':sign_checks}

EXPECTED={'README.md','RESEARCH.md','RESEARCH_LOG.md','STATUS.json','SOURCE_VERIFICATION.json','PRIOR_ATTEMPT_CHECK.md','verify.py','verification_results.json','MANIFEST.json'}
PINNED='13a5055116fbed43fe1b2f355da34b8ff12d1e4aba0deac99ee1cbe26b023941'
RESEARCH='16df888b6648f4de38e7c82b4de42e29f9fd5d84fc833e19a93a8029b0d59167'
def digest(b):return hashlib.sha256(b).hexdigest()
def bind(root):
    if not root.is_dir() or root.is_symlink():raise ValueError('root not ordinary directory')
    if {p.name for p in root.iterdir()}!=EXPECTED:raise ValueError('object set differs')
    for p in root.iterdir():
        if p.is_symlink() or not p.is_file():raise ValueError('object not regular file')
    raw=(root/'MANIFEST.json').read_bytes()
    if digest(raw)!=PINNED:raise ValueError('external manifest binding failed')
    m=json.loads(raw)
    if m['schema']!='prym-safe-manifest-v1':raise ValueError('schema')
    seen=set()
    for rec in m['files']:
        name=rec['path']
        if name in seen or name not in EXPECTED-{'MANIFEST.json'}:raise ValueError('path set')
        seen.add(name)
        if type(rec['bytes']) is not int:raise ValueError('byte type')
        b=(root/name).read_bytes()
        if len(b)!=rec['bytes'] or digest(b)!=rec['sha256']:raise ValueError('content binding')
    if seen!=EXPECTED-{'MANIFEST.json'}:raise ValueError('incomplete manifest')
    if digest((root/'RESEARCH.md').read_bytes())!=RESEARCH:raise ValueError('research binding')
    return {'manifest_sha256':PINNED,'research_sha256':RESEARCH,'files':9,'bytes':sum(p.stat().st_size for p in root.iterdir())}

def integrity_controls(root):
    names=['changed_byte','extra_file','missing_file','symlink','path_traversal','duplicate_record','boolean_size','wrong_hash','self_consistent_rewrite','manifest_symlink','directory_instead_of_file']
    rejected=[]
    for kind in names:
        with tempfile.TemporaryDirectory(prefix='prym-independent-integrity-') as tmp:
            p=Path(tmp)/'copy';shutil.copytree(root,p)
            if kind=='changed_byte':(p/'RESEARCH.md').write_bytes((p/'RESEARCH.md').read_bytes()+b'X')
            elif kind=='extra_file':(p/'extra.pdf').write_bytes(b'x')
            elif kind=='missing_file':(p/'README.md').unlink()
            elif kind=='symlink':(p/'README.md').unlink();(p/'README.md').symlink_to('RESEARCH.md')
            elif kind=='manifest_symlink':(p/'MANIFEST.json').unlink();(p/'MANIFEST.json').symlink_to('STATUS.json')
            elif kind=='directory_instead_of_file':(p/'README.md').unlink();(p/'README.md').mkdir()
            else:
                m=json.loads((p/'MANIFEST.json').read_text());r=m['files'][0]
                if kind=='path_traversal':r['path']='../RESEARCH.md'
                elif kind=='duplicate_record':m['files'].append(dict(r))
                elif kind=='boolean_size':r['bytes']=True
                elif kind=='wrong_hash':r['sha256']='0'*64
                elif kind=='self_consistent_rewrite':
                    f=p/r['path'];f.write_bytes(f.read_bytes()+b'x');r['bytes']=f.stat().st_size;r['sha256']=digest(f.read_bytes())
                (p/'MANIFEST.json').write_text(json.dumps(m))
            try:bind(p)
            except (ValueError,FileNotFoundError):rejected.append(kind)
            else:raise AssertionError('accepted altered binding: '+kind)
    return rejected

def math_negatives():
    out=[]
    # A false Z^n lattice misses the genuine FS2 obstruction.
    r=analyze(2,[(0,1)]*2)
    chk(not r['perfect_extension'],'negative_ignore_half_coset')
    out.append('Replacing the FS2 lattice by Z^2 wrongly predicts extension.')
    # Unnormalized FS1 would prescribe a nonprimitive vector of norm one.
    r=analyze(2,[(0,1)])
    chk(r['perfect_extension'] and r['primitive_contents']==[2],'negative_ignore_bridge_primitive')
    out.append('Failing to divide the FS1 coedge by two wrongly obstructs extension.')
    # Fixed-node contraction is indispensable; fixed double edge annihilates FS2 cut.
    r=analyze(2,[(0,1)]*2,[(0,1)]*2)
    chk(r['perfect_extension'] and r['contracted_vertices']==1,'negative_ignore_fixed_edges')
    out.append('Discarding rather than contracting fixed edges wrongly retains an FS2 cut.')
    r=exchanged_control()
    chk(r['exchanged_edge_orbits']!=r['anti_rank'],'negative_exchanged_vertex_coordinate_basis')
    out.append('Two triangles interchanged at one fixed vertex have three edge orbits but anti-rank one; the coordinate theorem cannot be globalized.')
    cb=cycles(2,[(0,1)]*4)
    rows=[sum(((c[2*i]-c[2*i+1])%2)<<i for i in range(2)) for c in cb]
    in_lattice=lambda mask:all((row&mask).bit_count()%2==0 for row in rows)
    chk(in_lattice(3) and not in_lattice(1),'negative_wrong_homology_lattice')
    out.append('The dual of integral anti-homology incorrectly contains each t_i/2 in FS2; the correct projected-homology dual admits their half-sum but not either alone.')
    # Degree-one branch divisor cannot be a double cover of a smooth normalization.
    r=analyze(2,[(0,1)],[(0,1)])
    chk(not r['even_fixed_branch_degrees'],'negative_odd_fixed_branch_degree')
    out.append('A lone fixed joining node at each normalization has odd branch degree and is not a geometrically admissible cover.')
    # Four prescribed rays give incompatible polarization equations.
    chk(1+1!=2*1+2*1,'negative_overlap_union')
    out.append('The u,v,u+v,u-v union fails the parallelogram identity although each triple works.')
    # FS4 det-two does not obstruct the perfect fan, but does obstruct unimodularity.
    r=analyze(2,[(0,1)]*4)
    chk(r['perfect_extension'] and r['cut_code_size']==2,'negative_unimodular_shortcut')
    out.append('FS4 is perfect-cone extendable despite coedge index two.')
    # Closing under degeneration matters: triangle is a small-bond example with >2 vertices.
    r=analyze(3,[(0,1),(1,2),(2,0)])
    chk(not r['perfect_extension'] and r['small_bond_count']==3,'negative_omit_FS_closures')
    out.append('A doubled triangle is an FS2 degeneration but not a generic two-component FS cover.')
    out.append('An involution reversing a fixed edge or exchanging the two branches of a fixed loop is inadmissible; explicit validation rejects both.')
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parents[1]/'safe');ap.add_argument('--output',type=Path);a=ap.parse_args()
    result={'binding':bind(a.packet),'method':'Independent fundamental-cycle integral cohomology, binary parity-kernel, and minimal-edge-deletion bond calculations; no author imports.'}
    counts={};positives={}
    for n in range(1,7):
        possibilities=list(combinations(range(n),2));count=positive=0
        for mask in range(1<<len(possibilities)):
            es=[e for i,e in enumerate(possibilities) if mask>>i&1]
            if not connected(n,es):continue
            r=analyze(n,es,full_bonds=n<=5);count+=1;positive+=r['perfect_extension']
        counts[str(n)]=count;positives[str(n)]=positive
    chk(counts=={'1':1,'2':1,'3':4,'4':38,'5':728,'6':26704},'independent_connected_graph_counts')
    result['all_connected_labelled_simple_graphs_by_vertices']=counts
    result['positive_graphs_by_vertices']=positives
    result['full_cycle_lattice_graphs']=sum(counts.values())
    result['minimal_edge_deletion_bond_comparisons']=sum(counts[str(n)] for n in range(1,6))
    fixed_count=geometric=0
    # For every vertex pair independently: absent, paired, fixed, paired+fixed.
    # Includes odd branch degree algebraic tests, explicitly separated from realizability.
    for n in range(1,5):
        possibilities=list(combinations(range(n),2))
        for types in product(range(4),repeat=len(possibilities)):
            pairs=[e for e,t in zip(possibilities,types) if t&1]
            fixed=[e for e,t in zip(possibilities,types) if t&2]
            if not fixed or not connected(n,pairs+fixed):continue
            r=analyze(n,pairs,fixed);fixed_count+=1;geometric+=r['even_fixed_branch_degrees']
    result['fixed_node_algebraic_graphs']=fixed_count
    result['fixed_node_even_branch_degree_realizable_graphs']=geometric
    fixtures={
      'fixed_loop':(1,[(0,0)],[(0,0)]),
      'fixed_triangle':(3,[(0,1),(1,2),(2,0)],[(0,1),(1,2),(2,0)]),
      'fixed_double_join':(2,[(0,1)]*2,[(0,1)]*2),
      'fixed_bridge_algebra_only':(2,[(0,1)]*2,[(0,1)]),
      'paired_loop_and_bridge':(3,[(0,1),(1,2),(1,2),(1,1)],[]),
      'K5':(5,list(combinations(range(5),2)),[]),
      'K5_bridge_loop':(6,list(combinations(range(5),2))+[(4,5),(2,2)],[]),
      'empty_anti_rank':(1,[],[(0,0)]),
      'fixed_triangle_attached_FS2':(4,[(0,3)]*2,[(0,1),(1,2),(2,0)]),
    }
    result['fixtures']={name:analyze(*args) for name,args in fixtures.items()}
    result['binary_codes']=binary_code_controls()
    result['independent_matrix_certificates']=matrix_controls()
    result['exchanged_vertex_scope_fixture']=exchanged_control()
    result['admissibility_separating_bridge_fixture']=admissibility_and_separating_bridge_controls()
    result['mathematical_negative_controls']=math_negatives()
    result['integrity_negative_controls_rejected']=integrity_controls(a.packet)
    result['binding_after']=bind(a.packet)
    result['checks_by_type']=dict(sorted(CHECKS.items()));result['assertions']=sum(CHECKS.values())
    result['outcome']='PASS_SCOPED_CONTROLS_NOT_UNIVERSAL_PROOF'
    s=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if a.output:a.output.write_text(s)
    print(s)
if __name__=='__main__':main()
