"""Optional generator. Floating phases propose exact inputs; verify_exact.py certifies them."""
import json
from fractions import Fraction as F
from pathlib import Path
from exact_core import Q
n=32;m=n//2;u=Q(F(869,2000),-F(5777,10000));alpha=1-u
b=[Q(1)]
for j in range(1,n+1):b.append(b[-1]*(alpha+j-1)/j)
v={k:b[n-k]/k for k in range(m+1,n+1)}
W=b[n]+u*sum(v.values(),Q())
f=lambda z:complex(float(z.re),float(z.im))
L=sum(abs(f(vk)) for vk in v.values());s=[u]*m
for k in range(m+1,n):
    z=f(W)/L*f(v[k]).conjugate()/abs(f(v[k]))
    s.append(Q(F(round(z.real*10**10),10**10),F(round(z.imag*10**10),10**10)))
s.append((W-sum((s[k-1]*v[k] for k in range(m+1,n)),Q()))/v[n])
certificate={'format':'Gaussian-rational first-n-power-sum certificate v1','n':n,'radius':'29/40','construction':'two-block coefficient cancellation; no root approximation','sums':[z.record() for z in s]}
p=Path(__file__).with_name('CERTIFICATE.json');p.write_text(json.dumps(certificate,indent=2)+'\n')
print(p.name, max(float(z.norm2())**.5 for z in s))
