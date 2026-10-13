# Independent audit of the Bernoulli lower bound

Source: family 259, `A group without fixed price`, read-only checkout
`/Users/alec/Desktop/math` at commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
Reviewed file hashes are recorded in `reviewed_sources.json`.

## Target, criteria, and current conclusion

The target is the source's precise inequality

\[
\operatorname{Cost}(\mathcal R_{\Gamma\curvearrowright X})
\ge 1+\eta,
\qquad \eta=\alpha/100>0,
\]

where `X` is the free conull restriction of the Lebesgue Bernoulli action,
`Gamma = A *_J (J x Z)`, `A=F(a,b_1,...,b_99)`,
`J=<b_1,...,b_99,w>`, and `w=ab_1ab_2...ab_99a`.
The exact hypotheses on alpha are `0<alpha<1/200` and `K alpha^3<1/2`,
with `K=e^96 96^99/95^95`.

Success for this audit means reconstructing every implication of the lower
bound, identifying any counterexample or unsupported transition, and
certifying a positive parameter without floating-point assumptions. An
audit's failure to find a defect is distinguished from a mechanized proof.

Current outcome: **no fatal defect identified in the full lower-bound
chain**. Every mathematical implication in that chain has a checkable
argument in the supplied source. A second independent planar-only adversarial
review completed with the same outcome; see `planar_falsifier/AUDIT.md`.
The independent L2-Betti bridge,
literature priority, and source-publication assessment are outside this
assigned audit and must be integrated by the parent researcher.

## Chain and line-referenced findings

### 1. Free Bernoulli action and relative deployment

- `build/group-actions.tex:105-124` explicitly constructs the action,
  proves freeness from the independent coordinates at 1 and g, and
  makes the restriction invariant and conull. No ergodicity hypothesis
  enters the lower-bound chain.
- `build/deployment.tex:45-68` justifies finite near-optimal graphings:
  after truncation, a finite group generating set supplies precisely
  those generator edges not already connected. The missing domains
  decrease in measure to zero.
- `build/deployment.tex:77-114` keeps the enlarged measure unnormalized.
  Subdivision adds exactly lambda(Z)-1 to graphing cost. The sheetwise
  projection is measure preserving even though the global projection
  is many-to-one.
- `build/compression.tex:154-196` deletes one *indexed* paid edge per
  finite supplied class outside the retained complete set. The two
  orientations cannot delete the same indexed edge twice because each
  choice strictly decreases distance. Finite-class counting gives the
  exact deleted cost.
- `build/compression.tex:198-257` handles the many-to-one collapse map
  by splitting into pieces on which its two endpoints agree with
  enumerated ambient partial isomorphisms. Each piece is then a true
  measure-preserving partial isomorphism. Overlaps of images do not
  invalidate summed graphing cost.
- `build/deployment.tex:128-160` telescopes the compression savings;
  both factor relations increase, even though the graphing families
  themselves do not increase. There is no unjustified monotone limit
  of graphing costs.
- `build/deployment.tex:167-207` exhausts the entire pulled-back
  J-relation. A shortest alternating chain whose endpoints are
  J-related would otherwise give an alternating factor word outside
  J with product in J, forbidden by amalgam normal form. Infinite
  J-classes then give kappa(S_n) -> 0 by dominated convergence.
- `build/deployment.tex:213-256` projects at each *finite* stage and
  obtains an admissible relative A-graphing after supplying R_J.
  The same shortest-chain normal-form argument proves generation of
  R_A. Consequently Cost(R_Gamma) >= 1+delta_X.

Finding: the lower-cost deployment proof is self-contained and its
normalization, monotonicity, and source/target splitting are consistent.

### 2. Transfer to ranks of finite exact A-models

- `build/finite-models.tex:41-52` correctly reorganizes the restriction
  of the Gamma Bernoulli action as a Bernoulli A-action with base
  Omega=[0,1]^(A\\Gamma).
- `build/finite-models.tex:54-78` constructs the word-valued cocycle
  theta(v,g). It is essential that this remembers the *group label*,
  not merely finite-action endpoints. Its defining row kills w and
  it kills all b_i; hence it kills every J-label at every source.
- `build/finite-models.tex:97-132` first fixes finitely many valid path
  *words equal to a in A*. Freeness of the original action guarantees
  that equality. Cylinder approximation changes domains only, never
  the words. Inverse-domain tests use the correct additional inverse
  displacement.
- `build/finite-models.tex:136-156` requires independence only among
  the finitely many coordinates at a *single source*, rather than
  among different sources. The exceptional-source estimate follows
  from the stipulated vanishing fixed-point fractions.
- `build/finite-models.tex:158-191` uses the cocycle identity to express
  every successful source generator x_v from the paid list. Adding
  x_v at every failed source completes generation. Taking expectation
  is valid because rank is bounded by this list for *every* labeling.

Finding: the transfer does not require any finite Gamma-model, does not
assume finite configurations are free, and fixes all local tests before
taking the model limit. It gives the asserted
delta_X >= limsup rk(D_V)/|V|.

### 3. Existence of expanding models with sparse overlaps

- `build/finite-models.tex:222-231`: a,u_1,...,u_99 is indeed a free
  basis. The inverse formula b_i=a^-1 u_(i-1)^-1 u_i is correct.
- `build/finite-models.tex:233-261`: the containment union bound is
  correct. For |T|=s, the 99 independent permutations contribute
  `(96s/n)^(99s)`, and the two binomial coefficients contribute
  powers s and 95s. The residual power is `99-1-95=3`, rather than
  an omitted or negative exponent. The fixed-size/tail split proves
  the sum of failure probabilities tends to zero.
- `build/finite-models.tex:263-293`: until the first repeated vertex,
  a freely reduced word always requests a new domain/range entry.
  An already exposed entry at the current new vertex could only
  immediately invert its incoming edge. The first-collision union
  bound gives the stated expected fixed-point fraction, and the
  simultaneous diagonal choice is valid.
- `build/finite-models.tex:295-317`: repeated columns and two-column
  row overlaps imply fixed points of nonidentity words from fixed
  finite lists. The proof explicitly handles u_0=1, including two
  zero indices in opposite positions. No growing-word uniformity
  estimate is being silently assumed.

Finding: both expansion and b(V_k)=o(n_k) hold along the same sequence
used in transfer. The source proves existence; it does not provide a
practically small deterministic model. That is not a gap in this claim.

### 4. Coefficient subgroup and saturation

- `build/rank-surgery.tex:48-75` selects a genuinely minimal finite
  labeled graph among graphs of bounded first Betti number. Pruning
  gives no degree-one vertices, and at most 3 beta arcs result.
- `build/rank-surgery.tex:78-113` adds at most 100b+90 beta initial/arc
  columns. If s=floor(alpha n) row additions occurred, the first s
  rows would have N(T) contained in a set of size less than 96s,
  contrary to expansion. Fewer than s additions leave |S|<=92alpha n<n.
  Every retained row is good, has at most 9 S-occurrences, and thus
  has at least 91 distinct positive U-letters.
- `build/rank-surgery.tex:115-130` is **not a circular use of a
  Freiheitssatz**. H is the actual subgroup of D generated by S.
  The right-hand relative presentation maps to D, and the original
  presentation maps back because omitted rows hold in H and every
  other row is retained. Both composites fix the generators. Hence
  this is an isomorphism, and the coefficient group embeds.

Finding: the injectivity input needed by the planar lemma is legitimately
supplied by the relative presentation, including when H has torsion or
is not finitely presented.

### 5. Planar lemma: critical topological and combinatorial checks

- `build/planar.tex:67-100` minimizes the number of genuine mixed
  relators in L=H*F(U). It uses only finitely many true H-relations
  to realize any individual equality, and never assumes the finite
  approximation K_H has the same fundamental group as H.
- `build/planar.tex:102-138` obtains disjoint cooriented inverse-image
  tracks of points internal to U-circles. Boundary signs are opposite
  at paired endpoints. If the disk/arc graph were disconnected, a
  separating curve avoiding the track points represents a conjugate
  of an H-element; capping its mixed holes makes it trivial in D.
  H-injectivity then permits replacement with zero mixed relators,
  contradicting minimality. Closed tracks need not be removed.
- `build/planar.tex:140-158` excludes inner loops by uniform sign.
  Copies of the same relator joined at its unique occurrence of u
  have inverse based loops at the track point; that track is
  constant. Their neighborhood has trivial boundary in L and
  removes a dipole. Different relators have at most one joining
  edge by their one-generator overlap bound.
- `build/planar.tex:160-186` compares coefficient gaps as actual
  H-elements. Collapsing the U-circles to the basepoint eliminates
  track-point conjugations; each bigon gives exactly inner-gap times
  inverse-outer-gap equal to 1. This is stronger than matching modulo
  a conjugacy class, and it is what rank surgery later needs.
- `build/planar.tex:192-220` has correct Euler sign and constants:
  sum c(v) <= 2E-2F, and V=N+1 gives
  sum(2-c(v)) >= 2N-2E+2F=2. Nonbigon face weights are at most ell-2
  including repeated face walks and outer loops.
- `build/planar.tex:222-256`: any positive inner vertex has outer
  edges. Every nonbigon gap among them costs at least 1; a gap with
  h inner edges costs 1+(h-1)/3. Positivity therefore permits one
  nonbigon gap and at most 3 inner edges. It exposes a single
  interval with at least m-3 exterior letters, with contribution at
  most 1. Total contribution >=2 forces two such vertices unless a
  full cyclic string already gives the full-match conclusion.
  Track endpoints make the two intervals exterior-disjoint.

Finding: two independent adversarial reads found no failure in tracks,
connectedness, dipole removal, exact gap matching, or curvature.
The independent child began without this audit's surrounding context.

### 6. Shortest loop, seam, and graph surgery

- `build/rank-surgery.tex:133-159` proves linear H-reduction of the
  shortest loop. A trivial S-gap between inverse U-letters either
  deletes a closed detour, or lets one edge slide across the gap and
  fold against the other. The slide preserves all D-valued loops
  because the gap is trivial in D; folding lowers edges without
  increasing graph rank.
- `build/rank-surgery.tex:161-185` shows the word P x_j^-1 is nontrivial
  in L although trivial in D. If cyclic cancellation removed all
  exterior letters, its residual conjugate H-element would be
  trivial in D and therefore H, a contradiction. Every cancellation
  begins at the appended letter and then works only from the ends
  of P; there is at most one seam letter or seam gap.
- `build/rank-surgery.tex:187-212` uses exterior disjointness so that
  one of the two long intervals avoids the seam. The resulting Q
  has at least 88 distinct exterior indices. Equality of H-gaps
  gives equality in D with the original row segment, and its
  complementary original word has length at most 12. An empty
  complement is replaced with a length-two identity word, so the
  inserted path has a positive number of edges.
- `build/rank-surgery.tex:214-237` forces a single arc traversal
  containing at least 31 exterior edges: otherwise complete arcs
  contribute zero and the two partial arcs contribute at most 60.
  Taking I from its first through its last exterior edge makes its
  boundary edges exterior. Distinct exterior indices in Q then
  prohibit Q_1 and Q_2 from entering I or from starting/ending in
  its interior. This also covers a closed I.
- `build/rank-surgery.tex:243-269` adds a path of k<=12 edges and
  deletes the l>=31-edge arc interior. Q_1^-1 Z Q_2^-1 is a retained
  bypass, so connectivity and all old D-valued loops survive.
  Both E and V change by k-l (including closed paths), preserving
  graph rank while reducing edge count by at least 19.

Finding: the path/arc distinction is handled; there is no use of an
arbitrary repeatedly traversed segment as though it were removable.
The deterministic theorem consequently gives rk(D_V)>alpha n/100.

## Exact positive eta certificate

Choose

\[
\alpha=2^{-61},\qquad
\eta=\frac{1}{100\cdot2^{61}}
=\frac{1}{230584300921369395200}.
\]

Indeed,

\[
K=e^{96}\,96^4(1+1/95)^{95}
<e^{97}\,96^4<3^{97}\,96^4,
\]

using the elementary inequalities `(1+1/95)^95<e<3`.
The remaining `K alpha^3<1/2` follows from the exact integer comparison

\[
2\cdot3^{97}\cdot96^4<2^{183}.
\]

`verify_constants.py` checks that comparison and the other rational
inequalities with arbitrary-precision integers/Fractions. It also gives
the exact height `M=22827845791215570124801` satisfying `99/M<eta`.
No approximation of e or floating-point comparison is needed.

## Exact remaining scope

An optional additional deduction is preserved in the child memo: because
inner-inner tracks join opposite relator-disk signs, the inner graph is
bipartite. Assigning weight 1/2 whenever an inner corner meets an inner
edge, and weight 1 when both edges meet O, preserves the face bound and
limits a positive vertex's exceptional gap to at most two inner edges.
This improves m-3 to m-2 (already for m>=4). I independently checked the
face and exceptional-gap inequalities, including repeated walks and O
loops. The enhancement is not needed for the inherited lower bound and
is not incorporated into the source.

The source's lower chain reaches Cost(R_X)>=1+eta. It does **not itself**
establish beta_1^(2)(R_X)=0, so that additional bridge must be proved
separately for the proposed follow-on construction. This audit records
no novel lower-bound theorem beyond the source and does not infer source
validity from its announced conclusion or from prior triage.
