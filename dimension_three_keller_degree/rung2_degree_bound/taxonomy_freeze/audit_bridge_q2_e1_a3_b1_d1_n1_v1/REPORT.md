# Independent hostile audit of the post-freeze fixed-linear bridge

## Verdict

**PASS**, completed 2026-07-25T22:50:57Z.

The exact bridge
`../BRIDGE_Q2_E1_A3_B1_D1_N1_v1.md` at SHA-256

```text
51f864184ac0eddea9ff8b4e0ab9f635ced58d02c7a42dfdb1b03141f727f740
```

correctly routes every point of every frozen coefficient-pivot stratum of

```text
Q2-E1-A3-B1-D1-N1
```

to an audited theorem, or proves the stratum empty by a division-free
rank argument.  All 45 frozen pivots are accounted for:

```text
C00--C29  30 potential strata, each routed globally if nonempty
C30--C44  15 forced-empty strata
```

The intrinsic tree expands to 48 disjoint audit atoms, including the
horizontal atom, and maps uniquely onto 15 terminal groups.  Every terminal
now has a pinned independent hostile PASS.  No mathematical or certification
blocker remains in this bridge.

This verdict says that every quartic Keller map in the frozen row is an
automorphism; it does not say that the row is empty as a coefficient locus.
It does not alter `CERTIFIED_EXCLUSION_STATUS.md` or any other status ledger.

## Independence protocol

Before reading the candidate bridge or its checker, I read only the frozen
taxonomy, frozen manifest, and theorem/audit artifacts below
`fixed_linear_cubic_pencil/`.  I then wrote and timestamped the complete
route in `RESEARCH_LOG.md` at 2026-07-25T22:27:27Z.  The sealed file at that
checkpoint had SHA-256

```text
9274f62721ff7eabb2f095c2acd4526cc5bde0b3ae9248edd216acb053a59af6
```

and explicitly recorded the still-unresolved quadratic-component
provenance caveat, every expected terminal, all 45 pivot IDs, and the stale
headers.  Only after that checkpoint did I open the candidate and checker.

The later comparison did not reveal a route that was absent from the
independent enumeration.

## 1. Frozen normalization

The frozen tuple is
\[
(\operatorname{rank}JH_4,e,a,b,\delta,\nu)
=(2,1,3,1,1,1).
\]
The canonical-pencil theorem therefore gives
\[
H_4=hA(p,q),
\]
where \(h\) is linear, \(p,q\) are the coprime canonical minimal cubics,
and \(A\) is a basepoint-free binary triple of degree one.  Writing
\[
A(u,v)=\mathbf a\,u+\mathbf b\,v,
\]
basepoint freeness says exactly that \(\mathbf a,\mathbf b\) are linearly
independent.  The three minors
\[
\Delta_{01},\quad\Delta_{02},\quad\Delta_{12}
\]
give a complete finite target-normalization cover.  On each chart,
completing \(\mathbf a,\mathbf b\) by the unused standard basis vector has
determinant, up to sign, equal to the selected minor and sends
\[
H_4\longmapsto h(p,q,0)^T.
\]

This normalization:

- divides by no frozen coefficient \(c_i\);
- preserves exact degree, the Keller property, and automorphism status;
- transports arbitrary lower jets bijectively to arbitrary lower jets; and
- supplies relative algebraic closure of \(\mathbb C(p/q)\) from the frozen
  canonical minimal pair, rather than as a genericity assumption.

No normalization gap or hidden coefficient-pivot chart was found.

## 2. Intrinsic first split and boundary routing

Restriction of the cubic pencil to \(h=0\) has rank two or one.  Rank two
is the horizontal branch.  Rank one gives a unique vertical member because
two vertical members would make \(h\) divide both canonical generators.
Rank zero contradicts their coprimality.

On the vertical branch, a source and pencil change gives
\[
h=z,\qquad p=z^m r,\qquad m=1,2,3,\qquad z\nmid rq.
\]
For \(m=3\), the complete cubic kernel is
\[
\langle z^3,q\rangle.
\]
The zero vector and the two nonzero companion orbits
\[
G_3=0,\qquad G_3=z^3,\qquad G_3=q
\]
are disjoint and exhaustive.

Whenever a later calculation forces
\[
q\in\operatorname{Sym}^3\langle z,L\rangle,
\]
the canonical cubic pair has become nonminimal.  Such a point is not
contradicted inside this row; the frozen boundary rule recomputes the tuple
and routes it to one of the \(e=1,a=1,b=3\) rows according to
\((\delta,\nu)\).  The bridge handles this scope correctly and appends no
new frozen leaf.

## 3. Complete terminal ledger

The following are the theorem/audit packages reached by the 15 terminal
groups.  Repeated root and collision atoms are retained inside the listed
scope.

| Route | Complete terminal scope | Audited exit |
|---|---|---|
| H | horizontal restriction rank two | `WORKING_HORIZONTAL_FIXED_LINEAR_CUBIC_PENCIL.md`; `audit_hostile/REPORT.md` |
| Z1--Z3 | \(m=1,2\), or \(m=3,G_3=0\) | vertical-multiplicity theorem and `audit_vertical_hostile/REPORT.md`; quadratic-component theorem and `audit_quadratic_component_exit/REPORT.md` |
| N1--N2 | \(m=3,G_3=q\), nontriple or triple \(q_0\) | both nonvertical lemmas; aggregate `audit_nonvertical_companion/REPORT.md` |
| V1--V2 | \(G_3=z^3,s\ne0\), nontriple \(q_0\), \(\ell=0\) or \(\ell\ne0\) | zero/nonzero-\(\ell\) lemmas and their separate hostile reports |
| V3 | \(G_3=z^3,s\ne0\), triple \(q_0\), \(\gamma\ne0\) | nonzero-\(\gamma\) theorem and hostile report |
| V4--V5 | same triple branch, \(\gamma=0\), arbitrary \(\ell\) | audited zero-\(\gamma\) reduction followed by the audited zero-\(\ell\) theorem |
| V6 | \(G_3=z^3,s=0,W_0=0\) | `VERTICAL_A0_W0_ZERO_EXCLUSION.md`; `audit_vertical_a0_w0_zero/REPORT.md` |
| V7 | \(G_3=z^3,s=0,W_0\ne0\) | `a0_w0_nonzero_attack/NOTE.md`; `audit_a0_w0_nonzero/REPORT.md` |

The 48-atom replay includes:

- all three binary-cubic root partitions;
- all three minimal triple-root charts;
- every squarefree root-line position;
- the double-root noncollision and both collision kernels;
- \(\gamma=0\) and \(\gamma\ne0\);
- \(\ell=0\) and \(\ell\ne0\);
- \(W_0=0\) and every rank/root-incidence atom for \(W_0\ne0\); and
- the horizontal, \(m=1\), \(m=2\), and zero-companion exits.

Every atom satisfies exactly one terminal predicate.  No discriminant,
lower-jet parameter, or collision divisor is silently discarded.

## 4. The 45 frozen coefficient pivots

For `C00`--`C29`, the bridge supplies exact leading-shape witnesses.
For each quartic monomial \(m_i\), choose a coordinate \(h_i\mid m_i\),
put \(p_i=m_i/h_i\), and take
\[
q_*=x^3+y^3+z^3.
\]
The two target placements
\[
(m_i,h_iq_*,0),\qquad(0,m_i,h_iq_*)
\]
have first pivots `C\(i\)` and `C\(15+i\)`.  A fresh dependency-free
sparse calculation checked:

- exact first-pivot positions;
- component gcd exactly \(h_i\);
- \(\gcd(p_i,q_*)=1\);
- three essential variables for \(q_*\), excluding a nonminimal binary
  cubic pair; and
- a nonzero \(2\times2\) Jacobian minor in every witness.

These witnesses establish compatibility with the frozen leading tuple;
they are not claimed to be Keller completions and therefore do not prove
that the corresponding Keller strata are nonempty.  The coverage statement
needs only the correct conditional route: every point in any nonempty one
of these thirty intersections enters the global theorem tree without
division by its pivot.

For `C30`--`C44`, component-major ordering makes
\[
H_{4,1}=H_{4,2}=0.
\]
The leading Jacobian then has at most one nonzero row, so every
\(2\times2\) minor vanishes, contradicting frozen rank two.  Thus all
fifteen are empty.  This uses no division and applies even if the third
component is arbitrary.

The two sets are disjoint and their union is exactly
`C00`--`C44`.

## 5. Quadratic-component provenance caveat

This was a genuine certification blocker in the original candidate state.
The fixed-linear notes called the quadratic-component exit “banked,” while
the only audit evidence was aggregate prose in `VERIFICATION.md`.  Three
terminals depend on it: \(m=1\), \(m=2\), and \(m=3,G_3=0\).

The blocker is now repaired.  The standalone hostile report
`../../audit_quadratic_component_exit/REPORT.md`, SHA-256

```text
8ee4a3ce87c3045b6f4dde58c5e20466e75e1ac4cecc5167a3853933d04aeb32
```

independently reconstructs the Hessian-coordinate proof, verifies
\[
\deg(F\circ T^{-1})\le4\cdot2=8,
\]
checks every plane restriction is Keller, and checks the exact
degree-at-most-twelve plane theorem and field/degree conventions against
Vistoli's journal pages 79--80.  Its verdict is PASS.  The final bridge and
checker pin this report.

The published plane theorem and the final injective-étale theorem remain
literature black boxes; the standalone audit checks their exact statements
and applicability rather than pretending to reprove them computationally.

## 6. Stale headers and supplied-checker attack

The original bridge/checker hashes

```text
f97616e83d5eec3731319de1357ff484c6782ed4f5c1400ec66e947f89632f04
3863a98850948b5e5d52a75093b40e7e6a2a5a0ef64e151d843e39fa8feb59ae
```

still marked \(s=0,W_0\ne0\) conditional after its hostile audit had
passed.  The parent vertical theorem, both nonvertical lemma headers, the
rank ledger, and the \(W_0\ne0\) theorem also lagged their later reports.
Those were stale status defects rather than scope defects.

They are repaired in the final pinned state:

- the bridge is unconditional and cites both newly required PASS reports;
- all 15 candidate-checker terminal flags are false;
- the quadratic theorem cites its standalone report;
- the vertical/nonvertical/\(W_0\) headers cite their audits; and
- the rank ledger records complete internal coverage.

The original supplied checker also did not pin the bridge itself.  Replacing
the bridge by a file containing only its ten required marker strings still
produced the old PASS sentinel.  This was a semantic fail-open defect in the
checker, not a counterexample to the bridge.  The repaired checker at
SHA-256

```text
700e6e487a91920f6292a4c89dadc1133e7949a0a9546a1b194deaa3006b718f
```

pins the exact bridge.  Both the repaired candidate checker and this
independent checker now reject the semantic truncation, and the candidate
checker separately rejects a mutated pinned theorem.

## 7. Independent checker and fail-closed tests

`verify_bridge_independent.py` uses only the Python standard library.  It
does not import the candidate checker or SymPy.  It independently:

- reconstructs the three target-minor normalization charts with sparse
  symbolic arithmetic;
- verifies all thirty leading witnesses and all fifteen empty pivots;
- expands the route to 48 disjoint atoms and tests unique routing;
- pins every terminal theorem and hostile report;
- requires the standalone quadratic-component report at all three zero
  companion terminals; and
- requires the final repaired bridge/checker/status headers.

The strict wrapper rejects each of these mutations:

```text
drop_normalization_chart
drop_pivot
overlap_pivot
drop_atom
overlap_terminal
drop_terminal
unaudit_a0
unaudit_quadratic
```

It also rejects optimized execution of the independent checker, checks
the candidate checker's optimized guard, replays the final
\(s=0,W_0\ne0\) hostile wrapper, and runs the quadratic-component exact
checker in ordinary and optimized modes.

The final exact output is:

```text
FROZEN_PIVOTS=45
POTENTIAL_ROUTED=30
FORCED_EMPTY=15
ROUTE_ATOMS=48
INTRINSIC_TERMINALS=15
AUDITED_TERMINALS=15
QUADRATIC_PROVENANCE=STANDALONE_HOSTILE_PASS
STALE_STATUS_MARKERS=0
CANDIDATE_STATUS=UNCONDITIONAL
BRIDGE_Q2_E1_A3_B1_D1_N1_INDEPENDENT_PASS_F4A93C
CANDIDATE_CHECKER_SEMANTIC_MUTATION=REJECTED
INDEPENDENT_CHECKER_SEMANTIC_MUTATION=REJECTED
CANDIDATE_CHECKER_PINNED_INPUT_MUTATION=REJECTED
BRIDGE_Q2_E1_A3_B1_D1_N1_STRICT_PASS_72C8E1
```

At this verdict, the independent checker and wrapper have hashes

```text
e3f93f0c87ac35030111ceb4829f1f19965e867fd0064a15ef11205c207293a9  verify_bridge_independent.py
8c1c9cd8a896ccba0e7d44ba4a9bf273dabf607b62806b9b0a2466fc8ef51c4e  verify_strict.sh
```

Run:

```sh
cd dimension_three_keller_degree/rung2_degree_bound/taxonomy_freeze/audit_bridge_q2_e1_a3_b1_d1_n1_v1
./verify_strict.sh
```

## Final disposition

No normalization leak, missing pivot, omitted route atom, illegal
reclassification, terminal scope mismatch, or unaudited terminal remains.
The post-freeze bridge passes at its exact final hash.

This audit and its software were produced with substantial AI assistance.
Exact computation is evidence about the encoded algebra and coverage
ledger, not peer review.
