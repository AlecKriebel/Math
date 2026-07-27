# Maximal violation without maximal global randomness

This package gives an exact counterexample to the maximal-randomness assertion
in Conjecture 2 of Perito, D'Avino, Jung, Mironowicz, Acín, and Augusiak for
their first augmented cyclic Bell family.

## Result

For every integer `d >= 4`, the package constructs order-`d` observables on
`C^d tensor C^d` and uses the maximally entangled state `Phi_d` with trivial
Eve. The strategy attains the exact maximum

```text
2*csc(pi/(2d)) + 1
```

but its designated `x=1,y=d` outputs obey

```text
G(AB|1,d,E)
  >= 1/d^2
     + 2*sin(pi/d)*sin(3*pi/d)/(d^2*(d-1))
  > 1/d^2.
```

Both one-party marginals are nevertheless uniform. The failure is in the
global joint distribution, not a local-output bias, and no adversarial side
information is needed.

At `d=4`, the exact table is

```text
p(a,b|1,4) = 1/32  when a+b is even,
             3/32  when a+b is odd.
```

Thus `G=3/32>1/16`, with strict gap `1/32`.

## Mathematical mechanism

Let `X|j>=|j+1 mod d>` and order the `d` roots
`z^d=(-1)^(d-1)` by a permutation `kappa`. The complete maximizing strategy
is the sparse weighted-shift family

```text
A0 = X
A1 = X*diag(z_{kappa_j})
V_y = X*diag((1+omega^y*z_{kappa_j})/abs(1+omega^y*z_{kappa_j}))
B_y = entrywise_conjugate(V_y)
B_d = X.
```

The weighted-shift power identity proves every order relation. The displayed
`V_y` are exactly the polar unitaries of `A0+omega^y*A1`, so the strategy
saturates the sharp Bell certificate term by term.

For

```text
kappa=(0,1,...,d-3,d-1,d-2),
```

the designated distribution has a nonzero second cyclic autocorrelation

```text
C_2=(z_{d-1}-z_{d-2})*(z_{d-3}-z_0),
|C_2|=4*sin(pi/d)*sin(3*pi/d).
```

Fourier inversion and Parseval give the explicit guessing gap.

## Verification

The exact finite verifier uses only Python's standard library:

```bash
python3 verify_exact.py
```

It reads `certificate.json`, reconstructs the sparse `d=4` observables, and
checks in `Q(zeta_16)=Q[x]/(x^8+1)`:

- unitarity and all fourth-order relations;
- all four exact factorizations and identification of their diagonal lengths
  as `2*cos(pi/8)` or `2*cos(3*pi/8)`, whose positivity is analytic;
- the original unaugmented and augmented Bell expressions;
- the full projector-derived probability table;
- an independent finite Fourier derivation;
- uniform local marginals; and
- `G=3/32>1/16`.

Secondary all-family tests require NumPy. The historical discovery search also
requires SciPy:

```bash
python3 -m pip install -r requirements.txt
PYTHON_BIN=python3 ./run_all.sh
python3 discovery_search.py --restarts 1
```

The discovery program is a nonconvex numerical search and is retained only as
a record of how the exact witness was found. It need not converge in every run
and is not used by `run_all.sh` or by any proof claim.

The regression suite checks the canonical family for `d=2,...,12`, the
nonuniform family for `d=4,...,12`, the polar factorizations, order relations,
Bell values, Fourier formula, uniform marginals, autocorrelation identity, and
the explicit lower bound. These finite checks support the analytic proof; they
are not an all-dimensional formal verification.

## Files

- `manuscript.tex` / `manuscript.pdf` — complete analytic note.
- `certificate.json` — compact sparse exact `d=4` certificate.
- `verify_exact.py` — independent exact-arithmetic verifier.
- `generate_certificate.py` — regenerates the JSON without importing the
  verifier.
- `family_certificate.json` — machine-readable all-dimensional formulas.
- `cycle_family.py` — transparent numerical constructor and evaluator.
- `test_cases.py` — independent floating-point regressions.
- `discovery_search.py` — historical numerical falsifier; not part of the
  proof.
- `claims_ledger.md`, `assumptions_ledger.md`,
  `failed_approaches.md`, `prior_art_audit.md` — scope and audit records.
- `RESEARCH_LOG.md` — dated derivation and release log.
- `MANIFEST.sha256` — release integrity hashes.

## Additional structural result

The manuscript appendix proves that every finite-dimensional exact maximizer
of the *augmented* functional has, on Alice's state-supported space, equal
multiplicities for all `d` eigenvalues of `A0^dagger*A1` allowed by the scalar
equality condition. Therefore `d` divides that supported dimension. The proof
uses a support-range argument for singular polar factors and a
reflection-product rank lemma. It does not classify all maximizers or imply a
Weyl representation.

## Open questions

This package does not determine:

- maximal-violation randomness for `d=2,3`;
- the complete maximizing face;
- the worst guessing probability among all exact maximizers; or
- robustness relative to that correct worst-case baseline.

## Status and disclosure

This is an unrefereed, AI-assisted research artifact by Alec Kriebel, with
heavy assistance from ChatGPT 5.6 Sol. Alec Kriebel cannot independently
validate the mathematical claims. No originating author or outside researcher
was contacted. Independent expert review is required.
