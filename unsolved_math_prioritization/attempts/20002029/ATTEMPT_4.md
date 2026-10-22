# Attempt 4: excluding the two recent dimension-eight divergence candidates

## Target and outcome

Merely observing that displayed Weyl factors in a formula do not prove that no alternative Schouten-only formula exists. This attempt replaces that visual inference with a pointwise obstruction certificate for the entire span of the two explicit dimension-eight examples in Case–Khaitan–Lin–Tyrrell–Yuan, arXiv:2404.11319v4, equation (3.4). No nonzero linear combination of those two invariants can have a pure-Schouten-jet representative.

This is not a classification of all weight -8 invariants and does not settle the original question in dimension eight.

## The two invariants and their Ricci-flat restriction

Use precisely the v4 invariants U1 and U2 of (3.4). Their Cotton terms vanish identically on every Ricci-flat metric, along with their derivatives. The pointwise restrictions are therefore

    U1 = nabla^a nabla^b T1_ab,
    U2 = nabla^a nabla^b T2_ab - (1/6)Delta A,

where

    T1_ab=R_acbd R_cefg R_defg,
    T2_ab=R_acde R_bcfg R_defg,
    A=R_abcd R_cdef R_efab.

All raised/lowered indices are evaluated in an orthonormal frame. These are exact pointwise restrictions, not identities modulo divergence. The sign convention for Cotton changed between some preprint versions; this restriction is independent of that change because Cotton vanishes identically.

## Two explicit eight-dimensional metrics

Use the positive-definite Kasner metrics from Attempt 3, now with seven spatial exponents. The constraints sum p_i=sum p_i^2=1 guarantee Ricci-flatness. Let

    p1=(-1/3,2/3,2/3,0,0,0,0),
    p2=(-1/2,1/2,1/2,1/2,0,0,0).

The extra zero exponents simply add flat factors. As before, in the orthonormal frame and at r=1,

    K_0i=p_i(1-p_i), K_ij=-p_i p_j,
    R_abcd=K_ab(delta_ac delta_bd-delta_ad delta_bc).

The symmetric tensors T1 and T2 are diagonal and scale as r^-6. Their constant diagonal coefficients are

    t1_a=2 sum_c K_ac (sum_e K_ce^2),
    t2_a=4 sum_c K_ac^3,
    A(r)=r^-6 sum_a t2_a.

The accompanying script also evaluates the unreduced component contractions and verifies every off-diagonal entry is zero.

## Derivative calculation

For a symmetric tensor T with orthonormal-frame components r^-6 diag(t0,t1,...,t7), the Kasner connection yields

    (div T)_0=r^-7[-6t0+sum_i p_i(t0-ti)]
               =r^-7[-5t0-sum_i p_i ti],
    (div T)_i=0.

The second divergence of a radial covector r^-7 v dr is (-7+sum p_i)r^-8 v=-6r^-8 v. Consequently,

    div(div T)|_(r=1)=30t0+6sum_i p_i ti.             (4.1)

For a radial scalar f(r)=r^-6 A0,

    Delta f=f''+(sum p_i)f'/r=36r^-8 A0.             (4.2)

Therefore the two invariant values are obtained directly from (4.1) and (4.2), without differentiating numerical samples.

## Exact certificate

The rows (U1,U2), evaluated at r=1, are

    p1: (0, -256/81),
    p2: (-63/4, -45/2).

The 2 by 2 determinant is -448/9, hence nonzero. The rational-arithmetic script checks the Kasner constraints, Ricci-flatness, direct cubic tensor contractions, both rows and the determinant.

If a U1+b U2 had a formula involving only complete contractions of Schouten jets, it would vanish on both metrics because P vanishes identically. The nonsingular matrix forces a=b=0. Thus the entire two-dimensional span is disjoint from the nonzero pure-Schouten class, not merely the two individual displayed formulas.

## Scope and remaining gap

This rules out the most immediate recent candidate family for a dimension-eight counterexample. Other conformal invariants of weight -8 can involve additional quartic Weyl or derivative contractions. No exhaustive spanning list or restriction matrix for that full space has been established here. The full n>=8 question remains open within this investigation.

Source: https://arxiv.org/html/2404.11319v4#S3, equation (3.4). Reproduce with python checks/verify_divergence_restrictions.py. Results are in checks/verify_divergence_restrictions.result.json. This explicit exclusion is a candidate useful certificate; priority is unestablished.
