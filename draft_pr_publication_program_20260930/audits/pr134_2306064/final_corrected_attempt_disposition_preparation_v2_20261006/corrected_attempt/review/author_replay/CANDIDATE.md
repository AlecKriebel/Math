# An explicit coefficient-sum test for every real alpha

**Target:** 2306064 / AMR-022-6064, Hayman Problem 6.64 (S. Miller).  
**Status:** final-operative-disposition-postimages-preparation_only. Original target already_solved by verified older mathematical consequence; candidate mathematics PASS; alternative polynomial novelty UNRESOLVED. Actual closure/global propagation pending; no publication authorization.  
**Scope:** normalized analytic functions on the unit disk; every real alpha. No novelty or human peer-review claim.

## 1. Exact source and prior method

The full [2018 source](https://arxiv.org/abs/1809.07200), printed p. 141 (PDF p. 142), asks for a generalization of the coefficient-sum sufficient conditions for starlikeness and convexity that guarantees membership in Miller's alpha-convex class. It allows every real alpha, and does not demand a necessary-and-sufficient characterization or a globally optimal coefficient region. Its adjacent update reports no progress communicated to the editors; that historical remark is not a current novelty certificate.

For a normalized analytic function

    f(z)=z+sum_(n>=2) a_n z^n,

write

    J_alpha[f](z)=(1−alpha) zf'(z)/f(z)
                     +alpha [1+zf''(z)/f'(z)].

Membership in M_alpha means f(z)f'(z)/z never vanishes and Re J_alpha[f](z)>0 throughout the open unit disk, with the removable expressions at zero defined by their limits. The source's endpoint conditions are sum n|a_n|<1 at alpha=0 and sum n²|a_n|<1 at alpha=1.

The valid prior mechanism is [Kumar–Ravichandran (2017), proof of Theorem 2.1, printed p. 368](https://mjms.upm.edu.my/fullpaper/2017-September-11-3/Kumar,%20S.-365-375.pdf), which displays the two-denominator absolute-coefficient majorant for 0<=alpha<=1 and applies it to sharp radii under coefficient envelopes. On that interval, the root-weight criterion below follows from the published majorant by the scalar moment reduction in this proof. For arbitrary real alpha, replacing the two multipliers by their absolute values is a direct formal proof adaptation beyond the paper's stated parameter scope. The paper is not credited with an explicit all-real root theorem or an express solution of the named problem. No identical earlier all-real theorem has yet been fully verified; priority remains pending.

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

## 5. Corrected attribution, scope and verification

This corrected postimage preserves the proved theorem and its restricted sharpness statement. The separate 2026-10-06 mathematical/source gate passed after exercise of the explicit-if checker repair. This staging artifact records accepted scientific clearance for the narrow original-target already_solved outcome; it is not human peer review, publication authorization, an alternative-novelty certificate, or a completed closure/global operation.

Kumar–Ravichandran's valid published moment estimate is credited as explained in section 1. The criterion on [0,1] is a consequence of that estimate. The all-real statement is a direct absolute-multiplier adaptation; its elementary dependence does not by itself prove historical resolution or absence of substantive novelty.

[Noor–Khan–Piejko (2016), Alpha Convex Functions Associated with Conic Domains, Definition 3 and Theorem 1, pp.71 and73–74](https://www.etamaths.com/index.php/ijaa/article/view/738/210) is not credited as a verified valid sufficient criterion. Its ordinary specialization is conic k=0,A=1,B=-1, with interpolation alpha in [0,1]. The written theorem repeats an outer sum although its F_n definition already sums over n: the literal double-sum statement is malformed and potentially vacuous, and is not categorically claimed false under that reading. Its natural intended single-total interpretation is exactly false. At alpha=1, f(z)=z-z³/5 has intended coefficient total 4/5+6/25=26/25<2 but J_1[f](3/4)=-1/53. On the whole disk, f/z and f' are nonzero and Re f'>2/5, which also gives univalence. Denominator or univalence assumptions therefore do not rescue the intended criterion. It supplies no valid subsumption of this theorem.

The [Bravo–Carrasco–Hernández–Venegas June2026 preprint, Proposition2.2](https://arxiv.org/abs/2606.21574) also supplies no imported theorem here. Its asserted convex-order-to-alpha-convex implication is falsified by f(z)=z-z²/6, which has Re(1+zf''/f')>1/2 on the disk and both denominators nonzero. At the proposition's beta=1/2 and alpha=1/(1-ln2), evaluation at z=19/20 gives

    J_alpha[f](19/20)=(2222-3362ln2)/[4141(1-ln2)]<0.

The exact enclosure 2/3<ln2<25/36 proves the sign. The proof's negative multiplier reverses its attempted lower-bound inference. This finding is limited to Proposition2.2; no other result in the preprint is imported without independent verification.

[Silverman1985, Coefficient Conditions for a Subclass of Alpha-Convex Functions, Contemporary Mathematics38, pp.91–97](https://doi.org/10.1090/conm/038/789450) now has authenticated permitted [GoogleBooks preview pages93–94](https://books.google.com/books?id=QuQbCAAAQBAJ), visually read independently. The visible Theorem1 concerns f=z-sum a_n z^n with a_n>=0 and 0<=alpha<=1: membership in its negative-coefficient class is equivalent to the disk-local two-denominator expression being below1 for every radius r<1. Its remark replaces this with a boundary non-strict condition when sum n a_n<1 and sum n² a_n is finite. The visible Theorem2 gives sharp starlikeness order beta=(sqrt(alpha²+8alpha)-3alpha)/[2(1-alpha)] for alpha<1, beta(1)=2/3, with quadratic extremal z-[(1-beta)/(2-beta)]z². Its constant satisfies beta=2kappa/(1+2kappa), so that quadratic coefficient equals 1/[2(1+kappa)]. These are earlier negative-coefficient [0,1] antecedents; they are not an explicitly published all-real theorem or express named-problem answer. Pages91–92 and95–97 were not read by this preparation agent, so neither full-chapter verification nor complete proof review is claimed. Silverman1986 and1991 remain unresolved fulltexts. Alternative polynomial-criterion priority and mathematical-substance reconciliation remain pending; the distinct original-target conclusion is recorded in section6.

The author controls beside this candidate and its identical author-replay copy are refreshed against their new artifact hash. The independent checker remains the previously exercised explicit-if version; its actual earlier normal/optimized and optimized false-parameter guard receipts are retained with their original PIDs/dates and are not claimed rerun by this stage. Finite exact diagnostics test algebra and signs; the analytic proof above establishes the all-function theorem. The original receipts and original review are separately retained as archival evidence, not endorsements of this revised source text.

## 6. Accepted original-target disposition and older all-real answer

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
