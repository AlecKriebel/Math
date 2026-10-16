# Current qualified original-target disposition — 2026-10-06T23:35:18.119666+00:00

**final-operative-disposition-postimages-preparation_only. Original target already_solved by verified older mathematical consequence; candidate mathematics PASS; alternative polynomial novelty UNRESOLVED; express first named-answer priority unverified.** Accepted scientific disposition clearance only. Actual closure/native/author/global propagation are pending and no publication is authorized. The sealed v2 review bundle below is archival; its earlier pending-disposition wording predates the accepted fresh gate. Neither the original reviewer nor the fresh disposition reviewer is represented as having approved these newly edited postimage bytes.

---

# Current preparation notice — 2026-10-06

**corrected-postimages-preparation_only; mathematics PASS; PRIORITY_NOT_CLEARED.** The historical review below concerns the original candidate SHA8ee69b778f281333c6a09850ed03de02f7d936174ab467e0899ca47799a2f4e7. Its prior source assessment of Noor2016 is superseded by the dated correction addendum. It did not review or certify the current citation text. Its original bytes and receipts are separately retained in archival_original.

---

# Independent review of the all-real-alpha coefficient criterion

**Verdict: PASS_COMPLETE_SUFFICIENT_CONDITION.** No mandatory correction was found. The candidate answers the literal sufficient-generalization request in Hayman Problem6.64 for every real alpha, recovers both endpoint weights, and proves the stated restricted-family sharpness for0<alpha<=1. This is an independent adversarial AI review, not human peer review. Priority is unestablished.

Reviewed CANDIDATE.md SHA-256: `8ee69b778f281333c6a09850ed03de02f7d936174ab467e0899ca47799a2f4e7`.

## Source and scope

The complete [Hayman2018 source](https://arxiv.org/abs/1809.07200), printed141/PDF142, was checked. It asks for a coefficient sufficient condition, not a necessary-and-sufficient classification or a globally optimal admissible region. It explicitly permits real alpha and requires nonvanishing of f/z and f'. The historical “no progress” update does not establish novelty.

[Kumar–Ravichandran2017](https://mjms.upm.edu.my/fullpaper/2017-September-11-3/Kumar,%20S.-365-375.pdf), printed368, displays the two-denominator majorization used here for0<=alpha<=1. The attribution is appropriate. [Noor–Khan–Piejko2016](https://www.etamaths.com/index.php/ijaa/article/view/738/210), Definition3 and Theorem1, supplies sufficient coefficient conditions for a conic-domain family whose k=0,A=1,B=-1 specialization is the ordinary class. These results show established prior method; neither source is presented as a novelty certificate. The [June2026 related preprint](https://arxiv.org/abs/2606.21574) has different stated characterization/coefficient/Schwarzian conclusions. Its proof is not required or independently certified here.

## Independent analytic derivation

Let b_n=|a_n|, and for k>0 put w_n=n[1+k(n-1)]. For a strict budget sum w_n b_n<1, the sums A=sum b_n, B=sum n b_n, X=sum(n-1)b_n and Y=sum n(n-1)b_n are finite; B<1, A<=B/2, and both analytic denominators are nonzero. Directly from the series,

    zf'/f-1 = sum (n-1)a_n z^(n-1) / (1+sum a_n z^(n-1)),
    zf''/f' = sum n(n-1)a_n z^(n-1) / (1+sum n a_n z^(n-1)).

This gives the two positive-denominator estimates without assuming univalence beforehand. A separate coefficientwise way to check the budget conversion is

    w_n-1=(n-1)(1+kn),      w_n-n=k n(n-1).

Thus 1-A>sum(w_n-1)b_n>=(1+2k)X and 1-B>kY. Unless f=z, both relevant moments are positive, yielding X/(1-A)<1/(1+2k) and Y/(1-B)<1/k. This independently recovers the author's equivalent Y>=2X argument.

Set a=|1-alpha| and b=|alpha|. For alpha nonzero, b>0, and the proposed positive root k satisfies exactly

    a/(1+2k)+b/k=1.

The resulting bound |J_alpha-1|<1 proves the required strict positive real part. Absolute values cover both negative alpha and alpha>1 without any sign interpolation assumption. The positive root is unique; the three piecewise formulas agree with the unified formula and with k(1)=1.

The alpha=0 case must not divide by k or require Y finite. The candidate correctly treats it separately: B<1 and (B-A)/(1-A)<1 give the conclusion and zero avoidance, with only the first weighted sum finite. The removable values at z=0 are f/z=f'=J_alpha=1.

For the nonstrict budget, dilating f_R(z)=f(Rz)/R for0<R<1 strictly lowers every nonzero coefficient contribution. Hence the strict theorem applies to f_R. For each original point w choose |w|<R<1; the exact rescaling of J and the denominators transfers the conclusion to w. The identity function is harmless. This is a valid proof of strict positivity in the open disk even when the coefficient budget is exactly one; no assertion of positivity on the unit circle is made.

## Sharpness and attempted counterexamples

For0<alpha<=1, the proposed witness f_c=z-cz^2 with0<c<1/2 has both required nonvanishing factors in the open disk. Independent algebra gives

    J_alpha[f_c] = [1-(4+alpha)x+4x^2]/[(1-x)(1-2x)], x=cz.

At c_*=1/[2(1+k)], the numerator is zero. Its derivative8x-(4+alpha) is strictly negative on0<=x<1/2 for alpha>0. If0<=lambda<k, the interval c_*<c<min(1/2,1/[2(1+lambda)]) is nonempty, and an interior real z>c_*/c yields negative J while the weaker coefficient budget is strictly satisfied. This proves precisely the stated sharpness inside the family n[1+lambda(n-1)]. It does not prove optimality for other weights or outside[0,1]; the candidate expressly avoids those claims.

The explicit naive-interpolation example also checks: alpha=1/2,c=8/25,z=31/32 gives x=31/100 and J=-53/1311, with naive budget24/25<1. Endpoint alpha=0 has minimal nonnegative family parameter0, while alpha=1 gives the usual n^2 test. Near-zero alpha, large positive/negative alpha, equality budgets, sparse polynomials and complex phases were included in independent controls; no gap was found.

## Reproducibility and limitations

The submitted verifier was replayed beside the frozen note. All50,840 assertions passed, and the receipt reproduced byte for byte, SHA-256 `42c249c59d8b6cdb47cbc226e96eb64d27678065a0886f39b998d51f4e8f1409`.

A separately written checker passed28,722 exact assertions, using69 rationally parameterized alpha/k pairs,3,312 Gaussian-rational interior evaluations,40 independently chosen sharpness witnesses, and the explicit interpolation failure. It parameterizes the quadratic relation independently and uses exact fractional complex arithmetic. These finite checks test algebra and sign handling; the all-function analytic proof is the argument above, not sampling.

The full sufficient-condition verdict does not establish priority or a necessary condition for membership in M_alpha. No corrections to the frozen mathematical file are required. Reviewer runtime model metadata is not exposed in this context; inherited settings were unchanged, and no unsupported model label is asserted.

## Current-corrections addendum — 2026-10-06

This is a bounded correction-preparation addendum, not a new human referee report. The mathematical proof body is unchanged and the separate2026-10-06 gate is PASS after exercise of the explicit-if checker repair. The current candidate artifact SHA-256 is fe20c46ed59355387ac63efa41f1e311cdca4697babbb7dbcae06ef0220bb80b. Current source status is PRIORITY_NOT_CLEARED; there is no publication or disposition readiness.

The positive historical characterization of Noor2016 as a verified sufficient criterion is withdrawn. Its literal repeated-sum statement is malformed/potentially vacuous; its intended single-total interpretation admits alpha1,f=z-z³/5,total26/25<2 yet J1(3/4)=-1/53. Both denominators are nonzero, and Re f'>2/5 gives univalence, so those hypotheses do not rescue it.

June2026 Proposition2.2 is also falsified by f=z-z²/6 at beta1/2,alpha1/(1-ln2),z19/20, yielding (2222-3362ln2)/[4141(1-ln2)]<0. The valid2017 displayed majorant yields the candidate on [0,1]; the every-real-alpha statement is a formal absolute-multiplier proof adaptation beyond that source's stated scope. An identical prior all-real theorem and express named-problem priority remain unverified. Authenticated Silverman1985 permitted preview pages93–94 now support the visible negative-coefficient [0,1] Theorems1/2, as detailed in the source-update supplement below; full-chapter and all-real priority remain unresolved.

The current author checks bind to the revised candidate hash; normal independent and optimized independent checks use the exact exercised explicit-if checker SHA4ccfb72d1f9e41c92eed9f26becd9ae1ece41f43718a74038bf993edf413686d. The optimized false-parameter control must fail. Actual executions and process IDs are recorded in the preparation's REPLAY_JOURNAL.jsonl and REPLAY_RESULTS.json. Historical byte-identical receipts belong to the original text, not the corrected candidate. Original effort1/5, one substantive approach, zero added central proofs, and no human peer-review claim remain unchanged.

## Partial-preview source-update supplement — 2026-10-06T23:15:45.249067+00:00

Actual preparation PID 75393. [Silverman1985, Coefficient Conditions for a Subclass of Alpha-Convex Functions, Contemporary Mathematics38, pp.91–97](https://doi.org/10.1090/conm/038/789450) now has authenticated permitted [GoogleBooks preview pages93–94](https://books.google.com/books?id=QuQbCAAAQBAJ), visually read independently. The visible Theorem1 concerns f=z-sum a_n z^n with a_n>=0 and 0<=alpha<=1: membership in its negative-coefficient class is equivalent to the disk-local two-denominator expression being below1 for every radius r<1. Its remark replaces this with a boundary non-strict condition when sum n a_n<1 and sum n² a_n is finite. The visible Theorem2 gives sharp starlikeness order beta=(sqrt(alpha²+8alpha)-3alpha)/[2(1-alpha)] for alpha<1, beta(1)=2/3, with quadratic extremal z-[(1-beta)/(2-beta)]z². Its constant satisfies beta=2kappa/(1+2kappa), so that quadratic coefficient equals 1/[2(1+kappa)]. These are earlier negative-coefficient [0,1] antecedents; they are not an explicitly published all-real theorem or express named-problem answer. Pages91–92 and95–97 were not read by this preparation agent, so neither full-chapter verification nor complete proof review is claimed. Silverman1986 and1991 remain unresolved fulltexts. Priority and mathematical-substance reconciliation remain pending.

This update credits only the claims visible on authenticated pages93–94; it does not pre-adopt unread pages or an all-real priority conclusion. The archived v1 preparation predates this source update. The citation change refreshes the normal author/replay artifact-hash receipts; unchanged independent checker and its normal/optimized/false-guard exercises are retained from v1 with their actual original PIDs and timestamps.

## Dated operative-disposition preparation addendum — 2026-10-06T23:35:18.119670+00:00

Actual stage PID 90793. Current prepared candidate SHA-256 fd4240fdd20ec35bb429a3d6c439d04cd5f4429a8b86b4239380c62deb4588f6. Proof sections2–4 remain byte-identical to original and sealed v2. The fresh scientific disposition report5f05db76d89edda6a694e06f8c307c2ec6dc535b30bfeeacb609c37bde627623 and accepted root gate1a3aa4f259f9b94afdbc02dae85969d9f49ff4e391a92ae6ed87cbce0cc9ef0f reviewed the sealed v2 input and narrow original-target outcome, not an unexecuted closure/global operation.

The accepted fresh scientific disposition distinguishes the original question from the alternative polynomial theorem above. The original literal all-real sufficient-generalization target is already mathematically answerable by the following consequence of published1975 results. Candidate mathematics remains PASS; the whole polynomial criterion is not proved historically subsumed, and its alternative novelty remains UNRESOLVED. No express first named-problem answer is assigned. This is scientific disposition clearance only: actual PR closure and native/author/global propagation remain pending, with no publication authorization.

[Silverman1975, Univalent Functions with Negative Coefficients, Theorem1 and its immediate corollary, printed110](https://doi.org/10.1090/S0002-9939-1975-0369678-0), gives sufficient absolute-coefficient conditions for arbitrary complex coefficients: sum n|a_n|<1 implies starlikeness and sum n²|a_n|<1 implies convexity. The negative-coefficient restriction applies to the converse, not to this sufficient direction. [Mocanu–Reade1975, The Radius of Alpha-Convexity for the Class of Starlike Univalent Functions, Alpha Real, printed397](https://doi.org/10.1090/S0002-9939-1975-0374404-5), gives the alpha-convexity radius of the entire starlike univalent class:

    R_alpha=(1+alpha)-sqrt((1+alpha)²-1),                   alpha>=0;
            sqrt[(2-sqrt(-alpha))/(2+sqrt(-alpha))],        -3<=alpha<=0;
            -(1+alpha)-sqrt((1+alpha)²-1),                  alpha<=-3.

The leading minus in the last branch is essential and was visually verified by the source/disposition reviewers. The branches agree at alpha=-3; R_0=1, and 0<R_alpha<1 for every nonzero alpha.

Define W_0(n)=n and W_1(n)=n². At every other real alpha define W_alpha(n)=n R_alpha^(1-n). Then

    sum_(n>=2) W_alpha(n)|a_n|<1

is an all-real sufficient generalization with both exact endpoint tests. For a nonendpoint alpha put R=R_alpha and define

    h(w)=w+sum_(n>=2) a_n R^(1-n) w^n.

The weighted bound makes sum n|a_n R^(1-n)|<1, so the series for h and h' converge on the closed disk and h is analytic on the open disk. The notation h(w)=R f(w/R) refers to this justified power-series extension, not an extra assumption that the original f was already defined outside its disk. Silverman's criterion makes h starlike. Nonvanishing also follows directly from |h/w-1|<=B/2<1 and |h'-1|<=B<1, with B=sum n|a_n R^(1-n)|.

Mocanu–Reade gives Re J_alpha[h](w)>0 on |w|<R. The radius conclusion is used only on this open disk; no positivity on its boundary is asserted. The exact identities

    h(Rz)=R f(z), h'(Rz)=f'(z), h''(Rz)=f''(z)/R,
    J_alpha[h](Rz)=J_alpha[f](z)

transfer strict positivity and both nonzero factors to every |z|<1. At zero the removable expressions equal1. The two endpoints follow directly from Silverman's coefficient conditions. All weights are positive and finite, and sufficiently small polynomial perturbations satisfy them. The source question does not require continuous parameter dependence or polynomial weights; the endpoint patch is explicit.

This is an audit deduction from older published theorems, not a claim that the1975 authors printed this scaling deduction or expressly answered Miller–Hayman6.64. It establishes the accepted original-target already_solved classification by mathematical consequence, while express historical named-answer priority remains unverified.

The two coefficient balls must not be conflated. For a nonendpoint alpha and epsilon=1/[2(1+kappa)], the coefficients a_n=epsilon/n⁴ give candidate sum below1/2 by sum_(n>=2)1/n²<1, yet have radius of convergence exactly1. Since R<1, the old terms epsilon R^(1-n)/n³ do not tend to zero. Thus the candidate ball is not fully subsumed by the old exponential test. Conversely, at alpha=-1/2, kappa=1, f=z-(3/10)z² has candidate total6/5>1 but old total(3/5)/R<1: here R=sqrt[(2-1/sqrt2)/(2+1/sqrt2)]>3/5, as verified by32>34/sqrt2. The balls are incomparable at this negative parameter. No uniformly stronger-ball claim is made.

The original1/5 effort, one substantive approach, zero added central proof-search turns, and no human-review claim are preserved. The accepted fresh report reviewed the sealed v2 input and proposed scientific outcome; it did not certify these newly prepared source/status postimage bytes or execute a service/global writer. A separate reviewed writer step is still required. No preprint, Zenodo DOI, or tracker entry is authorized or created.

The source/checker corrections from v2 remain operative: no valid sufficiency credit to the malformed/intended-false2016 criterion, no imported false June2026 Proposition2.2, and the unchanged explicit-if checker at SHA4ccfb72d1f9e41c92eed9f26becd9ae1ece41f43718a74038bf993edf413686d. New author/replay normal receipts bind to this prepared candidate hash. The earlier independent normal/optimized and optimized false guard retain their actual original PIDs/dates; this stage does not rerun or relabel them as fresh executions. Original effort1/5, substantive1,newproof0,no human referee.
