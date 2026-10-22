# Independent mathematical audit: B-regular localization

## Decision and exact scope

Problem ID 2303033, AMR-022-3033, catalog rank 901; partial investigation, 2/5 mathematical approaches. Audit date: 2026-10-06.

**Accept the authored mathematical partial result.** The lens example rigorously disproves preservation of resolutivity by zero extension from a cut domain to the original domain. The stated conditional transfer lemma is valid with its two additional assumptions. Neither result proves or disproves B-regular localization. The example has zero artificial-boundary data and does not depend on a defect at the point being localized.

**Qualify the original executable.** Its ordinary-mode successful output is reproducible, but every test is an `assert`, so optimized Python removes the tests. The original executable incorrectly reports success on controlled failing inputs under `-O`. A separately frozen derivative replaces assertions with explicit runtime checks. No mathematical text, formula, expected numerical value, or status is changed.

**Keep present-day literature status unverified and novelty unclaimed.** Gauthier's directly relevant 2010 chapter has still not been inspected in full. No assertion about its mathematical outcome follows from its title or the 2018 problem-list update.

## Exact object and identity review

The audit checked the complete immutable author ZIP, its external manifest, every member, the internal manifest, and the unpacked author directory against one another. The ZIP has exactly nine distinct flat-path members. CRC and every recorded byte count and SHA-256 match. The author external manifest itself is independently pinned in `ACCEPTANCE.json`.

The three complete supplied datasets were hashed in their entirety. Their exact ID 2303033 record and complete problem-number report were read. The complete pair was reserialized with `json.dumps([complete_record, report], sort_keys=True)`, using default separators and `ensure_ascii`; its SHA-256 is `4016cb6ecf86977e23fd9acd1e9ae27b38990e955b1c2036083dbc16074b7c09`. The exact statement hash, rank 901, problem number, and inherited gate all agree. The inherited report contains literature triage rather than an earlier substantive mathematical proof or computation. No source corpus contents are included in this audit bundle.

The task retains the full original quantifiers: a bounded open subset of R^n, n >= 2, with no connectedness or boundary regularity assumption, and all resolutive data bounded near the specified boundary point. The result proved is deliberately narrower and does not silently replace those hypotheses.

## Geometry, branch, and boundary assignment

Let a = (1 + i sqrt(3))/2 and b = conjugate(a). Both circles meet exactly at a and b. At a their inward half-planes have an intersection angle 2 pi/3; the same holds at b. Thus the exponent needed to straighten the corner is pi/(2 pi/3) = 3/2, not 2/3.

The fractional-linear map T(z) = (z-a)/(z-b) is injective on the sphere and takes the two supporting circles to lines through 0 and infinity. At the midpoint of the original boundary arc, z=1, T(1)=exp(-2 pi i/3), so its argument on the sector-side determination is 4 pi/3. At the midpoint of the artificial arc, z=0, T(0)=exp(2 pi i/3). At the interior point z0=1/2, T(z0)=-1. These values identify the selected angle as 2 pi/3 < arg T < 4 pi/3, rather than the complementary angle.

Consequently W=exp(-2 pi i/3)T maps the lens bijectively onto 0 < arg W < 2 pi/3. On this branch F=W^(3/2) maps it conformally onto the upper half-plane. Direct exact substitution gives F(1/2)=i, F(1)=-1, F(0)=1, a maps to 0, and b maps to infinity. The original arc maps to the negative real axis, the artificial arc to the positive real axis. The signs, inverse exponent, endpoint assignments, and branch used by the numerical diagnostic are consistent with the analytic argument.

These are exact geometric facts. Checking 12,275 numerical interior points is useful only as a diagnostic and is not used to infer conformality or surjectivity.

## Density and integrability

For an interior point of the original arc, set s=|z-a| and d=|z-b|. Differentiation yields

- |W| = s/d;
- |W'| = |a-b|/d^2 = sqrt(3)/d^2;
- |F'| = (3/2)|W|^(1/2)|W'|.

Pulling the Poisson density at i back through F gives

q_D(z) = (3 sqrt(3)/(2 pi)) s^(1/2) / (d^(5/2)(1+(s/d)^3)).

Since d tends to sqrt(3), q_D/s^(1/2) tends to 3^(1/4)/(2 pi), a strictly positive finite constant. Both the power and coefficient in the frozen proof are correct. Along the unit circle, ds/dt tends to 1 as arclength t tends to 0, so replacing arclength by s does not change integrability.

The set A is a short open portion of the inherited circle arc ending at, but excluding, a. For f=s^(-5/4) on A and zero elsewhere, the cut-domain integrand is comparable to s^(-3/4), which is integrable. In the disk, harmonic measure at 0 is constant arclength density and the integrand is comparable to s^(-5/4), which is not integrable. At any other fixed disk pole the Poisson density has a strictly positive lower bound on the compact circle; divergence therefore persists. All inequalities needed here are asymptotic comparabilities on a sufficiently short arc, not claims of global equivalence.

## Perron resolutivity, the corner, and nonnegative data

The proof does not confuse a finite harmonic integral with a pointwise continuous Dirichlet solution. The lens is a Jordan domain, and the usual PWB representation identifies harmonic-measure-integrable Borel data with finite resolutive data. Integrability at one interior pole implies integrability at every interior pole by Harnack comparison. The data are unbounded as the corner is approached along the inherited arc, but the assigned value at the corner is 0. That assignment does not create a problem: each boundary singleton has harmonic measure zero in the lens and the disk.

There is also a direct Perron justification for these particular nonnegative data. Both f and its disk zero extension g are lower semicontinuous on their entire boundaries. They are continuous on A and on the interior of its complement; at the cutoff and the corner the assigned value is 0 and every nearby value is nonnegative. On a compact metric boundary a nonnegative lower semicontinuous function is the increasing pointwise limit of bounded nonnegative continuous functions. Their harmonic solutions belong to the lower Perron class, and monotone convergence identifies their increasing limit with the Poisson integral.

For f the Poisson integral U is finite and harmonic. At a point of A, f is continuous in a boundary neighborhood, and the nonnegative Poisson integral has lower boundary limit at least f. Outside A the required lower limit is merely 0, satisfied by positivity. Thus U belongs to the upper Perron class. The continuous approximants give lower Perron solution at least U, while this upper-class membership gives upper Perron solution at most U. Comparison yields equality and finite resolutivity.

For g, the same continuous-approximation argument forces its lower Perron solution to be +infinity at every interior pole. Hence no finite PWB solution exists. This establishes the claimed nonresolutivity under the finite-solution convention used in the problem. It does not rest on cancellation of signed data or on any convention allowing identically infinite solutions to count as resolutive.

The support of f satisfies |z-y|>3/4 because |a-y|=1 and |z-a|<1/4. Therefore f vanishes in a neighborhood of y and is exactly zero on the artificial open arc. No infinite datum is imposed at y or at a.

## Conditional transfer lemma

For any bounded open Omega and D=Omega intersect B(y,r), the sets Gamma=boundary(D) intersect boundary(Omega) and Sigma=boundary(D) intersect Omega partition boundary(D). This remains true without connectedness assumptions.

Assuming the stated zero extension g is resolutive, the PWB restriction property supplies resolutive cut-boundary data F equal to g on Gamma and H_g on Sigma, with H_F on D equal to the restriction of H_g. Nonnegativity gives H_g>=0. On Gamma, f=F; on Sigma, f<=M<=M+F. Comparison and the finite constant-shift property give 0<=H_f<=M+H_g on D. For sufficiently small neighborhoods of y, the cut and original boundaries coincide; thus g is bounded near y. B-regularity of Omega applies to this g and gives one global neighborhood bound for H_g. The same bound works across every cut component. No unproved uniformity of component-specific constants is used.

This proves the lemma exactly as stated. It cannot be applied to arbitrary cut-boundary data, because neither boundedness on all of Sigma nor resolutivity of the zero extension is supplied by the localization question. The lens example defeats the second assumption even when the first holds with M=0.

## Why this is not a counterexample to localization

The disk is B-regular at y: near y, separate any integrable datum into its bounded nearby part and its integrable part supported away from y; disk Poisson kernels are uniformly bounded on the latter support. The cut lens is Lipschitz, and Sadi's local B-regularity discussion covers this class. More specifically, the constructed solution even tends to 0 at y. Its mapped support is a bounded interval of the negative real axis close to 0 and separated from F(y)=-1; the relevant Poisson kernels tend to 0 and are dominated by a constant multiple of the integrable reference kernel at i.

Thus the obstruction is to the proposed extension step, not to the desired regularity property. The stated remaining difficulty concerning cut-domain harmonic-measure domination is real, and arbitrary cut domains may have infinitely many components.

## Source review and limits

The locally supplied complete PDFs were checked against their published-source hashes. Sadi's definitions, nonnegative-data criterion, connected-domain harmonic-measure criterion, restriction property, and local examples were read. Images of printed pages 103 and 116 were visually inspected: page 103 has N>=2, resolving the OCR ambiguity; page 116 states the restriction formula and the converse question. These source observations support the uses made in the proof. The restriction property is a standard PWB fact, not a new theorem claimed by this package.

Hayman and Lingham's 2018 version 2 statement and update were checked. Its historical report does not certify status in 2026. Bibliographic and bounded public searches again identified Gauthier's 2010 chapter. The DOI route and a Google Books page-211 preview were inaccessible to the web reader; a lawful publisher front-matter scan hosted by ETH confirms the title, author, and start page but contains no chapter text. No authentication, CAPTCHA, payment, or denied-access workaround was attempted. The chapter remains an unresolved source lead. Earlier bounded GitHub-search results are preserved as historical author metadata, not promoted to a fresh exhaustive audit.

Sources:

- Amar Sadi, *Some types of regularity for the Dirichlet problem*, Nagoya Mathematical Journal 126 (1992), 103-124. https://doi.org/10.1017/S0027763000004013
- Walter K. Hayman and Eleanor F. Lingham, *Research Problems in Function Theory*, arXiv:1809.07200v2. https://arxiv.org/abs/1809.07200v2
- Paul M. Gauthier, *Whether regularity is local for the generalized Dirichlet problem*, CRM Proceedings and Lecture Notes 51 (2010), 211-214. Full text uninspected. https://doi.org/10.1090/crmp/051/16
- Publisher front matter and contents only: https://toc.library.ethz.ch/objects/pdf/e01_978-0-8218-4879-1_01.pdf

## Executable correction and acceptance boundary

The original diagnostic reproduces its stored JSON in ordinary and optimized modes, including 12,275 sampled points and maximum inverse error about 5.24e-16. However, changing `full_solution` to true or replacing a test with `assert False` causes ordinary execution to fail while optimized execution still prints `result: pass`. Optimized success is therefore not evidence that the original checks ran.

The corrected derivative replaces all 13 assertions by explicit `require` calls that raise on failure, and updates only the corresponding internal manifest entry. The derivative is separately hashed. Its original numerical output is unchanged. Isolated relocation replay in ordinary and optimized modes, plus status, rotation, exponent, density-factor, and forced-failure negative controls, is recorded in `REPLAY_RESULTS.json`. Neither the corrected executable nor this audit claims that finite diagnostics prove the analytic argument or the unresolved converse.

Final accepted disposition: **stalled partial, 2/5; rigorous zero-extension obstruction and conditional transfer lemma; no full solution, no localization counterexample, no novelty claim, current literature status unverified.** No publication, queue write, third-party-source copying, or private-source sharing was performed by this audit.
