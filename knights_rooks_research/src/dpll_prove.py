#!/usr/bin/env python3
"""Small dependency-free DPLL prover; emits an independently checkable tree.
Unit steps and conflicts reference ORIGINAL clauses, not hidden learned clauses.
"""
import argparse,json,hashlib,time
from pathlib import Path

def read_cnf(path):
    clauses=[]
    for line in path.read_text().splitlines():
        if not line or line[0] in 'cp':continue
        a=list(map(int,line.split()));assert a[-1]==0;clauses.append(a[:-1])
    return clauses

def solve(clauses,assignment,priority=()):
    steps=[]
    while True:
        changed=False;pending=[]
        for i,clause in enumerate(clauses):
            unknown=[];satisfied=False
            for lit in clause:
                v=abs(lit)
                if v not in assignment:unknown.append(lit)
                elif assignment[v]==(lit>0):satisfied=True;break
            if satisfied:continue
            if not unknown:return {'units':steps,'conflict':i}
            if len(unknown)==1:
                lit=unknown[0];assignment[abs(lit)]=lit>0
                steps.append([lit,i]);changed=True
            else:pending.append(unknown)
        if not changed:break
    if not pending:return {'satisfying_assignment':assignment}
    counts={}
    for clause in pending:
        for lit in clause:counts[abs(lit)]=counts.get(abs(lit),0)+2.0**(-len(clause))
    v=next((x for x in priority if x in counts),None) or max(counts,key=counts.get)
    yes=solve(clauses,dict(assignment) | {v:True},priority)
    if 'satisfying_assignment' in yes:return yes
    no=solve(clauses,dict(assignment) | {v:False},priority)
    if 'satisfying_assignment' in no:return no
    return {'units':steps,'split':v,'true':yes,'false':no}

def main():
    p=argparse.ArgumentParser();p.add_argument('cnf',type=Path);p.add_argument('output',type=Path);p.add_argument('--prefer',type=int,nargs='*',default=[]);a=p.parse_args()
    clauses=read_cnf(a.cnf);start=time.time();tree=solve(clauses,{},a.prefer)
    cert={'cnf_sha256':hashlib.sha256(a.cnf.read_bytes()).hexdigest(),'indexing':'zero-based original clauses','tree':tree}
    a.output.write_text(json.dumps(cert,indent=2)+'\n')
    def stats(t):
        if 'split' in t:
            x,y=stats(t['true']),stats(t['false']);return (x[0]+y[0]+1,x[1]+y[1]+len(t['units']),x[2]+y[2])
        return (1,len(t.get('units',[])),int('conflict' in t))
    print('SAT' if 'satisfying_assignment' in tree else 'UNSAT','nodes,unit_steps,conflicts=',stats(tree),'seconds',time.time()-start)
if __name__=='__main__':main()
