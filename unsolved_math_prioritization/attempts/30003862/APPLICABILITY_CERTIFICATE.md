# Credited prior-result certificate: polar cylinders and affine complements

Problem 30003862 / OWR-16169-009, rank 1202. Audited 10 October 2026 UTC.

## Decision

**ACCEPT_CREDITED_PRIOR_RESOLUTION**, for the source's del Pezzo hypersurface setting. The equivalence is an established result, credited to Jihun Park together with the earlier implication of Ivan Cheltsov, Adrien Dubouloz and Park. This certificate is an applicability and source-status audit, not a new solution or a claim of novelty.

There are **zero new proof-search turns**. The adjacent automorphism-extension problem 30003863 is not resolved, reclassified or otherwise accepted here.

## 1. Exact objects and conventions

Work over an algebraically closed field of characteristic zero. A del Pezzo surface is normal, projective and integral, and its anticanonical divisor is ample. The allowed singularities are at worst Du Val. The surface comes with the specified hypersurface embedding, not an arbitrary embedding into an unspecified ambient variety:

- A cubic surface in projective 3-space, with anticanonical degree 3.
- A degree-4 hypersurface in P(1,1,1,2), with anticanonical degree 2.
- A degree-6 hypersurface in P(1,1,2,3), with anticanonical degree 1.

The original report also lists hypersurface degrees 1 and 2 in projective 3-space. Those have different anticanonical degrees and are handled separately in Section 4. The degree of the defining polynomial must not be confused with K_S squared.

Write W = P minus S for the affine complement. In this certificate, **cylindrical affine** means that W contains a nonempty principal open subset W_f isomorphic to Z times A^1, for an affine variety Z. It does not mean that W itself is a product, nor merely that some unspecified open subset is a cylinder.

An anticanonical polar cylinder on S means an open set S minus Supp(E), isomorphic to Z times A^1, where E is an effective rational divisor with E Q-linearly equivalent to -K_S. The equivalence relation is Q-linear equivalence; ordinary numerical equivalence alone is insufficient. The divisor E need not be integral or reduced. The boundary uses its support.

“Unipotent subgroup” below means a nontrivial algebraic unipotent subgroup. Its trivial subgroup is not evidence of an action. In characteristic zero over the stated field, a nontrivial unipotent algebraic group contains a subgroup isomorphic to G_a. A nontrivial such subgroup in Aut(W) acts nontrivially on W.

## 2. The exact credited implication chain

Use these three predicates:

- A: S has an anticanonical polar cylinder.
- C: W contains a principal open cylinder.
- G: W admits a nontrivial algebraic G_a action.

Park's institutional preprint states A if and only if C explicitly as **Corollary 3.2**, p.5. Its **Proposition 2.3**, p.3, gives C if and only if G. Its **Theorem 1.3**, p.2, credits the earlier direction from A to a unipotent subgroup to Cheltsov–Dubouloz–Park. Its **Theorem 1.4**, p.2, supplies the converse obstruction: absence of A excludes such a subgroup. Consequently:

1. A implies G, hence C. Contraposition gives absence of C implies absence of A.
2. Absence of A implies absence of G, hence absence of C.
3. Together these give the requested equivalence of the two absence conditions.

The first of these directions was already available from the earlier result. There is no remaining “converse” to search for in this exact source setting.

This is not a conclusion inferred only from a paper's title. Park's original Oberwolfach contribution, printed pp.1728–1730 in **OWR 28/2018**, gives the earlier implication as Theorem 2, then reports that the displayed equivalence has been verified and supplies the needed Theorem 4 on p.1729. Conjecture 5 starts on p.1730 and asks a different, stronger question about all automorphisms.

The publication metadata is also verified: Jihun Park, *G_a-Actions on the Complements of Hypersurfaces*, **Transformation Groups 27 (2022), 651–657**, DOI **10.1007/s00031-020-09589-x**, published online **4 July 2020**. The publisher's accessible abstract confirms the polar-cylinder/unipotent-subgroup equivalence. The publisher's full subscription PDF was not inspected here; exact numbered statements and proofs were read in the five-page institutional preprint, corroborated by the published survey below.

## 3. Survey cross-check and general-theorem boundary

Cheltsov–Park–Prokhorov–Zaidenberg, *Cylinders in Fano varieties*, **EMS Surveys in Mathematical Sciences 8 (2021), 39–105**, DOI **10.4171/EMSS/44**, gives the exact three-way surface equivalence in **Theorem 4.20**, pp.82–83. Its standing field convention is algebraically closed characteristic zero. The surrounding setup explicitly restricts to Du Val del Pezzo surfaces of anticanonical degrees 1, 2 and 3 in the three models of Section 1.

Do not replace Theorem 4.20 by an unrestricted interpretation of **Theorem 4.25**, p.84. The latter is a separate, more general *one-way* statement and retains the preceding hypotheses:

- X is normal projective and D is ample Cartier.
- The section ring of (X,D), as a graded ring, is a weighted polynomial ring modulo one weighted-homogeneous polynomial F of degree d.
- The map of the ambient weighted projective space defined by its complete degree-d system is an embedding.

Under these conditions, a nontrivial G_a action on the complement implies a D-polar cylinder on X. The survey identifies this as Park's Theorem 3.1. It does not assert a converse for arbitrary X, nor does it remove the ring or embedding assumptions. For the present surface certificate, Theorem 4.20 and Park's explicit surface corollary avoid any need to extend these hypotheses.

The survey distinguishes arbitrary open cylinders from principal open cylinders near its introduction. For the affine-action equivalence used here, the principal-open convention is preserved exactly as in Park's Proposition 2.3 and the source report.

## 4. Plane and quadric boundary cases

Park's preprint discusses planes and quadrics and then excludes them from the main degree-1/2/3 anticanonical discussion. The following elementary coordinate checks cover these already-known cases without silently treating their anticanonical section rings as cubic models.

### Plane

If S is a plane in P^3, then P^3 minus S is A^3, hence a cylinder. On S = P^2, let L be a line. The effective divisor 3L is linearly equivalent to -K_S, and S minus L is A^2. Thus A and C are both true, and both absence conditions are false.

### Normal quadric

Over the stated field, a normal integral quadric in P^3 is either smooth or a rank-3 quadric cone. Coordinates can be chosen so that its equation is

    q = x_0 x_1 - Q(x_2,x_3) = 0,

where Q is x_2 x_3 in the smooth case or x_2 squared in the cone case. On the chart x_0 nonzero, S is A^2, with x_1 determined by x_2,x_3 after setting x_0=1. If H_0 denotes the hyperplane-section Cartier divisor cut by x_0=0, adjunction gives -K_S equivalent to 2H_0. Hence E=2H_0 supplies an anticanonical polar cylinder. On the cone, H_0 may be nonreduced; this is allowed, and taking its support gives the same affine chart.

On W=P^3 minus S, the homogeneous quotient f=x_0 squared/q is a regular function. Its nonvanishing locus is exactly the chart x_0 nonzero within W. With x_0=1 and t=q=x_1-Q(x_2,x_3), this principal open set is

    Spec k[x_2,x_3,t,t^(-1)] = (A^1 times G_m) times A^1.

This proves C. Again A and C are both true. Reducible or nonreduced quadrics fall outside the normal integral del Pezzo assumptions and are not added to the claim.

These elementary verifications explain why the source's initial degree-at-most-3 list causes no missing low-hypersurface-degree case. They are not novel results or proof-search routes.

## 5. One local proof clarification, with a limited role

The institutional proof of Theorem 3.1 clears denominators of a locally nilpotent derivation by a power of F, then passes to the quotient by F. Merely choosing an arbitrarily large clearing power is not sufficient to ensure that the quotient derivation is nonzero. For example, on k[F,x], F times d/dx vanishes modulo F.

The complete standard normalization is given in **DENOMINATOR_NORMALIZATION.md**: clear once, then remove the maximal common F-power from the generator images. That power exists by finite generation and positive grading. F-invariance preserves local nilpotence, and maximality ensures a nonzero reduction. Equivalently, minimize the clearing exponent over all integers. Minimizing only among nonnegative integers can miss a further division when exponent zero already clears denominators.

This addresses the specified local inference. It is not a claim that Park's theorem fails, an assertion about wording of the uninspected journal PDF, or a complete re-audit of every cited cone theorem. The main acceptance is a credited application of published mathematical inputs.

## 6. Acceptance and exclusions

Accepted: the equivalence for the source-corrected normal Du Val del Pezzo hypersurfaces over an algebraically closed characteristic-zero field, including the separate plane and normal-quadric checks. A dated triage that leaves the reverse direction open is superseded in this scope by the actual source statements.

Not accepted or inferred:

- Aut(P minus S) equals Aut(P,S). Absence of G_a actions does not classify all automorphisms. In particular, this certificate does not settle the smooth-cubic automorphism conjecture.
- A claim about all del Pezzo surfaces, more general singularities, arbitrary embeddings, higher-dimensional Fano varieties, positive characteristic, or nonclosed ground fields.
- A full independent verification of all proofs in the cited literature, formal proof-assistant certification, human peer review, exhaustive historical priority, or worldwide novelty.
- A new mathematical contribution based on rediscovering the cited equivalence.

## Public sources

1. J. Park, *Automorphism groups of the complements of hypersurfaces*, OWR 28/2018, printed pp.1728–1730: https://ems.press/content/serial-article-files/46750 ; report DOI https://doi.org/10.4171/owr/2018/28 .
2. J. Park, *G_a-Actions on the Complements of Hypersurfaces*, Transformation Groups 27 (2022), 651–657: https://doi.org/10.1007/s00031-020-09589-x .
3. Author's institutional preprint CGP18017: https://cgp.ibs.re.kr/files/preprints/CGP18017_JHP_Ga-Actions%20on%20the%20complements%20of%20hypersurfaces.pdf .
4. I. Cheltsov, J. Park, Y. Prokhorov and M. Zaidenberg, *Cylinders in Fano varieties*: https://ems.press/content/serial-article-files/37019 ; DOI https://doi.org/10.4171/EMSS/44 .
5. I. Cheltsov, A. Dubouloz and J. Park, *Super-rigid affine Fano varieties*, Compositio Mathematica 154 (2018), no.11, 2462–2484; cited as the earlier input in sources 1–4. Its complete proof was not newly inspected for this certificate.

See SOURCE_LEDGER.json for public PDF hashes, sizes, original retrieval metadata, and this audit's actual inspection scope. No third-party source document or copied source text is part of this edition.
