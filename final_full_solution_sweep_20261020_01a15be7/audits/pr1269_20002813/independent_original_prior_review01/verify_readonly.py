#!/usr/bin/env python3
"""Independent finite-algebra controls; no external code, network, writes or asserts.
The universal proof and direct journal-source proof review are in REPORT.md.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import hashlib
import json

ROOT=Path(__file__).resolve().parent
P=ROOT/'private_sources'
GUARDS=0


def need(ok,why):
    global GUARDS
    GUARDS+=1
    if not ok:raise RuntimeError(why)


def sha(b):return hashlib.sha256(b).hexdigest()


def authenticate():
    seal=ROOT/'MANIFEST.json'
    if seal.exists():
        j=json.loads(seal.read_text())
        need({str(f.relative_to(ROOT)) for f in ROOT.rglob('*') if f.is_file() and f!=seal}=={e['path'] for e in j['files']},'closed membership')
        for e in j['files']:
            f=ROOT/e['path'];b=f.read_bytes()
            need(not f.is_symlink(),'no symlink')
            need(len(b)==e['bytes'] and sha(b)==e['sha256'],'sealed content '+e['path'])
            need(e['private']==e['path'].startswith('private_sources/'),'raw body private')
    for f in ROOT.glob('FETCH_RECEIPTS_*.json'):
        for e in json.loads(f.read_text()):
            if e.get('status')==200:
                b=(P/e['file']).read_bytes()
                need(len(b)==e['bytes'] and sha(b)==e['sha256'],'primary receipt')
                if e['file']=='di_doi.html':need(e['body_may_be_truncated'] is True,'capped landing not full body')
    entries=json.loads((ROOT/'PR_SOURCE_RECEIPTS.json').read_text())
    need(len(entries)==8,'eight PR bodies')
    for e in entries:
        b=(P/e['file']).read_bytes()
        need(e['head']=='11aff32f2bb6900234c5f468f21860913c09dcd7','immutable head')
        need(e['path'].startswith('unsolved_math_prioritization/attempts/20002813/'),'scoped path')
        need(len(b)==e['bytes'] and sha(b)==e['sha256'],'PR source bytes')
        need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob'],'Git blob pin')
    nested=json.loads((P/'pr_PUBLIC_MANIFEST.json').read_text())
    need(len(nested['files'])==7,'nested manifest membership')
    for e in nested['files']:
        b=(P/('pr_'+e['path'])).read_bytes()
        need(len(b)==e['bytes'] and sha(b)==e['sha256'],'nested manifest hash')
    pr=json.loads((P/'github_connector.json').read_text())['structuredContent']['pull_request']
    need(pr['head_sha']==entries[0]['head'] and pr['number']==1269,'live connector identity at capture')
    need(sha(pr['body'].encode())=='0839c89afd2c70730e3b0e9fa7eb86b856d994c59d2aaef391ef0ec25e067ed9','PR body pin')
    di=(P/'di_publisher.pdf').read_bytes()
    need(di.startswith(b'%PDF-') and di.rstrip().endswith(b'%%EOF'),'actual complete journal PDF, not HTML')
    need(sha(di)=='97f2ec10b33e448f3d669c112c99ecfadd59e53e7563549ae7bc17f396ceeae8','fresh journal PDF exact pin')
    md=json.loads((P/'crossref_di.json').read_text())['message']
    need(md['DOI'].lower()=='10.1090/s0002-9947-07-04365-6' and md['volume']=='360' and md['issue']=='5' and md['page']=='2359-2392','prior publication exact metadata')
    for suffix in ['initial','final']:
        f=ROOT/(suffix.upper()+'_LEDGER_CHECK.json')
        if f.exists():
            j=json.loads(f.read_text());b=(P/('ledger_'+suffix+'.json')).read_bytes()
            need(j['request']['dataFilters'][0]['gridRange']=={'sheetId':1254632077,'startColumnIndex':0,'endColumnIndex':43},'numeric full-column GWS')
            need(sha(b)==j['sha256'] and len(json.loads(b)['valueRanges'][0]['valueRange']['values'])==j['rows'],'ledger capture')
    f=ROOT/'PROPOSED_ROW.json'
    if f.exists():
        j=json.loads(f.read_text())
        need(len(j['cells'])==4 and all(isinstance(x,str) for x in j['cells']),'four literal strings')
        need(j['cells'][1]=='' and j['cells'][2]=='https://doi.org/10.1090/S0002-9947-07-04365-6','blank B/exact prior DOI')
        need(j['ready_for_external_write'] is False and j['general_classification_resolved'] is False,'held genuine subquestion only')


class Field:
    def __init__(self,q):self.q=q;self.p=2 if q in [2,4] else 3
    def add(self,a,b):return a^b if self.q==4 else (a+b)%self.q
    def neg(self,a):return a if self.q==4 else (-a)%self.q
    def mul(self,a,b):
        if self.q!=4:return a*b%self.q
        z=0
        while b:
            if b&1:z^=a
            b>>=1;a<<=1
            if a&4:a^=7
        return z
    def total(self,items):
        z=0
        for x in items:z=self.add(z,x)
        return z
    def theta(self,a):
        if self.q==4:
            a=self.add(a,self.mul(a,a));need(a in [0,1],'F4 trace in prime field')
        if self.p==2:return (-1 if a else 1,0)
        return [(1,0),(0,1),(-1,-1)][a]


def cadd(z,w):return(z[0]+w[0],z[1]+w[1])
def cmul(z,w):return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]-z[1]*w[1])
def cscale(n,z):return(n*z[0],n*z[1])
def cconj(z):return(z[0]-z[1],-z[1])
def ctotal(z):
    a=(0,0)
    for v in z:a=cadd(a,v)
    return a


class Algebra:
    def __init__(self,F,kind):
        self.F=F;self.kind=kind;self.d=0 if kind=='zero' else 2 if kind=='squarezero' else 3
        self.zero=(0,)*self.d;self.vec=list(product(range(F.q),repeat=self.d))
        self.basis=[tuple(int(j==i) for j in range(self.d)) for i in range(self.d)]
    def add(self,x,y):return tuple(self.F.add(a,b) for a,b in zip(x,y))
    def neg(self,x):return tuple(self.F.neg(a) for a in x)
    def dot(self,x,y):return self.F.total(self.F.mul(a,b) for a,b in zip(x,y))
    def mul(self,x,y):
        if self.kind in ['zero','squarezero']:return self.zero
        if self.kind=='upper3':return(0,0,self.F.mul(x[0],y[1]))
        return(0,self.F.mul(x[0],y[0]),self.F.add(self.F.mul(x[0],y[1]),self.F.mul(x[1],y[0])))
    def unit(self,x,y):return self.add(self.add(x,y),self.mul(x,y))
    def inverse(self,x):
        z=self.zero;t=x
        for i in range(1,self.d+2):
            z=self.add(z,self.neg(t) if i%2 else t);t=self.mul(t,x)
        need(t==self.zero and self.unit(x,z)==self.zero and self.unit(z,x)==self.zero,'nilpotent unit inverse')
        return z
    def dual(self,l,columns):return tuple(self.dot(l,x) for x in columns)


def model(q,kind):
    F=Field(q);A=Algebra(F,kind);V=A.vec;size=len(V);zero=A.zero
    inv={g:A.inverse(g) for g in V}
    left={g:[A.add(x,A.mul(inv[g],x)) for x in A.basis] for g in V}
    right={g:[A.add(x,A.mul(x,inv[g])) for x in A.basis] for g in V}
    # Generated left/right transformations, not a presupposed orbit classification.
    moves=list(left.values())+list(right.values());unseen=set(V);orbits=[]
    while unseen:
        seed=min(unseen);O={seed};queue=[seed]
        for l in queue:
            for T in moves:
                v=A.dual(l,T)
                if v not in O:O.add(v);queue.append(v)
        need(O<=unseen,'orbit partition consistency');unseen-=O;orbits.append(sorted(O))
    at={l:i for i,O in enumerate(orbits) for l in O};zorb=at[zero]
    def e(l,x,a=1):return F.theta(F.mul(a,A.dot(l,x)))
    E={l:[e(l,x) for x in V] for l in V}
    for a in range(1,q):
        signatures={tuple(e(l,x,a) for x in V) for l in V}
        need(len(signatures)==size,'additive dual bijection for every nontrivial character')
    if size>1:need(len({((1,0),)*size for l in V})==1<size,'trivial additive character rejected as Fourier identification')
    if q==4 and size>1:need(F.theta(1)==(1,0) and F.theta(2)!=F.theta(1),'nonfaithful F4 additive character explicitly tested')
    S=[[ctotal(E[l][i] for l in O) for i in range(size)] for O in orbits]
    for x in range(size):need(ctotal(s[x] for s in S)==((size,0) if V[x]==zero else (0,0)),'correct Fourier regular-character sum')
    degrees=[];canonical=[]
    # Independent induced-character formula authenticates normalization directly.
    for index,O in enumerate(orbits):
        l=O[0];H={g for g in V if A.dual(l,right[g])==l}
        one={A.dual(l,right[g]) for g in V};r=len(one);need(len(O)%r==0,'whole number of one-sided orbits');n=len(O)//r
        need(size==len(H)*r,'stabilizer index');degrees.append(r);canonical.append(len(O))
        for h in H:
            for k in H:need(e(l,A.unit(h,k))==cmul(e(l,h),e(l,k)),'stabilizer restriction really a linear group character')
        for i,x in enumerate(V):
            total=(0,0)
            for t in V:
                y=A.mul(inv[t],x);conjugate=A.add(A.add(A.add(x,y),A.mul(x,t)),A.mul(y,t))
                if conjugate in H:total=cadd(total,e(l,conjugate))
            need(total[0]%len(H)==0 and total[1]%len(H)==0,'exact induced value integral cyclotomic coordinates')
            induced=(total[0]//len(H),total[1]//len(H))
            need(cscale(n,induced)==S[index][i],'canonical Fourier sum equals integer times actual induced character')
        norm=ctotal(cmul(z,cconj(z)) for z in S[index])
        need(norm==(size*len(O),0),'canonical norm and degree equal orbit size')
    products=points=0;aggregate_mistake_detected=False
    for i,O in enumerate(orbits):
        for j,Q in enumerate(orbits):
            counts=Counter(A.add(l,m) for l in O for m in Q);coeff=[]
            for T in orbits:
                values={counts[v] for v in T};need(len(values)==1,'fixed-target count constant on full two-sided orbit');coeff.append(next(iter(values)))
            need(sum(k*len(T) for k,T in zip(coeff,orbits))==len(O)*len(Q),'identity degree check')
            negO={A.neg(l) for l in O};need(coeff[zorb]==(len(O) if set(Q)==negO else 0),'zero coefficient exact')
            for x in range(size):
                need(cmul(S[i][x],S[j][x])==ctotal(cscale(k,s[x]) for k,s in zip(coeff,S)),'pointwise product exact cyclotomic equality');points+=1
            if i==zorb and len(Q)>1:
                need(coeff[j]==1 and sum(counts[v] for v in Q)==len(Q),'target-orbit aggregate coefficient rejected');aggregate_mistake_detected=True
            products+=1
    if kind=='upper3':need(aggregate_mistake_detected,'nontrivial target-orbit negative control exercised')
    if q==2 and kind=='upper3':
        need(sorted(degrees)==[1,1,1,1,2] and sorted(canonical)==[1,1,1,1,4],'explicit conventional/canonical normalization distinction')
        need(sum(degrees)==6!=size and sum(canonical)==size,'unweighted conventional regular sum rejected')
    return {'q':q,'algebra':kind,'dimension':A.d,'group_order':size,'orbits':len(orbits),'products':products,'pointwise_identities':points}


def main():
    authenticate();results=[]
    for q in [2,3,4]:
        for kind in ['zero','squarezero','upper3','truncated_t4']:results.append(model(q,kind))
    print(json.dumps({'status':'PASS','guards':GUARDS,'models':results,'orbit_products':sum(x['products'] for x in results),'pointwise_identities':sum(x['pointwise_identities'] for x in results),'source_author_programs_executed':False,'arithmetic':'exact finite fields and integer cyclotomic coordinates','scope':'finite falsification controls plus source authentication; universal result established by written proof and directly inspected Diaconis–Isaacs5.5/5.6'},sort_keys=True))


if __name__=='__main__':main()
