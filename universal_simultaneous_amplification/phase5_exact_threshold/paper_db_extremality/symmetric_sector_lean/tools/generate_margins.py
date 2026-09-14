#!/usr/bin/env python3
"""Generate floor-grid witnesses; Lean checks recurrence and inequalities.
The generator's assertions are diagnostic only and are not in the trust path.
"""
from pathlib import Path
SCALE=10000
ROOT=Path(__file__).resolve().parents[1]
def witness(n):
    w=[0]
    for j in range(1,n):
        w.append((2*n*SCALE+(j-1)*w[-1])//(2*n-j))
    return w

def generate():
    directory=ROOT/'SymmetricSector'/'GeneratedMargins'
    directory.mkdir(exist_ok=True)
    previous='SymmetricSector.Margins'
    for n in range(40,288):
        margin='1 / 200' if n==40 else '1 / 100'
        text = f"""import {previous}

set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace SymmetricSector.GeneratedMargins

def w{n} : List ℕ := {witness(n)}

theorem cert{n} : MarginCertificate {n} w{n} ({margin}) := by decide +kernel

theorem bound{n} : beta {n} + epsilon {n} ≤ 1 - ({margin} : ℚ) :=
  beta_add_epsilon_le_of_certificate (by norm_num) cert{n}

end SymmetricSector.GeneratedMargins
"""
        (directory/f'Order{n:03d}.lean').write_text(text)
        previous=f'SymmetricSector.GeneratedMargins.Order{n:03d}'
    # A dependency chain is intentional: it bounds peak memory during a clean
    # build, releasing kernel-reduction caches between finite certificates.
    (directory/'All.lean').write_text(f'import {previous}\n')

if __name__=='__main__':
    generate()
