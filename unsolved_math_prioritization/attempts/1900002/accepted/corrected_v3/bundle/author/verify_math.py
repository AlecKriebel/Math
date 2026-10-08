#!/usr/bin/env python3
"""Exact finite arithmetic/scope audit, not a formal proof or total IKEA solver."""
import argparse, hashlib, itertools, json, math, pathlib, random, stat, sys

def require(ok, message):
    if not ok:
        raise ValueError(message)

def strict_pairs(items):
    out = {}
    for k, v in items:
        require(k not in out, 'duplicate JSON key')
        out[k] = v
    return out

def bad_constant(value):
    raise ValueError('nonfinite JSON constant')

def loads(data):
    return json.loads(data, object_pairs_hook=strict_pairs, parse_constant=bad_constant)

def canonical(x):
    return json.dumps(x, sort_keys=True).encode('utf-8')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def integer_list(s, positive=False):
    require(type(s) is list and len(s) <= 4096, 'bounded integer list required')
    require(all(type(x) is int and abs(x) <= 10**12 and (not positive or x > 0) for x in s), 'invalid integer entry')

def continuant(s):
    p, q = 0, 1
    for x in s:
        p, q = q, x*q+p
    return q

def matrix(s):
    a, b, c, d = 1, 0, 0, 1
    for x in s:
        a, b, c, d = a*x+b, a, c*x+d, c
    return a, b, c, d

def sign_changes(s):
    t = [x for x in s if x]
    return sum(a*b < 0 for a,b in zip(t,t[1:]))

def concatenate(blocks, curvatures):
    result = []
    for i, block in enumerate(blocks):
        if i:
            result.append(curvatures[i-1])
        result.extend(block)
    return result

def evaluate(blocks, curvatures):
    require(type(blocks) is list and 3 <= len(blocks) <= 128, '3 to 128 angle blocks required')
    integer_list(curvatures)
    require(len(curvatures) == len(blocks), 'one curvature per edge required')
    for block in blocks:
        integer_list(block, positive=True)
        require(len(block) % 2 == 1, 'LLS block must have positive odd length')
    prefixes = [continuant(concatenate(blocks[:j], curvatures)) for j in range(1,len(blocks)+1)]
    tail = concatenate(blocks[1:], curvatures[1:])
    denominator = continuant(tail)
    numerator = continuant(tail+[1])
    closure = prefixes[-1] == 0
    last = denominator != 0 and curvatures[-1] == -(numerator // denominator)
    winding = sign_changes(prefixes) == len(blocks)-3
    return {'criterion': closure and last and winding, 'closure': closure, 'last_curvature': last,
            'winding': winding, 'prefix_continuants': prefixes, 'tail_denominator': denominator,
            'tail_numerator': numerator, 'sign_changes': sign_changes(prefixes)}

def bezout(a,b):
    aa,bb=abs(a),abs(b)
    r0,r1,s0,s1,t0,t1=aa,bb,1,0,0,1
    while r1:
        q=r0//r1
        r0,r1,s0,s1,t0,t1=r1,r0-q*r1,s1,s0-q*s1,t1,t0-q*t1
    require(r0==1, 'primitive vector required')
    return s0*(1 if a>=0 else -1),t0*(1 if b>=0 else -1)

def sub(a,b):
    return a[0]-b[0],a[1]-b[1]

def det(a,b):
    return a[0]*b[1]-a[1]*b[0]

def primitive(v):
    d=math.gcd(*v)
    require(d>0,'zero vector')
    return v[0]//d,v[1]//d

def odd_cf(p,q):
    require(p>=q>0 and math.gcd(p,q)==1, 'normalized fraction required')
    out=[]
    while q:
        a,r=divmod(p,q);out.append(a);p,q=q,r
    if len(out)%2==0:
        out[-1]-=1;out.append(1)
    return out

def angle_block(u,v):
    u,v=primitive(u),primitive(v)
    determinant=det(u,v)
    require(determinant>0, 'clockwise polygon angle ordering required')
    a,b=bezout(*u)
    x=(a*v[0]+b*v[1])%determinant
    if determinant==1:
        x=1
    return odd_cf(determinant,x)

def polygon_data(points):
    require(len(points)>=3, 'polygon too short')
    n=len(points)
    # Strong support-side test establishes strictly convex clockwise input.
    for i in range(n):
        e=sub(points[(i+1)%n],points[i])
        require(all(det(e,sub(points[j],points[i]))<0 for j in range(n) if j not in (i,(i+1)%n)), 'not a strict clockwise polygon')
    blocks=[];curvatures=[]
    for i in range(n):
        a,b,c,d=[points[k%n] for k in (i-1,i,i+1,i+2)]
        blocks.append(angle_block(sub(a,b),sub(c,b)))
        e=primitive(sub(c,b));r,s=bezout(*e)
        def xy(v):
            return r*v[0]+s*v[1],-det(e,v)
        ax,ay=xy(sub(a,b));dx,dy=xy(sub(d,c))
        require(ay>0 and dy>0, 'interior side convention')
        curvatures.append(-((-ax)//ay)-(dx//dy)-2)
    return blocks,curvatures

def hull(points):
    a=sorted(set(points))
    def half(seq):
        h=[]
        for p in seq:
            while len(h)>1 and det(sub(h[-1],h[-2]),sub(p,h[-1]))<=0:
                h.pop()
            h.append(p)
        return h
    return list(reversed(half(a)[:-1]+half(a[::-1])[:-1]))

def run_math():
    checks=0
    for length in range(7):
        for s in itertools.product(range(-2,3),repeat=length):
            a,b,c,d=matrix(s)
            require(continuant(s)==a, 'matrix/recurrence mismatch')
            require(a*d-b*c==(-1)**length, 'unimodular identity mismatch')
            require(continuant(s)==continuant(s[::-1]), 'continuant reversal mismatch')
            checks+=1
    require(continuant([-1,2,-3])==2, 'signed numerator convention')
    require(sign_changes([3,0,-1,0,-4,0,2,0])==2, 'zero deletion convention')
    example_blocks=[[1,3,1,1,1],[3],[1,2,1],[3,1,3]]
    example_curvatures=[-1,-2,-1,-1]
    example=evaluate(example_blocks,example_curvatures)
    require(example=={'criterion':True,'closure':True,'last_curvature':True,'winding':True,
                     'prefix_continuants':[14,-1,-15,0],'tail_denominator':-14,'tail_numerator':-17,'sign_changes':1}, 'published example mismatch')
    derived=polygon_data([(0,0),(2,3),(3,3),(4,-1)])
    require(derived==(example_blocks,example_curvatures), 'independent polygon extraction mismatch')
    cases=[[(0,0),(0,1),(1,0)],[(0,0),(0,2),(3,2),(3,0)],[(0,0),(0,2),(1,3),(3,3),(4,1),(2,0)]]
    rng=random.Random(1900002)
    for _ in range(200):
        p=hull([(rng.randrange(-15,16),rng.randrange(-15,16)) for _ in range(20)])
        if len(p)>=3:
            cases.append(p)
    realizations=0
    for p in cases:
        blocks,curvatures=polygon_data(p)
        require(evaluate(blocks,curvatures)['criterion'], 'geometric witness rejected')
        for j in range(len(p)):
            require(evaluate(blocks[j:]+blocks[:j],curvatures[j:]+curvatures[:j])['criterion'], 'cyclic convention mismatch')
        transformed=[(x+3*y+7, y-5) for x,y in p]
        require(polygon_data(transformed)==(blocks,curvatures), 'unimodular affine invariance mismatch')
        scaled=[(3*x,3*y) for x,y in p]
        require(polygon_data(scaled)==(blocks,curvatures), 'parallel scaling data mismatch')
        realizations+=1
    bad=example_curvatures.copy();bad[-1]=0
    require(not evaluate(example_blocks,bad)['criterion'], 'wrong closing curvature accepted')
    # Going twice around a triangle creates local closure with the wrong winding.
    tb,tc=polygon_data(cases[0])
    doubled=evaluate(tb*2,tc*2)
    require(doubled['closure'] and doubled['last_curvature'] and not doubled['winding'] and not doubled['criterion'], 'winding negative control failed')
    malformed=[([],[]),([[1],[1],[1]],[0,0]),([[1],[1],[True]],[0,0,0]),([[1],[1],[1.0]],[0,0,0]),([[1],[1],[-1]],[0,0,0]),([[1],[1],[1,1]],[0,0,0]),([[1],[1],[1]],[0,False,0]),([[1],[1],[10**13]],[0,0,0])]
    for b,c in malformed:
        try:
            evaluate(b,c)
        except ValueError:
            pass
        else:
            raise ValueError('malformed angle data accepted')
    for s in ['{"x":1,"x":2}','{"x":NaN}','{"x":Infinity}','{']:
        try:
            loads(s)
        except (ValueError,json.JSONDecodeError):
            pass
        else:
            raise ValueError('malformed JSON accepted')
    return {'matrix_words':checks,'convex_polygon_cases':realizations,'malformed_inputs_rejected':len(malformed)+4,
            'closing_curvature_control':'rejected','nonconvex_winding_control':'rejected','published_example':'matched'}

def read_regular(p):
    require(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode), 'regular file required')
    return p.read_bytes()

def match(data,identity):
    require(len(data)==identity['bytes'] and sha(data)==identity['sha256'], 'byte identity mismatch')

def corpus_binding(problems,reports):
    metadata=loads((pathlib.Path(__file__).parent/'CORPUS_BINDINGS.json').read_bytes())
    pb,rb=read_regular(problems),read_regular(reports)
    match(pb,metadata['corpora']['problems.json']);match(rb,metadata['corpora']['research_results.json'])
    p,r=loads(pb),loads(rb)
    require(type(p) is list and type(r) is dict,'corpus outer schema')
    selected=[v for v in p if type(v) is dict and v.get('id')==1900002]
    require(len(selected)==1 and selected[0].get('problem_number')=='AMR-018-0002','exact problem key match')
    report=r.get('AMR-018-0002');require(type(report) is dict,'report absent')
    require(sha(canonical(selected[0]))==metadata['problem_record_sha256'],'problem target hash mismatch')
    require(sha(canonical(report))==metadata['report_record_sha256'],'report target hash mismatch')

def source_binding(root):
    metadata=loads((pathlib.Path(__file__).parent/'SOURCE_METADATA.json').read_bytes())
    for item in metadata['pdfs']:
        match(read_regular(root/item['filename']),item)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--problems',type=pathlib.Path);ap.add_argument('--reports',type=pathlib.Path);ap.add_argument('--sources',type=pathlib.Path)
    a=ap.parse_args();require((a.problems is None)==(a.reports is None),'both corpora required together')
    result={'problem_id':1900002,'status':'SOLVED-IN-LITERATURE-PLANAR-CONVEX','proof_turns':0,
            'math_checks':run_math(),'corpus_binding':'not_supplied','source_binding':'not_supplied',
            'verification_limit':'finite exact arithmetic and byte binding; not formal proof or an exhaustive decision algorithm'}
    if a.problems is not None:
        corpus_binding(a.problems,a.reports);result['corpus_binding']='full_files_and_exact_target_records_match'
    if a.sources is not None:
        source_binding(a.sources);result['source_binding']='both_private_pdf_identities_match'
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except Exception as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(2)
