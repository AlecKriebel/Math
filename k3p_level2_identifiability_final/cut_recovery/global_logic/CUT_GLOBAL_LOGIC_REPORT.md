# Directed-cut global-logic audit

## Decisive verdict

**Outcome B: the reverse directed-cut implication is unresolved and currently
blocks K3P-SAME.**

For a source-relative containment

\[
N\preceq_{3,+}N',
\qquad
\Phi_N=\Phi_{N'}\circ\sigma\quad\hbox{on a source-open }U,
\]

generic K3P cut recovery proves exactly

\[
\boxed{\operatorname{Cut}(N')\subseteq\operatorname{Cut}(N)}.
\]

It does **not** prove the reverse inclusion. If a split is a source cut but a
target noncut, the analytic physical target section may lie entirely inside
the target's proper cut-rank locus. The definition does not require a target-
regular point, an open target-parameter image, or equality of source and
target image dimensions.

Thus the target reduced bridge tree is presently known only to be a labelled
contraction of the source reduced bridge tree. The existing bridge-fibre,
localization, fourteen-orbit, restoration, and probe results cannot be
invoked to upgrade this to equality without circularity.

This report does not exhibit a counterexample inside the strongly tree-child
class and therefore does not refute K3P-SAME. It identifies the exact missing
implication that prevents its certification from the current package.

## 1. Audited containment semantics

The inherited source-relative definition is unambiguous. In the K2P
manuscript, `k2p_level2_source.tex:355--365`, \(N\preceq N'\) means that
there are:

1. a regular **source** point;
2. a connected open set \(U\) in the source parameter space on which the
   source map has its generic rank; and
3. a real-analytic physical target section
   \(\sigma:U\to\Theta(N')\) with
   \(\Phi_N=\Phi_{N'}\circ\sigma\).

Symmetry is explicitly not part of the definition. The JC formulation at
`jc_level2_source.tex:403--420` says the same thing at image level and states
explicitly that the target dimension may be larger. The common-germ relation
\(\bowtie\), by contrast, is full-dimensional and regular in both images.

Consequently, differentiating the containment identity gives only

\[
d_N\le d_{N'}.
\]

It supplies neither \(d_N=d_{N'}\) nor target regularity.

## 2. What isotropic-JC generic cut recovery proves

Fix a labelled split \(S=A\mid A^c\). Let

\[
I_S=(M_{S,1},\ldots,M_{S,k})
\]

be the finite family of all \(5\times5\) minors of its K3P flattening.

- If \(S\) is a graph cut, every \(M_{S,i}\circ\Phi_N\) is identically zero.
- If \(S\) is a graph noncut, restriction to the isotropic slice
  \((c_e,g_e,t_e)=(r_e,r_e,r_e)\) gives the JC map. The corrected JC cut
  theorem supplies a point where at least one \(5\times5\) minor is nonzero.
  Hence at least one \(M_{S,i}\circ\Phi_N\) is a nonzero polynomial on the
  full K3P parameter space.

The isotropic slice lies in both the strict principal domain and strict
continuous time, so this argument proves generic cut recovery in either
domain.

Now assume \(N\preceq N'\).

### Target cut implies source cut

Suppose \(S\in\operatorname{Cut}(N')\). Every target pullback
\(M_{S,i}\circ\Phi_{N'}\) is identically zero. Therefore

\[
M_{S,i}\circ\Phi_N
=M_{S,i}\circ\Phi_{N'}\circ\sigma
=0
\qquad\hbox{on }U
\]

for every \(i\). If \(S\) were a source noncut, one of these source pullbacks
would be a nonzero polynomial. A nonzero real polynomial cannot vanish on the
nonempty Euclidean-open set \(U\). This proves

\[
\operatorname{Cut}(N')\subseteq\operatorname{Cut}(N).
\]

### Source cut does not generically imply target cut

Suppose instead that \(S\in\operatorname{Cut}(N)\). The same equality only
gives

\[
M_{S,i}\circ\Phi_{N'}\circ\sigma=0
\qquad\hbox{on }U.
\]

If \(S\notin\operatorname{Cut}(N')\), generic target recovery says merely
that some \(M_{S,i}\circ\Phi_{N'}\) is a nonzero target polynomial. It does
not prevent its zero set from containing the analytic submanifold
\(\sigma(U)\). This is the missing reverse inclusion.

The elementary exact model

\[
\phi(x)=(x,0),\qquad
\psi(u,v)=(u,v),\qquad
\sigma(x)=(x,0)
\]

makes the logic explicit: \(f(y_1,y_2)=y_2\) is nonzero on the target, but
\(f\circ\psi\circ\sigma=0\) on the entire regular, full-dimensional source
germ. Here the source and target ranks are one and two.

## 3. Two conditions under which generic recovery would suffice

The gap is directional, not a defect in generic recovery itself.

### Symmetric common germ

If \(N\bowtie N'\), the common germ is regular and full-dimensional in both
images. A nonzero cut minor cannot vanish on a full-dimensional relative-open
germ of either irreducible image. Generic recovery therefore gives equality
of cut sets in the \(\bowtie\) case.

### Equal image dimensions

If one independently knew \(d_N=d_{N'}\), the chain rule would make the
target regular along the section. A \(d_N\)-dimensional source image germ
contained in a regular \(d_{N'}\)-dimensional target germ would be relatively
open in that target branch. Generic recovery would again force equality of
cut sets.

No current dependency proves this dimension equality for an arbitrary
directed relation. Indeed, the bounded K3P candidates themselves include
directed rank comparisons such as \(20\to24\), and source-relative
containment semantics expressly allow a larger target.

## 4. Why the current local-to-global package does not close the gap

### Bridge fibre

At a source cut, positive rank-one character blocks intrinsically factor the
observed tensor. This remains true even if a target realization comes from a
graph with no corresponding bridge. But the factorization only produces
tensor slices. It does not make those slices physical factors of the target
graph. The JC bridge-fibre statement explicitly warns that slice tensors
need not themselves be physical local-network tensors
(`jc_level2_source.tex:909--927`).

### Coarse localization is outside the atlas

From the proved inclusion, every target cut is a source cut. One may therefore
cut along the target bridge tree. A target blob then corresponds on the
source side to a connected **superfactor**: possibly several source blobs and
ordinary components joined by the extra source-only bridges.

The certified local theorem does not cover that comparison. Its source and
target are one pair of corresponding complete nontrivial factors on the same
physical boundary set (`jc_level2_source.tex:1113--1123`), and the K2P
computer-assisted statement is explicitly for a pair of complete physical
cycle/theta factors (`k2p_level2_source.tex:1060--1074`). The fourteen K3P
orbits refine that same single-blob universe. They do not classify

\[
(\text{multi-blob source superfactor})
\longrightarrow
(\text{one target blob}).
\]

The published proof order confirms the dependency: bridge-tree equality is
used first, then the bridge fibre creates corresponding factors, and only
then is localization and the local theorem applied
(`jc_level2_source.tex:1557--1571` and
`k2p_level2_source.tex:1337--1347`). Reusing the local theorem to prove the
bridge-tree equality would be circular.

### Marginals, finite selection, restoration, and probes

- Marginal submersions preserve openness of restrictions that already arise
  from a fixed graph relation. They do not create a physical target port at a
  source-only bridge.
- Finite semialgebraic selection can select a target exceptional stratum of
  source dimension; it does not make that stratum target-open.
- Fixed-full restoration requires an actual target attachment and boundary
  transport. These are missing at a source bridge swallowed by one target
  blob.
- One- and two-port probes reconstruct words between already corresponding
  factors. They do not establish the factor correspondence.

The exact K3P tree--ordinary-sunlet separator can recover that particular
three-port decoration pointwise, but it does not exclude a target blob that
swallows a source bridge.

## 5. Exact physical counterexample to the proposed inference

The frozen tree--theta package gives an actual K3P realization of the same
exceptional-locus mechanism.

Let (h>0) satisfy (5h^4=1), with (2/3<h<7/10). The exact verifier
reconstructs a three-leaf K3P tree and a strict level-2 theta trinet with the
same distribution and strictly positive transition probabilities. At the
collision:

\[
\operatorname{rank}D\Phi_{\rm tree}=9,
\qquad
\operatorname{rank}D\Phi_{\theta}=15,
\]

and the target rank witness is

\[
\det J_*
=\frac{h(10h^2+1)}{2^{61}3^4 5^{14}}>0.
\]

Thus the theta map is a submersion onto the full normalized fifteen-
dimensional K3P tensor space. The inverse-function theorem supplies a
physical analytic theta section for every nearby tree tensor. The local
theta preimage of the tree model has dimension

\[
29-(15-9)=23.
\]

For example, the nonzero ambient cubic

\[
F_{m tree}
=q_{CGT}q_{GTC}q_{TCG}
-q_{CTG}q_{TGC}q_{GCT}
\]

vanishes on every three-star K3P tree by direct exponent cancellation. Since
the theta map is ambient-submersive, its pullback is not identically zero;
nevertheless it vanishes on the entire contained tree germ. This is the
precise phenomenon that invalidates the reverse generic-cut inference.

The exact tangent certificate also gives a strict continuous-time branch
with the same tree distribution. Hence open stochastic inequalities do not,
by themselves, prevent an analytic section from lying in a proper target
algebraic locus.

This theta topology is outside the strongly tree-child class: in its fixed
semi-directed graph, each of the two vertices (p,q) tails two retained
reticulation arcs and has only one ordinary incidence. The witness is
therefore **not** a counterexample to K3P-SAME. It is an exact counterexample
to treating generic target nonvanishing, positivity, or target dominance as
if they implied target-genericity along a source-relative section.

## 6. Exact remaining theorem obligation

Any one of the following would repair the global necessity proof:

1. prove pointwise K3P cut recovery throughout the strict domain;
2. prove the weaker strong-class statement that no physical analytic
   source-open cut germ lies in the cut-rank locus of a target noncut;
3. extend the exact atlas to every multi-blob-source-to-single-blob-target
   superfactor relation created by a lost split and certify zero survivors; or
4. independently prove that every directed containment in the strong class
   has equal source and target image dimensions.

None of these statements is present in the audited package. Generic cut
recovery alone is not a replacement lemma.

## 7. Replay and adversarial checks

From this directory run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_global_logic.py
PYTHONDONTWRITEBYTECODE=1 python3 test_global_logic_mutations.py
```

The first command binds all inputs, checks the exact logical model, replays
the complete K3P tree--theta certificate, independently confirms that the
theta violates the strong incidence criterion, and validates the JSON
verdict. The second rejects fourteen mutations, including source/target
reversal, promotion of the missing inclusion, invented target regularity or
dimension equality, circular extension of the atlas, and mislabelling the
outer witness as strongly tree-child.
