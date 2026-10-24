# Primary-source and priority audit: 21.121

Date: 24 October 2026 UTC. Scope: bounded preparation only. Source-audit completion **100%**; original-discovery completion **0%**. No provisional full solution or research selection is promoted.

## Finding with its precise limit

The current official Notebook explicitly records a negative answer to **(a)**. No complete affirmative proof or counterexample to **(b)** was located in the primary sources and searches listed below. That bounded negative search finding is not proof of global absence. Selection remains pending a fresh independent audit by the parent.

The latest official page links the 20 October update-3 main PDF and separate updates. Both freshly downloaded PDF hashes match the reused authenticated cache. Printed page 197 contains the original two-part problem and marks only (a) solved. The official repository likewise labels its linked paper as a solution of (a). Aggregator pages that label the whole number simply “open” were not treated as authority.

## Sources resolving (a), not (b)

**Achyuth Jayadevan, *Nonattainment of the p-Jordan exponent in locally finite triangular groups*.** Official-cited [Zenodo 22751568](https://zenodo.org/records/22751568), 14 September 2026; current [Zenodo 23421603](https://zenodo.org/records/23421603), 16 October 2026. Theorem 1.1 constructs, for every prime p, a countable locally finite upper-triangular subgroup of `GL_2(algebraic_closure(F_p))`, of derived length two, with `E_p(Gamma)=(1,infinity)`. This is a counterexample to attainment, while its optimal exponent is one. Both versions were retrieved; their PDF MD5 values match Zenodo's reported checksums. The official-hosted September PDF is byte-identical to the original Zenodo PDF and was deduplicated. The current version's mathematical theorem scope is unchanged. The presence of a Lean archive is recorded only as metadata; it was not downloaded or built.

**Kinyon–Urban mathematical edition, version 4, 19 September 2026**, [official-hosted PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/09/kourovka-mathematics.pdf). Section 3.45, pages 60–62, gives a countable 2-Jordan nonattainment example with exponent `log(24)/log(8)`. Section 4.3, pages 67–69, expressly limits its claims for (b): exponent two under soluble or uniformly virtually soluble finite-subgroup hypotheses; a normal-Sylow-p variant; an exact exponent `log(60)/log(4)` on the restricted direct sum of copies of A5 for p=2; and specified permanence statements. Its finite-kernel passage retains a generalized p-Jordan hypothesis. The section says that the unrestricted upper bound three remains unresolved. These are source-reported partial results, not claims independently reproved during preparation.

## Primary definition and linear-group trail

**Larsen–Pink**, *Finite subgroups of algebraic groups*, J. Amer. Math. Soc. **24** (2011), 1105–1158, [author-hosted final offprint](https://people.math.ethz.ch/~pink/ftp/LP5.pdf), DOI [10.1090/S0894-0347-2011-00695-4](https://doi.org/10.1090/S0894-0347-2011-00695-4). Theorem 0.4 gives `J'(n)|H_(p)|^3` for finite subgroups of `GL_n(K)` over characteristic p. Here n is fixed and J depends on n. This proves the stated subclass bound; arbitrary p-Jordan groups need not admit one fixed finite-dimensional representation.

**Brauer–Feit**, *An analogue of Jordan's theorem in characteristic p*, Ann. of Math. (2) **84** (1966), 119–131. Bibliography and its role were cross-checked in Larsen–Pink's primary text and in Hu/Chen–Shramov. Larsen–Pink explains that the earlier dependence on the Sylow-p order was exponential; its own theorem provides the cubic bound. Fresh access to the guessed Annals page returned 404, so no direct full-text claim about the 1966 proof is made. Do not attribute the exact cubic exponent to the 1966 argument alone.

**Fei Hu**, *Jordan property for algebraic groups and automorphism groups of projective varieties in arbitrary characteristic*, [arXiv:1804.10946v2](https://arxiv.org/abs/1804.10946v2), 25 September 2018; Indiana Univ. Math. J. **69** (2020), 2493–2504. Definition 1.6 defines p-Jordan; Theorem 1.5 cites the cubic linear result. Theorems 1.7/1.10 establish existence of finite exponents for algebraic groups and projective automorphism groups. Remark 1.8 gives the coarse exponent `3(r_G+1)c_G` for its construction. This does not prove that the optimal exponent exceeds three, nor extend the cubic result to every abstract p-Jordan group. Definition 1.2's generalized p-Jordan condition controls a different collection of finite subgroups.

## Current geometric results and their boundary

**Chen–Shramov**, *Automorphisms of surfaces over fields of positive characteristic*, Geom. Topol. **28** (2024), 2747–2791, [publisher PDF](https://msp.org/gt/2024/28-6/gt-v28-n6-p04-p.pdf); [arXiv:2106.15906v3](https://arxiv.org/abs/2106.15906), 23 August 2024. Definitions 1.2/1.3 separate generalized p-Jordan from p-Jordan; Theorem 1.4 restates the cubic linear theorem. Theorem 1.6 supplies a cubic bound for the Cremona group of rank two over any field of positive characteristic. Statements for birational automorphisms of arbitrary surfaces allow a nilpotent subgroup in the relevant conclusion and must not be substituted into the abelian target.

**Chen–Shramov**, *On p-Jordan constant of Cremona group of rank 2 in odd characteristic*, [arXiv:2509.15522v3](https://arxiv.org/abs/2509.15522), 30 March 2026; Pure Appl. Math. Q. **22**(1) (2026), 45–97, DOI [10.4310/PAMQ.260121024009](https://doi.org/10.4310/PAMQ.260121024009). Theorem 1.9 gives exponent three with explicit constants `7200` for p>=7, `168` for p=5, and `10` for p=3; the bounds are sharp over algebraically closed fields. This is a current strengthening inside the rank-two Cremona class, not the universal abstract-group statement. The paper also warns that checking a bound for a finite overgroup alone does not automatically establish the same constants for all its subgroups. The publisher page returned 403, but the exact journal metadata was authenticated through Crossref and the current full arXiv PDF was retrieved.

## Search coverage and access limits

The primary search used exact problem/subpart numbers, p-Jordan exponent and infimum formulations, universal bound three, counterexamples, soluble classes, and current geometric results. Full texts were inspected at the scope-bearing theorem/definition locations. The latest-version API was followed, rather than assuming the official-cited September Zenodo record remained current. The official repository index was checked for newly linked solutions.

`SEARCH_SCOPE.json` records the query families, primary sites, inspected sources, exclusions, and failed access. Direct MathSciNet and zbMATH databases were not queried. Search-engine coverage of new records can lag; unpublished or unindexed work is outside this bounded audit. No queue, pull-request body, repository status label, or aggregator classification was used as a problem source or a proof.

## Next gate

The source package is ready for the parent's independent audit. If that audit accepts the scope and absence finding, only **21.121(b)** can be considered for new research; part (a) is prior work. No research, originality claim, public status change, publication, release, or outreach is authorized by this preparation receipt itself.
