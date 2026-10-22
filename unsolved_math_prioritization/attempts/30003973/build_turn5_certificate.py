from pathlib import Path
import itertools,json
p=Path(__file__).parent
H=[5,4,2,2,1];J=[5,4,3,2,1]
def components(edges):
    adj={}
    for u,v in edges:adj.setdefault(u,set()).add(v);adj.setdefault(v,set()).add(u)
    out=[];seen=set()
    for v in adj:
        if v in seen:continue
        todo=[v];vs=set()
        while todo:
            w=todo.pop()
            if w in vs:continue
            vs.add(w);todo+=list(adj[w]-vs)
        seen|=vs;ee=[e for e in edges if e[0] in vs]
        if len(vs)==3 and len(ee)==3:kind='triangle'
        else:
            assert any(len(adj[w])==len(ee) for w in vs);kind='star'
        out.append((kind,ee))
    return out

def threshold_data(edges,target):
    cc=components(edges);ds=[len(e) for k,e in cc if k=='star'];z=sum(k=='triangle' for k,e in cc)
    tau={t:sum(k>=t for k in target) for t in set(target)};rows=[]
    for u,v in itertools.combinations_with_replacement(sorted(tau),2):
        forced=sum(d>=u+v-1 for d in ds)+z*(u<=2 and v<=2);required=tau[u]+tau[v]-1
        rows.append({'u':u,'v':v,'forced':forced,'required':required})
    return rows

def avoiding(edges,target):
    cc=components(edges);rows=threshold_data(edges,target);row=next(r for r in rows if r['forced']<r['required']);u,v=row['u'],row['v'];quota=[sum(k>=u for k in target)-1,sum(k>=v for k in target)-1];colors={}
    for kind,ee in cc:
        force=len(ee)>=u+v-1 if kind=='star' else u<=2 and v<=2
        if force:
            c=0 if quota[0] else 1;assert quota[c];quota[c]-=1
            if kind=='triangle':allocation=[len(ee),0] if c==0 else [0,len(ee)]
            elif c==0:allocation=[len(ee)-min(len(ee),v-1),min(len(ee),v-1)]
            else:allocation=[min(len(ee),u-1),len(ee)-min(len(ee),u-1)]
        elif kind=='triangle':allocation=[3,0] if u>=3 else [0,3]
        else:allocation=[min(len(ee),u-1),len(ee)-min(len(ee),u-1)]
        for i,e in enumerate(ee):colors[tuple(e)]=0 if i<allocation[0] else 1
    return {'threshold':[u,v],'colors':[colors[tuple(e)] for e in edges]}

edges=[];comps=[];start=0
for d in [9,8,7,6,5,4,2,1]:
    idx=[]
    for leaf in range(start+1,start+d+1):idx.append(len(edges));edges.append([start,leaf])
    comps.append({'kind':'star','degree':d,'edge_indices':idx});start+=d+1
idx=[]
for u,v in itertools.combinations(range(start,start+3),2):idx.append(len(edges));edges.append([u,v])
comps.append({'kind':'triangle','edge_indices':idx});start+=3
colors=[None]*len(edges)
for i,c in enumerate(comps):
    color=1 if i in [2,3,4,5] else 0
    for e in c['edge_indices']:colors[e]=color
deletions=[]
for i in range(len(edges)):
    remain=edges[:i]+edges[i+1:];deletions.append({'deleted_edge_index':i,**avoiding(remain,H)})
c={'problem_id':30003973,'target_H_star_sizes':H,'target_Hprime_star_sizes':J,'vertices':start,'edges':edges,'components':comps,'H_threshold_table':threshold_data(edges,H),'Hprime_avoiding_colors':colors,'H_edge_deletion_avoiding_colorings':deletions,'scope':'A2-Ramsey-minimal host forH that avoidsHprime in2colors. This refutes the restricted-host equivalence candidate, not the original2-to3 implication.'}
(p/'TURN_5_CERTIFICATE.json').write_text(json.dumps(c,indent=2)+'\n')
