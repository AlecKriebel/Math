#!/usr/bin/env python3
"""Independent EP-100 audit. Python 3.10+, standard library only.

No imports from the author's code. Algebra uses Q[t]/(t^4-10t^2+1),
t=sqrt(2)+sqrt(3), rather than the author's biquadratic basis.
Finite controls supplement the written audit, not a general-conjecture proof.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import isqrt
from pathlib import Path
import hashlib
import json
import stat
import sys
import zipfile

AUTHOR_ZIP_SHA = 'eab5d5ccc69c6fd8ef9771d14ca78c9da36fc31ddfc32052b718bce97684ce62'
AUTHOR_MANIFEST_SHA = '6156bec0ed953bc03854b4f6926b10eb9d8a4c3a1e676247716374e712a3bedc'
MEMBERS = {'AUTHOR_CHECKS.json','CONTROL_RESULTS.json','MANIFEST.json','PROOFS.md',
           'README.md','RESEARCH_LOG.md','SOURCE_VERIFICATION.json','verify_manifest.py','verify_math.py'}

def require(condition, message):
    if not condition:
        raise ValueError(message)

class K:
    """Reduced polynomial in the positive primitive element t=sqrt(2)+sqrt(3)."""
    def __init__(self, coefficients=0):
        if isinstance(coefficients,K):
            self.c=coefficients.c
            return
        if not isinstance(coefficients,(tuple,list)):
            coefficients=[coefficients]
        c=list(map(Q,coefficients))
        c += [Q(0)]*max(0,4-len(c))
        for j in range(len(c)-1,3,-1):
            # t^j = 10*t^(j-2) - t^(j-4)
            c[j-2]+=10*c[j]
            c[j-4]-=c[j]
        self.c=tuple(c[:4])
    def __add__(self,other):
        other=K(other)
        return K([a+b for a,b in zip(self.c,other.c)])
    __radd__=__add__
    def __neg__(self): return K([-a for a in self.c])
    def __sub__(self,other): return self+-K(other)
    def __rsub__(self,other): return K(other)+-self
    def __mul__(self,other):
        other=K(other)
        c=[Q(0)]*7
        for i,a in enumerate(self.c):
            for j,b in enumerate(other.c): c[i+j]+=a*b
        return K(c)
    __rmul__=__mul__
    def __truediv__(self,rational): return K([a/Q(rational) for a in self.c])
    def __pow__(self,n):
        require(isinstance(n,int) and n>=0,'invalid exponent')
        out=K(1)
        for _ in range(n): out=out*self
        return out
    def __eq__(self,other): return self.c==K(other).c
    def __hash__(self): return hash(self.c)
    def bounds(self):
        # Rational root enclosures selected independently of the author's code.
        den=10**30
        floors=[isqrt(r*den*den) for r in (2,3)]
        for r,b in zip((2,3),floors):
            require(b*b<r*den*den<(b+1)*(b+1),'root enclosure')
        lo=Q(sum(floors),den)
        hi=Q(sum(floors)+2,den)
        lower=upper=Q(0)
        for j,c in enumerate(self.c):
            lower+=c*(lo**j if c>=0 else hi**j)
            upper+=c*(hi**j if c>=0 else lo**j)
        return lower,upper
    def positive(self): return self.bounds()[0]>0

def within(z,lo,hi):
    a,b=z.bounds()
    return Q(lo)<a and b<Q(hi)

def pair_square(p,q):
    return sum(((a-b)**2 for a,b in zip(p,q)),K(0))

def algebra_and_construction():
    t=K([0,1]); rt2=(t**3-9*t)/2; rt3=(11*t-t**3)/2
    require(t**4-10*t**2+1==0,'primitive polynomial')
    require(rt2*rt2==2 and rt3*rt3==3,'positive radical identities')
    require(rt2.positive() and rt3.positive(),'positive square-root branches')
    y=(rt2*rt3-rt2)/2
    require(y*y==2-rt3 and y.positive(),'nested positive square root')
    x=(1+rt2)*y
    require(x**4+4*x**3-4*x*x-4*x+1==0,'seed polynomial')
    require(within(x,Q(1249,1000),Q(1250,1000)),'seed isolation')
    # The quartic is strictly increasing on [1.249,1.250]:
    # p'(z)=4z^3+12z^2-8z-4 >= 4l^3+12l^2-8u-4 > 0.
    l,u=Q(1249,1000),Q(1250,1000)
    p=lambda z:z**4+4*z**3-4*z*z-4*z+1
    require(p(l)<0<p(u),'opposite endpoint signs')
    require(4*l**3+12*l*l-8*u-4>0,'unique seed in rational interval')
    require((1+rt3)*x==2+rt2,'side identity')
    a=x*rt3/3; b=a+x; c=-a-b
    directions=[(K(1),K(0)),(K(Q(-1,2)),rt3/2),(K(Q(-1,2)),-rt3/2)]
    points=[(r*s+K(Q(7,13)),r*v-K(Q(11,17))) for r in (a,b,c) for s,v in directions]
    require(len(set(points))==9,'nine distinct points')
    lengths=[x,1+rt2,2+rt2,2+rt2+x]
    require(all(z.positive() for z in lengths),'positive distance values')
    require((lengths[0]-1).positive(),'minimum distance')
    gaps=[lengths[i+1]-lengths[i] for i in range(3)]
    require((gaps[0]-1).positive() and gaps[1]==1 and (gaps[2]-1).positive(),'three gaps')
    require(within(lengths[-1],Q(4663,1000),Q(4664,1000)),'diameter isolation')
    counts=[0]*4
    by_blocks={}
    for i,j in combinations(range(9),2):
        s=pair_square(points[i],points[j])
        require(s.positive(),'no coincident pair')
        ids=[k for k,r in enumerate(lengths) if s==r*r]
        require(len(ids)==1,'unique spectrum membership')
        counts[ids[0]]+=1
        block=f'{i//3}{j//3}'
        by_blocks.setdefault(block,[0]*4)[ids[0]]+=1
    require(counts==[6,18,6,6],'multiplicities')
    expected={'00':[3,0,0,0],'01':[3,6,0,0],'02':[0,6,3,0],
              '11':[0,0,3,0],'12':[0,6,0,3],'22':[0,0,0,3]}
    require(by_blocks==expected,'complete six-block partition')
    for i in range(3):
        endpoint_squares={pair_square(points[6+i],points[j]) for j in range(6) if j%3!=i}
        require(len(endpoint_squares)==1,'four-endpoint circle center')
    mutant=list(points); mutant[0]=(mutant[0][0]+K(Q(1,1000)),mutant[0][1])
    require(any(all(pair_square(mutant[i],mutant[j])!=r*r for r in lengths)
                for i,j in combinations(range(9),2)),'coordinate perturbation must be detected')
    require(not within(-x,Q(1249,1000),Q(1250,1000)),'negative-root mutant')
    return {'arithmetic':'Q[t]/(t^4-10*t^2+1), t=sqrt(2)+sqrt(3)',
            'seed_polynomial':'X^4+4X^3-4X^2-4X+1',
            'seed_unique_root_interval':['1249/1000','1250/1000'],
            'diameter_interval':['4663/1000','4664/1000'],
            'points':9,'pair_checks':36,'multiplicities':counts,
            'pair_partition':by_blocks,'minimum_gap':'1',
            'mutant_coordinate_rejected':True,'negative_seed_rejected':True}

def sqrt_interval(q,den=10**18):
    q=Q(q)
    require(q>=0,'nonnegative radicand')
    a=isqrt((q.numerator*den*den)//q.denominator)
    l=Q(a,den)
    if l*l==q:return l,l
    u=Q(a+1,den)
    require(l*l<q<u*u,'rational square-root bracket')
    return l,u

def gap_test(high,low):
    high,low=Q(high),Q(low)
    require(high>=low>=0,'ordered radicands')
    # Exact algebraic comparison, with a separately bracketed cross-check below.
    d=high-low-1
    return d>=0 and d*d>=4*low

def finite_controls():
    roots=0
    for a in range(1,150):
        for b in range(a):
            high,low=Q(a,7),Q(b,7)
            hl,hu=sqrt_interval(high); ll,lu=sqrt_interval(low)
            value=gap_test(high,low)
            if hl-lu>1: require(value,'root bracket lower failure')
            elif hu-ll<1: require(not value,'root bracket upper failure')
            else:
                require(hl==hu and ll==lu and hl-ll==1,'unexpected unresolved test')
                require(value,'root equality failure')
            roots+=1
    grid_sizes=0; grid_gaps=0
    for a in range(1,81):
        spectra=sorted({u*u+v*v for u,v in product(range(a+1),repeat=2) if u or v})
        require(spectra[0]==1 and spectra[-1]==2*a*a,'grid endpoints')
        for low,high in zip(spectra,spectra[1:]):
            require(gap_test(16*a*a*high,16*a*a*low),'safe grid scale')
            grid_gaps+=1
        require(not gap_test(4*a*a*(a*a+1),4*a**4),'insufficient grid scale')
        grid_sizes+=1
    require(all(gap_test(a,b) for a,b in [(16,9),(25,16)]),'3-4-5 admissible')
    require(not gap_test(Q(16,9),1),'3-4-5 normalization failure')
    require(not gap_test(2,1),'unscaled square failure')
    neighbour_tests=0
    for gs in product((Q(1),Q(4,3),Q(7,4)),repeat=4):
        values=[Q(5,4)]
        for g in gs: values.append(values[-1]+g)
        require(len(values)<=int(values[-1]),'spectrum cardinality')
        for m in (Q(1),Q(13,10),Q(2),Q(7,2),Q(8)):
            for r in values:
                require(sum(abs(s-r)<=m for s in values)<=2*(m.numerator//m.denominator)+1,'radius count')
                require(2*(2*(m.numerator//m.denominator)+1)<=6*m,'constant 6')
                neighbour_tests+=1
    # Coordinate elimination for |r-s|=1 is independently exact:
    # (r^2-s^2-1)^2 - 4s^2 = -4*y^2 for unit anchors.
    geometry_tests=0
    for den in (1,3,5):
        for ix,iy in product(range(-15,16),repeat=2):
            x,y=Q(ix,den),Q(iy,den)
            r2=x*x+y*y; s2=(x-1)**2+y*y
            require((r2-s2-1)**2-4*s2==-4*y*y,'reverse-triangle equality locus')
            require((r2==s2)==(x==Q(1,2)),'bisector locus')
            geometry_tests+=1
    return {'rational_root_gap_bracket_crosschecks':roots,'grid_sizes':grid_sizes,
            'grid_adjacent_gap_checks':grid_gaps,'radius_neighbour_and_constant_controls':neighbour_tests,
            'unit_pair_algebra_controls':geometry_tests,'normalization_rejected':True}

def no_duplicates(pairs):
    d={}
    for k,v in pairs:
        require(k not in d,'duplicate JSON key')
        d[k]=v
    return d

def freeze_integrity(author):
    author=Path(author)
    require(author.is_dir() and not author.is_symlink(),'regular input directory')
    require({p.name for p in author.iterdir()}==MEMBERS,'exact nine-member allowlist')
    for p in author.iterdir(): require(stat.S_ISREG(p.lstat().st_mode),'regular member')
    manifest_bytes=(author/'MANIFEST.json').read_bytes()
    require(hashlib.sha256(manifest_bytes).hexdigest()==AUTHOR_MANIFEST_SHA,'pinned author manifest')
    data=json.loads(manifest_bytes,object_pairs_hook=no_duplicates)
    require(data['problem_id']==1929 and data['status']=='unresolved-author-freeze','correct target/status')
    entries=data['files']
    require(len(entries)==8 and {e['path'] for e in entries}==MEMBERS-{'MANIFEST.json'},'entry allowlist')
    facts=[]
    for e in entries:
        raw=(author/e['path']).read_bytes(); h=hashlib.sha256(raw).hexdigest()
        require(len(raw)==e['bytes'] and h==e['sha256'],'pinned member bytes')
        facts.append({'path':e['path'],'bytes':len(raw),'sha256':h})
    zpath=author.parent/'ERDOS_1929_AUTHOR_SAFE_FREEZE.zip'
    zr=zpath.read_bytes()
    require(hashlib.sha256(zr).hexdigest()==AUTHOR_ZIP_SHA,'pinned author zip')
    with zipfile.ZipFile(zpath) as z:
        names=z.namelist()
        require(len(names)==9 and set(names)==MEMBERS,'zip exact allowlist')
        for name in names: require(z.read(name)==(author/name).read_bytes(),'zip directory identity')
    return {'author_zip_sha256':AUTHOR_ZIP_SHA,'author_zip_bytes':len(zr),
            'author_manifest_sha256':AUTHOR_MANIFEST_SHA,'zip_matches_directory':True,
            'files':facts}

def main():
    out={'passed':True,'scope':'Independent finite exact controls and pinned freeze integrity; general target unresolved.',
         'piepmeyer':algebra_and_construction(),'controls':finite_controls()}
    if len(sys.argv)>1: out['freeze']=freeze_integrity(sys.argv[1])
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
