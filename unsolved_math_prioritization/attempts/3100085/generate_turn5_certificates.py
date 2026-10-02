"""Exact fixed-span root isolation using the proved Turn4 reduction."""
from math import prod
from pathlib import Path
import json

P=lambda x,r:prod(range(x+1,x+r+1))
cases=[];left_cases=0;roots=[]
for r in range(3,13):
    for u in range(1,r):
        for v in range(u+1,r-u):
            s=r-u-v;delta=v-u;M=max(r-1,(r*r-1)//(6*delta)+1)
            for A in range(M-1):
                left_cases+=1;pa=P(A,r)**s;pu=P(A+u,s)**r
                if pa>=pu:continue
                D=lambda B:pa*P(B+v,s)**r-P(B,r)**s*pu
                L=A;U=A+1
                while D(U)>0:U=A+2*(U-A)
                if D(U)==0:
                    roots.append([r,u,v,A,U]);continue
                while U-L>1:
                    mid=(L+U)//2;z=D(mid)
                    if z==0:roots.append([r,u,v,A,mid]);L=U=mid;break
                    if z>0:L=mid
                    else:U=mid
                cases.append({'r':r,'u':u,'v':v,'s':s,'A':A,'L':L,'U':U,'D_L':D(L),'D_U':D(U)})
out={'outer_span_max':12,'left_cases':left_cases,'cases':cases,'integer_roots':roots}
Path(__file__).with_name('TURN_5_CERTIFICATES.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('left cases',left_cases,'root candidates',len(cases),'integer roots',len(roots))
