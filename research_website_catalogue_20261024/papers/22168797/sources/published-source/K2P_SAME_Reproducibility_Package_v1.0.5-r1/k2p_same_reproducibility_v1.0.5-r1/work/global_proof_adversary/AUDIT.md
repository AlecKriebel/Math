# Fail-closed audit of the global K2P proof layer

Audit date: 2026-08-21 (PDT)

## Verdict

**Global theorem promotion: PASS.**  Every precise repair identified in the
original adversarial pass has been incorporated into
`work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md`.
The corrected finite universe and all-primitive probe have also passed their
independent replays and mutations.  The promotion guard verifies 23 earlier
frozen inputs, three completed probe artifacts, six raw probe ledgers, ten
pass gates, and eight zero gates.

**Analytic/global layer: PASS.  Corrected finite and coherent-probe layers:
PASS.  Remaining load-bearing blockers: none.**

This audit makes no mixed-sign claim and does not promote any stale finite
ledger.

## Lemma ledger

| Layer | Verdict | Exact boundary |
|---|---|---|
| Principal domain and strict subdivision | PASS | The displayed inequalities and near-identity factorization are correct on `D_plus`; power roots handle strict continuous time. |
| Complete two-sector bridge fibre | PASS | The fibre has one paired `C/T` and one `G` incidence scale per endpoint on the retained strong class.  The componentwise argument below replaces the one-line appeal to observable symmetry. |
| Incidence freeness | PASS | Marked components have one-incidence anchors.  Unmarked degree at least three components have pair anchors.  The degree-two stabilizer is real but excluded from the retained class. |
| Physical local-product saturation | PASS | The proof starts at strict endpoint factors `(r,r)`, `r<1`, near `(1,1)`, not at the boundary point `(1,1)` itself.  The four relative endpoint coordinates are locally independent. |
| Paired marginal openness | PASS | The fixed-`r` section is analytic and physical.  This is a source restriction theorem only. |
| Restoration implication | PASS | It applies only after fixing one full containment and retaining an actual omitted label in those same networks; the corrected forest supplies finite child completeness. |
| Root reduction | PASS | Ordinary-path rerooting works, including when the old root subdivides an edge entering a reticulation; the switching-by-switching argument is given below. |
| One-/two-port word reconstruction | PASS | The corrected exact probe ledger has coherent parent transports and closes all 29,964 one-port and 544,571 two-port rows. |
| Local-to-global necessity | PASS | The proof uses the physical source product chart and intrinsic projective bridge extraction and never asserts that an arbitrary normalized target slice tensor is physical. |
| Local-to-global sufficiency | PASS | The common rank-nine triangle germ is propagated through one common context map by a maximal-rank argument. |
| Semialgebraic genericity | PASS | Full-dimensional semialgebraic intersection yields an open source germ; stratifying the physical incidence correspondence supplies the required analytic target section. |
| Exact reconstruction | PASS | It returns the unique canonical structural class modulo coherent triangle redirection outside the stated proper exceptional set; no pointwise-image equality is claimed. |
| Strict continuous-time transfer | PASS | The CT cone is Euclidean open; every nonzero polynomial certificate remains generically nonzero there, and the two-section bridge inequality supplies physical gluing. |
| Weak-class sharpness | PASS | Both exact replays pass.  Add the elementary upper-bound argument showing each cherry can add at most four image dimensions. |

## 1. Exact componentwise `C/T` scale lemma

Let `sigma` fix `0,G` and exchange `C,T`.  Let a positive normalized local
boundary tensor be transformed by incidence functions `c_e(h)>0`, with
`c_e(0)=1`, and suppose both the original and transformed tensors are
K2P-invariant under simultaneous application of `sigma`.  Put

\[
 \rho_e=\frac{c_e(C)}{c_e(T)}.
\]

There are two cases.

1. **Marked component.**  Choose one retained physical block.  The
   conservation-supported entry with `C` at incidence `e`, `C` at that block,
   and zero elsewhere is carried by `sigma` to the corresponding `T,T`
   entry.  Positivity and K2P invariance before and after transformation give
   `rho_e=1`, independently for every incidence.
2. **Unmarked component of degree `d>=3`.**  For every pair `e!=f`, compare
   the entries with `C,C` and `T,T` at incidences `e,f` and zero elsewhere.
   They give

   \[
   \rho_e\rho_f=1.
   \]

   Three distinct incidences imply `rho_e=rho_f=rho_k=1` by positivity, and
   every remaining incidence follows by pairing with one of them.

For `d=2` there is only `rho_1 rho_2=1`, leaving the genuine stabilizer

\[
 (\rho_1,\rho_2)=(t,t^{-1}),\qquad t>0.
\]

Thus a theorem stated for an arbitrary positive K2P-symmetric component
locus is false without an anchor hypothesis.  On the retained strong class
the defect is absent:

- every primitive finite anchor is physically marked;
- the graph-derived minimum supports have 3 ports for the cycle, 4 for
  `theta0`, `theta1`, `theta3`, and 5 for `theta2`;
- restoration and probes only add marked ports;
- every unmarked ordinary component has degree at least three; and
- the only simple reduced two-boundary theta has path lengths `(1,2,2)`,
  namely `K4-e`, and has 25 rooted binary acyclic presentations but zero
  tree-child presentations.

The independent exact replay is
`verify_component_scales.py`; its certificate payload is
`ce8f4e6860675e36238b8351458875bd46de0507df34f6729e34b20170e02acd`.
It also checks every primitive support directly from the graph encodings.

The singleton `G` orbit is not related to `C,T` by K2P symmetry and therefore
retains its independent positive incidence scale.  All-zero normalization
fixes the zero-character scale.  This gives exactly the claimed two-sector
action.

## 2. Physical quotient chart

The analytic normalizers are valid on positive anchors.  For an unmarked
degree-`d` component, the exponent rows

\[
 (12),(13),(23),(14),\ldots,(1d)
\]

have rank `d` and leading determinant `-2`, separately in the paired and
singleton sectors.  Marked components use the identity matrix.

The physical saturation argument must be phrased at an interior split.  For
an effective bridge `(s,g)` choose `r<1` sufficiently close to one so that

\[
 (r,r),\quad
 \left(\frac{s}{r^2},\frac{g}{r^2}\right),\quad
 (r,r)
\]

all lie strictly in `D_plus`.  Strictness supplies an open four-dimensional
neighborhood of the two endpoint pairs, while the residual pair stays
physical.  Relative to this interior base split, the endpoint ratios vary on
both sides of one and realize all four incidence directions.  Suppression of
the two serial degree-two vertices returns the same standard edge.  Applying
this independently on the bridge tree gives no holonomy.

This proves a physical quotient germ.  It does **not** prove that an arbitrary
ambient normalized slice representative is a physical local-network tensor.

## 3. Paired marginal openness and restoration

For a serial class of length `m`, let

\[
 M=\max\{S,G,2S-G,0\}<1
\]

and choose `M<r^(m-1)<1`.  The first `m-1` factors `(r,r)` and the last factor

\[
 \left(S/r^{m-1},G/r^{m-1}\right)
\]

are in `D_plus`, multiply to `(S,G)`, and give a local analytic section.  The
product Jacobian has independent `s` and `g` rows, hence rank two.  Coordinate
roots give the CT section.

Now fix one actual full containment `N -> N'`, one selected frozen parent,
and one actual omitted label in those same networks.  A small child-source
parameter germ lifts through the serial-product section to a full-source
parameter germ.  Because the witnessing source image germ is relatively
open, the lifted full distributions remain in it after shrinking.  Their
target representations marginalize to the actual target child.  Therefore
the enumerated direct child inherits an open source-relative containment.

No selected relation is lifted abstractly, and no target deletion map is
inverted.  The logical implication is valid once finite generation proves
that the actual child appears with its exact parent transport.

## 4. Root reduction and probe completeness

The current domain note proves reversibility for ordinary rerooting but omits
one admissible case.  The complete K2P lemma is as follows.

Choose a tree-child rooted partner.  Repeatedly choose an ordinary tree or
leaf child to obtain an ordinary root-to-leaf path.  Suppress the old root,
reverse only ordinary edges on that path, and insert the new root on the
terminal pendant edge.  The mixed graph is unchanged.  Symmetry of every K2P
transition matrix handles reversed ordinary edges, and strict K2P
subdivision handles the new root edge.

If the old root subdivides an edge entering a reticulation, check each
switching separately:

- when that reticulation parent is selected, the two root arms are serial and
  enter only through `(s_1 s_2,g_1 g_2)`;
- when the other parent is selected, the remaining one-child root stem
  subtends all observed leaves, so its Fourier character is zero and its
  multiplier is one.

Thus rerooting preserves every displayed-tree term and the strict physical
germ.  Strong tree-childness makes the new admissible rooting tree-child.

With a fixed rigid support, the word argument is exact: `A+p` locates the
unique directed segment of `p`; `A+p+q` fixes the order when `p,q` share a
segment; and pairwise comparisons are transitive because they are
restrictions of the same two actual full words.  Literal triangle edge sets
and parent-restricting vertex maps force one coherent triangle choice.

The corrected finite probe replay is now present.  It reconstructs all 176
anchors and classifies all 29,964 one-port and 544,571 two-port rows with zero
unresolved or incoherent records.  Its primary payload is
`674853fa730c4f54b9ba264d539a51591c8b926ad444195e68df086c26f83825`;
the clean-room graph/full-map replay payload is
`65160636abfa33de47136a222081ac70bd7b6fae0e029b7a7c379e2d8653df74`.

## 5. Local-to-global necessity and sufficiency

For necessity, recover the common decorated bridge tree first.  Pull an open
source containment germ back through the physical source product chart and
shrink to a product box.  Intrinsic positive block factorization maps each
observed tensor to the same projective local factors.  Projecting the box to
one source factor therefore yields an open source-relative containment in
the corresponding target **projective** local model.  All finite separators
used here must be invariant or multihomogeneous under both incidence sectors.
No distant factor can cancel one of them.

For sufficiency, isomorphisms transport physical sections.  The ordinary
triangle requires the following context lemma.

Let `tau_i:Theta_i -> Q` be any of the three ordinary K2P triangle maps.  At
the certified common CT point every `tau_i` has rank nine, the full dimension
of the normalized three-boundary K2P tensor space, so all three cover one
common open set `U` with physical analytic sections.  Cut the three ordinary
external arms and write the identical remaining context as one analytic map

\[
 H:Q\times C\longrightarrow Y.
\]

Choose `(q,c)` in the nonempty open set `U x C` where `DH` has its generic
maximal rank `R`.  Since each `tau_i x id_C` is a submersion,

\[
 \operatorname{rank}D(H\circ(\tau_i\times id_C))=R
\]

for every orientation.  The common set `H(U x C)` therefore contains an
`R`-dimensional regular germ which is full-dimensional in every redirected
network image.  This remains valid when the context reconnects triangle arms
inside one level-2 blob.

After local sections are chosen, simultaneous bridge gluing on `D_plus` uses
small `s,g` so that the original bridge and every section-transformed bridge
remain strict.  In CT, for two local sections use

\[
 \max\left\{1,\frac{B_1}{A_1^2},\frac{B_2}{A_2^2}\right\}s^2
 <g<\min\{1,B_1,B_2\}.
\]

The interval is nonempty for sufficiently small `s`.

## 6. Genericity and reconstruction

All physical images and their intersections are semialgebraic.  If an
intersection has full source dimension, a Whitney/cell stratification gives
a relatively open source stratum.  To justify the target-section clause,
stratify the physical incidence correspondence

\[
 Z=\{(q,\theta'):q=\Phi_{N'}(\theta')\}
\]

and its projection to that open source stratum.  Some stratum of `Z` projects
with full rank; the constant-rank theorem gives a local analytic physical
section.  Hence the section clause is automatic after shrinking.  The proof
should either include this argument or define containment directly by full
source-dimensional semialgebraic intersection.

For a fixed source topology, a Zariski-dense semialgebraic intersection has
full real dimension because the source parameter domain is Euclidean open
and the maximal real and complex Jacobian ranks agree.  The classification
then makes every inequivalent intersection closure proper.  Finiteness of
the labelled strong class gives one proper finite exceptional union.

With the finite theorem and probes closed, reconstruction returns the
lexicographically least topology in the structural quotient by coherent
ordinary triangle redirection.  It may also enumerate that **structural**
equivalence class.  A common regular triangle germ does not imply equality of
the complete triangle images, so the proof must not claim that every
redirected representative contains the particular input distribution.
Pointwise membership requires a separate semialgebraic test.

The stated `O(n^9)` number of bounded restrictions uses the corrected
release's certified nine-port maximum.  It is a count of
restrictions in addition to reading/Fourier-transforming the explicit
`4^n` table, not a bit-complexity bound.

## 7. Strict continuous time and sharpness

The CT cone `0<s<1, s^2<g<1` is a nonempty Euclidean-open parameter domain.
Thus every polynomial pullback known to be nonzero remains nonzero on a dense
open CT subset; it cannot vanish identically on an open cone.  Pointwise sign
certificates remain strict, power subdivision supplies marginal/root
sections, the rank-nine triangle point is CT, and the bridge inequality above
supplies simultaneous gluing.  The corrected finite and probe gates pass, so
the CT theorem follows.

The weak-sharpness construction passes both exact replays:

- primary certificate SHA-256
  `e66c78a0aeab990b4dc448f4f064b37e1e15ecbff75a5f472bf116d4464378bd`;
- independent certificate SHA-256
  `cfd8d3a2ebc7431d141cac6ebe943e25730eb086fbc84b52833a40bee40a5d52`.

At the three-leaf common point both maps have rank nine.  Replacing one leaf
by a cherry factors the entire extended image through the old tensor and the
four new arm eigenvalues, so image dimension can increase by at most four.
The rational observables `(u/v,uv)` in each sector have nonzero block
Jacobian, so it increases by at least four.  Hence it increases by exactly
four, and the shared germ has dimension `9+4(n-3)=4n-3`.  Pruning proves
weak-not-strong membership and inequivalence persist.

## Promotion gate closure

All originally required promotion conditions are now true:

1. replace every revoked rooted `tree--sunlet` finite label by the corrected
   whole-map `T_i` or other exact certificate and update every census;
2. land and independently replay the corrected all-primitive probe package;
3. insert the componentwise `C/T` lemma and degree-two exclusion;
4. insert the complete root-reduction and contextual-triangle lemmas;
5. state reconstruction only modulo the structural triangle quotient unless
   explicit pointwise membership tests are added; and
6. pass the unified independent release and mutation gates.

The fail-closed promotion guard passes.  `K2P-SAME` is established on the
principal `D_plus` domain under the exact hypotheses of the promoted
manuscript.  No mixed-sign extension is asserted.
