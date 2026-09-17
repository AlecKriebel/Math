#!/usr/bin/env python3
"""Independent, standard-library UNSAT certificate checker.

Does not import the generator or prover. Verifies each unit inference against
an original DIMACS clause, both sides of each Boolean split, and a falsified
original clause at every leaf. Refuses hash mismatches and malformed proofs.
"""
import argparse,hashlib,json
from pathlib import Path

def verify(cnf_path,cert_path):
    raw=cnf_path.read_bytes();cert=json.loads(cert_path.read_text())
    if cert['cnf_sha256']!=hashlib.sha256(raw).hexdigest():raise ValueError('CNF digest mismatch')
    clauses=[];nvars=nclauses=None;buffer=[]
    for line in raw.decode().splitlines():
        if not line.strip() or line.startswith('c'):continue
        if line.startswith('p '):
            p,typ,nv,nc=line.split();assert typ=='cnf';nvars,nclauses=int(nv),int(nc);continue
        for token in line.split():
            k=int(token)
            if k==0:clauses.append(frozenset(buffer));buffer=[]
            else:buffer.append(k)
    if buffer or len(clauses)!=nclauses:raise ValueError('Malformed DIMACS')
    if any(abs(l)>nvars or l==0 for cl in clauses for l in cl):raise ValueError('Invalid variable')
    counts={'nodes':0,'unit_steps':0,'conflicts':0,'splits':0}
    def clause(i):
        if type(i) is not int or not 0<=i<len(clauses):raise ValueError('Bad clause reference')
        return clauses[i]
    def walk(node,true_lits):
        counts['nodes']+=1;known=set(true_lits)
        for step in node.get('units',[]):
            if len(step)!=2:raise ValueError('Bad unit step')
            l,i=step
            if type(l) is not int or not 1<=abs(l)<=nvars:raise ValueError('Bad unit literal')
            if l in known or -l in known:raise ValueError('Unit variable already assigned')
            cl=clause(i)
            if l not in cl or any(-other not in known for other in cl if other!=l):
                raise ValueError(f'Clause {i} does not justify unit {l}')
            known.add(l);counts['unit_steps']+=1
        if 'conflict' in node:
            if 'split' in node:raise ValueError('Conflict and split both supplied')
            if any(-l not in known for l in clause(node['conflict'])):raise ValueError('Unfalsified conflict clause')
            counts['conflicts']+=1;return
        v=node.get('split')
        if type(v) is not int or not 1<=v<=nvars or v in known or -v in known:raise ValueError('Invalid split')
        counts['splits']+=1
        walk(node['true'],known|{v});walk(node['false'],known|{-v})
    walk(cert['tree'],set())
    return counts

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('cnf',type=Path);p.add_argument('certificate',type=Path);a=p.parse_args()
    counts=verify(a.cnf,a.certificate);print('VERIFIED UNSAT',json.dumps(counts,sort_keys=True))
if __name__=='__main__':main()
