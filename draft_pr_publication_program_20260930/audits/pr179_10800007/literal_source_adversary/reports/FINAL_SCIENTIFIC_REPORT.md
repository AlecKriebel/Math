Final report timestamp (UTC): 2026-10-13T04:49:01.382299+00:00

# Final scientific report: printed-scope adversarial audit

Target: PR 179 / attempt 10800007; supplied authenticated head 090b45356f5d6829f755fbc7c5b1fde5565de695. This report concerns source interpretation and the exact local-section theorem, not a complete historical-priority determination.

## Verdict

The candidate's main theorem is valid for the target actually printed: no open neighborhood of the zero coefficient system admits a continuous exact real-root choice. Hence no admissible open cover of all R^6 exists, even with infinitely many members. I independently obtained this conclusion from the primary source before reading the candidate and then checked the candidate's elementary loop proof. I found no mathematical gap or scope mismatch in its central theorem.

This is a substantive, checkable mathematical answer to the literal formulation, and it also exposes a defect in the source's finite-genus framing. Those descriptions are compatible. It does not demonstrate a new mathematical mechanism or resolve an unprinted intended variant. A campaign label such as solved must therefore retain the qualifier literal all-parameter exact-root formulation. Whether an elementary diagnosis of a formulation defect meets a broader publication program's novelty criterion is a separate decision, not a consequence of the theorem. Historical priority has not been cleared by this audit.

The precise answer is that the class of admissible open covers is empty. Infinity is a legitimate shorthand only after explicitly adjoining that value when the defining minimization has no admissible object. The candidate makes this qualification and does not mistakenly claim that an infinite cover exists.

## Source authority, reconstruction, and independence

The primary final article is V. A. Vassiliev, A Few Problems on Monodromy and Discriminants, Arnold Math. J. 1 (2015), 201-209, DOI 10.1007/s40598-015-0011-9, final [PDF](https://armj.math.stonybrook.edu/pdf-Springer-final/015-0011-9.pdf), [journal HTML](https://armj.math.stonybrook.edu/html-articles/Files-2015-2024/15-11/), and [publisher page](https://link.springer.com/article/10.1007/s40598-015-0011-9). The [preprint](https://arxiv.org/abs/1504.01997) is arXiv:1504.01997v1.

I read the whole final PDF through its complete 9-page extraction and the whole 10-page preprint. Final printed p.205 and preprint p.5 were rendered locally and visually inspected in full. Section 2 ends on final p.205; the preprint's final generalization continues onto p.6 and was text-read. Full journal HTML and current publisher Section 2 were also checked. Full-article restrictions in other sections do not qualify Problem 2A.

The six parameters are independent real coefficients in affine a and b. The root coordinates are real; the cover uses ordinary open subsets of the full coefficient space. The selection must be continuous and return an exact root at every parameter in its domain. No discriminant deletion, regular-value restriction, homotopy relaxation, stratification restriction, or approximate tolerance appears in this target. The adjacent Problem 2B explicitly introduces a positive root-distance tolerance. My proof below concerns Problem 2A alone.

Source-first assessment reports/FIRST_ASSESSMENT.md was sealed at 2026-10-13T04:44:04.590724+00:00, mode 0444, SHA256 72c3a7583a8943689d86c99433fa48a2218d073e9207a4937d7506324d0e3a73. At seal I had not read NO_COVER.md, upstream_report.json, original verdicts, Root assessments, or sibling work. Afterwards I read only the authenticated candidate NO_COVER.md among those categories. The other categories remain unread. I did not substitute the candidate's conclusions for source facts.

## Independent proof and exact assumptions

Write a=a_1x+a_2y+a_0 and b=b_1x+b_2y+b_0. For t=u+iv define iota(t)=(0,0,-u,0,0,-v/2) in the coefficient order (a_1,a_2,a_0,b_1,b_2,b_0). On this allowed constant-coefficient slice, the equations are x^2-y^2=u and 2xy=v, exactly equivalent to (x+iy)^2=t. There are precisely the two opposite complex square-root values for t nonzero and the single value 0 for t=0; there is no third real branch to select.

If U is an open coefficient set containing 0, iota^{-1}(U) is an open neighborhood of 0 in C. It contains a disk D_r. Restricting a purported root choice yields a continuous s:D_r->C with s(t)^2=t. Choose 0<rho<r. Then h(w)=s(rho w)/sqrt(rho) maps S^1 continuously to S^1 and satisfies h(w)^2=w. Degrees of circle maps multiply under composition, so the left side has degree 2 deg(h) while the right side has degree 1. The equation 2 deg(h)=1 is impossible for an integer degree. Thus no such U exists. Any open cover of all R^6 contains a member through 0, proving the no-cover conclusion.

Required assumptions are just the displayed polynomial family, the ordinary topology, openness at 0, continuity on a domain containing the chosen loop, and exactness of the root value. There is no numerical approximation, choice of ordering of roots, assumption of a global trivialization, reliance on nonsingular behavior at 0, or assumed finite number of cover members. This is a deduction, not an empirical model claim.

An equivalent elementary proof needs no degree theory: follow a nonzero path gamma from 1 to -1, square it to get a closed parameter loop, and compare s(c^2 gamma^2) with c gamma. Their ratio is continuous and valued in {1,-1}; connectedness makes it constant, whereas equal parameter endpoints and opposite gamma endpoints make its endpoint values opposite.

## Candidate proof check and adversarial attempts

The candidate uses that elementary ratio proof with two straight segments 1 to i to -1. In its first segment gamma=1-t+it for 0<=t<=1; in the second gamma=1-t+i(2-t) for 1<=t<=2. They agree at t=1. The squared norms are (1-t)^2+t^2 and (1-t)^2+(2-t)^2, respectively, bounded by 1 with minimum 1/2. Hence no denominator vanishes. Taking c^2<r makes c^2 gamma(t)^2 stay strictly inside D_r. Both endpoints of this parameter loop are c^2. The ratio q=s(c^2 gamma^2)/(c gamma) has q^2=1, is continuous, and is forced both to be constant and to change sign. Every step is exact. No sample-based continuity inference supplies the topological step.

| Falsification attempt | Checkable outcome |
| --- | --- |
| Constants are not among admissible coefficients | Degree at most one includes degree zero; the slice is allowed. |
| The factor xy rather than 2xy invalidates the complex square | b_0=-v/2 gives 2xy=v after multiplying the second zero equation by 2. |
| Other roots evade the square-root branches | The two real equations are exactly one complex square equation on the slice. |
| A tiny open neighborhood avoids a full loop | The slice preimage is open through 0 and contains a disk, hence arbitrarily small loops. |
| A branch can switch by passing through zero | The selected loop has nonzero parameters and all its roots are nonzero. |
| Algebraic multiplicity permits a continuous value change | Multiplicity is not an additional point in the R^2 target. |
| Disconnected open domains avoid the contradiction | A disk inside their slice preimage supplies the same connected loop. |
| Countably or uncountably many domains cover the bad point | Some member must contain 0 and would violate the local theorem. |
| The source secretly restricts to regular parameters | Full-article and Section 2 checks found no such restriction. |
| Approximation is implicitly allowed | It is separately stated in Problem 2B; exactness is explicit in 2A. |
| Fiber-bundle or homotopy-section convention removes the difficulty | The source definition requires genuine continuous sections and deliberately treats varying fibers. |

The candidate's first four sections are consistent with these checks. Its provenance claims about searches of earlier campaign attempts and its accompanying checker were not independently audited here; neither is needed for the theorem.

## Source versions and bounded correction clues

The final PDF, journal HTML, preprint v1, and current publisher Section 2 preserve the same full six-parameter base and exact continuous choice in Problem 2A. The preprint's general definition uses cross-section without the adjective continuous, while the final inserts that adjective; the actual preprint Problem 2A already requires continuity. The final also replaces the preprint's shorthand system notation with explicit zero equations. Neither change alters the obstruction. Full-article revisions are real, for example the final adds Problem 5D; the final is not merely a reflow of v1, but no analogous repair of 2A was found. The archive has a received-date discrepancy, which has no mathematical effect.

The internal clue is the source's assertion that the square-root example has covering number two. For the punctured parameter plane it does: two complementary slit domains support square-root branches, while a whole-circle degree obstruction excludes one domain. For the whole parameter plane, a section through 0 is impossible by the proof above. Thus the remark indicates either a missing domain qualification or a different intended convention. It cannot logically insert an unprinted hypothesis into the surrounding all-R^6 question.

With a fixed positive root-distance tolerance epsilon, the zero value is already admissible on the constant slice |t|<epsilon^2, so this local exact obstruction does not decide Problem 2B. Similarly, deleting a full discriminant removes the tested parameter; I did not compute the genus of the resulting six-parameter base. A finite cover by nonopen pieces or homotopy sections would also be a different problem.

The bounded source-correction check used four recorded queries, the arXiv version list, publisher correction/version text lookups, journal archive title/correction lookups, and [Crossref DOI metadata](https://api.crossref.org/works/10.1007/s40598-015-0011-9). The arXiv landing page lists only v1. Crossref returned an empty relation object and no update-to or updated-by field. No explicit correction to this article was recovered. The DOI resolver web request failed, while the direct publisher page succeeded; a remote web PDF screenshot failed, so local rendering supplied the visual check. These are bounded negative findings, not proof that no correction or prior observation exists anywhere. No broad citation chase or historical priority verdict was undertaken.

## Remaining gap and allowed promotion

The strongest verified result is the no-open-cover theorem for the literal source target. There is no remaining mathematical gap in that theorem identified by this audit. The exact unresolved external uncertainties are author-intended formulation, possible correction outside this bounded search, and historical priority. The potentially nontrivial repaired variants remain unaddressed.

An accurate public statement is: the printed all-parameter exact-root selection problem has no admissible open cover, because the zero coefficient parameter has a square-root local-section obstruction. It should not be promoted as a new finite-genus computation, a solution of Problem 2B, or a historical novelty result. No outside input was sought; clarifying intended interpretation would require human-led source follow-up if the human chooses it.

This independent audit is 100% complete within its assigned scope. Root case 5% and campaign counts 36 completed / 20 published remain unchanged. All edits were confined to literal_source_adversary; no Git/index/ref/checkout/remote writes, PR/Zenodo/tracker actions, outside-person communications, outreach drafts, other-chat messages, or recursive agents occurred.
