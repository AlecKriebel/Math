def zfun(s):
 n=len(s); z=[0]*n;l=r=0
 for i in range(1,n):
  if i<r:z[i]=min(r-i,z[i-l])
  while i+z[i]<n and s[z[i]]==s[i+z[i]]:z[i]+=1
  if i+z[i]>r:l,r=i,i+z[i]
 return z
t=''.join(str(i.bit_count()%2) for i in range(1<<20)); z=[i for i,c in enumerate(t) if c=='0']; w=''.join(str(b-a-1) for a,b in zip(z,z[1:]))[1:]
for prefix in ['21','02010','12010']:
 v=prefix+w[len(prefix):]; found=[]
 for a in range(len(prefix)):
  zz=zfun(v[a:]); found.extend((a,p) for p in range(1,len(zz)//2+1) if zz[p]>=p)
 print(prefix,len(v),found[:10],flush=True)
