#!/usr/bin/env python3
"""Untrusted exact witness discovery; only the generated Lean proofs certify answers.
Reconstructs Appendix A.12-A.16 directly, without importing the old verifier.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
from flint import fmpq, fmpq_mat
import argparse
ROOT=Path(__file__).resolve().parents[1]
def q(x):
    x=F(str(x)); return f'({x.numerator} / {x.denominator} : ℚ)'
def compute(N):
    d=[F(0)]*(N+1); c=F(2**N-1,N*2**(N-1))
    for k in range(1,N): d[k]=((k-1)*d[k-1]+2*N*(F(1,k)-c))/(N-k)
    assert (N-1)*d[N-1]+2*N*(F(1,N)-c)==0
    size=2*N-3; K=[[F(0) for _ in range(size)] for _ in range(size)]
    a=lambda k:k-1; b=lambda k:N+k-3
    for k in range(1,N):
        K[a(k)][a(k)]=F(k,2*N)
        if k+1<N:
            K[a(k)][a(k+1)]=F(N-k-1,2*N)
            K[a(k)][b(k+1)]=-F(1,N)
    for k in range(2,N):
        K[b(k)][a(k-1)]=F(k-1,2*k*N)
        K[b(k)][a(k)]=F(N-k,2*k*N)
        K[b(k)][b(k)]=F(N*(k-2)+k,2*k*N)
        if k>2: K[b(k)][b(k-1)]=F((k-1)*(k-2),2*k*N)
        if k+1<N: K[b(k)][b(k+1)]=F(N-k-2,2*N)
    s=[d[k]/2 for k in range(1,N)]+[d[k-1]/(2*k) for k in range(2,N)]
    g=[F(comb(N-2,k-1),2**(N-1)*(N+1)) for k in range(1,N)]+[-F(comb(N-3,k-2),2**(N-2)*(N+1)) for k in range(2,N)]
    cast=lambda x:fmpq(x.numerator,x.denominator)
    M=fmpq_mat([[cast(F(int(i==j))-K[i][j]) for j in range(size)] for i in range(size)])
    x=M.solve(fmpq_mat([[cast(x)] for x in s])); v=[F(str(x[i,0])) for i in range(size)]
    value=sum((g[i]*v[i] for i in range(size)),F(0))
    return d,v,value

def generate(N):
    d,v,value=compute(N)
    lines=['import SymmetricSector.Definitions','import SymmetricSector.Phase','import SymmetricSector.RowBounds','', 'open SymmetricSector.Phase', '', 'set_option maxRecDepth 2048', 'set_option maxHeartbeats 0', '',f'namespace SymmetricSector.Cert{N}','']
    if N > 3: lines.insert(0, f'import SymmetricSector.Small{N-1:02}')
    for k in range(1,N):
        lines += [f'theorem d_{k} : gradient {N} {k} = {q(d[k])} := by', '  rw [gradient]', '  norm_num only [show '+str(k)+' < '+str(N)+' by decide, if_true]', ('  rw [gradient]' if k==1 else f'  rw [d_{k-1}]'), '  norm_num [c₀]', '']
    lines += [f'theorem terminal_gradient : ({N-1} : ℚ) * gradient {N} {N-1} + 2*{N}*(1/{N} - c₀ {N}) = 0 := by', f'  rw [d_{N-1}]', '  norm_num [c₀]', '']
    lines += [f'def response : Channel {N} → ℚ', '  | .inl i => !['+', '.join(q(x) for x in v[:N-1])+'] i', '  | .inr i => !['+', '.join(q(x) for x in v[N-1:])+'] i','']
    lines += [f'theorem equations : (1 - coefficientK {N}).mulVec response = source {N} := by', '  apply funext', '  decide +kernel', '']
    lines += [f'theorem value : reducedScalar {N} = {q(value)} := by', '  unfold reducedScalar', '  rw [← witness_eq_inverse_mulVec (1 - coefficientK '+str(N)+')', '    (coefficient_system_isUnit '+str(N)+' (by norm_num))', '    (source '+str(N)+') response equations]', '  decide +kernel', '',f'theorem positive : 0 < reducedScalar {N} := by rw [value]; norm_num','',f'end SymmetricSector.Cert{N}','']
    (ROOT/'SymmetricSector'/f'Small{N:02}.lean').write_text('\n'.join(lines))
    return value
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--start',type=int,default=3);p.add_argument('--end',type=int,default=39);args=p.parse_args()
    for N in range(args.start,args.end+1):
        val=generate(N);print(N,val)
