from itertools import permutations,combinations
from pathlib import Path
import json
import twinwidth as t
from verify_small import verify

def main():
    adj=[0]*6;pairs=[(0,1),(2,3),(4,5)]
    for u,v in [(0,3),(1,3),(2,5),(3,5),(1,4),(1,5)]:adj[u]|=1<<v;adj[v]|=1<<u
    adj=tuple(adj);b,d,q=t.pair_profile(adj,pairs)
    assert b==[2,2,2]
    assert min(((adj[u]^adj[v])&~((1<<u)|(1<<v))).bit_count() for u,v in combinations(range(6),2))==2
    profiles=[]
    for order in permutations(range(3)):
        part=tuple(1<<i for i in range(6));ws=[]
        for z in order:
            x,y=pairs[z];part=t.merge(part,part.index(1<<x),part.index(1<<y));ws.append(t.width(adj,part))
        assert ws==[2,3,2]
        profiles.append({'order':order,'widths':ws})
    ex=t.exact(adj);alt=t.pair_only(adj,2)
    assert ex[0]==2 and verify(adj,ex[1],2)==2 and verify(adj,alt,2)==2
    out={'name':'triangle with one pendant leaf at each vertex (net graph)','adjacency':adj,'pairs':pairs,'base':b,'d':d,'q':q,'w':[[q[i][j]-d[i][j] for j in range(3)] for i in range(3)],'pair_orders':profiles,'exact':ex,'alternative_pair_sequence':alt}
    Path(__file__).with_name('cyclic_pair_obstruction.json').write_text(json.dumps(out,indent=2)+'\n')
    print('Verified six bad orders, exact lower bound 2, and two independent width-2 upper certificates.')
if __name__=='__main__':main()
