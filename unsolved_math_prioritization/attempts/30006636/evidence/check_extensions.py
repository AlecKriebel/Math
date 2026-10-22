#!/usr/bin/env python3
"""Exact finite controls for Approaches 2--5. Default output: stdout only.
No source files, network, floating point, assertions, or third-party modules.
"""
import argparse
from fractions import Fraction as Q
import itertools
import json
import os
from pathlib import Path
import sys


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def cube_floor(n):
    lo, hi = 0, n + 1
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** 3 <= n:
            lo = mid
        else:
            hi = mid
    return lo


def components_weight(count, external, edge_colors, incidences, n, drop_closed=False):
    result = 1
    for vertex in range(count):
        colors = {edge_colors[i] for i, v in enumerate(incidences) if v == vertex}
        if external[vertex] is not None:
            colors.add(external[vertex])
        if len(colors) > 1:
            return 0
        if not colors:
            result *= 1 if drop_closed else n
    return result


def glued_weight(left, right, edges, external, n):
    parents = list(range(left + right))
    def find(a):
        while parents[a] != a:
            a = parents[a]
        return a
    for a, b in edges:
        parents[find(a)] = find(left + b)
    roots = {find(i) for i in range(left + right)}
    result = 1
    for r in roots:
        labels = {external[i] for i in range(left + right)
                  if find(i) == r and external[i] is not None}
        if len(labels) > 1:
            return 0
        if not labels:
            result *= n
    return result


def d8mul(a, b, abelian=False):
    i,j=a
    k,l=b
    return ((i+k if abelian else i+(-1)**j*k) % 4, (j+l) % 2)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-readonly',action='store_true')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--mutant',choices=['drop-closed-color','wrong-product-trace',
                        'abelianize-dihedral','allow-negative-multiplicity',
                        'accept-noncube','forget-connectedness'])
    args=parser.parse_args()
    packet=Path(__file__).resolve().parent
    if args.output:
        require(args.output.is_absolute(),'Output must be explicitly absolute')
        require(not args.output.resolve().is_relative_to(packet),'Output must be outside packet')
        require(not args.output.exists(),'Output destination already exists')
    if args.require_readonly:
        require(os.geteuid()!=0,'Real nonroot execution is required')
        require(not os.access(packet,os.W_OK),'Packet is writable')
        for file in packet.iterdir():
            if file.is_file():
                require(not os.access(file,os.W_OK),'Packet file is writable')
        try:
            fd=os.open(packet/'WRITE_PROBE_MUST_FAIL',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        except PermissionError:
            pass
        else:
            os.close(fd)
            raise RuntimeError('Readonly write probe unexpectedly succeeded')
    cases=0
    for N in range(1,65):
        cube_N=cube_floor(N)**3==N
        for m in range(1,N+1):
            numerator=m**3*N**2
            dimension_integer=cube_floor(numerator)**3==numerator
            if args.mutant=='accept-noncube' and N==2:
                dimension_integer=True
            require(dimension_integer==cube_N,'Integer-dimension classification failed')
            cases+=1
    # Exhaustive finite models of compatible component-color gluing.
    # These are algebraic incidence models, not asserted manifold realizations.
    gluing_cases=0
    for n in (1,2,3):
        possible_external=[None]+list(range(n))
        for left,right in ((1,1),(1,2),(2,1),(2,2)):
            possible_edges=list(itertools.product(range(left),range(right)))
            edge_sets=[]
            for mask in range(1<<len(possible_edges)):
                edge_sets.append([edge for i,edge in enumerate(possible_edges) if mask & (1<<i)])
            edge_sets += [[(0,0),(0,0)],[(0,0),(0,0),(left-1,right-1)]]
            for edges in edge_sets:
                for external in itertools.product(possible_external,repeat=left+right):
                    composition=0
                    for colors in itertools.product(range(n),repeat=len(edges)):
                        lv=components_weight(left,external[:left],colors,[a for a,b in edges],n,
                                             args.mutant=='drop-closed-color')
                        rv=components_weight(right,external[left:],colors,[b for a,b in edges],n,
                                             args.mutant=='drop-closed-color')
                        composition += lv*rv
                    expected=glued_weight(left,right,edges,external,n)
                    require(composition==expected,'Component-color bordism gluing failed')
                    gluing_cases+=1
    rank_cases=0
    for n in range(1,7):
        for q in (Q(1,2),Q(1),Q(2)):
            weights=[Q(1),q,q*q]
            gram=[[n*x*y for y in weights] for x in weights]
            require(gram[0][0]!=0,'S3 pairing lost its nonzero entry')
            for i,j,k,l in itertools.product(range(3),repeat=4):
                require(gram[i][k]*gram[j][l]-gram[i][l]*gram[j][k]==0,'S3 pairing is not rank one')
            dd=n*n*q**4
            dc=n*q*q
            cc=n*q*q if args.mutant=='wrong-product-trace' else Q(n)
            determinant=dd*cc-dc*dc
            require(determinant==n*n*(n-1)*q**4,'Two-boundary Gram determinant failed')
            require((determinant==0)==(n==1),'Universal monoidal defect control failed')
            rank_cases+=1
    group=list(itertools.product(range(4),range(2)))
    r,s=(1,0),(0,1)
    multiply=lambda a,b:d8mul(a,b,args.mutant=='abelianize-dihedral')
    require(multiply(r,s)!=multiply(s,r),'Required noncentral simple-object obstruction vanished')
    for a,b,c in itertools.product(group,repeat=3):
        require(multiply(multiply(a,b),c)==multiply(a,multiply(b,c)),'Dihedral multiplication not associative')
    for a in group:
        require({multiply(a,b) for b in group}==set(group),'Regular action not transitive')
        require(any(multiply(a,b)==(0,0) and multiply(b,a)==(0,0) for b in group),'Missing group inverse')
    require(len(group)==8 and 8*2**2==32,'D8 extension dimension control failed')
    def coefficients(t0,t1):
        return ((t0+t1)/2,(t0-t1)/2)
    def normalizable(values):
        nonzero=[x for x in values if x]
        if not nonzero:
            return True
        if args.mutant=='allow-negative-multiplicity':
            return True
        return all(x/nonzero[0]>0 for x in nonzero)
    fourier_cases=0
    for nplus,nminus in itertools.product(range(5),repeat=2):
        traces=(Q(nplus+nminus),Q(nplus-nminus))
        require(coefficients(*traces)==(nplus,nminus),'Involution Fourier inversion failed')
        for scale in (Q(-3),Q(-1),Q(1),Q(2,7)):
            require(normalizable(coefficients(*(scale*t for t in traces))),
                    'Admissible multiplicities rejected after scalar rescaling')
            fourier_cases+=1
    require(not normalizable(coefficients(Q(1),Q(3))),
            'Synthetic opposite-sign Fourier obstruction was not detected')
    for N,m in ((2,1),(6,6),(8,1),(8,8),(27,3)):
        # The common mapping-torus value need not be rational; the formal pattern
        # is (c,c) -> (c,0), with c nonzero. Test coefficient pattern at c=1.
        require(coefficients(Q(1),Q(1))==(1,0),'Euler mapping-torus control failed')
    # Two copies of S3 with the component-swap involution: the identity
    # mapping torus has two components; the swap mapping torus has one.
    # With connected scalar c=2 and repair lambda=1/2, correct componentwise
    # normalization gives (1,1), whereas a uniform factor gives (2,1).
    c=Q(2)
    repair=Q(1,2)
    repaired_pair=(repair**2*c**2,repair*c)
    if args.mutant=='forget-connectedness':
        repaired_pair=(repair*c**2,repair*c)
    require(repaired_pair==(1,1),'Connected-component normalization scope control failed')
    result={'status':'pass','mode':{0:'normal',1:'-O',2:'-OO'}[sys.flags.optimize],
            'effective_uid':os.geteuid(),'readonly_enforced':args.require_readonly,
            'classification_cases':cases,'component_gluing_cases':gluing_cases,
            'universal_rank_cases':rank_cases,'dihedral_associativity_cases':len(group)**3,
            'dihedral_noncommuting_pair':{'rs':multiply(r,s),'sr':multiply(s,r)},
            'involution_fourier_rescaling_cases':fourier_cases,
            'disconnected_scope_negative_control':'component-swap case checked',
            'synthetic_nonextension_values_are_not_source_values':True,
            'writes':'stdout only' if not args.output else 'explicit external destination',
            'limits':'Finite controls only; proofs and all general hypotheses are in FIVE_APPROACH_REPORT.md.'}
    output=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        with args.output.open('x',encoding='utf8') as stream:
            stream.write(output)
    else:
        sys.stdout.write(output)

if __name__=='__main__':
    main()
