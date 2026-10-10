#!/usr/bin/env python3
"""Independent audit controls; not a continuum or literature-completeness certificate."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import subprocess
import sys

BASE = Path(__file__).resolve().parent.parent
PUB = BASE / 'public'
EXPECTED_MANIFEST = '337e5c6e1e319556d4ce3148a4fe9f6e3ceef6d6bcc3b07a9632296ec638942c'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def frozen():
    assert sha(PUB / 'SHA256SUMS') == EXPECTED_MANIFEST
    answer = {}
    for line in (PUB / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        assert sha(PUB / name) == digest
        answer[name] = digest
    return answer

def radial():
    # Derive the candidate as the harmonic majorant minus a triangular penalty,
    # rather than using the author's piecewise formula as the implementation.
    checks, regimes = 0, {'easy': 0, 'positive_knot': 0, 'empty': 0}
    As = [F(-3), F(-2), F(-1), F(-1,2), F(0), F(1,2), F(1)]
    Bs = [F(-3), F(-1), F(-1,2), F(0), F(1,3), F(1), F(2), F(4)]
    for A in As:
        for B in Bs:
            for k in range(1,12):
                s = F(k,12)
                if A > 0:
                    regimes['empty'] += 1
                    continue
                knot = A + (B-A)*s
                if knot <= 0:
                    regimes['easy'] += 1
                    left = right = B-A
                else:
                    regimes['positive_knot'] += 1
                    left, right = -A/s, B/(1-s)
                    assert right-left == knot/(s*(1-s)) > 0
                for x in sorted(set([F(j,24) for j in range(25)] + [s])):
                    h = A + (B-A)*x
                    p = max(knot,F(0))*min(x/s,(1-x)/(1-s))
                    f = h-p
                    assert f <= h
                    assert f == (A + left*x if x <= s else B-right*(1-x))
                    if x <= s:
                        assert f <= 0
                    if x == s:
                        assert f == min(knot,F(0))
                    if x == 0:
                        assert f == A
                    if x == 1:
                        assert f == B
                    checks += 1
    return {'parameter_regimes': regimes, 'exact_point_checks': checks}

def graph():
    # Assemble through undirected edge energies and solve with exact LDL^T,
    # independently of the author's neighborwise Gauss-Jordan implementation.
    nx,ny=4,8
    allnodes=[(i,j) for i in range(nx+1) for j in range(ny)]
    fixed={(0,j):F(0) for j in range(ny)} | {(nx,j):F(1) for j in range(ny)}
    fixed.update({(1,0):F(0),(2,0):F(0)})
    free=[p for p in allnodes if p not in fixed]
    idx={p:k for k,p in enumerate(free)}
    n=len(free)
    M=[[F(0) for _ in free] for _ in free]
    b=[F(0) for _ in free]
    edges=[((i,j),(i+1,j),F(16)) for i in range(nx) for j in range(ny)]
    edges += [((i,j),(i,(j+1)%ny),F(64)) for i in range(1,nx) for j in range(ny)]
    for p,q,w in edges:
        for a,c in [(p,q),(q,p)]:
            if a not in idx:
                continue
            k=idx[a]
            M[k][k]+=w
            if c in idx:
                M[k][idx[c]]-=w
            else:
                b[k]+=w*fixed[c]
    L=[[F(int(i==j)) for j in range(n)] for i in range(n)]
    d=[F(0)]*n
    for i in range(n):
        d[i]=M[i][i]-sum(L[i][k]**2*d[k] for k in range(i))
        assert d[i]>0
        for j in range(i+1,n):
            L[j][i]=(M[j][i]-sum(L[j][k]*L[i][k]*d[k] for k in range(i)))/d[i]
    y=[F(0)]*n
    for i in range(n):
        y[i]=b[i]-sum(L[i][j]*y[j] for j in range(i))
    z=[y[i]/d[i] for i in range(n)]
    x=[F(0)]*n
    for i in reversed(range(n)):
        x[i]=z[i]-sum(L[j][i]*x[j] for j in range(i+1,n))
    assert all(sum(M[i][j]*x[j] for j in range(n))==b[i] for i in range(n))
    values=fixed | dict(zip(free,x))
    for (i,j),v in values.items():
        assert max(F(0),F(2*i,nx)-1)<=v<=F(i,nx)
        assert v==values[(i,(-j)%ny)]
        if (i,j) in idx:
            assert 0<v<1
    for i,j in [(1,0),(2,0)]:
        lap=16*(values[(i-1,j)]+values[(i+1,j)]-2*values[(i,j)])
        lap+=64*(values[(i,(j-1)%ny)]+values[(i,(j+1)%ny)]-2*values[(i,j)])
        assert lap>0
    target=values[(1,4)]
    assert target==F(54206789,412704788)
    raw=json.dumps({f'{i},{j}':str(values[(i,j)]) for i,j in sorted(values)},sort_keys=True).encode()
    return {'unknowns':n,'method':'edge-energy assembly, exact LDL^T',
            'positive_pivots':n,'exact_residuals':'zero','target':str(target),
            'value_vector_sha256':hashlib.sha256(raw).hexdigest()}

def one_dimensional():
    # This is an audit of the scalar integral appearing in the proof, not an
    # audit of arbitrary Green kernels or a substitute for the analytic proof.
    def plogp(p):
        return 0.0 if p==0 else p*math.log(p)
    count=0
    for delta in [1e-6,0.125,1.0,3.0]:
        maxval=1+math.log(2/delta)
        for i in range(1601):
            q=i/200
            integral = (1-math.log(delta)-plogp(q)-plogp(1-q)
                        if q<=1 else 1-math.log(delta)+plogp(q-1)-plogp(q))
            assert integral<=maxval+1e-12
            if q==0.5:
                assert abs(integral-maxval)<1e-12
            count+=1
    intervals=0
    for a in [F(i,20) for i in range(61)]:
        for e in [F(i,100) for i in range(101)]:
            length=max(F(0),min(F(1),a+e)-max(F(0),a-e))
            assert length<=min(F(1),2*e)
            intervals+=1
    return {'log_integral_diagnostic_points':count,
            'exact_radial_interval_mass_checks':intervals,
            'scope':'scalar controls only; arbitrary-path theorem checked analytically'}

def main():
    before=frozen()
    completed=subprocess.run([sys.executable,str(PUB/'verify.py')],cwd=PUB,
                             text=True,capture_output=True,check=True)
    original=json.loads(completed.stdout)
    saved=json.loads((PUB/'verification.json').read_text())
    assert original==saved
    report={'status':'passed','frozen_manifest_sha256':EXPECTED_MANIFEST,
            'original_replay':original,
            'independent_radial':radial(),
            'independent_graph':graph(),
            'independent_scalar_controls':one_dimensional()}
    assert frozen()==before
    report['frozen_files_unchanged']=True
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
