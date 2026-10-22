"""Independent offline payload closure and bounded mathematical controls.

Reads only this review's retained evidence; no source programs are executed.
Finite controls do not certify the continuous or infinite analytic theorems.
"""
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent
PRIVATE = HERE/'private_sources'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def payloads():
    counts = {}
    for pr in [104,1168]:
        record = json.loads((PRIVATE/f'pr{pr}_record.json').read_bytes())
        require(record['state']=='done' and record['submitted'] is True, 'Unpublished record')
        for item in record['files']:
            raw=(PRIVATE/(f'pr{pr}_'+item['key'])).read_bytes()
            require(len(raw)==item['size'] and 'md5:'+hashlib.md5(raw).hexdigest()==item['checksum'], 'Payload mismatch')
        counts[pr]=len(record['files'])
    with zipfile.ZipFile(PRIVATE/'pr104_AMR-005-0008-source.zip') as z:
        require(z.testzip() is None, '104CRC')
        manifest=json.loads(z.read('source-archive-manifest.json'))['files']
        regular={i.filename for i in z.infolist() if not i.is_dir()}
        require(regular==set(manifest)|{'source-archive-manifest.json'}, '104membership')
        for name,item in manifest.items():
            raw=z.read(name)
            require(len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'],'104member')
        require(z.read('README_submission.md')==(PRIVATE/'pr104_AMR-005-0008-readme.md').read_bytes(),'104README')
    prefix='AIM-COMBINATORICS-0098-v0.2.0/'
    archive=PRIVATE/'pr1168_symmetry-respecting-tree-torsors-0.2.0-candidate.zip'
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None,'1168CRC')
        source=z.read(prefix+'PAPER.md')
        require(len(source)==28223 and hashlib.sha256(source).hexdigest()=='43d033dafb5568ce4d01b54171c0ff9d8f4fd7740b1ac9164d21dc4256796645','1168acceptedsource')
        require(z.read(prefix+'paper.pdf')==(PRIVATE/'pr1168_symmetry-respecting-tree-torsors-0.2.0-candidate.pdf').read_bytes(),'1168PDF')
        manifest=json.loads(z.read(prefix+'MANIFEST.json'))['sha256']
        for name,digest in manifest.items():
            require(hashlib.sha256(z.read(prefix+name)).hexdigest()==digest,'1168member')
    with zipfile.ZipFile(PRIVATE/'pr1168_symmetry-respecting-tree-torsors-frozen-editorial-submission.zip') as z:
        require(z.testzip() is None,'editorialCRC')
        older=z.read(prefix+'PAPER.md')
        require(len(older)==26787 and hashlib.sha256(older).hexdigest()=='a95f49f960c7682201e4ca2a9ca57e3260502377df2731d75978ca80936d5db1' and older!=source,'editorialsource')
    for line in (PRIVATE/'pr1168_SHA256SUMS.txt').read_text().splitlines():
        digest,name=line.split(maxsplit=1)
        require(hashlib.sha256((PRIVATE/('pr1168_'+name)).read_bytes()).hexdigest()==digest,'1168outerSUM')
    return counts


def subgroups(order):
    return [tuple(i for i in range(order) if mask>>i&1) for mask in range(1<<order)
            if mask&1 and all(mask>>(i^j)&1 for i in range(order) for j in range(order)
                              if mask>>i&1 and mask>>j&1)]


def torsor_control(n, units, action):
    order=len(units); hs=subgroups(order); perms=list(itertools.permutations(range(n)))
    require(all(action[g^h][x]==action[g][action[h][x]] for g in range(order) for h in range(order) for x in range(n)), 'Invalid input action')
    classes=set()
    for tail in itertools.product(range(n),repeat=order-1):
        c=(0,)+tail
        if all(c[g^h]==(c[g]+units[g]*c[h])%n for g in range(order) for h in range(order)):
            classes.add(min(tuple((c[g]+units[g]*b-b)%n for g in range(order)) for b in range(n)))
    t={h:sum(all(action[g][x]==x for g in h) for x in range(n)) for h in hs}
    d={h:sum(all(units[g]*x%n==x for g in h) for x in range(n)) for h in hs}
    kernels={h:{c for c in classes if any(all(c[g]==(b-units[g]*b)%n for g in h) for b in range(n))} for h in hs}
    positive=[h for h in hs if t[h]>0];zero=[h for h in hs if t[h]==0]
    eligible=set(classes)
    for h in positive:eligible &= kernels[h]
    nu=0
    if all(t[h] in [0,d[h]] for h in hs):
        for mask in range(1<<len(zero)):
            common=set(eligible)
            for j,h in enumerate(zero):
                if mask>>j&1:common &= kernels[h]
            nu+=(-1)**mask.bit_count()*len(common)
    direct=0
    for f in perms:
        if f[0]!=0:continue
        inverse=[f.index(x) for x in range(n)]
        if all(action[g][f[(b+inverse[x])%n]]==f[(units[g]*b+inverse[action[g][x]])%n]
               for g in range(order) for b in range(n) for x in range(n)):
            direct+=1
    automorphisms=sum(all(f[action[g][x]]==action[g][f[x]] for g in range(order) for x in range(n)) for f in perms)
    fixed=sum(all(units[g]*x%n==x for g in range(order)) for x in range(n))
    require(F(nu*automorphisms,fixed)==direct,'Torsor criterion/action count differs from direct enumeration')
    return direct,all(t[h] in [0,d[h]] for h in hs)


def mathematical_controls():
    torsors=0;positive=0
    for n in range(1,6):
        identity=tuple(range(n))
        for u in range(n):
            if math.gcd(u,n)!=1 or u*u%n!=1%n:continue
            for perm in itertools.permutations(range(n)):
                if not all(perm[perm[x]]==x for x in range(n)):continue
                count,unused=torsor_control(n,[1%n,u],[identity,perm]);torsors+=1;positive+=count>0
    v4=[tuple(g^x for x in range(4)) for g in range(4)]
    count,separate=torsor_control(4,[1]*4,v4)
    require(count==0 and separate,'Simultaneous-kernel negative control failed')
    crt=0;different=0
    for moduli in itertools.product(range(1,7),repeat=2):
        for residues in itertools.product(*(range(m) for m in moduli)):
            for left,length in [(-5,0),(-5,13),(0,1),(3,17),(10,29)]:
                plus=sum(all((v-r)%m==0 for m,r in zip(moduli,residues)) for v in range(left,left+length))
                minus=sum(all((v+r)%m==0 for m,r in zip(moduli,residues)) for v in range(left,left+length))
                require(abs(plus-minus)<=1,'Full-congruence reflection count failure');crt+=1;different+=plus!=minus
    periods=0
    for numerator in range(1,41):
        for denominator in range(1,41):
            if math.gcd(numerator,denominator)!=1:continue
            rho=F(numerator,denominator);c=4*rho*(1+rho)
            require(1+c==(1+2*rho)**2,'Rotational parameter bridge')
            least=next(k for k in range(1,2*denominator+1) if k%2==0 and k*numerator%denominator==0)
            require(least==math.lcm(2,denominator),'Arc parity/minimal period');periods+=1
    require(math.lcm(2,1)==2,'Odd equator period negative control')
    for j in range(1,1001):
        require(2**j>=j+1,'Logarithmic epsilon bridge')
    endpoints=0
    for n in range(3,201):
        N=n-1
        for m in range(1,N):
            j=N-m;k=j+1
            require(2<=k<n and n-k==m and m+j==N,'Epsilon shift endpoint');endpoints+=1
    require(F(2,99)<F(1) and F(-97,99)<-F(95,100),'Reflected normalization margin')
    return {'torsor_examples':torsors,'torsor_positive_examples':positive,'V4_C4_simultaneous_negative_control':True,
      'full_congruence_reflection_cases':crt,'genuinely_different_reflected_interval_counts':different,
      'rotation_period_examples':periods,'epsilon_shift_endpoint_checks':endpoints,'exact_power_inequalities':1000}


def main():
    inventories=payloads();controls=mathematical_controls()
    print(json.dumps({'status':'passed','published_payload_counts':inventories,'controls':controls,
      'limits':'Bounded controls and payload identity only; no whole Lauv3 proof, analytic subgroup theorem, generalized-theta full audit or infinite sieve-input reproof.'},sort_keys=True,indent=2))


if __name__=='__main__':
    main()
