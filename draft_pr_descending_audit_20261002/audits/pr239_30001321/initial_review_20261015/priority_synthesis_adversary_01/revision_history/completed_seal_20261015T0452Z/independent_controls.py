"""Read-only input validation and independent exact finite audit controls.

Writes its receipt only beside this script. These controls test identities and
bookkeeping; the analytic audit, not a finite run, establishes limit claims.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import comb, ceil
from datetime import datetime, timezone
import hashlib
import json

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
count = 0


def check(value):
    global count
    count += 1
    assert value, count


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifests():
    result = []
    for lane, name in [
        ('priority_historical_01', 'AUTHORED_MANIFEST.json'),
        ('priority_local_limit_01', 'PUBLIC_AUTHORED_MANIFEST.json'),
        ('priority_recent_01', 'AUTHORED_MANIFEST.json'),
        ('priority_bridge_01', 'PUBLIC_AUTHORED_MANIFEST.json'),
    ]:
        path = BASE / lane / name
        data = json.loads(path.read_text())
        for row in data['files']:
            f = path.parent / row['path']
            check(f.is_file())
            check(f.stat().st_size == row['bytes'])
            check(digest(f) == row['sha256'])
            check('private_reading' not in f.relative_to(path.parent).parts)
        result.append(dict(path=str(path.relative_to(BASE)), sha256=digest(path), entries=len(data['files'])))
    # Exact candidate inputs, independently compared with bridge and local lane pins.
    pins = json.loads((BASE/'priority_bridge_01/CANDIDATE_INPUTS.json').read_text())
    local = json.loads((BASE/'priority_local_limit_01/INPUT_HASHES.json').read_text())
    for row in pins:
        p = Path(row['path'])
        check(p.stat().st_size == row['bytes'])
        check(digest(p) == row['sha256'] == local[str(p)])
    return result


def exact_margins():
    gamma, beta, eta, b, rho = F(5,16), F(9,32), F(1,64), F(1,128), F(7,8)
    d = F(1,2)-gamma/rho
    check(beta-eta-2*b == F(1,4))
    check(beta-eta-2*b > F(1,2)-gamma)
    check(2*beta-F(1,2)-eta-2*b == F(1,32))
    check(gamma-beta == F(1,32) > b)
    check(d == F(1,7) > b)
    check(b <= F(1,8))
    check(b*rho/gamma == F(7,320))
    # The small-stage colored concentration power at n <= N^(1/4).
    check(F(1,4)-b/2 == F(63,256) > 0)
    return dict(gamma=str(gamma),beta=str(beta),eta=str(eta),b=str(b),rho=str(rho),d=str(d),M_power=str(b*rho/gamma),small_stage_power=str(F(1,4)-b/2))


def shear_control():
    # Different values at every visited space-time site; exact rational path laws.
    for n in range(1,11):
        xlaw = {0:F(1)}
        ylaw = {0:F(1)}
        for s in range(n):
            nx, ny = {}, {}
            for x,m in xlaw.items():
                p = F(1+((s*13+x*7)%18),20)
                nx[x+1] = nx.get(x+1,F(0))+m*p
                nx[x-1] = nx.get(x-1,F(0))+m*(1-p)
            for y,m in ylaw.items():
                p = F(1+((s*13+(2*y-s)*7)%18),20)
                ny[y+1] = ny.get(y+1,F(0))+m*p
                ny[y] = ny.get(y,F(0))+m*(1-p)
            xlaw,ylaw=nx,ny
            check(sum(xlaw.values()) == sum(ylaw.values()) == 1)
            for x,m in xlaw.items():
                check((x+s+1)%2 == 0)
                check(m == ylaw[(x+s+1)//2])
    return dict(max_n=10,exact_rational=True)


def partition_control():
    # Full deterministic inequality used to avoid unwarranted M-uniformity.
    sites = range(-4,5)
    measures=[]
    for k in range(9):
        measures.append({x:F(1 if x==-4+k else 0) for x in sites})
    measures.append({x:F(x+5,45) for x in sites})
    for mu in measures:
        for alpha in measures:
            for m in (1,2,3,4):
                for M in (2,3,5,7):
                    for shift in range(M):
                        fine={};target={};splitmass=F(0)
                        for x in sites:
                            fine.setdefault(x//m,[]).append(x)
                            target.setdefault((x-shift)//M,[]).append(x)
                        Lfine=sum(abs(sum(mu[x]-alpha[x] for x in J)) for J in fine.values())
                        Ltarget=sum(abs(sum(mu[x]-alpha[x] for x in J)) for J in target.values())
                        for J in fine.values():
                            if len({(x-shift)//M for x in J})>1:
                                splitmass += sum(alpha[x] for x in J)
                        check(Ltarget <= Lfine+2*splitmass)
    return dict(exact_rational=True,measures=len(measures))


def overlap_coloring():
    # Explicit interval supports check finite-cone coloring and weighted variance.
    for n in range(1,31):
        for h in range(1,n+1):
            D=ceil((2*n+h)/h)+1
            cells=range(-7,8)
            cones={j:set(range(j*h-n,(j+1)*h+n)) for j in cells}
            for j in cells:
                for k in cells:
                    if j<k and (j-k)%D==0:
                        check(cones[j].isdisjoint(cones[k]))
    # Exact Young/convolution bound used in quasi-local concentration.
    for n in range(1,41):
        weights={x:F(comb(n,x),2**n) for x in range(n+1)}
        sq=sum(w*w for w in weights.values())
        for R in range(5):
            conv={z:sum(weights.get(x,F(0)) for x in range(z-R,z+R+1)) for z in range(-R,n+R+1)}
            check(sum(w*w for w in conv.values()) <= (2*R+1)**2*sq)
    return dict(max_segment=30,convolution_max_n=40)


def funnel_control():
    records=[]
    for r in [F(1,9),F(2,7),F(4,9)]:
        d=1-2*r
        ratio=r/(1-r)
        pi0=(1-ratio)/2
        def right(x): return 1-r if x<=0 else r
        # Backward recursion of the exact endpoint-zero kernel, no truncation.
        law={0:F(1)}
        rows=[law]
        us=[F(1)]
        for t in range(1,49):
            law={x:right(x)*law.get(x+1,F(0))+(1-right(x))*law.get(x-1,F(0)) for x in range(-t,t+1)}
            rows.append(law);us.append(sum(law.values()))
        for t in range(49):
            rhs=1+d*sum(rows[s].get(0,F(0))+rows[s].get(1,F(0)) for s in range(t))
            check(us[t] == rhs)
            check(us[t] >= 1+d*pi0*ceil(t/2))
            check(sum(v for x,v in rows[t].items() if (x-t)%2==0) == us[t])
            if t%2==0:check(rows[t].get(0,F(0)) >= pi0)
        records.append(dict(r=str(r),u48=str(us[48]),lower48=str(1+d*pi0*24)))
    return records


def negative_controls():
    # Same-parity shift vanishes at large scales; adjacent original shift does not.
    for n in range(1,31):
        b={2*j-n:F(comb(n,j),2**n) for j in range(n+1)}
        adj=sum(abs(b.get(x,F(0))-b.get(x-1,F(0))) for x in range(-n-2,n+3))
        check(adj == 2)
        same=sum(abs(b.get(x,F(0))-b.get(x-2,F(0))) for x in range(-n-2,n+3))
        check(same == 2*max(b.values()))
    # A.S./L2 information is compatible with a fixed polynomial failure tail.
    for n in range(2,100):
        prob=F(1,n*n)
        check(prob > F(1,n**3))
    return dict(parity_max_n=30,rate_counterexample=True)


def main():
    receipt=dict(created_utc=datetime.now(timezone.utc).isoformat(),manifest_validation=manifests(),exact_margins=exact_margins(),shear=shear_control(),partition=partition_control(),coloring_and_convolution=overlap_coloring(),funnel=funnel_control(),negative_controls=negative_controls())
    receipt.update(status='PASS',exact_assertions=count,scope='finite identities and artifact integrity only; no novelty certificate')
    (HERE/'INDEPENDENT_CONTROLS_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
