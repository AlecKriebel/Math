# Analytic zero, convergence, and boundary adversarial audit

## Verdict and exact claim

**PASS_ALL_REAL_ALPHA_SUFFICIENT_CONDITION.** The immutable candidate proves its stated sufficient condition for every finite real alpha, including the non-strict coefficient budget. Its restricted one-parameter sharpness claim for 0<alpha<=1 also passes. No mandatory mathematical correction is identified. This verdict does not establish novelty, priority, a necessary condition, or a globally optimal coefficient region.

The audited head is `6a865c574586d08e6fa185b09ebe746122457ff0`, problem 2306064 / AMR-022-6064 / Hayman-Miller 6.64. The candidate SHA-256 is `8ee69b778f281333c6a09850ed03de02f7d936174ab467e0899ca47799a2f4e7`. All 17 authenticated original files have been hashed and match the immutable authentication record, with sizes recorded in INPUT_AUTHENTICATION.json.

For each real alpha, set

    a=|1-alpha|, b=|alpha|, d=a+2b-1,
    k=(d+sqrt(d^2+8b))/4,
    w_n=n[1+k(n-1)] (n>=2).

The exact hypothesis is that f is analytic in the open unit disk, normalized by f(0)=0 and f'(0)=1, with Taylor coefficients a_n, and

    T=sum_(n>=2) w_n |a_n| <= 1.

The required conclusion is that the removable product (f/z)f' has no zero in the disk and

    Re J_alpha[f](z)>0,
    J_alpha[f]=(1-alpha) zf'/f + alpha(1+zf''/f').

The quantifier is a valid parameter-dependent criterion for each alpha. It does not assert that one nonidentity function passes these weights simultaneously for all alpha. The same letter a in the scalar reduction is distinct from the Taylor coefficients a_n.

## Source scope and attribution

The [2018 Hayman-Lingham source](https://arxiv.org/pdf/1809.07200), Problem 6.64, printed 141 / PDF 142, was read completely and checked visually. It uses real alpha, the normalized analytic class and nonzero product, and asks for a sufficient coefficient generalization. Neither necessity nor global optimality is prescribed. The user-supplied 2019 edition, printed 162 / PDF 167, preserves this scope; the nonzero sign was checked in the rendered page because extracted glyphs were unreliable. Both editions' historical update supplies no 2026 priority certificate.

The complete [Kumar-Ravichandran article (2017)](https://mjms.upm.edu.my/fullpaper/2017-September-11-3/Kumar,%20S.-365-375.pdf) was read independently. Its alpha-convex Theorem 2.1 has 0<=alpha<=1 and radii under coefficient envelopes; the proof's printed 368 / PDF 4 two-denominator majorant was checked visually. Thus the candidate correctly credits that mechanism. The paper's separate arbitrary-beta derivative results concern a different expression and do not supply the audited all-real-alpha criterion. No broader literature claim is inferred here.

Source PDFs and rendered pages are private or ignored. This public audit contains mathematical derivations and brief paraphrases with primary locators, not reproduced source pages. Source hashes and sizes are recorded in INPUT_AUTHENTICATION.json.

## Independent disk-local proof, including equality

This argument verifies the central implication directly on each interior circle, rather than importing the original checker or relying on closure of alpha-convex classes under limits.

First, k(0)=0. If alpha is nonzero, b>0, d>0, and k is the unique positive root of

    2k^2-dk-b=0.

Indeed, d=alpha on [0,1], d=-3alpha on alpha<0, and d=3alpha-2 on alpha>1. The other quadratic root is negative. Rearranging the positive-root identity gives

    a/(1+2k)+b/k=1.                                      (A)

Fix 0<r<1. Define nonnegative disk-local sums

    A_r=sum |a_n| r^(n-1),
    B_r=sum n|a_n| r^(n-1),
    X_r=B_r-A_r=sum (n-1)|a_n| r^(n-1),
    Y_r=sum n(n-1)|a_n| r^(n-1).

Let T_r=sum w_n|a_n|r^(n-1). Since n>=2 and r^(n-1)<=r,

    T_r <= rT <= r <1.                                   (B)

At alpha=0, interpret T_r as B_r and do not introduce kY_r as a global 0 times infinity. At alpha nonzero, T_r=B_r+kY_r, with Y_r finite. In either case B_r<=T_r<1 and A_r<=B_r/2. Therefore, for |z|=r,

    |f(z)/z-1|<=A_r<1,
    |f'(z)-1|<=B_r<1.                                    (C)

Both denominator factors are nonzero at every nonzero disk point. At zero their analytic continuations are 1, so the removable product has value 1 and is nonzero there as well. More strongly, Re f'(z)>=1-B_r>0. Thus no univalence presumption or separate zero exclusion is hidden in the proof.

The analytic Taylor identities are

    zf'/f-1 = [sum (n-1)a_n z^(n-1)]/[1+sum a_n z^(n-1)],
    zf''/f' = [sum n(n-1)a_n z^(n-1)]/[1+sum n a_n z^(n-1)].

The triangle inequality, with the positive lower denominator bounds from (C), gives

    |zf'/f-1|<=X_r/(1-A_r),
    |zf''/f'|<=Y_r/(1-B_r).                              (D)

For alpha=0, B_r<1 implies

    X_r/(1-A_r)=(B_r-A_r)/(1-A_r)<1.

The second bound is not needed. Hence |J_0-1|<1.

For alpha nonzero, put D_r=1-B_r. Equation (B) gives D_r>kY_r. Coefficientwise n(n-1)>=2(n-1), hence Y_r>=2X_r. If f is not the identity, every fixed r>0 has X_r,Y_r>0. Consequently,

    D_r>kY_r>=2kX_r,
    X_r/(1-A_r)=X_r/(D_r+X_r)<1/(1+2k),
    Y_r/(1-B_r)=Y_r/D_r<1/k.

The decomposition J_alpha-1=(1-alpha)(zf'/f-1)+alpha zf''/f', equations (D), and (A) imply

    |J_alpha-1|
      <=a X_r/(1-A_r)+b Y_r/(1-B_r)
      <a/(1+2k)+b/k=1.

Strictness remains valid at alpha=1, where a=0, because b>0 and the second inequality is strict. At other nonzero alpha b remains positive. For the identity f=z, or at z=0 for any normalized admissible f, J_alpha=1 directly. Finally Re J_alpha>=1-|J_alpha-1|>0. This proves the exact claim, including T=1, arbitrary complex coefficient phases, every negative alpha, and every finite alpha>1.

## Infinite sums and analyticity

All manipulations above are valid for genuinely infinite Taylor series. At nonzero alpha, the budget yields

    B=sum n|a_n|<=1,
    kY=k sum n(n-1)|a_n|<=1,

so Y is finite. Then A, X, B, and Y converge absolutely, and their disk-local variants are justified termwise by nonnegative convergence and by the analytic derivative series.

At alpha=0 the budget guarantees B finite, hence A and X finite, but does not guarantee Y finite. This is correctly separated in the candidate. Even then f'' exists inside the disk by analyticity, and Y_r is finite for r<1 because sup_(n>=2) (n-1)r^(n-1) is finite and B is finite. The alpha=0 proof needs neither Y nor Y_r.

A concrete edge case is

    a_n=-1/[n^2(n-1)] (n>=2).

Its radius of convergence is 1. Its first weighted moment is

    B=sum 1/[n(n-1)]=1,

by telescoping, whereas its second moment is

    Y=sum 1/n=+infinity.

It satisfies the alpha=0 equality hypothesis and is covered by the preceding proof. For any nonzero alpha its weighted sum diverges, so it is outside that parameter's hypothesis. This change in the admissible coefficient class near alpha=0 is a real boundary phenomenon, not a failure of the theorem. No boundary regularity of f'' is required.

## Rescaling audit and limits of the conclusion

The candidate's alternative equality argument is also sound. For 0<R<1, the coefficients of f_R(z)=f(Rz)/R are a_n R^(n-1), and

    sum w_n|a_n|R^(n-1)<=RT<1.

Thus the strict theorem applies even without an identity exception. Its exact identities are

    f_R'(z)=f'(Rz), f_R''(z)=R f''(Rz),
    (f_R(z)/z)f_R'(z)=[f(Rz)/(Rz)]f'(Rz),
    J_alpha[f_R](z)=J_alpha[f](Rz).

For any original point w choose |w|<R<1 and set z=w/R. This transfers strict positivity and nonvanishing to w. It does not take a boundary limit and assume that a positive real part remains strictly positive there.

One must preserve the open-disk scope. At alpha=0, f=z-z^2/2 has coefficient budget 1 and

    J_0(r)=(1-r)/(1-r/2)>0 for 0<=r<1,

but J_0(r) tends to zero as r tends to 1. Its derivative vanishes at the boundary point 1. At alpha=1, f=z-z^2/4 also has budget 1 and the same expression for J_1(r), tending to zero at that boundary. Thus no positive global margin or strictly positive unit-circle conclusion follows. The source and candidate require neither.

## Parameter edge cases

The unified root gives exactly k(0)=0 and k(1)=1. For 0<=alpha<=1 it reduces to the displayed candidate formula, for alpha<0 to its negative-parameter formula, and for alpha>1 to its large-parameter formula. All weights are positive. The scalar mechanism uses absolute values of both multipliers, so it makes no convex-combination assumption outside [0,1].

As alpha approaches zero from either side, k tends to zero with leading order sqrt(|alpha|/2). The proof never divides by k at alpha=0. At alpha=1, k is continuous and equals 1, though the one-sided derivatives differ; no differentiability in alpha is needed.

For every nonzero alpha, d>0, and the root relation also gives

    d/2 < k < d/2+b/d.

Thus k is finite and positive for every finite alpha and grows linearly at either real infinity. Nothing in the proof is restricted to a bounded interval of parameters. “Every real alpha” includes arbitrarily large finite parameters, not an additional alpha=infinity class.

## Restricted sharpness and the interpolation counterexample

For f_c(z)=z-cz^2, 0<c<1/2, both f_c/z=1-cz and f_c'=1-2cz are nonzero in the disk. Setting x=cz gives the exact identity

    J_alpha[f_c](z)=[1-(4+alpha)x+4x^2]/[(1-x)(1-2x)].       (E)

For 0<alpha<=1, k satisfies 2k^2=alpha(k+1). Hence c_*=1/[2(1+k)] lies in (0,1/2) and makes the numerator of (E) zero. Its derivative is 8x-(4+alpha)<0 for 0<=x<1/2, so the numerator is negative for c_*<x<1/2.

For any 0<=lambda<k,

    c_* < min(1/2,1/[2(1+lambda)]).

Choose c strictly between these values and choose real z with c_*/c<z<1. The weaker coefficient sum is 2(1+lambda)c<1, while the numerator in (E) is negative and its denominator positive. Therefore Re J_alpha[f_c](z)<0 at an interior point. This establishes exactly the candidate's sharpness in the nonnegative one-parameter weight family, with no optimality assertion outside its stated interval or for different coefficient weights.

The explicit alpha=1/2, c=8/25, z=31/32 witness has naive affine-weight budget 24/25 and J=-53/1311. The naive linear interpolation is therefore false even with both analytic denominators nonzero. The corrected root parameter is mathematically material.

## Independence, controls, and remaining gap

INITIAL_ANALYTIC_CONCLUSION.md was frozen at 2026-10-06T22:42:03.074592Z, actual PID 51215, SHA-256 `96435b2e3ebc60dcd37e06a8089e4f38cfba47edad3b0001c1b011180bfabdfb`, before opening the original REVIEW, original checkers, or another family's report. The original REVIEW was subsequently read for reconciliation and agrees with the frozen conclusion. Original checker code was neither read nor imported nor executed. No other family's report was read.

The independently written exact_controls.py passed 205 small exact rational assertions, recorded with actual PID and UTC in EXACT_CONTROLS.json. These controls cover the scalar root relation on the negative, middle, and above-one parameter families; coefficient identities; sharpness witnesses near zero; endpoint boundary examples; the naive-interpolation witness; and the telescoping first moment. Their role is supplementary algebra verification. The all-function analytic conclusion is established by the proof above, not finite sampling.

Strongest verified result: the stated sufficient criterion and the explicitly restricted sharpness theorem are correct with the exact source assumptions and open-disk conclusion. Exact remaining mathematical gap within that claim: none found. Exact gap before any priority or first-resolution promotion: novelty is not established by this audit, and the known majorant method must remain credited. The parent is responsible for subsequent priority investigation and any publication decision after the mathematics gate.

Original research accounting remains the authenticated 1/5 attempt with substantive_approaches=1. This audit consumes no new central proof-search turn and invents no historical ledger. All writes are confined to this audit's folder; no PR, branch, Git, native-sheet, publication, or external outreach action was performed.
