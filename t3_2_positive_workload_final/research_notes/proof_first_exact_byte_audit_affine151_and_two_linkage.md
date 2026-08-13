# Proof-first exact-byte audit: affine151 and the two-linkage interface

**Audit date:** 2026-08-12 PDT.  
**Method:** independent symbolic proof audit plus exact finite support/tier-set
identities.  No reaction orientation, stochastic trajectory, state-space, or
rate-parameter enumeration was used.

## 1. Frozen inputs

The dispositions below apply only to these exact bytes.

| audited input | SHA-256 |
|---|---|
| `research_notes/stoichiometric_gate_feasibility.md` | `27b40b61903ae6c2e223d007ec08323ec9aec10e9198deb99d2d7c60d878d007` |
| `research_notes/global_atlas_interface_closure.md` | `3b80734707dcac833621770c881da2be9782efc5658605179cd18e327a3c07d9` |
| `src/global_tier_interface.py` | `b8feae08c2eecf21b6e4e387eeaa6f5b15f32d862fca5324d4523c38872494ab` |

Read-only finite-set dependencies used to reproduce the tables were:

| dependency | SHA-256 |
|---|---|
| `src/global_atlas_interface_closure.py` | `293a63711f6da152edd72615d27fad5bbb859aa33a4b7eb150673b27ae3cb5bd` |
| `src/stoichiometric_gate_feasibility.py` | `4602e7d31af02c26cc9785ed056c876e3e571e428ad974e861e4940b9edba9a1` |

## 2. Hostile disposition

| claim in the frozen inputs | disposition | reason |
|---|---|---|
| Theorem 2.1, affine tier-feasibility | **PASS** | The levelwise Gordan alternative is necessary, and the polynomial flag construction is sufficient. |
| Corollary 4.1, mathematical affine151 recurrence branch | **PASS** | The legacy cut is conservative, so absence of every legacy-feasible failure implies absence of every genuine class-feasible failure. The same 151 pairs survive the corrected cut. |
| Corollary 4.1, publication citation | **FAIL** | It cites arXiv Theorem 4.2. The version of record is Anderson--Kim (2018), journal **Theorem 9**; arXiv v3 calls the same result Theorem 4.2. |
| `global_atlas_interface_closure.md` (8.9), claimed arbitrary-orientation **iff** using the global top D-tier | **FAIL** | The condition is sufficient but not necessary when the global top D-tier is wholly disabled and the top S-tier lies lower. |
| `global_tier_interface.py::universal_orientation_tier_condition`, as an exact iff test on every descriptor | **FAIL** | It implements the preceding sufficient-only global-top-D cut. |
| Completeness of the 259 finite D-order/availability descriptors | **PASS** | The rational arrangement represents every finite D-preorder and exact bounded-coordinate availability pattern. |
| The 1,219 positive and 159 signed tier-certified pair sets | **PASS** | Every legacy pass is a genuine pass under the exact cut; the corrected pair sets are byte-for-byte identical. |
| The post-tier residual \(2312+199=2511\) | **PASS** | Correcting the cut changes 208 incidences but no pair-level pass/fail decision. The residual fingerprints are unchanged. |
| The exact incidence totals \(12886/9913/2973\) | **FAIL** | They include 208 false failures. Exact corrected totals are \(12678/9709/2969\). |
| The affine151 pair set and its fingerprints | **PASS** | Removing the 208 false failures changes no pair's status under the affine filter. |

Thus neither frozen note is publication-ready as an exact certificate.  The
mathematical affine151 conclusion and the 2,511 residual remain sound, but the
cut theorem, incidence totals, and citation must be replaced by the corrected
derivative dependency.

## 3. Audit of Theorem 2.1

Let \(S\subseteq\mathbb R^3\) be rational, let \(w\ge0\), and, at each
positive coordinate level \(r\), put

\[
 E_r=\{i:w_i=r\},\qquad L_r=\{i:w_i<r\},\qquad
 W_r=S\cap\{v:v_i=0\ (i\in L_r)\}.
\]

The required direction is a vector of \(W_r\) whose coordinates in \(E_r\)
are all positive.  If it does not exist, Gordan's theorem gives
\(0\ne y\ge0\), supported on \(E_r\), that annihilates the projection of
\(W_r\) to \(E_r\).  Since

\[
 W_r^\perp=S^\perp+\operatorname{span}\{e_i:i\in L_r\},
\]

\(y\) extends to an invariant \(q\in S^\perp\) that is zero above level
\(r\), nonnegative and nonzero at level \(r\), and unrestricted below it.
On any sequence realizing the descriptor, division by a level-\(r\)
coordinate makes \(q\cdot x_n\) tend to a strictly positive scale, whereas
the affine identity makes it constant.  This proves necessity.

Conversely, choose rational feasible directions \(v_r\), rescale them to
integral directions, and take

\[
 x(n)=b+\sum_r n^r v_r.
\]

For a coordinate of weight \(r\), every higher-power coefficient vanishes,
the degree-\(r\) coefficient is positive, and lower powers are negligible.
Zero-weight coordinates remain at the cap-compatible base \(b\).  The
sequence is eventually nonnegative, lies in one affine class, and realizes
all monomial comparisons and availability caps.  This proves sufficiency.

The theorem is about real affine feasibility.  The recurrence application
uses only its necessary direction for actual integer tier sequences in a
closed class, so no unproved lattice-realizability converse is being used.

## 4. The exact symbolic cut and the defect in (8.9)

Fix a descriptor.  Let \(E\) be the global top S-tier.  All members of \(E\)
lie in one D-tier; denote its level by \(r\).  For a linkage support \(L\),
define the S-level D-superlevel

\[
 U_L=\{y\in L:y\text{ lies at or above D-level }r\}.
\]

Then every strongly connected directed graph on the linkage supports has a
D-descending reaction sourced in \(E\) if and only if

\[
 \boxed{\text{for some }L,\quad
 \varnothing\ne U_L\subsetneq L\quad\text{and}\quad U_L\subseteq E.}
 \tag{4.1}
\]

This is a theorem about an arbitrary strongly connected graph, not an
enumeration of orientations.

For sufficiency, strong connectivity forces an edge out of the nonempty
proper set \(U_L\).  Its source lies in \(U_L\subseteq E\), and its target is
below D-level \(r\), so the edge is descending.

For necessity, suppose (4.1) fails.  Treat each linkage independently.  If
\(U_L=\varnothing\) or \(U_L=L\), no forced E-sourced exit exists.  Otherwise
choose \(b\in U_L\setminus E\).  A directed Hamiltonian cycle ordered as

\[
 U_L\setminus\{b\},\quad b,\quad L\setminus U_L
\]

has \(b\to L\setminus U_L\) as its only exit from \(U_L\).  That exit is not
sourced in \(E\); every E-vertex has its successor inside \(U_L\), at the same
or a higher D-level.  Hence the cycle has no E-sourced descending edge.
The union of these linkagewise cycles is the required strongly connected
counterorientation.  This proves the converse symbolically.

The frozen (8.9) used \(K_L=L\cap G\), where \(G\) is only the **global top
D-tier**.  It agrees with (4.1) when \(E\subseteq G\), but not when all of
\(G\) is disabled.

An explicit residual witness is

\[
 L_1=\{C,2C\},\qquad
 L_2=\{A,2A,A+B,A+C\},\qquad
 w=(0,3,1),\quad c=(0,2,2).
\]

Here \(A=0\), the global top D-tier is the disabled singleton
\(G=\{A+B\}\), and the global top S-tier is \(E=\{2C\}\).  Every strongly
connected graph on \(L_1\) contains a path from \(2C\) to \(C\), whose first
edge leaving \(\{2C\}\) is descending and sourced in \(E\).  Thus the exact
criterion passes, while frozen (8.9) fails.

## 5. Finite identity consequences

Replacing the legacy cut by (4.1) gives:

| family | legacy failing incidences | corrected failing incidences | removed false failures | corrected feasible | corrected infeasible |
|---|---:|---:|---:|---:|---:|
| positive | 12,450 | 12,250 | 200 | 9,349 | 2,901 |
| signed | 436 | 428 | 8 | 360 | 68 |
| **total** | **12,886** | **12,678** | **208** | **9,709** | **2,969** |

Of the 208 removed incidences, 204 were affine-feasible and four were
affine-infeasible.  They occur on 186 pairs.  Nevertheless, every affected
pair has another genuine failed descriptor, and no affine151 decision
changes.

The pair-level identities are exactly:

| family | pre-tier | certified | residual | certified SHA-256 | residual SHA-256 |
|---|---:|---:|---:|---|---|
| positive | 3,531 | 1,219 | 2,312 | `744d872920309c361d6d7f806f140a696e3fc3ae0f75d760d8a07f304d562b6b` | `0297ba35311c757cd5c6ec548d2af18410dfd37e791c7679de932fe4bf38695b` |
| signed | 358 | 159 | 199 | `7f59ea94fe876205ccb72dc97b026b2954feac62375122634aafa318084428ee` | `1a9c06123645855d3b4f23d4886b0ada3c3ff3614fc94a7d22c01f411c1355c8` |

Hence the exact post-tier residual remains \(2312+199=2511\).

The affine filter remains:

| set | count | SHA-256 |
|---|---:|---|
| no affine-feasible corrected failure | 151 | `55e243945f86d106b920a27e2249a20b7077b5dc718ec06918cca4368e4a6c96` |
| positive part | 143 | `f48882aa1ff52c1594a71fd217fa559492c7010e950285a9fa2e60e02b487b76` |
| signed part | 8 | `aead73fd44d08789019326cffcd706a776addf0cbc841979a3d54e8c80c5f88d` |

## 6. Pre-tier classwise reductions

The support identities before the tier cut also pass audit.

| family | unique pairs | finite strict invariant | active-chart invariant | deficiency zero | exact seven-support only | exact signed-service only | exact residual pair only | pre-tier residual |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| positive | 4,761 | 187 | 110 | 924 | 6 | 2 | 1 | 3,531 |
| signed | 408 | 0 | 0 | 50 | 0 | 0 | 0 | 358 |

A strictly positive invariant makes each nonnegative integer class finite.
An invariant positive in \(A,B\) excludes an \(A,B\to\infty\) escape only in
the chart where \(C\) is bounded; it is a chart exclusion, not a standalone
global recurrence theorem.  Weak reversibility plus full deficiency zero
gives the class-restricted product-Poisson law for all positive rates, with
nonexplosion supplied by the complex-balance theorem.  The three exact seam
columns are exact-support membership identities importing their separately
stated classwise physical-time theorems; no monotonic extension to support
supersets is used here.

## 7. Class-local Anderson--Kim corollary

The publication citation is David F. Anderson and Jinsu Kim, *Some Network
Conditions for Positive Recurrence of Stochastically Modeled Reaction
Networks*, **SIAM Journal on Applied Mathematics** 78(5) (2018), 2692--2713,
[doi:10.1137/17M1161427](https://doi.org/10.1137/17M1161427), **Theorem 9**.
Theorem 4.2 is only the numbering in arXiv v3.

The journal theorem is stated globally.  The needed class-local statement is
a short corollary of its proof:

> Let \(\Gamma\) be a closed irreducible class.  If every tier sequence
> contained in \(\Gamma\) has a descending source in its global top S-tier,
> then the entropy generator is at most \(-1\) off a finite subset of
> \(\Gamma\), and every state of \(\Gamma\) is positive recurrent.

Indeed, if no such finite set existed, properness of the entropy would give
an unbounded sequence \(x_n\in\Gamma\) with generator greater than \(-1\).
Extract the tier subsequence used in the proof of journal Theorem 9.  The
class-local tier premise makes that proof force the generator to
\(-\infty\), a contradiction.  Closedness makes the restricted generator
identical to the original generator on \(\Gamma\).  For a binary network,
nonexplosion follows independently because every population-increasing
reaction has source degree at most one and bounded jump size, so its total
increasing intensity is \(O(1+|x|)\).  Continuous-time Foster then gives
positive recurrence on the irreducible class.

For each of the 151 pairs, any class-contained countersequence would have a
descriptor satisfying Theorem 2.1's necessary affine flag conditions.  By
definition no corrected failed descriptor has those conditions.  Therefore
every class-contained tier sequence satisfies the Anderson--Kim premise, and
the class-local corollary applies.

## 8. Required repair

The frozen inputs must not be cited as the exact publication dependency.
Use instead:

- `research_notes/s_tier_superlevel_cut_and_affine151_corrected.md`;
- `src/s_tier_superlevel_interface.py`;
- `tests/test_s_tier_superlevel_interface.py`.

Those derivative files preserve the audited old bytes while replacing the
false necessity claim, the four incidence totals, and the theorem citation.
