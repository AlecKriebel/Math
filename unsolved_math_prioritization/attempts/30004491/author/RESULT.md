# Target, result, and scope

## Exact target

The primary source is Jorge Vitorio Pereira's workshop contribution, *Rational endomorphisms of codimension one foliations*, jointly with Federico Lo Bianco, Erwan Rousseau, and Frederic Touzet, in Oberwolfach Report 24/2020, printed pp. 1293–1295. Conjecture 4 is on p.1294. The workshop was in 2020; the report was published in 2021.

In precise terms the target is:

Let X be a smooth complex projective variety and F a possibly singular holomorphic foliation of complex codimension one. Let f:X -->> X be a dominant rational map with f*F=F. Suppose no positive iterate of f acts trivially on the general leaves of F. Must there exist a generically finite dominant rational map pi:Y -->> X such that pi*F is defined by a nonzero closed rational 1-form on Y?

The source's word `End` includes maps with indeterminacy and noninvertible dominant maps. It is not just the group of regular automorphisms. For automorphisms or birational maps one can quotient by the normal leaf-fixing subgroup; for all dominant rational maps the source uses the congruence identifying maps whose images of a general point lie on the same leaf. An infinite group of ambient symmetries and an infinite transverse action are different hypotheses.

“Virtual” allows a generically finite cover, including ramification and birational modifications. It does not mean an etale cover is guaranteed, nor that a chosen map f necessarily lifts to an arbitrarily chosen cover. The conclusion concerns a meromorphic/rational defining form, not a nonsingular holomorphic form or a rational first integral. “Projective” is a hypothesis on the ambient complex manifold; “transversely projective” is a separate hypothesis on F. Real codimension-one smooth foliations on compact manifolds are not the target.

## Literature gate

Lo Bianco–Pereira–Rousseau–Touzet, *Rational Endomorphisms of Codimension One Holomorphic Foliations*, arXiv:2007.12541v2 (29 October 2020), published in J. Reine Angew. Math. 789 (2022), 43–101, states the same unrestricted assertion as Conjecture D. Its Theorem A proves the implication when F is transversely projective. Proposition E requires Pic(X) isomorphic to Z and a regular self-map of degree greater than one, not merely an arbitrary rational self-map or an unstated Picard-number replacement. Theorem F concerns birational symmetries with explicit singularity and bigness assumptions. The algebraic-part and low-orbit-dimensional reductions are in Sections 2 and 4; those do not give an invariant surface section for every higher-dimensional orbit.

Primary-source searches through 5 October 2026 found no verified general resolution. Two later nearby works were examined rather than treated as solutions:

- Gabriel Fazoli, *Jets of flat partial connections II*, arXiv:2509.13510v1 (2025), Theorem C(A) and Proposition 5.3/Remark 5.4, require X=Pn, n>=3, vanishing of global foliated 1-forms, and instability of a specified first transverse-jet sheaf. Infinite transverse dynamics was not shown here to imply those extra conditions.
- Benoit Claudon–Frederic Touzet, *Structure of Kahler foliations with negative transverse Ricci curvature*, arXiv:2301.06473v2 (2 June 2025), Theorem E, treats regular holomorphic foliations on compact Kahler manifolds with an invariant transverse Kahler metric of quasi-negative Ricci curvature. Its finite transverse automorphism theorem does not cover general singular foliations and dominant rational maps. Section 8 itself distinguishes the possible bimeromorphic extension.

The authors' current publication lists and the arXiv revision pages were checked. A negative search is not a proof that no unpublished or unindexed resolution exists. Both the arXiv v2 and the complete published-version PDF linked from Touzet's publication list were recovered. The published article's Conjecture D, principal theorem hypotheses, definitions, reductions, and selected proof passages were inspected. The full proof and all imported foundations were not independently re-proved. No assertion of a byte match between the arXiv and published versions is made.

## Established here

`PROOFS.md` supplies full arguments for:

1. The standard rational infinitesimal-symmetry normalization: a transverse rational infinitesimal symmetry gives a closed rational defining form.
2. The rational-first-integral case, and a differential-field lemma showing that a foliation with constant field C acquires no nonconstant algebraic first integral in a finite extension.
3. An explicit irrational logarithmic foliation and monomial birational map, with infinite transverse action and no rational first integral on any finite cover.
4. An explicit degree-two quotient of that example, on another P1 x P1, which is virtually additive but not additive downstairs. The formulas, birational descent, degree of the cover, and infinite transverse action are all proved.
5. The precise covariance equation for a rational defining form and the limited conclusion obtainable if a flat affine structure is already known.

These are classical mechanisms or elementary controls, not claimed advances over the general literature. The explicit quotient is a useful test case for this investigation, with no asserted novelty.

## Remaining gap

For an arbitrary singular codimension-one foliation preserved by an arbitrary dominant rational map with infinite transverse action, this investigation does not construct either a transverse rational infinitesimal symmetry or a transversely projective structure. Passing to the algebraic quotient and then an irreducible general orbit closure can leave a purely transcendental foliation with Zariski-dense dynamics in dimension at least three. The restriction and descent results require structure on that orbit closure, which is precisely what is missing.

The covariance identity alone does not produce a flat rational connection, a finite-monodromy affine structure, or an algebraic integrating factor. Bounded symbolic checks and the worked logarithmic model establish none of these assertions for a general f. The five approaches are therefore exhausted with disposition **unsolved, 5/5**.

## Prior-attempt check

The supplied catalog has a queued 0/5 descriptor for this exact ID. The two complete public dataset files were locally hashed and matched the repository's pinned manifest. The target problem record exists, but the separate research-results dictionary has no key `OWR-1703871-006`; this is absence, not a present null-valued report. Exact-ID GitHub code, PR, commit, and branch searches were empty, and the observed main attempts listing did not contain this ID. Topic PR results concerned other foliation problems.

These checks do not certify the absence of deleted branches, unpublished local work, or unindexed conversations. No prior proof is silently credited or overwritten.
