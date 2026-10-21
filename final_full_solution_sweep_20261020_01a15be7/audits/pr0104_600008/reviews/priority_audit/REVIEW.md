# Independent priority review of PR104 / 600008

Review completed: 2026-10-21 UTC. Scope: the frozen analytic criterion at PR head `4d8ba8e9438c9c8a463721adc1102dee821b11df`, theorem SHA256 `608217a2ffc120a965b165f5b6065edd83f8cf94c5e77f0f95a0326640db2dae`.

**Verdict: no clearance to publish this as a new resolution of an open problem.** The analytic closure theorem is recoverable as a direct consequence of prior separated equations, a classical complete third-kind integral identity, and elementary geometric counting. This is a priority decision, not a finding that the claimed analytic theorem is false.

This review was performed without reading the historical PR104 audit verdicts. An initial assessment was saved before the reconstruction; source hashes, exact checks, and the full derivation are retained here. The parent supplied a completed live spreadsheet duplicate check before this work began. No external communications or record mutations occurred.

## Exact target and scope

[GKT (2007), Problem 5.2](https://arxiv.org/pdf/0705.0188v1), printed p.18, asks for parameters of the folded equator map with prescribed iteration count and actual winding. [Tabachnikov (2015), Section 7](https://amj.math.stonybrook.edu/pdf-Springer-final/014-0001-3.pdf), printed p.62, asks the corresponding question for tropic-to-tropic chains. The literal request is for conditions in the axes; classical Cayley theory is its motivation. An analytic necessary-and-sufficient condition is responsive to that literal request, so absence of a polynomial determinant is not itself a reason to reject the candidate as incomplete. The original sources establish that this question was posed as open in 2007 and 2015. They do not certify that it remained open in September 2026.

The frozen theorem treats both conventions, all positive real parameters, the rotational case, actual unreduced winding, iterates and least periods. I found no extra original-problem hypothesis silently removed by this formulation. This priority audit does not replace the separate full mathematical audit.

## Antecedent reconstructed rather than assumed

The relevant prior source is [Dragović–Radnović (2019)](https://arxiv.org/pdf/1909.08154v1). Its Eq. 3.2 and coordinate ranges lead to the same positive periods after specialization. Its general assertion that it solves the question is insufficient evidence by itself: fixed billiard reflection counts cannot simply be carried into a grazing surface limit. In `DERIVATION.md` I independently verify the surviving differential by differentiating confocal coordinates directly. This supplies the surface equation without assuming convergence of any sequence of periodic billiards. The finite algebraic conditions elsewhere in that paper are not being endorsed by this review. The publisher records a [2020 proceedings version](https://link.springer.com/chapter/10.1007/978-3-030-57000-2_8); only its metadata was checked, with the 2019 author preprint supplying the equations.

The reconstruction yields horizontal circumference $4I_u$, positive advance $2I_v$ for either a full tropic arc or a folded equator excursion, and therefore

\[
 \rho=I_v/(2I_u),\qquad nI_v=2rI_u.
\]

The factor two is independently fixed by coordinate unfolding and agrees with two $Y=0$ plane crossings per physical turn. Full arcs additionally require even $n$, because successive endpoints occupy opposite tropics. The folded equator map allows odd periods. The elementary example $a=b=1,c=8$ has folded lift 1 and period 1, while one physical full arc ends on the opposite boundary and is not closed. Thus this audit does not conflate odd equator periods with physical closure.

The candidate's complementary-period identity is exactly a specialization of [DLMF 19.7.8](https://dlmf.nist.gov/19.7.E8). With

\[
 n_0=(a-b)/a,\quad m_0=c/(b+c),\quad k^2=n_0m_0,\quad C=2b/\sqrt{a(b+c)},
\]

the explicit substitutions give $I_u=C\Pi(n_0,k)$, $I_v=C[\Pi(m_0,k)-K(k)]$. The complete connection formula gives $I_u+I_v=\pi$. Therefore $I_u=\pi\mathcal M$ yields exactly the frozen formula $\rho=(1-\mathcal M)/(2\mathcal M)$, with the same winding equation. The axisymmetric evaluation, monotonicity, uniqueness and parameter bounds are elementary consequences of this positive integral. These refinements do not establish a distinct new closure mechanism.

## Reproducibility and falsification checks

`independent_priority_checks.py` verifies 17 exact symbolic/integer checks: the surface identity, the induced diagonal metric and zero cross term, equality with the prior limiting differential, both rational substitutions and all their endpoints, the positive complete-identity factor, rotation conversion, the rotational formula and least physical periods on all reduced positive rational samples with numerator and denominator at most 19. Eight independently parametrized, 70-digit numerical quadratures test unequal axes, nearly equal axes, large aspect ratio and small/large $c$. All checks pass. Quadrature is diagnostic evidence; the written substitutions and positive branches supply the identity proof.

The script uses `sympy==1.14.0` and `mpmath==1.3.0`, read from the parent's isolated verification environment. Its receipt records versions and its exact SHA256. No global dependencies were changed.

## Further priority search and current publication overlap

[Wüstholz's 2017 primary slides](https://viasm.edu.vn/Cms_Data/Contents/viasm/Media/file/billards_halong2017.pdf), final five slides, explicitly discuss this null-chain problem and announce a number-field arithmetic characterization. That narrower arithmetic announcement is not substituted for a proof of the unrestricted-real-parameter analytic criterion. The [2021 publisher record](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/198/4/114162/elliptic-and-abelian-period-spaces) verifies related period theory, but a referenced complete billiard manuscript was not recovered. Dataset and repository-generated summaries were treated as search leads, never as independent priority authority.

A fresh search found Alper Ferudun's [14 October 2026 preprint](https://eulersolve.org/papers/amr-005-0008/). Its Theorem 1 states the same analytic criterion, even-leg convention and least-period distinction, followed by additional arithmetic claims. The downloaded PDF SHA256 matches the site's machine-readable metadata. The author advertises DOI `10.5281/zenodo.23371160`; my public Zenodo/DOI requests returned 403 or were unavailable, retained in `sources/EXTERNAL_OVERLAP_MANIFEST.json`. Subsequently the parent retrieved the public Zenodo API record successfully. I inspected that separate receipt: record 23371160 is submitted:true/state:done, dated 2026-10-14, author Ferudun, Alper, with the matching title, version 1.0, PDF, source ZIP and README. The receipt SHA256 is `0ec86359519b4da022be8d71c5e7a5334b833676d625ddcd9bb665ca9cd735a9`. This establishes an external-author publication; my failed requests are not represented as successful. The parent subsequently checked the DOI with HTTP 200 at 2026-10-21T01:25:40.228811+00:00, resolving to https://zenodo.org/records/23371160; that distinct receipt is ../../EXTERNAL_OVERLAP_DOI_CHECK.json. This subagent inspected the saved receipt; it did not repeat that successful request. PR104 was created 30 September 2026, so this later work cannot by itself establish antecedent priority against this PR. It does establish a current exact publication overlap requiring reconciliation before any future publication. I did not audit its additional arithmetic claims, infer its independence or suggest an authorship relationship.

## Exact remaining gap and disposition

The present record does not identify a substantive new mathematical theorem beyond the reconstructed antecedent analytic closure result. It also does not establish who first printed this exact simplified formula with all conventions. Absence of such a first-print match is not enough to claim a novel resolution. A finite algebraic Cayley condition is a different, stronger interpretation, and this audit neither supplies nor validates one.

Preserve the candidate as a credited, independently checkable derivation. Leave the already closed, unmerged PR unchanged and record the reason for no new publication as **priority/originality gate not met**, rather than mathematical invalidity. Do not convert the later external author's advertised DOI into a publication owned by this repository. No new DOI, paper package, spreadsheet row or PR action is justified by this review.

Audit completion estimate: 100% of this assigned priority review, subject to the explicitly recorded bibliographic access limits. Novel-publication clearance: false. No historical audit verdict was read.
