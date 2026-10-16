# Fresh overall adversarial adjudication: PR563 / Problem 2306072

**Decision: retain the hold on acceptance as an apparently new full original-target resolution and on publication.** The complete new primary texts survive an independent attempt to falsify their source-scoped non-overlap with the candidate. They supply no earlier actual support slit with the two target failures and no identical mixed fourth-coefficient perturbation construction. That bounded result closes substantial previously named gaps; it does not close three specifically relevant unread-source comparisons. No verified earlier full solution has been found that would justify an `already_solved` disposition. The final changed publication package has not been reviewed or accepted here.

This decision preserves the intended goal: an apparently new, independently checkable resolution of both original questions. Publishing the exact theorem with a novelty disclaimer does not meet that goal while material priority gaps remain. Conversely, the hold concerns evidence for novelty and attribution; it is not a newly found mathematical disproof of the candidate.

## Independent scope and inputs

I first read the original problem, frozen original proof and compared manuscript, then wrote `INDEPENDENT_MECHANISM.md`. Before consulting any earlier source-family report, I read the complete article proofs, examples, remarks and references of all seven newly available primary texts: Zemyan 2003, 2005, 2007; Duren-Leung-Schiffer 1983; Zhang-Ma 1991; Brickman 1984; and Goh 1994. This is **60 article pages**, distinct from publisher wrappers. Critical printed equations were visually inspected. `SOURCE_COVERAGE.json` distinguishes full article coverage from key-page visual coverage; it does not claim that every page was independently rendered and viewed.

After that independence checkpoint I read the 06/07/08/09 reports and root notes/replay. They are evidence to reconcile, not substitutes for the seven primary texts. I also read the earlier 04/05 follow-ups and 03 report for the disposition of inherited families. I have not freshly read every older primary paper, nor independently reproved all classical theorems. Duren 1981 pp.352-355 were read directly for the actual support geometry and conventions.

The mathematical manuscript comparison is pinned to the parent's immutable `root_reproduction/PRIMARY_AUDIT_BASELINE.tex`, SHA256 `eaf22e2617d2dbbe240b4adc7661801cff2cfa3751ba834379002789c4e7eb83`, which is the exact text first read as `publication/support_slit.tex`. Source identities and hashes are in `SOURCE_INPUTS.json`. Later canonical attribution edits are outside this review's input. All authored work remains in this review folder; no index, branch, remote, publication or canonical content was changed. The branch was main. No external person or other review agent was contacted. Only the parent received coordination messages.

## Exact original target and falsifiable success criterion

Hayman-Lingham, *Research Problems in Function Theory* (2018), printed p.143 / PDF p.144, Problem 6.72, asks whether the analytic arc omitted by a support point of normalized schlicht S must have monotonic argument, and whether the angle between radius and tangent vectors must be monotonic. Its update records lack of progress reported to the editors. It cannot certify present-day openness.

The candidate fixes exactly

\[
\epsilon=10^{-24},\quad\eta=10^{-12},\qquad
L(f)=a_2(f)+i\epsilon(a_4(f)-3a_3(f)),
\]

and asserts the failures for **every global maximizer of Re L on full S**, on its **actual omitted arc**. It covers continuous polar argument, signed outward radial angle and ordinary unsigned radial angle. It does not claim an explicit maximizing map, uniqueness, a tangent-waver count, or a converse saying arbitrary Schiffer trajectories are extremal.

For outward radius-ordered w, let

\[
\theta=\arg w,\qquad\phi=\arg w',\qquad
\beta=\phi-\theta=\arg(w'/w),\qquad\alpha=|\beta|.
\]

With r=|w|, the exact relation is

\[
w_r/w=1/r+i\theta_r,\qquad\theta_r=\tan\beta/r,
\qquad\phi_r=\theta_r+\beta_r.
\]

A reversal of phi' alone does not give a reversal of theta', beta' or alpha'. A prior actual polar reversal, together with the support limit beta -> 0 at infinity, would defeat novelty of both negative target answers even if its functional differed. Thus functional inequality alone is never the exclusion criterion used below.

The candidate's key formal extraction, checked from -f^2/w-f^3/w^2-f^4/w^3 through degree four, is

\[
\Phi(w)=-a/w-b/w^2-c/w^3,\quad Q=\Phi/w^2,
\]

\[
a=1+i\epsilon(2a_3+a_2^2-6a_2),\quad
b=i\epsilon(3a_2-3),\quad c=i\epsilon.
\]

For w=-v^-2 its natural-coordinate polynomial is P=a-bv^2+cv^4. At the limiting Koebe coefficients,

\[
P=1+i\epsilon(-2-3v^2+v^4)+O(\epsilon\eta),\qquad
tV'/V=1+i\epsilon q(t)+O(\epsilon\eta),
\]

\[
q(t)=t^2-2t^4/5,
\quad q(1)=3/5,\quad q(7/4)=-441/640.
\]

The certified O-term bound is 2000 epsilon eta. These are theta/beta tests: for W=-V^-2 and inward t,

\[
\theta_t=-2\Im(tV'/V)/t,\qquad\beta=\arg(tV'/V).
\]

The sign margins are greater than epsilon/2. Beta -> 0 at infinity plus opposite beta signs precludes either monotone direction; continuity makes alpha zero between two positive endpoint values. Reversing traversal, tangent direction, or using the acute tangent-line convention cannot remove these failures.

## Actual slit membership and boundaries

The candidate starts with compactness of S and nonconstancy of Re L, so its maximizers exist and have classical support geometry before any trajectory is constructed. Its all-maximizer coefficient bounds are uniform, not differentiability assumptions about an optimizing selection. Its area-theorem estimate at z=-2/3 and the correctly directed conformal-radius inequality give the **actual** finite tip bound

\[
r_{tip}<7/25+7\eta<3/10.
\]

The constructed regular segment satisfies |W|>25/81, leaving gap 7/810 above 3/10. The actual slit tail and W share Im G=0 near infinity; oddness identifies the two lifted real rays. Local trajectory uniqueness then propagates coincidence on a relatively open and closed membership set. The radius gap excludes stopping at the actual finite tip. Re(tV'/V)>0 fixes inward traversal and the outward tangent -W'.

This is essential. Q may be nonzero at an actual finite tip, so nonvanishing and formal continuation alone would not establish membership. The candidate has not made that error. From its |A|<3, |B|<4 bounds and every omitted |w|>=1/4, the lower-order numerator terms are at most 32 epsilon times the leading |w|^2 factor, less than 1-3 epsilon. Thus Q has no zero on its actual slit, but that observation supplements rather than replaces the tip gate. The discriminant margin 28 epsilon^2<4 epsilon also gives two distinct formal numerator roots inside the quarter disk.

At epsilon=0 the candidate becomes the Koebe a2 problem, and the strict reversal margin disappears. All estimates and the verdict concern the specified nonzero epsilon. This review found no new circularity, unsupported trajectory converse or boundary-tip continuity assumption in the compared proof. The previously audited uniform analytic remainders and classical support/area/coefficient premises remain its proof inputs; the finite checks here do not formalize them.

## Complete new source comparisons

| Complete primary source | Actual result/mechanism and limiting hypotheses | Adversarial target comparison |
|---|---|---|
| Zemyan 2003, pp.791-796, DOI 10.1080/02781070310001599359 | An actual Brown point-evaluation global extremizer, z0=(2/5)exp(5 pi i/6), with w=-4B k(exp((t-T)/sqrt B)). Tangent angular velocity reverses; source p.792 explicitly retains Brown polar/radial monotonicities. Complete tip determination and example are given. | Its actual omitted arc is a positive counter-control to the false tangent-to-target bridge. It does not settle either target negatively or reproduce the coefficient perturbation. Source approximations are not by themselves directed bounds; 06 supplies reproducible interval checks. |
| Zemyan 2005, pp.1-17, DOI 10.1007/BF03321083 | Bounds hypothetical wiggle counts through spherical curvature and Schwarzian level sets; Koebe and Pearce examples are half-lines. Later level-set questions and Pearce variations remain conditional. | Upper bounds do not prove existence. Curved Pearce level-set arcs lie in the parameter disk, not on the omitted slit. No support construction with either target failure is supplied. |
| Zemyan 2007, pp.175-181, DOI 10.1080/17476930601065169 | Finiteness of wiggles/wavers, eventual endpoint sign stability, and conditional alternating/intervening-waver properties. 2003 is cited only for actual tangent wavers. | A bounded reversal is compatible with finite and eventually stable signs. Arbitrary full-S slit examples mentioned in contrast to support points supply no global support certificate. No target negative construction or candidate mechanism appears. |
| Duren-Leung-Schiffer 1983, pp.263-277, DOI 10.1080/17476938308814018 | Classical geometry, coefficient extraction, rational-type functionals, strict coefficient tip-angle theorem. The second extremizer/differential and equality classifications require magnitude pi/4 **at the finite tip**. | Its Theorem 3 applies directly and ensures the candidate tip is strictly below pi/4. The equality premise is therefore absent. Interior theta/beta failures do not contradict its classifications. No prior target failure appears. |
| Zhang-Ma 1991, pp.598-601, DOI 10.1016/0022-247X(91)90330-3 | Claims rational-type maximum-tip half-line classification without DLS's double-zero restriction; reciprocal continuation and unique-germ argument. | Still requires exactly saturated tip angle, excluded for the candidate. No separate construction or target nonmonotonicity result appears. Printed local gap is limited below. |
| Brickman 1984, pp.372-376, DOI 10.1090/S0002-9939-1984-0759655-5 | Cauchy-integral duality proves rational Phi for one f iff L is a finite derivative-evaluation combination; type preserved by composition/truncation. | Rational L does not imply rational maximizing f. Truncation starts with an actual support slit, and preserves the nonzero fourth coefficient here. No arbitrary-trajectory converse or negative target example. |
| Goh 1994, pp.463-468, DOI 10.1090/S0002-9939-1994-1197537-4 | Pole-order rigidity **assuming rational f**; separate theorem assuming two independently maximized derivative evaluations at distinct nonzero points. Complete paired-equation continuation proof. | The candidate maximizes one sum. Its summands need not be separately maximized; rationality of Phi cannot supply rational f. No target reversal or identical coefficient perturbation is supplied. Its 1992 thesis reference is distinct from the missing 1992 journal article. |

For the Zemyan 2003 formula, direct differentiation gives

\[
w'/w=q_B(1+s)/(1-s),\qquad
w''/w'=q_B(1+4s+s^2)/(1-s^2),
\]

where q_B=1/sqrt B and s=exp((t-T)q_B). These distinct expressions explain how tangent wavering can coexist with the two source-stated monotonicities. Nothing in this argument assumes the formula describes an arbitrary newly chosen support arc: its actual realization is Brown's extremal family.

For any half-line w/b=x+t+iy with increasing modulus and x>0,

\[
\theta_t=-y/((x+t)^2+y^2),\quad
\beta_t=y/((x+t)^2+y^2),\quad
\alpha_t=-|y|/((x+t)^2+y^2).
\]

Thus all explicitly identified Koebe/Pearce/rational-f half-line examples are monotone in the target quantities. The equality |y|=x at the tip preserves those conclusions; y=0 makes both angles constant.

Rational-type does give a useful consistency deduction, conditional on Goh's rational-f rigidity. Here Phi has its only finite pole at 0, of order three. Goh 1994 Remark (iii)(a), retaining rational f, would force any rational candidate maximizer to be a Koebe rotation k_u=z/(1-u z)^2. Then |u-1|<4 eta, and its radial slit w=-r/u would require

\[
\Phi(-r/u)=a u/r-bu^2/r^2+cu^3/r^3
\]

to be real for all r>=1/4. In particular Im(cu^3)=epsilon Re(u^3) must vanish. But Re(u^3)>1-12 eta>0. Hence the candidate maximizers cannot be rational under these established inputs. This deduction rebuts the inappropriate rational-L-to-straight-slit inference; it is not asserted as a novel historical contribution.

## Narrow printed-proof qualifications

The source-scoped verdict does not depend on discrediting any published theorem. Three qualifications independently agree with 07/08:

1. In Zhang-Ma p.600, case (9) with u=omega+c(z-z1)^alpha, P(omega) nonzero, allows alpha=1 from the first equation. If P(omega)=P(u0) and P-P(u0) has a double zero at omega, the second equation has order 2 rather than the order zero tacitly used in the printed contradiction. The explicit polynomial witness in `exact_checks.py` has P(0)=0 simple, P(1)=P(2)=i, P'(2)=-2-i/2, P'(1)=0 and P''(1)=2. This verifies an omitted **local elimination case**, not a global support functional, a counterexample to the theorem, or a priority result. Additional global information could repair the proof. The candidate does not invoke this classification.
2. Zemyan 2007 pp.178-179 sets g(tau)=tau w(tau) and uses g''/g' for the tangent derivative. The correct quotient is

   \[
   w''/w'=\tau g''/(\tau g'-g)-2/\tau.
   \]

   Since g(0) is nonzero, its corrected imaginary part is analytic near zero, giving the same eventual first-nonzero-coefficient sign mechanism. The rational diagnostic w=1/tau+i+tau has real w''/w' but nonreal g''/g'; it is solely an auxiliary formula test, with no support membership claim. No global finiteness theorem is refuted. Distinct accumulation points and a regular geometric rather than potentially singular natural tip parameter must also be understood in the source proof; the candidate's witness is regular and separated from its actual tip.
3. Zemyan 2005 Remark 3.1(e)-(f), pp.8-9, asserts a waver after the last wiggle and #G<=#V, while the published 2007 theorem states only intervening wavers and #G<=#V+1. The stronger assertion lacks a derivation in the inspected cited publication. An auxiliary geometric arc would not refute a theorem about actual support points. This is a support-specific proof obligation for that stronger source statement, not evidence of a prior target example. The candidate uses none of these count bounds.

## Inherited families, chronology and attribution

The earlier complete 04 and 05 comparisons are retained with their precise limits. Hibschweiler 1996 proves actual two-evaluation/non-Koebe/conjugate existence and conditional rational cases, but its full source contains no checked theta/beta reversal. Non-Koebe status and opposite conjugate arcs do not establish reversal on one slit. Friedland-Schiffer 1977 gives substantial classical global coefficient-extremal machinery and an explicit degree-four family maximized by Koebe. Its general boundary/control reductions are not solved target instances; a coefficient-body boundary or constrained extremizer must not silently be promoted to full-S support. This review read the follow-up reports, not all of those primary pages afresh.

The candidate's coefficient extraction, Schiffer coordinates, compactness, support geometry and extremal perturbation framework are substantially classical. Absence of an identical q polynomial in the fresh corpus is not a claim that those tools are new. The concrete extra assertion is controlled sign reversal on the actual slit of every maximizer of a specified functional, with quantitative membership and errors.

Journal issue dates have priority relevance: Zemyan 2003 precedes its wrapper's 2010 online date; DLS 1983 precedes its wrapper's 2007 posting; Zemyan 2005 cites a submitted paper later published in 2007. None of these is a chronology contradiction or an excuse to treat the source as later than the candidate. The chapter conventionally labeled Duren 2014 has primary online date 28 August 2013 and print year 2014. The Crossref 14 records represent 13 bibliography entries because the Russian/English Bakhtin item is split. These metadata establish identity and a later reference trail, not the chapter's theorem scope.

The compared baseline attribution is now stale where it says the five supplied papers' complete comparisons are missing. A final manuscript should replace that with the exact complete-source findings and credit DLS, Brickman and Goh alongside Zemyan and the already credited classical families. It should retain the actual material missing sources and avoid historical-first or 2026-openness assertions. The parent's planned rewrite does not receive package acceptance from this source audit.

## Every remaining material gap and concrete next evidence

| Item | Positive reason it remains relevant; exact unknown | Disposition and decisive next step |
|---|---|---|
| Duren 2013-online/2014-print commentary, DOI 10.1007/978-1-4614-7949-9_22, pp.499-516 | A later primary retrospective tied to the original problem's author, with deposited references to rational/two-functional coefficient work beyond the 1983 article. None of its commentary prose was obtained. Earlier title, keywords and bibliography do not exclude a later geometric example or historical attribution. | **Material blocker to apparent-new-resolution/publication acceptance.** Obtain the lawful complete chapter, including commentary, and compare retrospective claims, actual support constructions and theta/beta quantities. Full old DLS text cannot substitute for it. Ordinary publisher/Google Books access denials are recorded; no repeated bypass or outreach is appropriate. |
| Goh 1992 **journal article**, DOI 10.1080/17476939208814600, pp.197-206 | Its primary abstract is specifically about coefficient functionals; the later primary commentary cites it. The final two-functional conclusion alone has an absent premise here, but the intermediate coefficient geometry/examples and remarks are uninspected. Goh 1994's thesis reference is a different work. | **Material blocker.** Read all ten pages and identify whether any single-functional support construction or coefficient perturbation already gives the target reversal. The parent has already requested a human-provided fulltext path; lack of response is not permission or evidence of non-overlap. |
| Hibschweiler 1995, *Geometric properties of some support points of univalent functions*, HJM 21(1), pp.95-102 | Direct primary indexed excerpt around p.101 treats precisely eventual polar and radial-angle monotonicity; Zemyan 2007 p.177 explicitly attributes eventual polar stability to it. Those known tail results permit the candidate's bounded reversal, but full examples, terminal-support arguments and remaining sections have not been reliably read. | **Material close-source scope gap, lower collision evidence than the first two, still unclosed.** Obtain complete eight pages or an equivalently complete reliable primary rendering. Determine whether its actual terminal constructions do more than the known tail/evaluation statements. A later statement that the polar question was open reduces concern but cannot replace full coverage. |
| Changed manuscript/PDF/verification archive | The candidate PDF/ZIP belongs to the prior technical draft freeze. The new complete-source findings require an attribution and source-receipt update. | **Separate final-acceptance gap.** After integration, freeze exact updated inputs, rerun the portable archive, inspect the rebuilt PDF and manifest, and obtain fresh adversarial review of the complete changed package. No final package review was performed here. |

This is a bounded list, not a demand to read every background reference. Haario 1978 remains an uninspected coefficient-body source (49 pages), identified through the inspected Haario 1983 route including V3. It is not cleared or declared harmless, but current evidence supplies no specific full-S target reversal or solved candidate-degree-four instance. It is an unresolved background lead rather than an additional independent blocker. A concrete actual-support construction, all-S degree-four theorem or target-angle statement would raise its materiality immediately. The newer Haario source's restricted real bounded-rotation example is not such evidence.

Goh 1998, Bakhtin 1981/1986 and the Goh/Brown theses similarly remain disclosed subsidiary trails. Goh's advertised nonzero derivative evaluations have different origin-pole structure from this functional; that excludes identity of the advertised class, not every possible shared support point or unseen remark. Neither metadata nor missing text is a universal exclusion. Without a specific target construction or critical implication, their existence as bibliography entries alone does not independently require publication to remain held. This distinction is based on the concrete main-hypothesis mismatch and strength of the lead, not a harmlessness assumption from a title.

No negative verdict on novelty can be promoted merely from these access gaps, and no positive novelty verdict can be promoted from search absence. If the material texts provide only the absent-premise/tail mechanisms, complete receipts can close those comparisons. If they identify an earlier actual polar reversal, publication must credit and reposition the result; a different exact functional would not rescue a claim of a new resolution of the original questions.

## Reproducibility and final strength of evidence

`exact_checks.py` uses only standard-library exact rational Gaussian arithmetic; all **42 checks pass**. It reproduces sign/error/tip margins, coefficient extraction in exact diagnostic instances, the corrected 2007 quotient identity, the 1991 omitted local-order witness, half-line angle identities and persistence of the fourth coefficient under origin composition. Generic algebra and the actual-slit argument are stated above. These are finite, reproducible supports for the derivations, not proof-assistant certification, a source theorem refutation or a novelty oracle.

`seal.py` seals every present authored output except the manifest itself and ignored `.cache/`; raw PDFs, OCR and images are excluded. `SOURCE_INPUTS.json` hashes the external evidence without republishing it. Run `python3 exact_checks.py`, then `python3 seal.py --verify`; optional `--sources` also checks external input hashes in this local workspace. Source/canonical files are never rewritten by these tools.

Strongest verified result: independent complete-text exclusion of an earlier full target resolution or identical construction within the seven newly available primary articles, together with a preserved actual-support proof mechanism for the candidate under its stated classical inputs. Exact remaining gap: the three named material source comparisons and the changed complete-package acceptance. This closes the bounded review assignment, not the requested discovery/publication goal. No `first`, `already solved`, `novel resolution accepted`, `still open in 2026`, or final package clearance is certified.
