# Attempt 4: local reconstruction and the exact conditional gap

This attempt reconstructs Sambale's Theorems 13–14 in a focused form. It is a conditional argument, not a proof of their unproved hypothesis.

## The square-count function

For u in D put

    q(u) = #{e in E outside D : e^2=u}.

This function is constant on D-conjugacy classes and satisfies q(u)=q(u^(-1)), by e -> e^(-1). Its total mass is |D|. Character orthogonality and the reality of the Gow indicators give the exact Fourier expansion

    q(u) = sum_{lambda in Irr(D)} g(lambda) lambda(u).       (2)

For example, the coefficient of lambda is |D|^(-1) sum_e conjugate(lambda(e^2)), equal to g(lambda) because g is real.

## A sufficient subsection identity

Use the standard nilpotent-block parametrization Gamma(lambda)=lambda*chi_0, choosing the 2-rational height-zero chi_0 with epsilon(chi_0)=+1 supplied by Gow's theorem. For a compatible subsection (u,b_u), the sole Brauer character phi_u has

    d^u_{Gamma(lambda),phi_u}=sigma(u) lambda(u),
    sigma(u) in {+1,-1}.

These are existing structural facts used in Sambale's Theorem 14. Suppose in addition that every subsection satisfies

    sum_{chi in Irr(B)} epsilon(chi) d^u_{chi,phi_u}=q(u).    (3)

Write v_lambda=epsilon(Gamma(lambda)). Then (3) says

    sigma(u) sum_lambda v_lambda lambda(u)=q(u).

The coefficient of the trivial character yields

    1 = v_1 = (1/|D|) sum_{u in D} sigma(u) q(u)
      <= (1/|D|) sum_{u in D} q(u) = 1.

Since q(u)>=0 and sigma(u) is a sign, equality forces sigma(u)=+1 whenever q(u)>0. Thus the signs disappear from (3). Uniqueness in (2) gives v_lambda=g(lambda) for every lambda. This would prove the full conjecture, and even for this particular Broue–Puig bijection.

The assertion (3) is sufficient. We do not claim that existence of an arbitrary bijection in the original conjecture implies (3).

## Why central quotients enter

Here is the elementary mechanism behind the local reduction. Let b be a real block with one Brauer character phi, and let u be a central 2-element of its ambient group H. Put Z=<u>, and let bar(b) be the block of H/Z dominated by b. The central 2-subgroup acts trivially on simple modules, so bar(b) also has one Brauer character. Let Phi and bar(Phi) be the respective projective indecomposable characters, with the latter inflated when comparing ordinary constituents.

For a real irreducible chi in b, the central scalar chi(u)/chi(1) is +1 or -1. It is +1 precisely when u is in its kernel. Non-real irreducibles have indicator zero. The ordinary decomposition numbers of the deflated characters are unchanged. Consequently

    sum_{chi in Irr(b)} epsilon(chi) d^u_{chi,phi}
       = 2 epsilon(bar(Phi)) - epsilon(Phi).                (4)

Let (D_0,E_0) be the local defect pair, with Z central in E_0. Define I(E_0,D_0) to be the number of outside involutions. Then the group-theoretic counterpart is

    #{e in E_0 outside D_0 : e^2=u}
       = 2 I(E_0/Z,D_0/Z) - I(E_0,D_0).                    (5)

For u nontrivial, an outside coset eZ that is an involution modulo Z has e^2=u^k. Its lifts e u^j square to u^(k+2j). If k is even, exactly two lifts square to 1 and none square to u; if k is odd, exactly two square to u and none to 1. Summing proves (5). The case u=1 is the identity I=2I-I.

Assuming the projective-indicator formula epsilon(Phi)=I for both b and bar(b), equations (4) and (5) agree. Applying the standard subsection reduction to H=C_G(u) gives (3): every square root of u centralizes u. Non-real local blocks contribute zero, and their compatible local extended pair has no outside elements. This is the route established in Sambale's Theorem 13.

## Where the proof stops

The scalar formula for the original block does not supply the scalar formulas for all these centralizers and central quotients. That missing family of statements is an unproved input, not an induction conclusion. For a nonsplit local pair the projective formula is already known: both sides vanish by Proposition 8(ii). The unresolved uses occur in split local pairs or split central quotients. In particular, when e^2=u, the image of e outside D_0/Z is an involution, so the quotient pair splits. Passing to a quotient does not automatically put the problem in the easy nonsplit case.

A source-algebra argument could alternatively supply (3), but it would have to preserve the form-sign information identified in Attempt 2. No such argument is obtained here.

**Outcome:** full conditional reconstruction, with an explicit, unproved local projective-indicator hypothesis. This is a transparent rederivation of published reductions, not new progress establishing that hypothesis.

Source: [Sambale](https://arxiv.org/abs/2301.13440), Lemma 2, Proposition 8, Theorems 13–14. The original [Oberwolfach report](https://ems.press/content/serial-article-files/47014?nt=1), pp.1055–1056, also displays the needed subsection identity.
