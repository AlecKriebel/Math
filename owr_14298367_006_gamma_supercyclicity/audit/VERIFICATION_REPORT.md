# Verification and priority decision

## Verdict

The submitted argument is mathematically valid under the original report's standing hypotheses. It establishes the full equivalence for every subset Gamma of the complex numbers, including empty and zero-only sets. No measurability, closure, boundedness, or multiplicative property of Gamma is required.

**The priority gate does not clear a claim that the main theorem and scalar criterion are new.** The scalar criterion predates the candidate, and the full Banach-valued amplification is a short corollary of a 2020/2021 theorem. The conclusion may be a useful explicit observation answering the later Oberwolfach question, but that is a narrower contribution than a new underlying dynamical theorem.

This distinction matters: a proof can correctly settle the mathematical question while failing a clean originality audit. We have not found an explicit earlier printed answer to this exact question; the negative priority assessment concerns the concrete derivability of the claimed main ingredients from earlier results.

## Exact scope

Assume a separable complex Lp(X,mu), 1 <= p < infinity; a bijective bimeasurable map f for which both composition directions are bounded; a measurable wandering generator W with 0 < mu(W) < infinity and X the disjoint union of its integer iterates; and a uniform bounded-distortion constant K comparing mu(f^j A)/mu(A) with mu(f^j W)/mu(W) for measurable A contained in W.

For the associated shift defined by

\[
(B_w a)_j=w_{j+1}a_{j+1},\qquad
w_j=\left(\frac{\mu(f^{j-1}W)}{\mu(f^jW)}\right)^{1/p},
\]

the statement verified is

\[
T_f\text{ is }\Gamma\text{-supercyclic}
\iff B_w\text{ is }\Gamma\text{-supercyclic}.
\]

The original question is on p.1083 of [Oberwolfach Report 19/2024](https://doi.org/10.4171/OWR/2024/19). Separability is stated in the talk's general setting on p.1081 and in the preceding talk on p.1078. The supplied catalog page returned a challenge, so its current status and ID mapping could not be independently inspected.

## Mathematical checks

| Component | Result | Evidence |
| --- | --- | --- |
| Original hypotheses and shift convention | Pass | `source-match.md`, official report pp.1078–1083 |
| Composition/sequence-space conjugacy | Pass | Measure-class, measurable gluing, norm bounds, and surjectivity checked |
| Scalar shift isometry | Pass | Exact index identity DBw = SD |
| Necessity of both tails with the same lambda | Pass | `proof-adversary.md`; independently rederived with a single anchor coordinate |
| Submitted gliding-hump construction | Pass | Both earlier/later cross-term estimates and convergence checked |
| Independent sufficiency proof | Pass | `independent-derivation.md`: finite-support perturbations and Baire theorem |
| Arbitrary Gamma, p=1, complex phases | Pass | No algebraic closure of Gamma used; inverse scalar appears only in the constructed vector |
| Nonseparable extension | False | Explicit counterexample in `source-match.md` |

The proof has no unresolved substantive mathematical gap in this scope. The original infinite series proof is longer than necessary, but correct. A concise proof uses the perturbation a + lambda^(-1) R_n b to establish transitivity of the family, then the countable-base Baire argument to obtain one dense orbit. Arbitrary uncountable unions of open sets cause no problem.

Required presentation fixes are to state separability explicitly, define k_0=0, and choose each inductive finite set nonempty. The abstract lemma actually needs only a bounded forward translation, since inverse translations can be confined to finitely supported vectors; this strengthening is not needed for the original question.

## Decisive priority check

Abbar and Kuznetsova, *Gamma-supercyclicity of families of translates in weighted Lp-spaces on locally compact groups*, [arXiv:2005.11230v2](https://arxiv.org/abs/2005.11230v2), Theorem B, is a primary antecedent. Version 1 was submitted 22 May 2020, version 2 on 28 October 2020; the journal article is J. Math. Anal. Appl. 495(1) (2021), 124709, [DOI 10.1016/j.jmaa.2020.124709](https://doi.org/10.1016/j.jmaa.2020.124709).

Here is the independently checked application, rather than an inference based solely on its title:

1. On the discrete group Z with weight omega(j)=c_j^(1/p), Theorem B gives the two finite-block tail bounds from scalar Gamma-supercyclicity. With counting measure, an exceptional set of measure less than 1 must be empty.
2. Apply the same theorem to Z^2, translations (-n,0) for n >= 0, and weight omega(j,k)=c_j^(1/p). Each finite set projects to a finite set in the first coordinate, so exactly the same bounds verify the criterion. The resulting operator is the amplification on l^p(Z,c;l^p(Z)).
3. For any nonzero separable Banach E, choose vectors e_k of norm at most 1 whose span is dense. The map R(a)=sum_{k>=1} 2^(-k) a_k e_k from l^p(Z) to E is bounded and has dense range. Its coordinatewise extension is bounded, has dense range, and commutes with translation. The image of a dense Gamma-orbit is dense.
4. The already-verified composition conjugacy and scalar quotient complete the exact equivalence in the candidate.

See `priority-derivation-independent.md` for full assumptions and inequalities. The separate priority audit records the earlier scalar criterion, additional antecedents, contemporary related papers, and the limits of the search.

## Publication disposition

**Original audit disposition (2026-09-23T04:11:29Z):** The user's requested original-resolution paper, GitHub Pages site, and Zenodo upload were conditional on a clean priority audit. That condition was not met. The audit and its checkable evidence were retained and committed. An attributed explanatory note would be a different publication claim and should explicitly foreground the older theorem; no claim to a new amplification theorem or new scalar criterion is warranted by this audit.

**Subsequent authorized scope (2026-09-23):** After discussing the limited novelty and uncertain journal prospects, the user explicitly requested the attributed note, repository publication, website, and manual Zenodo upload package. Version 1.0.0 therefore publishes the explicit application with full attribution, a direct proof, and a derivation from prior results. This change in publication scope does not reverse the priority finding above. See `note-proof-review.md` and `note-attribution-review.md` for the actual manuscript reviews.

The reviews were independent AI-agent analyses followed by synthesis and direct source checking. They are not external refereeing or formal proof-assistant validation. Finite exact-arithmetic checks support only the identities and examples specified in their README; the analytic proofs carry the universal quantifiers.
