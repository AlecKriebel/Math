# Indirect deduction from established compact-condensor and Sobolev theory

This deduction was assembled independently in this audit on 17 October 2026. It is **not** represented as a theorem explicitly printed in an earlier source, nor as a priority claim. It supplies a checkable indirect-overlap test for the exact target without using the submitted proof's lower-semicontinuous density majorant, weighted path-distance construction, or small-circle argument.

## Imported results and their inspected scope

1. Hesse, *A p-extremal length and p-capacity equality*, Arkiv för Matematik 13 (1975), 131–144, Definition 3.2 and Theorem 5.5: for disjoint nonempty compact plates inside a domain, the all-locally-rectifiable-curve modulus equals the infimum of the gradient energy of continuous ACL potentials with the prescribed plate values. The scan's pp. 132 and 140–143 were inspected; Definition 3.1 allows extended nonnegative Borel densities. DOI: https://doi.org/10.1007/BF02386202. No assertion about touching or noncompact plates is imported.
2. Di Nezza–Palatucci–Valdinoci, arXiv:1104.4345v3 (19 November 2011), Propositions 3.4 and 3.8: the flat trace of a planar W^{1,2} function belongs to H^{1/2}(R), with continuous trace map. These statements and their surrounding proof were inspected. https://arxiv.org/abs/1104.4345.
3. Brezis, *How to recognize constant functions. Connections with Sobolev spaces* (2002), Corollary 1 and Remark 3: an integer-valued critical fractional Sobolev function is constant almost everywhere on a connected open set. The author-hosted body was inspected. https://sites.math.rutgers.edu/~brezis/PUBlications/180.pdf.
4. Diening–Harjulehto–Hästö–Růžička, author-hosted monograph draft dated 3 December 2010, Lemma 11.1.2, Lemma 11.1.4(a), and Corollary 11.2.5: strong convergence of continuous Sobolev functions has a subsequence converging quasi-everywhere; quasicontinuous representatives equal almost everywhere agree quasi-everywhere; zero-boundary Sobolev functions have zero extensions vanishing quasi-everywhere outside the domain. All are specialized to constant exponent 2. The draft's printed pp. 334–341 were inspected. Publisher metadata authenticates the related 2011 book, but the publisher's final theorem numbering/pages were not body-matched. https://www.math.lmu.de/~diening/archive/book.pdf; https://doi.org/10.1007/978-3-642-18363-8.
5. Hunter's 2009 half-space notes, Theorem 3.42, identify the kernel of the half-space trace with W^{1,2}_0. The body was inspected; a displayed k in the theorem is read in the explicitly discussed first-order case k=1. https://www.math.ucdavis.edu/~hunter/m218a_09/ch3.pdf. Alternatively the elementary cutoff proof of the standard first-order zero-trace result suffices.

Here C_2 denotes the inhomogeneous Euclidean Sobolev capacity. Quasi-everywhere always refers to this capacity. The passage to conformal curve modulus is justified explicitly below; logarithmic-capacity equivalence is not assumed.

## Exact hypothesis

Let E be a nonempty compact subset of [0,1], F=R\E within the real axis, and let rho:R^2->[0,infinity] be Borel, square integrable, and admissible for **every** E-to-F connector in the chosen convention. We allow either all globally rectifiable connectors, or all continuous connectors locally rectifiable away from their endpoints. We prove that the modulus of the corresponding entire E-to-S_2 family is zero.

## 1. Exhaust only the second plate

Put Q=(-2,3)x(-2,2), and for j>=2 set

    F_j = { (x,0): -2+1/j <= x <= 3-1/j, dist(x,E)>=1/j }.

Each F_j is nonempty, compact, contained in Q, and disjoint from E. They increase and exhaust (R\E) intersected with Q. The first plate remains the same compact E.

Hesse's curve convention uses curves on an open parameter interval whose **image closure** meets both plates. To connect it carefully with either target convention, take rho_epsilon=(rho+epsilon*1_Q)1_Q. Every locally rectifiable Hesse curve in Q with infinite Euclidean length has infinite rho_epsilon-length. Any such curve with finite Euclidean length extends continuously to a compact rectifiable curve. Its compact image meets both plates, so it contains a rectifiable subconnector from E to F_j. That subconnector is in the target E-to-F family, and its rho-integral is at least 1. Thus rho_epsilon is admissible for Hesse's full family. Endpoint values of an infinite density contribute zero arclength and cause no exception.

Letting epsilon decrease to zero gives

    M_Hesse(E,F_j;Q) <= integral_Q rho^2 <= C,
    C = integral_R^2 rho^2 < infinity.

Hesse Theorem 5.5 therefore gives continuous ACL functions u_j on Q, with u_j=0 on E, u_j=1 on F_j, and integral_Q |grad u_j|^2 <= C+1. Truncation gives 0<=u_j<=1 without increasing energy. Bounded ACL functions with square-integrable first partial derivatives belong to W^{1,2}(Q).

Choose a smooth compactly supported eta in Q, 0<=eta<=1, equal to 1 near E. Define w_j=eta(1-u_j), extended by zero outside Q. These are continuous compactly supported W^{1,2}(R^2) functions, uniformly bounded in that space; all satisfy w_j=1 on E, and w_j=0 on F_j. Their supports lie in the same fixed compact set K contained in Q.

## 2. Retain the plate values by strong tail convexification

Reflexivity gives a weakly convergent subsequence. Mazur's lemma gives convex combinations v_n of its tails, converging strongly in W^{1,2}(R^2) to w. The least original index in each tail tends to infinity. Consequently v_n=1 on E for every n, and for each fixed k, v_n=0 on F_k for all sufficiently large n. Also 0<=v_n<=1 and supp v_n is contained in K.

The quasi-everywhere subsequence theorem for these continuous v_n gives a quasicontinuous representative w* of w and a C_2-null set N such that a subsequence converges to w* at every point outside N. In particular,

    w*=1 on E\N;   w*=0 on (F intersect Q)\N.

There is no assertion that arbitrary almost-everywhere representatives preserve these values. This is precisely the capacity-sensitive content of the strong convergence step.

## 3. Identify the ordinary trace and use critical rigidity

For every real x outside E, either (x,0) lies outside K, where all v_n vanish, or it belongs to some F_k, where the v_n eventually vanish. On E all v_n equal 1. Thus v_n(x,0) converges **pointwise on the entire real line** to 1_E(x). Boundedness and common compact support give convergence in L^2(R).

For continuous Sobolev v_n their restrictions to the line give their ordinary traces almost everywhere. The continuous flat trace operator and strong W^{1,2} convergence therefore identify Tw=1_E in L^2(R). The trace belongs to H^{1/2}(R). Brezis's critical integer-valued rigidity makes 1_E constant almost everywhere; its compact support forces the constant to be zero. Hence |E|=0 and Tw=0.

This conclusion alone would not settle the target. A zero-length compact set can still have positive conformal capacity.

## 4. Use the zero-trace theorem at the level of capacity

The restrictions of w to the upper and lower half-planes have zero ordinary trace. The half-space trace-kernel theorem places them in W^{1,2}_0 of the respective half-planes. The zero-extension theorem gives quasicontinuous functions w_+ and w_- on the whole plane agreeing almost everywhere with these restrictions and vanishing quasi-everywhere outside their respective half-planes.

Their sum agrees with w almost everywhere in the plane and vanishes quasi-everywhere on the real line. It is quasicontinuous. Uniqueness of quasicontinuous representatives then gives

    w*=w_++w_- quasi-everywhere in R^2,
    w*=0 quasi-everywhere on R.

But w*=1 quasi-everywhere on E by Step 2. Therefore C_2(E)=0. This step includes all zero-length positive-capacity candidates and makes no continuum or interval assumption on E.

## 5. Return to all-curves modulus without an exceptional-curve shortcut

By the definition of C_2(E)=0, choose nonnegative h_m in W^{1,2}(R^2), at least 1 almost everywhere on an open neighborhood O_m of E, with norm tending to zero. Fix a smooth cutoff xi equal to 1 near E and supported in B(0,3/2). Multiplication preserves convergence to zero in W^{1,2}. Mollify xi*h_m at a positive radius small enough that every convolution ball centered in E lies inside O_m and the region where xi=1, and small enough to keep the support inside B(0,7/4). This yields smooth compactly supported phi_m with

    phi_m>=1 on E;   phi_m=0 on S_2;
    integral |grad phi_m|^2 -> 0.

For every globally rectifiable E-to-S_2 connector the fundamental theorem along the curve gives integral_gamma |grad phi_m| ds >=1. For a connector only locally rectifiable off the endpoints, apply the same inequality on compact interior subcurves and let the endpoints tend to those of the full curve. Continuity of phi_m and of the curve gives the same lower bound by monotone convergence of the nonnegative line integrals. Thus |grad phi_m| is admissible for **every** target connector in either convention.

The entire E-to-S_2 family consequently has modulus zero. This proves the contrapositive of the exact target. Empty E is immediate.

## Audit conclusion and limitation

The compact exhaustion closes the precise noncompact-plate gap in a naive application of Hesse. Strong convergence and the zero-boundary theorem close the precise null-length gap in a trace-only argument. The all-curves bridges are explicit at both ends. No central difficulty is transferred to an unsupported touching-plate identity.

This establishes a complete indirect deduction from inspected earlier general theory. It does not establish that an earlier author wrote this combination, recognized the implication for Problem 7.58, or published this exact theorem. Nor does it establish an oldest source. The source-body/dating scope of the monograph draft is retained above.
