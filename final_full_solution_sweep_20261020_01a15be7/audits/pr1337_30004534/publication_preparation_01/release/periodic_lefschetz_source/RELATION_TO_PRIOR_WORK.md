# Relation to prior work and exact scope

The result is an explicit counterexample to the unrestricted eventual WLP and
SLP dichotomies in Tim Römer's contribution, *Asymptotic properties of invariant
chains*, printed pp.1594–1596 of OWR31/2020. The primary contribution fixes a
field K and integer c>=1, with symmetric groups permuting columns in c rows.
It requires invariant ideals and compatibility under extension and larger
column permutations. The question concerns Artinian quotients; it does not
impose characteristic zero, one row, monomial generators, or Gorenstein quotients.
The preparer read the complete contribution's extracted text from the pinned
publisher PDF. The report's pp.1544–1545 working-group discussion deliberately
concentrates on one-row monomial ideals. That is a distinct special setting.
The present construction is generally nonmonomial and uses two rows.

The mathematical contribution claimed here is the single explicit uniform
chain and its elementary complete classification. Every n>=2 has Hilbert
function (1,2n,2n). For every form with x-coefficients a_i, the determinant is
(-1)^(n-1)(n-1) product(a_i^2). In characteristic p, n congruent to 1 modulo p
is bad, and every other n>=2 is good. Width one is separately SLP.
The counterexample already exists over F_p(t), with fixed p and fixed c=2.
No variation of field or separate choice of ideals according to congruence is
used. The entire chain is generated from width three. These are stronger
compatibility details than merely exhibiting unrelated algebras at each n.
The underlying determinant, rank and socle techniques are standard; no new
general Lefschetz mechanism is claimed.

Alexandra Seceleanu and Liana Şega's *General symmetric ideals*,
https://arxiv.org/abs/2506.15459v1, submitted 18 June 2025, is a closely related
positive asymptotic study. Its ambient ring has one row of variables and its
objects are general symmetric ideals. Theorem B (Theorem7.10/Corollary7.11)
assumes the field is infinite and has characteristic zero or characteristic
greater than n, as well as its explicit lower bound on n. Its item(4) gives WLP.
Its Theorem9.2, summarized with Theorem9.3 in Theorem C, assumes characteristic
zero and proves preservation of generality in the orbit-generated chain from
a sufficiently large starting width. These hypotheses do not supply a fixed
positive-characteristic two-row counterexample. With p fixed, p>n cannot
hold along arbitrarily large n. The preparer read the byline, introduction,
Theorem B/C statements, chain setup, and complete Theorem9.2 text/proof.
The entire paper and all its proofs were not audited; none is imported as a
premise in the present proof. The recorded comparison is to v1, not an assumed
different journal or later version. The fresh arXiv primary page still lists
the 18 June 2025 submission. PDF and metadata captures have separate hashes.

David Cook II's 2012 paper, *The Lefschetz properties of monomial complete
intersections in positive characteristic*, J.Algebra369,42–58,
https://doi.org/10.1016/j.jalgebra.2012.07.015, is standard background for
characteristic-sensitive Lefschetz maps. Only the primary journal title,
bibliographic information and abstract were inspected in this preparation.
No theorem from its full body is invoked. The proof here defines the properties
and uses only explicitly proved linear algebra and quotient computations.

The earlier independent source review additionally compared the introduction
of the FPSAC2025 Article51 family of characteristic-zero squarefree algebras
with a power-of-sum relation. The preparer read that review comparison rather
than auditing the full paper. It does not enter the theorem or novelty claim.
The related native Zenodo record22950380 concerns symmetric-determinant
apolarity, with WLP/SLP thresholds in the matrix size; its native metadata
does not describe this two-row chain or periodic bad widths. The register's
Sperner complete-intersection record23204810 explicitly excludes a Lefschetz
claim. Other broad register/search hits concerned allocation theory or unrelated
uses of Lefschetz. These are search leads, not proof dependencies.

The own-project proof source is https://github.com/AlecKriebel/Math/pull/1337,
head aa737e6da42a3a464761dd5d36de4d1f34781ff4, PROOF.md SHA256
bbd42519c66c1a74004b3edfafbf9c0cdb9d46af1c5798367240bc9b1f97e5db.
That PR is unpublished. A reviewer proposed a source-only register row pointing
to it; such a row cannot turn the PR into an existing publication. This note
is a separate dated preparation, not a claim that a prior DOI or paper exists.
Catalog30004534 and source code OWR-2654827-016 identify one result family.
The report DOI and arXiv DOI are references, not this note's solution DOI.

Fresh GWS read-only checks covered all 43 columns in both value/formula views,
with stable metadata before and after. Fresh public searches covered exact
catalog/PR/title aliases, periodic Lefschetz wording, invariant/symmetric ideal
chains, positive characteristic, the author ORCID, and primary source pages.
Native Zenodo attempts with size100/sort mostrecent returned400; corrected
bounded queries with size25 succeeded. Exact target phrases returned zero.
Broad word searches have loose semantics and truncated result sets; no global
absence inference is drawn from them. The earlier independent source review
also searched broader terminology and source families. Within these bounded
checks, no earlier full-target publication or full-solution DOI was authenticated.
This is not a certification of exhaustive novelty, exclusive firstness, author
discovery priority, or present open status. No outside person was contacted.

The strongest supported claim is the self-contained theorem and its explicit
negative answer to the original unrestricted dichotomies. The characteristic-zero
and one-row variants receive no negative answer from this example. Preparation
QA and finite computation do not replace new independent whole-package reviews.
