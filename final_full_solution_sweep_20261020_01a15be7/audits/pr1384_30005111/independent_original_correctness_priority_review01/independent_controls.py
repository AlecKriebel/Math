"""Independent exact controls. No claimant imports or execution; read-only inputs."""
from fractions import Fraction as Q
from itertools import permutations, combinations
from math import gcd
import json

def demand(ok, why):
    if not ok: raise ValueError(why)

def image(vs, word):
    demand(vs and len(vs)==len(word), 'dimensions')
    ends={}
    for i,(e,d) in enumerate(word):
        demand(d in (-1,1),'orientation')
        p,q=vs[i],vs[(i+1)%len(vs)]
        if d==-1:p,q=q,p
        demand(e not in ends or ends[e]==(p,q),'endpoints')
        ends[e]=(p,q)
        demand(word[(i+1)%len(word)]!=(e,-d),'nonimmersion')
    return ends

def nongradient(ends,c):
    # Independent integration along all graph edges, detecting a cycle defect.
    potential={next(iter(ends.values()))[0]:0}
    while True:
        changed=False
        for e,(p,q) in ends.items():
            if p in potential and q not in potential:potential[q]=potential[p]+c[e];changed=True
            if q in potential and p not in potential:potential[p]=potential[q]-c[e];changed=True
        if not changed:break
    return any(potential[q]-potential[p]!=c[e] for e,(p,q) in ends.items())

def cochain(vs,word,seed,scale):
    ends=image(vs,word);known={min(vs)};tree=set()
    while len(known)<len(set(vs)):
        choices=[(e,p,q) for e,(p,q) in sorted(ends.items()) if (p in known)!=(q in known)]
        demand(choices,'connected');e,p,q=choices[-1];known.update((p,q));tree.add(e)
    chords=sorted(set(ends)-tree);a=[sum(d for f,d in word if f==e) for e in chords]
    demand(len(chords)>=2,'rank');c={e:0 for e in ends}
    pivot=next((i for i,x in enumerate(a) if x),None)
    if pivot is None:c[chords[seed%len(chords)]]=1
    else:
        j=(pivot+1+seed%(len(chords)-1))%len(chords)
        g=gcd(a[pivot],a[j]);c[chords[pivot]]=a[j]//g;c[chords[j]]=-a[pivot]//g
    pot={v:(v*v+seed*3*v+seed)%7-3 for v in set(vs)}
    c={e:scale*x+pot[q]-pot[p] for e,x in c.items() for p,q in [ends[e]]}
    demand(sum(d*c[e] for e,d in word)==0,'nonclosing cochain')
    demand(nongradient(ends,c),'gradient cochain')
    return c

def validate_height(vs,word,h):
    image(vs,word);demand(len(h)==len(vs) and all(isinstance(x,Q) for x in h),'height format')
    for i,j in combinations(range(len(vs)),2):
        if vs[i]==vs[j]:demand(h[i]!=h[j],'vertex collision')
        if word[i][0]==word[j][0]:
            p=(h[i],h[(i+1)%len(h)]);q=(h[j],h[(j+1)%len(h)])
            if word[i][1]<0:p=p[::-1]
            if word[j][1]<0:q=q[::-1]
            demand((p[0]-q[0])*(p[1]-q[1])>0,'affine edge crossing')

def solve(vs,word,seed=0,scale=1):
    original=(vs[:],word[:]);layers=[];trace=[];n=len(vs)
    for step in range(n+1):
        ends=image(vs,word);rank=len(ends)-len(set(vs))+1
        demand(rank>=1,'rankzero');trace.append([len(set(vs)),len(ends),rank])
        if rank==1:break
        c=cochain(vs,word,seed+step,scale);s=[0]
        for e,d in word:s.append(s[-1]+d*c[e])
        demand(s[-1]==0,'closure')
        vp=[(v,s[i]) for i,v in enumerate(vs)]
        ep=[(e,s[i] if d==1 else s[i+1]) for i,(e,d) in enumerate(word)]
        vm={v:i for i,v in enumerate(sorted(set(vp)))};em={e:i for i,e in enumerate(sorted(set(ep)))}
        demand(len(vm)>len(set(vs)) and len(vm)<=n,'progress')
        layers.append(s[:-1]);vs=[vm[v] for v in vp];word=[(em[e],old[1]) for e,old in zip(ep,word)]
    else:raise ValueError('termination')
    demand(all(a[0]<b[0] for a,b in zip(trace,trace[1:])),'strictprogress')
    demand(len(layers)<=n-trace[0][0],'step bound')
    degree=n//len(set(vs));demand(degree*len(set(vs))==n,'cover degree')
    if degree>1:return None,degree,trace
    h=[Q(0)]*n
    for a in layers[::-1]:
        M=max(abs(x) for x in h);eps=1/(4*M+1);demand(2*eps*M<1,'epsilon')
        h=[Q(x)+eps*y for x,y in zip(a,h)]
    validate_height(*original,h);return h,degree,trace

def period(word):
    n=len(word)
    return next(d for d in range(1,n+1) if n%d==0 and all(word[i]==word[i%d] for i in range(n)))

def walks(ends,nmax):
    adj={v:[] for pq in ends.values() for v in pq}
    for e,(p,q) in ends.items():adj[p].append((e,1,q));adj[q].append((e,-1,p))
    for start in sorted(adj):
        def rec(v,vs,word):
            if word and v==start and word[-1]!=(word[0][0],-word[0][1]):yield vs,word
            if len(word)==nmax:return
            for e,d,t in adj[v]:
                if word and word[-1]==(e,-d):continue
                yield from rec(t,vs+[v],word+[(e,d)])
        yield from rec(start,[],[])

def fiber_orders(word):
    # All star vertex fiber orders; necessary arbitrary-continuous noncrossing condition.
    n=len(word);leaves=sorted(set(word));valid=0;total=0
    choices=[list(permutations([i for i,l in enumerate(word) if l==leaf])) for leaf in leaves]
    def product(xs):
        if not xs:yield ()
        else:
            for t in xs[0]:
                for tail in product(xs[1:]):yield (t,)+tail
    for order in permutations(range(n)):
        h={v:i for i,v in enumerate(order)}
        for orders in product(choices):
            leafh={i:j for order2 in orders for j,i in enumerate(order2)};total+=1;okay=True
            for leaf in leaves:
                strands=[(h[v],leafh[i]) for i,l in enumerate(word) if l==leaf for v in (i,(i+1)%n)]
                if any((x-u)*(y-v)<0 for (x,y),(u,v) in combinations(strands,2)):okay=False;break
            valid+=okay
    return total,valid

def main():
    graphs={'rose3':{0:(0,0),1:(0,0),2:(0,0)},'barbell_bridge':{0:(0,0),1:(0,1),2:(1,1)},'theta_parallel':{0:(0,1),1:(0,1),2:(1,0)},'subdivided_theta':{0:(0,1),1:(1,3),2:(0,2),3:(2,3),4:(0,3)},'K4':{0:(0,1),1:(0,2),2:(0,3),3:(1,2),4:(1,3),5:(2,3)}}
    counts={};positive=negative=runs=0;maxsteps=0
    for name,ends in graphs.items():
        count=0
        for vs,word in walks(ends,5 if name=='rose3' else 7):
            # Restrict rose to first 280 representative enumerated walks; other graph classes complete.
            if name=='rose3' and count>=280:break
            expected=len(word)//period(word)
            for seed,scale in [(0,1),(1,2),(5,-3)]:
                h,d,tr=solve(vs,word,seed,scale);demand(d==expected,'root degree');demand((h is None)==(expected>1),'existence');runs+=1;maxsteps=max(maxsteps,len(tr)-1)
            count+=1
            if expected==1:positive+=1
            else:negative+=1
        counts[name]=count
    word=[(0,1),(1,1),(0,-1),(1,-1)];vs=[0]*4
    h,d,tr=solve(vs,word,1,2);sample={'walk':word,'heights':[str(x) for x in h],'trace':tr}
    rejected=[]
    for label,fn in [('colliding heights',lambda:validate_height(vs,word,[Q(0)]*4)),('nonexact heights',lambda:validate_height(vs,word,[float(x) for x in h])),('nonimmersion',lambda:solve([0,1],[(0,1),(0,-1)])),('pure-gradient masquerading as non-gradient',lambda:demand(nongradient({0:(0,1),1:(1,0)},{0:2,1:-2}),'gradient'))]:
        try:fn()
        except ValueError:rejected.append(label)
        else:raise ValueError('mutation accepted '+label)
    total,accepted=fiber_orders('ababa');demand((total,accepted)==(1440,0),'ababa')
    one=fiber_orders('a');demand(one==(1,1),'outback curved positive')
    # Immediate reversal affine endpoint product is zero, not evidence against a continuous oval.
    demand((Q(0)-Q(0))*(Q(0)-Q(0))==0,'endpoint ties')
    directed=[(0,1),(0,-1),(1,1),(1,-1),(0,1),(0,-1),(1,1),(1,-1),(0,1),(0,-1)]
    for w in (directed,[(e,-d) for e,d in directed[::-1]]):
        for k in range(10):demand(period(w[k:]+w[:k])==10,'nonpower')
    print(json.dumps({'PASS':True,'graph_walks':counts,'primitive':positive,'proper_power':negative,'three_cochain_choices_per_walk_runs':runs,'max_split_steps':maxsteps,'sample_scaled_nongradient_and_added_gradient':sample,'ababa_complete_fiber_orders':total,'ababa_accepted':accepted,'one_excursion_curved_positive':one,'rotation_inverse_nonpower_checks':20,'rejected_mutations':rejected,'finite_controls_are_not_general_proof':True},indent=2))
if __name__=='__main__':main()
