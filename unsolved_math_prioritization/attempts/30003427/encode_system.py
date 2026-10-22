"""Compile the bounded-tree consistency system, without running quantifier elimination.
Usage: python encode_system.py 1 1 > system.json
Arguments are numbers of actual calls at each date. Coefficients/inputs remain symbolic.
Each predicate is [left polynomial, relation, right polynomial].
"""
import json,sys
from itertools import product

def compile_system(shape):
    assert shape and all(isinstance(n,int) and n>=1 for n in shape)
    T=len(shape);q=sum(shape);b=q+2
    nodes=[u for t in range(T+1) for u in product(range(b),repeat=t)]
    if len(nodes)>50000:raise ValueError('Output-size safeguard; theoretical formula is unchanged. Raise manually if desired.')
    def tag(u):return 'root' if not u else '_'.join(map(str,u))
    def var(stem,u):return stem+'_'+tag(u)
    params=['epsilon','s_bid','s_ask'];unknown=[];pred=[]
    def add(l,op,r):pred.append([str(l),op,str(r)])
    for t,n in enumerate(shape,1):
        for i in range(n):params.extend([f'k_{t}_{i}',f'bid_{t}_{i}',f'ask_{t}_{i}'])
    add('epsilon','>=',0);add('s_ask-s_bid','<=','epsilon')
    add('z_root','>=','s_bid');add('z_root','<=','s_ask');add('w_root','=',1)
    for u in nodes:
        unknown.extend([var('w',u),var('z',u)])
        t=len(u)
        if t<T:
            p=[var('p'+str(j),u) for j in range(b)]
            unknown.extend(p)
            for x in p:add(x,'>',0)
            add('+'.join(p),'=',1)
            for j in range(b):add(var('w',u+(j,)),'=',var('w',u)+'*'+p[j])
            add(var('z',u),'=','+'.join(p[j]+'*'+var('z',u+(j,)) for j in range(b)))
        if t:
            r=var('r',u);z=var('z',u);unknown.append(r)
            add(r,'>',0);add(z,'>',0);add(r,'>=','epsilon')
            add(r+'-'+z,'>=','-epsilon');add(r+'-'+z,'<=','epsilon')
            for i in range(shape[t-1]):
                c=var('c'+str(i),u);k=f'k_{t}_{i}';unknown.append(c)
                add(c,'>=',0);add(c,'>=',r+'-'+k)
                add(c+'*('+c+'-'+r+'+'+k+')','=',0)
    for t,n in enumerate(shape,1):
        for i in range(n):
            price='+'.join(var('w',u)+'*'+var('c'+str(i),u) for u in nodes if len(u)==t)
            add(price,'>=',f'bid_{t}_{i}');add(price,'<=',f'ask_{t}_{i}')
    inputs=[['s_bid','>', '0'],['s_ask','>=','s_bid']]
    for t,n in enumerate(shape,1):
        for i in range(n):
            inputs.extend([[f'k_{t}_{i}','>', '0'],[f'bid_{t}_{i}','>', '0'],[f'ask_{t}_{i}','>=',f'bid_{t}_{i}']])
            if i:inputs.append([f'k_{t}_{i}','>',f'k_{t}_{i-1}'])
    assert len(unknown)==len(set(unknown))
    return {'shape':shape,'branching':b,'nodes':len(nodes),'leaves':b**T,'free_parameters':params,'input_conditions':inputs,'existential_variables':unknown,'conjunction':pred,'quantifier':'exists all existential_variables','interpretation':'Source epsilon consistency; no QE solver has been invoked.'}
if __name__=='__main__':
    print(json.dumps(compile_system([int(s) for s in sys.argv[1:]]),indent=2,sort_keys=True))
