#!/usr/bin/env python3
"""Exploratory bounded positive-measure search; exact verification for witnesses."""
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
import argparse, hashlib, json, platform, time
import numpy as np
import scipy
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
PAIRS=[(3,2),(20,14),(119,84)]
def search(amax,bmax,tmax,seconds):
    # One variable describes an equally weighted pair v,-v. The pushforward
    # of such a pair is determined by the absolute projected value.
    triples=[(a,b,t) for a in range(-amax,amax+1) for b in range(-bmax,bmax+1) for t in range(-tmax,tmax+1) if (a>0 or (a==0 and b>0))]
    rowmap={}; rr=[]; cc=[]; vv=[]
    def row(key):
        if key not in rowmap: rowmap[key]=len(rowmap)
        return rowmap[key]
    for j,(a,b,t) in enumerate(triples):
        for i,(p,q) in enumerate(PAIRS):
            left,right=abs(p*a+t),abs(q*b+t)
            if left!=right:
                rr.extend([row((i,left)),row((i,right))]); cc.extend([j,j]); vv.extend([1.,-1.])
    nr=len(rowmap)
    for j,(a,b,t) in enumerate(triples):
        if a: rr.append(nr);cc.append(j);vv.append(float(a*a))
    mat=coo_matrix((vv,(rr,cc)),shape=(nr+1,len(triples))).tocsr()
    rhs=np.zeros(nr+1);rhs[-1]=1
    started=time.monotonic()
    opt=linprog(np.zeros(len(triples)), A_eq=mat,b_eq=rhs,bounds=(0,None),method='highs',options={'time_limit':seconds})
    out={'box':[amax,bmax,tmax], 'variables':len(triples),'equations':nr+1,'status':int(opt.status),'message':opt.message,'seconds':round(time.monotonic()-started,4),'interpretation':'Exploratory numerical LP status only; no rigorous nonexistence inference.'}
    if opt.success:
        support=[(triples[i],Fraction(float(v)).limit_denominator(10**9)) for i,v in enumerate(opt.x) if v>1e-10]
        equalities=[]
        for p,q in PAIRS:
            bal={}
            for (a,b,t),w in support:
                u,v=abs(p*a+t),abs(q*b+t)
                bal[u]=bal.get(u,Fraction())+w
                bal[v]=bal.get(v,Fraction())-w
            equalities.append(all(v==0 for v in bal.values()))
        exact=all(equalities) and sum(a*a*w for (a,b,t),w in support)==1 and all(w>0 for v,w in support)
        out['support_size']=len(support);out['exact_certificate_passed']=exact
        out['support']=[{'triple':list(v),'weight':str(w)} for v,w in support]
        out['max_constraint_residual']=float(abs(mat@opt.x-rhs).max())
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--boxes',nargs='+',default=['2,3,10','3,5,20','4,6,30','6,9,40']);ap.add_argument('--seconds',type=float,default=35)
    args=ap.parse_args();payload={'utc':datetime.now(timezone.utc).isoformat(),'pairs':PAIRS,'numpy':np.__version__,'scipy':scipy.__version__,'python':platform.python_version(),'scope':'bounded rational multiset searches only; infeasible floating-point LP output is not an exact certificate; exact positive weights must satisfy all projection equations','runs':[],'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    target=Path(__file__).with_name('multiset_results.json')
    for b in args.boxes:
        dims=tuple(map(int,b.split(',')));res=search(*dims,args.seconds);payload['runs'].append(res);target.write_text(json.dumps(payload,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k!='support'}),flush=True)
        if res.get('exact_certificate_passed'): break
if __name__=='__main__':main()
