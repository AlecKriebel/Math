# Primary-source claim specification

This is the referee's independent restatement of the claims actually made by
the revised article.  It is based on the paper and supplement, not on package
status fields.

## Model and topology hypotheses

- The leaf set is finite, fixed, and labelled.
- Networks are binary, standard semi-directed networks obtained by the stated
  one-step root suppression; isomorphisms preserve labels, ordinary edges,
  arrowheads, and vertex roles.
- Every blob has at most two reticulations.
- The principal classification is restricted to the strongly tree-child
  class: an admissible rooting exists and every admissible rooting is
  tree-child.
- Every inheritance probability is strictly between zero and one.
- Edge Fourier spectra use the fixed observable characters `C,G,T`.  In the
  principal branch they lie in the strict stochastic domain
  `D3,+`; in the continuous-time branch they satisfy
  `c>g*t`, `g>c*t`, and `t>c*g`.

## Main classification

For two networks `N,N'` in that class, the following are equivalent:

1. A regular full-dimensional source-parameter neighborhood of `N` has a
   physical real-analytic section into the parameter space of `N'` on which
   the observable K3P tensors agree.
2. The labelled reduced trees of blobs agree, every corresponding
   nontriangle factor is a labelled mixed-graph isomorphism, and each remaining
   three-cycle factor differs by one coherent ordinary-triangle redirection.
3. The two physical images share a common regular full-dimensional analytic
   germ with physical sections on both sides.

Consequently there is no proper one-sided containment of this specified kind
inside the strong class.  This is not equality of the complete stochastic
images and not numerical parameter identifiability.

The same equivalence holds on the strict continuous-time domain.  Necessity
uses that this is an open full-dimensional subset of the principal domain;
sufficiency requires the triangle germ and bridge gluing to remain physical in
continuous time.

## Generic identifiability and reconstruction

For each fixed topology `N`, the paper removes a proper complex
Zariski-closed exceptional set from its irreducible model closure.  Every exact
physical tensor outside that set identifies the labelled standard
semi-directed topology uniquely modulo ordinary-triangle equivalence.

The reconstruction claim is an exact-real termination theorem.  Its input
must support field operations, exact polynomial-sign decisions, and
real-closed-field quantifier elimination.  It gives neither bit complexity nor
conditioning, finite-sample, or statistical guarantees.

## Sharpness and outer obstruction

For every `n>=3`, the paper constructs two binary, standard, level-2 networks
in weak-but-not-strong tree-child class which are labelled nonisomorphic and
not ordinary-triangle-equivalent, yet whose strict continuous-time K3P images
share a common full-dimensional regular analytic germ of dimension `6n-3`.
The three-leaf equality-slice root is asserted unique only inside its selected
15-dimensional rational box, not globally in parameter space.

A separate tree/double-theta proper-containment example lies outside even the
weak tree-child class and is not the sharp class-boundary construction.

## Explicit nonclaims and boundaries

- No conclusion is asserted for arbitrary weak tree-child networks, boundary
  edge spectra, zero/one inheritance weights, nonstandard root suppression, or
  higher-level blobs.
- Ordinary-triangle ambiguity is structural and contextual; it is not a claim
  that every representative realizes every tensor of every other
  representative.
- The generic noncut flattening statement is not promoted to a universal
  pointwise cut-rank converse.  Pointwise rank `>4` is used only for the finite
  204-direction one-active target universe in the reverse cut inclusion.
- The theorem concerns observable image germs and topology, not recovery of
  every numerical edge or inheritance parameter.
