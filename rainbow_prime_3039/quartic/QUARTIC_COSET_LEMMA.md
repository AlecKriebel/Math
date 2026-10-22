# Quartic multiplicative colorings: a restricted positive result

## Scope and status

This is a standard character-sum application, not a solution for arbitrary balanced four-colorings and not a novelty claim. It applies only when the four nonzero color classes are the cosets of the fourth-power subgroup of F_p^*, with zero assigned to any one of them. Its purpose is to eliminate this structured family as a source of large-prime counterexamples.

## Proposition

Let p be a prime with p ≡ 1 (mod 4), and let χ:F_p^*→{1,i,−1,−i} be a multiplicative character of exact order four. Color each nonzero x by χ(x), and give zero any of the four colors. For p ≥ 263681, every nonzero d∈F_p admits a∈F_p such that

    a, a+d, a+2d, a+3d

are all nonzero and have four distinct colors. The same conclusion therefore holds under the simpler hypotheses p ≥ 514²=264196 or p ≥ 10^6.

The coloring is balanced in the usual strongest possible sense: its color-class sizes are (p+3)/4 once and (p−1)/4 three times.

## Counting lemma

For any prescribed z_0,z_1,z_2,z_3∈{1,i,−1,−i}, not necessarily distinct, write

    N(z) = #{t∈F_p : t+j ≠ 0 and χ(t+j)=z_j for j=0,1,2,3}.

Then

    N(z) ≥ (p − 256 − 513√p)/256.

### Proof

Since p ≥ 5, the four elements 0,−1,−2,−3 are distinct. Put U=F_p\{0,−1,−2,−3}. On U all character arguments are nonzero. Root-of-unity orthogonality gives

    256 N(z)
      = Σ_{t∈U} Π_{j=0}^3 Σ_{e_j=0}^3 [z_j^(−1)χ(t+j)]^(e_j)
      = (p−4) + Σ_{e∈{0,1,2,3}^4\{0}} c_e S_e,

where |c_e|=1 and

    S_e=Σ_{t∈U} χ(f_e(t)),
    f_e(T)=Π_{j:e_j>0}(T+j)^(e_j).

This formula never uses a convention for 0^0: every argument in the initial expansion is nonzero, and the zero-exponent factors in f_e are omitted.

Let s=|{j:e_j>0}|. The monic polynomial f_e has exactly s distinct roots, each with multiplicity in {1,2,3}. In particular, it is not a constant multiple of a fourth power, even over the algebraic closure. The multiplicative Weil bound for the exact-order-four character χ, extended by χ(0)=0, gives

    |Σ_{t∈F_p} χ(f_e(t))| ≤ (s−1)√p.

Of the four omitted points, s are roots of f_e and contribute zero. The other 4−s points each have contribution of modulus one. Thus

    |S_e| ≤ (s−1)√p + (4−s).

There are binomial(4,s)3^s exponent vectors of support size s. Summing the four support-size contributions gives

    Σ_{s=1}^4 binomial(4,s)3^s(s−1) = 0+54+216+243 = 513,
    Σ_{s=1}^4 binomial(4,s)3^s(4−s) = 36+108+108+0 = 252.

The expansion is real (it equals 256N); taking real parts and using the triangle inequality proves

    256N ≥ p−4−513√p−252 = p−256−513√p.

This proves the counting lemma.

### Positivity threshold

The numerator is positive if p−256>513√p. For p≥263681, both sides are nonnegative, and the squared difference is

    (p−256)^2−513²p = p²−263681p+65536.

At p=263681 this is 65536>0; the polynomial is increasing for all real p≥263681 because its derivative is 2p−263681>0. This proves the stated threshold without floating-point reliance. The positive real root is approximately 263680.751457, but this numerical approximation is not used in the proof.

For the simpler threshold, √p≥514 implies

    p−513√p−256 = √p(√p−513)−256 ≥514−256=258>0.

### Deduction for every difference

Apply the counting lemma with z_j=i^j. Choose t with χ(t),χ(t+1),χ(t+2),χ(t+3) equal to 1,i,−1,−i. For any d≠0 put a=dt. Then

    χ(a+jd)=χ(d)χ(t+j)=χ(d)i^j.

Multiplication by χ(d) permutes the four colors. None of these four points is zero, so the arbitrary color of zero is irrelevant. The progression is nondegenerate: p≥5 and d≠0 make its four points distinct. This completes the proposition.

## Source and relation to existing literature

Chaim Even-Zohar, Michael Farber, and Lewis Mead, “Ample simplicial complexes,” European Journal of Mathematics 8 (2022), 1–32, DOI 10.1007/s40879-021-00521-5.

Public article: https://link.springer.com/article/10.1007/s40879-021-00521-5

Theorem A.1 states precisely the multiplicative Weil estimate in terms of the number of distinct polynomial roots, under the hypothesis that the polynomial is not a constant multiple of an m-th power. Lemma 6.6 gives a more general prescribed-coset intersection estimate; applying it with m=d=4 already yields N≥p/256−3√p−1, sufficient for p≥10^6. The coefficient 513 above comes only from retaining support sizes in the standard expansion rather than using three for all 255 nonconstant terms. Neither this observation nor the coloring corollary is claimed to be new.

The publisher's accessible HTML was inspected on 2026-10-20. It labels the theorem “Theorem A.1”; its appendix is rendered as Section 7 in that HTML. The proof here is independently written and the source is not copied into the publication deliverable.
