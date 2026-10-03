"""New exact controls. No candidate or earlier audit modules are imported.

Finite calculations verify the stated formulas, not the universal open problem.
All matrix calculations use fractions from the Python standard library.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt
import json

def rref(a):
    a = [[F(x) for x in row] for row in a]
    pivots=[]; r=0
    if not a: return a,pivots
    for c in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][c]),None)
        if p is None: continue
        a[r],a[p]=a[p],a[r]; z=a[r][c];a[r]=[x/z for x in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][c]:
                z=a[i][c];a[i]=[x-z*y for x,y in zip(a[i],a[r])]
        pivots.append(c);r+=1
        if r==len(a):break
    return a,pivots

def rank(a): return len(rref(a)[1])
def mul(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def transpose(a):return list(map(list,zip(*a)))
def kernel(a):
    rr,pp=rref(a); n=len(a[0]); free=[j for j in range(n) if j not in pp]; vv=[]
    for j in free:
        v=[F(0)]*n;v[j]=1
        for i,p in enumerate(pp):v[p]=-rr[i][j]
        vv.append(v)
    return transpose(vv)

def tm_image(w):return ''.join('01' if x=='0' else '10' for x in w)
@lru_cache(None)
def tm_language(n):
    # Every factor of length <=2^k is contained in two adjacent k-supertiles.
    k=max(0,(n-1).bit_length()); seeds=['00','01','10','11']
    for _ in range(k):seeds=[tm_image(w) for w in seeds]
    return frozenset(w[i:i+n] for w in seeds for i in range(len(w)-n+1))

def tm_collared_control():
    edges=sorted(tm_language(3)); vertices=sorted(tm_language(2)); vi={v:i for i,v in enumerate(vertices)};ei={e:i for i,e in enumerate(edges)}
    b=[[0]*len(edges) for _ in vertices]
    m=[[0]*len(edges) for _ in edges];v=[[0]*len(vertices) for _ in vertices]
    for j,e in enumerate(edges):
        b[vi[e[1:]]][j]+=1;b[vi[e[:2]]][j]-=1
        image=tm_image(e)
        for t in [image[1:4],image[2:5]]:m[ei[t]][j]+=1
    for j,p in enumerate(vertices):v[vi[str(1-int(p[0]))+p[1]]][j]=1
    assert mul(b,m)==mul(v,b)
    z=kernel(b); power=eye(len(edges));ranks=[]
    for _ in range(5):
        ranks.append(rank(mul(power,z)));power=mul(m,power)
    assert ranks==[3,2,2,2,2]
    # No invented border data: each output collar is read directly from sigma(abc).
    return {'vertices':vertices,'collared_edges':edges,'boundary_matrix':b,'edge_substitution_matrix':m,'vertex_substitution_matrix':v,'cycle_image_ranks':ranks,'chain_map_verified':True}

def shear_control():
    p=lambda n:len(tm_language(n))
    rows=[]
    for n in range(3,131):
        m=n+1;k=n+m-2
        cells=[p(k-1)*m,p(k)*m,p(k)*(m+1),p(k+1)*(m+1)]
        chi=cells[0]-cells[1]-cells[2]+cells[3]
        assert chi==(m+1)*(p(k+1)-p(k))-m*(p(k)-p(k-1))
        if chi>n:rows.append({'rectangle_sides':[n,m],'TM_length_middle':k,'TM_increment_pair':[p(k)-p(k-1),p(k+1)-p(k)],'cells_V_Eh_Ev_F':cells,'Euler':chi,'H2_lower_bound':chi-1})
    assert rows and max(r['Euler'] for r in rows)>200
    return rows

def delayed_death_control():
    # Backbone survives; transient n is born at n and dies at 2n+1.
    labels=lambda i:[0]+[n for n in range(1,i+1) if i<=2*n]
    image_rank=lambda i,j:sum(n==0 or j<=2*n for n in labels(i))
    examples=[]
    for lag in [1,2,7,19,51]:
        i=2*lag+3
        assert image_rank(i,i+lag)>1 and image_rank(i,2*i+1)==1
        examples.append({'lag':lag,'i':i,'raw_rank':len(labels(i)),'rank_after_lag':image_rank(i,i+lag),'rank_at_2i_plus_1':image_rank(i,2*i+1)})
    return {'limit_rank_proved_symbolically':1,'no_uniform_lag_proved_symbolically':True,'exact_examples':examples}

def cyclic_cover_control():
    out=[]
    for d in [3,5,7]:
        cocycle=(1,0); first=cocycle; rows=[]
        for stage in range(8):
            # Fibonacci rose automorphism a->ab,b->a. v_i=T^t v_(i+1).
            nxt=(cocycle[1]%d,(cocycle[0]-cocycle[1])%d)
            assert ((nxt[0]+nxt[1])%d,nxt[0])==cocycle
            b=[[0]*(2*d) for _ in range(d)]
            for q in range(d):
                for g in range(2):b[(q+cocycle[g])%d][2*q+g]+=1;b[q][2*q+g]-=1
            assert rank(b)==d-1
            # Lift every a-edge to ab and every b-edge to a; test endpoints.
            for q in range(d):
                assert (q+nxt[0]+nxt[1])%d==(q+cocycle[0])%d
                assert (q+nxt[0])%d==(q+cocycle[1])%d
            rows.append({'stage':stage,'monodromy':list(cocycle),'next_monodromy':list(nxt),'vertices':d,'edges':2*d,'H1_rank':2*d-rank(b)})
            cocycle=nxt
        assert any(tuple(r['monodromy'])!=first for r in rows)
        out.append({'degree':d,'changing_monodromy_lifts':rows})
    return out

def transfer_control():
    # Jump module J=(t-1)Q[t,t^-1] is free rank one. J/(t^D-1)J has rank D.
    out=[]
    for d in [1,2,4,8,16,32]:
        n=2*d;shift=[[int(i==(j+d)%n) for j in range(n)] for i in range(n)]
        boundary=[[shift[i][j]-int(i==j) for j in range(n)] for i in range(n)]
        assert n-rank(boundary)==d
        # Pullback repeats residues; transfer adds the two lifts. Include constants.
        inc=[[int((i%d)==j) for j in range(d)] for i in range(2*d)]
        trace=transpose(inc)
        assert mul(trace,inc)==[[2*int(i==j) for j in range(d)] for i in range(d)]
        assert rank(inc)==d
        out.append({'D':d,'jump_coinvariant_rank':d,'suspension_Sturmian_power_H1_rank':d+1,'product_with_Sturmian_H2_rank':2*(d+1),'pullback_rank':rank(inc),'trace_pullback_equals_2I':True})
    # Finitary clopen tests factor through mod 2^N; translation preserves equal residues.
    obstructions=[]
    for exponent in [1,3,6,9]:
        a=0;b=2**exponent; modulus=2**exponent
        assert all((a+t)%modulus==(b+t)%modulus for t in range(-100,101))
        obstructions.append({'partition_modulus':modulus,'distinct_fibre_points':[a,b],'all_time_equal_residues_proved_by_modular_identity':True})
    return {'transfer_tower':out,'finite_generator_obstruction':obstructions}

def sharp_product_control():
    # Mechanical word uses exact sqrt comparisons, only as a finite calibration.
    floor_alpha=lambda k:(isqrt(5*k*k)-k)//2
    word=''.join(str(floor_alpha(k+1)-floor_alpha(k)) for k in range(12000))
    p=[len({word[i:i+n] for i in range(len(word)-n+1)}) for n in range(1,21)]
    assert p==list(range(2,22))
    return {'exact_mechanical_sample_word_counts':p,'Sturmian_product': [{'d':d,'total_rational_rank':3**d,'asymptotic_complexity_coefficient':1,'sharp_ratio':3**d} for d in range(1,7)],'finite_sample_is_not_universal_proof':True}

def roof_control():
    # Fractional position rescaling respects roof seam, but changes time speed.
    roof=F(3,2);t=F(1,4);dt=F(1,8)
    assert (t+dt)/roof-t/roof==dt/roof and dt/roof!=dt
    return {'rational_roof':str(roof),'time_increment':str(dt),'mapped_increment':str(dt/roof),'seam_coordinates':[0,1],'homeomorphism_does_not_imply_time_conjugacy':True}

def main():
    data={'matrix_arithmetic':'exact rational stdlib; no candidate imports','product':sharp_product_control(),'Thue_Morse_collared':tm_collared_control(),'sheared_TM_Sturmian':shear_control(),'nonuniform_persistence':delayed_death_control(),'fixed_degree_changing_monodromy':cyclic_cover_control(),'inverse_2adic_transfers':transfer_control(),'roof_rescaling':roof_control()}
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
