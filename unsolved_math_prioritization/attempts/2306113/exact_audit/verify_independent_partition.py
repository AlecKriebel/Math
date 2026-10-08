#!/usr/bin/env python3
"""Exact geometric checker for independently reconstructed dyadic disk leaves."""
from fractions import Fraction as Q
import json,sys,pathlib,copy
class Rejected(ValueError):pass
def need(ok,why):
 if not ok:raise Rejected(why)
def verify(leaves):
 gamma=Q(1000000,1002001);roots={s:{} for s in (1,-1)}
 for leaf in leaves:
  sign=leaf['sign'];path=leaf['path'];need(sign in roots,'sign');need(type(path) is str and len(path)<=40 and set(path)<=set('01'),'path')
  node=roots[sign]
  for bit in path:
   need('leaf' not in node,'prefix overlap');node=node.setdefault(bit,{})
  need(not node,'duplicate leaf or prefix overlap');node['leaf']=leaf
  need(Q(leaf['bound'])<gamma,'leaf bound not strict')
 def region(node):
  if 'leaf' in node:
   need(set(node)=={'leaf'},'leaf/internal overlap');a,b,c,d=map(Q,node['leaf']['rectangle']);need(0<=a<b<=1 and -1<=c<d<=1,'rectangle range');return (a,b,c,d)
  need(set(node)=={'0','1'},'missing coverage child')
  a,b,c,d=region(node['0']);e,f,g,h=region(node['1'])
  radial=(b==e and c==g and d==h and b==(a+f)/2)
  angular=(a==e and b==f and d==g and d==(c+h)/2)
  need(radial != angular,'children fail exact midpoint partition')
  return (a,f,c,d) if radial else (a,b,c,h)
 for s in (1,-1):need(region(roots[s])==(Q(0),Q(1),Q(-1),Q(1)),'incomplete root rectangle')
 return {'status':'PASS','leaves':len(leaves),'two_complete_midpoint_partition_trees':True,'all_leaf_bounds_strict':True}
if __name__=='__main__':
 leaves=json.loads(pathlib.Path(sys.argv[1]).read_text());result=verify(leaves);controls=[]
 for label,change in [('missing_leaf',lambda ls:ls.pop()),('duplicate_leaf',lambda ls:ls.append(copy.deepcopy(ls[0]))),('non_strict_bound',lambda ls:ls[0].update(bound='1000000/1002001')),('rectangle_gap',lambda ls:ls[0]['rectangle'].__setitem__(1,str((Q(ls[0]['rectangle'][0])+Q(ls[0]['rectangle'][1]))/2)))]:
  altered=copy.deepcopy(leaves);change(altered)
  try:verify(altered)
  except Rejected as e:controls.append({'case':label,'status':'REJECT','reason':str(e)})
  else:raise RuntimeError('bad certificate accepted: '+label)
 result['negative_controls']=controls;print(json.dumps(result,indent=2))
