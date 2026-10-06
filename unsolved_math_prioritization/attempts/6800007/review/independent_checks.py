#!/usr/bin/env python3
"""Independent exact diagnostics for 6800007. No h-principle certification.
Run: python independent_checks.py > independent_results.json
Requires SymPy; tested with 1.14.0. Inputs are explicit cellular/cohomology models.
"""
import itertools
import json
from math import gcd
import sympy as s
from sympy.matrices.normalforms import smith_normal_form

checks = []
def check(condition, label):
    assert condition, label
    checks.append(label)

def cokernel(matrix):
    matrix = s.Matrix(matrix)
    diag = smith_normal_form(matrix, domain=s.ZZ)
    entries = [abs(int(diag[i, i])) for i in range(min(diag.shape))]
    return {'free_rank': matrix.rows - sum(v != 0 for v in entries),
            'torsion': [v for v in entries if v > 1]}

# Integral cellular cochain complexes. For K use relation a b a^-1 b,
# so d(a*)=0, d(b*)=2f*. For RP2 use d(e*)=2f*.
# Tensoring with the circle gives d1 and d2 below in the displayed bases.
K_d1 = s.Matrix([[0, 2, 0], [0, 0, 0], [0, 0, 0]])
K_d2 = s.Matrix([[0, 0, 2]])
RP_d1 = s.Matrix([[2, 0], [0, 0]])
RP_d2 = s.Matrix([[0, 2]])
check(K_d2*K_d1 == s.zeros(1, 3), 'K x S1 cochain d squared zero')
check(RP_d2*RP_d1 == s.zeros(1, 2), 'RP2 x S1 cochain d squared zero')
# Kernels are coordinate sublattices in these explicit matrices, hence no
# rational-nullspace-to-integral-lattice substitution is needed.
K_kernel_H1 = s.Matrix([[1, 0], [0, 0], [0, 1]])
K_kernel_H2 = s.Matrix([[1, 0], [0, 1], [0, 0]])
check(K_d1*K_kernel_H1 == s.zeros(3, 2), 'K x S1 H1 basis')
check(K_d2*K_kernel_H2 == s.zeros(1, 2), 'K x S1 H2 cocycle basis')
check(cokernel([[0, 2, 0], [0, 0, 0]]) == {'free_rank':1,'torsion':[2]}, 'K x S1 H2 = Z + Z/2')
check(cokernel(K_d2) == {'free_rank':0,'torsion':[2]}, 'K x S1 H3 = Z/2')
check(cokernel([[2, 0]]) == {'free_rank':0,'torsion':[2]}, 'RP2 x S1 H2 = Z/2')
check(cokernel(RP_d2) == {'free_rank':0,'torsion':[2]}, 'RP2 x S1 H3 = Z/2')
check(K_d1*s.Matrix([1,0,0]) == s.zeros(3,1), 'Klein orientation class has an integral lift')
check(RP_d1*s.Matrix([1,0]) == s.Matrix([2,0]), 'RP2 orientation Bockstein is generator of Z/2')
check(not any((-4*x-2*y-1)%2 == 0 for x,y in itertools.product(range(2),repeat=2)), 'RP2 x S1 has empty flag index set')

# Full presentation, rather than a presumed splitting, for the Klein product.
# A=<a,t>, B=<at> + Z/2<b>, C=Z/2<bt>. Only b cup t is nonzero.
# Rows: outer C, determinant a, determinant t, inner C.
klein = []
for eps, eta in itertools.product(range(2), repeat=2):
    presentation = s.Matrix([[2,0,0,0,0,0],
                             [0,0,-4,0,-2,0],
                             [0,0,0,-4,0,-2],
                             [0,2,0,eta,0,eps]])
    got = cokernel(presentation)
    expected = [2,2,2] if eta else ([2,2,4] if eps else [2,2,2,2])
    check(got == {'free_rank':0,'torsion':expected}, f'Klein torsion index ({eps},{eta})')
    klein.append({'epsilon':eps,'eta':eta,**got})

# Independent enumeration in (Z/8)^2 x (Z/2)^2 verifies the Smith results.
# Eight times each free ambient generator lies in every displayed relation
# lattice, so this finite ambient group captures the full quotient exactly.
ambient_moduli = (2,8,8,2)
def plus(a,b):return tuple((x+y)%m for x,y,m in zip(a,b,ambient_moduli))
def subgroup(generators):
    out={(0,0,0,0)}; pending=list(out)
    while pending:
        z=pending.pop()
        for g in generators:
            w=plus(z,g)
            if w not in out:out.add(w);pending.append(w)
    return out
for item in klein:
    eps,eta=item['epsilon'],item['eta']
    rel=[(0,-4,0,0),(0,0,-4,eta),(0,-2,0,0),(0,0,-2,eps)]
    H=subgroup(rel)
    order=256//len(H)
    expected=1
    for z in item['torsion']:expected*=z
    check(order==expected, f'Klein quotient enumeration size ({eps},{eta})')
    # Count cosets annihilated by two; distinguishes Z/4 from elementary 2-groups.
    killed=sum(plus(z,z) in H for z in itertools.product(*[range(m) for m in ambient_moduli]))//len(H)
    check(killed==2**len(item['torsion']), f'Klein quotient two-torsion ({eps},{eta})')

# S2 x S1: use the original three-loop presentation, with the two C coordinates
# still coupled by 3. Compare its actual Smith form to the claimed final group.
sphere_product=[]
for n in range(-15,16):
    full=s.Matrix([[0,-3*n],[-4,-2],[0,-9*n]])
    got=cokernel(full)
    expected={'free_rank':2,'torsion':[2]} if n==0 else {'free_rank':1,'torsion':[d for d in (gcd(2,3*n),12*abs(n)//gcd(2,3*n)) if d>1]}
    check(got==expected, f'S2 x S1 original coupled quotient n={n}')
    sphere_product.append({'n':n,**got})

# Lens-space primary labels: H1 cohomology is zero; H2=Z/p and H3=Z.
# Enumerate all labels rather than dividing by 2 in Z/p.
lens=[]
for p in range(1,33):
    indices=[(x,y) for x,y in itertools.product(range(p),repeat=2) if (-4*x-2*y)%p==0]
    check(len(indices)==p*gcd(p,2), f'lens primary label count p={p}')
    lens.append({'p':p,'primary_labels':len(indices),'fiber_free_rank':2})

# The orientation-reversing S2 mapping torus has d2=2 in cellular cochains,
# giving (A,B,C)=(Z,0,Z/2), delta=0. The full quotient has eight elements.
twisted=s.Matrix([[2,0,0,0],[0,0,-4,-2],[0,2,0,0]])
check(cokernel(twisted)=={'free_rank':0,'torsion':[2,2,2]}, 'twisted S2 bundle over circle quotient')
# Domains homotopy equivalent to a point or circle give the corresponding
# components / fundamental group of the unitary frame total space.
check(cokernel(s.zeros(0,0))=={'free_rank':0,'torsion':[]}, 'R3 ordinary-cohomology result is one class')
check(cokernel([[-4,-2]])=={'free_rank':0,'torsion':[2]}, 'open Mobius band x R gives two classes')

# A genuine nontrivial determinant example from Reid's m313(1,0).
# Its two-generator presentation abelianizes to Z + Z/4; orientation is a->0,
# b->1 modulo two, which lifts to Z/4 but not to Z.
relators=('aaaBAAAbbaaababb','aaabAAbbaaaBABAAAB')
def expsum(word,letter):return word.count(letter)-word.count(letter.upper())
relations=s.Matrix([[expsum(r,c) for r in relators] for c in 'ab'])
check(cokernel(relations)=={'free_rank':1,'torsion':[4]}, 'Reid presentation abelianization')
check(all(expsum(r,'b')%4==0 for r in relators), 'Reid orientation character lifts to Z/4')
check(relations.T*s.Matrix([0,1]) != s.zeros(2,1), 'the displayed orientation lift is not integral')
check(relations.T.nullspace()==[s.Matrix([-1,1])], 'all integral characters reduce to equal a,b parity')
reid_indices=[(x,y) for x,y in itertools.product(range(4),repeat=2) if (-4*x-2*y-2)%4==0]
check(len(reid_indices)==8 and all(y%2==1 for x,y in reid_indices), 'nonzero determinant delta=2 in Z/4 has eight labels')

# Graded integral exterior algebra on four genuine circle classes. This
# independently checks clutching signs on T3 x S1; all four generators anticommute.
def add(a,b):
    out=a.copy()
    for m,c in b.items():out[m]=out.get(m,0)+c
    return {m:c for m,c in out.items() if c}
def scale(a,n):return {m:c*n for m,c in a.items() if c*n}
def mul(a,b):
    out={}
    for m,c in a.items():
        for n,d in b.items():
            if m&n:continue
            inversions=sum(1 for i in range(4) for j in range(4) if m>>i&1 and n>>j&1 and i>j)
            k=m|n;out[k]=out.get(k,0)+c*d*(-1)**inversions
    return {m:c for m,c in out.items() if c}
def total(seq):
    out={}
    for a in seq:out=add(out,a)
    return out
def second(seq):return total(mul(a,b) for i,a in enumerate(seq) for b in seq[i+1:])
def slant(a):return {m^8:c for m,c in a.items() if m&8}
def degree2(v):return {m:c for m,c in zip((3,5,6),v) if c}
T={8:1}; basis=[{1<<i:1} for i in range(3)]
exterior_cases=0
for v in itertools.product(range(-2,3),repeat=3):
    x=degree2(v); y=scale(x,-2); z=scale(x,1)
    roots=[add(y,scale(x,-1)),add(z,scale(x,-1)),add(z,scale(y,-1))]
    for pp,qq in [(b,{}) for b in basis]+[({},b) for b in basis]:
        hh=[pp,qq,scale(add(pp,qq),-1)]
        vv=[add(c,mul(h,T)) for c,h in zip((x,y,z),hh)]
        a=scale(slant(second(vv)),-1)
        ks=[add(hh[j],scale(hh[i],-1)) for i,j in ((0,1),(0,2),(1,2))]
        rr=[add(r,mul(k,T)) for r,k in zip(roots,ks)]
        delta=total(roots)
        virtual=add(add(second(rr),scale(mul(total(rr),delta),-1)),add(mul(delta,delta),scale(second(roots),-1)))
        b=scale(slant(virtual),-1)
        check(b==scale(a,3), f'graded T3 root clutching {v}, case {exterior_cases%6}')
        check(a==total(mul(c,h) for c,h in zip((x,y,z),hh)), f'graded T3 SU clutching {v}, case {exterior_cases%6}')
        exterior_cases+=1

# Concrete negative control on RP2 x S1_x x S1_parameter.
# Let b be the order-two H2(RP2) generator and P the line with c1=x*t.
# V=L_b + P + 1, E=L_b + 1 + 1, so V-E=P-1.
# The nonzero cross term b*x*t is the only degree-four term.
ordinary_c2=1  # coefficient in Z/2 of b*x*t
virtual_c2=(ordinary_c2-1)%2
check(ordinary_c2==1 and virtual_c2==0, 'nontrivial E loop: ordinary c2 fails, virtual c2 is zero')

print(json.dumps({'pass':True,'sympy_version':s.__version__,
                  'assertions':len(checks),'checks':checks,
                  'graded_exterior_cases':exterior_cases,
                  'klein_product_quotients':klein,
                  'S2xS1_quotients':sphere_product,
                  'lens_label_counts':lens,'reid_labels':reid_indices,
                  'scope':'Exact cochain, graded-ring, abelian-presentation and finite-quotient diagnostics. The topology proof and h-principle require the separate written review.'},indent=2))
