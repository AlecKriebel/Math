# Exact-byte hostile audit of the raw SS-446 composition

**Independent proof-first audit, 2026-08-12 PDT.**  This audit freezes the
exact theorem/certificate/test triple

```text
research_notes/proof_first_raw_ss446_invariant_dz_service_composition.md
SHA-256 c5283bfcb9cafb5eaea97e3287e6fdbc2c52ac19ea201651db6f26ab242553d7
216 lines, 8497 bytes

src/raw_ss446_composition_certificate.py
SHA-256 7376b9fd3913145d7ff806c6622db0aad9a8f5ffb1be413cfde108c16fa7eaf2
220 lines, 7058 bytes

tests/test_raw_ss446_composition_certificate.py
SHA-256 d212e126d113600179c37c3e16648d2485b4b3fbfda336c99cb0e4e34821f49a
71 lines, 2313 bytes
```

The verdict is **STRICT PASS** at these exact bytes.  The finite certificate
proves only the support--workload identity; the arbitrary-orientation and
arbitrary-rate conclusions are analytic.

## 1. Exact set replay

The audit independently replayed the ordered Q/U/C/S classifier on every
ordered disjoint pair of nontrivial supports for the four frozen workloads.
The SS output has 446 incidences on 322 distinct ordered support pairs.

Applying the theorem's disjoint priority gives

\[
\begin{array}{c|r|r}
\text{branch}&\text{incidences}&\text{pairs}\\ \hline
q_A,q_B,q_C>0&18&18\\
q_A,q_B>0\text{ only}&364&268\\
\delta=0&60&32\\
\text{literal service}&4&4.
\end{array}
\]

The sum is 446 and the residual count is zero.  The canonical raw and
branch-annotated fingerprints replay as

```text
842920b5280d96c96e49e0b0b959d548acb2ac43a5dfee4ab110346958acc45f
8870e74f85a50608b2f5586c87a3dc73cf825ae292df41063b77ebae7e1924e3
```

The four service rows are exactly the two support pairs

\[
 \{C,2C\}\ \&\ \{0,A,2A,B+C\},\qquad
 \{0,C,2C\}\ \&\ \{A,2A,B+C\},
\]

with both linkage orders, all at workload $(1,3,0)$.  No superset predicate
enters the certificate.

## 2. Invariant branches

The invariant predicates compute the common orthogonal complement of all
within-linkage support differences.  Hence every selected $q$ annihilates
every possible physical reaction displacement, for every orientation and
rate vector.

When all three coefficients are positive, a fixed nonnegative-integer level
set of $q\cdot x$ is finite.  When only $q_A,q_B$ are required positive, the
bounded $C$ phase keeps $q_CC$ bounded while
$q_AA+q_BB\to\infty$.  This contradicts the fixed-class invariant on a
two-active escape.  The theorem correctly labels this second conclusion as a
chart exclusion, not a global proper-potential theorem.

## 3. Deficiency-zero branch and nonexplosion

Two strongly connected linkage graphs form a weakly reversible reduced
network.  Full deficiency zero therefore gives a positive complex-balanced
vector for every positive rate vector.  The class-restricted product form is
summable because its normalizing mass is bounded by
$\exp(c_A+c_B+c_C)$.

The target also supplies an independent binary nonexplosion proof.  A
molecularity-two source cannot increase total population because every
binary target also has molecularity at most two.  Every positive total-count
jump consequently has constant or linear propensity, and bounded size, so a
linear pure-birth comparison applies.  Neutral quadratic clocks do not
invalidate this Lyapunov comparison: total-count sublevel sets are finite and
each state's total hazard is finite.

Thus an irreducible class has a normalizable invariant probability and is
nonexplosive, which gives positive recurrence.  The primary-literature audit
pin in the theorem separately verifies the deterministic deficiency-zero,
stochastic product-form, and complex-balanced nonexplosion citations.

## 4. Literal signed-service handoff

The service predicate returns exactly the four rows above.  Each is a literal
case of the frozen signed-service theorem at SHA

```text
4ec0ae7007184f2c5bda82bd55df5707d2c3570c7fdf2683ad87b97f75930738
```

The independent physical-seam audit is frozen at

```text
e7e76b76cd1371f98d19da0a1f5362ab4a0696548fba62028b29ccd2950617c9
```

It passes precisely those displayed supports for every strongly connected
orientation and positive rate vector.  The SS theorem does not import the
signed theorem for a strict support superset.

## 5. Executable and render replay

The frozen test file produced

```text
Ran 5 tests in 0.465s
OK
```

The exact theorem bytes were rendered independently with Pandoc's
single-backslash TeX-math reader, both to MathJax HTML and through Tectonic to
PDF.  Tectonic produced zero stderr bytes.  The four-page letter-sized PDF
was checked page by page; all long hashes, tables, equations, and the theorem
block render without overflow or clipping.

## 6. Frozen verdict

**STRICT PASS** for the exact theorem/certificate/test triple above.  The
18/364/60/4 split is an exact exhaustive union, the first two branches are
literal invariants, deficiency zero is classwise and nonexplosive, and the
last four incidences use only the independently audited literal service
supports.
