# Bounded Omega audit

Status: **OMEGA-PASS-ALL-(n)**

Scope: only the immutable historical `N16`/`N26` Omega source and target in
`../frozen_input/historical/jc_omega_move.json`, under the fixed, already-simple,
one-step `sd_0` convention of the baseline paper.  No Omega variant, chain,
alternate labelling, richer substitution model, or repair gadget was searched.

## O1 — fixed-graph topology

**VERIFIED.**  Direct one-step reduction marks the arcs entering `V` and `X0`,
undirects all others, deletes only the root `S`, and joins its two children.
No loop, parallel edge, degree-two internal vertex, or lost reticulation is
created.  Each resulting mixed graph is binary, LSA-rootable, level two, and
has one nontrivial blob.  Exact cycle enumeration gives cycle lengths
`[4,4,6]`, hence no triangle.

For each of `N16_source`, `N16_target`, `N26_source`, and `N26_target`, exhaustive
orientation of the fixed mixed graph gives seven LSA-valid admissible rootings.
Exactly two are tree-child.  The displayed historical rooting is one of those
two.  The remaining five preserve the omnian at `U`, which tails both retained
reticulation edges and has only one undirected incidence.  Thus both fixed
topologies lie in `W_TC \ S_TC`, not in the positive theorem's `S_TC` class.
The complete canonical rooting records are in
`../independent/output/omega_release_audit.json`.

## O2 — labelled graph distinction

**VERIFIED.**  Exact arrowhead- and label-preserving mixed-graph
canonicalization gives different encodings.  A human-readable invariant is
already enough: in the N16 source, labelled leaf 1 has unordered distances
`{3,3}` to the two reticulations; in the target it has `{2,4}`.  Because both
graphs are triangle-free, ordinary triangle redirection is unavailable.

## O3 — exact JC equality

**EXACTLY COMPUTED.**  The primary symbolic verifier and a clean-room direct
displayed-tree implementation independently enumerate four switchings and all
descendant masks.  The N16 source-to-target correspondence fixes

```text
a5=a6=a11=lambda_V=lambda_X0=1/2
```

and uses the nine free source coordinates
`(A,B,C,D,E,F,P,Q,R)=(a0,a1,a2,a3,a4,a7,a8,a9,a10)`.  With
`G=E+2F` and `H=AF+2E`, it sets

```text
b0=2F(4-A)/G,       b1=D/(4-A),        b2=C,
b3=2BH/G,           b4=4ER(4-A)/H,     b5=b6=1/2,
b7=2ARG/H,          b8=Q,              b9=P,
b10=G/8,            b11=1/2,           mu_V=mu_X0=1/2.
```

All 64 zero-sum Fourier identities reduce exactly to zero.  At the certified
strict point every edge multiplier and inheritance probability lies in
`(0,1)`.  The clean-room replay checks the complete 256-entry Fourier tensor,
performs the inverse transform, and checks equality and strict positivity of
all 256 site-pattern probabilities.

## O4 — full-dimensional regular overlap

**VERIFIED.**  Exact rational-function row reduction gives core rank six.
Four pendant torus directions add at most four dimensions, while the exact
Euler identity

```text
x4*d(c_g)/dx4 + x7*d(c_g)/dx7 = 1[g4 != 0]*c_g
```

removes one direction, proving the upper bound nine.  Independent exact
rank-nine minors prove the matching lower bound on both sides:

```text
N16_source  -171/2305843009213693952000000
N16_target  -513/9223372036854775808000000
N26_source    57/576460752303423488000000
N26_target   189/2305843009213693952000000
```

The rational correspondence is defined on an open neighborhood of the strict
source point because `G`, `H`, and `4-A` are nonzero there; continuity keeps
all target coordinates in `(0,1)` after shrinking.  Its common coordinate map
has rank nine.  Since both complete models have dimension nine and both points
are regular, the common image is a relatively open nine-dimensional germ in
both images.  Locally,

```text
dim M_Omega = dim M_Omega' = dim(M_Omega intersect M_Omega') = 9.
```

## O5 — direct all-n propagation

**VERIFIED.**  Repeatedly replace the same corresponding leaf other than leaf
1 by an identical cherry.  The existing leaf-substitution identity has the
positive analytic inverse

```text
uv = P_tilde(0,h,h),
u/v = P_tilde(g_X,h,0) / P_tilde(g_X,0,h).
```

It therefore adds exactly two model dimensions and preserves the common
regular germ.  Pendant substitution creates no cycle or blob, so simplicity,
triangle-freeness, and level two persist.  A tree-child admissible rooting
extends through the pendant tree, while the original non-tree-child rooting
and its omnian remain.  The labelled distance witness at leaf 1 remains.
Consequently, for every `n>=4` there is a triangle-free pair in
`W_TC \ S_TC` with common full-dimensional regular overlap of dimension
`9+2(n-4)=2n+1`.

## O6 — clean-room replay and mutations

**VERIFIED.**  The clean-room graph/rooting code, displayed-tree engine,
dual-number Jacobian code, determinant routine, and mixed-graph canonicalizer
import no discovery implementation.  The integrated release verifier checks
all topology, stochastic, rank, and propagation gates.  It rejects all twelve
required mutations, including deletion of a rooting, use of only the displayed
rooting, an added triangle edge, a reversed arrowhead, a relabelling, a changed
reticulation parent, a boundary parameter, a changed Fourier entry, a replaced
rank certificate, graph identification, promotion from one tree-child rooting,
and a triangle-free claim without cycle enumeration.

## Reproduction

```bash
PYTHONPATH=omega_audit/frozen_input/historical/src \
  python omega_audit/frozen_input/historical/src/verify_jc_omega_move.py

PYTHONPATH=omega_audit/frozen_input/historical/src \
  python omega_audit/frozen_input/historical/src/verify_jc_omega_move_stdlib.py

python omega_audit/independent/verify_omega_release.py
```

The historical symbolic replay requires `sympy` and `python-flint`; the
integrated clean-room release verifier requires only `sympy`.  Complete
transcripts and hashes are under `../transcripts/`.

## Disposition

**OMEGA-PASS-ALL-(n).**  The final paper may state that triangle-free weakly
tree-child level-2 networks are not generically identifiable under open JC for
arbitrarily many taxa.  This sharpens the boundary theorem without changing
the positive theorem's locked `S_TC` scope.  The triangle-containing Theta
family remains a second, algebraically distinct weak-class mechanism.
