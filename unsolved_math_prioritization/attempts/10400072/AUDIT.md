# Source-credit audit: noninjectivity of the loop/hair expansion

Audit date: 10 October 2026. Target: Ohtsuki Conjecture 3.22, record 10400072 / AMR-103-0072.

## Decision and exact scope

**ACCEPTED: prior published negative resolution, credited to Bertrand Patureau-Mirand.** Theorem 4 of *Noninjectivity of the “hair” map*, Algebraic & Geometric Topology 12 (2012), 415–420, gives a nonzero kernel element for the exact Laurent-polynomial map (30) in the original problem. This is also map (29) with the admissible choice A(t)=1. It therefore disproves the stated conjecture, including its explicitly asserted particular case.

This is a source-based acceptance after independent inspection of the complete short proof, its domain comparison, and the hypotheses of its imported diagram results. It is **not** a new counterexample, a self-contained reconstruction of Vogel's zero divisor, or an independently reproduced computer certificate. This authored audit is AI-assisted and unrefereed; its acceptance does not mean external human peer review, journal acceptance of this audit, or proof-assistant certification.

The audit does not establish that the same witness remains nonzero after every nontrivial localization Q[t,t^-1,1/A(t)]. That stronger statement is unnecessary for the decision and must not be inferred. It also does not construct two knots with identical Kontsevich invariants or show that every diagrammatic kernel element is realized by knot invariants.

## Primary sources and inspected locations

1. T. Ohtsuki, editor, *Problems on invariants of knots and 3-manifolds*, Geometry & Topology Monographs 4 (2002), 377–572. [Publisher PDF](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf). Exact target and maps: PDF pp. 69–70, printed pp. 441–442; underlying ordinary diagram conventions: PDF pp. 26, 33 and 65, printed pp. 398, 405 and 437. The map illustrations and both bead relations in Figures 13–14 were visually inspected.
2. Bertrand Patureau-Mirand, *Noninjectivity of the “hair” map*, Algebraic & Geometric Topology 12(1) (2012), 415–420, DOI [10.2140/agt.2012.12.415](https://doi.org/10.2140/agt.2012.12.415). [Publisher page](https://msp.org/agt/2012/12-1/p16.xhtml), [publisher PDF](https://msp.org/agt/2012/12-1/agt-v12-n1-p16-s.pdf). All six pages were read; PDF pp. 2–5 were visually inspected, including every diagram used in the kernel proof. The publication page confirms 14 March 2012. [arXiv math/0202065](https://arxiv.org/abs/math/0202065) records v1 on 7 February 2002 and v3 on 13 December 2011 and identifies the journal publication. The theorem accepted here is the publisher's 2012 version, not an inference from the earlier submission date.
3. P. Vogel, *Algebraic structures on modules of diagrams*, Journal of Pure and Applied Algebra 215(6) (2011), 1292–1339, DOI [10.1016/j.jpaa.2010.08.013](https://doi.org/10.1016/j.jpaa.2010.08.013). The [publisher record](https://www.sciencedirect.com/science/article/pii/S0022404910001842) verifies journal identity. The inspected [author-hosted manuscript](https://webusers.imj-prg.fr/~pierre.vogel/diagrams.pdf) has 71 pages; the author's page labels it a 2010 preprint, and its introduction identifies an expanded, updated version of a 1995 preprint. These are **manuscript page numbers**, not journal pagination: definitions and gradings pp. 2–5; rational freeness pp. 11–14; character construction/formula pp. 50–56; Theorem 8.4 and Proposition 8.5 pp. 61–66. Pages 14, 52, 55, 61 and 63–66 were visually inspected. The manuscript's full typeset identity was not byte-matched to the journal article.

The Patureau-Mirand paper refers to Ohtsuki Conjecture 3.18. The inspected original record prints Conjecture 3.22. The audit resolves the mismatch by comparing definitions and maps, not by assuming numbering is stable. The exact historical reason for the numbering change is not required and was not independently established.

A bounded title/author search for corrections or retractions found no such notice, and the checked publisher/arXiv records do not display one. This is bounded status evidence, not an exhaustive guarantee.

## Exact map comparison

Use z for the edge-bead variable here; use tau for Vogel's algebra element denoted t in the papers. These are unrelated objects.

The original scalar field is Q. For map (30), the edge-label ring is Q[z,z^-1], with involution z -> z^-1. Patureau-Mirand calls the same ring R=Q[b,b^-1]. The isomorphism b -> z changes no scalar field or relation. In particular, the rational coefficients in the statement mean rational-number linear combinations, not a quotient in which all rational functions of beads have already been inverted.

Both sources use cyclic orientations at trivalent vertices, arbitrary edge orientations with label inversion upon reversal, rational multilinearity in each bead, and multiplication of successive beads. Their push relations agree: moving one monomial factor through a vertex changes the three incident exponents by the coboundary of a vertex function. The original diagram with outward z-labels deleted is equivalent, after reversing an incident edge, to the paper's displayed one-in/two-out push relation. The AS relations coincide. The ordinary local IHX move has no nontrivial bead on its internal edge, made explicit in the later paper; all external labels are retained. Thus this comparison is made in the same beaded AS/IHX/push quotient, not a quotient obtained by imposing extra relations or by forgetting beads.

A monomial z^n maps to the series with k hairs and coefficient n^k/k!. This is exactly substitution z=exp(h). The finite linearity convention then gives the same map for every Laurent polynomial. For the generalized original ring, A(1)=1 permits formal substitution in 1/A(exp(h)); no such inverse is used in the witness.

The ordinary target is the rational AS/IHX space of vertex-oriented unitrivalent graphs with indistinguishable hairs. Patureau-Mirand obtains indistinguishable hairs as symmetric-group coinvariants and explicitly completes in half-total-vertex degree. The original prints B while displaying infinite formal series; the comparison uses its formal-series interpretation. There is no convergence issue: each coefficient below vanishes already in the ordinary diagram quotient. Patureau-Mirand cites Garoufalidis–Kricker, *A rational noncommutative invariant of boundary links*, Geometry & Topology 8 (2004), 115–204, for well-definedness of the hair map. This audit compares the already-defined original and published maps; it does not reconstruct that additional well-definedness proof. Both definitions allow the closed diagrams needed for the source witness. The witness is connected, so restricting attention to connected source diagrams would not remove it.

## Checked proof of nonzero kernel, with imports isolated

### Imported diagram facts

Work over Q, so 6 is invertible. Let Lambda be the totally antisymmetric part of the space of connected three-legged Jacobi diagrams, with the vertex-insertion multiplication. In Vogel's notation one must use F'_k(0) and F'_k(2), meaning connected diagrams with at least one trivalent vertex; the prime excludes degenerate circle/strut cases. These agree with the corresponding F_0 and F_2 conventions in Patureau-Mirand.

The precise imported facts are:

- Vogel Corollary 4.6: F'_Q(0) is a free rank-one Lambda-module on theta. Therefore r != 0 implies r.theta != 0. This implication is essential; a character of r alone would not automatically certify a closed diagram.
- Vogel Theorem 8.4 and Proposition 8.5 supply a homogeneous r of Lambda-degree 15 with r != 0 and tau r=0. Patureau-Mirand's Corollary 2 also identifies the corresponding three-legged inserted diagram with 2 tau r, hence zero.

The nonzero statement is over Q, not merely modulo a prime and not inferred from failure of familiar Lie algebra weight systems to detect r.

### Cohomological separation of the bead terms

Expand each Laurent bead into monomials. An exponent assignment is an integral 1-cochain on the graph. A graph has no 2-cells, so every such cochain is a cocycle. Vertex pushes add integral coboundaries. The equivalent description therefore labels a graph D by a class x in H^1(D;Z).

Define the content of x as the nonnegative generator of its evaluation ideal in Z; content zero means x=0. Integral cohomology is free abelian. Reversal and graph isomorphisms preserve content. In IHX, each of the three graphs collapses its unlabelled internal edge to the same four-valent graph. These contractions induce integral cohomology isomorphisms, so all terms have the same content. The relations are homogeneous for content, and projection onto content zero is well defined on the quotient. Its image is the ordinary unlabelled closed-diagram quotient, with inverse given by labelling all edges 1. Evaluating every bead at 1 is used only on this content-zero summand; it is not being mistaken for a projection on all summands.

Insert r into one vertex of a theta graph, and put z-1 on the distinguished outside edge shown in Theorem 4. Denote this finite linear combination by W. Multilinearity gives W=D_z-D_1. For each connected summand of r, the distinguished edge lies on a cycle: connect two of r's boundary ends inside r, and use the corresponding two edges to the remaining theta vertex. A cycle crossing the distinguished edge once has exponent evaluation +1 or -1. Hence D_z has primitive, nonzero cohomology class and content 1. D_1 has content zero and equals r.theta. Consequently the content-zero projection of W is -r.theta != 0. This proves W != 0 in the exact Laurent-beaded source.

This argument explains why evaluating z=1 would be an invalid nonzero test: that evaluation sends W to zero. It also explains why adding rational-function inverses is not automatically harmless: the monomial-content direct sum is the Laurent-ring argument.

### Termwise vanishing after adding hairs

The z-1 bead expands as exp(h)-1. The zero-hair term cancels exactly. For every k>=1, the remaining graph contains the zero three-legged subdiagram 2 tau r from Corollary 2. One can isolate it using r, the opposite theta vertex, and the nearest hair vertex; the rest of the hair chain is outside its three boundary points. Gluing a zero AS/IHX diagram into a larger diagram yields zero because those relations remain local after gluing. Thus each coefficient of H(W) is zero, and H(W)=0 in the completed target.

No passage from a finite truncation to an unverified infinite identity is involved: the same subdiagram argument applies to every positive k.

## Nonzero certification and computational dependence

The imported r can be chosen as phi(omega P_gl P_osp P_exc), with the degree assignments deg(tau)=1, deg(sigma)=2, deg(omega)=3. Vogel's character associated to the D(2,1,alpha) family sets tau=0 and yields

chi(r) = 27 omega^3 (27 omega^2 + 4 sigma^3),

where sigma=4(ab+bc+ca), omega=8abc and a+b+c=0. Using the published character formula, the exact arithmetic substitution (a,b,c)=(1,2,-3) gives sigma=-28, omega=-48 and chi(r)=76,441,190,400, which is nonzero. This independently checks the elementary nonvanishing arithmetic conditional on the imported character theorem; it does **not** reconstruct a graph weight-system evaluation from first principles.

Vogel's proof explicitly invokes computer work: the modules G_n in the proof of Theorem 8.4 are described using low-cardinality calculations (manuscript p. 63); p. 64 invokes a computer-checked surjectivity G_6(X)->G_7(X) for |X|<6; p. 65 states a computer calculation of the nonzero proportionality coefficient 2^-10. An earlier supporting diagram relation in Lemma 5.7.1 (p. 25) likewise refers to computer calculations. The p. 65 discussion mentions another evaluation route through the Lie superalgebra, but this audit does not claim to implement that route or eliminate all computational dependence.

No raw calculation files or complete graph-reduction certificate for those imported steps were recovered or rerun. The acceptance is based on the published theorem with these dependencies disclosed. The short hair-map argument itself adds a cohomological grading and a termwise gluing argument; its correctness does not require a new graph enumeration in this audit.

## Grading and scope checks

The two uses of “loop degree” differ. An r of Lambda-degree 15 has F_3 degree 17, hence 34 total vertices, of which three are univalent and 31 trivalent. Inserting it into one theta vertex leaves 32 trivalent vertices and 48 edges. The connected closed graph therefore has b_1=48-32+1=17, as stated by Patureau-Mirand. Ohtsuki's source loop-degree is half the trivalent count, namely **16**, not 17. Adding k hairs gives ordinary total degree 16+k while retaining b_1=17 and Ohtsuki loop-degree (T-U)/2=16.

The element is finite in one source degree and does not rely on completing the source. The target completion accommodates infinitely many zero coefficients. The decisive ring is the original Q[z,z^-1]. Taking A=1 satisfies A(1)=1 and symmetry and recovers that ring exactly; therefore no unproved injectivity of extension to a larger bead ring is needed.

## Acceptance boundaries

- Credit: Patureau-Mirand's published Theorem 4, using Vogel's imported diagram results.
- Accepted outcome: the original stated injectivity conjecture is false; its explicit Laurent case is false.
- Not claimed: novelty, a freshly enumerated kernel certificate, minimal possible loop degree, noninjectivity for every separate localization, or a knot-realizability theorem.
- Audit checks: exact primary-source hashes and sizes; all short-proof diagrams; independent map/quotient comparison; the content-zero projection argument; formal-series vanishing; exact degree conversion; nonzero arithmetic from the imported character formula.
- This edition preserves the complete substantive audit without a mathematical correction. It distributes authored audit, acceptance, status and source metadata only; programs, raw outputs, generated certificates, datasets, copied third-party source documents/text/images and private coordination material are excluded.
- Edition preparation rechecked accepted-package byte identities and publication integrity. It did not newly retrieve or inspect third-party source content, repeat the literature search, rerun mathematical programs, or reproduce Vogel's imported computational steps. Historical inspection and bounded status findings remain those of the October 10, 2026 audit.
- QUEUE.md and unrelated repository content are unchanged. No merge, release, DOI creation, journal submission or external outreach is implied.
