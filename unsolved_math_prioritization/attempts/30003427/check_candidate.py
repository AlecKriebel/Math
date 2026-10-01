"""Exact finite compression and encoding controls. No CAD/QE solver is run."""
from fractions import Fraction as F
from collections import Counter
from itertools import product
import json,copy
import sympy as sp
from encode_system import compile_system
counts=Counter()
def ck(v,label):
    assert v,label
    counts[label]+=1
def caratheodory(points,weights):
    points=list(points);weights=list(weights);indices=list(range(len(points)));d=len(points[0])
    original=[sum(w*x[j] for w,x in zip(weights,points)) for j in range(d)]
    while len(points)>d+1:
        A=sp.Matrix([[1]*len(points)]+[[sp.Rational(x[j].numerator,x[j].denominator) for x in points] for j in range(d)])
        c=[F(v) for v in A.nullspace()[0]]
        if not any(v>0 for v in c):c=[-v for v in c]
        theta=min(w/v for w,v in zip(weights,c) if v>0)
        weights=[w-theta*v for w,v in zip(weights,c)]
        ck(all(w>=0 for w in weights),'compression_nonnegative_weights')
        keep=[i for i,w in enumerate(weights) if w]
        points=[points[i] for i in keep];weights=[weights[i] for i in keep];indices=[indices[i] for i in keep]
        ck(sum(weights)==1,'compression_normalization')
        ck([sum(w*x[j] for w,x in zip(weights,points)) for j in range(d)]==original,'compression_barycenter_exact')
    return indices,weights
# Original finite models with adapted reference coordinate independent of shadow-history coding.
def build(depth,T,code):
    if depth==T:return {'z':F(4)+F(code%17,19),'children':[],'depth':depth,'code':code}
    children=[build(depth+1,T,8*code+j+1) for j in range(8)]
    raw=[F(1+(code+3*j)%5) for j in range(8)];total=sum(raw);weights=[w/total for w in raw]
    return {'z':sum(w*c['z'] for w,c in zip(weights,children)),'children':list(zip(weights,children)),'depth':depth,'code':code}
def assign(node,T,history):
    d=node['depth']
    if d:
        node['r']=node['z']+F((node['code']%5)-2,8)
        history=history+[max(F(0),node['r']-(F(2)+F(d,3)))]
    if not node['children']:node['V']=history
    else:
        for w,c in node['children']:assign(c,T,history)
        node['V']=[sum(w*c['V'][j] for w,c in node['children']) for j in range(T)]
def compress(node):
    if not node['children']:return copy.deepcopy(node)
    points=[[c['z']]+c['V'] for _,c in node['children']]
    ids,ws=caratheodory(points,[w for w,_ in node['children']])
    out={k:copy.deepcopy(v) for k,v in node.items() if k!='children'}
    out['children']=[(w,compress(node['children'][i][1])) for i,w in zip(ids,ws)]
    return out
def audit(node,T,history):
    d=node['depth']
    if d:
        ck(node['r']>=1 and node['z']>0 and abs(node['r']-node['z'])<=1,'node_model_conditions')
        history=history+[max(F(0),node['r']-(F(2)+F(d,3)))]
    if not node['children']:
        ck(node['V']==history,'leaf_actual_payoff_vector')
        return history,1
    ck(len(node['children'])<=T+2,'uniform_branch_bound')
    ck(all(w>0 for w,_ in node['children']) and sum(w for w,_ in node['children'])==1,'positive_conditional_law')
    ck(sum(w*c['z'] for w,c in node['children'])==node['z'],'node_martingale_preserved')
    vals=[(w,audit(c,T,history)) for w,c in node['children']]
    avg=[sum(w*v[0][j] for w,v in vals) for j in range(T)]
    ck(avg==node['V'],'conditional_all_quote_expectations')
    return avg,sum(v[1] for _,v in vals)
for T in [2,3]:
    for seed in [1,4,11]:
        original=build(0,T,seed);assign(original,T,[]);new=compress(original)
        values,leaves=audit(new,T,[])
        ck(values==original['V'],'global_quotes_preserved')
        ck(new['z']==original['z'],'initial_shadow_preserved')
        ck(leaves<=(T+2)**T,'leaf_bound')
# Verify every generated polynomial is quadratic and symbols are correctly scoped.
for shape in [[1],[1,1],[1,2],[2,1,1]]:
    out=compile_system(shape);names=out['free_parameters']+out['existential_variables']
    syms=sp.symbols(' '.join(names));lookup=dict(zip(names,syms))
    for lhs,rel,rhs in out['conjunction']+out['input_conditions']:
        expr=sp.sympify(lhs,locals=lookup)-sp.sympify(rhs,locals=lookup)
        poly=sp.Poly(expr,*(sorted(expr.free_symbols,key=str) or [syms[0]]))
        ck(poly.total_degree()<=2,'encoded_degree_at_most_two')
        ck(poly.as_expr().free_symbols<=set(syms),'encoded_symbol_scope')
    ck(out['leaves']==(sum(shape)+2)**len(shape),'compiled_leaf_bound')
# Positive-part encoding excludes each wrong branch.
for r,k,c in product([F(-2),F(-1,3),F(0),F(1,4),F(2),F(5)],repeat=3):
    encoded=c>=0 and c>=r-k and c*(c-r+k)==0
    ck(encoded==(c==max(F(0),r-k)),'positive_part_exact_equivalence')
# Two-date strict-positive witness for every sampled positive epsilon.
strikes=[F(1,4),F(1,2),F(3,4)];prices=[F(13,16),F(5,8),F(7,16)]
for den in range(5,101):
    e=F(1,den);rs=[e,F(4,3)];zs=[e,F(4,3)-e/3];ps=[F(1,4),F(3,4)]
    ck(sum(p*z for p,z in zip(ps,zs))==1,'example_shadow_mean')
    for t in [1,2]:
        for r,z in zip(rs,zs):ck(r>=e and r>0 and z>0 and abs(r-z)<=e,'example_pathwise_admissibility')
        for k,c in zip(strikes,prices):ck(sum(p*max(F(0),r-k) for p,r in zip(ps,rs))==c,'example_call_calibration')
    for z in zs:
        ck(sum(F(1,8)*z for _ in range(8))==z,'example_constant_second_transition')
# Test all compiled constraints on an explicit full 8-ary two-date model.
compiled=compile_system([3,3]);b=8
for den in [5,7,11,29,101]:
    e=F(1,den)
    values={'epsilon':e,'s_bid':F(1),'s_ask':F(1),'w_root':F(1),'z_root':F(1)}
    for t in [1,2]:
        for i,(k,c) in enumerate(zip(strikes,prices)):
            values[f'k_{t}_{i}']=k;values[f'bid_{t}_{i}']=c;values[f'ask_{t}_{i}']=c
    for t in range(3):
        for u in product(range(b),repeat=t):
            tag='root' if not u else '_'.join(map(str,u))
            if t:
                low=u[0]<2;r=e if low else F(4,3);z=e if low else F(4,3)-e/3
                values['w_'+tag]=F(1,b**t);values['z_'+tag]=z;values['r_'+tag]=r
                for i,k in enumerate(strikes):values['c'+str(i)+'_'+tag]=max(F(0),r-k)
            if t<2:
                for j in range(b):values['p'+str(j)+'_'+tag]=F(1,b)
    ck(set(values)==set(compiled['free_parameters']+compiled['existential_variables']),'full_witness_variable_coverage')
    for lhs,rel,rhs in compiled['conjunction']+compiled['input_conditions']:
        x=eval(lhs,{'__builtins__':{}},values);y=eval(rhs,{'__builtins__':{}},values)
        ck({'=':x==y,'>':x>y,'>=':x>=y,'<=':x<=y}[rel],'full_witness_all_polynomial_constraints')

# Exact boundary identities used to rule out epsilon=0.
ck(prices[0]-2*prices[1]+prices[2]==0,'example_zero_butterfly_price')
ck((prices[0]-prices[2])/(strikes[2]-strikes[0])==F(3,4),'example_forced_upper_probability')
ck(prices[2]+strikes[2]*F(3,4)==1,'example_forced_upper_mean')
x=sp.symbols('x')
# Butterfly piecewise is 0, x-1/4, 3/4-x, 0 on the four strike regions.
ck(sp.expand((x-sp.Rational(1,4))-2*(x-sp.Rational(1,2)))==sp.Rational(3,4)-x,'butterfly_right_piece')
ck(sp.expand((x-sp.Rational(1,4))-2*(x-sp.Rational(1,2))+(x-sp.Rational(3,4)))==0,'butterfly_tail_piece')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'families':dict(sorted(counts.items())),'sympy_version':sp.__version__,'scope':'Exact finite compression, encoding and attainment controls; no general quantifier-elimination solver execution or independent theorem review.'},indent=2,sort_keys=True))
