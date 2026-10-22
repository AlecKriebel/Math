# Verification report

This accompanies **A telescoping verification of a focal-inversion area invariant**, by Alec Kriebel.

## Mathematical scope

The positive theorem concerns a proper boundary ellipse and a strictly nested nondegenerate confocal elliptical caustic. The orbit has genuine least collision period `N=4n`, with every admitted coprime winding included. Area means the signed shoelace sum, counting traversal multiplicity. The inverse polygon consists of the original vertices inverted in a unit circle about an original focus, joined by straight segments. Both foci give the same product; reversal preserves it and repeating an admitted primitive cycle scales the product quadratically.

The arXiv-v11 source table does not explicitly require least period. The stronger repeated-list interpretation is false. Exact triangles on `x^2/8+y^2/5=1`, tangent to `x^2/(32/9)+y^2/(5/9)=1`, give two products differing by `-20 sqrt(6)/9` after four traversals. An explicit continuous triangular family and a confocal reflection identity establish that the two examples belong to one forward Euclidean billiard family. Hyperbolic and degenerate caustics are outside the positive theorem.

## Proof checks

Independent AI reviews reconstructed the submitted complex divisor/pole proof, independently propagated Euclidean rays, checked the source contract and the exact period boundary, and reconstructed the alternate rational telescope plus Fourier proof. The alternate proof's fresh reviewer found no substantive mathematical defect within this scope. The Root reproduced its 23 exact algebra checks byte-identically in a separate copy. These scoped checks are distinct from whole-publication-package reviews.

The manuscript gives the local identity explicitly, verifies all coefficient denominators on the real domain, includes the regular `V=0` four-period case, telescopes the derivative terms and proves the normalized cyclic dn formula by an absolutely convergent Fourier expansion. The half-grid shift gives the stated positive constant.

## Current portable checks

`verification/verify_exact.py` certifies **77 exact scalar identities**, including the focal-distance square, original and inverse edge determinants, area factors, local decomposition, cyclic coefficient, four-period value, and exact triangular boundary.

`verification/diagnose_geometry.py` uses canonical coordinates to select a known closed pair, then propagates actual Euclidean reflected rays. The default run checks eight families at four phases each, at 90 digits; the recorded optional stress run checks twelve families at 130 digits. Both foci, reversal, similarity, closure, winding and the explicit constant are checked. Wrong-parity and repeated-period-six controls resolve nonconstant products.

`verification/validate_fail_closed.py` records eleven execution cases. Exact acceptance survives optimized Python. Three damaged mathematical formulas and an injected NaN fail under `-O`; invalid physical/period inputs, insufficient stress precision and attempts to replace existing output are rejected. The Root reproduced all eleven cases in a fresh owned run. No stored PASS record is used as an oracle.

Finite floating-point residuals are diagnostics, not rigorous interval bounds. Near `k=1` or small shifts, cancellation may require substantially increased precision. The finite checkers do not replace canonical parametrization, real-domain reasoning, finite reindexing or Fourier convergence in the proof.

## Priority and review limits

Ferudun, DOI **10.5281/zenodo.23093706**, already gives the exact positive theorem and repeated-list obstruction. The classical local/cyclic master identities and generalized Landen formula, Stachel's canonical coordinates, Chavez-Caliz's original/tangent-polygon theorem and Garcia--Reznik's four-period value are credited. Bounded primary-source comparison supplies no theorem or proof-method novelty clearance.

The observed PR and deposit dates are recorded in TIMELINE.json. They establish dates of records, without certifying first discovery, independence, simultaneous discovery, every historical byte's public visibility or current openness. New October16 work is not backdated to the original PR.

AI assistance was used extensively. Mathematical and package reviews by AI agents are not conventional human peer review, refereeing, or proof-assistant formalization. No such human review or formalization is claimed.
