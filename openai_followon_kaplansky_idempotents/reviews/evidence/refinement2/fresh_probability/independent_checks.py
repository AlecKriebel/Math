#!/usr/bin/env python3
"""Fresh exact checks derived from the primary construction.

Reads frozen payload; writes no file. This verifies the finite label model
and parameter certificates, not an unlisted good matching or group algebra.
"""
from collections import Counter
from fractions import Fraction as R
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json
import random

ROOT = Path(__file__).resolve().parents[3]

def require(truth, label):
    if not truth:
        raise ValueError(label)

def poly_mul(a, b):
    return 0 if not a or not b else _poly_mul(a, b)

def _poly_mul(a, b):
    out = 0
    for i in range(a.bit_length()):
        if (a >> i) & 1:
            for j in range(b.bit_length()):
                if (b >> j) & 1:
                    out ^= 1 << (i+j)
    return out

def rem(a, b):
    require(b > 0, 'zero polynomial divisor')
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length()-b.bit_length())
    return a

def gcd(a, b):
    while b:
        a, b = b, rem(a, b)
    return a

def frozen_hashes():
    frozen = json.loads((ROOT/'reviews/refinement2_manifest.json').read_text())
    checked = []
    for record in frozen['files']:
        data = (ROOT/record['path']).read_bytes()
        require(len(data) == record['bytes'], 'size: '+record['path'])
        require(sha256(data).hexdigest() == record['sha256'], 'hash: '+record['path'])
        checked.append(record['path'])
    source = ROOT/'sources/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/build'
    primary = {}
    pinned = {entry['path']: entry for entry in json.loads((ROOT/'sources/SOURCE_MANIFEST.json').read_text())['files']}
    for path in sorted(source.rglob('*.tex')) + [source/'references.bib']:
        name = str(path.relative_to(ROOT))
        body = path.read_bytes()
        digest = sha256(body).hexdigest()
        require(name in pinned and digest == pinned[name]['sha256'] and len(body)==pinned[name]['bytes'], 'pinned primary identity: '+name)
        primary[name] = digest
    return {'frozen_file_count': len(checked), 'primary_source_hashes': primary}

def quotient_from_actual_letters(q, seed):
    v = q*q+q+1
    p = R(q+1,v)
    ordinary = list(range(v))
    random.Random(seed).shuffle(ordinary)
    inverse = {}
    for i in range(7):
        inverse[v+i] = ordinary[i]
        inverse[ordinary[i]] = v+i
    for i in range(7,v,2):
        inverse[ordinary[i]] = ordinary[i+1]
        inverse[ordinary[i+1]] = ordinary[i]
    classes = [list(range(v,v+7)), ordinary[:7], ordinary[7:]]
    kinds = ['E' if t>=v else 'S' if t in ordinary[:7] else 'O' for t in range(v+7)]
    sizes = [7,7,v-7]
    known = [[7*p*p,R(6,(q+1)**2),R(v-7,(q+1)**2)],
             [R(3,2),7*p*p,(v-7)*p*p],
             [7*p*p,R(7,(q+1)**2),R(v-8,(q+1)**2)]]
    for ci, letters in enumerate(classes):
        for t in letters:
            counts = [Counter(),Counter(),Counter()]
            for cj, successors in enumerate(classes):
                for u in successors:
                    if u == inverse[t]:
                        continue
                    if inverse[t] < v and u < v:
                        weight = 'ordinary'
                    elif inverse[t] >= v and u >= v:
                        weight = 'extra'
                    else:
                        weight = 'mixed'
                    counts[cj][weight] += 1
            values = [R(c['ordinary'],(q+1)**2)+R(c['extra'],4)+c['mixed']*p*p for c in counts]
            require(values == known[ci], f'actual quotient q={q}, seed={seed}, letter={t}')
    return known, sizes, v

def exact_parameters():
    evidence = []
    for q in (4,8,16,32,64):
        for seed in (0,17):
            Q,sizes,v = quotient_from_actual_letters(q,seed)
        f = [R(1),R(13,5),R(1)] if q == 32 else [R(193,500),R(1),R(97,250)]
        ratios = [sum(row[j]*f[j] for j in range(3))/f[i] for i,row in enumerate(Q)]
        lam = R(987,1000)
        mu = R(503,500)
        if q in (4,8,16):
            require(min(ratios)>mu, f'lower strict ratios {q}')
            bound = 'lower'
            prefactor = sum(R(sizes[i])*f[i] for i in range(3))
        elif q==32:
            require(max(ratios)<lam, 'upper strict ratios')
            bound = 'upper'
            prefactor = sum(R(sizes[i])*f[i] for i in range(3))
            require(prefactor==R(5376,5), 'upper prefactor')
        else:
            bound = 'quotient only'
            prefactor = 0
        # Actual total word mass at h=0 is a separately defined empty word;
        # the manuscript theorem begins at h=1. For h>=1 this is exact.
        y = [R(1),R(1),R(1)]
        masses = [R(1)]
        for h in range(1,5):
            mass = sum(R(sizes[i])*y[i] for i in range(3))
            masses.append(mass)
            if bound=='lower':
                require(mass >= prefactor*mu**(h-1), f'h={h} lower bound q={q}')
            if bound=='upper':
                require(mass <= prefactor*lam**(h-1), f'h={h} upper bound q={q}')
            y = [sum(row[j]*y[j] for j in range(3)) for row in Q]
        evidence.append({'q':q,'letters':sum(sizes),'actual_pairings_checked':2,
                         'ratios':list(map(str,ratios)),'strict_margin':str(min(ratios)-mu if bound=='lower' else lam-max(ratios) if bound=='upper' else 0),
                         'h0_h1_h2_h3_h4_exact_mass':list(map(str,masses)),
                         'bound':bound,'prefactor':str(prefactor)})
    require(not any((3*m-1)%4==0 and 3*(m-1)%4==0 for m in range(4)), 'q=2 incompatibility')
    q=32;v=1057;p=R(33,1057)
    require(2*(v+7)/p < 2**17, 'c0 first log')
    require(40<2**6, 'c0 second log')
    eta=R(1,10**6)
    require(17*eta < p/4, 'expansion denominator')
    # binom(4|T|k^2,r) <= (4e|T|k^2/r)^r;
    # r>=33k/2 permits C2<24|T|/33, using e<3.
    D=R(48*(v+7),33)/p
    C3=R(9,4)*D**17
    require(C3*R(1,10**87)<R(1,2), 'expansion union bound')
    allq_base = R(21,33)+R(7*33,32**2)
    require(allq_base<1, 'all q>=32 ordinary row bound')
    require(R(3,2)+1+R(1,32)+R(21,32**2)<4, 'all q>=32 extra row bound')
    return {'word_mass_cases':evidence,'q2_slot_incompatibility':True,
            'c0':'1/100','eta':str(eta),'capacity':str(R(7*33,4*v)),
            'expansion_D_bound':str(D),'C3_eta_29over2':str(C3*R(1,10**87)),
            'all_larger_q_ordinary_bound':str(allq_base)}

def finite_incidence():
    data=json.loads((ROOT/'data/plane32_incidence.json').read_text())
    mod=37
    table=[[rem(poly_mul(a,b),mod) for b in range(32)] for a in range(32)]
    x=2
    frob=x
    for _ in range(5):
        frob=rem(poly_mul(frob,frob),mod)
    require(frob==x and gcd(rem(poly_mul(x,x),mod)^x,mod)==1, 'Frobenius irreducibility')
    inverses={a:next(b for b in range(1,32) if table[a][b]==1) for a in range(1,32)}
    for a,b,c in product(range(32),repeat=3):
        require(table[table[a][b]][c]==table[a][table[b][c]], 'associativity')
        require(table[a][b^c]==(table[a][b]^table[a][c]), 'distributivity')
    def normalize(t):
        b=next(b for b in t if b)
        return tuple(table[a][inverses[b]] for a in t)
    classes=Counter(normalize(t) for t in product(range(32),repeat=3) if any(t))
    points=sorted(classes)
    require(len(points)==1057 and set(classes.values())=={31}, 'projective partition')
    require(points==list(map(tuple,data['points'])), 'supplied points')
    require(points==list(map(tuple,data['line_covectors'])), 'supplied covectors')
    lines=[];bits=[];columns=[0]*1057
    for i,(a,b,c) in enumerate(points):
        row=[j for j,(u,v,w) in enumerate(points) if table[a][u]^table[b][v]^table[c][w]==0]
        require(len(row)==33 and row==data['line_point_indices'][i], 'incidence row')
        lines.append(row);mask=0
        for j in row:
            mask|=1<<j;columns[j]|=1<<i
        bits.append(mask)
    require(all(col.bit_count()==33 for col in columns), 'point degree')
    pairs=0
    for i,j in combinations(range(1057),2):
        require((bits[i]&bits[j]).bit_count()==1, 'line intersections')
        require((columns[i]&columns[j]).bit_count()==1, 'point line uniqueness')
        pairs+=1
    fano_lines=sorted(set(tuple(sorted((a,b,a^b))) for a,b in combinations(range(1,8),2)))
    complements=[set(range(1,8))-set(line) for line in fano_lines]
    require(data['fano_lines']==list(map(list,fano_lines)), 'fano lines')
    require(data['fano_complements']==[sorted(c) for c in complements], 'fano complements')
    require(all(sum(a in d for d in complements)==4 for a in range(1,8)), 'extra balance')
    require(all(sum(a in d and b in d for d in complements)==2 for a,b in combinations(range(1,8),2)), 'extra pair balance')
    require(all(len(a&b)==2 for a,b in combinations(complements,2)), 'extra even intersections')
    inverse={}
    for a,b in data['inverse_pairs']:
        require(a!=b and a not in inverse and b not in inverse, 'inverse pair overlap')
        inverse[a]=b;inverse[b]=a
    require(set(inverse)==set(range(1064)), 'inverse coverage')
    require(all(inverse[inverse[a]]==a for a in inverse), 'inverse involution')
    require(all(inverse[1057+i]==i for i in range(7)), 'extra mates')
    # Type assignment at m=13 uses 107 or 99 vertices for each complement.
    # A direct round-robin placement realizes the bounded per-line demands.
    m=13;am=(33*m-1)//4;bm=33*(m-1)//4
    require(4*am+1==33*m and 4*bm==33*(m-1), 'exact slots')
    demandA=[0]*1057;demandB=[0]*1057
    for di in range(7):
        for j in range(am): demandA[(j+di*am)%1057]+=1
        for j in range(bm): demandB[(j+di*bm)%1057]+=1
    demandA[0]+=1
    require(max(demandA)<=m and max(demandB)<=m-1,'disjoint type capacity')
    # Pair parity includes empty, complement, and the unique full special type.
    extras=[set()]+complements
    require(all(len(a&b)%2==0 for a,b in product(extras,repeat=2)),'all ordinary extra intersections')
    require(all(len(set(range(1,8))&a)%2==0 for a in extras),'special extra intersections')
    require((33+7)%2==0 and all((33+len(a))%2==1 for a in extras),'degree parity')
    return {'field_order':32,'field_triples':32**3,'projective_nonzero_vectors':32**3-1,
            'points':1057,'lines':1057,'incidences':1057*33,
            'point_and_line_pairs_each':pairs,'signed_letters':1064,'rose_edges':len(inverse)//2,
            'm13_type_demands_max_A_B':[max(demandA),max(demandB)],
            'data_sha256':sha256((ROOT/'data/plane32_incidence.json').read_bytes()).hexdigest()}

if __name__=='__main__':
    print(json.dumps({'status':'passed','scope':'Frozen identity, exact squared-word matrices, full actual-letter row reductions, finite field and incidence, type parity and capacity only; no matching witness or group-ring product certificate.',
                      'identity':frozen_hashes(),'parameters':exact_parameters(),'finite_model':finite_incidence()},indent=2))
