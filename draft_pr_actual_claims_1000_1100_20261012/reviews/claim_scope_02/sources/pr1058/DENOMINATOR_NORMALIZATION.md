# Nonzero reduction after clearing an invariant denominator

## Purpose and status

This is a self-contained standard algebra clarification for the denominator-clearing step in the institutional version of Park's *G_a-Actions on the Complements of Hypersurfaces*, Theorem 3.1, p.4. The prior theorem and its published status remain credited to Park. This note does not compare against the inaccessible journal PDF or claim a new theorem resolving problem 30003862.

## Lemma

Let k have characteristic zero. Let A be a finitely generated k-domain, let F in A be nonzero, and suppose

    intersection over n>=0 of F^n A = {0}.

Let delta be a nonzero locally nilpotent k-derivation of the localization A_F, and assume delta(F)=0. Then some integer e (possibly negative) makes

    Delta = F^e delta

preserve A and induce a nonzero locally nilpotent derivation of A/(F).

The quotient must, of course, be nonzero for this conclusion. The intersection hypothesis already excludes F being a unit in nonzero A. No assertion that A/(F) is a domain is needed for this lemma; in the geometric application that quotient is the relevant section-ring domain.

## Proof

Choose finitely many algebra generators a_1,...,a_s of A. Every delta(a_i) lies in A_F, so some integer M>=0 clears all denominators. Put Delta_0=F^M delta. Its values on the generators lie in A; the Leibniz rule therefore shows Delta_0(A) is contained in A.

Because delta(F)=0, for each n>=1 and a in A_F,

    Delta_0^n(a) = F^(Mn) delta^n(a).

Thus Delta_0 is locally nilpotent on A. It is nonzero there: if it vanished on every generator, it would vanish on A; since it also kills F, its extension to A_F would vanish, contradicting delta being nonzero.

For each nonzero Delta_0(a_i), its divisibility by powers of F has a largest finite exponent. Indeed, the admissible exponents form an initial subset of the nonnegative integers, and an unbounded such subset would place the element in their intersection, which is zero. Take r to be the least of these largest exponents over the nonzero generator images. Equivalently, r is the largest nonnegative integer such that every Delta_0(a_i) belongs to F^r A.

In A_F define

    Delta = F^(-r) Delta_0 = F^(M-r) delta.

It is a k-derivation because it is a scalar multiple of a derivation. It maps every generator into A and hence preserves A. It still kills F. Moreover F is invertible and invariant in A_F, so for each n>=1,

    Delta^n(a) = F^(-rn) Delta_0^n(a).

Local nilpotence of Delta_0 proves local nilpotence of Delta, both on A_F and on its invariant subring A.

Since Delta(F)=0, the ideal FA is stable under Delta: Delta(Fa)=F Delta(a). The derivation consequently descends to A/(F), where it remains locally nilpotent. If its reduction were zero, every Delta(a_i) would belong to FA, so every Delta_0(a_i)=F^r Delta(a_i) would belong to F^(r+1)A. That contradicts maximality of r. The induced derivation is therefore nonzero. This proves the lemma.

## Why the hypotheses hold in the indicated step

In Park's notation, R is a polynomial ring with positive integer weights, F is nonzero weighted-homogeneous of degree d>0, and

    A = R^[d] = direct sum over m>=0 of R_(dm).

Regrade A so R_(dm) has degree m. It is a finitely generated positively graded k-domain, with A_0=k and F of degree 1. Finite generation of this Veronese ring can be seen directly: each monomial can be factored into powers of x_i^d and one of finitely many monomials having every exponent less than d; the weighted-degree-divisible-by-d ones among these remainders suffice. If a nonzero element a lies in F^n A, its highest nonzero graded degree is at least n. Consequently a fixed nonzero a cannot lie in F^n A for arbitrarily large n, proving the intersection hypothesis.

The lifted action fixes the invertible F. Alternatively, any locally nilpotent derivation of a characteristic-zero domain kills its units. For completeness, define the delta-degree of a nonzero element u as the largest j with delta^j(u) nonzero. The Leibniz formula and the nonzero top binomial coefficient give deg_delta(uv)=deg_delta(u)+deg_delta(v). Applying this to u times u^(-1)=1 makes both degrees zero.

Finally, because F has weighted degree d,

    A/(F) = (R/(F))^[d].

To verify the kernel equality, a homogeneous multiple Fg of weighted degree dm has g of weighted degree d(m-1). Decomposing into homogeneous pieces gives (F)R intersect A = FA. The assumed graded section-ring presentation then identifies A/(F) with the section ring for dD. The nonzero quotient derivation supplies the required additive action on that cone. Invoking the *credited* cone/cylinder theorem yields a dD-polar cylinder; dividing its effective rational boundary by d preserves support and yields a D-polar cylinder. That last cone/cylinder theorem is an external published input, not proved in this note: Park's Theorem 2.2 cites T. Kishimoto, Yu. Prokhorov and M. Zaidenberg, *G_a-actions on affine cones*, Transformation Groups 18 (2013), no.4, 1137-1153, Corollary 3.2. It is also recorded as Theorem 1.15 in the 2021 Cheltsov–Park–Prokhorov–Zaidenberg survey (https://ems.press/content/serial-article-files/37019).

## Why “sufficiently large” alone does not prove nonzero reduction

Let A=k[F,x] and delta=d/dx. Although delta itself induces a nonzero derivation modulo F, F delta induces zero. Arbitrarily enlarging a clearing exponent can therefore destroy the desired nonzero quotient action.

The lemma supplies precisely the missing choice. It may also be phrased as choosing the **least integer** e for which F^e delta preserves A. Such integers exist and are bounded below by the finite F-divisibility of one nonzero generator image. If its image were contained in FA, the smaller integer e-1 would work. A least *nonnegative* integer is not sufficient: for delta=F d/dx, exponent zero is least nonnegative but the correct normalization uses exponent -1.

The examples diagnose only the choice of scalar in this inference. They are not counterexamples to Park's theorem or its del Pezzo consequence.
