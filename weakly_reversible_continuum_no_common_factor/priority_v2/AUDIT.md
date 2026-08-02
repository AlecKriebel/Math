# Narrow post-solution priority audit: the fixed-support gcd-one family

**Audit date:** 1 August 2026  
**Status:** conservative, targeted audit of primary sources; not a claim of exhaustive global priority

## Question audited

This audit was performed only after the construction, family theorem, and independent symbolic verifier were complete. It addresses the strengthened claim about the *family*, rather than redoing the mathematical search.

The precise conjunction sought in earlier work was:

1. a fixed weakly reversible, preferably reversible, reaction support;
2. a positive-dimensional family of positive rate vectors, with dimensions remaining after quotienting by global time scaling;
3. the same positive-dimensional equilibrium continuum in one stoichiometric compatibility class for every rate vector in that family; and
4. no nonconstant common factor in the coordinate vector field for a nonempty Zariski-open subset of the family.

For the construction proved in this project, the fixed support has three species, ten complexes, twenty directed reactions (ten reversible pairs), one linkage class, and full stoichiometric rank. The conic-preserving rate locus is a four-dimensional linear kernel in the twenty-dimensional rate space. Its positive part is a relatively open rational polyhedral cone; after global rate scaling it has three nontrivial projective dimensions. Geometric gcd one holds on a nonempty Zariski-open subset of this four-dimensional family.

## Executive conclusion

No audited source supplies the four properties above in combination. The defensible priority statement is therefore that this appears to be the first explicit **fixed-support positive rate family preserving a compatibility-class continuum while having generically gcd-one coordinate polynomials**.

Two qualifications are essential.

- It is **not** safe to claim the first positive-dimensional fixed-support rate family preserving a steady-state continuum. Boros--Craciun--Yu already give substantial rate flexibility on a fixed reversible support, and their displayed formulas contain a positive-dimensional subfamily preserving the same curve. Every member of that family, however, obtains the continuum from a common scalar factor.
- The four-dimensional cone here is not open in the ambient twenty-dimensional rate space. It has codimension sixteen. “Relatively open in the conic-preserving linear family” is accurate; “robust under arbitrary rate perturbations,” “an open set of rates,” or “generic in rate space” is not.

Thus the credible novelty is the conjunction of a nontrivial fixed-support family and generic absence of a coordinate common factor, not any one of “continuum,” “nonprincipal steady-state ideal,” “rate family,” or “fixed support” in isolation.

## The direct predecessor and a necessary correction

Boros, Craciun, and Yu construct weakly reversible systems with infinitely many positive steady states, including a reversible network with a single connected component. Their abstract and constructions state explicitly that the continua are produced by a common multivariate factor. They end by asking whether a weakly reversible mass-action system can have infinitely many positive steady states *without* a common factor in the coordinate polynomials [BCY20].

Their Section 5 also makes clear that their example is not an isolated rate vector. In the notation of their Example 4.3, they impose

\[
\frac{\kappa^1_2}{\kappa^1_1}
=\frac{\kappa^2_2}{\kappa^2_1}
=\frac{\kappa^3_2}{\kappa^3_1}
=\frac{\kappa^4_2}{\kappa^4_1},
\qquad
\frac{\kappa^1_3}{\kappa^1_2}
=\frac{\kappa^2_3}{\kappa^2_2}
=\frac{\kappa^3_3}{\kappa^3_2}
=\frac{\kappa^4_3}{\kappa^4_2}.
\]

The common scalar factor is

\[
\kappa^1_1x^2+\kappa^2_1xy^2+\kappa^3_1y-\kappa^4_1xy.
\]

This gives six free positive parameters: four coefficients of the scalar polynomial and the two common positive ratios. This dimension count is our inference from their displayed parametrization, not a priority claim made in their paper. If the four polynomial coefficients are fixed up to a common positive scalar, the exact same zero curve remains while the scalar and two ratios vary. Hence their formulas already contain a three-dimensional same-curve family, or two dimensions after quotienting by global time scaling. The coordinate polynomials throughout that family retain the displayed common factor.

Obatake and Walker later revisit this example and again identify the common-factor curve. They also display a fixed-support positive rate ray

\[
(k,k,5k,k,k,5k,k,k,k,k,k,k,k,k,5k,k,5k,k,k,k),\qquad k>0,
\]

which preserves the continuum by global time scaling [OW24]. This ray is not a nontrivial projective family, but it reinforces the need to state precisely whether dimensions are counted before or after time scaling.

The correction to any broad draft claim is therefore:

> Do not say “the first positive-dimensional fixed-support rate family preserving a continuum.” Say that the new family is, to our knowledge, the first such weakly reversible family whose coordinate vector field is gcd one on a nonempty Zariski-open subset of the continuum-preserving family.

## Ambient genericity and the exceptional parameter locus

Feliu, Henriksson, and Pascual-Escudero prove that parameters admitting infinitely many compatible positive steady states lie in a proper algebraic set (Corollary 3.5), and that weakly reversible mass-action networks are nondegenerate in the sense needed for generic finiteness (Corollary 3.13) [FHP26]. Their Example 3.12 discusses the fine-tuned common-factor construction of Boros--Craciun--Yu.

This generic-geometry result does not conflict with the present family. The conic-preserving family is a four-dimensional linear subspace of a twenty-dimensional rate space, hence an ambient exceptional locus of codimension sixteen. Positivity is open only relative to that subspace. Likewise, the Zariski-open gcd-one assertion is relative to the four-dimensional family, not to all twenty rate coordinates.

Recommended terminology is:

- “a four-dimensional conic-preserving positive rate cone”;
- “relatively open in its four-dimensional linear span”;
- “gcd one on a nonempty Zariski-open subset of that family”; and
- “three dimensions modulo global time scaling.”

## Adjacent algebraic and rate-locus results

The following primary sources delimit what is and is not new.

| Source | Relevant earlier result | Why it does not supply the audited conjunction |
|---|---|---|
| Pérez Millán--Dickenstein--Shiu--Conradi [PMDSC12] | Binomial, often nonprincipal steady-state ideals and monomial parametrizations of positive-dimensional steady-state varieties; includes weakly reversible toric examples. | It does not give the required fixed full-rank weakly reversible family with a continuum inside one compatibility class and generically gcd-one coordinate polynomials. Positive-dimensional steady-state varieties alone are therefore not a novelty claim. |
| Adamer--Helmer [AH20] | “Families” of toric reaction networks generated recursively from smaller networks. | Here “family” primarily means a sequence of changing network supports, not a positive-dimensional rate locus on one fixed support preserving one fixed compatible continuum. |
| Rahkooy--Sturm [RS21] | Necessary and sufficient parameter conditions for toricity and shifted toricity on parametrized reaction systems. | It establishes fixed-support parameter strata for an algebraic property, but not the weakly reversible compatible-continuum/gcd-one conjunction. |
| Brustenga i Moncusí--Craciun--Sorea [BCS22]; Craciun--Deshpande--Jin [CDJ24] | Positive-dimensional disguised-toric loci of rate constants, including dimension results for such loci. | Systems in these loci are dynamically equivalent to complex-balanced systems; the cited work uses the unique positive equilibrium in each invariant polyhedron. Thus the disguised-toric mechanism itself does not yield a positive continuum in one compatibility class. |
| Feliu--Henriksson [FH26] | Fixed-support vertically parametrized systems whose solution sets are toric or invariant, with parameter-dependent monomial descriptions. | This is close in its treatment of whole parameter families, but it does not provide the audited same-compatible-continuum and coordinate-gcd conjunction. |
| Banaji--Feliu [BF26] | General geometric results allow exceptional full-rank sparse systems to have a continuum of positive degenerate equilibria; see Theorem 4.24 and Corollary 4.25. | The results do not impose weak reversibility or reversibility, analyze a coordinate common factor, or exhibit the required fixed-support positive rate family. They do show that exceptional full-rank continua are anticipated by general theory. |
| Kothari--Deshpande [KD24] | Endotactic and strongly endotactic networks with infinitely many positive steady states. | Their highlighted examples are not weakly reversible and use a scalar-polynomial common-factor construction; some have no weakly reversible dynamically equivalent realization. |
| Curiel et al. [C+24] | Classification and algebraic study of positive steady-state varieties in small two-species, two-reaction networks. | This is useful small-network context, but does not provide a reversible fixed-support family with the audited properties. |

These works also rule out several overbroad formulations. The present result should not be advertised as the first nonprincipal steady-state ideal, the first positive-dimensional mass-action steady-state variety, the first algebraically constrained rate locus, or the first family of toric/steady-state systems.

## Manuscript-ready priority language

A conservative paragraph suitable for the manuscript is:

> Boros, Craciun, and Yu constructed weakly reversible, including reversible connected, mass-action systems with positive steady-state continua, but their continua arise from a common scalar factor in every coordinate of the vector field. Their parametrized formulas also allow positive-dimensional fixed-support rate families, so rate flexibility by itself is not new. The construction here instead supports a four-dimensional positive cone of rates preserving the same conic in the unique positive compatibility class (three dimensions modulo global time scaling), while geometric gcd one holds on a nonempty Zariski-open subset of that cone. In a targeted audit of primary sources through 1 August 2026, we found no earlier weakly reversible fixed-support family with this conjunction. The cone is a codimension-sixteen exceptional locus in the ambient twenty-dimensional rate space, consistent with generic finiteness results for weakly reversible systems.

An even more cautious priority sentence is:

> To our knowledge, this is the first explicit weakly reversible fixed-support positive rate family that preserves a continuum in one compatibility class and is generically free of a common coordinate factor within that family.

Wording to avoid:

- “the first positive-dimensional fixed-support family preserving a continuum”;
- “an open set of rate constants,” unless immediately qualified as relative openness;
- “a structurally robust continuum” or “robust under rate perturbations”;
- “generic rates,” without specifying the four-dimensional constrained family;
- “the first nonprincipal or toric steady-state ideal”; and
- any global minimality or exhaustive-priority claim.

## Search protocol and limitations

The audit used narrow searches for combinations of:

- “weakly reversible” or “reversible” with “infinitely many positive steady states,” “continuum,” and “positive-dimensional”;
- “common factor,” “no common factor,” “gcd,” and “nonprincipal steady-state ideal”;
- “fixed support,” “rate family,” “parameter locus,” “toric locus,” and “disguised toric locus”; and
- generic geometry of mass-action steady states and parameter-dependent toricity.

Author manuscripts on arXiv and official DOI/publisher records were used as primary sources. Secondary pages and search snippets were used, if at all, only to locate primary material and not as support for a substantive conclusion. No author or other researcher was contacted.

This is a targeted priority audit, not a systematic review. It may miss work described with different terminology, unindexed or unpublished manuscripts, work outside the searched language and databases, or results embedded in papers whose titles and abstracts do not expose the relevant conjunction. “To our knowledge” and “we found no earlier example” are therefore warranted; an unqualified proof of worldwide priority is not.

## Primary-source bibliography

**[AH20]** M. F. Adamer and M. Helmer, “Families of Toric Chemical Reaction Networks,” *Journal of Mathematical Chemistry* **58** (2020), 2061--2093. [DOI](https://doi.org/10.1007/s10910-020-01162-x); [arXiv:1906.03931](https://arxiv.org/abs/1906.03931).

**[BCY20]** B. Boros, G. Craciun, and P. Y. Yu, “Weakly Reversible Mass-Action Systems With Infinitely Many Positive Steady States,” *SIAM Journal on Applied Mathematics* **80** (2020), 1936--1946. [DOI](https://doi.org/10.1137/19M1303034); [arXiv:1912.10302](https://arxiv.org/abs/1912.10302).

**[BCS22]** L. Brustenga i Moncusí, G. Craciun, and M.-Ș. Sorea, “Disguised Toric Dynamical Systems,” *Journal of Pure and Applied Algebra* **226** (2022), 107035. [DOI](https://doi.org/10.1016/j.jpaa.2022.107035); [arXiv:2006.01289](https://arxiv.org/abs/2006.01289).

**[BF26]** M. Banaji and E. Feliu, “Positive Equilibria in Mass Action Networks: Geometry and Bounds,” arXiv:2409.06877, version 4, 4 May 2026. [arXiv](https://arxiv.org/abs/2409.06877).

**[C+24]** M. Curiel, E. Farr, G. Fries, L. D. García Puente, J. Hutchins, and V. Nguyen Hoang, “Positive Steady-State Varieties of Small Chemical Reaction Networks,” arXiv:2406.09514 (2024). [arXiv](https://arxiv.org/abs/2406.09514).

**[CDJ24]** G. Craciun, A. Deshpande, and J. Jin, “The Dimension of the Disguised Toric Locus of a Reaction Network,” arXiv:2412.02620 (2024). [arXiv](https://arxiv.org/abs/2412.02620).

**[FH26]** E. Feliu and O. Henriksson, “Toric Invariance of Vertically Parametrized Systems,” arXiv:2411.15134, version 4, 14 May 2026. [arXiv](https://arxiv.org/abs/2411.15134).

**[FHP26]** E. Feliu, O. Henriksson, and B. Pascual-Escudero, “The Generic Geometry of Steady State Varieties,” *SIAM Journal on Applied Algebra and Geometry* **10** (2026), 519--548. [DOI](https://doi.org/10.1137/25M1731289); [arXiv:2412.17798](https://arxiv.org/abs/2412.17798).

**[KD24]** S. Kothari and A. Deshpande, “Endotactic and Strongly Endotactic Networks With Infinitely Many Positive Steady States,” *Journal of Mathematical Chemistry* **62** (2024), 1454--1478. [DOI](https://doi.org/10.1007/s10910-024-01617-5); [arXiv:2303.08781](https://arxiv.org/abs/2303.08781).

**[OW24]** N. K. Obatake and E. Walker, “Newton--Okounkov Bodies of Chemical Reaction Systems,” *Advances in Applied Mathematics* **155** (2024), 102672. [DOI](https://doi.org/10.1016/j.aam.2024.102672); [arXiv:2203.03840](https://arxiv.org/abs/2203.03840).

**[PMDSC12]** M. Pérez Millán, A. Dickenstein, A. Shiu, and C. Conradi, “Chemical Reaction Systems With Toric Steady States,” *Bulletin of Mathematical Biology* **74** (2012), 1027--1065. [DOI](https://doi.org/10.1007/s11538-011-9685-x); [arXiv:1102.1590](https://arxiv.org/abs/1102.1590).

**[RS21]** H. Rahkooy and T. Sturm, “Parametric Toricity of Steady State Varieties of Reaction Networks,” in *Computer Algebra in Scientific Computing (CASC 2021)*, LNCS **12865** (2021), 314--333. [DOI](https://doi.org/10.1007/978-3-030-85165-1_18); [arXiv:2105.10853](https://arxiv.org/abs/2105.10853).
