#!/usr/bin/env python3
"""Exact spectra for repeated proper-colored K5 blocks in a rainbow finite core."""
import itertools,json,math

def k5_core(n,b):
    assert n>=5*b
    edges={}; nxt=2+5*b
    for i in range(n):
      for j in range(i+1,n):
        if i//5==j//5 and i//5<b:
          edges[i,j]=2+5*(i//5)+(i%5+j%5)%5
        else:
          edges[i,j]=nxt;nxt+=1
    return {'n':n,'tail':0,'spokes':[1]*n,'edges':[[i,j,col] for (i,j),col in edges.items()]}

def spectrum(model):
    n=model['n'];edge={(i,j):c for i,j,c in model['edges']};pal=[1<<model['tail']]*(1<<n);sp=model['spokes'];counts={}
    for S in range(1<<n):
      if S:
        bit=S&-S;i=bit.bit_length()-1;T=S^bit
        p=pal[T]|(1<<sp[i]);rest=T
        while rest:
          b=rest&-rest;j=b.bit_length()-1;rest^=b
          p|=1<<edge[min(i,j),max(i,j)]
        pal[S]=p
      count=pal[S].bit_count();counts[count]=counts.get(count,0)+1
    return sorted(counts),counts

def main():
    results=[]
    for b in range(1,4):
      n=5*b;model=k5_core(n,b);s,counts=spectrum(model)
      assert sum(counts.values())==2**n
      expected=2+math.comb(n,2)-5*b
      assert max(s)==expected
      results.append({'n':n,'blocks':b,'colors':expected,'spectrum':s,'subsets_checked':sum(counts.values())})
    model=k5_core(16,2);s,counts=spectrum(model)
    assert 43 not in s and max(s)==112
    open('witness_c112_m43.json','w').write(json.dumps({'c':112,'m':43,'model':model,'spectrum':s,'subsets_checked':sum(counts.values())},indent=2)+'\n')
    results.append({'n':16,'blocks':2,'colors':112,'avoided_m':43,'spectrum':s,'subsets_checked':sum(counts.values())})
    out={'description':'Finite core certificate and exact complete subset replay. No novelty or complete Erickson resolution asserted.','results':results}
    print(json.dumps(out,indent=2));open('deficit_block_checks.json','w').write(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
