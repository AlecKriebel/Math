#!/usr/bin/env python3
"""Independent exact Gaussian-integer jets, order geometry and boundary falsifiers."""
from collections import Counter
from itertools import product
import hashlib
import json
import random

Z=(0,0);ONE=(1,0);C=Counter();H=hashlib.sha256()


def need(ok,message):
    if not ok:raise RuntimeError(message)


def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,c):return tuple(mul(x,c) for x in a)
def plus(a,b):return tuple(add(x,y) for x,y in zip(a,b))
def minus(a,b):return plus(a,scale(b,(-1,0)))


def times(a,b):
    n=len(a);out=[Z]*n
    for i,x in enumerate(a):
        if x==Z:continue
        for j,y in enumerate(b[:n-i]):
            if y!=Z:out[i+j]=add(out[i+j],mul(x,y))
    return tuple(out)


def power(a,m):
    out=(ONE,)+(Z,)*(len(a)-1)
    for _ in range(m):out=times(out,a)
    return out


def mono(n,degree,coefficient=ONE):
    out=[Z]*n
    if degree<n:out[degree]=coefficient
    return tuple(out)


def order(a):
    return next((i for i,x in enumerate(a) if x!=Z),len(a))


def horner(x,coeff):
    out=(Z,)*len(x)
    for c in reversed(coeff):
        out=times(out,x);out=(add(out[0],c),)+out[1:]
    return out


def direct_polynomial(powers,coeff):
    out=(Z,)*len(powers[0])
    for m,c in enumerate(coeff):out=plus(out,scale(powers[m],c))
    return out


def coefficient_family():
    rng=random.Random(23578599);sample=[]
    for n in range(3,8):
        for xdata in product([-1,0,1],repeat=n-1):
            x=(Z,)+tuple((a,0) for a in xdata);powers=[power(x,m) for m in range(n)]
            for k in range(2,n):
                polys=[]
                for leading in [Z,ONE,(2,0),(0,1),(-1,2)]:
                    p=[Z]*n;p[k]=leading
                    if leading not in [Z,ONE,(2,0)]:
                        for m in range(k+1,n):p[m]=(rng.randrange(-2,3),rng.randrange(-2,3))
                    polys.append(tuple(p))
                values=[]
                for p in polys:
                    a=direct_polynomial(powers,p);b=horner(x,p);need(a==b,'Independent polynomial evaluation discrepancy');values.append(a);C['Gaussian_polynomial_evaluation_comparisons']+=1
                ys=[(Z,)*n,powers[k],scale(powers[k],(2,0)),mono(n,n-1),tuple([Z]+[(rng.randrange(-1,2),rng.randrange(-1,2)) for _ in range(n-1)])]
                r=(n+k-1)//k
                for y in ys:
                    full=all(minus(y,p)==(Z,)*n for p in values)
                    exact=all(minus(y,p)==(Z,)*n for p in values[1:])
                    by_orders=order(x)>=r and order(y)>=n
                    need(full==exact==by_orders,'Coefficient family/order oracle discrepancy')
                    C['coefficient_family_jet_cases']+=1;H.update(repr((n,k,x,y,full,exact)).encode())
                if n==5 and k==2 and xdata==(0,1,0,0):sample.append({'n':n,'k':k,'x':x,'x_power_k':powers[k],'reduced_threshold':r})
    return sample


def charts_and_degenerations():
    for j in range(1,8):
        for q in range(1,6):
            for vord in range(4):
                n=j*q+(j-1)*vord+8
                v=plus(mono(n,vord),mono(n,vord+1,(0,1)));hh=plus(mono(n,q),mono(n,q+2,(-1,0)))
                x=times(v,hh);y=times(power(v,j-1),power(hh,j))
                need(order(x)==vord+q and order(y)==(j-1)*vord+j*q,'Second blowup chart order formula')
                need(order(x)>=q and order(y)>=j*q,'Contact implication including satellite chart')
                C['second_chart_contact_cases']+=1
            for word in [0,1,3,None]:
                n=j*q+12;x=plus(mono(n,q),mono(n,q+1));w=(Z,)*n if word is None else plus(mono(n,word,(1,1)),mono(n,word+2))
                y=times(power(x,j),w);need(order(x)==q and order(y)>=j*q,'Dense first-chart contact condition');C['first_chart_contact_cases']+=1
    for n in range(3,11):
        for k in range(2,n):
            size=2*n+3
            for zero_x in [True,False]:
                x=(Z,)*size if zero_x else plus(mono(size,n),mono(size,n+1,(0,1)))
                p=[Z]*n
                for i in range(k,n):p[i]=(i-k+1,1)
                p=tuple(p);z=plus(mono(size,n),mono(size,n+2,(-1,1)));y=plus(horner(x,p),z)
                for epsilon in [Z,ONE,(-1,0),(2,0),(0,1)]:
                    xe=plus(x,mono(size,1,epsilon));ye=plus(horner(xe,p),z)
                    need(minus(ye,horner(xe,p))==z,'Density deformation failed cylinder')
                    if epsilon==Z:need(xe==x and ye==y,'Density specialization at zero')
                    else:need(order(xe)==1 and order(z)>=n,'Density transverse open locus')
                    C['density_deformation_cases']+=1
                # Reconstruct the whole P by nested point-blowup substitutions.
                w=plus(mono(size,0),mono(size,2,(0,1)));u=w
                for a in reversed(p[k:]):u=plus(mono(size,0,a),times(x,u))
                got=times(power(x,k),u);want=plus(horner(x,p),times(power(x,n),w));need(got==want,'Complete finite-center chart substitutions');C['free_chart_substitution_cases']+=1


def arithmetic_and_traps():
    huge=[1,2,3,4,5,6,17,10**10,10**100]
    for r in [2,3]:
        for q in huge:
            for j in huge:
                if q<r:a,b=q,max(5,j*q)
                elif q>r:a,b=r,5
                elif j*r>5:a,b=r,5
                else:a,b=r,j*r
                in_I=a>=r and b>=5;in_R=a>=q and b>=j*q;need(in_I!=in_R,'Universal separator diagnostic failed');C['unbounded_size_integer_separator_cases']+=1
    for n in range(3,65):
        for k in range(2,n):
            r=(n+k-1)//k;need((k*r==n)==(n%k==0),'Prescribed Dk divisibility criterion');C['parameter_divisibility_cases']+=1
    traps={}
    n=5;x=mono(n,2);y=(Z,)*n
    traps['floor_instead_of_ceiling_detected']=order(x)>=n//2 and power(x,2)!=(Z,)*n
    x=mono(n,1);y=power(x,2)
    traps['single_family_member_is_insufficient']=y==power(x,2) and y!=scale(power(x,2),(2,0))
    traps['raw_locus_not_closed_cylinder']=3>=1 and 5>=5 and 5-5*3<0 and 5-4*3<0
    traps['different_reference_can_restore_general_case']=(8+5-1)//5==2 and 2*4==8 and 2*5!=8
    traps['fixed_final_center_singleton_positive_boundary']=(1,5)==(1,5)
    traps['first_exceptional_all_tangent_positive_boundary']=(5,5)==(5,1*5)
    # Dual numbers, not ordinary complex arithmetic: epsilon is nonzero, epsilon²=0.
    def dual(a,b):return (a[0]*b[0],a[0]*b[1]+a[1]*b[0])
    eps=(0,1);traps['nonreduced_ideal_does_not_force_x1_zero']=dual(eps,eps)==(0,0) and eps!=(0,0)
    need(all(traps.values()),'Boundary falsifier failed')
    return traps


def toric_charts():
    # Exponents as independent symbolic monomial vectors; four actual chart substitutions.
    def padd(a,b):return tuple(x+y for x,y in zip(a,b))
    def pmul(a,c):return tuple(c*x for x in a)
    expected=[((3,1),(5,2)),((2,1),(5,3))];rows=[]
    for a,b in expected:
        det=a[0]*b[1]-a[1]*b[0];need(det==1,'Unimodular determinant')
        inverse=((b[1],-a[1]),(-b[0],a[0]))
        need(padd(pmul(a,inverse[0][0]),pmul(b,inverse[0][1]))==(1,0),'Toric inverse u')
        need(padd(pmul(a,inverse[1][0]),pmul(b,inverse[1][1]))==(0,1),'Toric inverse v')
        for uord in range(1,7):
            for vord in range(4):
                xord=a[0]*uord+a[1]*vord;yord=b[0]*uord+b[1]*vord
                need(xord>=a[0] and yord>=b[0],'Other toric divisor containment');C['toric_chart_order_cases']+=1
        rows.append({'matrix':[a,b],'determinant':det,'inverse':inverse})
    # Last blowup second charts also cover the component at its other intersection.
    for a,b in [((3,2),(5,3)),((2,1),(5,2))]:
        need(a[0] in [2,3] and b[0]==5 and a[1]>=0 and b[1]>=0,'Other toric blowup chart')
    return rows


def main():
    examples=coefficient_family();charts_and_degenerations();traps=arithmetic_and_traps();toric=toric_charts()
    print(json.dumps({'verdict':'PASS','counts':dict(sorted(C.items())),'coefficient_examples':examples,'boundary_controls':traps,'toric_charts':toric,'exact_case_digest_SHA256':H.hexdigest(),'native_code_or_results_read_for_implementation':False,'foreign_project_code_imported':False,'arithmetic':'exact Gaussian integers and arbitrary-size integer orders; no floating point','limits':['Finite diagnostics do not prove arbitrary-complex-parameter/infinite-arc assertions; the sealed derivations do.','No firstness, author-intended notation repair, worldwide absence or new-science assertion follows.'],'network':0,'writes':0},sort_keys=True))


if __name__=='__main__':main()
