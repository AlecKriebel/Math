from pathlib import Path
from itertools import combinations
from collections import Counter
import ast,json,datetime
E=Path(__file__).resolve().parent;tree=ast.parse((E/'check_crossing_dag.py').read_text());ns={'I':tuple((i,) for i in range(1,7))};funcs=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ['need','step','action']];exec(compile(ast.Module(body=funcs,type_ignores=[]),'<owned_analytic_functions_only>','exec'),ns)
step,action,need,I=ns['step'],ns['action'],ns['need'],ns['I'];rows=[]
for i in range(1,6):
 expected=list(I);expected[i-1]=(i,i+1,-i);expected[i]=(i,);need(step(I,i)==tuple(expected),'literal_primary_inverse_generator_calibration');need(step(step(I,i),-i)==I==step(step(I,-i),i),'both_F6_inverse_compositions');rows.append({'generator':i,'images':step(I,i),'two_sided_inverse':True})
for i in range(1,5):need(action([i,i+1,i])==action([i+1,i,i+1]),'F6_braid')
for i,j in combinations(range(1,6),2):
 if j-i>1:need(action([i,j])==action([j,i]),'F6_distant')
words={'c':[1,2,3,4]*5,'h':[5,4,3,2,1,1,2,3,4,5],'z':[1,2,3,4,5]*6,'c_squared':[1,2,3,4]*10};link=[]
for name,w in words.items():
 p=list(range(6));C=Counter()
 for g in w:i=g-1;C[tuple(sorted((p[i],p[i+1])))]+=1;p[i],p[i+1]=p[i+1],p[i]
 need(p==list(range(6)) and all(v%2==0 for v in C.values()),'models_pure');link.append({'word':name,'exponent':len(w),'permutation':[v+1 for v in p],'linking':[[i+1,j+1,C[i,j]//2] for i,j in combinations(range(6),2)]})
(E/'RELATION_CALIBRATIONS.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','F6_primary_generator_images':rows,'F6_adjacent_braid_relations':4,'F6_distant_commutations':6,'convention':'SourceGMusesrho(sigma_i)=inverse ofTi; right-orderedU(w)=rho(w^-1) under usualleftcomposition. Inversionisbijective, sofaithfulnessdetectsequality.','model_linking':link,'provided_source_program_or_stream_loaded':False,'own_definitions_loaded_without_top_level_DAG_reexecution':True},indent=2)+'\n');print('PASS F6calibration, inverses, braid/commutations, four model linking vectors')
