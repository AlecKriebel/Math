# Independent audit: modern K3 Problem 3.72, catalog 2870

Audit date: 2026-10-05 UTC.

## Verdict

**Accept the scoped `unsolved`, five-approach disposition, with the citation
clarification supplied in this audit.** Neither target part is proved. No
substantive mathematical error was found in the elementary reductions,
conditional algebra, or the deduction that the standard DHST summand meets the
rational-filling kernel trivially. The optional ordinary-d cross-check needs one
additional credited theorem; its conclusion is correct after adding that input.
The main exclusion argument does not depend on this cross-check.

This is a mathematical dependency and argument audit, with exact diagnostic
replay. It is not a formal verification of the foundational Floer theories,
a rederivation of the source Kirby diagrams, or a certificate of global openness.

## Frozen object and independent checks

The audited author manifest has SHA-256
`8074d0a6a5ec04ee4ba269300bb0bddad6b49595e955f456d26a10898b757888`.
The audited proof has SHA-256
`4ae92f8adaabff6700ee8a6da5a178e629321729cbd4420153d6c2f64975ac36`.
All eight members named by the manifest verified; together with the manifest
there are nine frozen files. The original checker ran successfully and its
9,495-assertion output matched the recorded output byte for byte. None of the
frozen files was edited.

The nine downloaded source PDFs were independently rehashed and their sizes
checked against the source metadata; all nine matched. This checks the local
source bindings, not the unrelated upstream dataset corpora. No corpus rehash
or byte comparison is claimed.

Separate, independently written controls passed 6,470 assertions. They include
symbolic polynomial multiplication and translation; finite-field enumeration
rather than the author's elimination routine; rational-image correction with
nonzero torsion residuals; nonzero diagonal minors after clearing denominators
and killing torsion; and countermodels for ordinary-d detection and integral
retractions. The tests found 1,687 cases where rational equality alone leaves a
nonzero torsion residual, illustrating why the second correction step matters.
No finite test is represented as a computation of a Floer invariant or as proof
of independence of actual manifolds.

## Target identity and quantifiers

The K3 source's printed pp.181 and 183 were checked; p.183 was also visually
inspected. The target is smooth, oriented integral homology spheres modulo
integral homology cobordism, mapped to smooth rational homology cobordism.
Part (a) asks for a countable free subgroup of infinite rank in its kernel;
part (b) asks for such a subgroup splitting in that kernel. The statement does
not require a splitting in the full integral group, a spin rational filling,
or a fixed fundamental group. The packet retains these distinctions.

The modern number is correctly distinguished from the unrelated 1997
convergence-group problem. No numerical match to Bowditch is used as a theorem
about this kernel. The reported queue position and historical duplicate-search
coverage are author provenance, not independently repeated repository searches
in this audit. The mathematical target itself is independently verified.

Source: Baykur--Kirby--Ruberman, *K3: A New Problem List in Low-Dimensional
Topology*, pp.181,183,
https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

## Route 1: rational fillings and the membership/independence gap

Proposition 1.1 is correct. Capping a rational cobordism at its sphere end and
puncturing a rational ball are inverse homological constructions. The relative
orientation class supplies the required boundary H3 isomorphisms; having only
the same abstract homology groups would not by itself suffice. Boundary
connected sum joins two components with a 1-handle and does not add rational
H1. Orientation reversal supplies inverses. These operations establish closure
of kernel membership, not a relation obstruction.

Proposition 1.2 is correct for a nonzero rational attaching class. The relative
2-handle chain has one rational generator and its connecting map to H1 is a
nonzero map between one-dimensional vector spaces. Therefore both positive
homology groups that could remain vanish. The asserted boundary-to-interior
H1 isomorphism follows from Poincare--Lefschetz duality and the pair sequence.
The boundary of the original rational homology circle is connected: the
relative orientation map surjects onto its H3, which has one generator for
each boundary component. Surgery on a knot preserves connectedness.
No restriction on framing is required for the rational calculation.

The four credited family triples, their pairwise-coprime conditions, and the
parity ranges for the cited nontrivial examples agree with the inspected
Akbulut--Larson and Savk statements. In particular, the latter source states an
integer Neumann--Siebenmann value in its nontriviality argument; the packet does
not silently promote it to an additive invariant on the entire cobordism
group. The rational fillings themselves remain credited geometric inputs.

The odd-multiple rank-one countermodel correctly defeats the inference from
infinitely many different examples or a nonzero parity invariant to infinite
rank. No independence argument for these actual kernel families is present.

Sources: https://arxiv.org/abs/1704.07739 (Theorem 1, Lemma 2),
https://arxiv.org/abs/1912.04654 (Theorem 1.1, Lemma 2.1),
https://arxiv.org/abs/2006.14509 (Lemma 1.1).

## Route 2: paired torsion and handles

Proposition 2.1 is correct. Finite generation and rational acyclicity make the
positive integral homology finite. The relative fundamental class identifies
the degree-four relative group with the degree-three boundary group. The next
relative group is H^1(W;Z)=0, so H3(W;Z)=0. The homology-sphere boundary then
identifies H2(W;Z) with H^2(W;Z). Universal coefficients give Ext(H1(W;Z),Z),
since the Hom term of finite H2 vanishes. The noncanonical qualification for
identifying a finite abelian group with its dual is appropriate.

Corollary 2.2 is correct for ordinary absolute handle decompositions of W.
Without 3-handles, H2 is a subgroup of a free abelian handle-chain group, hence
cannot contain the finite torsion required by a nontrivial defect. Without
1-handles, H1 is zero. Either absence forces an integral homology ball. Thus
a rational filling of a nonzero kernel class requires both handle indices.
The presence of both indices is only necessary. The Stein consequence uses the
standard index-at-most-two fact and agrees with the inspected 2026 Lemma 1.2.
No obstruction to arbitrary smooth rational fillings is inferred from it.

The model chain complex has the asserted H1 and H2, both Z/m, and zero H3.
It does not realize a manifold merely by satisfying these algebraic identities.
The missing geometric realization/separation step remains clearly stated.

Source: Alfieri--Cavallo--Matkovic, Lemma 1.2,
https://arxiv.org/abs/2605.13812 .

## Route 3: homology and invariant domains

The universal-coefficient calculation in Proposition 3.1 is correct, including
the two contributions to degree two and the Tor contribution to degree three.
The p-primary cyclic-factor count gives Betti numbers (1,r,2r,r,0). For p=2,
vanishing of the defect forces vanishing H^2 with mod-two coefficients, hence
spin. The unique boundary spin structure and zero signature then contradict a
Rokhlin-one boundary. The converse is not asserted.

Proposition 3.2 is correct and does not require additivity for constancy on the
kernel. The ordinary correction term is handled with the essential extending
Spin-c qualification: an oriented smooth four-manifold admits a Spin-c
structure, and an integral homology sphere has only one boundary Spin-c
structure. Therefore Ozsvath--Szabo Proposition 9.9 implies d(Y)=0 for every
kernel class. It would be incorrect to replace this with an assertion that all
rational balls are spin, or that a rational sphere has a unique Spin-c
structure. Neither replacement occurs.

NST Theorem 5.15 explicitly supplies rational-cobordism invariance on integral
homology spheres. The normalization on S3 is infinity, so both orientations of
a kernel element have infinite r_s. There is no finite-r_0 independence route
for these elements. Rokhlin yields only a parity restriction on coefficients.
The Neumann--Siebenmann scope warning is sound.

Sources: https://arxiv.org/abs/math/0110170 (Proposition 9.9, p.67),
https://ems.press/content/serial-article-files/48226 (p.4702 and Theorem 5.15,
p.4745). Relevant formula pages were visually checked.

## Route 4: rank transfer and the DHST exclusion

Proposition 4.1 is correct even if the rational image has torsion: tensoring
an exact sequence with Q computes rank, and finite rank of the image gives
unbounded finite rank of the kernel inside the free subgroup. Countably many
Q-independent lifts generate a free abelian subgroup; this proves no splitting.
The concrete correction criterion is also valid. If image relations hold only
after tensoring, denominators must first be cleared and the remaining torsion
then killed by nonzero integer multiples. Nonzero coordinates on the original
independent family preserve independence.

For Proposition 4.2 every dependency needed for the stronger exclusion was
checked:

1. DHST's proof of Theorem 1.1 identifies precisely the family
   B_n=Sigma(2n+1,4n+1,4n+3), n>=1, as free direct-summand generators in the
   integral group. This is not a mere existence theorem for some other family.
2. The triples are pairwise coprime for every n: subtraction reduces the first
   two gcd comparisons to 1 and the remaining comparison to an odd integer
   against 2.
3. Lee--Savk's orientation convention is the link/negative-plumbing orientation.
   The proof of Theorem 3.3 explicitly records R(B_n)=1 for this same family.
4. NST Corollary 1.4 has finite r_0 on the negative of this orientation, and
   infinity on the positive orientation. The minus sign and infinity symbol
   were checked visually, not inferred from degraded text extraction.
5. The exponent product is 32n^3+48n^2+22n+3. Its next-step difference is
   96n^2+192n+102, positive for all n>=1. Thus the reciprocals decrease strictly.
6. Applying NST Corollary 5.6 to -B_n meets both its finite-decreasing and its
   opposite-orientation-infinite hypotheses. Theorem 5.15 explicitly upgrades
   the resulting conclusion to independence in the rational group. Integral
   independence alone would not be enough.
7. Injectivity of q on this span gives F intersect ker(q)=0. Reversing all
   generators changes no independence assertion.

Thus the exclusion is valid for every finite integer combination, not just for
individual generators. It is an application of credited theorems, not a new
Floer-theoretic independence theorem.

Lee--Savk's local-equivalence-kernel examples are also correctly distinguished
from the target kernel. Theorem 3.3 provides rational independence for its two
listed families together, and Theorem 3.4 provides it for its further family.
Consequently each stated independent span has trivial intersection with the
rational-filling kernel. Nothing here identifies local equivalence with rational
homology cobordism.

Sources: https://arxiv.org/abs/1810.06145 (Theorem 1.1 and its proof),
https://arxiv.org/abs/2508.15384 (orientation convention, Theorems 2.14,2.15,
3.3,3.4), https://ems.press/content/serial-article-files/48226 (Corollaries
1.4,5.6 and Theorem 5.15).

### Audit clarification: ordinary d versus upper involutive d

The optional paragraph after Proposition 4.2 says that Lee--Savk Theorems 2.5
and 3.1 give ordinary d(B_n)=2n. Their Theorem 2.5 actually identifies the upper
involutive correction term with the upper monotone-root parameter. Together
with Theorem 3.1 this directly gives bar-d(B_n)=2n, not by itself ordinary d.

The missing bridge is Dai--Manolescu, *Involutive Heegaard Floer homology and
plumbed three-manifolds*, Theorem 1.2, p.2: for the boundaries of negative-definite AR plumbings, with their boundary
orientation, the upper involutive and ordinary correction terms coincide. The canonical negative-plumbing orientation of B_n is exactly
the required one. Therefore the desired ordinary-d value follows after this
additional credited input. The theorem and its orientation hypothesis were
independently inspected, including the rendered formula.

For a later revision, the bounded correction is to add this theorem to that
paragraph's citation chain, or simply omit the optional cross-check. No change
to the r_0 argument is needed. This audit supplies the missing credit while the
original freeze remains untouched.

Source: https://web.stanford.edu/~cm5/HFIplumbed.pdf ; bibliographic identifier
https://arxiv.org/abs/1704.02020 . The inspected author-hosted PDF is 481,989 bytes,
35 pages, SHA-256
`c56f82f3fc9f11112bed7d251d5673dc89bef22facf702c15d001fd2174b98e6`.

## Route 5: subgroup versus direct summand

Proposition 5.1 is an exact retraction criterion. Integer coordinate maps with
the Kronecker condition ensure the restriction to H is the identity; pointwise
finite support is needed to assemble them into a map to a direct sum rather
than merely a product. Additivity follows because a union of two finite supports
is finite. Conversely a splitting supplies precisely these coordinate maps.

The doubled-basis example correctly shows that an independent subgroup need
not split. The direct sum of copies of Q is divisible, has an infinite free
subgroup, and has no nonzero homomorphism to Z; therefore it has no nonzero free
summand. The example K=Z inside A=Q likewise distinguishes a splitting in K
from one in A. These are abstract logical countermodels, not assertions about
the actual cobordism kernel.

No actual locally finite family of integer-valued dual maps on K is constructed.
This is the precise missing input for this route.

## Disposition and publication boundary

The record supports five distinct investigative mechanisms, all stopped at
identified gaps. Neither an infinite-rank kernel subgroup nor a direct summand
of it has been established. The disposition remains `unsolved`; the audit does
not turn successful finite diagnostics into a solution claim. Current-source
spot checks did not supply a resolution and do not establish global absence of
one.

The audit deliverables consist only of authored analysis, executable diagnostic
code, hash/size bindings, replay results, and public bibliographic metadata.
No source PDF, extracted source text, source screenshot, dataset contents, or
private coordination material is included. No helper was delegated and no
remote write was performed during this audit.
