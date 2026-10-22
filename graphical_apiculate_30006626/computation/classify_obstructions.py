from atlas_apex import *
p=__file__.replace('classify_obstructions.py','atlas_apex_results.json');r=json.load(open(p));atlas=nx.graph_atlas_g();types={}
def signature(S,a):
    signatures=[]
    for p in itertools.permutations(S):
        inv={v:i for i,v in enumerate(p)}
        signatures.append(tuple(inv[a[x,y,z]] for x,y,z in itertools.product(p,repeat=3)))
    return min(signatures)
for f in r['failures']:
    a,_=apex_table(atlas[f['atlas_index']])
    for w in f['witnesses']:
        if len(w['subset'])!=4:continue
        sig=signature(w['subset'],a)
        if sig not in types:types[sig]={'first_atlas_index':f['atlas_index'],'subset':w['subset'],'canonical_edges':w['canonical_edges'],'failure':w['failure'],'occurrences':0,'signature':sig}
        types[sig]['occurrences']+=1
result={'four_point_obstruction_types':list(types.values()),'every_nongraphical_graph_has_four_point_obstruction':all(any(len(w['subset'])==4 for w in f['witnesses']) for f in r['failures'])}
with open(__file__.replace('classify_obstructions.py','four_point_obstructions.json'),'w') as out:json.dump(result,out,indent=2)
print(json.dumps(result,indent=2))
