"""Reviewer-authored finite controls. No author checker is imported.

Usage: python independent_check.py AUTHOR_DIRECTORY SOURCE_DIRECTORY
The read-only source join uses the already installed xlrd package.
These controls do not constitute knot recognition or a homological theorem prover.
"""
from pathlib import Path
from itertools import product, permutations, combinations
from collections import Counter
from fractions import Fraction
import math, json, sys

A, S = map(Path, sys.argv[1:3])
checks = Counter()
def ck(x, family):
    assert x, family
    checks[family] += 1

# Direct simultaneous SL(2,Z) map from (+1,+1),(-1,+1) to any oriented
# primitive slope pair of determinant +2. This uses no Bezout routine.
vectors = [(x,y) for x in range(-15,16) for y in range(-15,16) if math.gcd(x,y)==1]
distance_two_pairs = 0
for a in vectors:
    for b0 in vectors:
        determinant = a[0]*b0[1]-a[1]*b0[0]
        if abs(determinant) != 2:
            continue
        distance_two_pairs += 1
        b = b0 if determinant == 2 else (-b0[0],-b0[1])
        ck(tuple(x%2 for x in a)==tuple(x%2 for x in b), 'same_mod2_pairing')
        u = tuple((a[i]-b[i])//2 for i in (0,1))
        v = tuple((a[i]+b[i])//2 for i in (0,1))
        ck(tuple(u[i]+v[i] for i in (0,1))==a, 'first_crossing_slope')
        ck(tuple(-u[i]+v[i] for i in (0,1))==b, 'second_crossing_slope')
        ck(u[0]*v[1]-u[1]*v[0]==1, 'orientation_preserving_basis')

# Independent determinant/minor computation for the two Alexander blocks.
def det(M):
    if not M: return 1
    return sum((-1)**j*M[0][j]*det([r[:j]+r[j+1:] for r in M[1:]]) for j in range(len(M)))
P = [[0,0,1],[1,0,0],[0,1,0]]
for c,d in [(2,-1),(1,-2)]:
    B = [[c*int(i==j)+d*P[i][j] for j in range(3)] for i in range(3)]
    ds = []
    for size in (1,2,3):
        values=[abs(det([[B[i][j] for j in cols] for i in rows]))
                for rows in combinations(range(3),size) for cols in combinations(range(3),size)]
        g=0
        for v in values:g=math.gcd(g,v)
        ds.append(g)
    ck(ds==[1,1,7], 'third_cover_determinantal_divisors')
for t in range(-30,31):
    # det(V-t V^T) is the negative of the chosen Alexander normalization.
    ck((2-t)*(1-2*t)==2*t*t-5*t+2, 'alexander_polynomial_up_to_sign')
ck(abs(2*(-1)**2-5*(-1)+2)==9, 'determinant_nine')
for a in range(-20,21):
    for b in range(1,21):
        if a==0: continue
        x=Fraction(b*b-a*a,b*b+a*a)
        y=Fraction(2*a*b,b*b+a*a)
        ck(x*x+y*y==1, 'rational_circle')
        ck(9*(1-x)**2+y*y>0, 'signature_opposite_eigenvalues')
for t in range(7):
    singular=((2-t)*(1-2*t))%7==0
    ck(singular==(t in (2,4)), 'deck_eigenvalues')

# Exact syntactic verification of every saved Artin/Markov macro move.
C = json.loads((A/'braid_upper_certificate.json').read_text())
word=C['source_word']; certificate=C['certificate']
ck(certificate['changes_zero_based']==[2,3,7], 'three_changes')
changed=[-v if i in (2,3,7) else v for i,v in enumerate(word)]
ck(certificate['initial']==[4,changed], 'changed_initial_word')
def components(n,w):
    p=list(range(n))
    for x in w:
        j=abs(x)-1;p[j],p[j+1]=p[j+1],p[j]
    seen=set(); cycles=0
    for j in range(n):
        if j in seen:continue
        cycles+=1
        while j not in seen:
            seen.add(j);j=p[j]
    return cycles
ck(components(4,word)==1, 'source_is_knot')
state=certificate['initial']
for step in certificate['moves']:
    ck(step['before']==state, 'trace_continuity')
    n,w=state; nn,v=step['after']; op=step['move']; name=op[0]
    ck(components(n,w)==components(nn,v)==1, 'closure_component_preservation')
    if name=='cancel':
        i=op[1]
        ck(w[i]+w[i+1]==0 and nn==n and v==w[:i]+w[i+2:], 'literal_inverse_cancellation')
    elif name=='artin':
        i=op[1]; a,b,c=w[i:i+3]
        ck(a==c and a*b>0 and abs(abs(a)-abs(b))==1, 'inverse_artin_hypothesis')
        ck(nn==n and v==w[:i]+[b,a,b]+w[i+3:], 'literal_artin_rewrite')
    elif name=='mixed_artin_reverse':
        i=op[1];a,b,c=w[i:i+3]
        ck(a==-c and a*b<0 and abs(abs(a)-abs(b))==1, 'mixed_artin_hypothesis')
        ck(nn==n and v==w[:i]+[b,-a,-b]+w[i+3:], 'literal_mixed_rewrite')
    elif name=='destabilize_end':
        end,i=op[1:]
        ck(end in (1,n-1) and sum(abs(x)==end for x in w)==1 and abs(w[i])==end, 'unique_extreme_generator')
        remaining=w[:i]+w[i+1:]
        if end==1:remaining=[(1 if x>0 else -1)*(abs(x)-1) for x in remaining]
        ck(nn==n-1 and remaining==v, 'markov_macro_output')
        # Moving the distinguished letter to the end leaves cyclically reordered
        # remaining letters. A further conjugation returns the displayed order.
        cyclic=w[i+1:]+w[:i]
        ck(any(cyclic[j:]+cyclic[:j]==w[:i]+w[i+1:] for j in range(len(cyclic) or 1)), 'implicit_cyclic_conjugation')
    else: raise AssertionError(name)
    state=step['after']
ck(state==[1,[]], 'unknot_final_braid')

# Complete Boolean covariance test on a three-crossing cube, no knot recognition.
for perm in permutations(range(3)):
    relabel=lambda m:sum(((m>>i)&1)<<perm[i] for i in range(3))
    for truth in range(1,256):
        selected=[m for m in range(8) if (truth>>m)&1]
        image=[relabel(m) for m in selected]
        ck(Counter(m.bit_count() for m in selected)==Counter(m.bit_count() for m in image), 'resolution_cardinality')
        w=(1,4,9);wr=[0]*3
        for i in range(3):wr[perm[i]]=w[i]
        cost=lambda m,weight:sum(weight[i] for i in range(3) if (m>>i)&1)
        ck(min(cost(m,w) for m in selected)==min(cost(m,wr) for m in image), 'resolution_weight_minimum')

# All-pairs distances, independent of the author's BFS traversal.
vertices=('U','A','Ap','B','Bp','T','Tp'); loc=[(1,3),(3,5),(5,0),(2,4),(4,6),(6,0)]
def distances(edges):
    D=[[0 if i==j else 100 for j in range(7)] for i in range(7)]
    for i,j in edges:D[i][j]=D[j][i]=1
    for k in range(7):
        for i in range(7):
            for j in range(7):D[i][j]=min(D[i][j],D[i][k]+D[k][j])
    return D
dl=distances(loc);df=distances(loc+[(1,5)])
rho=(0,2,1,4,3,6,5)
for i in range(1,7):
    delta=min(dl[i][5],dl[i][6]);mut_delta=min(dl[rho[i]][5],dl[rho[i]][6])
    ck(delta==mut_delta, 'local_graph_invariance')
    defect=delta-df[i][0]+1;other=mut_delta-df[rho[i]][0]+1
    ck(defect>=0 and df[rho[i]][0]-df[i][0]==defect-other, 'local_defect_identity')
ck((df[1][0],df[2][0])==(2,3), 'abstract_only_gap')

# Read-only workbook/table snapshot independently reconstructed by row labels.
import xlrd
book=xlrd.open_workbook(str(S/'knotinfo_data_complete.xls'),on_demand=True)
sheet=book.sheet_by_index(0); headers=sheet.row_values(0)
columns={x:headers.index(x) for x in ['name','unknotting_number','unknotting_number_anon','braid_notation','dt_notation'] if x in headers}
rows={sheet.cell_value(i,0):i for i in range(2,sheet.nrows)}
def cell(name,column): return sheet.cell_value(rows[name],headers.index(column))
groups=[]
for filename in ['12mut.out','13mut.out']:
    pending=[]
    for line in (S/filename).read_text().splitlines()+['']:
        if not line.strip():
            if pending:groups.append(pending);pending=[]
            continue
        crossing,index,*dt=map(int,line.split());offset={11:367,12:1288,13:4878}[crossing]
        name=f'{crossing}'+('a' if index<=offset else 'n')+'_'+str(index if index<=offset else index-offset)
        ck(name in rows, 'table_row_join')
        ck(sorted(abs(x) for x in dt)==list(range(2,2*crossing+1,2)), 'dt_permutation')
        pending.append((name,dt))
def interval(value):
    if isinstance(value,(float,int)):return (int(value),int(value))
    numbers=json.loads(value)
    return (min(numbers),max(numbers))
different=[]
for group in groups:
    vals=[interval(cell(name,'unknotting_number')) for name,dt in group]
    ck(max(x[0] for x in vals)<=min(x[1] for x in vals), 'displayed_interval_overlap')
    if len(set(vals))>1:different.append([name for name,dt in group])
ck(len(groups)==865 and sum(len(g) for g in groups)==1841, 'snapshot_totals')
ck(different==[['11n_76','11n_78']], 'sole_different_interval_pair')
ck(interval(cell('11n_76','unknotting_number'))==(3,3), 'n76_displayed_cell_only')
ck(interval(cell('11n_78','unknotting_number'))==(2,3), 'n78_displayed_cell_only')
ck(all(cell(x,'unknotting_number_anon')=='' for x in ('11n_76','11n_78')), 'blank_reference_cells')
ck(json.loads(cell('11n_78','braid_notation'))==word, 'named_word_source')
target_dt=next(dt for g in groups for name,dt in g if name=='11n_78')
ck(target_dt==[4,8,-14,2,-20,-16,-18,-6,-12,-22,-10], 'source_dt_literal')
book.release_resources()

print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),
 'categories':dict(sorted(checks.items())), 'distance_two_pairs':distance_two_pairs,
 'source_groups':len(groups), 'source_member_rows':1841,
 'scope':'Independent finite algebra, explicit braid trace, and pinned read-only data controls. No knot recognition, unrestricted lower bound, table completeness or mutation counterexample.'},indent=2,sort_keys=True))
