def app(s,a):
 v=s+a
 return all(v[-2*p:-p]!=v[-p:] for p in range(1,len(v)//2+1))
words=['']
for L in range(1,33):
 words=[s+a for s in words for a in '012' if app(s,a)]
 if L in [24,26,28,30,32]:
  out=[]
  for n in [1,2,3,4,5,6]:
   if n>=L:continue
   buckets={}
   for s in words:buckets.setdefault(s[n:],[]).append(s[:n])
   unique=[k for k,v in buckets.items() if len(v)==1]
   out.append((n,len(unique)))
  print(L,len(words),out,flush=True)
