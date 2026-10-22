# The real ternary zero threshold: a consequence of prior work

## Review status of this edition

This is an AI-assisted mathematical exposition accompanied by an independent internal AI mathematical and source audit. These authored documents are unrefereed. Acceptance means the scoped theorem-dependent conclusion of that audit, not external human peer review, journal acceptance of this exposition or audit, or formal proof-assistant certification. The credited existence theorem and its patchworking foundations are prior mathematics of the cited authors; no novelty or full independent reproof is claimed.

## Claim and credit

For every integer k >= 3, alpha(k) >= k^2 + 1, where alpha(k) is the least integer A such that a real positive semidefinite homogeneous ternary form p of degree 2k with more than A distinct zeros in RP^2 has a factorization p = h^2 q with h indefinite.

The existence input is prior work of Erwan Brugallé, Alex Degtyarev, Ilia Itenberg, and Frédéric Mangolte (BDIM), not a new construction. The primary route here uses their Theorem 4.5. The argument below completely proves the implication from that stated existence theorem to the threshold claim. It imports the existence theorem and its patchworking foundations; it does not replace their proof with a coefficient-level construction.

## The exact imported theorem

BDIM, Theorem 4.5, supplies for every k >= 3 a finite real algebraic plane curve C of degree 2k. Its number B(k) of distinct real projective points is

- B(3l) = 12l^2 - 4l + 2;
- B(3l + 1) = 12l^2 + 4l + 3;
- B(3l + 2) = 12l^2 + 12l + 6.

Here l >= 1 in every case. The ambient plane has the standard real structure and real part RP^2. The count is ordinary cardinality, not a singularity-weighted count. The theorem and construction are on page 14 of the inspected author manuscript; the underlying real-polynomial patchworking statement is Theorem 3.1, pages 6-7. [BDIM]

## Connectedness and sign

The complement of a finite set E in S^2 is path connected. If E is nonempty, stereographic projection from a point of E reduces the assertion to R^2 minus finitely many points. Given two points in that complement, choose a third point off the finitely many lines joining either endpoint to a removed point. The two resulting line segments avoid the removed points. The case E empty is immediate. Lifting a finite subset of RP^2 to S^2 and projecting connecting paths proves that RP^2 minus finitely many points is also path connected.

Let F be a nonzero real homogeneous polynomial of degree 2k with a finite projective zero set. The function

    [v] -> F(v) / (v_1^2 + v_2^2 + v_3^2)^k

is well defined on RP^2. It is continuous and nowhere zero on the nonempty connected complement of that zero set. It therefore has a single sign there. Multiplying F by +1 or -1 makes it nonnegative on all nonzero real vectors; it vanishes at the origin because its degree is positive. Thus one of the two signs of F is PSD, with exactly the same zeros and degree.

## A real equation of the correct degree

A reduced plane algebraic curve of degree d has a squarefree homogeneous defining polynomial F over C of degree exactly d, unique up to nonzero scalar. Invariance under standard complex conjugation implies conjugate(F) = cF, with c conjugate(c) = 1. Choose a nonzero scalar a with a/conjugate(a) = c. Then aF has real coefficients. This descent does not assume that C is irreducible.

The curves used in BDIM's construction are reduced algebraic curves. Their construction uses real polynomials and the coordinate squaring map; away from the coordinate divisors the map is étale, and none of those divisors is a component of the constructed curve. In particular this is an ordinary reduced degree-2k plane curve, not a nonreduced divisor whose support has silently been assigned the divisor's degree. Equivalently, one can use its real homogeneous defining equation directly. [BDIM, Sections 3.1 and 4.1]

Applying this to Theorem 4.5 gives a real degree-2k equation F with precisely B(k) distinct projective zeros. The preceding sign argument supplies a PSD form p with those same zeros.

## Why the forbidden factor is absent

An indefinite real homogeneous ternary form h takes opposite signs at two nonzero real vectors. Positive normalization places those vectors on S^2 without changing their signs, regardless of the parity of deg(h). If the projective zero set of h were finite, its inverse image on S^2 would be finite. The restriction of h to the complement would be a nonzero continuous function on a connected space, and could not take opposite signs. Thus an indefinite form has infinitely many distinct projective zeros.

If p = h^2 q, every projective zero of h is a zero of p. The finite zero set of the constructed p consequently excludes every indefinite square factor. This does not exclude semidefinite square factors, and no such stronger claim is needed.

## All degrees and the strict threshold

In the three residue classes, direct subtraction gives

- B(3l) - ((3l)^2 + 1) = (3l - 1)(l - 1) >= 0;
- B(3l + 1) - ((3l + 1)^2 + 1) = 3l(l - 1) + l + 1 > 0;
- B(3l + 2) - ((3l + 2)^2 + 1) = 3l^2 + 1 > 0.

These algebraic inequalities hold for every integer l >= 1. They are not an extrapolation from finite testing. The endpoint k = 3 has B(3) = 10 = 3^2 + 1.

For each k, the constructed PSD form has B(k) distinct zeros and no indefinite square factor. Every integer A < B(k) therefore fails the threshold property, since this form has strictly more than A zeros. Hence

    alpha(k) >= B(k) >= k^2 + 1

for every k >= 3. A witness with N zeros rules out thresholds below N; it does not alone rule out threshold N. This proves exactly the requested direction.

## The other theorem and the inspection limit

BDIM's Theorem 4.8 states the existence of finite degree-2k real plane curves with k^2 + g + 1 real points when 0 <= g <= k - 3. Its statement, specialized to g = 0, also implies the target through the same bridge. It is from the same paper, not an independent literature confirmation.

The audit did not fully reconstruct one interface in its printed patchworking proof. The curve C1 is specified with one order-(2k-4) boundary contact, while the perturbed curve named from Lemma 3.2 has k-2 separate order-two contacts on the matching boundary. Theorem 3.1 requires common-edge compatibility. For k >= 4 these contact profiles differ; no unstated deformation is certified here. Theorem 4.5 does not use this C1/Lemma 3.2 interface. This is an explicit limit of the reconstruction, not a proof that Theorem 4.8 is false.

There is also a minor numerical discrepancy near Theorem 4.5: its formula gives B(6) = 42, whereas the following degree-12 discussion refers to 43. This proof uses the displayed theorem formula, for which 42 >= 37; it does not silently alter either passage. The discrepancy does not affect the implication proved above.

## Original problem and exclusions

Reznick's Oberwolfach contribution uses half-degree indexing alpha(k); his 2015 slides instead use alpha(2k) for the same degree-2k threshold. The original threshold applies to arbitrary PSD ternary forms; an introductory discussion of irreducible examples does not add an irreducibility restriction to it. [OWR, R15]

This is a credited prior-result resolution of the specified lower-bound question. It does not compute alpha(k) exactly, resolve a general SOS isolated-zero maximum, supply explicit coefficients for every degree, reconcile historical exception lists, or claim novelty.

## References and inspected editions

- [BDIM] E. Brugallé, A. Degtyarev, I. Itenberg, F. Mangolte, *Real algebraic curves with large finite number of real points*, European Journal of Mathematics 5 (2019), 686-711. DOI: https://doi.org/10.1007/s40879-019-00324-9 . Author manuscript: https://www.i2m.univ-amu.fr/perso/frederic.mangolte/FiniteCurves.pdf . arXiv record: https://arxiv.org/abs/1807.03992 . The theorem locators above refer to the inspected 19-page author manuscript and matching arXiv theorem statements. Publication metadata was verified at the publisher. The publisher's full version-of-record PDF was not inspected.
- [OWR] B. Reznick, *Some old and new results and examples on psd forms which are not sos*, Oberwolfach Report 17/2014, printed pages 1010-1013; target on page 1011. https://doi.org/10.4171/owr/2014/17 . Public PDF: https://ems.press/content/serial-article-files/46507 .
- [R15] B. Reznick, *Ternary forms with lots of zeros (Slightly corrected version)*, CIRM, October 16, 2015. https://reznick.web.illinois.edu/10-16-15f.pdf . Definition on PDF slides 11-16, conjecture on slide 29, historical exception list on slides 47-48.
