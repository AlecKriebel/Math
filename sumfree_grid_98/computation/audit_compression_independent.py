import json
out=[]
for d in range(1,5):
 q=1<<d
 def D(F):
  return {a|b for a in F for b in F if not a&b}
 for mask in range(1<<q):
  F={a for a in range(q) if mask>>a&1};old=D(F)
  for i in range(d):
   moved={a for a in F if not a>>i&1 and a|(1<<i) not in F}
   G=(F-moved)|{a|(1<<i) for a in moved}
   if len(G)!=len(F) or not D(G)<=old:raise ValueError((d,mask,i))
 out.append({'dimension':d,'families':1<<q,'coordinates_tested_per_family':d})
print(json.dumps(out,indent=2))
