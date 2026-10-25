"""Independent graph/switching arithmetic, written from the printed manuscript.
Does not import any published program, certificate, or reviewer conclusion.
"""
import itertools as it, json, math, time
from pathlib import Path
from datetime import datetime, timezone
import sympy as S
F=S.Rational
OUT=Path(__file__).parent
checks=[]
def ck(name, value, detail=None):
    checks.append({'name':name,'pass':bool(value),'detail':detail})
    if not value: raise AssertionError((name,detail))

def xor(xs):
    y=0
    for x in xs:y^=x
    return y

def fourier(edges, leaves, params, weights, chars):
    """Rooted switching formula via direct descendant sets, no suppression."""
    parents={}
    for u,v in edges:parents.setdefault(v,[]).append(u)
    ret=[v for v,p in parents.items() if len(p)==2]
    result=0
    for selection in it.product([0,1], repeat=len(ret)):
        chosen={v:parents[v][k] for v,k in zip(ret,selection)}
        es=[(u,v) for u,v in edges if v not in chosen or chosen[v]==u]
        children={u:[] for e in es for u in e}
        for u,v in es:children[u].append(v)
        def desc(v):return {v} if v in leaves else set().union(*(desc(w) for w in children[v]))
        val=S.prod(weights[v][chosen[v]] for v in ret)
        for u,v in es:
            h=xor(chars[leaves.index(w)] for w in desc(v))
            if h:val*=params[(u,v)][int(h==2)]
        result+=val
    return S.expand(result)

def rootings(edges, leaves):
    """Brute-force all mixed-edge root placements and all free orientations."""
    parents={}
    for u,v in edges:parents.setdefault(v,[]).append(u)
    ret={v for v,p in parents.items() if len(p)==2}
    root_children=[v for u,v in edges if u=='r']
    mixed=[]
    for u,v in edges:
        if u!='r': mixed.append((u,v,v if v in ret else None))
    a,b=root_children
    mixed.append((a,b,(a if a in ret else b) if (a in ret or b in ret) else None))
    result=[]
    for site,(a,b,head) in enumerate(mixed):
        rest=mixed[:site]+mixed[site+1:]
        fixed=[(u,v) if h==v else (v,u) for u,v,h in rest if h]
        ordinary=[(u,v) for u,v,h in rest if not h]
        for flip in it.product([0,1],repeat=len(ordinary)):
            es=fixed+[e[::-1] if f else e for e,f in zip(ordinary,flip)]+[('r',a),('r',b)]
            verts=set(sum(([u,v] for u,v in es),[]))
            ins={v:[] for v in verts};outs={v:[] for v in verts}
            for u,v in es:ins[v].append(u);outs[u].append(v)
            if any((len(ins[v]),len(outs[v]))!=((0,2) if v=='r' else (1,0) if v in leaves else (2,1) if v in ret else (1,2)) for v in verts):continue
            order=[]; todo=['r']; ind={v:len(ins[v]) for v in verts}
            while todo:
                u=todo.pop();order.append(u)
                for v in outs[u]:
                    ind[v]-=1
                    if ind[v]==0:todo.append(v)
            if len(order)!=len(verts):continue
            dominators={'r':{'r'}}
            for v in order[1:]:dominators[v]=set.intersection(*(dominators[p] for p in ins[v]))|{v}
            if set.intersection(*(dominators[v] for v in leaves))!={'r'}:continue
            tc=all(any(w not in ret for w in outs[v]) for v in verts if outs[v])
            result.append({'site':site,'edge':[a,b],'tree_child':tc,'arcs':es})
    return mixed,result

def run():
    # Exact domain controls: independently derive inverse Fourier transform.
    s,g=S.symbols('s g')
    H=S.Matrix([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])
    p=H*S.Matrix([1,s,g,s])/4
    ck('inverse Fourier probabilities', p==S.Matrix([(1+2*s+g)/4,(1-2*s+g)/4,(1-g)/4,(1-g)/4]))
    bad=(F(4,5),F(61,100))
    ck('positive domain includes non-CT edges',bad[1]>2*bad[0]-1 and bad[1]<bad[0]**2)
    ck('square-root closure is false on principal domain',S.sqrt(bad[1])<2*S.sqrt(bad[0])-1)
    for d in range(3,11):
        rows=[]
        for a,b in [(0,1),(0,2),(1,2)]+[(0,k) for k in range(3,d)]:
            rows.append([int(i in [a,b]) for i in range(d)])
        ck(f'bridge anchor determinant degree{d}',S.Matrix(rows).det()==-2)
    # Triangle formula independently differentiated in ordinary coordinates.
    letters='abcdef';sym={e:S.symbols(e+'s '+e+'g') for e in letters};la=S.symbols('lam')
    spec=lambda e,h: 1 if h==0 else sym[e][int(h==2)]
    def tri(h):
        x,y,z=h
        return spec('a',x)*spec('b',y)*spec('c',z)*(la*spec('f',y)*spec('d',z)+(1-la)*spec('f',x)*spec('e',z))
    qs=[(0,0,0),(0,1,1),(0,2,2),(1,0,1),(1,1,0),(1,2,3),(1,3,2),(2,0,2),(2,1,3),(2,2,0)]
    tensor=[tri(h) for h in qs]
    witness={la:F(1,2)}
    witness.update({v:F(1,3) if k=='f' else F(1,2) for k,vs in sym.items() for v in vs})
    tv=[q.subs(witness) for q in tensor]
    ck('triangle common symmetric tensor',tv==[1,F(1,12),F(1,12),F(1,12),F(1,12),F(1,48),F(1,48),F(1,12),F(1,48),F(1,12)])
    jac=S.Matrix(tensor[1:]).jacobian(sum((list(v) for v in sym.values()),[])+[la]).subs(witness)
    ck('triangle exact Jacobian rank',jac.rank()==9,{'rank':jac.rank(),'pivot_columns':list(jac.rref()[1])})
    xs,xg,yg,zg,V=tri((1,1,0)),tri((2,2,0)),tri((2,0,2)),tri((0,2,2)),tri((1,3,2))
    formula=-sym['a'][0]**2*sym['b'][0]**2*sym['a'][1]*sym['b'][1]*sym['c'][1]**2*sym['f'][0]**2*la*(1-la)*sym['d'][1]*sym['e'][1]*(1-sym['f'][1])**2
    ck('whole-map T3 identity',S.expand(V**2*xg-xs**2*yg*zg-formula)==0)
    # Printed weak-class graphs, not the classifier encodings.
    graphW=[('r','S'),('r','L0'),('S','U'),('S','V'),('U','X'),('V','Z'),('Z','X'),('U','V'),('Z','L1'),('X','L2')]
    graphV=[('r','S'),('r','L0'),('S','U'),('S','X0'),('V','X0'),('U','X1'),('V','X1'),('U','V'),('X0','L1'),('X1','L2')]
    ds=F(1,2**30); root_records={}
    for name,edges,base,ws,pend,cols,rows,expected in [
      ('W',graphW,F(1,7),{'X':{'Z':F(15996,16339),'U':F(343,16339)},'V':{'S':F(1,8),'U':F(7,8)}},[F(86779,80)*ds,F(320,253)*ds,F(114373,20240)*ds],[('Z','X'),('S','V'),('r','S'),('S','U'),('U','V')],[1,2,3,5,4,7,6,8,9],F(10368019213741323,563981315074464023964442388464888915634290688)),
      ('Wprime',graphV,F(1,4),{'X1':{'V':F(1,2),'U':F(1,2)},'X0':{'V':F(1,6),'S':F(5,6)}},[F(16,3)*ds,F(32,9)*ds,F(96,5)*ds],[('V','X1'),('V','X0'),('U','V'),('r','S'),('S','X0')],[1,2,3,5,4,6,7,8,9],F(1435825,85002596691653613846528))]:
        leaves=['L0','L1','L2']; internal=[e for e in edges if e[1] not in leaves]
        pairs={e:S.symbols('s_'+e[0]+e[1]+' g_'+e[0]+e[1]) if e in internal else (1,1) for e in edges}
        polys=[fourier(edges,leaves,pairs,ws,h) for h in qs]
        at={v:base for e in internal for v in pairs[e]}
        val=[q.subs(at) for q in polys]
        physical=[val[i]*S.prod(pend[j] for j,h in enumerate(chars) if h) for i,chars in enumerate(qs)]
        ck(name+' common tensor',physical==[1,ds**2,ds**2,ds**2,ds**2,F(4,5)*ds**3,F(4,5)*ds**3,ds**2,F(4,5)*ds**3,ds**2])
        columns=sum((list(pairs[e]) for e in cols),[])[:9]
        minor=S.Matrix([polys[i] for i in rows]).jacobian(columns).subs(at).det()
        ck(name+' printed exact minor',minor==expected,{'actual':str(minor)})
        ck(name+' strict CT values',all(0<x<1 and x>x*x for x in [base]+pend))
        mixed,rooted=rootings(edges,leaves)
        census=[len(rooted),sum(r['tree_child'] for r in rooted),sum(not r['tree_child'] for r in rooted)]
        ck(name+' independent rooting census',census==([5,2,3] if name=='W' else [7,2,5]),census)
        root_records[name]={'mixed':mixed,'rootings':rooted}
    # Completion arithmetic derived directly from the printed grammar.
    specs=[(2,1,1),(5,1,2),(5,1,2),(6,2,4),(6,2,2)]
    def completions(k,inc):return sum(r*sum(math.comb(q,j)*math.comb(k-inc-j+m-1,m-1) for j in range(q+1) if k-inc-j>=0) for m,q,r in specs)
    for k,inc,count in [(4,1,831),(4,0,1983),(5,1,1983),(5,0,4155)]:ck(f'completion count {k},{inc}',completions(k,inc)==count)
    ck('four-port directions',6*(completions(4,0)+completions(4,1))*math.factorial(4)==405216)
    ck('five-port directions',4*(completions(5,0)+completions(5,1))*math.factorial(5)==2946240)
    OUT.joinpath('independent-rootings.json').write_text(json.dumps(root_records,indent=2)+'\n')

if __name__=='__main__':
    start=time.monotonic();error=None
    try:run()
    except Exception as e:error=repr(e)
    result={'utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-start,'count':len(checks),'all_pass':error is None,'error':error,'checks':checks}
    OUT.joinpath('independent-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if error:raise SystemExit(1)
