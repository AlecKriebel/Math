# Independent arithmetic and analytic-tail audit

Date: 2026-09-14 UTC. Responsibility: inspect Appendix A finite certificates,
indexing, boundary inequalities, and infinite analytic tail independently of
prior reviews. Initial findings below were obtained before implementing the
replacement Lean proofs. No external communication or release was performed.

## Source and statement audit

The symmetric source uses `N = n - 1`; a ranks are `1,...,N-1`, b ranks are
`2,...,N-1`. The physical scalar is the bilinear pairing
`gᵀ (I-K)⁻¹ s`, with the negative b reward retained. The first exact interval
has 37 orders, `3 ≤ N ≤ 39`; the phase interval has 248 orders,
`40 ≤ N ≤ 287`. The maximum defining beta includes exactly
`1 ≤ j ≤ N-2`, not the top a rank. Omitting the negative reward or confusing
K with its transpose would change the problem.

An independent rational reconstruction gives:

- `N=3`: determinant `det(I-K)=13/27`; solution
  `(69/104, 9/16, 207/416)`; scalar `3/208`.
- `N=4`: determinant `det(I-K)=6665/24576`; solution
  `(1072/1333,4139/7998,7/15,2144/3999,2316/6665)`;
  scalar `359/26660`.
- Direct Python `Fraction` evaluation of every finite beta term for all 248
  orders reproduces strict positivity of all margins. The exact minimum is
  `639304267467075678841/115369588296792467144716`, at `N=40`;
  the maximizing rank there is `j=20`, with
  `beta=16571794416619567125/17686584132575880292` and
  `epsilon=375/6523`.

These independent arithmetic checks are corroboration, not Lean proofs.
The original complete verifier could not run in the root `.venv` because
`python-flint` is absent there; its solver output was not treated as an axiom.

## Simpler exact certificates discovered

The discriminant-only verifier checks correct identities but does not itself
implement the real-root implication used in the prose. That implication is
mathematically valid for these cubics (positive leading coefficient, negative
cubic discriminant, positive value at zero), but would add unnecessary Lean
root-counting infrastructure. The following exact alternatives directly
establish the domain inequalities.

For the actual polynomial `G` in (A.34),

```
24000 G(N,j) = j(12000j-6250N)^2
  + Nj(6081500N-510672000)
  + N(45144000N-240768000)
  + 288000000j^2 + 240768000j + 300960000.
```

Every nonconstant term is nonnegative for `N≥84`, `j≥0`; thus `G>0` on
an even larger domain than the required `N≥288`.

For `P` in (A.23), put `x=k/N`, `m=N-25`,
`f=50x³-64x²+21x`, and `g=36x²-57x+14`. Then

```
P(N,k)/N = m² f + m(50f+g) + (625f+25g-14x),
f = x(50(x-16/25)^2+13/25),
50f+g = 2500x(x-16/25)^2 + ((72x-31)^2+1055)/144,
625f+25g-14x = 31250x(x-16/25)^2 + ((900x-557)^2+4751)/900.
```

This proves `P>0` for `N≥25`, `k≥0`. The special physical interval at
`N=24` remains an exact finite check.

The square-root radial argument can also be replaced. The rational
subsolution `24N/(25N-24k)` has the exact cleared recurrence residual
`2N²(25N-24k-276)`, nonnegative for `N≥288`, `k≤N-1`.
Its base comparison has residual `2N(N-12)>0`. These formulas avoid
formalizing square-root approximations while proving the same required bound.

## Matrix and boundary findings

Every full interior Q row already has positive deficit:

```
1 - (Q[k,k-1]+Q[k,k]+Q[k,k+1])
  = (Nk+N+k²)/(Nk(k+1)) = 1/k + k/(N(k+1)) ≥ 1/N.
```

Deleting absent boundary entries only increases the deficit. Therefore the
uniform estimate `Q·1 ≤ (1-1/N)·1` is available; graph reachability of strict
boundary rows is unnecessary to establish inverse positivity.

The left supersolution Y boundary formulas in (A.29) presuppose distinct
endpoints (`N≥4`). At `N=3` both bad endpoints are the single rank `k=2`;
the actual residual is `1/3`, while the separately printed endpoint formulas
are different. This is not a gap in the large-order argument, which applies
them only well above this exceptional order, but general Lean statements must
not assert those endpoint equalities at `N=3`. Similarly the h-hat boundary
formulas must respect overlapping boundaries. The symmetric-balanced sector
at population `n=3` (`N=2`) is absent; it must not be assigned an artificial
positive scalar by extrapolating expressions containing `N-2` in denominators.

## Remaining mathematical/formalization obligations

No counterexample or central mathematical gap in the symmetric phase argument
was found in this audit. This is not a claim that the whole proof is verified.
The finite and infinite phase inequalities must be connected to actual block
systems through nonnegative inverse bounds, source gradient bounds, all
boundary rows, and Schur elimination. The quotient must then be linked to the
actual active-chain perturbation quadratic form for every population size.
Neither finite numerical checks nor these polynomial certificates alone prove
those identifications. The independent translation reviewer owns the latter
review.

Implementation status and final theorem/axiom output are recorded by the
parent research log; the exact Lean artifacts accompanying this audit are
`SymmetricSector/Analytic.lean` and `SymmetricSector/AnalyticTail.lean`.
