#!/usr/bin/env python3
"""Independent mechanism: collect actual truncated-ring units, not Lie linear sums.
Produces a straight-line group word certifying s in <L,exp(I)> for the class10 quotient.
"""
from nilpotent_lie_filter import P,add,scalar,prod,exp,log,inverse
from pathlib import Path
import json,time
C=json.loads(Path(__file__).with_name('rank5_lie_certificate.json').read_text());cap=C['class_bound'];one={'':1}
nodes=[];units=[]
def node(d,u):nodes.append(d);units.append(u);return len(nodes)-1
def seed(kind,index,u):return node({'op':'seed','kind':kind,'index':index},u)
def power(a,k):
    k%=P
    if k==1:return a
    u=exp(scalar(log(units[a],cap),k),cap)
    return node({'op':'pow','arg':a,'exponent':k},u)
def multiply(a,b):return node({'op':'multiply','left':a,'right':b},prod(units[a],units[b],cap))
def commutator(a,b):return multiply(multiply(multiply(power(a,-1),power(b,-1)),a),b)
def key(w):return (len(w),w)
rows={};queue=[]
def reduce(a):
    for pivot,b in sorted(rows.items(),key=lambda z:key(z[0])):
        coefficient=units[a].get(pivot,0)
        if coefficient:a=multiply(power(b,-coefficient),a)
    return a

def insert(a):
    a=reduce(a);u=add(units[a],one,-1)
    if not u:return None
    pivot=min(u,key=key);a=power(a,pow(u[pivot],-1,P));rows[pivot]=a;queue.append(a);return a
start=time.time()
for i,r in enumerate(C['ideal_basis']):insert(seed('ideal_exponential',i,exp(r,cap)))
for i,r in enumerate(C['L_generator_logs']):insert(seed('L_generator_exponential',i,exp(r,cap)))
for position,a in enumerate(queue):
    da=min(len(w) for w in units[a] if w)
    for b in queue[:position]:
        db=min(len(w) for w in units[b] if w)
        if da+db<=cap:insert(commutator(a,b))
    if position%10==0:print('processed',position,'basis',len(queue),'nodes',len(nodes),flush=True)
snode=seed('s',0,exp({'x':1},cap));remainder=reduce(snode);assert units[remainder]==one
# Reduce proof DAG to exactly the ancestors used in this identity.
keep=set()
def visit(i):
    if i in keep:return
    keep.add(i);n=nodes[i]
    if n['op']=='pow':visit(n['arg'])
    if n['op']=='multiply':visit(n['left']);visit(n['right'])
visit(remainder);ids=sorted(keep);remap={old:i for i,old in enumerate(ids)};proof=[]
for old in ids:
    d=dict(nodes[old])
    for field in ('arg','left','right'):
        if field in d:d[field]=remap[d[field]]
    proof.append(d)
out={'scope':'Exact ring-unit identity showing q(s) belongs q(L5) in the exp(R)/exp(I) quotient; together with geometry this certifies interosculation, so this finite cover is not special.','prime':P,'class':cap,'basis_dimension_found':len(rows),'proof_nodes':proof,'identity_node':remap[remainder],'original_basis_count':len(rows),'elapsed_seconds':time.time()-start}
Path(__file__).with_name('rank5_s_membership_slp.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'basis_dimension':len(rows),'nodes_before_pruning':len(nodes),'proof_nodes':len(proof),'seconds':time.time()-start,'identity':units[remainder]}))
