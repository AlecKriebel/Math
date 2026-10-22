"""Finite checks only. The accompanying argument proves the all-prime claim."""
from itertools import product

def ap_sets(p):
    return {tuple(sorted((a+i*d)%p for i in range(4)))
            for a in range(p) for d in range(1,p)}

def pair_link_components(p,A,B):
    vertices=set(range(p))-A-B
    adj={x:set() for x in vertices}
    for progression in ap_sets(p):
        for u in set(progression)&A:
            for v in set(progression)&B:
                x,y=set(progression)-{u,v}
                if x in vertices and y in vertices:
                    adj[x].add(y); adj[y].add(x)
    unseen=set(vertices); components=[]
    while unseen:
        component={unseen.pop()}; todo=list(component)
        while todo:
            for y in adj[todo.pop()]&unseen:
                unseen.remove(y); component.add(y); todo.append(y)
        components.append(sorted(component))
    return sorted(components,key=lambda c:(-len(c),c))

for p in [17,19,23,29,31,43]:
    domains={x:set(range(1,5)) for x in range(p)}
    domains.update({0:{1},1:{2},2:{3},p-1:{1,2,3},3:{1,2,3}})
    constraints=ap_sets(p)
    for edge in constraints:
        supports={x:set() for x in edge}
        for values in product(*(domains[x] for x in edge)):
            if len(set(values))<4:
                for x,c in zip(edge,values): supports[x].add(c)
        assert all(supports[x]==domains[x] for x in edge)
    print(f'p={p}: all {len(constraints)} individual 4AP constraints arc-consistent')
A={1,11,14,15,22}; B={0,3,4,5,8,17}
components=pair_link_components(23,A,B)
assert components==[[2,7,9,10,12,13,16,18,19,20,21],[6]]
print('p=23 pair-link components:',components)
