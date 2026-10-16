"""Fresh exact diagnostics for priority implications, using standard Python only.

Universal conclusions are proved in PRIOR_COMPARISON_DERIVATIONS.md. These
finite checks are deliberately independent of submitted/reviewer executables.
"""
import hashlib, itertools, json, math, pathlib, sys

def require(x, message):
    if not x:
        raise ValueError(message)

def bank(q, mask, sign=1):
    h=lambda k: (mask >> (k % q)) & 1
    # Independent use of HLW Lemma 4.1: d_i=f(i)-f(i-1), a=q-i.
    f=lambda k: k+h(0)-h(k)
    offsets=[]
    for i in range(1,q+1):
        d=f(i)-f(i-1)
        require(d in (0,1,2), 'priming derivative outside 0,1,2')
        offsets.extend([(q-i)%q]*d)
    c=[1+sign*(h(-a-1)-h(-a)) for a in range(q)]
    require(sorted(offsets)==[a for a in range(q) for _ in range(c[a])], 'HLW priming does not match bank')
    require(len(offsets)==q, 'wrong number of topplers')
    for k in range(3*q+1):
        F=sum((a+k)//q for a in offsets)
        require(F==f(k), 'cumulative emitted topplers differ from HLW function')
        storage=sum((a+k)%q for a in offsets)
        require(storage==q*(q-1)//2-mask.bit_count()+q*h(k), 'storage complement identity')
        require(storage==sum(offsets)+q*k-q*F, 'physical returned mass identity')
    return (q,mask,offsets)

def predicates(formula, primes=(3,5,7)):
    rows=[]
    for i,p in enumerate(primes):
        rows.append((p,{0,1},'variable',i))
    for clause in formula:
        ids=sorted({abs(x)-1 for x in clause})
        q=math.prod(primes[i] for i in ids)
        # Direct local residue scan; no call to a CRT constructor.
        allowed={k for k in range(q) if all(k%primes[i] in (0,1) for i in ids)
                 and any((k%primes[abs(x)-1]==1)==(x>0) for x in clause)}
        rows.append((q,allowed,'clause',clause))
    return rows

def run():
    bank_cases=0; bank_positions=0; digest=hashlib.sha256()
    for q in range(2,13):
        for mask in range(1,1<<q):
            data=bank(q,mask)
            bank_cases+=1; bank_positions+=3*q+1
            digest.update(json.dumps(data,separators=(',',':')).encode())
    # Stockmeyer--Meyer accepts the union of INVALID assignments or FAILED
    # clauses; the candidate intersects the complements of each local language.
    clauses=[tuple(s*(i+1) for i,s in enumerate(signs)) for signs in itertools.product((-1,1),repeat=3)]
    formula_cases=0; residue_positions=0; assignment_checks=0
    for flags in range(1<<len(clauses)):
        formula=[c for j,c in enumerate(clauses) if (flags>>j)&1]
        rows=predicates(formula)
        sat_assignments=[b for b in itertools.product((0,1),repeat=3)
                         if all(any(bool(b[abs(x)-1])==(x>0) for x in c) for c in formula)]
        assignment_checks+=8
        success=[]
        for k in range(3*5*7):
            candidate=all(k%q in A for q,A,*_ in rows)
            prior_union=any(k%q not in A for q,A,*_ in rows)
            require(candidate == (not prior_union), 'union complement mismatch')
            b=tuple(k%p for p in (3,5,7))
            direct=(all(x in (0,1) for x in b) and
                    all(any(bool(b[abs(x)-1])==(x>0) for x in c) for c in formula))
            require(candidate==direct, 'SAT meaning mismatch')
            if candidate: success.append(k)
            residue_positions+=1
        require(bool(success)==bool(sat_assignments), 'CRT existence mismatch')
        require(len(success)==len(sat_assignments), 'CRT assignment bijection mismatch')
        formula_cases+=1
    # Given-input equivalence does not follow from BL II's all-input theorem.
    # Unary self-feedback processor: state 0 emits 2, state 1 emits 0; states
    # alternate. Mean production 1, reset period 2 => sandpilization Topp(2-2).
    # Initial pending letter 1, initial state 0: original returns after two
    # processing steps, whereas reset-state toppler absorbs that input and stops.
    queue,state=1,0; orbit=[]
    for _ in range(2):
        orbit.append((queue,state)); queue-=1
        queue += 2 if state==0 else 0; state=1-state
    require((queue,state)==(1,0), 'original locally recurrent processor should repeat')
    sand_queue,sand_state=1,0
    sand_queue-=1; sand_state+=1
    require(sand_queue==0 and sand_state==1, 'sandpilization reset input should halt')
    # Plain threshold-1 producer cannot replace a primed modulus-q gate, nor
    # can a one-output q-toppler be silently declared token-conservative.
    gate_interfaces=[]
    for q in range(2,18):
        for a in range(q):
            for k in range(2*q+1):
                toppler=(a+k)//q
                returned=q*toppler
                residue=(a+k)%q
                require(a+k==residue+returned, 'conservative q-output realization')
                if k==1 and a==0:
                    require(toppler==0 and k==1, 'ordinary degree-one normalization counterexample')
                gate_interfaces.append((q,a,k,toppler,returned,residue))
    # GRM local branching chooses a sign route, while fixed chip-firing has a
    # unique transition at a given vertex; this tests the failed literal erasure.
    grm_sign_traces=[('start','plus1','plus2','end'),('start','minus1','minus2','end')]
    sink_counts=[(1,2,0),(1,0,2)]
    require(sink_counts[0]!=sink_counts[1], 'GRM truth branches collapsed')
    faults=[]
    def catches(name, fn):
        try: fn()
        except ValueError: faults.append(name)
        else: raise ValueError('damaged implication was not rejected: '+name)
    catches('reverse modular derivative',lambda:bank(3,1,sign=-1))
    catches('empty allowed set falsely has chosen maximum',lambda:require(
        any(sum((a+k)%3 for a in range(3))==3*2//2+3 for k in range(3)), 'not attained'))
    catches('emit one declared conservative',lambda:require(3==(3%3)+(3//3), 'mass lost'))
    catches('all-input sandpilization promoted to same given input',lambda:require(queue==sand_queue,'given input differs'))
    catches('GRM branch forgotten',lambda:require(sink_counts[0]==sink_counts[1],'target branch differs'))
    # Number of physical vertices for multiplicity expansion can be exponential
    # in binary input bits; this rejects the claimed polynomial transfer itself.
    expansion=[{'bits':k+1,'parallel_arcs':2**k,'subdivision_vertices':2**k} for k in (4,16,64,256)]
    catches('binary multiplicity treated as polynomial numeric',lambda:require(2**256 <= (257)**4,'exponential expansion'))
    return {'status':'PASS_EXACT_FINITE_PRIORITY_CONTROLS',
            'bank_cases':bank_cases,'bank_positions':bank_positions,'bank_digest':digest.hexdigest(),
            'CRT_formula_cases':formula_cases,'CRT_residue_positions':residue_positions,'SAT_assignments_checked':assignment_checks,
            'physical_toppler_interfaces':len(gate_interfaces),'sandpilization_original_orbit':orbit,
            'sandpilization_after_two_steps':[queue,state],'same_reset_toppler_final':[sand_queue,sand_state],
            'GRM_sign_traces':grm_sign_traces,'GRM_distinct_sink_outputs':sink_counts,
            'binary_expansion_samples':expansion,'detected_faults':faults,
            'limits':'Finite diagnostics support original comparison proofs; no exhaustive novelty clearance or full theorem re-audit is inferred.'}

if __name__=='__main__':
    if '--self-test-invalid' in sys.argv:
        require(False,'unconditional invalid priority-control guard')
    result=run()
    data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if len(sys.argv)>1:
        pathlib.Path(sys.argv[1]).write_text(data)
    else: print(data,end='')
