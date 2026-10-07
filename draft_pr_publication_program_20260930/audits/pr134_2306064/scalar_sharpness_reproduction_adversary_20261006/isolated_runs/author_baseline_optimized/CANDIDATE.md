# An explicit coefficient-sum test for every real alpha

**Target:** 2306064 / AMR-022-6064, Hayman Problem 6.64 (S. Miller).  
**Status:** complete candidate sufficient-condition answer to the literal question; separate adversarial review pending.  
**Scope:** normalized analytic functions on the unit disk; every real alpha. No novelty or human peer-review claim.

## 1. Exact source and prior method

The full [2018 source](https://arxiv.org/abs/1809.07200), printed p. 141 (PDF p. 142), asks for a generalization of the coefficient-sum sufficient conditions for starlikeness and convexity that guarantees membership in Miller's alpha-convex class. It allows every real alpha, and does not demand a necessary-and-sufficient characterization or a globally optimal coefficient region. Its adjacent update reports no progress communicated to the editors; that historical remark is not a current novelty certificate.

For a normalized analytic function

    f(z)=z+sum_(n>=2) a_n z^n,

write

    J_alpha[f](z)=(1−alpha) zf'(z)/f(z)
                     +alpha [1+zf''(z)/f'(z)].

Membership in M_alpha means f(z)f'(z)/z never vanishes and Re J_alpha[f](z)>0 throughout the open unit disk, with the removable expressions at zero defined by their limits. The source's endpoint conditions are sum n|a_n|<1 at alpha=0 and sum n²|a_n|<1 at alpha=1.

The principal majorization estimate used below is classical: [Kumar–Ravichandran (2017), proof of Theorem 2.1, printed p. 368](https://mjms.upm.edu.my/fullpaper/2017-September-11-3/Kumar,%20S.-365-375.pdf) explicitly displays its two-denominator form for 0<=alpha<=1, and uses it for sharp radius results under coefficient envelopes. We credit that estimate and method. The extension using absolute values for arbitrary real alpha and the particular one-parameter sufficient bound below are proved directly. Priority for these consequences is not asserted.

## 2. One explicit weighted sum, including all real alpha

For real alpha define

    a=|1−alpha|,       b=|alpha|,
    d=a+2b−1,
    kappa(alpha)=[d+sqrt(d²+8b)]/4.                         (1)

Then kappa(0)=0, and kappa(alpha)>0 when alpha is nonzero.

**Theorem 1.** If

    sum_(n>=2) n[1+kappa(alpha)(n−1)] |a_n| <= 1,           (2)

then f belongs to M_alpha. In particular the strict version of (2) is a sufficient-condition answer to the source. The condition also guarantees the required nonvanishing, so that hypothesis need not be assumed separately.

At alpha=0, kappa=0 and (2) is exactly the starlike coefficient weight n. At alpha=1, kappa=1 and it is exactly the convex coefficient weight n². For 0<=alpha<=1 the formula simplifies to

    kappa(alpha)=[alpha+sqrt(alpha²+8alpha)]/4.             (3)

For alpha<0 it is [−3alpha+sqrt(9alpha²−8alpha)]/4, and for alpha>1 it is [3alpha−2+sqrt((3alpha−2)²+8alpha)]/4. Formula (1) handles all cases without interpreting a potentially negative coefficient weight.

### Proof

First suppose the left side of (2) is strictly less than one. Put

    A=sum |a_n|,       B=sum n|a_n|,
    X=B−A=sum (n−1)|a_n|,
    Y=sum n(n−1)|a_n|.

If alpha is nonzero, kappa>0 and (2) makes all four sums finite. If alpha=0 only A, B and X are required; no assumption of a finite second moment is made. In either case B<1 and A<=B/2, so

    |f(z)/z−1|<=A<1,       |f'(z)−1|<=B<1.

Thus f/z and f' are nonzero throughout the disk. For |z|<1, the numerator series give

    |zf'/f−1| <= X/(1−A),
    |zf''/f'| <= Y/(1−B),                                 (4)

where the second estimate is used only if alpha is nonzero. These follow from the triangle inequality and termwise differentiation of the analytic series; convergence of the corresponding coefficient sums justifies the displayed uniform bounds.

If alpha=0, (4) immediately gives

    |J_0[f]−1| <= (B−A)/(1−A)<1,

proving the claim. Now suppose alpha is nonzero and write k=kappa(alpha), D=1−B. The hypothesis is B+kY<1. Also

    Y>=2X>=0,       D>kY>=2kX.

If f is the identity there is nothing to prove. Otherwise X,Y>0 and

    X/(1−A)=X/(D+X)<1/(1+2k),       Y/D<1/k.

Formula (1) says exactly that k is the positive root of

    2k²−(a+2b−1)k−b=0,

or, equivalently,

    a/(1+2k)+b/k=1.                                       (5)

Using (4), the absolute values of the two real multipliers, and b>0, we obtain

    |J_alpha[f]−1|
      <= a X/(1−A)+b Y/(1−B)
      < a/(1+2k)+b/k = 1.

Hence Re J_alpha[f]>0. This proves the strict case for every real alpha.

For the non-strict hypothesis in (2), fix 0<R<1 and apply the strict result to f_R(z)=f(Rz)/R. Unless f is the identity, its weighted coefficient sum is strictly smaller than one because every nonzero term acquires R^(n−1)<1. Thus f_R belongs to M_alpha. Given any w in the original disk, choose |w|<R<1 and use J_alpha[f_R](w/R)=J_alpha[f](w), with the identical rescaling of the nonvanishing conditions. This proves (2), including boundary equality. QED.

## 3. Sharpness within this interpolation family

The theorem is not a necessary condition for all alpha-convex functions. The following sharpness assertion is restricted to the stated one-parameter weights.

**Theorem 2.** Fix 0<alpha<=1. Among conditions of the form

    sum_(n>=2) n[1+lambda(n−1)]|a_n|<1,
    with lambda>=0,

the constant lambda=kappa(alpha) in (3) cannot be decreased while keeping the implication for every normalized analytic f with f f'/z nonzero. No optimality claim is made for alpha outside [0,1], or for other systems of coefficient weights.

### Proof

Let k=kappa(alpha), and put c_*=1/[2(1+k)]. For f_c(z)=z−c z², where 0<c<1/2, both f_c/z and f_c' are nonzero in the disk. With x=cz,

    J_alpha[f_c](z)
      = [1−(4+alpha)x+4x²]/[(1−x)(1−2x)].                 (6)

The relation 2k²−alpha k−alpha=0 shows that the numerator vanishes at x=c_*. Since 0<c_*<1/2 and its derivative 8x−(4+alpha) is negative for 0<=x<1/2, the numerator is negative for c_*<x<1/2.

If 0<=lambda<k, choose

    c_* < c < min(1/2, 1/[2(1+lambda)]).

This interval is nonempty. The coefficient sum with lambda is 2(1+lambda)c<1, but choosing a positive real z with c_*/c<z<1 makes (6) negative. Thus f_c is not alpha-convex. This proves the claimed sharpness. At alpha=0 the admissible family lambda>=0 already has minimal parameter zero. QED.

## 4. Why naive linear interpolation does not work

Replacing kappa(alpha) by alpha gives the tempting weights n[1+alpha(n−1)], interpolating n and n² linearly. For every 0<alpha<1, formula (3) has kappa(alpha)>alpha, and Theorem 2 shows that this weaker proposal fails.

An exact example is

    alpha=1/2,       f(z)=z−(8/25)z².

Its naive weighted sum is 3(8/25)=24/25<1. It satisfies the nonvanishing assumptions, but at z=31/32 one has x=31/100 and

    J_(1/2)[f](31/32)=−53/1311<0.

The conclusion of the theorem therefore depends on its explicit corrected coefficient, not merely on taking an affine average of the endpoint weights.

## 5. Attribution, scope and verification

This is a sufficient-condition answer to the literal generalization request, covering the whole real parameter line and preserving both endpoint tests. The source does not require a unique generalization, a necessary-and-sufficient coefficient characterization, or the optimal admissible region; none is claimed here.

The estimate (4) and coefficient-majorization method have explicit prior precedent in Kumar–Ravichandran. Their paper treats 0<=alpha<=1 and radius questions for prescribed coefficient envelopes. [Noor–Khan–Piejko (2016), Definition 3 and Theorem 1](https://www.etamaths.com/index.php/ijaa/article/view/738/210) also gives coefficient sufficient conditions in a conic-domain family containing the ordinary alpha-convex case on 0<=alpha<=1. Thus coefficient criteria in this area are established prior work. Current related literature also includes [Bravo–Carrasco–Hernández–Venegas (June 2026)](https://arxiv.org/abs/2606.21574), on characterizations and coefficient/Schwarzian bounds for alpha-convex functions. Those are different stated conclusions; none is imported as a theorem needed for this proof. The search does not establish priority for (1)–(3) or their consequences.

The accompanying exact controls check the scalar inequality, parameter identities, coefficient sums and explicit quadratic witness. They do not prove the analytic theorem by sampling; its proof is given above. A separate adversarial review is required before any claimed-result PR.
