# The physical hard 188-template common-potential theorem

**Proof-first composition theorem, 2026-08-12 PDT. Audit status: pending.**
This note combines two analytic macroscopic theorems.  It does not infer a
stopping-time estimate from a finite search.  The finite normalized table is
used only to verify the disjoint exhaustion

\[
                         188=19+169.                         \tag{1.1}
\]

Fix a physical two-active hard descriptor, relabel its inactive coordinate
as \(I\), its lower-weight active coordinate as \(U\), and its higher-weight
active coordinate as \(V\).  Along the descriptor,

\[
 U=s^{p+o(1)},\qquad V=s^{q+o(1)},\qquad I=0,
 \qquad (p,q)\in\{(1,2),(1,3),(4,5)\}.              \tag{1.2}
\]

For an arbitrary fixed correction \(\ell\), put

\[
 G_\ell(x)=K_\ell+\sum_i\log(x_i!)+\ell\cdot x\ge1,
 \qquad W_\ell=G_\ell^4.                            \tag{1.3}
\]

Orient both linkage supports arbitrarily strongly and fix arbitrary positive
rates.  Constants may depend on those fixed data, never on \(s\).

## 1. Exact carrier pairs

Nineteen normalized rows have carrier linkage

\[
                         \{aU,V+I\},\qquad a\in\{0,1,2\}.    \tag{1.4}
\]

The exact-carrier theorem contracts this reversible carrier in physical
time.  For a lower source \(y=cU+bI\), define

\[
 w_a(y)=c+ab,\qquad \phi(y)=p w_a(y)-qb.             \tag{1.5}
\]

Its exact carrier occupation formula shows that the effective source rate
is \(s^{\phi(y)+o(1)}\).  A clean lower macro \(y\to z\) has the exact
leading factorial increment

\[
 \Delta G_\ell=\{\phi(z)-\phi(y)\}\log s+o(\log s). \tag{1.6}
\]

Thus rate selection is the negative gradient of physical factorial entropy.
Eighteen rows have a unique maximizing source.  The remaining row has a
two-source equality shell; its proof uses a killed exponential Green
estimate, an integrable positive-overshoot bound, and a strict terminal cut.
It does not assert the false pathwise sign on every equality-shell history.
Sourcewise ordered-Green bounds charge all lower interruptions and the
actual included endpoint.  The resulting physical stopping time satisfies,
for every fixed moment order \(r\),

\[
 \mathbb E\Delta G_\ell\le-c\log s,\qquad
 \mathbb E|\Delta G_\ell|^r=O(\log^r s),\qquad
 \mathbb E\sigma^r=s^{o(1)}.                        \tag{1.7}
\]

This theorem received a strict independent proof audit at its frozen hash.

## 2. Nonexact carriers

The other 169 normalized rows have a larger support in the linkage
containing \(V+I\), or have their maximal base source in the other linkage.
Let \(dU\), \(d\in\{1,2\}\), be the maximal base complex in either
linkage.  Every row obeys

\[
                              q-pd\ge1.              \tag{2.1}
\]

The nonexact Schur theorem contracts an exact
\(dU\to V+I\to dU\) physical self return and retains its time.  Strong
connectivity and nonexactness give a uniform geometric exit from that
two-node retry.  A nonself dominant clean macro either lands at \(cU\),
\(c<d\), or services one unit of \(V\).  In the latter case the two fast
targets can increase \(U\) by at most \(d\), so

\[
 \Delta G_\ell\le(pd-q)\log s+o(\log s)
                 \le-\log s+o(\log s).              \tag{2.2}
\]

Subdominant initiators and dirty fast-window interruptions have included
endpoint moments \(s^{-1+o(1)}\).  Exact retries are geometric and fast
windows are bounded, so all physical-time moments are bounded.  The proof
does not use the category name after its structural hypotheses are stated:

* 145 rows have a genuinely mixed support after deleting \(V+I\);
* eight separated rows have one clean carrier window and the same strong
  cut; and
* sixteen no-history rows have the maximal base source in the base-only
  linkage, so the first dominant nonself reaction is an immediate strict
  base descent.

The 145-row theorem and its 169-row analytic corollary both received strict
independent proof audits.

## 3. Unified physical theorem

The exact and nonexact categories are disjoint and exhaustive by (1.1).
Both use the same arbitrary fixed \(\ell\), the same physical population
potential, actual included endpoints, and raw physical time.  Taking the
appropriate stopped rule gives

\[
 \mathbb E_x\!left[
 W_\ell(X_\sigma)-W_\ell(x)+\sigma
 \right]
 \le-cG_\ell(x)^3\log s                              \tag{3.1}
\]

along every physical hard two-active bad descriptor.  Arbitrary fixed
endpoint and duration moments hold, and every terminal population is
eligible for immediate descriptor reclassification under the identical
\(W_\ell\).

### Theorem 3.1

For every one of the 188 normalized physical hard ratio/support templates,
every strong orientation, every fixed positive rate vector, and every fixed
correction \(\ell\), there is a raw physical stopped block satisfying
(3.1).  The finite table proves only the partition (1.1) and the structural
hypotheses of the two analytic inputs.

This is a local physical two-active theorem.  It does not certify any pair:
one-active, other two-active, all-active, passing-descriptor, common-\(\ell\),
and fixed-class gluing obligations remain separate.

## 4. Frozen inputs

The analytic inputs are pinned to:

* exact-carrier theorem:
  `3c18d0ee481e5c351663e4923b97473e871030c86ff37ca674f00688d66a047f`;
* exact-carrier finite premises:
  `43788cb4a458f6950d9316959393efc7270fbb2ef52bbb2f82bca0b6da848e66`;
* exact-carrier independent audit:
  `754bd752d707348a4098fdd3658fc2449034dcf4e208f13f5853092533f3f6c2`;
* mixed-145 Schur theorem:
  `d53772170088cccbacc7a0911b6a71e05ad6cbe856fbaddf8858769d19805714`;
* repaired mixed-145 finite premises:
  `ac9319af8d21f03a67e95458b90d26eb1d04a3274edbcd76b858650d25439e9f`;
* nonexact-169 corollary:
  `734f4cc3b0732b97c361100f2375c5b36a757da8926446c738dfdeef66130645`;
* nonexact-169 finite premises:
  `e34038585e738a42fce5a6587e578f28fe8b570c18c376e1394bf8e5791554a4`;
* nonexact-169 audit:
  `938fc5e653c7f19b575ee761b6e87dfc395d80498adf7cf5ee282657baf0be4f`.

No pair or global flag changes before an independent replay of this exact
composition.
