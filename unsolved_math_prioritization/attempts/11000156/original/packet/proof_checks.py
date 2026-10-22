#!/usr/bin/env python3
"""Finite checks only. No theorem-proving or mapping-class-group oracle."""
import itertools
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def mm(a, b):
    return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2)) for i in range(2) for j in range(2))


def mpow(a, n):
    p = (1, 0, 0, 1)
    for _ in range(n):
        p = mm(p, a)
    return p


def check_matrices():
    a, b = (1, 1, 0, 1), (1, 0, -1, 1)
    z = mpow(mm(a, b), 3)
    require(mm(mm(a,b),a) == mm(mm(b,a),b), 'braid relation')
    require(z == (-1,0,0,-1), 'orientation-reversing block')
    require(mm(z,a) == mm(a,z), 'centrality')
    require(mpow(mm(a,b),6) == (1,0,0,1), 'boundary image')
    count = 0
    for p,q,r,s in itertools.product(range(-3,4), repeat=4):
        m = (p,q,r,s)
        if p*s-q*r != 1:
            continue
        commute = mm(m,a)==mm(a,m)
        require(commute == (r==0 and s==p and p in (-1,1)), 'centralizer formula')
        count += 1
    return {'sl2_integer_matrices_checked':count, 'block_image':list(z)}


def check_doubling():
    count = 0
    for m in range(3,31):
        for j in range(m+1):
            ks = (m-j,m+3*j,m-2*j)
            if not (1<=ks[0]<=m and 1<=ks[1]<=4*ks[0] and 1<=ks[2]<=4*ks[1]):
                continue
            data = [m]
            genus = 2*m+1
            g0 = genus
            blowups = 0
            for k in ks:
                require(1<=k<=data[0], 'doubling domain')
                blowups += data[0]-k
                data += [0]
                data = [4*k,0,data[0]+data[1]-k]+data[2:]
                while data and data[-1]==0:
                    data.pop()
                genus = 2*genus+k-1
            expected = [4*m-8*j,0,3*m+14*j,3*m-7*j,j]
            while expected[-1]==0:
                expected.pop()
            require(data==expected, 'exceptional recurrence')
            require(blowups+data[0]==10*m, 'common total blowups')
            require(genus==8*g0+7*m-7, 'common genus')
            count += 1
    require(sum((-1,3,-2))==0 and sum(x*y for x,y in zip((4,2,1),(-1,3,-2)))==0, 'kernel direction')
    return {'admissible_doubling_sequences_checked':count, 'scope':'arithmetic recurrence only; geometry cited'}


def omega(a,b):
    return (a[0]*b[1]+a[1]*b[0]+a[2]*b[3]+a[3]*b[2])%2


def transvection(a,x):
    return tuple((x[i]+omega(a,x)*a[i])%2 for i in range(4))


def quadratic(x,l):
    return (x[0]*x[1]+x[2]*x[3]+sum(i*j for i,j in zip(x,l)))%2


def check_quadratics():
    vectors = list(itertools.product((0,1),repeat=4))
    count = 0
    for a,l,x in itertools.product(vectors,vectors,vectors):
        lhs = quadratic(transvection(a,x),l)
        rhs = (quadratic(x,l)+omega(x,a)*(quadratic(a,l)+1))%2
        require(lhs==rhs, 'quadratic transformation formula')
        require(transvection(a,transvection(a,x))==x, 'transvection involution mod two')
        count += 1
    basis = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]
    a,v = (1,0,1,0),basis[1]
    before = [l for l in vectors if all(quadratic(x,l)==1 for x in basis+[v])]
    after = [l for l in vectors if all(quadratic(x,l)==1 for x in basis+[transvection(a,v)])]
    require(before==[(1,1,1,1)] and after==[], 'quadratic existence counterexample in quotient')
    return {'quadratic_identities_checked':count, 'before_refinements':len(before), 'after_refinements':len(after), 'scope':'Sp(4,F2) only; no mapping-class lift claimed'}


def check_finite_orbits():
    permutations = list(itertools.permutations(range(3)))
    identity = (0,1,2)
    def mul(a,b):
        return tuple(a[b[i]] for i in range(3))
    def inv(a):
        return tuple(a.index(i) for i in range(3))
    def prod(word):
        p=identity
        for a in word:
            p=mul(p,a)
        return p
    transpositions = [p for p in permutations if p!=identity and mul(p,p)==identity]
    words = {w for w in itertools.product(transpositions,repeat=6) if prod(w)==identity}
    require(len(words)==243, 'identity word count')
    edge_counts=[0,0]
    def neighbors(w,partial):
        for i in range(5):
            a,b=w[i:i+2]
            v=w[:i]+(b,mul(inv(b),mul(a,b)))+w[i+2:]
            require(v in words, 'Hurwitz edge product')
            edge_counts[0]+=1
            yield v
        if not partial:
            return
        for i in range(6):
            for j in range(i+1,7):
                block=prod(w[i:j])
                for t in transpositions:
                    if mul(t,block)==mul(block,t):
                        v=w[:i]+tuple(mul(t,mul(a,t)) for a in w[i:j])+w[j:]
                        require(v in words, 'partial conjugation product')
                        edge_counts[1]+=1
                        yield v
    def components(partial):
        remaining=set(words)
        sizes=[]
        while remaining:
            seed=min(remaining)
            remaining.remove(seed)
            seen={seed}
            stack=[seed]
            while stack:
                for v in neighbors(stack.pop(),partial):
                    if v not in seen:
                        seen.add(v)
                        stack.append(v)
                        remaining.discard(v)
            sizes.append(len(seen))
        return sorted(sizes)
    h=components(False)
    p=components(True)
    require(h==[1,1,1,240], 'Hurwitz component sizes')
    require(p==[243], 'partial conjugation orbit')
    s,t=transpositions[:2]
    u=mul(t,mul(s,t))
    require(u!=s, 'subgroup change')
    def closure(gens):
        out={identity}
        todo=[identity]
        while todo:
            z=todo.pop()
            for a in gens:
                v=mul(z,a)
                if v not in out:
                    out.add(v)
                    todo.append(v)
        return out
    require(len(closure([s]))==2 and len(closure([s,u]))==6,'generated subgroup change')
    return {'ambient_words':729,'identity_words':len(words),'hurwitz_components':h,'partial_components':p,'edges_checked':edge_counts,'scope':'S3 only; not a mapping-class orbit calculation'}


def main():
    return {'matrices':check_matrices(),'doubling':check_doubling(),'quadratics':check_quadratics(),'finite_orbits':check_finite_orbits(),'main_problem_resolved':False,'formal_certification':False}


if __name__=='__main__':
    print(json.dumps(main(),sort_keys=True))
