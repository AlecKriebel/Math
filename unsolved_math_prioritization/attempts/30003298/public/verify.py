#!/usr/bin/env python3
"""Source-free integrity/scope and exact finite diagnostics; not a proof checker."""
import hashlib
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

PAYLOAD = {'README.md', 'PROOF.md', 'APPROACHES.md', 'SOURCES.md',
           'PROVENANCE.json', 'LEDGER.md', 'CLAIMS.json', 'verify.py', 'test_verifier.py'}
EXPECTED_CLAIMS = {
 'problem_id':30003298,'problem_code':'OWR-15177-016','queue_rank':997,
 'status':'unsolved','approaches':5,'surface':'closed connected oriented',
 'group':'orientation-preserving Mod_g','subgroup':'every torsion-free finite-index Gamma',
 'coefficient':'H_(2g-2)(C_g;Z), natural action','genus_min':2,
 'target_degree':[2,-1],'proved_degree':[4,-5],'target_solved_genera':[2],
 'general_target_solved':False,'rational_rank_proved':'infinite in degree 4g-5',
 'novelty_claim':False,'independent_review':'pending','formal_verification':False,
 'avramidi_dependency_in_main_theorem':False}

class VerificationError(Exception):
    pass

checks = 0

def require(condition, message):
    global checks
    if not condition:
        raise VerificationError(message)
    checks += 1

def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise VerificationError('duplicate JSON key: ' + key)
        out[key] = value
    return out

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object,
                      parse_constant=lambda x: (_ for _ in ()).throw(VerificationError('nonfinite JSON')))

def rank(a):
    if not a:
        return 0
    require(all(len(row)==len(a[0]) for row in a), 'ragged matrix')
    b = [[Fraction(x) for x in row] for row in a]
    row = 0
    for col in range(len(b[0])):
        pivot = next((i for i in range(row,len(b)) if b[i][col]),None)
        if pivot is None:
            continue
        b[row],b[pivot] = b[pivot],b[row]
        p = b[row][col]
        b[row] = [x/p for x in b[row]]
        for i in range(len(b)):
            if i != row and b[i][col]:
                c=b[i][col]
                b[i]=[x-c*y for x,y in zip(b[i],b[row])]
        row += 1
        if row == len(b):
            break
    return row

def sp_order(g,p):
    value=p**(g*g)
    for i in range(1,g+1):
        value *= p**(2*i)-1
    return value

def dimension(g,p):
    return Fraction(sp_order(g,p),g*(p**(2*g)-1))

def partitions(n,maximum=None):
    if n==0:
        yield ()
        return
    if maximum is None:
        maximum=n
    for j in range(min(n,maximum),1-1,-1):
        for tail in partitions(n-j,j):
            yield (j,)+tail

def factorial(n):
    z=1
    for j in range(1,n+1):
        z*=j
    return z

def finite_diagnostics():
    # Tests scalar formulas and independently evaluates the partition recurrence.
    primes=[2,3,5,7,11,13,17,19,23,29,31]
    for g in range(2,31):
        require((4*g-5)-(2*g-1)==2*g-4,'duality degree mismatch')
        require(((4*g-5)==(2*g-1))==(g==2),'genus scope mismatch')
        last=0
        for p in primes:
            z=dimension(g,p)
            require(z.denominator==1 and z>last,'quotient-dimension diagnostic')
            last=z
    require(dimension(2,2)==24,'exact quotient-formula control')
    require(dimension(2,3)==324,'exact quotient-formula control')
    require(dimension(3,2)==7680,'exact quotient-formula control')
    for p in [2,3,5,7]:
        for g in range(1,9):
            total=Fraction(0)
            for part in partitions(g):
                term=Fraction(1)
                for a in set(part):
                    count=part.count(a)
                    term *= Fraction(1,a*(p**(2*a)-1))**count / factorial(count)
                total += term
            expected=Fraction(p**(g*(2*g-1)),sp_order(g,p))
            require(total==expected,'partition recurrence diagnostic')
    # Greedy unbounded-rank witness sizes, illustrating the proof's finite criterion.
    greedy=[]
    for g in range(2,9):
        previous=0
        chosen=[]
        for p in primes:
            r=dimension(g,p)
            if r>previous:
                chosen.append(p)
                require(r>previous,'greedy rank separation')
                previous += r
        require(len(chosen)>=5,'insufficient finite rank examples')
        greedy.append({'genus':g,'primes':chosen})
    # Exhaust every pair of 2x2 matrices over {-1,0,1}; exact Q-rank subadditivity.
    matrices=[[[a,b],[c,d]] for a,b,c,d in itertools.product([-1,0,1],repeat=4)]
    ranks=[rank(a) for a in matrices]
    for i,a in enumerate(matrices):
        for j,b in enumerate(matrices):
            s=[[a[x][y]+b[x][y] for y in range(2)] for x in range(2)]
            require(rank(s)<=ranks[i]+ranks[j],'rank subadditivity counterexample')
    # Cyclic permutation actions: average a diagonal positive form, then pull back
    # along the surjection Q^(n+2)->Q^n. Check invariance and exact pullback rank.
    for n in range(1,13):
        weights=list(range(1,n+1))
        b=[[sum(weights[(i+k)%n] for k in range(n)) if i==j else 0
            for j in range(n)] for i in range(n)]
        require(all(b[(i+1)%n][(j+1)%n]==b[i][j] for i in range(n) for j in range(n)),
                'averaging invariance')
        require(all(b[i][i]>0 for i in range(n)),'averaging positivity')
        pull=[[b[i][j] if i<n and j<n else 0 for j in range(n+2)] for i in range(n+2)]
        require(rank(b)==n and rank(pull)==n,'surjective pullback rank')
    # Formal inference negative controls: a rank-one invariant pairing does not
    # bound the dimension of the module; target and top degrees differ for g>=3.
    require(rank([[1,0],[0,0]])==1,'degenerate-form diagnostic')
    require((4*3-5)!=(2*3-1),'wrong-genus claim accepted')
    return greedy

def main():
    require(len(sys.argv)==1,'no arguments accepted')
    root=Path(__file__).resolve().parent
    found={x.name for x in root.iterdir()}
    require(found==PAYLOAD|{'MANIFEST.json'},'unexpected or missing packet member')
    require(all(x.is_file() and not x.is_symlink() for x in root.iterdir()),'nonregular packet member')
    manifest=read_json(root/'MANIFEST.json')
    require(type(manifest) is dict and set(manifest)=={'schema','files'},'manifest schema')
    require(type(manifest['schema']) is int and manifest['schema']==1,'manifest version')
    entries=manifest['files']
    require(type(entries) is list and len(entries)==len(PAYLOAD),'manifest entries')
    names=[]
    for entry in entries:
        require(type(entry) is dict and set(entry)=={'name','bytes','sha256'},'entry schema')
        name=entry['name']
        require(type(name) is str and name in PAYLOAD and name not in names,'unsafe/duplicate path')
        names.append(name)
        require(type(entry['bytes']) is int and entry['bytes']>=0,'byte-count schema')
        h=entry['sha256']
        require(type(h) is str and len(h)==64 and all(x in '0123456789abcdef' for x in h),'digest schema')
        data=(root/name).read_bytes()
        require(len(data)==entry['bytes'],'byte mismatch: '+name)
        require(hashlib.sha256(data).hexdigest()==h,'hash mismatch: '+name)
    require(set(names)==PAYLOAD,'manifest inventory mismatch')
    claims=read_json(root/'CLAIMS.json')
    # Canonical serialization also distinguishes booleans from integers.
    require(json.dumps(claims,sort_keys=True)==json.dumps(EXPECTED_CLAIMS,sort_keys=True),'wrong or malformed claim')
    provenance=read_json(root/'PROVENANCE.json')
    require(provenance['problem_id']==30003298,'provenance target')
    require(provenance['exact_research_report_present'] is False,'research-report scope')
    require(provenance['source_documents_in_public_packet'] is False,'source exclusion')
    require(provenance['dataset_contents_in_public_packet'] is False,'dataset exclusion')
    require(provenance['remote_writes_performed'] is False,'remote-action scope')
    require(len(provenance['source_pdfs'])==4,'source inventory')
    greedy=finite_diagnostics()
    print(json.dumps({'status':'PASS','checks':checks,'files':len(PAYLOAD),
      'scope':'Integrity, frozen claims, and finite algebra/arithmetic diagnostics only; not formal mathematical verification.',
      'greedy_rank_examples':greedy},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except (VerificationError,ValueError,TypeError,KeyError,OSError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
