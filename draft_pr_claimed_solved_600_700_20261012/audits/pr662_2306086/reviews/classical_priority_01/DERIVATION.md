# Classical structural priority audit: explicit implication tests

UTC audit date: 2026-10-15. PR 662 / problem 2306086 only. Immutable head: `e31701151c331a6eed9224fb37a75a374ea1043e`.

## Exact proposition being tested

Let S_R be the normalized injective holomorphic maps of the disk with real Taylor coefficients. Put

    A_f(z) = (1-|z|^2) f''(z)/f'(z) - 2 conjugate(z).

The proposition is

    M(z) = max_{f in S_R} |A_f(z)| < 4,  Im z != 0,
    M(x) = 4,  -1 < x < 1.

It includes a common positive gap on every compact subset of the nonreal disk, by joint continuity and compactness. It does not evaluate M, provide an explicit upper gap, determine extremizers, or give the full value region. The source's expression at zero is identically zero; A_f(0) is a different auxiliary normalized expression.

The governing primary problem (Hayman–Lingham 2018 draft, printed p.147) fixes the evaluation point before asking about improvement under reality of f. No explicit requirement of a sharp or numerical answer is present. Thus this audit does not manufacture such a requirement in order to reject the qualitative proposition.

## 1. What the classical coefficient theorem does imply

The area-theorem second-coefficient bound on S is

    |a_2(F)| <= 2,
    equality iff F(w) = w/(1-lambda w)^2, |lambda|=1.

For a fixed a in the disk, the normalized Koebe transform T_a f has

    a_2(T_a f) = A_f(a)/2.

Consequently |A_f(a)| <= 4 and equality implies that f maps the disk onto a complex affine image of the complement of a ray. This is an implication of old coefficient theory. It does NOT by itself say that f is a normalized Koebe rotation: precomposition by a general disk automorphism changes the normalization and the position of the omitted ray relative to the origin.

For f in S_R, reflection makes the image domain conjugation-invariant. A single omitted ray must therefore have a real endpoint and real direction. Because zero belongs to the image, the omitted set has one of the forms (-infinity,c] with c<0, or [c,infinity) with c>0.

The maps g=4|c| k_+ or 4|c| k_- map onto the same slit domain and fix zero, where k_+=z/(1-z)^2 and k_-=z/(1+z)^2. The disk automorphism g^{-1} composed with f fixes zero. Its derivative there has modulus 1, while its derivative is 1/(4|c|). Hence |c|=1/4; since both normalized derivatives are 1, uniqueness gives f=k_+ or f=k_-.

For those two functions direct calculation gives

    |A_{k_+}(z)|^2 = |A_{k_-}(z)|^2
                  = 16 - 48 (Im z)^2/|1-z^2|^2.

Thus neither real Koebe function attains 4 at a nonreal point. On the real diameter their A-values are +4 and -4.

The growth estimate on S makes S compact in local uniform convergence; its real subfamily is closed. The functional A_f(a) is continuous because derivatives converge locally uniformly and the limiting normalized injective map has nonvanishing derivative. Therefore a maximum on S_R exists. If it were 4 at a nonreal a, the preceding equality analysis would force a real Koebe function there, a contradiction.

This explicitly reconstructs the theorem's bridge from the classical coefficient bound. It identifies a short application of old foundations. It is not evidence that the real-subfamily conclusion was previously stated or that an earlier overlapping extremal theorem had already resolved it. Every proof follows earlier foundations; that observation alone is not a historical priority obstruction.

The original author's note supplies a self-contained area/equality proof. Belyaev's author-hosted notes, Theorems 3.2.3 and 3.2.8, independently display the classical coefficient/equality and Koebe-transform mechanism. Their displayed text contains typographical inconsistencies (strict coefficient sign alongside equality, and a factor in a later equality discussion); this audit uses the corrected standard statements above, justified by the explicit area argument, and imports no erroneous numerical assertion from those notes.

## 2. Why Koepf's extreme-point theorem is not the needed older result

Koepf (1986), printed p.578, Section 4 Corollary, identifies the extreme points of S_R as

    f_y(z)=z/[(1-y z)(1-conjugate(y) z)], |y|=1.

The surrounding discussion concerns continuous linear functionals and the closed convex hull. The map f -> f''(a)/f'(a) is nonlinear in f. In a convex combination, its derivative quotient has complex derivative-dependent weights rather than nonnegative real weights. Thus the extreme-point theorem does not transfer the maximum of this quotient to the displayed family.

A checkable obstruction to the naive convex-hull argument is

    q=(k_++k_-)/2=z(1+z^2)/(1-z^2)^2,
    q'=(1+6z^2+z^4)/(1-z^2)^3.

At a=i(sqrt(2)-1), q' vanishes simply and q'' does not. Thus the pre-Schwarzian has a pole there, although q is a convex combination of two elements of S_R. Approaching q through unequal weights gives unbounded quotient values at that fixed point whenever the numerator does not vanish in the limit. Accordingly a finite uniform-in-f bound cannot be recovered merely by replacing S_R by its closed convex hull.

The exact remaining bridge would be a theorem on this nonlinear functional over S_R, or an admissible variational reduction proving its maximizers satisfy the required hypotheses. No such bridge was verified in the inspected Koepf article. This route is blocked as a priority argument; reopening it requires a materially new theorem or evidence.

## 3. Why the concave variability theorem does not cover S_R

Bhowmik–Ponnusamy–Wirths, arXiv:1008.4861v1, pp.2 and 4, define Co(alpha) by normalized univalence, a pole at the boundary point 1, convexity of the omitted set, and an angle condition. Their Theorem 2.5 gives a disk of variability for the pre-Schwarzian on that class. Theorem 2.5 is genuinely stronger for its stated class, but it is not a statement on every real schlicht map.

For example f(z)=z belongs to S_R and is bounded, has no pole at 1, and C\f(D) is not convex: the omitted points 2 and -2 have midpoint zero inside the image. Thus even the most basic target member fails the class hypotheses. Rotating Co(alpha) does not repair this example. No inclusion S_R subset Co(alpha), or reduction carrying every target f to Co(alpha) while preserving the functional, was verified. A theorem restricted to that class therefore cannot defeat priority of the present all-S_R assertion.

The ordinary global norm inequality ||f''/f'|| <= 6 for f in S is also insufficient: its direct triangle-inequality consequence is |A_f(z)| <= 6+2|z|, which does not even recover 4. Bounds on a convex subclass likewise do not apply to the whole real class; k_+ itself has a nonconvex image.

## 4. Same operator in later Hardy-space work is not an implication

Chuaqui–Efraimidis–Hernández (arXiv:2510.05395v1, submitted 2025-10-06) use A_f/2 as the second coefficient of a Koebe transform. Their lower order is the infimum over evaluation points for one function. The inspected introductory theorems and their real-class discussion concern Hardy exponents, convex subclasses, and derivatives with pathological radial behavior. These are different quantifiers and different conclusions from a maximum over all real functions at one fixed nonreal point.

This work is a related contemporary source to acknowledge if useful. Its shared notation and transform identity supply no verified stronger bound implying M(z)<4. No assertion of absence from its entire literature neighborhood is made.

## 5. Sources that could not be promoted into a verified implication

* Jenkins (1960), DOI 10.2307/1969877: publisher issue metadata confirms title, author, volume 71(1), pp.1–15. Full article retrieval yielded only a short HTML response rather than a PDF. Secondary discovery descriptions concern f(z)-variability; they were not promoted into technical evidence about the uninspected original. More significantly, the independently inspected 1962 original survey explicitly confirms derivative bounds in the 1960 paper, as detailed next. The exact formulas remain an unresolved priority lead. Knowing a point-value region alone would not license differentiation of its boundary to obtain a pre-Schwarzian region.
* Jenkins (1962), DOI 10.1090/S0002-9904-1962-10670-3: my direct publisher requests returned HTTP 403, but the parent subsequently supplied the exact original nine-page PDF (777738 bytes, SHA-256 f5e81479d158b49f557bcce334f8c4992ef4543b2b81eba3db92e8842808650d). I independently read all nine pages. Printed p.7 explicitly says the 1960 real-coefficient paper includes “bounds involving the derivatives of these functions,” in addition to image and value regions. Thus the 1960 lead must NOT be characterized as only a point-value result. However, no formula, derivative order, extremal description, or applicable hypotheses are supplied there. This strengthens the unresolved access lead without establishing the target implication. Its very general coefficient theorem does not by itself prove historical coverage of this particular application. An initial attempted issue-2 URL was wrong and is retained in the retrieval ledger as such; the metadata-corrected issue-1 forms also failed directly.
* Rodemich, AMS Notices January 1979, abstract 763-30-11, printed A-68, received October 20, 1978: an indexed primary-PDF excerpt announces an inequality for normalized real-coefficient univalent maps and defines q=|z-conjugate(z)|/(1-|z|^2). The left-hand functional is missing from the indexed excerpt. Direct PDF retrieval was HTTP 403; the web PDF parser also failed. A rotation-type estimate is only a tentative interpretation and was not used as fact. This is a concrete unresolved access lead, not a verified prior solution.
* Tepper, AMS Notices January 1976, abstract 731-30-27: indexed primary excerpt announces Loewner distortion estimates and exhibits an argument estimate for f. The original full page was not retrieved. No pre-Schwarzian conclusion is attributed to it.
* Kraus–Roth AASF 31 (2006): a primary indexed PDF lead discusses two-point distortion, but current direct retrieval returned 404 and further web reads failed. No precise theorem or target implication was verified from the incomplete access.

## 6. Result of this route

No inspected older theorem has been shown, with its actual hypotheses, to imply the target as an already covered special case. The strongest positive verified relation is the classical-foundation derivation in Section 1. The exact historical novelty of the real-subfamily application remains unestablished; in particular Jenkins and Rodemich source-access limits remain.

Reasonable presentation: a short note giving a qualitative answer at nonreal points, real-axis sharpness, and the compact-set corollary, explicitly derived from classical coefficient rigidity. Do not claim a new method, first proof, complete sharp quantitative resolution, or exhaustive priority clearance. The proof may be mathematically sound and an appropriate narrowly framed contribution even though no novelty guarantee is possible. This family has no evidence-based recommendation to close the PR for an already known solution.
