# Independent adversarial review of PR134's original-target disposition

**Verdict: PASS for the narrowly stated original-literal-target outcome.** The generalization requested in Miller–Hayman Problem6.64 is mathematically answerable by the verified1975 theorems and the scaling deduction below. Under this program's requirement to publish a decisive new resolution of the original unsolved problem, classifying that original target already_solved and closing its claimed-resolution PR unmerged is defensible. This is not a finding that the candidate theorem is false, that its entire polynomial criterion was previously published, or that no distinct contribution can remain. Its alternative-criterion novelty remains unresolved.

Reviewed proposal SHA-256 de95307b19c2035e58e41a2f2d8e2c54c8a05d673fc0773ff9e4d3c84e50431f; proposed closure comment eb12f6eab8726111df1c3cc01f93f4345b5d8b34b5233cf2ea6b6c9251d82007. No scientific blocker was found in either proposal at these exact bytes. This report supplies bounded scientific decision clearance, not authorization or certification of an unexecuted global or service writer.

## Independent procedure and exact source

I independently read the relevant complete passages in both Hayman2018 and the user-supplied2019 edition, the full extracted eight-page Silverman1975 paper, and the full six-page Mocanu–Reade1975 paper. I separately rendered and visually read Hayman printed141/162, Silverman printed110, and Mocanu–Reade printed397. The latter visual reading verified the essential leading minus in the negative-alpha radius branch that OCR omitted. Input bytes and renders are pinned in the private source/render receipt.

Both Hayman passages ask for a sufficient generalization of the n and n² absolute-coefficient conditions that implies membership in M_alpha, with alpha real. Neither passage prescribes a continuous parameter dependence, polynomial weights, a unique interpolation, an optimal region, or a necessary-and-sufficient characterization. The adjacent no-progress report is a historical report to the editors; it cannot negate the validity of a checked mathematical consequence of other published results. The original candidate and its readiness record themselves use this literal sufficient-condition scope.

I attempted the following scope objections: the exponential condition might secretly add an analytic-continuation assumption; the radius theorem might apply only to negative coefficients; the endpoint patch might fail to generalize both tests; the radius supremum might give only nonnegative real part; an implicit continuity or polynomial condition might exclude the construction; and lack of express named-answer priority might invalidate every already_solved classification. None defeats the narrow mathematical conclusion. The last objection does constrain what may be claimed about historical priority, as discussed below.

The initial independent conclusion was frozen at 2026-10-06T23:23:57.763333+00:00, before reading another family's final report, at SHA-2569cb9c477a00ac593eca794de563bc25ee6d5315e79fda5d6943b0ede0561ee38. The parent proposal was the disclosed task hypothesis, not an independently unseeded literature search. I did not read other families' final scientific reports to generate this conclusion.

## Checked older consequence, including every boundary and analytic condition

[Silverman1975](https://doi.org/10.1090/S0002-9939-1975-0369678-0), Theorem1 and its immediate corollary on printed110, state sufficient absolute-coefficient tests for f=z+sum a_n z^n without restricting those a_n to negative reals. The converse later in Theorem2 has the negative-coefficient restriction. At order zero, sum n|a_n|<1 implies starlikeness and sum n²|a_n|<1 implies convexity. The source actually permits equality; the strictly smaller hypotheses used here are valid special cases. The paper title does not convert its sufficient theorem into a negative-coefficient-only result.

[Mocanu–Reade1975](https://doi.org/10.1090/S0002-9939-1975-0374404-5), printed397, gives the alpha-convexity radius of the entire starlike univalent class, with the same differential expression as the target:

    R_alpha = (1+alpha)-sqrt((1+alpha)^2-1),                 alpha>=0;
              sqrt((2-sqrt(-alpha))/(2+sqrt(-alpha))),      -3<=alpha<=0;
              -(1+alpha)-sqrt((1+alpha)^2-1),               alpha<=-3.

For alpha>0 the first expression equals 1/[1+alpha+sqrt((1+alpha)^2-1)], so it is strictly between zero and one. In the middle branch t=sqrt(-alpha) lies in [0,sqrt3], strictly below2, and the ratio is positive, equaling one only at alpha0. For alpha<-3 write x=-(1+alpha)>2: the last expression equals 1/[x+sqrt(x²-1)], strictly between zero and one. At alpha=-3, (2-sqrt3)/(2+sqrt3)=(2-sqrt3)², so the two formulas agree at2-sqrt3. At alpha0 both applicable formulas give1. No other real alpha gives radius1.

Set W_0(n)=n and W_1(n)=n². At every other alpha set W_alpha(n)=n R_alpha^{1-n}. Suppose sum W_alpha(n)|a_n|<1. For an alpha outside the two endpoints put R=R_alpha and define

    h(w)=w+sum_(n>=2) b_n w^n,  b_n=a_n R^(1-n).

Then B=sum n|b_n|<1. Consequently sum |b_n|<=B/2<1/2 and the series for h and h' converge uniformly on the closed unit disk. Thus the notation h(w)=R f(w/R) is justified by the power series extension forced by the condition itself; it does not assume an unspecified value of the given f outside its original disk. Silverman's criterion makes h starlike on D. One can also check nonvanishing directly: |h(w)/w-1|<=B/2<1 and |h'(w)-1|<=B<1. These estimates include the removable value at zero.

The radius theorem gives Re J_alpha[h](w)>0 for every |w|<R. Defining the radius as a supremum causes no endpoint problem: the admissible radii form a downward-closed set, and every fixed r<R lies below an admissible larger radius. We use only open |w|<R, never assert strict positivity on |w|=R.

The exact chain-rule identities are

    h(Rz)=R f(z), h'(Rz)=f'(z), h''(Rz)=f''(z)/R,
    J_alpha[h](Rz)=J_alpha[f](z).

They transfer strict positivity and both required nonzero factors to every z in D. At zero both J expressions have their common removable value1. At alpha0 the coefficient condition is exactly the source's starlike test; at alpha1 it is exactly the convex test. All weights are finite and positive for each fixed alpha and integer n. The condition is nonvacuous: the identity and every sufficiently small finite coefficient perturbation satisfy it. Parameter continuity at alpha1 is not needed for the literal source question; the endpoint patch is explicit, not hidden.

This proves a complete sufficient generalization for every real alpha as a short audit deduction from old published theorems. It is not evidence that either1975 author wrote this particular deduction, expressly answered Miller6.64, or deserves a newly assigned first named-answer date. The historical and mathematical claims remain different.

## Candidate validity and why whole-theorem historical subsumption does not follow

I read the candidate proof, including the special alpha0 case without a finite second moment, the positive-root identity, equality by dilation, and restricted sharpness for0<alpha<=1. Its moment proof remains valid. In the strict case B+kappa Y<1 and Y>=2(B-A) give the two strict majorant bounds; their coefficients |1-alpha| and |alpha| are nonnegative, with the second positive away from alpha0. The alpha0 estimate is independent of Y. Dilation turns the nonstrict budget into a strict local budget and transfers back. The quadratic sharpness witness stays below1/2, has nonzero denominators, and crosses the first real numerator root; it proves precisely the stated parameter-family sharpness. It does not establish arbitrary-weight optimality or sharpness for alpha outside[0,1].

The parent proposal correctly refuses to equate elementary derivation with historical publication. A valid non-subsumption witness is a_n=epsilon/n⁴, epsilon=1/[2(1+kappa)]. Term by term its candidate sum is bounded by epsilon(1+kappa)sum_(n>=2)1/n²<1/2, since 1/n²<1/[n(n-1)] and the latter series telescopes to1. Its power-series radius is exactly1 by the root test. For every R<1, the old exponential terms epsilon R^(1-n)/n³ do not tend to zero. This function meets the candidate condition but fails the old exponential test. The witness is intended for alpha outside the two patched endpoints; it does not purport to distinguish the identical endpoint tests.

The reverse inclusion fails at alpha=-1/2: kappa=1, and f=z-(3/10)z² has candidate sum6/5>1. Its old exponential sum is(3/5)/R<1. For R²=(2-1/sqrt2)/(2+1/sqrt2), the inequality R>3/5 reduces to32>34/sqrt2, which follows from1024>578 after squaring positive quantities. The balls are therefore incomparable at that parameter. A description of the candidate as uniformly stronger than the older ball would be false.

I visually read authenticated permitted Silverman1985 preview pages93–94. They indeed display a negative-coefficient, alpha-in[0,1] moment criterion, a sharp starlikeness-order constant, and the related quadratic extremal. Their beta satisfies beta=2kappa/(1+2kappa), so the quadratic coefficient equals1/[2(1+kappa)]. They do not, at the inspected pages, state the candidate's all-real arbitrary-complex-coefficient theorem. I did not inspect preview pages96–97 in this audit, and do not claim full-chapter review; the parent separately recorded its broader partial coverage. None of this permits a categorical claim that every candidate conclusion was known. The alternative polynomial theorem could remain distinct; novelty and value of that different paper target remain uncleared.

## Reasonable repair and the program's outcome boundary

I authenticated all166 members in the sealed corrected-attempt preparation, all17 original and corrected bodies, and the exact preservation of proof sections2–4. The prepared candidate hash is fe20c46ed59355387ac63efa41f1e311cdca4697babbb7dbcae06ef0220bb80b. The repaired independent checker uses explicit guards at SHA4ccfb72d1f9e41c92eed9f26becd9ae1ece41f43718a74038bf993edf413686d. Its existing actual normal/optimized and injected-failure receipts retain their original PIDs and dates; citation-only v2 author/replay receipts refresh the new artifact hash. I did not rerun or alter those preserved author artifacts.

I read the prepared attribution corrections and their dated archival-review limits. They withdraw positive reliance on the defective intended Noor2016 criterion, record the June2026 counterexample, credit the older method, and avoid claiming that the historical reviewer approved revised source text. The two counterexample evaluations themselves check algebraically: the cubic at3/4 has J_1=-1/53; the quadratic at19/20 gives exactly (2222-3362 ln2)/[4141(1-ln2)]. The bounds2/3<ln2<25/36 follow from the positive atanh(1/3) series, bounding every remaining denominator by3. These source repairs are reasonable attempts to repair an otherwise valid mathematical candidate. This disposition audit does not substitute for full independent reviews of those two separate papers.

Repairs cannot change the fact that the original unrestricted existence target follows from older valid theorems. The persistent program specifically requires a decisive new resolution of the original unsolved problem with cleared provenance and priority. A separate potentially new coefficient improvement, without cleared novelty, does not automatically meet that narrower publication scope. The user authorized a priority-qualified publication exception for PR50; I find no evidence that this authorizes the same exception here.

Accordingly I find the proposed original-target already_solved classification and unmerged closure scientifically defensible within that program. The reason is failure of the previously-unsolved-original-target framing, rather than a refutation of the candidate mathematics or a proof of no novelty anywhere in it. The existing proposal and comment preserve this distinction. There are no substantive scientific corrections required to those exact proposed bodies.

Global propagation must preserve the same fields distinctly: original target already_solved by an older mathematical consequence; candidate mathematics PASS; alternative criterion priority unresolved; express historical named-answer priority unverified. The current repaired17 staging postimages predate this disposition and correctly say preparation-only/priority pending. A later operative writer must add the present qualified target conclusion and source explanation; it must not simply rename every priority field PRIORITY_CLEARED, erase historical originals, or call the whole candidate historically subsumed. Those are remaining execution requirements, not claims of completed propagation.

## Controls, limitations and completion

Own explicit-guard controls ran in eight actual subprocesses:4,209 checks passed identically normally and optimized, and wrong rescaling, a wrong negative radius sign, and an overstated subsumption condition each failed under both modes. Exact rational checks cover336 J-scaling identities,48 derivative-jet identities,12 coefficient rescalings,3,000 tail term inequalities, and the negative quadratic inequalities; the radius positivity/junction samples are explicitly labeled90-digit Decimal samples. These controls are diagnostics. The all-function analytic proof above supplies the general conclusion; finite sampling is not presented as proof.

This review did not perform a fresh service/API readback, assign earliest historical priority, clear an alternative paper's novelty, or execute Git/index/main/native/author/PR/publishing/tracker changes. All writes are within this audit's dedicated folder. No external individual was contacted. Original effort remains1/5 with one substantive approach; this validation adds zero central proof-search turns and makes no conventional human-refereeing claim.

Bounded scientific disposition audit:100% complete at the final seal's actual UTC/PID. Remaining parent work is separately reviewed, coordinated global/native propagation, actual service closure/comment/readback and checkpoint release. The overall persistent goal remains incomplete.
