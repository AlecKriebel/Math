# RBM(4,3): verification of a prior negative resolution

Problem 20002559 / AIM-PROBABILITY-0001. Investigation date: 5 October 2026.

## Disposition and credit

The question has a negative answer supported by an already published, explicitly
unrefereed computer-assisted proof. This investigation independently reconstructed
its finite certificate and checked the argument connecting that certificate to
the full Euclidean closure. The recommended disposition is **verified prior
resolution / already solved**, after the separately required uninvolved audit.
This is one substantive approach, not five exhausted approaches. There is no
claim of a new obstruction or historical priority in this investigation.

The result belongs to **Anonymous, _An eight-point obstruction to universality
of RBM(4,3)_, version 0.2.0-candidate, 6 September 2026**,
[DOI 10.5281/zenodo.22550044](https://doi.org/10.5281/zenodo.22550044).
The verified source is the versioned
[repository](https://github.com/ipitchford/rbm43-eight-point-obstruction/tree/fac57cd9a497a509d443f34f9b9843f6c7a7042f).
Its public provenance names Ian Pitchford / Evidence Press as maintainer/publisher
and discloses AI assistance. Anonymous remains the scholarly attribution.
No evidence establishes that this is the user's prior work.

Independent computational reconstruction is not human specialist review,
journal acceptance, or proof-assistant verification. The source's unrefereed
status is retained. The finite identities, exact coverage and mathematical
implications are verified here rather than accepted from the press announcement.

## 1. Recovered question and model

The catalog title about local surjectivity is a summary of an earlier partial
attempt. The actual question asks whether the closure of the binary model with
four visible units and three hidden units is the whole probability simplex on
sixteen visible states. The full imported problem record and its complete
research report were inspected, not only the title or summary.

The public UnsolvedMath item and canonical AimPL section were unavailable through
the web tool. The independent primary-source confirmation is the
[AIM workshop summary, page 2](https://aimath.org/pastworkshops/boltzmannrep.pdf),
which specifies the dimensions and arbitrary approximation throughout the
15-dimensional simplex. Its workshop took place in September 2018. The report
distinguishes known parity-support results from a proposed proof outline for
arbitrary eight-vertex supports; the outline is not an established theorem.

For x in {0,1}^4 and h in {0,1}^3, use real finite parameters b, c, W and

\[
 Q_\theta(x,h)=Z_\theta^{-1}
 \exp\!\left(b\cdot x+c\cdot h+\sum_{i,j}W_{ij}x_i h_j\right),
 \qquad p_\theta(x)=\sum_h Q_\theta(x,h).
\]

Write R for the Euclidean closure of the visible laws. On this finite space this
is also total-variation closure. It is not Zariski closure. Finite parameter
values produce only strictly positive laws; the problem permits arbitrarily
large parameters and targets with zeros. It asks about density, not merely
finite-parameter exact representation or local full dimension.

## 2. The credited obstruction

Define

\[
 S=\{0000,0001,0010,0100,0111,1001,1010,1100\}.
\]

The prior result, independently checked below, is

\[
 p(S^c)\geq\left(\frac{\min_{x\in S}p(x)}8\right)^4
 \qquad (p\in R).                                      \tag{1}
\]

Consequently no law having support exactly S is in R. In particular, the uniform
law q on S is excluded. This is an obstruction to approximation, not just the
automatic fact that a zero-containing law has no finite-parameter representation.

Let u be uniform on the full four-cube and put

\[
 q^+=(1-2^{-25})q+2^{-25}u.
\]

This law is strictly positive, with coordinates 67108863/536870912 on S and
1/536870912 off S. The inherited quantitative bounds are

\[
 \inf_{p\in R}d_{TV}(p,q)\geq2^{-25},\qquad
 \inf_{p\in R}d_{TV}(p,q^+)\geq2^{-26}.                 \tag{2}
\]

The constants are certified lower bounds, not optimal distances or practical
training-error estimates. In particular, neither exact representation nor
arbitrary approximation of every strictly positive distribution is possible.

## 3. Complete analytic bridge

For a joint state z=(x,h), define the twenty-dimensional integer vector

\[
 A_z=(1,x_1,x_2,x_3,x_4,h_1,h_2,h_3,(x_i h_j)_{i,j}).
\]

Consider two multisets L and T of joint states with the same total feature sum,
\(\sum_{z\in L}A_z=\sum_{z\in T}A_z\). The constant coordinate says that both
multisets have the same cardinality D. Substitution of the exponential-family
formula therefore gives

\[
 \prod_{z\in L}Q_\theta(z)=\prod_{z\in T}Q_\theta(z).  \tag{3}
\]

Every exponent of every parameter agrees, and both normalizing denominators
are Z^D. Repetition in a multiset is ordinary positive integer multiplicity.

The finite certificate establishes this precise fact: for **every** function
f:S→{0,1}^3, one checked identity (3) has all its T states among (x,f(x)),
while L has o≥1 states, counted with multiplicity, over S^c, and D≤4o.
Section 4 describes an exhaustive reconstruction of this universal finite
quantifier. The maximum D is seven; replacing D/o≤4 by D≤4 would be incorrect.

For a finite RBM law, choose for each x∈S a hidden state maximizing Q(x,h).
There are eight hidden states, so each selected joint probability is at least
m=(min_S p)/8. Apply the finite certificate to this selector. Put r=p(S^c).
Every off-S joint probability is at most r, and every remaining joint probability
is at most one. Equation (3) yields

\[
 m^D\leq\prod_{z\in T}Q(z)=\prod_{z\in L}Q(z)\leq r^o.
\]

Because 0<m≤1 and D/o≤4, we obtain r≥m^(D/o)≥m^4. This proves (1) for all
finite real parameters, without any bound on their size. Both sides of (1)
are continuous in the visible probability vector, so the same inequality holds
at every point of R. When min_S p=0 the extended inequality remains valid.
This continuity argument includes all possible multi-scale escapes to infinity;
it does not require a classification of their leading or subleading terms.

For q uniform on S, the left side of (1) vanishes and the right side is
(1/64)^4>0. Thus R is a proper subset of the simplex, which fully answers the
recovered question in the negative.

For completeness, if δ=d_TV(p,q), then p(S^c)≤δ and min_S p≥1/8−δ. If δ≥1/128,
the first bound in (2) already holds. Otherwise min_S p>15/128, and (1) gives
δ>(15/1024)^4=50625/2^40>32768/2^40=2^(-25). Moreover d_TV(q,q^+)=2^(-26), so
the triangle inequality gives the second bound in (2). The coordinate formulas,
normalization, direct violation of (1), and all rational comparisons are also
checked by the independent program.

## 4. Independent finite verification

Only the published proof, printable appendix and JSON certificate were used as
mathematical input. No producer executable was retrieved or executed. The newly
written standard-library checker does the following:

1. Parses all 42 multiset identities from the printable appendix.
2. Expands the JSON multiplicities and verifies exact agreement with every
   printed row, including its degree and off-support multiplicity.
3. Reconstructs all 128 feature vectors directly from binary indices and checks
   all twenty integer coordinates of every identity.
4. Enumerates the full signed coordinate-permutation group of the visible cube
   and retains exactly its six S-preserving elements. It independently enumerates
   all 48 hidden cube symmetries.
5. Directly rechecks the feature identity, off-support condition and exponent
   ratio for all 42×6×48=12,096 transformations. Symmetry invariance is therefore
   not an unchecked computational premise.
6. Converts each transformed right multiset into its required selector values.
   The result consists of 6,608 distinct partial assignments.
7. Enumerates the free base-eight digits of every partial assignment, marking
   its entire cylinder in an array indexed by all **8^8=16,777,216** selectors.
   All entries are marked. There are 64,569,344 markings counting overlaps.

The enumeration deliberately does not normalize the selector at one visible
state. It therefore verifies more raw selector indices than the producer's
normalized enumeration, while proving the same finite statement. Maximum
degree seven and maximum ratio four are independently recovered.

Normal and optimized Python runs agree. Eight hostile controls reject a changed
support, changed or negative multiplicity, omitted JSON row, invalid printed
identity, an identity without forbidden states, an empty cover, and an
insufficient cover of otherwise valid identities. The same rejection gates
remain active under python -O. Saved receipts contain only verification metadata,
not imported certificate contents.

## 5. What the earlier partial approach did and did not show

The prior imported attempt established a positive Hadamard-factor formulation,
an explicit full-rank local chart, and necessary tropical cancellation equations
for strictly positive closure points omitted by the finite image. Those results
do not imply global density. The old determinant was recomputed with exact
rational elimination:

\[
 -4292546820857203/11884241136598188669271898437500\ne0.
\]

The new verification does not claim this determinant as new. It confirms that
local full dimension and non-universality coexist.

The topology distinctions also explain why several relaxations do not resolve
the question by themselves:

- Three positive two-term product factors are more constrained than generic
  complex rank-two factors. The 2025 Hadamard-rank paper explicitly separates
  ordinary-topology semialgebraic approximation from Zariski filling.
- The maximum supermodular rank on four bits is three, so merely checking a
  three-term supermodular decomposition cannot exclude a four-bit log table.
- Summing over three hidden bits gives a mixture of eight product distributions,
  but that relaxation is too broad: any four-bit law is a mixture of at most
  eight products by conditioning on its first three bits. The shared RBM
  parameters impose the additional constraints used in (3).
- Simple maximum-mode counts and parameter counts lose the joint-state
  compatibility captured by the finite selector identities.
- Necessary leading ReLU cancellation equations do not characterize all
  subleading limits. Inequality (1) avoids that unresolved classification.

The familiar sufficient upper bound of seven hidden units is not the best bound
already recorded in the 2018 review: it gives an upper bound of six for four
visible bits. Combining that established upper bound with the credited negative
(4,3) result gives 4≤m_min≤6. This investigation does not settle which of four,
five or six hidden units is optimal.

## 6. Prior-work and search checks

The actual prior imported attempt was read in full. Targeted searches of
AlecKriebel/Math for the ID, problem code, RBM and the (4,3) combination found no
matching earlier implementation or PR. A complete recursive traversal of the
repository's problems subtree returned 725 entries and no matching target path;
all 62 entries of the campaign attempts directory were also inspected without
a target match, and branch search for this ID was empty. The repository-wide recursive tree
endpoint failed, so this is a bounded search, not a proof of repository absence.
An adjacent already completed RBM radius investigation addresses a different
model and objective and is not a previous solution of this problem.

The public search located the September 2026 obstruction, predating this work
and later than the imported August report. The source repository, pinned commit,
citation file, provenance and repository copy of deposit metadata were checked; no authorship
connection to Alec Kriebel was inferred from topic similarity. No verified
withdrawal, correction or later specialist acceptance was found in the targeted
search. Such absence is not a comprehensive citation-history claim.

Because this first substantive approach found and reconstructed a complete prior
proof, no speculative additional research approaches were pursued. The remaining
gate for this packet is uninvolved audit of both the exact checker and the
written analytic bridge. There is no identified mathematical gap in the fixed
(4,3) negative answer after author verification; larger-model thresholds and
optimal approximation constants are different questions.

## References

- Anonymous (2026). _An eight-point obstruction to universality of RBM(4,3)_,
  v0.2.0-candidate. [Versioned proof](https://github.com/ipitchford/rbm43-eight-point-obstruction/blob/fac57cd9a497a509d443f34f9b9843f6c7a7042f/proof.md),
  [printable certificate](https://github.com/ipitchford/rbm43-eight-point-obstruction/blob/fac57cd9a497a509d443f34f9b9843f6c7a7042f/appendix.md),
  [machine certificate](https://github.com/ipitchford/rbm43-eight-point-obstruction/blob/fac57cd9a497a509d443f34f9b9843f6c7a7042f/certificate.json).
- AIM. _Boltzmann machines: Workshop summary_, page 2.
  https://aimath.org/pastworkshops/boltzmannrep.pdf
- Montúfar (2018). _Restricted Boltzmann Machines: Introduction and Review_,
  Sections 6 and 9. https://arxiv.org/abs/1806.07066
- Sonthalia, Seigal and Montúfar. _Supermodular Rank: Set Function Decomposition
  and Optimization_, Theorem 10, 2023 preprint.
  https://arxiv.org/abs/2305.14632
- Antolini, Montúfar and Oneto (2025). _Hadamard ranks of algebraic varieties_,
  especially Section 5.5. https://arxiv.org/abs/2510.05231
