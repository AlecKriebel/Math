# Independent priority and source audit: OWR-16407-007

Audit date: 2026-09-23 UTC. Scope: the all-orders identity supplied by the user, not a claim of uniqueness of every nonperturbative solution of the model.

**Verdict: the proposed identity is established prior work of Erik Panzer and Raimar Wulkenhaar. A new-resolution priority claim fails.** The submitted argument reproduces their resummation and omits their separate verification that the resummation solves the defining equation.

## Historical source and exact claim

The [EMS source report](https://ems.press/journals/owr/articles/16407) is *Non-commutative Geometry, Index Theory and Mathematical Physics*, Oberwolfach Report 32/2018, DOI [10.4171/OWR/2018/32](https://doi.org/10.4171/OWR/2018/32), for the meeting of 8–14 July 2018. Wulkenhaar's contribution, joint with Panzer, occupies printed pp. 1938–1941.

In the [report PDF](https://ems.press/content/serial-article-files/46757), printed p. 1939, equation (7) defines the coupled angle/integral problem; equation (8) is conjectured after checks through order ten; equation (9) is exactly the derivative expansion supplied by the user. Printed p. 1940, equation (10), already gives its Lambert-W resummation. Thus proving the resummation alone was not the historical missing step.

The UnsolvedMath URL could not be retrieved: the web tool reported inaccessible and a direct HTTPS request returned HTTP 429. The coordinating reviewer subsequently retrieved the page through the browser and reported a literature review dated 2026-08-21 that calls the all-orders identity conjectural. This subreviewer did not independently retrieve that text. The original EMS text establishes the mathematical match directly.

## Version history and what changed

The [arXiv record](https://arxiv.org/abs/1807.02945) dates v1 to **9 July 2018, 05:12:06 UTC**, and v2 to **4 November 2018, 11:59:01 UTC**. Its revision comment is: “v2: main conjecture in v1 is now a theorem”.

[Version 1](https://arxiv.org/html/1807.02945v1) has the submitted series as equation (31), implicit K equation (35), Lambert formula (36), logarithmic L formula (38), and resummed I formula (39). Its equation (54) identifies the remaining task: establish equality between the integral-defined I and that closed form. Section 9.1 still discusses a conjecture extrapolated from the computed orders. The candidate's quotation of (31) as an exact defining equation reverses this logic. Formal inversion proves equivalence of the proposed series and proposed closed form; it does not establish their identification with the original I.

## Where the missing proof already appears

[Version 2, section 5.2](https://arxiv.org/html/1807.02945v2#S5.SS2) supplies the verification. Equation (21) is the coupled definition, on the chosen solution with homogeneous freedom h(a)=0:

\[
\tau_b(a)=\arctan_{[0,\pi]}\frac{\lambda\pi}{1+a+b-\lambda\log a+I_\lambda(a)},\qquad
I_\lambda(a)=\frac1\pi\int_0^\infty\left(\tau_a(p)-\frac{\lambda\pi}{1+p}\right)dp.
\]

The target series is (26); K and L are (29)–(33). Lemma 10 proves two integral evaluations, (36a) and (36b), by contour integration and resummation. Proposition 11 then verifies the pair (21) for I=K−λL. Its proof substitutes p=u+λlog(1+u), uses the two lemma identities, and controls the cutoff remainder. Equation (38) is precisely the required integral equality. Theorem 1 establishes the resulting two-point solution; subsequent analytic continuation covers a domain containing (−1/log 4,∞). The paper explicitly allows the possibility of other nonanalytic solutions; no unrestricted uniqueness claim follows.

## Why the old and revised definitions describe the same target

The original definition has an exponential Hilbert-transform factor. The bridge is an identity, not a notational assumption: v2 Proposition 4, equation (17c), gives at a common finite cutoff

\[
\int_0^{\Lambda^2}e^{-\mathcal H_p^\Lambda[\tau]}\sin\tau(p)\,dp
=\int_0^{\Lambda^2}\tau(p)\,dp.
\]

Applying it to v1 equation (25), subtracting the same counterterm before taking the common cutoff limit, yields the revised definition. Neither unrenormalized integral should be treated separately as convergent. The authors' v2 footnote 6 expressly records their earlier use of the harder exponential integral.

For the formal question, uniqueness also prevents a loophole. Write the revised definition as I=T(I), using the angle branch with zero constant term. If I−J has first nonzero coefficient at order m, the corresponding angle difference starts at order m+1: its derivative with respect to I(p) is

\[
-\frac{\lambda\pi}{(1+a+p-\lambda\log p+I(p))^2+(\lambda\pi)^2}=O(\lambda).
\]

Coefficientwise integration preserves that order within the admissible perturbative class, so T(I)−T(J) cannot start at order m. This contradicts both fixed-point equations. Thus the normalized formal solution is unique. Version 2 section 8.1 separately records formal uniqueness and analytic uniqueness for the original two-point equation.

Consequently, the literature note reported from the current listing accurately describes the July 2018 conjectural stage but misses the November 2018 proof. Retaining the heading “Conjecture 6” in the revised paper's discovery narrative does not negate the later Proposition 11. A possible preference for a purely combinatorial induction proof is not an unresolved truth claim about the displayed coefficient identity.

## Publication and follow-up check

The [publisher record](https://link.springer.com/article/10.1007/s00220-019-03592-4) confirms publication on **30 October 2019**, in *Communications in Mathematical Physics* **374**, 1935–1961 (2020), DOI **10.1007/s00220-019-03592-4**. Its abstract states that an exact solution is proved. The accessible arXiv v2 supplies the full proof; the publisher page available in this audit is a subscription preview.

Later related work includes Grosse, Hock and Wulkenhaar, [*Solution of all quartic matrix models*](https://arxiv.org/abs/1906.04600), initially submitted 11 June 2019, which treats a broader class. This is contextual corroboration, not needed for the decisive priority finding. Targeted searches combining the earlier identifier/title with “erratum”, “corrigendum”, “error”, “correction”, and “conjecture” did not reveal a correction retracting this identity. That negative search result is not an exhaustive certificate.

## Consequence for the proposed publication

The strongest defensible output is an attributed verification or audit of an already proved result. The supplied candidate is not a self-contained proof from the defining problem, and the theorem it aims to establish predates this project. A paper, website, or DOI package must not represent it as a new resolution or assign the theorem's priority to the current researcher. This verdict does not preclude useful new expository proofs or reproducibility artifacts, but none is evidence of a new theorem by itself.
