#!/usr/bin/env python3
"""Independent finite mathematical audit. No source documents or datasets required."""
import argparse, hashlib, importlib.util, itertools, json, math, pathlib, random, sys
from fractions import Fraction

PIN = 'e571e6d24aa8087e6a62c694a1c6969428f523de834fe8d8ea6c278193d0aca4'
def need(ok, message):
    if not ok: raise ValueError(message)
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def minus(a,b): return (a[0]-b[0],a[1]-b[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def primitive(a):
    g=math.gcd(*a);need(g>0,'zero direction');return (a[0]//g,a[1]//g)
def hull(points):
    ordered=sorted(set(points))
    def chain(seq):
        out=[]
        for p in seq:
            while len(out)>1 and cross(minus(out[-1],out[-2]),minus(p,out[-1]))<=0:out.pop()
            out.append(p)
        return out
    return chain(ordered)[:-1]+chain(ordered[::-1])[:-1]
def matching_K(word):
    # Enumerate path matchings, multiplying weights of unmatched vertices.
    n=len(word);total=0
    for mask in range(1<<max(0,n-1)):
        if mask & (mask<<1):continue
        covered=mask | (mask<<1);term=1
        for i,x in enumerate(word):
            if not (covered>>i)&1:term*=x
        total+=term
    return total

def matrix_product(word):
    M=((1,0),(0,1))
    for x in word:
        T=((x,1),(1,0))
        M=tuple(tuple(sum(M[i][k]*T[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    return M
def matrix_K(word):return matrix_product(word)[0][0]
def word_for(blocks,cs):
    out=[]
    for i,a in enumerate(blocks):
        if i:out.append(cs[i-1])
        out+=a
    return out

def criterion(blocks,cs):
    prefixes=[matrix_K(word_for(blocks[:i],cs)) for i in range(1,len(blocks)+1)]
    nonzero=[q for q in prefixes if q]
    changes=sum((a>0)!=(b>0) for a,b in zip(nonzero,nonzero[1:]))
    tail=word_for(blocks[1:],cs[1:]);den=matrix_K(tail);num=matrix_K(tail+[1])
    closure=prefixes[-1]==0
    final=den!=0 and cs[-1]==-math.floor(Fraction(num,den))
    return (closure and final and changes==len(blocks)-3,prefixes,den,num,changes)

def brute_sail(u,v):
    # Work directly with all lattice points of the primitive triangle 0,u,v.
    u,v=primitive(u),primitive(v);need(cross(u,v)>0,'ordered positive angle')
    pts=[]
    for x in range(min(0,u[0],v[0]),max(0,u[0],v[0])+1):
        for y in range(min(0,u[1],v[1]),max(0,u[1],v[1])+1):
            p=(x,y)
            if p!=(0,0) and cross(u,p)>=0 and cross(p,v)>=0 and cross(minus(v,u),minus(p,u))>=0:pts.append(p)
    h=hull(pts);need(u in h and v in h,'ray endpoint not extreme')
    if len(h)==2:sail=[u,v]
    else:
        sail=[u];i=h.index(u)
        for _ in range(len(h)):
            i=(i-1)%len(h);sail.append(h[i])
            if h[i]==v:break
        need(sail[-1]==v,'sail endpoint absent')
    for p,q in zip(sail,sail[1:]):need(cross(minus(q,p),(-p[0],-p[1]))>0,'origin support side')
    out=[]
    for i,(p,q) in enumerate(zip(sail,sail[1:])):
        if i:
            a=primitive(minus(sail[i-1],p));b=primitive(minus(q,p));out.append(abs(cross(a,b)))
        out.append(math.gcd(*minus(q,p)))
    need(all(x>0 for x in out) and len(out)%2==1,'sail data')
    return out

def unit_interior(e):
    bound=max(abs(e[0]),abs(e[1]),1)
    for x in range(-bound,bound+1):
        for y in range(-bound,bound+1):
            if cross(e,(x,y))==-1:return (x,y)
    raise ValueError('unit interior point missing')

def threshold(predicate):
    # Exact monotone integer search, without the producer's floor quotient formula.
    lo,hi=-1,1
    while predicate(lo):lo*=2
    while not predicate(hi):hi*=2
    while hi-lo>1:
        m=(hi+lo)//2
        if predicate(m):hi=m
        else:lo=m
    return hi

def independent_chord(a,b,c,d):
    e=primitive(minus(c,b));w=unit_interior(e)
    need(cross(minus(a,b),e)>0 and cross(minus(d,c),e)>0,'local clockwise sides')
    t=threshold(lambda t:cross(minus(a,b),(w[0]+t*e[0],w[1]+t*e[1]))>=0)
    z=-threshold(lambda t:cross(minus(d,c),(w[0]-t*e[0],w[1]-t*e[1]))<=0)
    L=math.gcd(*minus(c,b));displacement=L+z-t
    return L-displacement-2,displacement

def independent_polygon(points):
    n=len(points);blocks=[];curves=[];displacements=[]
    need(n>=3,'short polygon')
    for i in range(n):
        a,b,c,d=[points[j%n] for j in (i-1,i,i+1,i+2)]
        blocks.append(brute_sail(minus(a,b),minus(c,b)))
        curve,displacement=independent_chord(a,b,c,d)
        curves.append(curve);displacements.append(displacement)
    return blocks,curves,displacements

def frame_vertices(blocks,cs):
    result=[(1,0)]
    for i in range(1,len(blocks)+1):
        word=word_for(blocks[:i],cs)
        result.append((matrix_K(word[1:]),matrix_K(word)))
    return result

def rational_polygon(blocks,cs):
    B=frame_vertices(blocks,cs);n=len(blocks)
    need(B[-1]==((-1)**n,0),'closed endpoint parity')
    e=[(((-1)**i)*B[i+1][0],((-1)**i)*B[i+1][1]) for i in range(n)]
    need(all(cross(e[i-1],e[i])<0 for i in range(n)),'strict clockwise direction turns')
    # Tangential real polygon has supports ||normal||. Approximate them rationally.
    normals=[(-p[1],p[0]) for p in e]
    for power in range(0,80):
        Q=1<<power
        supports=[Fraction(math.isqrt(dot(p,p)*Q*Q),Q) for p in normals]
        pts=[]
        for i in range(n):
            a,b=normals[i-1],normals[i];D=cross(a,b)
            pts.append(((supports[i-1]*b[1]-a[1]*supports[i])/D,(a[0]*supports[i]-supports[i-1]*b[0])/D))
        if all(dot(normals[i],pts[j])<supports[i] for i in range(n) for j in range(n) if j not in (i,(i+1)%n)):
            scale=math.lcm(*(v.denominator for p in pts for v in p))
            return [(int(x*scale),int(y*scale)) for x,y in pts],power
    raise ValueError('finite test construction cap reached')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--checker',required=True,type=pathlib.Path);args=ap.parse_args()
    need(hashlib.sha256(args.checker.read_bytes()).hexdigest()==PIN,'producer checker pin mismatch')
    spec=importlib.util.spec_from_file_location('producer',args.checker);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    counts={};words=0
    for length in range(8):
        for word in itertools.product(range(-2,3),repeat=length):
            expected=matching_K(word)
            need(p.continuant(word)==expected,'continuant/path-matching mismatch');words+=1
    counts['independent_path_matching_words']=words
    grid=list(itertools.product(range(4),repeat=2));polygons=set()
    for size in range(3,len(grid)+1):
        for subset in itertools.combinations(grid,size):
            H=hull(subset)
            if len(H)>=3:polygons.add(tuple(reversed(H)))
    signs=set();zero_prefix=0;cyclic=0;transforms=0;witnesses=[]
    for polygon in sorted(polygons):
        blocks,cs,displacements=independent_polygon(polygon)
        need(p.polygon_data(polygon)==(blocks,cs),'independent sail/chord data disagreement')
        got=p.evaluate(blocks,cs);other=criterion(blocks,cs)
        need(got['criterion'] and other[0] and got['prefix_continuants']==other[1],'geometric necessity failed')
        signs.update((x>0)-(x<0) for x in displacements)
        zero_prefix+=int(0 in other[1][:-1])
        for i in range(len(blocks)):
            need(p.evaluate(blocks[i:]+blocks[:i],cs[i:]+cs[:i])['criterion'],'cyclic rotation failure');cyclic+=1
        for a,b,c,d in [(0,1,-1,0),(1,3,0,1),(-1,0,0,1),(1,0,0,-1)]:
            transformed=[(a*x+b*y+7,c*x+d*y-4) for x,y in polygon]
            if a*d-b*c<0:
                transformed=list(reversed(transformed))
                expected_b=[list(reversed(z)) for z in reversed(blocks)]
                expected_c=cs[-2::-1]+cs[-1:]
            else:expected_b,expected_c=blocks,cs
            need(p.polygon_data(transformed)==(expected_b,expected_c),'GL2/reflection block-index convention');transforms+=1
        if len(witnesses)<100:witnesses.append((blocks,cs))
    counts.update(exhaustive_grid_polygons=len(polygons),cyclic_checks=cyclic,GL2_checks=transforms,polygons_with_internal_zero_prefix=zero_prefix,chord_displacement_signs=sorted(signs))
    # Systematically test integer curvature witnesses, including zero and positive entries.
    attempts=0;accepted=0;nonconvex=0;unusual=0;constructed=0;max_power=0;seen=set()
    alphabet=[[1],[2],[1,1,1]]
    for n in (3,4,5):
        bwords=itertools.product(alphabet,repeat=n) if n<5 else [([1],)*5]
        for blocktuple in bwords:
            blocks=[list(x) for x in blocktuple]
            for prefix in itertools.product(range(-5,3),repeat=n-1):
                cs=list(prefix)+[0];test=criterion(blocks,cs);attempts+=1
                if test[1][-1]!=0:continue
                need(test[2]!=0,'closing denominator vanished')
                M=matrix_product(word_for(blocks,cs));epsilon=M[0][1]
                need(epsilon==M[1][0] and abs(epsilon)==1,'closed primitive frame')
                cs[-1]=-epsilon*M[1][1]
                need(cs[-1]==-math.floor(Fraction(test[3],test[2])),'floor/monodromy disagreement')
                need(matrix_product(word_for(blocks,cs)+[cs[-1]])==((epsilon,0),(0,epsilon)),'full scalar monodromy')
                got=p.evaluate(blocks,cs)
                expected=criterion(blocks,cs);need(got['criterion']==expected[0],'independent criterion mismatch')
                if not got['criterion']:nonconvex+=1;continue
                accepted+=1
                if max(cs)>=0:unusual+=1
                key=(n,max(cs)>=0,tuple(len(z) for z in blocks),tuple((x>0)-(x<0) for x in cs))
                if key in seen:continue
                seen.add(key);witnesses.append((blocks,cs))
    for blocks,cs in witnesses:
        pts,power=rational_polygon(blocks,cs);max_power=max(max_power,power)
        need(p.polygon_data(pts)==(blocks,cs),'constructive sufficient witness not recovered');constructed+=1
    counts.update(curvature_candidates=attempts,accepted_curvature_witnesses=accepted,closed_wrong_winding_witnesses=nonconvex,accepted_zero_or_positive_curvature=unusual,constructed_integer_polygons=constructed,max_support_refinement_power=max_power)
    malformed=[(None,[]),([],[]),([[1]]*2,[0]*2),([[1]]*129,[0]*129),([[1]]*3,None),([[1]]*3,(0,0,0)),([[1]]*3,[0]*2),([[1]]*3,[0]*4),([[1],[1],[]],[0]*3),([[1],[1],[1,1]],[0]*3)]
    for value in [False,True,1.0,None,'1',0,-1,10**12+1]:malformed.append(([[1],[1],[value]],[0]*3))
    for value in [False,True,0.0,None,'0',10**12+1,-10**12-1]:malformed.append(([[1]]*3,[0,0,value]))
    malformed.append(([[1],[1],[1]*4097],[0]*3))
    for blocks,cs in malformed:
        try:p.evaluate(blocks,cs)
        except (TypeError,ValueError):pass
        else:raise ValueError('malformed input accepted')
    count_json=0
    for data in ['{"a":1,"a":2}','{"outer":{"a":1,"a":2}}','NaN','Infinity','-Infinity','[1,]','{','{"a":}','\xff']:
        try:p.loads(data)
        except (ValueError,TypeError):pass
        else:raise ValueError('malformed JSON accepted')
        count_json+=1
    for pts in [[(0,0),(1,0),(2,0)],[(0,0),(1,1),(0,1),(1,0)],[(0,0),(0,1),(1,0),(0,0)],[(0,0),(1,0),(0,1)]]:
        try:p.polygon_data(pts)
        except ValueError:pass
        else:raise ValueError('malformed polygon accepted')
    tb,tc=p.polygon_data([(0,0),(0,1),(1,0)]);twice=p.evaluate(tb*2,tc*2)
    need(twice['closure'] and twice['last_curvature'] and not twice['winding'],'winding sentinel')
    local_examples=[((0,-1),(0,0),(3,0),(3,-1)),((0,-1),(0,0),(1,0),(0,-1)),((1,-2),(0,0),(1,0),(0,-2))]
    displacements=[independent_chord(*q)[1] for q in local_examples]
    need(displacements==[3,0,-1],'signed/degenerate local chord controls')
    counts['local_chord_displacements']=displacements
    counts.update(malformed_angle_inputs=len(malformed),malformed_JSON=count_json,malformed_polygons=4,wrong_winding_rejected=True)
    print(json.dumps({'accepted':True,'optimize':sys.flags.optimize,'checker_sha256':PIN,'counts':counts,'limit':'Independent finite arithmetic and constructive controls; not formal verification or a total angles-only decision procedure.'},sort_keys=True))
if __name__=='__main__':main()
