from pathlib import Path
import sys,json,hashlib,networkx as nx
P=Path(__file__).resolve().parent
R=P.parents[1]/'sources/published-source/K2P_SAME_Reproducibility_Package_v1.0.5-r1/k2p_same_reproducibility_v1.0.5-r1'
sys.path.insert(0,str(R/'package/referee/k2p_offline_sweep_portable/atlas'))
import k2p_atlas_core as a
f=json.loads((P/'fresh_false_exclusion.json').read_text());src=a.source_supports()[2];tar=a.relabel_record((a.target_completions(4,True)+a.target_completions(4,False))[85],(2,0,1,3));out=[]
for n,rec in [('source',src),('target',tar)]:
 g=nx.DiGraph(f[n+'_arcs'])
 for v in g:g.nodes[v].update(label=int(v[1:]) if v.startswith('L') else None,role='leaf' if v.startswith('L') else 'root' if v=='r' else 'retic' if v in ['V','X'] else 'tree')
 match=nx.algorithms.isomorphism.DiGraphMatcher(g,rec.graph,node_match=lambda x,y:(x['role'],x['label'])==(y['role'],y['label']));assert match.is_isomorphic()
 out.append({'graph':n,'core':rec.core_id,'repair':rec.repair_index,'selected_labels':list(rec.selected_labels),'dummy_labels':list(rec.dummy_labels),'incoming_selected':rec.incoming_selected,'selected_sink_mask':rec.selected_sink_mask,'words':rec.words,'literal_to_published_rooted_graph_map':{v:str(w) for v,w in match.mapping.items()}})
(P/'literal_witness_binding.json').write_text(json.dumps({'atlas_sha256':hashlib.sha256(Path(a.__file__).read_bytes()).hexdigest(),'witness_sha256':hashlib.sha256((P/'fresh_false_exclusion.json').read_bytes()).hexdigest(),'rooted_graph_matches':out},indent=2)+'\n');print('Both literal witness graphs equal their exact released source/target presentations')
