# Algorithms for multigraded regularity: scope audit and monomial control

Problem 30005078, OWR-10252925-002, catalogue rank 789.

## Verdict

**The general finitely presented module problem is unresolved by this work.**
The unrestricted finite-frontier interpretation for coherent sheaves is false:
the structure sheaf of the diagonal in P^1 x P^1 has regularity a+b>=0 and
infinitely many incomparable minimal degrees (t,-t). This does not rule out
algorithms returning other kinds of finite descriptions for sheaves.

The positive deliverable is an exact, terminating algorithm for monomial
quotients (and their associated sheaves), with an explicit proved frontier box,
full-region output, exact arithmetic, and replay tests. This is a separately
scoped result, not a substitution for the general target. No novelty claim,
first-resolution claim, journal-acceptance claim, or independent-audit claim is made.

## Primary target and dated literature check

The controlling source is Juliette Bruce's contribution, with Lauren Cranton
Heller and Mahrud Sayrafi, in the [2022 Toric Geometry report](https://ems.press/content/serial-article-files/46955?nt=1).
Its Question 3.1 is on printed p. 873 (PDF p. 13); the product grading is set
up on p. 871. The surrounding paragraph asks for all minimal regularity degrees
and links the task to a finite box. The following Question 3.2 is a separate
general-toric finite-generation question. The report's workshop was 27 March
through 2 April 2022; the imported citation's parenthetical 2023 is not its
workshop date. The live numeric landing page could not be inspected.

The [2026 characterization paper](https://arxiv.org/abs/2110.10705), v4 dated
27 May 2026, supplies exact degreewise membership under H_B^0(M)=0, through
quasilinear resolutions of truncations. It supplies inner bounds, and an exact
formula for saturated complete intersections generated inside B. Its main
uniqueness result also bears on the neighboring record 30005077. None of
these statements is used as a general terminating frontier algorithm here.
The author's [publication list](https://mahrud.github.io/research/) identifies
Advances in Mathematics 500 (2026), 111049 for that paper.

[Bounds on Multigraded Regularity](https://arxiv.org/abs/2208.11115), v2 dated
28 February 2025, gives finite generation for faithful modules on smooth
projective toric varieties and an effective outer translate, with a nonzero
associated-sheaf qualification. It also shows why general toric varieties are
different. An outer translate does not furnish an upper box for all frontier
coordinates. This source was publicly listed as submitted when checked.

The [current Macaulay2 documentation](https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/VirtualResolutions/html/_multigraded__Regularity.html)
describes cohomology and truncation searches and warns about hypotheses and
some lower limits. The inspected [upstream implementation](https://github.com/Macaulay2/M2/blob/stable/M2/Macaulay2/packages/VirtualResolutions.m2)
also explicitly says no default upper limit valid for every example is known.
It searches a selected bounded range. A routine's name is not a completeness
certificate. Macaulay2 itself was not installed or executed in this investigation.

The [2025 bigraded Gröbner-basis paper](https://arxiv.org/abs/2407.13536)
narrows the earlier multigraded title to the bigraded setting. Its partial
regularity regions do not identify the entire regularity frontier; in general
bigeneric initial ideals do not preserve that region. Classical [monomial
Cech methods](https://arxiv.org/abs/math/0001159) provide context for our
scoped computation, whose complete argument is supplied in PROOF.md.

This was a targeted source search through 5 October 2026, not an exhaustive
proof of literature-wide open status. Downloading a paper is not independently
checking all of its proofs. Exact inspected locations and bytes are recorded
in SOURCE_VERIFICATION.json; no source texts or PDFs are distributed here.

## Five approach families and stopping point

1. Exact degreewise resolution/cohomology criteria: available, but a membership
   decision is not a terminating all-frontier procedure.
2. Effective inner/outer bounds plus Dickson finiteness: insufficient alone;
   PROOF.md gives an explicit oracle obstruction and arbitrarily distant corners.
3. Gröbner degeneration and bigraded partial regularity: no valid preservation
   theorem supplies the missing full frontier; the central gap remains.
4. Fine-graded monomial Cech cells: completed as the separate scoped theorem,
   including an effective box, all minimal points, and the complete region.
5. Sheaf/module boundary: diagonal counterexample and exact contrasting module
   calculation completed. These correct the finite-output formulation but do
   not settle the substantive general-module question.

No additional proof-search family is claimed after this five-family stop.
The small complete-intersection helper merely implements an already published
formula, conditional on its hypotheses; it does not certify those hypotheses.

## Replay and deliverables

Run `python test_regularity.py` from this directory (Python standard library).
It rewrites RESULTS.json deterministically. The script checks nine explicit
examples over Q, F_2, F_3 and F_101; 80 singly graded cases against independently
constructed Koszul homology; 144 cell-invariance comparisons; and 1,681 checks
of the diagonal's geometric cohomology model. These finite checks do not
replace the proofs.

* PROOF.md: complete scoped proofs, conventions, exact general gap
* monomial_regularity.py: authored reference implementation
* test_regularity.py and RESULTS.json: replay and recorded finite controls
* SOURCE_VERIFICATION.json: source and public-corpus verification metadata
* RESEARCH_LOG.md: dated decisions and qualified completion estimates
* AUTHOR_MANIFEST.json: allowlisted artifact hashes

The Cech construction is intentionally small-scale and can be exponentially
expensive. It is a termination/completeness reference, not a performance claim.
It rejects zero-dimensional projective factors rather than silently treating
them as independent Picard directions. The exact ranks in characteristic p
also apply to any extension field of F_p, and characteristic-zero ranks to any
characteristic-zero field.

No remote writes, publication, release, or external correspondence were made.
