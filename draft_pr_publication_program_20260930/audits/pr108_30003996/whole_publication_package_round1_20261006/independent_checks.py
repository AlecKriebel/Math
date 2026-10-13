#!/usr/bin/env python3
"""Fresh R1 checks; no import of published verifier or previous audit checker."""
import argparse,datetime,hashlib,itertools,json,os,pathlib,sys
def require(v,msg):
    if not v: raise AssertionError(msg)
def build(clauses,B):
    n=max(abs(l) for c in clauses for l in c);m=len(clauses);N=n+m+2
    edges=sorted({(0,1)}|{(h,i+2) for h in (0,1) for i in range(n)}|{(abs(l)+1,n+2+j) for j,c in enumerate(clauses) for l in c})
    arcs=[a for u,v in edges for a in ((u,v),(v,u))]
    costs=[]
    for r in range(N):
        row=[]
        for u,v in arcs:
            w=0
            if r==0:
                w=0 if {u,v}=={0,1} else B if max(u,v)>=n+2 else 1
            elif r>=n+2:
                for l in clauses[r-n-2]:
                    if (u,v)==(abs(l)+1,1 if l>0 else 0):w=1
            row.append(w)
        costs.append(row)
    return {'N':N,'edges':edges,'costs':costs,'K':B*m+n},n,m
def tree_costs(inst,chosen,inward=False,transpose=False,shift=0):
    N=inst['N'];index={arc:k for k,arc in enumerate(a for u,v in inst['edges'] for a in ((u,v),(v,u)))}
    adj=[[] for _ in range(N)]
    for u,v in chosen:adj[u].append(v);adj[v].append(u)
    sums=[]
    for root in range(N):
        seen={root};stack=[root];cost=0
        while stack:
            u=stack.pop()
            for v in adj[u]:
                if v in seen:continue
                seen.add(v);stack.append(v)
                a=(v,u) if inward else (u,v)
                if transpose:a=a[::-1]
                cost+=inst['costs'][root][index[a]]+shift
        if len(seen)!=N:return None
        sums.append(cost)
    return sums
def cut_costs(inst,chosen):
    N=inst['N'];totals=[0]*N;index={e:k for k,e in enumerate(inst['edges'])}
    for u,v in chosen:
        adj=[[] for _ in range(N)]
        for a,b in chosen:
            if (a,b)!=(u,v):adj[a].append(b);adj[b].append(a)
        seen={u};stack=[u]
        while stack:
            a=stack.pop()
            for b in adj[a]:
                if b not in seen:seen.add(b);stack.append(b)
        require(v not in seen,'fundamental_cut')
        for r in range(N):totals[r]+=inst['costs'][r][2*index[u,v]+int(r not in seen)]
    return totals
def census(inst,n,m,B):
    costs=[];structured=[];trees=[]
    for chosen in itertools.combinations(inst['edges'],inst['N']-1):
        totals=tree_costs(inst,chosen)
        if totals is None:continue
        require(totals==cut_costs(inst,chosen),'independent_DFS_cut_agreement')
        require(tree_costs(inst,chosen,inward=True,transpose=True)==totals,'independent_transposition')
        require(tree_costs(inst,chosen,shift=1)==[x+inst['N']-1 for x in totals],'independent_shift')
        q=sum(max(u,v)>=n+2 for u,v in chosen);h=int((0,1) in chosen);p=len(chosen)-q-h
        require(q>=m and totals[0]==p+B*q==inst['K']+(1-h)+(B-1)*(q-m),'independent_base_identity')
        value=sum(totals);costs.append(value);trees.append(chosen)
        if h==1 and q==m:structured.append(value)
        elif B>=2:require(value>inst['K'],'unstructured_threshold_exclusion')
    require(bool(costs),'nonempty_census')
    return {'trees':len(costs),'minimum':min(costs),'minimum_structured':min(structured),'minimum_tree':trees[costs.index(min(costs))]}
def min_unsat(clauses,n):
    return min(sum(not any(a[abs(l)-1]==(l>0) for l in c) for c in clauses) for a in itertools.product((False,True),repeat=n))
def main():
    p=argparse.ArgumentParser();p.add_argument('fixture',type=pathlib.Path);p.add_argument('--negative',choices=('guard','cost','minimum'));p.add_argument('--output',type=pathlib.Path);args=p.parse_args()
    if args.negative=='guard':require(False,'independent_false_guard')
    saved=json.loads(args.fixture.read_text());inst=saved['instance'];cs=((1,2),(1,-2),(-1,2),(-1,-2))
    expected,n,m=build(cs,2)
    if args.negative=='cost':inst['costs'][0][0]+=1
    require(inst['costs']==expected['costs'],'complete_fixture_cost_table')
    require(inst['N']==expected['N'] and list(map(tuple,inst['edges']))==expected['edges'] and inst['K']==expected['K'],'complete_fixture_graph_threshold')
    inst['edges']=list(map(tuple,inst['edges']))
    fixture=census(inst,n,m,2);want=10 if args.negative=='minimum' else 11
    require(fixture['trees']==384 and fixture['minimum']==want,'independent_fixture_exact_minimum')
    require(sum(map(len,inst['costs']))==208 and set(x for row in inst['costs'] for x in row)<={0,1,2},'208_explicit_bounded_cost_entries')
    require(saved['spanning_tree_count']==fixture['trees'] and saved['exact_minimum']==fixture['minimum'] and saved['threshold_yes']==(fixture['minimum']<=inst['K']),'fixture_saved_claims')
    contrasts=[]
    for clauses,B in [(((1,2),(2,),(-2,)),1),(((1,2),(2,),(2,),(2,),(-2,),(-2,),(-2,)),2),(((1,2),(2,),(2,),(2,),(-2,),(-2,),(-2,)),3)]:
        model,n,m=build(clauses,B);r=census(model,n,m,B);r.update({'clauses':clauses,'B':B,'K':model['K'],'min_unsatisfied':min_unsat(clauses,n)})
        if B==1:require(r['minimum']==model['K'] and r['min_unsatisfied']>0,'unclaimed_B1_fails')
        else:require(model['K']<r['minimum']<model['K']+r['min_unsatisfied'] and r['minimum_structured']==model['K']+r['min_unsatisfied'],'unclaimed_global_OPT_identity_fails')
        contrasts.append(r)
    report={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PID':os.getpid(),'optimization_level':sys.flags.optimize,'all_pass':True,'fixture':fixture,'counterchecks':contrasts,'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'fixture_sha256':hashlib.sha256(args.fixture.read_bytes()).hexdigest(),'scope':'Fresh implementation and actual controls; finite corroboration only, no all-size or historical-priority inference.'}
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
if __name__=='__main__':main()

