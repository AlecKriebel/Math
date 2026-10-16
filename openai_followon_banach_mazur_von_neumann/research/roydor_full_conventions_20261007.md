# Independent audit of the complete supplied Roydor article

Audit date: 2026-10-07. Auditor: internal AI research subagent. This is a
primary-input/conventions audit, not a final-package review, upstream proof
certification, novelty determination, or publication clearance. No external
individual was contacted. No manuscript, Git state, or publication artifact
was changed.

## Verdict and exact claim

The actual supplied article's **Theorem 1.2 explicitly assumes that the fixed
von Neumann algebra M has separable predual**. It does not state the original
arbitrary, possibly nonseparable target. Its ordinary norm, coefficient
module, actual-image cohomology, predual, and Jordan/isometry conventions
otherwise match the intended composition with family 295. In particular,
ordinary actual-image H^3(M,M)=0 supplies its weaker assumption that B^3(M,M)
is closed in Z^3(M,M).

Consequently, conditional on the mathematical validity of the pinned
family-295 theorem, the **direct theorem-to-theorem consequence** is:

> For every complex von Neumann algebra M with separable predual there is
> epsilon_M > 0 such that, for every complex von Neumann algebra N, either
> d_BM(M,N) < 1 + epsilon_M or d_BM(M_*,N_*) < 1 + epsilon_M implies that M and
> N are Jordan *-isomorphic. The same epsilon works for these two implications.

The arbitrary nonseparable target requires an additional proof extension or a
separate correctly scoped theorem. There is a concrete extension mechanism
in Roydor's proof; this audit does **not** identify a counterexample or declare
that extension impossible. It does rule out describing the full target as an
immediate application of the literal Theorem 1.2, or citing the slides as if
they had the same scope as the article.

## Source identity and completeness

Primary file inspected:

- `sources/roydor/roydor2020_user_supplied.pdf`
- SHA256: `2320e92723841bd9414c4d846a489bbe78d01a03403b8078ca43354407cfacb4`
- Size: 431,430 bytes; PDF 1.4; 26 pages; not encrypted.
- Title: Jean Roydor, *Banach-Mazur stability of von Neumann algebras*.
- First page prints DOI `10.1142/S1793525321500151`, received 18 May 2020,
  revised/accepted 26 August 2020, and published 11 December 2020.
- The file carries a World Scientific header, the production stamp
  `December 9, 2020 15:25 WSPC/243-JTA 2150015`, and `2nd Reading`. Its own
  printed article pagination is 1-26. Metadata reports creation 2020-12-09
  and modification 2020-12-12.
- Pages 1-4 are the introduction and theorem statements; pages 4-11 contain
  Section 2; pages 11-17 contain Section 3; pages 18-24 contain Section 4;
  pages 25-26 contain acknowledgments and the complete references, ending
  with reference 36. The full proof is present, not merely an abstract,
  opening-page preview, slides, or search snippet.

The existing layout extraction has SHA256
`30fb985def03134ed115779e02a70e95432bd21bcf005c5bb3232cbd91f4414e`.
I independently extracted pages from the actual PDF with `pdftotext` and read
the complete article text, paying particular attention to the statements,
Section 3 decomposition, and all of Section 4. I rendered and visually
inspected printed pages 1, 2, 13, 20, 21, 22, 23, and 26. Rendering was to
memory, so no replacement PDF or persistent render files were created.
The separability condition and the differential misprint described below
were verified in the pixels, not inferred from extraction alone.

The exact inspected version should be identified as the **supplied complete
2020 publisher-formatted article, internally paginated 1-26**. It is not
evidence that I downloaded and byte-compared the final issue-paginated PDF.
Publisher-deposited [Crossref metadata](https://api.crossref.org/works/10.1142/S1793525321500151),
read 2026-10-07, matches the DOI/title/author, reports online publication
2020-12-11, print publication September 2022, volume 14, issue 03, pages
767-792, and a publisher PDF link marked `vor`. Its returned `relation` was
empty and `update-to` absent. These metadata facts do not establish the
absence of all later textual corrections. All theorem/page citations below
refer to the supplied article's printed pages, not an assumed offset into
the 2022 pagination.

## Exact conventions against the primary article

| Issue | Actual primary evidence | Audit result |
| --- | --- | --- |
| Distance | Page 2 defines d(X,Y) as infimum of ||L|| ||L^{-1}|| over bounded linear isomorphisms L:X -> Y. | Ordinary Banach-Mazur distance; no cb norms and no logarithm. Taking the empty infimum as infinity agrees with the requested convention. |
| Field | C*-algebras are used throughout; page 5 uses complex scalars z, and linearity in z is essential to the proof of Proposition 2.2. Page 13 uses M_2(C). | The intended maps are complex linear. There is no blanket sentence explicitly declaring the field on page 20, so this is the standard complex C*-algebra convention confirmed by the proof, not a quotation of an absent declaration. |
| Cohomology cochains | Section 4.2.1, page 20: L^k(A,X) is the space of all bounded k-linear maps A^k -> X with the usual multilinear norm; L^0(A,X)=X. | Ordinary bounded cochains. No normality, separate-normality, positivity, or complete-boundedness requirement is imposed in this definition. |
| Coefficients | Theorem 1.2, page 2, and Lemma 4.4/Theorem 4.5, pages 20-21, use (M,M)/(A,A). | Self-module under left/right multiplication, as required. No coefficient replacement by B(H), M_*, or a different dual module. |
| Coboundaries | Page 20 defines B^k(A,X)=Ran(delta^{k-1}). | Actual image, without norm closure. |
| Cocycles/cohomology | Page 20 defines Z^k=Ker(delta^k), H^k=Z^k/B^k. | Unreduced cohomology. H^3=0 is enough for the closedness hypothesis. |
| Norm/topology of closedness | L^k has its usual Banach multilinear norm; Theorem 1.2 asks that B^3 be closed in Z^3. | Norm closedness in the cochain Banach space, equivalently relative norm closedness in the closed subspace Z^3. |
| Fixed algebra | Theorem 1.2, page 2, fixes M with separable predual and cohomology assumptions. Page 3 says the epsilon depends a priori on M. | This is a local threshold depending on M. No universal epsilon follows from this literal composition. |
| Comparison algebra | Theorem 1.2: for any von Neumann algebra N. | N must be a von Neumann algebra; N is not assumed separately to have separable predual. It is not an arbitrary nearby Banach space. |
| Threshold | Theorem 1.2 assertions (iv) and (v) use strict inequalities d < 1+epsilon. | No conclusion at equality is supplied by this theorem. |
| Predual | Theorem 1.2 calls the predual L^1(M); page 24, Remark 4.9, calls preduals noncommutative L^1 spaces. | Canonical predual M_*, not the full Banach dual M^* and not a choice of faithful trace. |
| Jordan structure | Page 7 defines x circ y=(xy+yx)/2; pages 22-23 construct a central direct sum of a *-isomorphism and an anti-*-isomorphism. | Conclusion is Jordan *-isomorphism. An ordinary surjective isometry may carry an extra unitary multiplier. No *-isomorphism conclusion for the entire algebra follows. |

### A real printed error in the displayed differential

The page-20 display of delta^k has summation upper limit k-1 and final sign
(-1)^k, while its argument tuple has k+1 inputs. Those are not the standard
Hochschild indices/signs, and the error survives visual inspection. The
intended conventional differential is

\[
 (\delta^k\phi)(a_1,\ldots,a_{k+1})
 =a_1\phi(a_2,\ldots,a_{k+1})
 +\sum_{i=1}^{k}(-1)^i
   \phi(a_1,\ldots,a_ia_{i+1},\ldots,a_{k+1})
 +(-1)^{k+1}\phi(a_1,\ldots,a_k)a_{k+1}.
\]

This is more than an OCR ambiguity. For k=1, the printed display would give
delta^1(phi)(a,b)=a phi(b)-phi(a)b. Combined with the printed correct
delta^0(x)(a)=ax-xa, it gives

\[
 (\delta^1\delta^0 x)(a,1)=xa-ax.
\]

In M_2(C), take x=e_11 and a=e_12 to obtain e_12, contradicting the very next
sentence's assertion delta^k delta^{k-1}=0. The corrected standard formula
does give zero. The section identifies itself as the Hochschild complex and
cites Sinclair-Smith; Theorem 4.5 explicitly invokes Johnson's ordinary
Hochschild theorem. Therefore the coherent dependency is the standard
Hochschild complex with this display treated as a typographical error.
Do not transcribe the erroneous display into the new paper, or claim the
two sources' literal displayed formulas agree. This audit did not verify
whether the final issue PDF corrected the display.

### Why actual H^3 vanishing supplies exactly what Roydor needs

For the corrected standard differential, delta^3 is bounded on C_b^3(M,M)
(with norm at most 5), so Z^3=Ker(delta^3) is closed. Actual-image H^3=0
means B^3=Z^3, not merely that B^3 is dense in Z^3. Thus B^3 is closed in
Z^3, and also in C_b^3. The implication uses no uniform quantitative
primitive estimate and no cb or normal-only theorem.

## Pinned upstream convention comparison and limit of this review

The upstream clone reports HEAD
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`, exactly the pinned input. Its
family-295 path's last commit is also that commit. The local copied files
read for this audit agree byte-for-byte with that clone for the two
sections listed below. This clone was read only.

- `build/sections/01-introduction.tex`, SHA256
  `ddec01dc15fa257e3f1e85004b54225dd43df633bbdfa957de98353c069ce4b2`:
  defines C_b^k(M,M) as bounded **complex** multilinear maps, ordinary norm,
  the standard differential above, and the quotient by its actual image.
  Its main theorem quantifies over every complex von Neumann algebra and
  every k>=2, with no separability/type restriction.
- `build/sections/05-cohomology.tex`, SHA256
  `c6c8e63bac0e543624ac63fd50a046878ba7082a531115111563455682e4d437`:
  begins with separately normal cocycles, removes separability using
  conditional expectations and finite-set compactness, uses central cuts
  with an explicit homotopy, then applies the normal reduction to arbitrary
  bounded original cocycles. Its final paragraph explicitly obtains an
  actual bounded primitive and disclaims any complete-boundedness
  hypothesis.
- Copied `paper.pdf`, SHA256
  `56ec913df9fbe4a2daf371eec1cb06ddc5b544cf9defc838aab540f33171f753`.
- The manuscript README, attribution file, and `lean_scope_295.md` were
  read. A scope document's assertion is not a reproduced Lean check.

This establishes **semantic agreement of the claimed cohomology input**.
I read the cohomology argument, but did not independently reprove the
walk/Liouville/rigidity machinery or reproduce a full formal build here.
The project must continue to use its separate adversarial upstream audit
before promoting family 295 as a verified unconditional input. Neither
this conventions match nor the presence of a Lean scope file certifies
the central upstream mathematics.

## Isometry and canonical-predual equivalences, without separability

The following deductions hold for arbitrary complex von Neumann algebras.
They were also checked by an independent internal subagent given the actual
PDF and this narrow sub-question, before I received its reasoning.

Let J:M -> N be a bijective complex-linear Jordan * map. It is unital:
J(1) circ b=b for every b by surjectivity, and putting b=1 gives J(1)=1.
Both J and its inverse preserve positive elements, since a positive
element is h^2 for a self-adjoint h and J(h^2)=J(h)^2. Hence J is an order
isomorphism of the self-adjoint parts. Unital positive maps are contractive;
applying this to J and J^{-1} proves that J is an isometry.

For a bounded increasing positive net a_lambda with supremum a, the
element J(a) is its image net's least upper bound: any upper bound b pulls
back through J^{-1} to an upper bound of a_lambda. Thus J preserves
arbitrary bounded increasing suprema. This proves normality of J; the same
argument proves normality of its inverse. It uses nets, so has no
separability restriction. Consequently composition with J gives an
isometric bijection

\[
 J_*:N_*\longrightarrow M_*,\qquad \omega\longmapsto\omega\circ J.
\]

An ordinary complex-linear surjective isometry I between the algebras is
uJ, where u=I(1) is unitary, by Kadison's theorem (Roydor page 2 and
reference 17). Such I is also automatically normal, since fixed-unitary
multiplication is ultraweakly continuous. I itself need not be Jordan or
unital: x -> ix is an elementary example.

Conversely, the adjoint of an isometric bijection S:M_* -> N_* is an
isometric bijection S^*:N -> M, and Kadison supplies a Jordan
*-isomorphism. Also, for every bounded predual isomorphism S,

\[
 \|S^*\|\|(S^*)^{-1}\|=\|S\|\|S^{-1}\|,
 \qquad d_{BM}(M,N)\le d_{BM}(M_*,N_*).
\]

Thus a valid algebra-stability threshold automatically gives the predual
threshold with the same epsilon, whether or not M has separable predual.
These deductions do not remove the substantive separability condition on
Roydor's implication (v)->(i), and they do not establish normality of an
arbitrary intermediate bounded near-isometry.

## Where the proof uses scope and what a nonseparable extension must check

### Broad components actually present in the article

Theorem 1.1 (page 2; proof pages 18-20) has no separability hypothesis and
controls the respective I, II_1, II_infinity, III summands. It is continuity
of type decomposition, not already isometric rigidity of every type-I
summand.

Lemma 3.1 (pages 11-13) constructs nearly isometric compression maps,
including central compressions, without a separability restriction.
Proposition 2.13 (pages 10-11) constructs an isomorphism of central
projection lattices and extends it to a *-isomorphism of the centers,
also without a separability restriction. Since an order isomorphism of
complete projection lattices preserves arbitrary suprema, its bijection
handles uncountable central partitions as well as countable ones.

Theorem 3.2 (page 13; proof pages 13-17) has no separability hypothesis.
Its stated structural assumption is that the **finite** type-I part of the
source has only even homogeneous degrees. Its proof begins by halving the
unit into equivalent projections and working with a 2-by-2 matrix system.
Arbitrary infinite homogeneous type-I cardinalities can be halved, so
infinite cardinality alone does not obstruct this step. In particular,
all algebras without a type-I summand meet its structural assumption.

Theorem 4.5 (page 21) is the ordinary Banach-algebra multiplication
stability theorem attributed to Johnson [16, Theorem 2.1]. Its hypotheses
are H^2(A,A)=0 and closedness of B^3 in Z^3. It concerns bounded associative
bilinear multiplications, equivalent to maps on the Banach projective
tensor product. The construction in pages 21-22 explicitly uses a
self-adjoint conjugacy for * compatible transported products, producing a
*-isomorphism on one central piece and an anti-*-isomorphism on the other.

No separability use is visible in that non-type-I part of the proof. But
removing a hypothesis from the conclusion requires giving a proof with
its quantifiers controlled, not saying that the author never mentions the
hypothesis again.

### Uniformity over central corners is a checkable repair

The projection p produced by Theorem 3.2 depends on the comparison map.
Merely applying a separate existence theorem to pM with an unspecified
epsilon_{pM} would not produce a threshold fixed before N is chosen.
There is a standard explicit repair for the cohomological constants.

For a central projection p, define, in each positive degree,

\[
 (E_p f)(a_1,\ldots,a_k)=f(pa_1,\ldots,pa_k),\qquad
 (R_p F)(x_1,\ldots,x_k)=pF(x_1,\ldots,x_k),\quad x_i\in pM.
\]

The output of E_p lies in pM, included in M. Both are norm-one chain
maps, and R_p E_p=id. Centrality verifies the outer differential terms.
Open mapping supplies finite primitive constants K_2(M), K_3(M) when
actual H^2 and H^3 vanish. Extending a pM-valued cocycle by E_p, solving
it in M with one of these constants, and restricting by R_p gives the
same bound for **every** central p. Thus the Johnson proof's constants
can be controlled uniformly over the central pieces selected later.
For the weaker closed-range formulation, the analogous quotient norm
estimate also descends through these chain maps. This is a proof of
uniformity over central corners, not a uniform constant over all M.

This supplies a concrete nonseparable route for the no-type-I case using
Roydor's Theorem 3.2 and Theorem 4.5 rather than misquoting Theorem 1.2.
Any completed note claiming that extension should write out the above
uniformity step and ensure the involution-compatible Johnson correction
is being used in the scope claimed. This audit read Roydor's formulation
and use of Johnson, not the full original Johnson paper independently.

### The type-I place where the literal proof is narrower

At the bottom of page 22, the proof writes the type-I parts as

\[
 M_I=\bigoplus_{j\in J}L^\infty(\Omega_j,M_j),\qquad
 N_I=\bigoplus_{k\in K}L^\infty(\Sigma_k,M_k),
 \qquad J,K\subset\mathbb N\cup\{\infty\}.
\]

For separable-predual algebras this is the intended finite/countable-rank
picture. It does not itself express arbitrary nonseparable homogeneous
type I_kappa pieces. The proof on page 23 compares j,k, treating the
even/infinite case by Theorem 3.2 and the finite odd case by the even
(j-1)-corner. Infinite cardinalities need to be recorded separately,
not all identified by a single infinity symbol.

A genuine extension can replace j,k by homogeneous cardinal labels and
use the same even/infinite versus finite-odd division. The main checks are:

1. Use arbitrary-cardinal homogeneous central decompositions and the
   correct tensor-product representation, not a separable measurable-field
   convention silently applied to arbitrary Hilbert dimension.
2. Show the central-projection correspondence preserves arbitrary joins,
   so the reconstructed pieces exhaust both algebras.
3. In the even/infinite case, obtain an actual *- or anti-*-isomorphism
   of a nonzero corresponding central cut; use invariance of the
   homogeneous **cardinal** to conclude the labels agree. If Theorem 3.2
   is applied to the inverse because only the target is even/infinite,
   justify the target's cohomological constants from the classical type-I
   results, rather than presuming family 295 gives a uniform constant over
   variable N.
4. In the finite-odd case, retain the rank-(j-1) argument and the needed
   uniform estimates for its noncentral type-I corners. The central
   chain-map argument above alone does not supply noncentral-corner bounds.
5. Identify the centers of matching homogeneous pieces and assemble the
   resulting isomorphisms through the bounded direct product. No countable
   sum or sequence may replace the required nets.

Primary-author support found independently for the structure mechanism:
[Anantharaman-Popa, *An introduction to II_1 factors*](https://www.math.ucla.edu/~popa/Books/IIun.pdf),
printed page 78, Examples 5.5.5(a) and Remark 5.5.6, states cardinal
invariance for homogeneous type-I algebras and the general product
description by abelian algebras tensor B(H_i), citing Takesaki Theorem
V.1.27. Albeverio, Ayupov, and Kudaybergenov's author manuscript
[*Description of Derivations on Measurable Operator Algebras of Type I*](https://webdoc.sub.gwdg.de/ebook/serien/e/sfb611/361.pdf)
(17 October 2007),
printed page 13, explicitly states the unique cardinal-indexed homogeneous
central partition. I read these passages, but did not independently read
the full proof of Takesaki V.1.27 during this subtask. These support a
repair mechanism; the entire arbitrary-cardinal stability extension has
not been cleared by this audit.

Corollary 1.3 (page 3) is printed without a separability assumption and
with a uniform explicit threshold for its listed classes; a purely type-I
algebra has zero II_1 summand and meets the displayed tensor-absorption
condition vacuously. Its proof (page 23) invokes Theorem 1.2. The mismatch
between that literal corollary scope and the main theorem/proof's stated
scope should be recorded, not silently used to erase the issue. A route
using arbitrary type-I rigidity from this corollary needs either an
independent check of the broader type-I proof or an independently scoped
type-I stability source. The article's broad corollary statement is useful
evidence that the extension may be intended; it is not a completed check
of missing arbitrary-cardinal details.

## Boundary checks and conclusions that must not be promoted

- A zero algebra can be handled separately: finite distance from it is
  possible only to the zero algebra. The literal infimum/product convention
  can give d(0,0)=0, whereas some authors normalize that degenerate value to
  1; neither choice changes this rigidity case. Do not rely on a nonzero
  unit in the zero-algebra case.
- The distance hypothesis is about a surjective bounded complex-linear
  isomorphism, with invertible bounded inverse. It does not concern an
  embedding, an arbitrary real-linear map, or arbitrary Banach comparison
  spaces.
- No passage from ordinary distance to cb distance is justified or needed.
  Roydor explicitly explains their divergence on pages 3-4. The central
  * and anti-* pieces preserve the opposite-algebra possibility.
- The supplied article's page-2 introductory phrase about a cb threshold
  below 4 times 10^{-6} omits the expected additive 1 for a multiplicative
  distance. It is not a convention change that permits using d<10^{-6}.
  The actual cb comparator should be cited directly for its threshold;
  it was not fully reaudited in this narrow subtask.
- The sentence before Theorem 4.5 discusses K=L=1 and numerical constants.
  This audit does not turn a qualitative family-295 vanishing theorem into
  a universal Roydor epsilon or promote those numbers for all M. A fixed-M
  open-mapping bound is sufficient for the required qualitative targets.
- No result here concerns L^p for p other than 1/infinity; Remark 4.9
  explicitly raises that further question.
- No conclusion here implies the whole follow-on is formally verified,
  conventionally human-refereed, novel, or ready for production publication.

## Checkpoint log and exact remaining gap

- **2026-10-07 13:50 UTC:** read AGENTS.md and full project brief; verified
  supplied PDF hash and 26-page identity. Audit completion estimate: 15%.
  Mathematical-resolution/package percentages are not reassessed at this
  intake checkpoint.
- **2026-10-07 13:52 UTC:** read actual Theorem 1.2 and complete Section 4;
  discovered the explicit separable-predual condition and checked the
  ordinary actual-image complex. Audit completion estimate: 55%.
  The direct route to the full arbitrary target remains incomplete.
- **2026-10-07 13:55 UTC:** visually confirmed the theorem, differential
  misprint, Theorem 3.2, and type-I proof; independently checked canonical
  predual equivalences. Audit completion estimate: 85%.
- **2026-10-07 14:01 UTC:** completed source-version/metadata and pinned
  upstream convention checks, and recorded the nonseparable repair
  mechanism and its uniformity/cardinality obligations. Audit completion
  estimate: 100%. For this audit's relevant mathematical discovery goal
  (validating a direct all-M composition), best-guess completion is **60%**:
  the cohomology convention bridge and separable case are checked, while
  the additional scope proof remains. Publication clearance attributable
  to this review is **0%**; this was not a full-package review. These are
  workflow estimates, not mathematical evidence or replacements for the
  project's own global percentages.

**Strongest verified dependency consequence:** the separable-predual
statement above, conditional on the independently validated family-295
input. Exact isometry/Jordan/canonical-predual equivalences hold without
separability. Roydor's no-type-I machinery has a concrete broader proof
route once the fixed-M uniformity and involution-compatible correction are
written out.

**Exact remaining original-scope obligation:** provide and independently
verify an arbitrary nonseparable stability argument, especially the
arbitrary-cardinal type-I step and the quantitative control needed when
switching to target/noncentral type-I corners. A literal application of
Theorem 1.2 does not discharge it. This obligation is separate from the
remaining upstream central-proof, priority, final-package, and publication
checks.
