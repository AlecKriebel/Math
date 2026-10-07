#!/usr/bin/env python3
"""Independent exact check; imports neither author verifier nor any author implementation.
Uses closed-form conductor equations and shortest residue-class paths (Apery sets).
"""
from pathlib import Path
from fractions import Fraction
from math import gcd
from heapq import heappush, heappop
import hashlib, json, tarfile
BASE=Path(__file__).resolve().parent.parent
PACK=BASE/'public_candidate'

def require(value, message):
    if not value:
        raise RuntimeError(message)

def fingerprint(path):
    b=path.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

# The threshold alone gives m <= 7. For these m there are at most two gcd drops.
# Enumerate semigroup generators using conductor = sum((n_i-1)*v_i)-m+1,
# rather than the author's characteristic-increment recursion.
rows=[]
for m in range(2,8):
    for v1 in range(m+1,92):
        e=gcd(m,v1)
        if e==m or Fraction(1,m)+Fraction(1,v1)<Fraction(3,11):
            continue
        if e==1:
            if (m-1)*(v1-1)==90:
                rows.append((m,(v1,),(m,v1)))
            continue
        numerator=90+m-1-(m//e-1)*v1
        if numerator%(e-1):
            continue
        v2=numerator//(e-1)
        if v2<=m//e*v1 or gcd(e,v2)!=1:
            continue
        beta2=v1+v2-(m//e)*v1
        rows.append((m,(v1,beta2),(m,v1,v2)))
rows.sort()
require(len(rows)==12,'threshold inventory is not twelve')

def apery(gens):
    m=gens[0]
    dist=[10**12]*m
    dist[0]=0
    heap=[(0,0)]
    while heap:
        val,res=heappop(heap)
        if val!=dist[res]:
            continue
        for gen in gens[1:]:
            new=val+gen
            rr=new%m
            if new<dist[rr]:
                dist[rr]=new
                heappush(heap,(new,rr))
    require(all(x<10**12 for x in dist),'semigroup not cofinite')
    return dist

def count(ap,limit):
    m=len(ap)
    return sum(max(0,(limit-1-w)//m+1) for w in ap)

# Independently check the packet's wider claim of twenty-two genus-45 signatures
# for degree eleven. Enumerate ordered multiplicative gcd-drop indices n_i,
# then solve the conductor as a weighted generator sum; no characteristic
# increment recursion from the author's program is used.
def ordered_factorizations(m):
    yield (m,)
    for n in range(2,m):
        if m%n==0:
            for tail in ordered_factorizations(m//n):
                yield (n,)+tail

def generator_solutions(m,indices):
    target=90+m-1
    def step(pos,old_gcd,remaining,gens):
        if pos==len(indices):
            if remaining==0:
                yield tuple(gens)
            return
        ni=indices[pos]
        new_gcd=old_gcd//ni
        lower=m+1 if pos==0 else indices[pos-1]*gens[-1]+1
        upper=remaining//(ni-1)
        for vi in range(lower,upper+1):
            if gcd(old_gcd,vi)==new_gcd:
                yield from step(pos+1,new_gcd,remaining-(ni-1)*vi,gens+[vi])
    return step(0,m,target,[])

all_semigroups=[]
for m in range(2,11):
    for indices in ordered_factorizations(m):
        for positive in generator_solutions(m,indices):
            betas=[positive[0]]
            for i in range(1,len(positive)):
                betas.append(betas[-1]+positive[i]-indices[i-1]*positive[i-1])
            all_semigroups.append((m,tuple(betas),(m,)+positive))
require(len(all_semigroups)==len(set(all_semigroups))==22,'full signature count')
require(sorted(r for r in all_semigroups if Fraction(1,r[0])+Fraction(1,r[1][0])>=Fraction(3,11))==rows,'full enumeration threshold mismatch')
full_distribution_survivors=[]
for m,betas,gens in all_semigroups:
    a=apery(gens)
    require(max(a)-m+1==90,'full inventory conductor')
    require(Fraction(sum(a),m)-Fraction(m-1,2)==45,'full inventory genus')
    if all(count(a,11*j+1)==(j+1)*(j+2)//2 for j in range(10)):
        full_distribution_survivors.append((m,betas,gens))
require(full_distribution_survivors==[(10,(11,),(10,11))],'full semigroup survivor inventory')

# Compare against the packet only after deriving the candidates independently.
recorded=json.loads((PACK/'checks_result.json').read_text())
expected={(x['multiplicity'],tuple(x['characteristic_exponents']),tuple(x['generators'])):x
          for x in recorded['witnesses']}
require(set(rows)==set(expected),'candidate signature mismatch')
certificates=[]
for m,betas,gens in rows:
    a=apery(gens)
    # Standard Apery formulas give exact conductor and number of gaps without a cutoff.
    conductor=max(a)-m+1
    gap_count=Fraction(sum(a),m)-Fraction(m-1,2)
    require(conductor==90 and gap_count==45,'Apery genus/conductor mismatch')
    j=expected[(m,betas,gens)]['j']
    cutoff=11*j+1
    actual=count(a,cutoff)
    mandated=(j+1)*(j+2)//2
    elements=[n for n in range(cutoff) if n>=a[n%m]]
    require(actual==len(elements)==expected[(m,betas,gens)]['count'],'witness count mismatch')
    require(elements==expected[(m,betas,gens)]['elements'],'witness elements mismatch')
    require(actual>mandated,'no semigroup obstruction')
    all_counts=[count(a,11*k+1) for k in range(10)]
    certificates.append({'multiplicity':m,'characteristic_exponents':betas,'generators':gens,
      'apery_by_residue':a,'conductor':conductor,'gap_count':int(gap_count),
      'lct':str(Fraction(1,m)+Fraction(1,betas[0])),
      'j':j,'cutoff_exclusive':cutoff,'elements':elements,
      'actual':actual,'required':mandated,'counts_j_0_through_9':all_counts})

# Independent easy Markov obstruction after descent to a maximum of eleven.
# For a>=2, F_a(b) is decreasing for a<=b<=11 and F_a(a)=121-31*a*a<0.
require(all(22<33*a and 121-31*a*a<0 for a in range(2,12)), 'Markov monotonicity')
require(4*4-33*4+122==6 and 5*5-33*5+122==-18,'Markov a=1 interval')
markov_solutions=[(a,b) for a in range(1,12) for b in range(a,12)
                 if a*a+b*b+121==33*a*b]
require(not markov_solutions,'unexpected Markov eleven')

# Include composite odd p as required by Proposition 3.1.
hyper_tests=0
for p in range(5,102,2):
    g=(p-1)*(p-2)//2
    require(2*g-2==p*(p-3),'canonical degree')
    for k in range(0,2*p+2):
        n=k*p
        # Count the two residue families in the Weierstrass semigroup <2,2g+1>.
        h=sum(max(0,(n-start)//2+1) for start in (0,2*g+1))
        pl=(k+2)*(k+1)//2-(max(0,k-p+2)*max(0,k-p+1))//2
        require(h>=pl,'Hilbert inequality')
        if k<=p-3:
            require(h-pl==k*(p-k-3)//2,'low-power closed form')
        else:
            require(h==pl==n-g+1,'nonspecial equality')
        hyper_tests+=1
partitions=[(11-m*e,m,e) for m in range(2,6) for e in range(2,6) if 4<=m*e<11]
require(sorted(partitions)==[(1,2,5),(1,5,2),(2,3,3),(3,2,4),(3,4,2),(5,2,3),(5,3,2),(7,2,2)],'net factorization')

manifest=json.loads((PACK/'MANIFEST.json').read_text())
for rec in manifest['files']:
    require(fingerprint(PACK/rec['path'])=={'bytes':rec['bytes'],'sha256':rec['sha256']},'manifest mismatch')
with tarfile.open(BASE/'authored_candidate.tar.gz') as archive:
    members=[m for m in archive.getmembers() if m.isfile()]
    require(len(members)==10,'archive member count')
    for member in members:
        name=Path(member.name).name
        require(archive.extractfile(member).read()==(PACK/name).read_bytes(),'archive and directory differ')
archive_hash=fingerprint(BASE/'authored_candidate.tar.gz')
require(archive_hash['sha256']=='39569a25dc07224ee3494a9ba7e44cced3063653127e315c2764fe392e02fed7','archive fingerprint')
result={'status':'PASS','method':'closed-form conductor equations plus Apery shortest-path certificates',
 'original_archive':archive_hash,'original_manifest':fingerprint(PACK/'MANIFEST.json'),
 'original_manuscript_tex':fingerprint(PACK/'manuscript.tex'),
 'original_manuscript_pdf':fingerprint(PACK/'manuscript.pdf'),
 'archive_files_match':len(members),'manifest_files_match':len(manifest['files']),
 'all_genus_45_signatures':len(all_semigroups),'full_distribution_survivors':full_distribution_survivors,
 'threshold_candidates':len(rows),'survivors':0,'hyperelliptic_cases':hyper_tests,
 'hyperelliptic_odd_p_range':[5,101],'markov_eleven_solutions':markov_solutions,
 'net_partitions_degree_eleven':sorted(partitions),'certificates':certificates}
print(json.dumps(result,indent=2))
