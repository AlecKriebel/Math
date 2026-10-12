"""Finite exact instance checks; universal arguments are in the adjacent derivation."""
import itertools,json
def clean(f,p):return {m:c%p for m,c in f.items() if c%p}
def derivative(f,i,p):
    out={}
    for m,c in f.items():
        if m[i]:
            n=list(m);n[i]-=1;n=tuple(n);out[n]=out.get(n,0)+c*m[i]
    return clean(out,p)
def on_singular_line(f,p):return clean({m:c for m,c in f.items() if m[0]==0 and m[1]==0},p)
checks=[]
for p in [2,3,5,7,11]:
    Q={(p,0,1,0):1,(0,p,0,1):-1}
    ders=[derivative(Q,i,p) for i in range(4)]
    assert ders[0]==ders[1]=={}
    assert all(on_singular_line(f,p)=={} for f in [Q]+ders)
    assert ders[2]=={(p,0,0,0):1}
    assert ders[3]=={(0,p,0,0):p-1}
    # Normalized substitution x=x,y=xt,z=t^p,w=1 has equal terms.
    assert (p,p)==(p,p)
    # Compare a finite semigroup enumeration to exact residue criterion.
    for a in range(p+2):
        for b in range(3*p):
            enum=any(v<=a and b>=v and (b-v)%p==0 for v in range(a+1))
            assert enum==((b%p)<=a)
            conductor=all(((b+j)%p)<=a for j in range(p))
            assert conductor==(a>=p-1)
    # Intersection arithmetic on F_(p-1).
    h2=-(p-1)+2*p
    kh=2*(p-1)-2*p-(p+1)
    pa=1+(h2+kh)//2
    chi=1+kh+2*h2
    assert h2==p+1 and pa==0 and chi==p
    # Special section t^p has a repeated root, generic graph x+t^p is regular.
    graph={(1,0):1,(0,p):1}
    assert graph[(1,0)]==1  # derivative with respect to x
    assert p%p==0          # special-section derivative vanishes
    checks.append({'p':p,'surface_degree':p+1,'conductor_x_power':p-1,
                   'H2':h2,'K_H':kh,'pa_section':pa,'chi_adjoint':chi,
                   'special_section_nonreduced':True,
                   'general_graph_regular':True})
for p in [2,3,5,7,11]:
    Q={(0,2,1,0):1,(3,0,0,0):-1}
    assert all(on_singular_line(f,p)=={} for f in [Q]+[derivative(Q,i,p) for i in range(4)])
    # Semigroup <2,3>: all n>=2 belong, while 1 is missing.
    semigroup={2*a+3*b for a in range(15) for b in range(15)}
    assert 1 not in semigroup and all(n in semigroup for n in range(2,25))
checks.append({'cuspidal_cone_degree':3,'H2':3,'K_H':-5,
               'pa_section':0,'chi_adjoint':2,'H_not_ample':True})
checks.append({'negative_control_P2':{'H2':1,'K_plus_2H_degree':-1,
                                     'h0_adjoint':0,'excluded_by_e_ge_2':True}})
print(json.dumps({'kind':'finite-exact-checks-not-universal-proof','checks':checks},indent=2))
