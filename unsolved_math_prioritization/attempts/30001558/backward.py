t=''.join(str(i.bit_count()%2) for i in range(16384))
z=[i for i,x in enumerate(t) if x=='0']; g=''.join(str(z[i+1]-z[i]-1) for i in range(len(z)-1)); w=g[1:]
def prep(a,s):
 s=a+s
 return all(s[:p]!=s[p:2*p] for p in range(1,len(s)//2+1))
print('g',g[:100]);print('w',w[:100])
for n in [2,5,8,12]:
 tail=w[n:n+512]; states=['']; counts=[]
 for k in range(n):
  states=[a+p for p in states for a in '012' if prep(a,p+tail)]
  counts.append(len(states))
  if len(states)>100000: break
 print(n,len(states),max(counts),states[:5] if len(states)<6 else '',flush=True)
