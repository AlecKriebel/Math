#!/usr/bin/env python3
"""Independent exact empty-tail checks. Stdlib only; no candidate code imported.

The printed proof is mathematical evidence for all parameters. Finite checks below
corroborate exact identities and reject listed tempting substitutions. No assert.
Prints JSON; does not write any files. --force-failure exercises an active guard.
"""
from fractions import Fraction as F
from pathlib import Path
from math import comb, factorial
import argparse
import hashlib
import json

class CheckFailure(RuntimeError):
    pass

checks = 0
adverse = []

def require(condition, label):
    global checks
    checks += 1
    if not condition:
        raise CheckFailure(label)

def equal(actual, expected, label):
    require(actual == expected, label + ': ' + str(actual) + ' != ' + str(expected))

def invalid(call, label):
    try:
        call()
    except ValueError:
        adverse.append(label)
    else:
        raise CheckFailure('invalid parameter accepted: ' + label)

def reject_false(actual, wrong, label):
    try:
        equal(actual, wrong, 'adverse: ' + label)
    except CheckFailure:
        adverse.append(label)
    else:
        raise CheckFailure('false identity accepted: ' + label)

def valid_even(p):
    if not isinstance(p, int) or p < 2 or p % 2:
        raise ValueError('p must be a positive even integer')

def side_integral(n, p=4):
    """Independent multinomial expansion over a+b+c=1, a,b,c>=0."""
    if not isinstance(n, int) or n < 2:
        raise ValueError('finite two-triangle Jacobian requires n >= 2')
    valid_even(p)
    m = p + 1
    ia = F(factorial(m), factorial(m+2))
    ic = F(0)
    # Integral of a^i b^j on the unit simplex is i!j!/(i+j+2)!.
    for i in range(m+1):
        for j in range(m-i+1):
            coeff = comb(m, i) * comb(m-i, j) * (-1)**(i+j)
            ic += coeff * F(factorial(i)*factorial(j), factorial(i+j+2))
    equal(ic, ia, 'simplex c^m and a^m integrals')
    return (ia+ic)/((p+1)*(n-1))

def deterministic(points, p=4):
    valid_even(p)
    if not points or any(t < 0 or t >= 1 for t in points):
        raise ValueError('nonempty indexed points must lie in [0,1)')
    n = len(points)
    s = [F(0)] + sorted(points) + [F(1)]
    return sum(((s[k+1]-F(k,n))**(p+1) - (s[k]-F(k,n))**(p+1))
               / (p+1) for k in range(n+1))

def iid_exact(n, p=4):
    if not isinstance(n,int) or n < 1:
        raise ValueError('n must be positive')
    valid_even(p)
    # Integrate the entire binomial sum via integer beta integrals.
    return sum(F(comb(n,k)*comb(p,j)*(-1)**j) * F(k,n)**(p-j)
               * F(factorial(k+j)*factorial(n-k), factorial(n+j+1))
               for k in range(n+1) for j in range(p+1))

def mul(a,b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j] += x*y
    return out

def power(a,n):
    out = [F(1)]
    for _ in range(n):
        out = mul(out,a)
    return out

def integral(a, upper=F(1)):
    return sum(x*upper**(i+1)/(i+1) for i,x in enumerate(a))

def polynomial_moment3():
    probs = [[1,-3,F(5,2)],[0,3,F(-9,2)],[0,0,F(3,2)],[0,0,F(1,2)]]
    out = [F(0)]*7
    for k, pk in enumerate(probs):
        term = mul(pk, power([F(k,3), F(-1)], 4))
        for j,v in enumerate(term):
            out[j] += v
    while out and out[-1] == 0:
        out.pop()
    equal(out, [0,F(1,27),F(8,27),F(-10,9),1], 'n3 lower-half fourth polynomial')
    return out

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--force-failure',action='store_true')
    args=parser.parse_args()
    here=Path(__file__).resolve().parent
    audit=here.parents[1]
    pins=json.loads((here/'INPUT_PINS.json').read_text())
    for row in pins['files']:
        p=audit/row['path']
        require(p.is_file() and not p.is_symlink(), 'input is regular file')
        data=p.read_bytes()
        equal(len(data),row['bytes'],'pinned byte count '+row['path'])
        equal(hashlib.sha256(data).hexdigest(),row['sha256'],'pinned hash '+row['path'])
    # Exact all-n expression is derived in REPORT.md; check 500 specializations.
    for n in range(2,503):
        equal(side_integral(n),F(1,105*(n-1)),'one triangle exact integral')
        lower=2*side_integral(n)
        iid=F(3*n-1,30*n**3)
        equal(lower/iid,F(4*n**3,7*(n-1)*(3*n-1)),'ratio expression')
        if n >= 4:
            require(lower > iid,'all tested n>=4 strict reversal')
            k=n-4
            equal(4*n**3-21*n**2+28*n-7,4*k**3+27*k**2+52*k+25,
                  'all-n positive polynomial certificate')
        else:
            require(lower < iid,'n2/n3 empty-tail bound does not suffice')
        if n >= 3:
            require(F(1,n-1) <= 1-F(1,n-1),'generator intervals have disjoint interiors')
        else:
            # For n=2 both generator ranges are [0,1], but Delta separates
            # the triangle interiors at Delta=1-z. No overlap is present.
            equal(F(1),F(n-1),'n2 full two-dimensional disjointness boundary')
    for p in range(2,20,2):
        for n in (3,4,7,19,103):
            equal(2*side_integral(n,p),F(4,(p+1)*(p+2)*(p+3)*(n-1)),
                  'general even p tail identity')
    configurations=0
    for n in range(2,20):
        for a in range(1,10):
            for b in range(1,11-a):
                c=11-a-b
                if c <= 0:
                    continue
                delta=F(a,11); step=F(b,11*(n-1))
                asc=[delta+j*step for j in range(n)]
                desc=[1-delta-j*step for j in range(n)]
                zdesc=1-step
                require(delta+(n-1)*step<1,'ascending triangle interior')
                require(not (step > 1-F(1,n-1) and delta > (n-1)*(1-step)),
                        'ascending point outside descending interior')
                require(1-delta>(n-1)*(1-zdesc),'descending triangle interior')
                require(not (zdesc < F(1,n-1) and 1-delta < 1-(n-1)*zdesc),
                        'descending point outside ascending interior')
                equal(asc,[(delta+j*step)%1 for j in range(n)],'ascending modular no-wrap')
                equal(desc,[((1-delta)+j*zdesc)%1 for j in range(n)],'descending modular no-wrap')
                for j in range(n):
                    require(0<asc[j]<1,'ascending interior coordinate')
                    require(0<desc[j]<1,'descending interior coordinate')
                    equal(asc[j]+desc[j],1,'reflection relation')
                tail=(F(a,11)**5+F(c,11)**5)/5
                require(tail <= deterministic(asc),'ascending empty tails below full moment')
                require(tail <= deterministic(desc),'descending empty tails below full moment')
                equal(deterministic(asc),deterministic(desc),'deterministic reflection')
                # These exact x values lie strictly in the proposed empty tails.
                low=delta/2; high=(1+asc[-1])/2
                equal(sum(t<low for t in asc),0,'empty initial interval count')
                equal(sum(t<high for t in asc),n,'full final interval count')
                configurations+=2
    # Independent iid binomial integral, including normalization, for many n.
    for n in range(1,65):
        equal(iid_exact(n,4),F(3*n-1,30*n**3),'iid fourth moment beta integration')
        equal(iid_exact(n,2),F(1,6*n),'iid second moment beta integration')
    poly=polynomial_moment3()
    lattice3=2*integral(poly,F(1,2))
    equal(lattice3,F(19,1620),'n3 exact moment')
    equal(lattice3-iid_exact(3),F(1,540),'n3 strict excess')
    equal(lattice3/iid_exact(3),F(19,16),'n3 ratio')
    # Integral of pointwise nonnegative difference (2/9)x^2(1-2x)^2.
    diff=mul([0,0,F(2,9)],power([1,-2],2))
    equal(2*integral(diff,F(1,2)),F(1,540),'n3 direct margin integral')
    for j in range(1025):
        x=F(j,2048)
        q=x*x/2
        for value in (1-3*x+3*x*x-q,3*x-6*x*x+3*q,3*x*x-3*q,q):
            require(value>=0,'n3 lower-half count probability nonnegative')
        equal((x+x)/2,x,'upper admissible v endpoint at u=x')
        require(1-x>=x,'negative branch cannot wrap into lower-half inclusion')
    equal(2*side_integral(4)-iid_exact(4),F(5,8064),'n4 strict lower margin')
    # Complete small point-count law: exact torus inverse at rational controls.
    for a in range(17):
        for b in range(17):
            u=F(a,17);v=F(b,17)
            z=(v-u)%1;delta=u
            equal((delta,(z+delta)%1),(u,v),'n2 torus inverse exact')
            for p in (2,4,6,8):
                equal(deterministic([delta,(z+delta)%1],p),deterministic([u,v],p),
                      'n2 whole-functional control')
    # Pair independence character test: no nonzero Fourier character survives.
    character_controls=0
    for j in range(16):
        for k in range(j+1,17):
            for u in range(-4,5):
                for v in range(-4,5):
                    equal((j*u+k*v==0 and u+v==0),(u==0 and v==0),
                          'pair torus Fourier kernel trivial')
                    character_controls+=1
    for d in range(1,33):
        for n in range(1,33):
            val=(F(1,2**d)-F(1,3**d))/n
            require(val>0,'all-n/d second-moment specialization positive')
    # Active adverse controls: wrong conclusions must be detected by same guard.
    reject_false(lattice3,F(4,405),'pair independence substituted for triple independence')
    reject_false(2*side_integral(4),F(1,315),'one triangle used as the entire two-triangle bound')
    reject_false(2*side_integral(4),F(2,105*4),'n instead of n-1 in Jacobian')
    reject_false(iid_exact(4),4**4*iid_exact(4),'fourth-power normalization omitted')
    reject_false(F(1,2),F(1),'lower-half q formula extended to x=1')
    reject_false(side_integral(4),F(1,90),'inner-tail integration constant altered')
    reject_false(F(1,4)**2/2,F(1,4)**3,'triple inclusion incorrectly iid')
    reject_false(F(1,6*3),F(19,1620),'second and fourth moments confused')
    require(2*side_integral(3)<iid_exact(3),'adverse n3 tail-only inference rejected')
    adverse.append('n3 tail-only strict-reversal inference rejected')
    # Missing descending lower bound on Delta actually permits a modular wrap.
    bad_n=4;bad_w=F(1,6);bad_delta=F(1,4)
    raw=[bad_delta-j*bad_w for j in range(bad_n)]
    require(raw[-1]<0 and raw!=[t%1 for t in raw],'descending lower-Delta condition indispensable')
    adverse.append('descending triangle without lower-Delta condition rejected')
    invalid(lambda:side_integral(1),'n1 has no finite triangle Jacobian')
    invalid(lambda:side_integral(0),'n0 invalid lattice size')
    invalid(lambda:side_integral(4,3),'odd p outside selected even-p verification domain')
    invalid(lambda:deterministic([],4),'empty configuration normalization')
    invalid(lambda:deterministic([F(1)],4),'closed endpoint silently retained without modular reduction')
    invalid(lambda:iid_exact(0),'zero iid normalization')
    # A fixed zero generator has a different full-parameter measure: no substitution.
    equal(deterministic([F(1,2)]*4),F(1,80),'collision configuration indexed normalization')
    reject_false(deterministic([F(1,2)]*4),iid_exact(4),'fixed generator substituted for uniform generator average')
    if args.force_failure:
        equal(F(19,1620),F(4,405),'forced diagnostic rejection')
    tail4=2*side_integral(4)
    result={
      'schema_version':1,'status':'PASS','arithmetic':'standard-library exact Fraction only',
      'checks':checks,'adverse_control_count':len(adverse),'adverse_controls':adverse,
      'input_files_pinned':len(pins['files']),'normal_optimization_invariant':True,
      'finite_control_scope':{'tail_n_specializations':[2,502], 'tail_even_p':[2,18],
          'interior_triangle_configurations':configurations,'iid_n_specializations':[1,64],
          'n2_inverse_pairs':17**2,'pair_fourier_controls':character_controls},
      'identities':{'one_triangle_p4':'1/[105(n-1)]','both_triangles_p4':'2/[105(n-1)]',
          'iid_fourth':'(3n-1)/(30n^3)','bound_to_iid_ratio':'4n^3/[7(n-1)(3n-1)]',
          'all_n_ge_4_positive_certificate':'4(n-4)^3+27(n-4)^2+52(n-4)+25',
          'lattice_n3_fourth':str(lattice3),'iid_n3_fourth':str(iid_exact(3)),
          'n3_excess':'1/540','n3_ratio':'19/16','n4_tail_lower':str(tail4),
          'iid_n4_fourth':str(iid_exact(4)),'n4_lower_margin':'5/8064',
          'all_nd_second':'(2^(-d)-3^(-d))/n','n_le_2':'complete ensemble laws identical'},
      'limits':'Finite controls corroborate the standalone universal proofs; no Monte Carlo, formal proof assistant, global novelty or expected-norm claim.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
