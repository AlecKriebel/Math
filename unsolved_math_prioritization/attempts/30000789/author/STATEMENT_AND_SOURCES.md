# Target and evidence boundaries

## Recovered primary question

Wilking's contribution, jointly with Böhm, in *Differentialgeometrie im Grossen*, Oberwolfach Report 32/2007, pp. 1878–1879, considers closed convex cones

\[
C_c=\{R:\operatorname{scal}(R)\ge0,\ \|R_W\|^2\le c\|R_I\|^2\},\qquad c>0,
\]

and invariance under \(R'=R^2+R^\#\). It announces a sufficiently-large-dimensional classification: the even case has the unique value \(c=n/(n-2)\), and the other parity has an interval around that value. The proposed least threshold is 12; a lower bound of 12 is stated. The report describes the work as in progress.

The printed 2007 text repeats “even” in part (b) and uses equality between a scalar and an interval. These are genuine printed defects, visually checked on page 1878, not merely extraction errors. Reading part (b) as the odd case with interval membership is an inferred repair, corroborated by Böhm's later 2008 report. It is not an author-approved erratum.

The 2008 report uses a strict cone and states PDE sufficiency, with necessity separately conjectural. It must not be silently substituted for the closed-cone ODE equivalence in the target.

The live aggregator page https://www.unsolvedmath.com/problems/30000789 could not be opened by the web tool. Identity and current record wording were checked against the supplied full record and the primary report; the live page was not freshly read. The supplied record's misleading parenthetical “2008” does not change the primary report's verified 2007 date.

## Literature check, 2026-10-06

- **Primary target:** B. Wilking, joint with C. Böhm, contribution in OWR 32/2007, pp. 1878–1879. https://doi.org/10.4171/OWR/2007/32 ; official repository https://publications.mfo.de/handle/mfo/3018 . Target pages extracted and page 1878 visually inspected.
- **Later restatement:** C. Böhm, joint with B. Wilking, *Ricci flow in higher dimensions*, in *Geometrie*, OWR 34/2008, pp. 1941–1942. https://ems.press/content/serial-article-files/46179 . Relevant contribution read. It corroborates the parity interpretation, not a sharp-threshold proof.
- **Thesis:** S. F. Beitz, *Bianchi-convexity and applications to Ricci flow*, Münster, 2018, §6.3.2, Remark 6.3.15 and Lemma 6.3.16. https://noah.nrw/ulbmshsnoah/content/titleinfo/4277665 . This records an unpublished broader Böhm–Wilking conjecture and a near-round partial result.
- **Recent published work:** Y. Xu, *On some new Ricci flow invariant curvature conditions*, J. Geom. Anal. 35, 321 (2025), published 20 August 2025. https://doi.org/10.1007/s12220-025-02158-2 . Publisher metadata and abstract inspected. Detailed arguments inspected in the accessible author preprint https://arxiv.org/abs/2412.13633v1 (18 December 2024), especially Conjecture 1, Theorem 1.1, Lemma 2.6, Proposition 2.7, and identities (2.26), (2.40), (2.41). The subscription version-of-record body was not inspected, so exact version equivalence is not asserted.

Xu's family has a parameter, denoted \(\alpha\) here to avoid collision with our scalar coefficient:

\[
\alpha\|E\|^2+\frac{n-2+4\alpha}{4}\|W\|^2
\le\frac{n-4\alpha}{4}\|R_I\|^2,\qquad\operatorname{scal}>0.
\]

The target central cone is the endpoint \(\alpha=0\). Xu proves preservation near \(\alpha=n/4\), with \(\alpha\ge n/4-1/n\) for \(n\ge11\); at \(n=12\), this means \(\alpha\ge35/12\). This does not reach zero. The preprint labels the broader \(n\ge12\) assertion conjectural. No inspected source proves the requested sharp threshold. This bounded search does not prove global literature openness.

## Actual prior-work check

Exact problem-ID and OWR-ID searches over AlecKriebel/Math pull requests returned no matching attempt. Exact-ID code and commit searches returned no matches. A broader Weyl/cone PR search returned no match. The freshly read repository queue row remains `queued`, `0/5` at rank 815. The supplied full report map has no report for this problem number, so its review value is `{}`. These observations are not evidence of actual prior mathematical work and were not used to skip research. Search completeness across all unpublished branches or private work is not claimed.

## Scope distinctions

The mathematics below concerns algebraic curvature operators at one point and the finite-dimensional ODE. There are no compactness assumptions on this algebraic vector space. The standard tensor maximum principle transfers a closed convex O(n)-invariant ODE cone to a smooth Ricci flow on a closed manifold for its existing time interval, with the conventional factor-two time rescaling. No converse PDE implication, noncompact PDE theorem, singularity theorem, or metric construction is asserted.

Nonnegative scalar curvature and a Weyl norm bound are not the same as nonnegative sectional curvature, nonnegative curvature operator, or nonnegative/positive isotropic curvature. The traceless-Ricci component is unrestricted. Our closure includes the entire scalar-zero conformally-flat traceless-Ricci subspace, not just the zero operator. Strict positivity formulations in related papers require separate care.
