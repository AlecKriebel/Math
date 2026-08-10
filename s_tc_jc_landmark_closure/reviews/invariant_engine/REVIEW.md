# Adversarial clean-room review of the primary JC invariant engine

## Final verdict

**VERIFIED.** The current primary JC invariant engine passed this review after
two previously identified implementation corrections: restoration of
all-outgoing ordered quartet probes and the explicit `+1` transport of the
seventh invariant from its 14-nontrivial-coordinate convention to the current
15-coordinate convention.

No unresolved mathematical defect was found in the reviewed Fourier indexing,
quartet-deck generation, invariant transport, sparse pullback expansion,
modular prefilter, factor/Bernstein sign prover, descriptor zipping, or
reticulation-choice symmetry.

This is deliberately **not** a verdict on the completeness of any finite
topology atlas. It does not prove generator exhaustiveness, relation coverage,
bounded-support promotion, root reduction, probe coherence, or the global
strong-tree-child identifiability theorem. Those claims remain **UNRESOLVED by
this review** and require their own gates.

## Independence boundary

The expected mathematics is implemented from scratch in
`cleanroom_engine.py`. It imports no code from `primary/`, no historical
Fourier engine, no graph canonicalizer, and no historical invariant evaluator.
The six historical invariant templates and the seventh JSON table are parsed
only as inert integer coefficients.

`run_review.py` first derives the expected coordinates, invariant orbit,
pullbacks, and sign proofs. It then loads the current primary modules strictly
as the system under test. Every compared pullback is regenerated from its
descriptor; no cached topology identifier or historical polynomial is accepted
as evidence.

## 1. Four-port JC coordinates

**VERIFIED.** Starting with

\[
G=(\mathbb Z/2\mathbb Z)^2=\{0,1,2,3\},
\]

the reviewer enumerates the 64 assignments
\((g_1,g_2,g_3,g_4)\) with XOR sum zero, then quotients by all six
permutations of the three nonzero characters. There are exactly 15 orbits. In
the primary lexicographic convention they are

```text
 0  (0,0,0,0)
 1  (0,0,1,1)
 2  (0,1,0,1)
 3  (0,1,1,0)
 4  (0,1,2,3)
 5  (1,0,0,1)
 6  (1,0,1,0)
 7  (1,0,2,3)
 8  (1,1,0,0)
 9  (1,1,1,1)
10  (1,1,2,2)
11  (1,2,0,3)
12  (1,2,1,2)
13  (1,2,2,1)
14  (1,2,3,0)
```

The independently derived ordered list agrees exactly with
`primary/jc_tensor.py`. Coordinate 0 is the trivial Fourier coordinate. The
historical seventh table indexes only the remaining 14 entries, so historical
index \(i\) maps to current index \(i+1\). This is a convention identity, not
an empirical guess.

## 2. Complete ordered quartet deck

**VERIFIED.** For \(m\) boundary ports, `all_port_quartet_deck` returns every
ordered injection of four slots into the boundary set, hence

\[
P(m,4)=m(m-1)(m-2)(m-3)
\]

keys. Independent synthetic raw descriptors with zero, one, and two
reticulations agreed exactly with the primary output for \(m=4,5,6,7\).

**FALSE.** The withdrawn incoming-fixed deck is not complete. At five ports it
contains 96 of the 120 ordered restrictions and omits the 24 permutations of
the all-outgoing quartet. The current implementation restores all 24. The
mandatory deletion mutation is therefore rejected by exact key coverage.

## 3. Seventh transport, invariant orbit, and bridge-arm gauge

**VERIFIED.** After the required `+1` transport, the six inert historical
templates and the seventh template generate exactly 84 distinct invariants
under all leaf permutations and JC colour canonicalization. The independently
generated normalized orbit agrees byte-for-byte with the primary orbit; its
normalized SHA-256 is

```text
5f8f73dee3faf5eac0e81d4922ef63cfe16fa4ec7d3ca1204f6a77d3e15f3f26
```

Every monomial in each invariant has the same four-port arm multidegree.
Consequently multiplication of a port arm by a positive incidence scale
multiplies the whole invariant by one positive monomial, preserving zero status
and strict sign. The trinet invariant

\[
F=abc-t^2
\]

has arm multidegree \((2,2,2,0)\), so it has the same projective property.

**FALSE.** Omitting the `+1` shift leaves 24 of the 84 orbit elements
non-multihomogeneous. That mutation is rejected.

## 4. Exact sparse pullbacks and modular prefilter

**VERIFIED.** The clean-room engine independently expands each displayed-tree
mixture over \(\mathbb Z\), including every inheritance factor \(\lambda\) or
\(1-\lambda\), and independently multiplies sparse coordinate polynomials.

The exhaustive small descriptor universe has 310 canonical descriptors:

- 121 reticulation-free descriptors containing at most two distinct nonzero
  masks;
- all 135 one-row one-reticulation descriptors over all four-port masks,
  modulo choice flip;
- all 54 one-row two-reticulation descriptors over displayed masks
  \(\{0,1,2,3\}\), modulo reticulation permutations and flips.

An additional 64 descriptors with up to two reticulations and six edge rows
were generated from a fixed adversarial seed. Across these 374 descriptors,
all 31,416 invariant pullbacks from `pullbacks_shared` agree exactly with the
independent sparse engine. A further 132 comparisons show agreement between
the primary shared and standalone pullback paths.

For the three production modular seeds, 18,432 nonzero residues were checked.
A nonzero residue is sound because the zero integer polynomial maps to zero
under every modular evaluation. Modular zero is never accepted as an identity:
75,816 zero events were observed, and 32 representative descriptors were
checked end-to-end against exact bit decks. When every modular coordinate was
forcibly replaced by zero, the primary routine still recovered the complete
nonzero bit deck by exact fallback. The mutation that trusts modular zero is
therefore rejected.

## 5. Factor/Bernstein strict-sign certificates

**VERIFIED.** For a polynomial factor \(f\) of multidegree
\((d_1,\ldots,d_k)\), the independent prover converts the power coefficients
\(a_j\) to tensor-product Bernstein coefficients using

\[
b_i=\sum_{j\le i}a_j
\prod_{r=1}^k\frac{\binom{i_r}{j_r}}{\binom{d_r}{j_r}}.
\]

Every Bernstein basis function is strictly positive on the open cube. Thus
nonnegative coefficients with at least one positive coefficient prove
\(f>0\) there; the analogous nonpositive condition proves \(f<0\). Exact
factor multiplicities then determine the product sign. Every factorization was
multiplied back exactly.

The audit compared not only the final sign but every primary proof field:
factor multiplicity, used variables, degree elevation, coefficient count, and
exact minimum and maximum Bernstein coefficients. Seven adversarial hand
polynomials behaved correctly, including the uncertified sign-changing
polynomial \(x-y\). Of 80 regenerated invariant pullbacks, 73 received matching
strict certificates and seven were correctly left uncertified by this
sufficient method.

The domain is strictly the open unit cube. In particular,
\(x(1-x)>0\) on \((0,1)\) but vanishes at both endpoints; the mutation changing
the claim to the closed cube is rejected. Pullbacks contain integer
coefficients and nonnegative exponents only, so this engine introduces no
denominators.

The exact-polynomial hash is sign-sensitive. The primitive-polynomial hash is
intentionally sign-insensitive, so it cannot carry sign by itself. Both primary
sign libraries are keyed by the exact-polynomial hash and store the strict sign
separately. The verifier also regenerates the polynomial before checking the
hash; a valid proof attached to a different descriptor is rejected.

## 6. Descriptor zipping and reticulation-choice symmetries

**VERIFIED.** If \(k\) edges have the same complete displayed-mask row, every
Fourier monomial either contains all \(k\) edge multipliers or none. They enter
only as the effective product

\[
z=x_1\cdots x_k.
\]

For \(0<x_i<1\), also \(0<z<1\); conversely every \(z\in(0,1)\) has an open
positive factorization, for example \(x_i=z^{1/k}\). Forty-five exact
coordinate checks confirm the symbolic product substitution for zero, one,
and two reticulations.

Reticulation permutations merely permute inheritance variables. Flipping one
displayed-parent bit sends \(\lambda\mapsto1-\lambda\), an analytic involution
of \((0,1)\). All ten permutations/flips for the one- and two-reticulation
fixtures preserve every exact coordinate. The primary and independent row
canonicalizers also agree on 128 adversarial raw descriptors.

## 7. Mutation ledger

All eight required mutations were rejected:

| Mutation | Status | Exact detector |
|---|---|---|
| Remove all-outgoing quartets | **FALSE** | Five-port key set loses 24 of 120 entries |
| Omit seventh `+1` transport | **FALSE** | 24 orbit elements lose arm multihomogeneity |
| Trust modular zero | **FALSE** | Forced-zero modular deck disagrees with exact fallback |
| Swap invariant coordinate indices | **FALSE** | Global swap changes orbit size from 84 to 102 |
| Corrupt one coefficient | **FALSE** | Regenerated orbit and pullback bindings change |
| Replace open cube by closed cube | **FALSE** | \(x(1-x)\) vanishes on the boundary |
| Reuse a proof on the wrong descriptor | **FALSE** | Regenerated exact polynomial hashes disagree |
| Reverse a strict sign | **FALSE** | Exact Bernstein proof and rational interior evaluation disagree |

The first draft of the coordinate-swap mutation changed only one sorted
monomial containing both swapped indices and was therefore a no-op. The run
failed closed rather than reporting success. This review-harness failure is
preserved in `failure_log.json`; the corrected mutation is global and genuinely
changes the orbit.

## 8. Preserved replay failure

**FALSE.** The claim that the shell's default Python can replay the complete
review is false in the present environment. The first run reached the sign gate
and stopped because Homebrew Python 3.14.6 did not provide SymPy. The exact
traceback is preserved in `python314_environment_failure.txt`.

The deterministic command is pinned to Homebrew Python 3.11, with SymPy
1.14.0:

```bash
bash s_tc_jc_landmark_closure/reviews/invariant_engine/verify_all.sh
```

## 9. Status ledger and scope limit

| Claim | Status |
|---|---|
| Current 15-coordinate JC indexing | **VERIFIED** |
| Current complete ordered quartet deck | **VERIFIED** |
| Historical incoming-fixed deck is sufficient | **FALSE** |
| Explicit seventh-invariant `+1` transport | **VERIFIED** |
| Unshifted seventh table is valid in the current engine | **FALSE** |
| Current 84-element orbit is arm-multihomogeneous | **VERIFIED** |
| Current exact sparse pullbacks | **VERIFIED** |
| Current modular nonzero/fallback logic | **VERIFIED** |
| Current factor/Bernstein open-cube sign prover | **VERIFIED** |
| Current descriptor zipping and reticulation symmetries | **VERIFIED** |
| Finite decorated-atlas exhaustiveness | **UNRESOLVED** |
| Completeness of local separators for all topology relations | **UNRESOLVED** |
| Bounded-support promotion and probe coherence | **UNRESOLVED** |
| Global standard-strong JC identifiability modulo `T` | **UNRESOLVED** |

The final adversarial verdict is therefore narrow and affirmative: the
**current invariant engine is exact for the reviewed contracts**, but it cannot
by itself promote the landmark topology theorem.
