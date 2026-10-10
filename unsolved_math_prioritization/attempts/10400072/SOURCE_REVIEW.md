# Source review and attribution

Problem 10400072 / AMR-103-0072 is Ohtsuki Conjecture 3.22 about injectivity
of the hair expansion. The accepted result is a prior published negative
resolution of its exact Laurent-polynomial case.

## Original statement and precise match

T. Ohtsuki, editor, Problems on invariants of knots and 3-manifolds,
Geometry & Topology Monographs 4 (2002), 377–572, states the conjecture on
printed pages 441–442 (PDF pages 69–70). Map (30) has edge labels in
Q[t,t^-1]; map (29) recovers exactly this ring at A(t)=1.
[Original publisher PDF](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

The map/quotient comparison in [AUDIT.md](AUDIT.md) checks the field, bead
involution, edge reversal, multilinearity, bead multiplication, vertex pushes,
AS and IHX, indistinguishable hairs and formal-series completion. Both sources
allow the closed connected diagrams needed for the witness. The published
paper's citation to Conjecture 3.18 is reconciled by matching definitions and
maps to the original's 3.22; no historical renumbering explanation is asserted.

## Credited published resolution

Bertrand Patureau-Mirand, Noninjectivity of the “hair” map, Algebraic &
Geometric Topology 12(1) (2012), 415–420, Theorem 4, supplies the nonzero
kernel element. The publisher records March 14, 2012. The accepted theorem
is this published version; arXiv records a February 7, 2002 initial submission
and December 13, 2011 revision v3.
[Publisher page](https://msp.org/agt/2012/12-1/p16.xhtml),
[publisher PDF](https://msp.org/agt/2012/12-1/agt-v12-n1-p16-s.pdf),
[DOI](https://doi.org/10.2140/agt.2012.12.415),
[arXiv record](https://arxiv.org/abs/math/0202065).

The complete six-page paper was read historically; PDF pages 2–5 were visually
inspected, including every diagram used in the kernel proof. The authored
argument in AUDIT.md separates bead terms by integral cohomological content,
uses the content-zero projection to prove the finite witness nonzero, and
shows that every positive-hair coefficient contains the same zero local
three-legged subdiagram. Its connected closed source has first Betti number
17 and Ohtsuki loop-degree 16. These two degrees must not be conflated.

## Imported diagram results and computational dependence

Pierre Vogel, Algebraic structures on modules of diagrams, Journal of Pure
and Applied Algebra 215(6) (2011), 1292–1339, is the source of essential
imported diagram results. The inspected file is the author-hosted 71-page
manuscript, linked as a 2010 preprint; it was not byte-matched to the journal
PDF. Its page references are manuscript pages.
[Author manuscript](https://webusers.imj-prg.fr/~pierre.vogel/diagrams.pdf),
[publisher record](https://www.sciencedirect.com/science/article/pii/S0022404910001842),
[DOI](https://doi.org/10.1016/j.jpaa.2010.08.013).

Corollary 4.6 supplies rational rank-one freeness of the closed-diagram module.
Theorem 8.4 and Proposition 8.5 supply the nonzero degree-15 zero divisor
annihilated by Vogel's algebra element tau. Patureau-Mirand's Corollary 2
identifies the zero three-legged inserted diagram used to kill every hair
coefficient. Acceptance relies on these published imports. It does not
reconstruct the zero divisor from first principles.

Vogel's proof invokes low-cardinality module calculations, computer-checked
surjectivity and a computer-calculated nonzero proportionality coefficient;
a supporting relation in Lemma 5.7.1 likewise cites computer calculations.
No complete graph-reduction certificate or raw calculation files for those
steps were recovered or rerun. The independent nonzero arithmetic check uses
the imported character formula and does not reproduce a graph weight-system
evaluation. The original hair-map well-definedness reference is also imported,
not reconstructed here. AUDIT.md retains the exact dependencies and locations.

## Review and distribution boundaries

The original stated conjecture is false because its explicit Laurent case
fails. This does not assert survival of the witness under every nontrivial
localization, minimal loop degree, or realization by knot invariants.
No new counterexample, proof novelty or priority is claimed.

The authored audit is AI-assisted and unrefereed. Its acceptance is not
external human peer review, journal acceptance of this audit, or proof-assistant
certification. The cited 2012 theorem and 2011 diagram work are published
sources; that status is distinct from the status of this audit. The bounded
correction/retraction search found no notice, which is not an exhaustive
status guarantee.

[SOURCE_METADATA.json](SOURCE_METADATA.json) preserves exact recorded public
source identities, hashes, byte counts and inspection/retrieval history.
An initial incorrect p17 publisher-page retrieval was explicitly excluded;
the verified hair-map page is p16. Preparation of this edition rechecked
accepted-package byte identities and publication integrity only. It did not
newly retrieve or inspect third-party source content, repeat literature
searches or rerun mathematical programs. No source documents/text/images,
code, raw outputs, generated certificates, datasets or private coordination
material are distributed.
