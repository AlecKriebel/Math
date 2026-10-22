#!/usr/bin/env python3
"""Independent exact finite audit. Python >= 3.10; standard library only.

No assert statements: every requirement raises AuditFailure under python -O too.
The source proof is read only to verify bytes. No executable historical checker
or data is imported. All operations are authored here from the mathematical law.
"""
from collections import Counter, deque
from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json
import sys
import time

HERE = Path(__file__).resolve().parent
PROOF = HERE.parent.parent / 'inputs' / 'PROOF.md'
EXPECTED = '68c040d5bfe5d536e6f33f0f319a2d721bac5c562ec60f802fc516f293205b75'
COUNTS = Counter()
STAGES = []
class AuditFailure(Exception):
    pass

def need(condition, label, witness=None):
    COUNTS[label] += 1
    if not condition:
        raise AuditFailure(json.dumps({'label': label, 'witness': witness}, sort_keys=True))

def stamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

def stage(name, function):
    before = sum(COUNTS.values())
    start = time.monotonic()
    result = function()
    record = {'name': name, 'status': 'PASS', 'guards': sum(COUNTS.values())-before,
              'seconds': round(time.monotonic()-start, 3), 'details': result}
    STAGES.append(record)
    print(json.dumps(record, sort_keys=True), flush=True)

# Four coefficients of x,x^2,x^3,x^4, in little-endian base five.
COEFF = tuple(tuple((i // (5 ** j)) % 5 for j in range(4)) for i in range(625))
def encode(coeff):
    return sum((a % 5) * (5 ** i) for i, a in enumerate(coeff))

def poly_add(a, b):
    return encode(tuple(x+y for x,y in zip(COEFF[a], COEFF[b])))

def poly_mul(a, b):
    out = [0]*4
    for i, x in enumerate(COEFF[a], 1):
        for j, y in enumerate(COEFF[b], 1):
            if i+j < 5:
                out[i+j-1] += x*y
    return encode(out)

def scale_ring(a, n):
    return encode(tuple(n*x for x in COEFF[a]))

ADD = []
MUL = []
LOG = []
EXP = []
SIG = tuple(encode(tuple((-1)**(j+1)*c for j,c in enumerate(COEFF[a]))) for a in range(625))
NEG = tuple(scale_ring(a, -1) for a in range(625))
V = tuple(i for i in range(32) if i.bit_count() % 2 == 0)
VBASIS = (17, 18, 20, 24)
Q = {v: (v.bit_count()//2) % 2 for v in V}
def beta(v,w):
    return (v&w).bit_count() % 2

def rotate(v):
    return ((v << 1) & 31) | (v >> 4)

ROT = {}
for s in range(5):
    for v in V:
        w=v
        for _ in range(s):
            w=rotate(w)
        ROT[s,v]=w

ZERO = (0,0,0)
X = (1,0,0)
A = (125,0,0)
B = (0,0,1)
BASIS = tuple((5**j,0,0) for j in range(4)) + tuple((0,v,0) for v in VBASIS) + (B,)
ELEMENTS = tuple((r,v,z) for r in range(625) for v in V for z in range(2))

def ring_circle(r,u):
    return ADD[ADD[r][u]][MUL[r][u]]

def eta(r):
    return COEFF[LOG[r]][3]

def add(a,b):
    r,v,z=a; u,w,Z=b
    return ADD[r][u], v^w, z^Z

def neg(a):
    return NEG[a[0]], a[1], a[2]

def sub(a,b):
    return add(a,neg(b))

def scale(a,n):
    return scale_ring(a[0],n), a[1] if n%2 else 0, a[2] if n%2 else 0

def circle(a,b, mutation=None):
    r,v,z=a; u,w,Z=b
    e=z^Q[v]
    s=eta(r)
    if mutation == 'drop_Q': e=z
    if mutation == 'raw_a4': s=COEFF[r][3]
    if mutation == 'sigma_identity': e=0
    if mutation == 'M_identity': s=0
    uu=SIG[u] if e else u
    ww=ROT[s,w]
    zz=z^Z^beta(v,ww)
    if mutation == 'drop_beta': zz=z^Z
    return ADD[ADD[r][uu]][MUL[r][uu]], v^ww, zz

def lam(a,b):
    r,v,z=a; u,w,Z=b
    uu=SIG[u] if z^Q[v] else u
    ww=ROT[eta(r),w]
    return ADD[uu][MUL[r][uu]], ww, Z^beta(v,ww)

def star(a,b):
    # Deliberately compute from direct circle and additive subtraction.
    return sub(sub(circle(a,b),a),b)

# Independent coordinates for G0: k1,k2,k3,e,v,s.
GZERO=(0,0,0,0,0,0)
def psi(a):
    l=COEFF[LOG[a[0]]]
    return l[0],l[1],l[2],a[2]^Q[a[1]],a[1],l[3]

def unpsi(g):
    k1,k2,k3,e,v,s=g
    return EXP[encode((k1,k2,k3,s))],v,e^Q[v]

def gmul(a,b):
    k1,k2,k3,e,v,s=a; h1,h2,h3,f,w,t=b
    sign=-1 if e else 1
    return ((k1+sign*h1)%5,(k2+h2)%5,(k3+sign*h3)%5,e^f,v^ROT[s,w],(s+t)%5)

def ginv(a):
    k1,k2,k3,e,v,s=a
    sign=-1 if e else 1
    return ((-sign*k1)%5,(-k2)%5,(-sign*k3)%5,e,ROT[(-s)%5,v],(-s)%5)

def inv(a):
    return unpsi(ginv(psi(a)))

def comm(a,b):
    return circle(circle(circle(a,b),inv(a)),inv(b))

def setup():
    need(sha256(PROOF.read_bytes()).hexdigest()==EXPECTED,'frozen_input_hash')
    for a in range(625):
        ADD.append([poly_add(a,b) for b in range(625)])
        MUL.append([poly_mul(a,b) for b in range(625)])
    for a in range(625):
        powers=[a]
        for _ in range(3): powers.append(MUL[powers[-1]][a])
        # Coefficients computed from inverses in F5, rather than copied decimals.
        logarithm=0; exponential=0
        factorial=1
        for n,power in enumerate(powers,1):
            logarithm=ADD[logarithm][scale_ring(power,(-1)**(n+1)*pow(n,-1,5))]
            factorial*=n
            exponential=ADD[exponential][scale_ring(power,pow(factorial,-1,5))]
        LOG.append(logarithm); EXP.append(exponential)
    return {'ring_size':625,'V_size':len(V),'brace_size':len(ELEMENTS)}

def ingredients():
    need(len(set(LOG))==625 and len(set(EXP))==625,'log_exp_bijections')
    for r in range(625):
        need(LOG[EXP[r]]==r and EXP[LOG[r]]==r,'log_exp_inverse',r)
        a1,a2,a3,a4=COEFF[r]
        closed=(a4-a1*a3-a2*a2*pow(2,-1,5)+a1*a1*a2-a1**4*pow(4,-1,5))%5
        need(eta(r)==closed,'eta_closed_formula',r)
        need(LOG[SIG[r]]==SIG[LOG[r]],'log_sigma',r)
        need(eta(SIG[r])==eta(r),'eta_sigma',r)
        need(SIG[SIG[r]]==r,'sigma_involution',r)
        for u in range(625):
            c=ring_circle(r,u)
            need(LOG[c]==ADD[LOG[r]][LOG[u]],'log_circle_homomorphism',(r,u))
            need(SIG[ADD[r][u]]==ADD[SIG[r]][SIG[u]],'sigma_additive',(r,u))
            need(SIG[MUL[r][u]]==MUL[SIG[r]][SIG[u]],'sigma_multiplicative',(r,u))
    for v,w in product(V,repeat=2):
        need(Q[v^w]==(Q[v]^Q[w]^beta(v,w)),'Q_polarization',(v,w))
        need(beta(v,w)==beta(w,v),'beta_symmetric',(v,w))
        for u in V:
            need(beta(v^w,u)==(beta(v,u)^beta(w,u)),'beta_bilinear',(v,w,u))
        for s in range(5):
            need(beta(ROT[s,v],ROT[s,w])==beta(v,w),'M_preserves_beta',(s,v,w))
    for v in V:
        need(beta(v,v)==0,'beta_alternating',v)
        need(v==0 or any(beta(v,w) for w in V),'beta_nondegenerate',v)
        need(Q[rotate(v)]==Q[v],'M_preserves_Q',v)
        need(rotate(ROT[4,v])==v,'M_fifth_power',v)
        need(v==0 or rotate(v)!=v,'M_no_nonzero_fixed',v)
    need(len({rotate(v)^v for v in V})==16,'M_minus_identity_bijection')
    binary_span={0}
    for b in VBASIS:
        binary_span |= {v^b for v in tuple(binary_span)}
    need(binary_span==set(V),'binary_basis_generates_V')
    ring_span={encode(coeff) for coeff in product(range(5),repeat=4)}
    need(ring_span==set(range(625)),'ring_monomials_generate_R')
    # Ring associativity on basis tensors; convolution is biadditive by its formula.
    for i,j,k in product((1,5,25,125),repeat=3):
        need(MUL[MUL[i][j]][k]==MUL[i][MUL[j][k]],'ring_basis_associativity',(i,j,k))
    return {'log_ordered_pairs':625**2,'binary_polarization_pairs':16**2,
            'binary_bilinear_triples':16**3,'ring_basis_triples':4**3}

def factored_group_and_lambda():
    # Exhaustive first-coordinate product certificate: independent of v,w,z,Z
    # except for e. It simultaneously checks the k and s coordinates of psi.
    for r,u in product(range(625),repeat=2):
        for e in range(2):
            uu=SIG[u] if e else u
            first=ADD[ADD[r][uu]][MUL[r][uu]]
            l,h=COEFF[LOG[r]],COEFF[LOG[u]]
            sign=-1 if e else 1
            expected=((l[0]+sign*h[0])%5,(l[1]+h[1])%5,(l[2]+sign*h[2])%5,(l[3]+h[3])%5)
            need(COEFF[LOG[first]]==expected,'factored_psi_ring_product',(r,u,e))
            # A separately computed matrix for u -> (1+r)sigma^e(u).
            matrix=[]
            for j in range(4):
                basis=5**j
                image=ADD[basis][MUL[r][basis]]
                matrix.append(tuple(((-1)**(j+1) if e else 1)*c for c in COEFF[image]))
            image=encode(tuple(sum(matrix[j][i]*COEFF[u][j] for j in range(4)) for i in range(4)))
            need(image==ADD[uu][MUL[r][uu]],'ring_lambda_matches_linear_matrix',(r,u,e))
    for v,w,s,z,Z in product(V,V,range(5),range(2),range(2)):
        ww=ROT[s,w]
        outv=v^ww; outz=z^Z^beta(v,ww)
        need((outz^Q[outv])==(z^Q[v]^Z^Q[w]),'factored_psi_binary_product',(v,w,s,z,Z))
    # Enumerate triangular binary lambda maps and certify each is linear/bijective.
    for v,s in product(V,range(5)):
        values=[]
        for w,Z in product(V,range(2)):
            out=(ROT[s,w],Z^beta(v,ROT[s,w]))
            values.append(out)
            assembled=(0,0)
            for j,basis in enumerate(VBASIS):
                if w & (1<<j):
                    m=ROT[s,basis]
                    assembled=(assembled[0]^m,assembled[1]^beta(v,m))
            assembled=(assembled[0],assembled[1]^Z)
            need(out==assembled,'binary_lambda_matches_linear_matrix',(v,s,w,Z))
        need(len(set(values))==32,'binary_lambda_bijection',(v,s))
    for a in ELEMENTS:
        need(unpsi(psi(a))==a,'psi_inverse_all_elements',a)
        ai=inv(a)
        need(circle(a,ai)==ZERO and circle(ai,a)==ZERO,'direct_inverse_all_elements',a)
        need(circle(a,ZERO)==a and circle(ZERO,a)==a,'direct_identity_all_elements',a)
        for b in BASIS:
            need(lam(a,b)==sub(circle(a,b),a),'lambda_direct_definition',(a,b))
    for r,u in product(range(625),repeat=2):
        need(star((r,0,0),(u,0,0))==(MUL[r][u],0,0),
             'P5_star_equals_ring_product',(r,u))
    return {'first_coordinate_cases':625**2*2,'binary_product_cases':16**2*5*4,
            'ring_lambda_matrix_cases':625**2*2,'binary_lambda_maps':16*5,
            'whole_element_inverse_cases':20000,'lambda_basis_cases':20000*9,
            'P5_star_pair_cases':625**2,
            'analytic_deduction':'Full psi product identity follows by independent factors; G0 is an ordinary semidirect product. Each lambda is linear and invertible. No 20000^3 enumeration.'}

class IdealTrace:
    def __init__(self,seed):
        self.nodes=[seed]
        self.records=[['seed',list(seed)]]
    def emit(self,kind,refs,actor,out):
        self.nodes.append(out)
        self.records.append([kind,refs,actor,list(out)])
        return len(self.nodes)-1
    def scale(self,i,n):
        return self.emit('integer_multiple',[i],n,scale(self.nodes[i],n))
    def ld(self,i,actor):
        return self.emit('lambda_difference',[i],list(actor),sub(lam(actor,self.nodes[i]),self.nodes[i]))
    def st(self,i,actor):
        return self.emit('star',[i],list(actor),star(self.nodes[i],actor))
    def eq(self,i,target,label):
        need(self.nodes[i]==target,label,{'node':i,'actual':self.nodes[i],'expected':target})
    def from_p5(self,i):
        r,v,z=self.nodes[i]
        need(r!=0 and v==z==0,'ideal_P5_nonzero',self.nodes[i])
        j=next(k for k,c in enumerate(COEFF[r],1) if c)
        c=COEFF[r][j-1]
        q=i if j==4 else self.ld(i,(5**(3-j),0,0))
        self.eq(q,(125*c,0,0),'ideal_top_degree_isolation')
        q=self.scale(q,pow(c,-1,5))
        self.eq(q,A,'ideal_obtains_a')
        return q
    def from_p2(self,i):
        r,v,z=self.nodes[i]
        need(r==0 and (v!=0 or z!=0),'ideal_P2_nonzero',self.nodes[i])
        if v:
            w=next(w for w in V if beta(w,v))
            i=self.ld(i,(0,w,0))
        self.eq(i,B,'ideal_obtains_b')
        return i

def verify_transcript(seed,records):
    """Independent certificate consumer; it does not know the proof strategy.

    Lambda differences are recomputed via direct multiplication, and stars via
    the separately encoded lambda formula, opposite to transcript generation.
    Integer multiples are recomputed by repeated addition.
    """
    need(records[0]==['seed',list(seed)] and seed!=ZERO,'transcript_seed')
    known=[seed]
    for record in records[1:]:
        kind,refs,actor,out=record
        need(len(refs)==1 and 0<=refs[0]<len(known),'transcript_prior_reference',record)
        member=known[refs[0]]
        if kind=='integer_multiple':
            need(isinstance(actor,int) and actor>=0,'transcript_integer_scalar',record)
            value=ZERO
            for _ in range(actor): value=add(value,member)
        elif kind=='lambda_difference':
            actor=tuple(actor)
            value=star(actor,member)
        elif kind=='star':
            actor=tuple(actor)
            value=sub(lam(member,actor),actor)
        else:
            raise AuditFailure('unrecognized ideal derivation operation')
        need(value==tuple(out),'transcript_operation_recomputed',record)
        known.append(value)
    need(set(BASIS)<=set(known),'transcript_contains_additive_generators',seed)

def ideal_seeds():
    m_inverse={rotate(w)^w:w for w in V}
    counts=Counter(); maxsteps=0
    receipt_hash=sha256()
    receipt_path=HERE/'ideal_seed_derivations.jsonl'
    sample_traces=[]
    with receipt_path.open('w',encoding='utf8') as stream:
        for seed in ELEMENTS:
            if seed==ZERO: continue
            trace=IdealTrace(seed)
            r,v,z=seed
            if r:
                pure=trace.scale(0,2)
                trace.eq(pure,(scale_ring(r,2),0,0),'ideal_seed_primary_projection')
                ia=trace.from_p5(pure)
                route='nonzero_ring_projection'
                ib=None
            else:
                ib=trace.from_p2(0)
                three_x=trace.st(ib,X)
                trace.eq(three_x,(3,0,0),'ideal_b_to_three_x')
                ia=trace.from_p5(three_x)
                route='nonzero_binary_projection'
            vnodes=[]
            for target in VBASIS:
                node=trace.st(ia,(0,m_inverse[target],0))
                trace.eq(node,(0,target,0),'ideal_a_to_binary_basis')
                vnodes.append(node)
            if ib is None: ib=trace.from_p2(vnodes[0])
            three_x=trace.st(ib,X)
            trace.eq(three_x,(3,0,0),'ideal_b_to_three_x')
            ix=trace.scale(three_x,2)
            trace.eq(ix,X,'ideal_obtains_x')
            monomials=[ix]
            for j in range(3):
                node=trace.ld(monomials[-1],X)
                trace.eq(node,(5**(j+1),0,0),'ideal_ring_basis_successor')
                monomials.append(node)
            final=[trace.nodes[i] for i in monomials+vnodes+[ib]]
            need(tuple(final)==BASIS,'ideal_all_nine_additive_generators',seed)
            verify_transcript(seed,trace.records)
            # Checkable transcript hashes are per seed; full transcripts can be
            # regenerated with --trace-seed R,V,Z, avoiding redundant megabytes.
            blob=json.dumps(trace.records,separators=(',',':')).encode()
            record={'seed':seed,'route':route,'steps':len(trace.records)-1,
                    'trace_sha256':sha256(blob).hexdigest()}
            line=json.dumps(record,separators=(',',':'))+'\n'
            stream.write(line); receipt_hash.update(line.encode())
            counts[route]+=1; maxsteps=max(maxsteps,record['steps'])
            if seed in ((0,0,1),(0,3,0),(1,0,0),(1,3,1),(125,0,0)):
                sample_traces.append({'seed':seed,'records':trace.records})
    (HERE/'sample_ideal_traces.json').write_text(json.dumps(sample_traces,indent=2)+'\n')
    need(sum(counts.values())==19999,'all_nonzero_ideal_seeds_covered')
    return {'seeds':19999,'routes':dict(counts),'maximum_steps':maxsteps,
            'receipt_sha256':receipt_hash.hexdigest(),
            'scope':'Every transcript uses only integer multiples, lambda_a(i)-i and i*a from a previously obtained ideal member. Nine additive basis vectors certify full B. The implication from the ideal definition is mathematical, not computational.'}

def invariants_and_witnesses():
    fixed=set(ELEMENTS)
    fixed_checks=0
    for a in ELEMENTS:
        for b in tuple(fixed):
            fixed_checks+=1
            if lam(a,b)!=b: fixed.remove(b)
    expected_fixed={(125*c,0,z) for c in range(5) for z in range(2)}
    need(fixed==expected_fixed,'fixed_set_exact',sorted(fixed))
    socle=[]
    for a in ELEMENTS:
        if all(lam(a,b)==b for b in BASIS): socle.append(a)
    need(socle==[ZERO],'socle_exact',socle)
    # G0 generators independent from the additive basis of the brace.
    ggens=[(1,0,0,0,0,0),(0,1,0,0,0,0),(0,0,1,0,0,0),
           (0,0,0,1,0,0),(0,0,0,0,0,1)]
    ggens += [(0,0,0,0,v,0) for v in VBASIS]
    subgroup={GZERO}; queue=deque([GZERO])
    while queue:
        g=queue.popleft()
        for h in ggens:
            q=gmul(g,h)
            if q not in subgroup: subgroup.add(q);queue.append(q)
    need(len(subgroup)==20000,'group_generators_generate_all')
    center=[]
    for g in subgroup:
        if all(gmul(g,h)==gmul(h,g) for h in ggens): center.append(g)
    expected_center={(0,k2,0,0,0,0) for k2 in range(5)}
    need(set(center)==expected_center,'multiplicative_center_exact',center)
    # Compute a normal commutator-generating set, then its actual subgroup.
    commgens=set()
    for g,h in product(ggens,repeat=2):
        commgens.add(gmul(gmul(gmul(g,h),ginv(g)),ginv(h)))
    todo=deque(commgens)
    while todo:
        d=todo.popleft()
        for h in ggens:
            q=gmul(gmul(h,d),ginv(h))
            if q not in commgens: commgens.add(q);todo.append(q)
    derived={GZERO}; queue=deque([GZERO])
    while queue:
        g=queue.popleft()
        for h in commgens:
            q=gmul(g,h)
            if q not in derived: derived.add(q);queue.append(q)
    expected_derived={(k1,0,k3,0,v,0) for k1,k3,v in product(range(5),range(5),V)}
    need(derived==expected_derived,'derived_subgroup_exact')
    need(all(gmul(a,b)==gmul(b,a) for a,b in product(derived,repeat=2)),'derived_abelian')
    p5=[(a,b,c,0,0,s) for a,b,c,s in product(range(5),repeat=4)]
    p2=[(0,0,0,e,v,0) for e,v in product(range(2),V)]
    need(all(gmul(a,b)==gmul(b,a) for a,b in product(p5,repeat=2)),'Sylow5_abelian')
    need(all(gmul(a,b)==gmul(b,a) for a,b in product(p2,repeat=2)),'Sylow2_abelian')
    need(len(p5)==625 and len(p2)==32,'Sylow_orders')
    xx=star(X,X); xxx=star(xx,X)
    need(xx==(5,0,0) and xxx==(25,0,0),'nonzero_Sylow_triple_witness',(xx,xxx))
    central=(encode((0,1,0,3)),0,0)
    need(psi(central)==(0,1,0,0,0,0),'explicit_central_witness',central)
    h=(EXP[2],0,0); d=comm(B,h)
    need(d==(encode((1,3,1,4)),0,0),'explicit_commutator_witness',d)
    du=star(d,X); gdu=star(X,du)
    need(du==(encode((0,1,3,1)),0,0),'explicit_derived_star_witness',du)
    need(gdu==(encode((0,0,1,3)),0,0),'explicit_failure_derived_star_fixed',gdu)
    need(du not in fixed,'derived_star_not_fixed',du)
    need(psi(d) in derived,'explicit_commutator_in_derived')
    return {'Fix_size':len(fixed),'fixed_intersection_evaluations':fixed_checks,
            'socle_size':len(socle),'center_size':len(center),'derived_size':len(derived),
            'abelianization_order':20000//len(derived),'Sylow5_order':len(p5),'Sylow2_order':len(p2),
            'triple_witness':xxx,'central_witness':central,'commutator':d,'derived_star':du,
            'star_of_derived_star':gdu}

def negative_controls():
    controls=[]
    w=next(v for v in V if v)
    x3=(25,0,0)
    triples={
        'raw_a4':(X,x3,(0,w,0)),
        'drop_Q':((0,3,0),(0,5,0),X),
        'drop_beta':((0,3,0),(0,5,0),X),
    }
    for mutation,(a,b,c) in triples.items():
        left=circle(circle(a,b,mutation),c,mutation)
        right=circle(a,circle(b,c,mutation),mutation)
        need(left!=right,'negative_associativity_control',mutation)
        controls.append({'mutation':mutation,'detected':'nonassociativity','a':a,'b':b,'c':c,'left':left,'right':right})
    for mutation,a,b in [('sigma_identity',B,X),('M_identity',A,(0,w,0))]:
        mutated=sub(sub(circle(a,b,mutation),a),b)
        need(mutated==ZERO and star(a,b)!=ZERO,'negative_simplicity_propagation_control',mutation)
        controls.append({'mutation':mutation,'detected':'required_ideal_propagation_disappears','star':mutated,'original_star':star(a,b)})
    need(any(Q[v^w]!=(Q[v]^Q[w]) for v,w in product(V,repeat=2)),'negative_Q_without_beta_control')
    bad=next(r for r in range(625) if LOG[ADD[EXP[r]][MUL[MUL[r][r]][r]]]!=r)
    controls.append({'mutation':'add_extra_t_cubed_to_exp','detected':'log_exp_inverse_failure','input':bad})
    return controls

# Direct generic two-trivial-factor operations for CYCLIC T,S. The input b is
# not assumed biadditive. This tests the manuscript's generalized cocycle claim.
def generic_cyclic(n,m,action,table):
    es=tuple(product(range(n),range(m)))
    z=(0,0)
    def bc(t,u): return table[t][u]
    def plus(a,b): return ((a[0]+b[0])%n,(a[1]+b[1]+bc(a[0],b[0]))%m)
    def minus(a): return ((-a[0])%n,(-a[1]-bc(a[0],(-a[0])%n))%m)
    def difference(a,b): return plus(a,minus(b))
    def circ(a,b): return ((a[0]+action[a[1]]*b[0])%n,(a[1]+b[1])%m)
    def lm(a,b): return difference(circ(a,b),a)
    def st(a,b): return difference(lm(a,b),b)
    brace=all(lm(a,plus(b,c))==plus(lm(a,b),lm(a,c)) for a,b,c in product(es,repeat=3))
    biadd=all(bc(t,(u+v)%n)==(bc(t,u)+bc(t,v))%m for t,u,v in product(range(n),repeat=3))
    if brace:
        need(biadd,'general_cocycle_brace_forces_biadditivity',(n,m,table))
        need(all(lm(a,b)==(action[a[1]]*b[0]%n,(b[1]-bc(action[a[1]]*b[0]%n,a[0]))%m) for a,b in product(es,repeat=2)), 'general_lambda_formula',(n,m,table))
        primes=[]
        for p in (2,3):
            if n*m%p==0: primes.append(p)
        abelian_all=True; triple_checks=0
        for p in primes:
            P=[]
            for a in es:
                value=z
                for k in range(1,n*m+1):
                    value=plus(value,a)
                    if value==z: break
                order=k
                while order%p==0: order//=p
                if order==1:P.append(a)
            need(all(plus(a,b) in P and circ(a,b) in P for a,b in product(P,repeat=2)), 'generic_primary_subbrace',(n,m,p))
            abelian=all(circ(a,b)==circ(b,a) for a,b in product(P,repeat=2))
            abelian_all=abelian_all and abelian
            if abelian:
                for a,b,c in product(P,repeat=3):
                    need(st(st(a,b),c)==z,'generic_abelian_Sylow_triple_zero',(n,m,p,a,b,c))
                    triple_checks+=1
        return True,biadd,abelian_all,triple_checks
    return False,biadd,False,0

def generalized_obstruction():
    counts=Counter(); rejected_witnesses=[]
    cases=[(2,2,(1,1)),(3,3,(1,1,1)),(4,2,(1,1)),(4,2,(1,3)),(3,2,(1,2)),(2,4,(1,1,1,1))]
    for n,m,action in cases:
        need(all(action[s]*action[t]%n==action[(s+t)%m]
                 for s,t in product(range(m),repeat=2)), 'generic_action_homomorphism',(n,m,action))
        pairs=[(i,j) for i in range(1,n) for j in range(i,n)]
        for values in product(range(m),repeat=len(pairs)):
            counts['symmetric_normalized_maps']+=1
            table=[[0]*n for _ in range(n)]
            for (i,j),v in zip(pairs,values): table[i][j]=table[j][i]=v
            cocycle=all((table[t][u]+table[(t+u)%n][v]-table[u][v]-table[t][(u+v)%n])%m==0 for t,u,v in product(range(n),repeat=3))
            if not cocycle:continue
            counts['symmetric_cocycles']+=1
            preserve=all(table[action[s]*t%n][action[s]*u%n]==table[t][u] for s,t,u in product(range(m),range(n),range(n)))
            if not preserve:continue
            counts['action_preserving_cocycles']+=1
            brace,biadd,allabel,triple=generic_cyclic(n,m,action,table)
            counts['valid_braces']+=int(brace)
            counts['valid_with_all_abelian_Sylows']+=int(brace and allabel)
            counts['triple_tests']+=triple
            if not brace and not biadd:
                counts['nonbilinear_cocycles_rejected_by_brace_identity']+=1
                if len(rejected_witnesses)<3:rejected_witnesses.append({'T_order':n,'S_order':m,'action':action,'b':table})
    # Necessary-hypothesis control: T=F2^2, S=F2, alpha swaps bits,
    # b(t,u)=dot(t,u). This is a genuine asymmetric product but its Sylow2
    # is nonabelian and the triple obstruction is false.
    es=tuple(product(range(4),range(2)))
    def dot(t,u):return (t&u).bit_count()%2
    def sw(t):return ((t&1)<<1)|((t&2)>>1)
    def plus(a,b):return a[0]^b[0],a[1]^b[1]^dot(a[0],b[0])
    def minus(a):return a[0],a[1]^dot(a[0],a[0])
    def diff(a,b):return plus(a,minus(b))
    def circ(a,b):return a[0]^(sw(b[0]) if a[1] else b[0]),a[1]^b[1]
    def lm(a,b):return diff(circ(a,b),a)
    def st(a,b):return diff(lm(a,b),b)
    for a,b,c in product(es,repeat=3):
        need(plus(plus(a,b),c)==plus(a,plus(b,c)),'negative_nonabelian_additive_group')
        need(circ(circ(a,b),c)==circ(a,circ(b,c)),'negative_nonabelian_multiplicative_group')
        need(lm(a,plus(b,c))==plus(lm(a,b),lm(a,c)),'negative_nonabelian_brace_valid')
    witness=next((a,b,c,st(st(a,b),c)) for a,b,c in product(es,repeat=3) if st(st(a,b),c)!=(0,0))
    need(any(circ(a,b)!=circ(b,a) for a,b in product(es,repeat=2)),'negative_nonabelian_Sylow_hypothesis_fails')
    need(witness[3]!=(0,0),'negative_nonabelian_triple_nonzero')
    counts['nonabelian_control_brace_triples']=8**3
    return {'counts':dict(counts),'nonbilinear_cocycle_controls':rejected_witnesses,
            'nonabelian_Sylow_nonzero_triple_witness':witness,
            'scope':'Finite cyclic tests and an order-eight vector control support, but cannot establish, the universal obstruction. Universal reduction still requires the abstract proof.'}

def replay_one(seed):
    # Generate all transcripts by running the deterministic seed routine only
    # when requested; locate selected seed's receipt in the published result.
    if seed==ZERO or seed not in ELEMENTS:raise AuditFailure('invalid nonzero seed')
    t=IdealTrace(seed);r,v,z=seed
    if r:ia=t.from_p5(t.scale(0,2));ib=None
    else:
        ib=t.from_p2(0);ia=t.from_p5(t.st(ib,X))
    mi={rotate(w)^w:w for w in V}
    vn=[t.st(ia,(0,mi[v],0)) for v in VBASIS]
    if ib is None:ib=t.from_p2(vn[0])
    ix=t.scale(t.st(ib,X),2);mono=[ix]
    for j in range(3):mono.append(t.ld(mono[-1],X))
    need(tuple(t.nodes[i] for i in mono+vn+[ib])==BASIS,'replay_all_generators')
    return {'seed':seed,'records':t.records,'trace_sha256':sha256(json.dumps(t.records,separators=(',',':')).encode()).hexdigest()}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--trace-seed',help='Print full deterministic transcript for R,V,Z integer encoding')
    args=parser.parse_args()
    started=stamp()
    stage('independent_encoding_and_frozen_input',setup)
    if args.trace_seed:
        seed=tuple(map(int,args.trace_seed.split(',')))
        print(json.dumps(replay_one(seed),indent=2));return
    stage('exhaustive_ingredients',ingredients)
    stage('factored_group_and_lambda_identities',factored_group_and_lambda)
    stage('all_nonzero_ideal_seed_derivations',ideal_seeds)
    stage('invariants_and_explicit_obstruction_witnesses',invariants_and_witnesses)
    stage('mathematical_mutation_negative_controls',negative_controls)
    stage('generalized_two_trivial_product_finite_controls',generalized_obstruction)
    result={'status':'PASS','started_utc':started,'completed_utc':stamp(),
            'proof_sha256':EXPECTED,'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'python_version':sys.version,'guard_count':sum(COUNTS.values()),'guard_counts':dict(COUNTS),
            'stages':STAGES,'explicit_limits':['No enumeration of all 20000^3 triples.','General obstruction theorem cannot be established by finite examples.','No historical novelty or source-authentication conclusion.']}
    (HERE/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','guard_count':result['guard_count'],'result_file':str(HERE/'results.json')},sort_keys=True))

if __name__=='__main__':
    try:main()
    except AuditFailure as error:
        print(json.dumps({'status':'FAIL','error':str(error)}),file=sys.stderr)
        sys.exit(1)
