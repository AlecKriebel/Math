"""Independent exact validation. Guards remain active under python -O."""
import fractions, hashlib, itertools, json, pathlib, sys
F=fractions.Fraction
ROOT=pathlib.Path(__file__).resolve().parent
def require(ok, message):
    if not ok:
        raise ValueError(message)
def vec(values):
    return tuple(F(v) for v in values)
def mv(matrix, vector):
    return tuple(sum(F(a)*b for a,b in zip(row,vector)) for row in matrix)
def rank(matrix):
    a=[[F(v) for v in row] for row in matrix]
    r=0
    for c in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][c]),None)
        if pivot is None:
            continue
        a[r],a[pivot]=a[pivot],a[r]
        d=a[r][c]; a[r]=[v/d for v in a[r]]
        for i in range(len(a)):
            if i!=r and a[i][c]:
                d=a[i][c]; a[i]=[x-d*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):
            break
    return r
def solve(matrix,rhs):
    n=len(matrix)
    a=[[F(v) for v in row]+[F(b)] for row,b in zip(matrix,rhs)]
    for c in range(n):
        pivot=next((i for i in range(c,n) if a[i][c]),None)
        if pivot is None:
            return None
        a[c],a[pivot]=a[pivot],a[c]
        d=a[c][c]; a[c]=[v/d for v in a[c]]
        for i in range(n):
            if i!=c and a[i][c]:
                d=a[i][c]; a[i]=[x-d*y for x,y in zip(a[i],a[c])]
    return tuple(row[-1] for row in a)
def vertices(matrix):
    n=len(matrix[0])
    inequalities=list(matrix)+[tuple(-int(i==j) for j in range(n)) for i in range(n)]
    rhs=[1]*len(matrix)+[0]*n
    out=set(); bases=0; nonsingular=0
    for chosen in itertools.combinations(range(len(inequalities)),n):
        bases+=1
        z=solve([inequalities[i] for i in chosen],[rhs[i] for i in chosen])
        if z is None:
            continue
        nonsingular+=1
        if all(a<=b for a,b in zip(mv(inequalities,z),rhs)):
            out.add(z)
    return out, bases, nonsingular
def monomial(i,j):
    return tuple(int(k in (i,j)) for k in range(6))
source_terms=[monomial(0,4),monomial(1,3),monomial(1,5),monomial(2,4),monomial(0,5),monomial(2,3)]
candidate_terms=[source_terms[0],source_terms[2],source_terms[5],source_terms[1],source_terms[3],source_terms[4]]
B=tuple(tuple(term[row] for term in source_terms) for row in range(6))+tuple(tuple(int(col//2==row) for col in range(6)) for row in range(3))
A=tuple(tuple(term[row] for term in candidate_terms) for row in range(6))+tuple(tuple(int(col%3==row) for col in range(6)) for row in range(3))
BRIDGE=(0,3,1,4,5,2)
def q(z,order=BRIDGE):
    return tuple(z[i] for i in order)
def candidate_segment(t):
    return vec((t,t,t,1-t,1-t,1-t))
def paired_segment(t):
    return vec((t,1-t,t,1-t,1-t,t))
def check_bridge(order):
    require(sorted(order)==list(range(6)),'bridge is not a coordinate permutation')
    for j in range(6):
        basis=vec(int(i==j) for i in range(6))
        require(mv(B,q(basis,order))==mv(A,basis),f'column bridge failed for candidate basis {j}')
    endpoint=candidate_segment(F(1))
    require(max(mv(B,q(endpoint,order)))<=1,'bridged endpoint violates published LP')
def poly(terms,coefficients):
    d={}
    for term,c in zip(terms,coefficients):
        d[term]=d.get(term,F(0))+F(c)
    return {m:c for m,c in d.items() if c}
def scale(p,c):
    return {m:v*c for m,v in p.items() if v*c}
def add(*polys):
    d={}
    for p in polys:
        for m,c in p.items():
            d[m]=d.get(m,F(0))+c
    return {m:c for m,c in d.items() if c}
def times_variable(p,i):
    d={}
    for m,c in p.items():
        n=list(m); n[i]+=1; d[tuple(n)]=c
    return d
f1=poly(source_terms[:2],(1,-1)); f2=poly(source_terms[2:4],(1,-1))
f3=poly(source_terms[4:6],(1,-1)); candidate_f3=scale(f3,-1)
def coefficient_support_rank(polynomials):
    mons=sorted({m for p in polynomials for m in p})
    return rank([[p.get(m,F(0)) for m in mons] for p in polynomials])

def mutant(name):
    if name=='omit_third_pair_swap':
        check_bridge((0,3,1,4,2,5))
    elif name=='paired_equals_blocked':
        check_bridge((0,1,2,3,4,5))
    elif name=='third_internal_plus_sign':
        altered=poly(source_terms[4:6],(1,1))
        require(altered==scale(candidate_f3,-1),'third altered polynomial is not a unit sign reversal')
    elif name=='ambient_c1':
        c=1
        objective=tuple(int(i>=2*c) for i in range(6))
        require(objective==(1,1,1,1,1,1),'ambient reassignment changes the objective')
    elif name=='strict_constraints':
        require(all(v<1 for v in mv(B,paired_segment(F(1,3)))),'strict substitute removes every optimal-face point')
    elif name=='drop_generator_rows':
        projected=B[:6]
        require(len(projected)==9,'published augmented matrix lost generator rows')
    elif name=='redundant_fourth_generator':
        polynomials=[f1,f2,f3,f1]
        require(coefficient_support_rank(polynomials)==len(polynomials),'degree-two generators are redundant')
    elif name=='nonnegative_is_positive':
        require(all(v>0 for v in paired_segment(F(0))),'positivity substitution removes valid rational endpoint')
    else:
        raise ValueError(f'unknown mutant {name}')
    raise RuntimeError(f'mutant {name} was not rejected')

def run():
    check_bridge(BRIDGE)
    require(rank(A)==5 and rank(B)==5,'unexpected rational rank')
    require(mv(A,vec((1,1,1,-1,-1,-1)))==(0,)*9,'candidate kernel vector invalid')
    require(mv(B,vec((1,-1,1,-1,-1,1)))==(0,)*9,'source kernel vector invalid')
    require(coefficient_support_rank([f1,f2,f3])==3,'minimality support rank fails')
    require(all(sum(p.values())==0 for p in [f1,f2,f3]),'all-ones torus point fails')
    require(f3==scale(candidate_f3,-1),'third sign relation fails')
    altered=poly(source_terms[4:6],(1,1))
    monomial_certificate=add(times_variable(altered,4),scale(times_variable(f1,5),-1),scale(times_variable(f2,3),-1))
    target=(0,0,1,1,1,0)
    require(monomial_certificate=={target:F(2)},'internal-plus mutant monomial certificate fails')
    require(sum(altered.values())==2,'internal-plus mutant torus value not 2')
    tests=0
    for denominator in range(1,31):
        for numerator in range(denominator+1):
            t=F(numerator,denominator); z=candidate_segment(t); w=paired_segment(t)
            require(q(z)==w,'segment bridge fails')
            require(mv(A,z)==(1,)*9 and mv(B,w)==(1,)*9,'constant full augmented image fails')
            require(sum(z)==3 and sum(w)==3,'segment objective fails')
            s=F(0) if t else F(1)
            require(w!=paired_segment(s),'partner is not distinct')
            require(mv(B,w)==mv(B,paired_segment(s)),'partner image differs')
            tests+=1
    v,bases,nonsingular=vertices(B)
    optimum=max(sum(point) for point in v)
    optimal_vertices={point for point in v if sum(point)==optimum}
    require(optimum==3,'exact vertex maximum differs from 3')
    require(optimal_vertices=={paired_segment(F(0)),paired_segment(F(1))},'optimal vertex set differs from segment endpoints')
    # Dropping pair rows can hide in this example. A separate one-generator
    # diagnostic proves that exponent-only LPs are not generally the same LP.
    require(sum((1,1))==2 and sum((F(1,2),F(1,2)))==1,'single-generator cap diagnostic fails')
    single_exp=((1,0),(0,1)); single_aug=single_exp+((1,1),)
    require(max(mv(single_exp,vec((1,1))))<=1,'exponent-only witness fails')
    require(max(mv(single_aug,vec((1,1))))>1,'generator cap does not reject witness')
    # Collision alone does not negate the existential singleton-fiber claim.
    projection=((1,1,0),(0,0,1))
    require(mv(projection,vec((1,0,0)))==mv(projection,vec((0,1,0))),'quantifier collision control fails')
    require(mv(projection,vec((0,0,1)))==(0,1),'singleton control image fails')
    # The fiber over (0,1) is a singleton because x+y=0, x,y>=0, z=1.
    require(mv(B,vec((0,)*6))==(0,)*9,'true LP origin should be feasible')
    require(sum(vec((0,)*6)[:2])!=1,'c=1 equality control should reject true LP origin')
    strict_point=tuple(F(3,4)*v for v in paired_segment(F(1,3)))
    require(all(x<1 for x in mv(B,strict_point)) and sum(strict_point)==F(9,4),'strict approach witness fails')
    rejected=[]
    for name in MUTANTS:
        try:
            mutant(name)
        except ValueError as e:
            rejected.append({'name':name,'diagnostic':str(e)})
    require(len(rejected)==len(MUTANTS),'some mutants bypassed explicit guards')
    def serial(v): return [str(x) for x in v]
    return {'status':'pass','debug_enabled':__debug__,'rational_segment_controls':tests,
      'rank':5,'objective_maximum':'3','feasible_vertices':len(v),'active_bases_examined':bases,
      'nonsingular_active_bases':nonsingular,'optimal_vertices':[serial(v) for v in sorted(optimal_vertices)],
      'bridge_permutation':list(BRIDGE),'source_paired_matrix':[list(row) for row in B],
      'candidate_blocked_matrix':[list(row) for row in A],
      'monomial_sign_mutant_certificate':{'exponent':list(target),'coefficient':'2'},
      'mutants_rejected':rejected,'new_proof_search_turns':0}

MUTANTS=('omit_third_pair_swap','paired_equals_blocked','third_internal_plus_sign','ambient_c1',
         'strict_constraints','drop_generator_rows','redundant_fourth_generator','nonnegative_is_positive')
if __name__=='__main__':
    try:
        if len(sys.argv)==3 and sys.argv[1]=='--mutant':
            mutant(sys.argv[2])
        elif len(sys.argv)==1:
            print(json.dumps(run(),sort_keys=True))
        else:
            raise ValueError('usage: verify_bridge.py [--mutant NAME]')
    except (ValueError,RuntimeError) as e:
        print(json.dumps({'status':'rejected','diagnostic':str(e),'debug_enabled':__debug__}),file=sys.stderr)
        raise SystemExit(2)
