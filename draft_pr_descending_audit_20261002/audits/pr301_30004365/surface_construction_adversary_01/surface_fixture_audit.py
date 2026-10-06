#!/usr/bin/env python3
"""Independent exact lozenge quotient and vertex-link audit; no winding emulator."""
from collections import Counter, defaultdict
from itertools import combinations_with_replacement, product
import hashlib, json, pathlib

class UF:
    def __init__(self, xs): self.p = {x:x for x in xs}
    def find(self,x):
        while x != self.p[x]:
            self.p[x] = self.p[self.p[x]]; x=self.p[x]
        return x
    def union(self,a,b): self.p[self.find(a)] = self.find(b)

# Polygon is oriented G,S,R,T counterclockwise, with sides GS,SR,RT,TG.
SIDES = ((0,1),(1,2),(2,3),(3,0))
def quotient(arrows, gluings, require_alternating=True, original_n=None):
    m=len(arrows); cs=[(a,k) for a in range(m) for k in range(4)]
    ss=[(a,k) for a in range(m) for k in range(4)]
    corners=UF(cs); edges=UF(ss)
    germs=UF([(a,e,k) for a,e in ss for k in SIDES[e]])
    glued=set()
    for (a,e),(b,f) in gluings:
        assert (a,e) not in glued and (b,f) not in glued and (a,e)!=(b,f)
        glued.update(((a,e),(b,f))); edges.union((a,e),(b,f))
        # Colored endpoints match colored endpoints; polygon orientation reverses.
        for k,l in zip(SIDES[e],reversed(SIDES[f])):
            assert (k in (0,2)) == (l in (0,2))
            corners.union((a,k),(b,l)); germs.union((a,e,k),(b,f,l))
    links=defaultdict(list)
    for a,k in cs:
        incident=[e for e,pair in enumerate(SIDES) if k in pair]
        links[corners.find((a,k))].append(tuple(germs.find((a,e,k)) for e in incident))
    interior=[]; boundary=[]
    for v, es in links.items():
        degrees=Counter(x for pair in es for x in pair)
        adjacency=defaultdict(set)
        for x,y in es: adjacency[x].add(y); adjacency[y].add(x)
        reached=set(); todo=[next(iter(degrees))]
        while todo:
            x=todo.pop()
            if x in reached: continue
            reached.add(x); todo.extend(adjacency[x]-reached)
        assert reached == set(degrees), ('disconnected link',v)
        ends=sum(d==1 for d in degrees.values())
        assert all(d in (1,2) for d in degrees.values()) and ends in (0,2), ('bad link',v,degrees)
        (boundary if ends==2 else interior).append(v)
    bedges=[s for s in ss if s not in glued]
    badj=defaultdict(set)
    for a,e in bedges:
        k,l=SIDES[e]; x,y=corners.find((a,k)),corners.find((a,l))
        badj[x].add(y);badj[y].add(x)
    seen=set(); bc=[]
    for x in badj:
        if x in seen: continue
        todo=[x]; comp=[]
        while todo:
            v=todo.pop()
            if v in seen:continue
            seen.add(v);comp.append(v);todo.extend(badj[v]-seen)
        bc.append(comp)
    faceadj=defaultdict(set)
    for (a,e),(b,f) in gluings:faceadj[a].add(b);faceadj[b].add(a)
    seen=set(); comps=[]
    for a in range(m):
        if a in seen:continue
        todo=[a]; faces=[]
        while todo:
            v=todo.pop()
            if v in seen:continue
            seen.add(v);faces.append(v);todo.extend(faceadj[v]-seen)
        vs={corners.find((a,k)) for a in faces for k in range(4)}
        es={edges.find((a,k)) for a in faces for k in range(4)}
        boundaries=[c for c in bc if set(c)<=vs]
        chi=len(vs)-len(es)+len(faces)
        b=len(boundaries); genus=(2-b-chi)//2
        assert 2-b-chi >=0 and (2-b-chi)%2==0
        color=lambda k, domain:len({corners.find((a,k)) for a in faces if corners.find((a,k)) in domain})
        marks=[{'white':sum(v in {corners.find((a,0)) for a in faces} for v in c),
                'black':sum(v in {corners.find((a,2)) for a in faces} for v in c)} for c in boundaries]
        if require_alternating:
            assert all(c['white']==c['black'] and c['white']>0 for c in marks)
        comps.append({'faces':len(faces),'vertices':len(vs),'edges':len(es),'chi':chi,'b':b,'g':genus,
          'white_boundary':color(0,boundary),'black_boundary':color(2,boundary),
          'white_interior':color(0,interior),'black_interior':color(2,interior),'boundary_marks':marks})
        if original_n is not None:
            # Each red half-edge through an original quiver vertex is one dual-arc end.
            ends={(edges.find((a,e)),corners.find((a,2))) for a in faces for e in (1,2)
                  if arrows[a][0 if e==1 else 1] < original_n}
            degree=Counter(v for e,v in ends)
            white={corners.find((a,0)) for a in faces}
            black={corners.find((a,2)) for a in faces}
            # Clockwise outer collars have one + sector per white mark, all other
            # sectors have - sign. Puncture collars have all negative sectors.
            records=[{'n':sum(v in white for v in c),'dual_ends':sum(degree[v] for v in c if v in black),
                      'w':2*sum(v in white for v in c)-sum(degree[v] for v in c if v in black)} for c in boundaries]
            punctures=[{'n':0,'dual_ends':degree[v],'w':-degree[v]} for v in sorted(black & set(interior))]
            comps[-1]['boundary_collar_records']=records
            comps[-1]['puncture_collar_records']=punctures
            assert sum(c['w'] for c in records+punctures)==4-2*(b+len(punctures))-4*genus
    return comps

def local_extensions(n,arrows,rels):
    result=[]
    for v in range(n):
        inc=[a for a,(s,t) in enumerate(arrows) if t==v]
        out=[a for a,(s,t) in enumerate(arrows) if s==v]
        good=[]
        for p in ((0,1),(1,0)):
            if all(((a,b) in rels)==(p[i]==j) for i,a in enumerate(inc) for j,b in enumerate(out)):
                good.append(p)
        if not good:return None
        result.append(good)
    return result

def finite(arrows,rels):
    permitted={a:[b for b in range(len(arrows)) if arrows[a][1]==arrows[b][0] and (a,b) not in rels] for a in range(len(arrows))}
    for a in permitted:
        reached=set();x=a
        while permitted[x]:
            if x in reached:return False
            reached.add(x);x=permitted[x][0]
    return True

def build(n,orig,rels,choices):
    arrows=list(orig); N=n
    incoming=[];outgoing=[]
    for v in range(n):
        inc=[a for a,(s,t) in enumerate(arrows) if t==v]
        out=[a for a,(s,t) in enumerate(arrows) if s==v]
        while len(inc)<2:inc.append(len(arrows));arrows.append((N,v));N+=1
        while len(out)<2:out.append(len(arrows));arrows.append((v,N));N+=1
        incoming.append(inc);outgoing.append(out)
    gluings=[]; green=[]
    for v,p in enumerate(choices):
        for i,a in enumerate(incoming[v]):
            for j,b in enumerate(outgoing[v]):
                if p[i]==j:pair=((a,2),(b,1))
                else:pair=((a,3),(b,0));green.append(pair)
                gluings.append(pair)
    surface=quotient(arrows,gluings,original_n=n)
    dual_cut=quotient(arrows,green,require_alternating=False)
    assert all(c['g']==0 and c['b']==1 and c['chi']==1 and c['white_boundary']==1 and c['white_interior']==0 for c in dual_cut)
    assert all(c['white_interior']==0 for c in surface)
    return {'surface':surface,'dual_cut_polygons':len(dual_cut),
      'arrows_completed':arrows,'side_pairings':gluings}

def audit(n,arrows,rels):
    extensions=local_extensions(n,arrows,rels)
    assert extensions is not None and finite(arrows,rels)
    runs=[build(n,arrows,rels,p) for p in product(*extensions)]
    keys=[json.dumps(sorted(r['surface'],key=lambda c:json.dumps(c,sort_keys=True)),sort_keys=True) for r in runs]
    assert len(set(keys))==1,('completion changes topological/color data',arrows,rels)
    return {'n':n,'arrows':arrows,'relations':sorted(rels),'completion_choices':len(runs),'certificate':runs[0]}

def all_small():
    count=0; choices=0; genera=Counter(); examples={}
    for n in (1,2):
        ends=list(product(range(n),repeat=2))
        for m in range(2*n+1):
            for arrows in combinations_with_replacement(ends,m):
                if any(sum(s==v for s,t in arrows)>2 or sum(t==v for s,t in arrows)>2 for v in range(n)):continue
                composable=[(a,b) for a in range(m) for b in range(m) if arrows[a][1]==arrows[b][0]]
                for mask in range(1<<len(composable)):
                    rels={ab for bit,ab in enumerate(composable) if mask>>bit&1}
                    if local_extensions(n,arrows,rels) is None or not finite(arrows,rels):continue
                    r=audit(n,arrows,rels);count+=1;choices+=r['completion_choices']
                    for c in r['certificate']['surface']:
                        genera[c['g']]+=1
                        examples.setdefault(str((c['g'],c['b'],c['black_interior'])),r)
    return {'valid_finite_labeled_inputs':count,'completion_runs':choices,'component_genera':dict(genera),'topological_examples':examples}

if __name__=='__main__':
    fixtures={
      'isolated_field':(1,[],set()),
      'two_isolated_fields':(2,[],set()),
      'square_zero_loop':(1,[(0,0)],{(0,0)}),
      'full_relation_three_cycle':(3,[(0,1),(1,2),(2,0)],{(0,1),(1,2),(2,0)}),
      'genus_one_two_vertices':(2,[(0,1),(0,1),(1,0)],{(0,2),(2,1)}),
      'fork':(3,[(0,1),(0,2)],set()),
      'ordinary_A2':(2,[(0,1)],set())}
    out={'scope':'Exact quotient topology, links, colors, matching choices and disk dual polygons; no complete invariant or full production implementation.',
      'fixtures':{name:audit(*q) for name,q in fixtures.items()},'exhaustive_small':all_small()}
    pathlib.Path('surface_fixture_results.json').write_text(json.dumps(out,indent=2)+'\n')
    summary={'fixtures':{k:{'surface':v['certificate']['surface'],'dual_cut_polygons':v['certificate']['dual_cut_polygons'],'completion_choices':v['completion_choices']} for k,v in out['fixtures'].items()},
      'small':{k:v for k,v in out['exhaustive_small'].items() if k!='topological_examples'}}
    print(json.dumps(summary,indent=2))
