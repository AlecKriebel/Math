# Independent initial hypothesis

Recorded: 2026-10-12 06:40:57 UTC. Review completion estimate: 25%.

This was written before reading ROOT_MATHEMATICAL_REVIEW.md, any prior audit, frozen author proof, or peer report. It uses only the original public report and the public Quellmalz 2020 article; the parent supplied a tentative classification, which remains a hypothesis here.

## Exact target reconstructed from the original

Stephens' abstract in Oberwolfach Report 31/2008, printed pp. 1762-1764, defines normalized equatorial averaging on continuous functions, its dual R on spherical measures, and the geodesic Wasserstein-p metric on all probability measures. Its final question asks for a uniform reverse contraction bound. The displayed contraction formula has the usual ambient dimension n >= 3 regime; p is in [1,infinity). The source does not impose antipodal symmetry, projective identification, support, smoothness, or positive lower density assumptions.

The substantive target is therefore the existence of a finite inverse constant K(p,n), equivalently a positive lower contraction constant c(p,n), such that

    W_p(mu,nu) <= K(p,n) W_p(R mu,R nu)

for every pair of probability measures on S^(n-1). If the phrase allows zero as the lower constant, its only uniform lower constant can be zero, which is not an inverse stability estimate.

Primary source: https://ems.press/content/serial-article-files/46174, printed p. 1763. The target reconstruction is an interpretation of the final question in its explicitly declared domain, not a claim that the source itself prints the displayed reverse inequality.

## Tentative disposition

Hypothesis: the literal all-probability target is already resolved negatively by an elementary classical consequence of the definition, so it should not qualify as a new solution of a surviving difficult problem. This is distinct from claiming a previously printed Wasserstein formulation has been located.

Let A(u)=-u. Since E(u)=E(-u), normalized equatorial averaging R0 satisfies R0 f(u)=R0 f(-u) for every continuous f. Duality then gives

    <f,R delta_u> = R0 f(u) = R0 f(-u) = <f,R delta_(-u)>.

Thus R delta_u=R delta_(-u), while their input geodesic W_p distance is pi for every finite p>=1. No inverse constant can exist. This argument uses output parity of R0 and the dual definition directly; it does not improperly assume that the function kernel equals the dual kernel.

Even requiring strictly positive smooth probability densities would not repair the literal domain. With normalized spherical area sigma and 0<epsilon<1, use densities 1+epsilon (u dot x) and 1-epsilon (u dot x). They have unit mass, are strictly positive and distinct. Their difference annihilates every even function R0 f by antipodal change of variables, hence their R images agree. Wasserstein distance is positive because it is a metric. Self-adjointness is unnecessary.

## Classical correspondence and remaining challenges

Quellmalz 2020, Section 2.2.2 equation (2.5), uses the same equator mean normalization on S^(d-1), d>=3. Its Section 4 describes the ordinary Funk nullspace as odd functions and reduces its generalized symmetry to antipodal oddness when z=0. The publisher records publication on 11 August 2020, before the proposed 2026 contribution. This is positive earlier evidence of the underlying obstruction, even though the source question was posed in 2008.

Public primary comparator: https://link.springer.com/article/10.1007/s13324-020-00383-2.

Potential falsifiers still to examine: an omitted source-domain qualification; an author proof addressing an even/projective target that might supersede the literal question; a classification convention requiring an explicit previously printed negative W_p statement rather than a routine consequence; or a metric convention that identifies antipodes. A strengthened theorem on even densities could remain meaningful and possibly new, but neither novelty nor its correctness has yet been assessed here.

## Scope and publication hygiene

Only authored reports and sanitized public-source receipts in this dedicated review directory are eligible review outputs. No foreign copied artifacts, private fixtures, source status changes, queue changes, repository index/branch edits, cloud writes, remote writes, or communication with individuals were performed.
