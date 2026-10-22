# Independent priority audit: PR1129 / 30005461

**Disposition: priority fails for publication as a novel resolution.** Both original target conclusions follow from prior literature. Clause 1 is an expressly published theorem. Clause 2 is a direct specialization of a February 2026 theorem, with a short, coefficient-independent singularity calculation. This is a positive identification of prior mathematical coverage, not an inference from an unsuccessful search.

Reviewed immutable head: `26fed29c1130e539ba018a37200f133870f0e036`, author/commit date 2026-10-10 03:47:44 −0700. The parent reported the mandatory live spreadsheet duplicate check completed 2026-10-21T22:48:06.950961+00:00, before substantive candidate work: 180 rows, no ID/alias/Motzkin/mixed-odd match. This child did not independently read or mutate that spreadsheet. Publication priority and spreadsheet duplication are distinct checks.

## Exact original target and prior coverage

Bruce Reznick, *The Odd Powers of the Motzkin Polynomial, etc.*, Oberwolfach Report 14/2023, printed pp.778–780, asks two relevant questions on p.780 (captured PDF p.40):

1. If real polynomials p^(2i+1) and q^(2j+1) are sums of squares, is (p+q)^(2i+2j+1) a sum of squares?
2. For f_c=x^4y^2+x^2y^4+1−cx^2y^2 and {c:f_c^(2k+1) SOS}=(-∞,c_k], what is lim c_k?

The nearby perturbation M+ε(x²+y²+z²)³ has its own already established eventual-power result. That different family does not by itself answer question 2. Nor does question 2 ask for an explicit exponent, convergence rate, strict increase of c_k, or an SOS power at c=3.

**Clause 1.** Blekherman–Kozhasov–Reznick, *On odd powers of nonnegative polynomials that are not sums of squares*, Forum Math. Sigma 14 (2026), e65, Theorem 5.3, DOI [10.1017/fms.2026.10221](https://doi.org/10.1017/fms.2026.10221), gives exactly the mixed exponent k+ℓ−1 for odd k,ℓ. It was already Theorem 44 of [arXiv:2407.21779v1](https://arxiv.org/abs/2407.21779v1), submitted 31 July 2024. Its Pinelis attribution must be retained. The PR correctly calls this credited background. Different polynomial degrees are handled by harmless even-degree homogenization to a common degree.

**Clause 2.** Baldi–Blekherman–Kozhasov–Plaumann–Reznick–Sinn, *Stubborn Polynomials*, [arXiv:2602.01191v1](https://arxiv.org/abs/2602.01191v1), submitted 1 February 2026, manuscript dated 3 February 2026, Theorem 6.4 (p.20), says that a nonnegative non-SOS ternary sextic with total real delta invariant at most 8 is not stubborn. Theorem 1.2 states the full classification. “Not stubborn” means at least one odd power is SOS. The currently returned arXiv history lists only v1. The author publication page calls it submitted for publication; I did not establish a journal publication. A public preprint still establishes prior availability.

## Independent specialization proving complete prior coverage

Put M_c=x^4y²+x²y^4+z^6−cx²y²z². For c≤0 it is already a sum of monomial squares. Fix 0<c<3.

AM–GM gives x^4y²+x²y^4+z^6≥3x²y²z². Thus M_c≥0; if xyz≠0 then M_c≥(3−c)x²y²z²>0. If xyz=0, direct substitution shows that its only real projective zeros are [1:0:0] and [0:1:0]. This enumerates all real zeros, including infinity in the affine z=1 problem.

For completeness M_c is non-SOS throughout this range. The half Newton triangle has exactly the cubic lattice exponents (2,1,0),(1,2,0),(0,0,3),(1,1,1). In any SOS, cubic roots can use only these four monomials, by the Newton support property. Of all ordered pairs of allowed exponents, only (1,1,1)+(1,1,1) equals (2,2,2). Consequently the coefficient of x²y²z² would be a sum of squares of real coefficients, whereas it is −c<0. The finite enumeration is independently reproduced offline. The Newton support property is standard and is also explicitly used in Notices 2021 Example 1.5 and BKR Lemma 3.14; this audit does not pretend to infer an SOS decomposition from numerical tests.

At [1:0:0], in coordinates (u,v)=(y,z), the local equation is

    h0 = u²+u⁴+v⁶−cu²v².

Its multiplicity is 2 and its tangent cone is u², with a single real projective tangent. Blow up that tangent using u=av and divide by v²:

    h1 = a²+a⁴v²+v⁴−ca²v².

Again the only real point above the origin is (a,v)=(0,0), multiplicity 2, tangent cone a². Substitute a=bv and divide by v²:

    h2 = b²+b⁴v⁴+v²−cb²v².

This last real singular point has multiplicity 2 and positive definite tangent cone b²+v². It therefore has no real first-order infinitely near point: on the exceptional projective line that homogeneous quadratic has no real zero. Equivalently the third blow-up has leading exceptional restriction b_new²+1, with no real zero; the complementary chart likewise has 1+v_new². The local real delta recurrence of *Stubborn Polynomials*, Definition 6.3, therefore gives

    δR_[1:0:0](M_c) = binom(2,2)+binom(2,2)+binom(2,2) = 3.

Symmetry gives the same value at [0:1:0]. The parameter c only occurs above the relevant lowest degrees in each step, so the argument holds for every real 0<c<3, not merely c=1 or rational c. Hence total δR(M_c)=6≤8. All hypotheses of the previously available Theorem 6.4 hold, so some odd M_c^(2j(c)+1) is SOS. Multiplying its SOS representation by the square M_c^(k−j(c)) gives SOS for every k≥j(c). Dehomogenizing z=1 gives precisely the original affine f_c, without an extraneous multiplier or denominator.

BKR Theorem 6.3 identifies the same intervals (-∞,c_k] and monotonicity. For each fixed c<3 the preceding conclusion implies c_k≥c eventually. Also f_c(1,1)=3−c<0 if c>3, hence no odd SOS power is possible there. Thus lim c_k=3. The limit conclusion, including all fixed real c<3 and all sufficiently large odd exponents, is already a consequence of the February theorem plus this elementary calculation.

Theorem-level reliance is explicit: the last paragraph of the source proof prints an inconsistent invocation of Scheiderer (X=Z and L=M=ω). Its preceding construction and displayed square-root degrees require the contracted anticanonical model X=Zbar and L=M=ω_Zbar^(-1). The anticanonical inverse is ample; ω itself is not the ample bundle asserted there. These are proof-invocation notation/sign errors, not a change in the stated Theorem 6.4 or its all-c specialization. I import that theorem as a prior literature result, with its intended invocation understood; I have not independently reconstructed all Demazure/Dolgachev facts behind its proof. This audit therefore does not provide a formal foundational certification of that theorem.

No claim of a uniform exponent in c is made. At c=3 four extra real zeros appear, and this argument is inapplicable; BKR proves the Motzkin endpoint stubborn. The all-c calculation is a routine specialization of the publicly available classification and does not establish a new resolution.

## Why the lingering printed question does not establish novelty

The final April 2026 BKR article still asks whether lim c_k=3 at the end of §6 (p.24). However, p.23 of that same final article cites *Stubborn Polynomials*, Theorem 1.2, as a completed classification. Both statements have been directly checked in the publisher PDF and HTML. A retained question does not negate a theorem that already implies its answer. The decisive objection is the explicit deduction above, not speculation about the authors' intentions.

The PR's independent cubic-surface proof may be useful exposition. It also needs context: Blekherman–Sinn–Smith–Velasco, *Sums of Squares: A Real Projective Story*, Notices AMS 68 (2021), 734–747, DOI [10.1090/noti2280](https://doi.org/10.1090/noti2280), already presents the identical cubic xyz=w³, associated Motzkin quadratic, and the same monomial representation up to renaming/reordering, at pp.735 and 737 (Example 1.5). Scheiderer's [arXiv:1104.1772v1](https://arxiv.org/abs/1104.1772v1), Corollary 4.2 (p.11), already supplies eventual SOS powers for strictly positive square-line-bundle sections on the required reduced projective schemes. I checked these passages independently. I do not assert that the exact two-source combination was explicitly written before this PR; that weaker historical question is immaterial after the direct 2026 classification specialization.

## Scope, evidence and remaining limitations

The conclusions about novelty are stronger than search-based absence findings: precise prior theorems cover the complete target. Query strings and search limitations are in QUERY_LOG.json; retrieved bytes and failures are bound in SOURCE_FETCH.json. Only primary sources support mathematical conclusions. Secondary search results were leads, not authority. The Reznick publication list retrieved is explicitly last updated April 2023 and lists a Shankar collaboration as in preparation; it cannot certify current status. Broad Delzell searches supplied no additional exact theorem used here. No worldwide literature-absence certificate is claimed. Searching for an even earlier exact specialization is unnecessary for this publication decision and remains uncompleted.

Complete PDF/text files were captured; focused direct reading covered OWR pp.778–780, Stubborn pp.1–2 and 18–21, BKR published §5–§6 pp.21–24 and the introduction's distinction between perturbations, Scheiderer pp.1–3 and 9–11 with Corollary 4.2, Notices pp.734–737. Other bodies were searched for relevant terms and leads, not line-by-line audited throughout. Stubborn's cited Demazure/Dolgachev resolution theory was not independently reproved or fully retrieved. The priority conclusion imports its explicit theorem just as research ordinarily imports literature theorems; there is no new mathematical objection to its statement here. This is not a complete independent correctness audit of the PR's alternative geometric proof.

The offline verifier checks source bindings, exact blow-up identities, all local multiplicities/tangent cones, the finite Newton-support enumeration, and the recorded disposition, using explicit failure guards. It does not formally verify the imported mathematical theorems, AM–GM, real projective geometry, or historical originality. Those trust boundaries are explicit in CHECKS.json. Normal and optimized Python runs and meaningful corrupted-input controls are reported outside the sealed package. No captured/original/sealed program was executed in place, and no PR, provider, ledger, Git index/ref, publication, or unrelated files were modified.

After my decisive source finding and independent calculation, the parent disclosed that a separate October 17 audit had reached the same priority objection. I did not inspect or rely on that earlier effort, and it supplies no premise of this report.

Recommended parent action: record the candidate as covered by prior mathematical literature; do not publish either clause as a novel open-problem resolution. Any preservation of the alternative proof should credit these prior results and distinguish exposition from new discovery. No public communication was prepared or initiated by this child.
