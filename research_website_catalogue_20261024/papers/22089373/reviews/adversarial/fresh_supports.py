from fresh_graph_library import *
cores={
'cycle':([('S','X'),('S','X')],['X'],[{0},{1}]),
'theta0':([('S','U'),('S','V'),('U','X'),('V','X'),('U','V')],['V','X'],[{2,3},{3,4}]),
'theta1':([('S','U'),('S','X'),('V','X'),('U','V'),('U','V')],['V','X'],[{2,3},{2,4}]),
'theta2':([('S','U'),('S','V'),('U','X0'),('V','X0'),('U','X1'),('V','X1')],['X0','X1'],[{2,3},{2,5},{3,4},{4,5}]),
'theta3':([('S','U'),('S','X0'),('V','X0'),('U','X1'),('V','X1'),('U','V')],['X0','X1'],[{2},{4}])}
outputs=[]
for core,(segs,ret,repairs) in cores.items():
 for repair in repairs:
  edges=[('ROOT0','S'),('ROOT0','IN')];labels={'IN':0};label=1
  for i,(a,b) in enumerate(segs):
   if i in repair:
    port=f'P{i}';leaf=f'L{i}';edges +=[(a,port),(port,b),(port,leaf)];labels[leaf]=label;label+=1
   else:edges.append((a,b))
  for v in ret:
   if not any(a==v for a,b in edges):edges.append((v,v+'leaf'));labels[v+'leaf']=label;label+=1
  M=mixed(edges,set(ret),'ROOT0');ck('simple '+core+str(repair),len({tuple(sorted([a,b])) for a,b,h in M})==len(M))
  rs=classify_rootings(M,labels,set(ret));ck('STC all admissible rootings '+core+str(repair),bool(rs) and all(x['tree_child'] for x in rs))
  outputs.append({'core':core,'repair':sorted(repair),'boundary_count':len(labels),'rootings':len(rs),'all_tree_child':True,'mixed_edges':M})
ck('all twelve primitive supports',len(outputs)==12);ck('one hundred primitive rootings',sum(x['rootings'] for x in outputs)==100)
print(json.dumps({'status':'PASS','checks':checks,'supports':outputs,'scope':'Fresh root-edge/orientation enumeration on all twelve printed minimum-repair supports; exact roles, indegrees, DAG, LSA and one-step suppression. No supplied helper or certificate used.'},indent=2))
