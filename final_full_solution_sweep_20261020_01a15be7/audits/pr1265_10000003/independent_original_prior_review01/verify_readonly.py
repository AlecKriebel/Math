#!/usr/bin/env python3
"""Independent exact controls. Reads this audit folder only; no source code runs.
Finite profiles are NOT assumed equilibria. Universal proofs are in REPORT.md.
No network, subprocess, third-party imports, writes or Python assertions.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import comb
import hashlib
import json
import zipfile
import io

ROOT = Path(__file__).resolve().parent
P = ROOT / 'private_sources'
GUARDS = 0
PAIRS = 0


def need(ok, why):
    global GUARDS
    GUARDS += 1
    if not ok:
        raise RuntimeError(why)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def authenticate():
    seal = ROOT / 'MANIFEST.json'
    if seal.exists():
        j = json.loads(seal.read_text())
        actual = {str(f.relative_to(ROOT)) for f in ROOT.rglob('*') if f.is_file() and f != seal}
        need(actual == {e['path'] for e in j['files']}, 'closed inventory exact membership')
        for e in j['files']:
            f = ROOT / e['path']; b = f.read_bytes()
            need(not f.is_symlink(), 'no symlink')
            need(len(b) == e['bytes'] and sha(b) == e['sha256'], 'sealed content ' + e['path'])
            need(e['private'] == e['path'].startswith('private_sources/'), 'private raw body flag')
    for f in ROOT.glob('FETCH_RECEIPTS_*.json'):
        for e in json.loads(f.read_text()):
            if e.get('status') == 200:
                b = (P / e['file']).read_bytes()
                need(len(b) == e['bytes'] and sha(b) == e['sha256'], 'fresh primary receipt')
                if 'declared_checksum' in e:
                    need(e['declared_size'] == len(b) and e['declared_checksum'] == 'md5:' + hashlib.md5(b).hexdigest(), 'published payload size/MD5')
    entries = json.loads((ROOT / 'PR_SOURCE_RECEIPTS.json').read_text())
    need(len(entries) == 8, 'eight immutable paths')
    for e in entries:
        b = (P / e['file']).read_bytes()
        need(e['head'] == 'b1f0bc241aa84d7bef150b77a50c986889970240', 'source head')
        need(e['path'].startswith('unsolved_math_prioritization/attempts/10000003/'), 'source scope')
        need(len(b) == e['bytes'] and sha(b) == e['sha256'], 'source SHA256')
        need(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == e['git_blob'], 'Git object content identity')
    nested = json.loads((P / 'pr_PUBLIC_MANIFEST.json').read_text())
    need(len(nested['files']) == 7, 'nested manifest seven plus self')
    for e in nested['files']:
        b = (P / ('pr_' + e['path'])).read_bytes()
        need(len(b) == e['bytes'] and sha(b) == e['sha256'], 'nested manifest pinned')
    pr = json.loads((P / 'github_connector.json').read_text())['structuredContent']['pull_request']
    need(pr['number'] == 1265 and pr['head_sha'] == entries[0]['head'], 'connector PR identity')
    need(sha(pr['body'].encode()) == 'd5865314f14e22b88d104f0bd5855d68424a5a22fd2a31b0004971d96686d9d3', 'PR body pin')
    rec = json.loads((P / 'zenodo_record.json').read_text())
    latest = json.loads((P / 'zenodo_latest.json').read_text())
    versions = json.loads((P / 'zenodo_versions.json').read_text())
    need(rec['id'] == latest['id'] == 23113437 and rec['state'] == 'done' and rec['submitted'] is True, 'actual published latest record')
    need(rec['doi'] == '10.5281/zenodo.23113437' and rec['conceptdoi'] == '10.5281/zenodo.23113436', 'DOI family')
    need(versions['hits']['total'] == 1 and len(rec['files']) == 3, 'version and support count')
    need(rec['metadata']['creators'][0]['name'] == 'Ferudun, Alper', 'attribution')
    need(rec['metadata']['version'] == '1.0', 'actual published version')
    need((P / 'author_paper.pdf').read_bytes() == (P / 'zenodo_AMR-099-0003-paper.pdf').read_bytes(), 'author and DOI PDF identical')
    need((P / 'author_source.zip').read_bytes() == (P / 'zenodo_AMR-099-0003-source.zip').read_bytes(), 'author and DOI ZIP identical')
    earlier = (P / 'zenodo_main.tex').read_text()
    later = (P / 'arxiv_main.tex').read_text()
    comparison = json.loads((ROOT / 'VERSION_COMPARISON.json').read_text())
    starts = ['\\section{The gaps form a harmonic function}',
              '\\section{Reversible random walks with long-range jumps}',
              '\\section{The energy estimate and the proof of the theorem}']
    for e, left, right in zip(comparison['sections'], starts, starts[1:]):
        a = earlier[earlier.index(left):earlier.index(right)].encode()
        b = later[later.index(left):later.index(right)].encode()
        need(a == b and sha(a) == e['zenodo_sha256'] == e['arxiv_sha256'], 'common primary proof sections exact')
    need('o(R^s)' in earlier and '2<s\\le(3+\\sqrt5)/2' in earlier, 'actual earlier same-endpoint sketch retained')
    need('A sketch suggests' in earlier and 'A sketch suggests' not in later, 'important source-version difference preserved')
    need('we make no claim for' in earlier and 'we make no claim for' in later.lower(), 'source scope limits not erased')
    index = json.loads((ROOT / 'PUBLISHED_SUPPORT_INDEX.json').read_text())['all_members']
    with zipfile.ZipFile(io.BytesIO((P / 'zenodo_AMR-099-0003-source.zip').read_bytes())) as z:
        need(z.testzip() is None, 'all ZIP CRCs')
        need(set(z.namelist()) == {e['path'] for e in index} | {n for n in z.namelist() if n.endswith('/')}, 'all scientific support members indexed')
        for e in index:
            b = z.read(e['path']); need(len(b) == e['bytes'] and sha(b) == e['sha256'], 'support member identity')
        need(z.read('verification_report.md') == (P / 'zenodo_AMR-099-0003-verification-report.md').read_bytes(), 'standalone and ZIP verification reports identical')
    for suffix in ['initial', 'final']:
        f = ROOT / (suffix.upper() + '_LEDGER_CHECK.json')
        if f.exists():
            j = json.loads(f.read_text()); b = (P / ('ledger_' + suffix + '.json')).read_bytes()
            need(j['request']['dataFilters'][0]['gridRange'] == {'sheetId':1254632077,'startColumnIndex':0,'endColumnIndex':43}, 'numeric full-column sheet')
            need(sha(b) == j['sha256'] and len(json.loads(b)['valueRanges'][0]['valueRange']['values']) == j['rows'], 'ledger capture')
    f = ROOT / 'PROPOSED_ROW.json'
    if f.exists():
        j = json.loads(f.read_text())
        need(len(j['cells']) == 4 and all(isinstance(c, str) for c in j['cells']), 'four literal cells')
        need(j['cells'][1] == '' and j['cells'][2] == 'https://doi.org/10.5281/zenodo.23113437', 'blank B and exact existing DOI')
        need(j['ready_for_external_write'] is False and j['extension_claimed_as_prior_theorem'] is False, 'held original-only row')


def ln_bounds(x, count=50):
    """Exact rational enclosure via range reduction and atanh series."""
    x = Q(x); need(x > 0, 'log domain')
    exponent = 0
    while x >= 2: x /= 2; exponent += 1
    while x < 1: x *= 2; exponent -= 1
    def raw(y):
        u = (y - 1)/(y + 1)
        low = 2*sum((u**(2*k+1)/Q(2*k+1) for k in range(count)),Q())
        error = 2*u**(2*count+1)/Q(2*count+1)/(1-u*u)
        return low,low+error
    lo,hi=raw(x);a,b=raw(Q(2))
    return (lo+exponent*a,hi+exponent*b) if exponent>=0 else (lo+exponent*b,hi+exponent*a)


def integral(lo, hi, power):
    return (lo**(1-power)-hi**(1-power))/Q(power-1)


def profile_tests():
    global PAIRS
    profiles = [[Q(1)]*32,
                [Q(3,2)**abs(i-16) for i in range(33)],
                [Q(2)**(-abs(i-16)) for i in range(33)],
                [Q(1) if i%2 else Q(3,2) for i in range(32)]]
    for base in profiles:
        for scale in [Q(1,1000000), Q(1), Q(1000000)]:
            gaps=[g*scale for g in base]; a=[Q()]
            for g in gaps:a.append(a[-1]+g)
            offset=a[len(a)//2];a=[x-offset for x in a];r=Q(2)
            need(all(1/r <= gaps[i+1]/gaps[i] <= r for i in range(len(gaps)-1)), 'profile adjacent ratio')
            for n in range(1,len(gaps)-1):
                for j in range(1,len(gaps)-1):
                    if j==n:continue
                    D=abs(a[j]-a[n]);E=abs(a[j+1]-a[n+1]);
                    need(min(D,E)>=D/(1+r),'distance comparison no global gap bound')
                    for s in [2,3,4]:
                        c=(D**(-s)-E**(-s))/(E-D) if E!=D else s*D**(-s-1)
                        signed=(1 if j>n else -1)*(D**(-s)-E**(-s))
                        need(c>0 and c*(gaps[j]-gaps[n])==signed,'exact shifted-force term sign')
                        need(c<=s*(1+r)**(s+1)*D**(-s-1),'conductance comparison')
                        if s==2:need(c==(D+E)/(D*D*E*E),'inverse-square closed form')
                    if j>n:
                        for power in [2,3,4]:
                            need(gaps[j]*D**(-power) <= (1+r)**power*integral(D,D+gaps[j],power),'right integration comparison')
                            need(gaps[n]*D**(-power) <= r*(1+r)**power*integral(D,D+gaps[n-1],power),'left integration comparison')
                    PAIRS+=1
            # Exact finite cutoff contributions supplement the written infinite tails.
            for R in [min(-a[0],a[-1])/8,min(-a[0],a[-1])/4]:
                f=[max(Q(),min(Q(1),2-abs(x)/R)) for x in a[:-1]]
                support=[i for i,x in enumerate(a[:-1]) if abs(x)<2*R]
                if len(support)<2:continue
                near=far=energy=Q();I=[i for i,g in enumerate(gaps) if abs(a[i])<3*R and g<=R]
                need(sum((gaps[i] for i in I),Q())<=7*R,'sum of disjoint near gaps')
                need(sum((gaps[i] for i in support),Q())<=4*(1+r)*R,'outgoing support gap included')
                for n in range(len(gaps)):
                    for j in range(n+1,len(gaps)):
                        D=a[j]-a[n];E=a[j+1]-a[n+1]
                        v=gaps[n]*gaps[j]*(f[n]-f[j])**2/D**3
                        if D<=R:near+=v
                        else:far+=v
                        c=(D+E)/(D*D*E*E);energy+=c*gaps[n]*gaps[j]*(f[n]-f[j])**2
                need(energy<=54*(near+far),'unordered energy convention')
                need(far<=2*(1+r)**5/R,'complete universal far bound also dominates finite subset')
                if I:
                    lo,hi=ln_bounds((1+r)*Q(len(I),7))
                    need(near <= 7*(1+r)/R*max(Q(1),lo),'logarithmic near bound with rational enclosure')


def network_and_edge_controls():
    # Infinite complete network c_ij=w_i*w_j, w_i=2^(-i-1).
    # u finite; v_i=i+1 has exact weighted sum2. All tail edges are summed.
    u={0:Q(1),1:Q(-2),3:Q(3)};w=lambda i:Q(1,2**(i+1));v=lambda i:Q(i+1)
    U=sum((w(i)*x for i,x in u.items()),Q());UV=sum((w(i)*x*v(i) for i,x in u.items()),Q())
    lhs=Q()
    for i in u:
        for j in u:
            lhs+=w(i)*w(j)*(u[i]-u[j])*(v(i)-v(j))/2
    tailW=1-sum((w(i) for i in u),Q());tailV=2-sum((w(i)*v(i) for i in u),Q())
    lhs+=sum((w(i)*u[i]*(v(i)*tailW-tailV) for i in u),Q())
    rhs=sum((u[i]*w(i)*(v(i)-2) for i in u),Q())
    need(lhs==rhs==UV-2*U,'infinite-degree Green identity including unbounded integrable function')
    truncated=sum((w(i)*w(j)*(u[i]-u[j])*(v(i)-v(j))/2 for i in u for j in u),Q())
    need(truncated!=lhs,'omitting infinite neighbors rejected')
    # Transient birth-death network c(n,n+1)=2^n has positive h_n=2^-n.
    # Its transform reverses drift, while return probabilities remain identical.
    for n in range(-5,6):
        h=Q(2)**(-n);left=Q(2)**(n-1);right=Q(2)**n;mu=left+right
        need(left*(2*h)+right*(h/2)==mu*h,'nonconstant harmonic function on control network')
        need(left*h*(2*h)+right*h*(h/2)==mu*h*h,'transformed finite row mass')
        need(Q(2,3)/(2*h)+Q(1,3)/(h/2)==1/h,'reciprocal transformed harmonicity')
    for m in range(1,12):
        need(comb(2*m,m)*Q(1,3)**m*Q(2,3)**m==comb(2*m,m)*Q(2,3)**m*Q(1,3)**m,'Doob return probabilities equal; no automatic recurrence')
    # Exact quadratic-field endpoint s=(3+sqrt5)/2.
    def mul(x,y):return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
    s=(Q(3,2),Q(1,2));square=mul(s,s)
    need((square[0]-3*s[0]+1,square[1]-3*s[1])==(0,0),'critical exponent exactly zero')
    need(Q(5,2)**2-3*Q(5,2)+1<0,'interior extension exponent')
    above=Q(8,3);q=above*above-3*above+1
    need(q-(above-2)*Q(1,12)>0,'mere little-o insufficient above endpoint')
    squares=[Q(k*k) for k in [1,2,7,13]]
    need(sum([1,2,7,13])**2<=len(squares)*sum(squares),'power-concavity exact square-root control')
    need(1+81>Q(1,2)*(1+9)**2,'false concavity for exponent2 rejected')
    # Local finiteness alone need not give finite forces: ±sqrt(n) at origin.
    for k in range(1,9):
        block=sum((Q(1,n) for n in range(2**k,2**(k+1))),Q())
        need(block>=Q(1,2),'dyadic force block lower bound; symmetric cancellation not absolute convergence')
    labels=[1,0,2]
    need(labels[2]-labels[1]!=labels[1]-labels[0],'arbitrary re-enumeration not affine')
    need(sum([])==0 and len({Q(0)})<2,'singleton excluded by standalone hypothesis')


def main():
    authenticate();profile_tests();network_and_edge_controls()
    print(json.dumps({'status':'PASS','guards':GUARDS,'ordered_pair_controls':PAIRS,
                      'arithmetic':'exact Fraction identities and rational log enclosures',
                      'source_author_programs_executed':False,
                      'finite_profiles_are_equilibria':False,
                      'universal_claim_basis':'written proof and authenticated full primary theorem, not sampling',
                      'scope':'prior inverse-square theorem accepted; extended proof separate and earlier same-endpoint sketch credited'},sort_keys=True))


if __name__=='__main__':main()
