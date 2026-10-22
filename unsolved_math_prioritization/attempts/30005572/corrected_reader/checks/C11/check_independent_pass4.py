"""Independent finite checks of audit algebra; not geometric proof certificates."""
import itertools, json, math
from pathlib import Path

def require(condition):
    if not condition:
        raise RuntimeError("Independent exact audit check failed")

def field(p, ext=False):
    if not ext:
        return list(range(p)), lambda a,b:(a+b)%p, lambda a,b:a*b%p, 0,1
    # F25 = F5[t]/(t^2-2).
    els=list(itertools.product(range(5),repeat=2))
    return els,lambda a,b:((a[0]+b[0])%5,(a[1]+b[1])%5),lambda a,b:((a[0]*b[0]+2*a[1]*b[1])%5,(a[0]*b[1]+a[1]*b[0])%5),(0,0),(1,0)

inc=[]
for p,ext in [(2,False),(3,False),(5,False),(7,False),(5,True)]:
    E,add,mul,z,o=field(p,ext); q=len(E)
    V=list(itertools.product(E,repeat=2)); counts={v:0 for v in V}
    reps=[(o,t) for t in E]+[(z,o)]
    for x,y in reps:
        D={(mul(a,x),mul(a,y)) for a in E}
        require(len(D)==q)
        for v in D: counts[v]+=1
    require(counts[(z,z)]==q+1)
    require(all(n==1 for v,n in counts.items() if v!=(z,z)))
    inc.append({'q':q,'lines':len(reps),'zero_multiplicity':counts[(z,z)],'nonzero_points':q*q-1,'all_nonzero_multiplicities_one':True})

# Exact integer coefficient module on F2^2, permutation action of SL2(F2).
def mm(a,b):
    return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2))%2 for i in range(2) for j in range(2))
def inv(a): return (a[3],a[1],a[2],a[0])
def mv(a,v): return ((a[0]*v[0]+a[1]*v[1])%2,(a[2]*v[0]+a[3]*v[1])%2)
G=[a for a in itertools.product(range(2),repeat=4) if (a[0]*a[3]-a[1]*a[2])%2==1]
V=list(itertools.product(range(2),repeat=2)); vi={v:i for i,v in enumerate(V)}
H=[g for g in G if mv(g,(1,0))==(1,0)]
reps=[]; remaining=set(G)
while remaining:
    r=min(remaining); reps.append(r); remaining-=set(mm(r,h) for h in H)
def plus(a,b): return [x+y for x,y in zip(a,b)]
def minus(a,b): return [x-y for x,y in zip(a,b)]
def act(g,a): return [a[vi[mv(inv(g),v)]] for v in V]
def N(a): return [a[vi[v]]+a[vi[((v[0]+1)%2,v[1])]] for v in V]
def Nr(r,a): return act(r,N(act(inv(r),a)))
m=[2,0,4,1]
def coc(g): return minus(act(g,m),m)
def sumv(vs):
    a=[0]*4
    for v in vs:a=plus(a,v)
    return a
u=sumv(Nr(r,coc(r)) for r in reps)
nonzero_coboundaries=0
for g in G:
    cor=[0]*4
    for r in reps:
        gr=mm(g,r)
        rr=next(t for t in reps if mm(inv(t),gr) in H)
        h=mm(inv(rr),gr)
        cor=plus(cor,act(rr,N(coc(h))))
    A_z=sumv(Nr(r,coc(g)) for r in reps)
    delta_u=minus(act(g,u),u)
    require(cor==plus(A_z,delta_u))
    nonzero_coboundaries+=any(delta_u)
require(nonzero_coboundaries>0)

# A retained residue-group toy model: R-localized F11^x has order5.
C=list(range(5))
require(all((pow(r,4)-1)%5==0 for r in range(1,25) if r%5))
require([x for x in C if (625*x-x)%5==0]==[0])
require(all((5**f-1)%5 for f in range(1,11)))
# F=Q(sqrt(-5)), 11 inert; its norm is121 and residue support has a5-part.
require(pow((-5)%11,5,11)==10)
require(121%5==1 and (121-1)%5==0)
report={'scope':'Finite independent algebra checks only; no claim that they prove geometric or arithmetic theorems.','kernel_incidence':inc,'transfer':{'group':'SL2(F2)','group_order':len(G),'subgroup_order':len(H),'cosets':len(reps),'coefficient_module':'Z-valued functions on F2^2','all_group_elements_checked':True,'nonzero_coboundary_cases':nonzero_coboundaries,'correction_u':u},'finite_field_constants':{'localized_F11_units_order':5,'eventual_scalar_norm_fixed':True,'T5_fixed_subgroup_trivial':True,'characteristic5_unit_orders_checked':[5**f-1 for f in range(1,11)]},'exceptional_residue_support_example':{'F':'Q(sqrt(-5))','rational_prime':11,'inert':True,'norm_q':121,'class_q':'principal','class_number':2,'residue_group':'two copies of F121^x','five_primary_support_not_excluded':True,'actual_cocycle_nonvanishing_claimed':False}}
Path(__file__).with_name('INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
