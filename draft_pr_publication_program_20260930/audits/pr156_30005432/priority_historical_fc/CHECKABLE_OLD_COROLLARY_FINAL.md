# A checkable composite consequence of earlier results

This is the auditor's derivation, not a claim that an earlier author stated the counterexample. The input results are independently identified in primary sources, with exact versions below. All calculations are exact over the integers.

Let Q be any finite skew left brace and let chi:(Q,circle)->{+1,-1} be a group homomorphism. Give the integers the trivial brace structure. Inversion is an automorphism of this trivial brace. Smoktunowicz–Vendramin's semidirect construction (arXiv:1705.06958v3, Corollary 2.37; published 2018, Corollary 3.37) therefore gives

    B = Z x Q,
    (n,q)+(m,r) = (n+m,q+r),
    (n,q) circle (m,r) = (n+chi(q)m,q circle r).

Its lambda maps are

    lambda_(n,q)(m,r) = (chi(q)m,lambda_q(r)).

Every element has at most 2|Q| lambda images and at most |Q| additive conjugates. Thus every element is theta_f. By Cascella–Properzi–Van Antwerpen, arXiv:2603.06177v1 Proposition 5.17 (public March 6, 2026), the (s)-set of B is precisely FC(B,circle). This use of the theorem checks its ambient theta_f hypothesis, rather than dropping it. The same proposition occurs in v2 (September 14, 2026).

The circle inverse of (t,r) is (-chi(r)t,r^{-1}), so its conjugation of (n,q) is

    (t,r) circle (n,q) circle (t,r)^{-1}
       = ((1-chi(q))t + chi(r)n, r circle q circle r^{-1}).

Here chi(r q r^{-1})=chi(q), and chi(r)^2=1. If chi(q)=-1, taking r=0 and allowing t to vary produces the infinitely many first coordinates n+2t. If chi(q)=1, the first coordinate is either n or -n and the second coordinate lies in the finite group Q. Consequently

    S(B) = FC(B,circle) = Z x ker(chi).

The same equality has a direct proof from CFT's original index definition, without the 2026 characterization. If chi(q)=1, Fix(lambda_(n,q)) contains Z x {0}, so its additive index is finite. Its lambda orbit is finite, hence its lambda stabilizer has finite circle index. The displayed conjugation formula shows that its circle centralizer also has finite index. Their intersection therefore has finite circle index. If chi(q)=-1, Fix(lambda_(n,q)) is contained in {0} x Q and has infinite additive index. Thus the old construction plus the original definition already makes the example an elementary consequence; CPV provides an independently applicable conceptual characterization.

This is a normal circle subgroup. It fails to be an additive subgroup whenever ker(chi) fails to be an additive subgroup of Q. Lambda invariance likewise reduces to the corresponding invariance of this kernel in Q.

For the accepted candidate, take Q=C4 with c circle d=c+d+2cd mod 4. Bachiller's Proposition 2.4(iii), arXiv:1407.5224 (2014; published 2015), gives this precise finite brace. Its circle group is V4. The four elements have binary labels 0=00,1=01,2=10,3=11; circle multiplication is bitwise addition modulo 2. The character chi(c)=(-1)^highbit(c) has kernel {0,1}. It is a circle character, but its kernel is not additive since 1+1=2.

An even closer old construction occurs in Dietzel, arXiv:1801.06911v1 and v2, Theorem 5(iv), PDF/printed p19. It writes c=highbit(c) lowbit(c) as a binary string and gives star multiplication on C4 x Cq, q>3 prime,

    (c,a) star (d,b) = (2cd,(omega^highbit(c) mu^lowbit(c)-1)b),
    omega,mu in {+1,-1}.

Setting omega=-1,mu=1 and replacing circle by plus+star gives

    (c,a) circle (d,b) = (c+d+2cd, a+chi(c)b),

with the second coordinate modulo q. Swapping coordinates makes this literally the candidate formula with Z replaced by Cq. Dietzel thus already selects the high-bit inversion character in a finite parameter family. All elements of this finite brace have (s); no negative answer is inferred from its finiteness alone. Replacing the acted-on trivial Cq by the trivial Z is licensed by the earlier general semidirect construction; the infinite conjugation calculation supplies the obstruction.

For the candidate, lambda_(n,c)(m,d)=(chi(c)m,(1+2c)d). The fixed subgroup of lambda_(0,1) is Z x {0,2}, of additive index 2. Its lambda stabilizer intersected with its circle centralizer is also Z x {0,2}, of circle index 2. For (0,2), the fixed subgroup is {0} x C4, of infinite additive index; its corresponding circle subgroup is finite, also of infinite index. Thus (0,1) belongs to S but its additive double does not. Lambda_(0,1)(0,1)=(0,3) also leaves S. Right distributivity fails because with a=b=(0,1),z=(1,0), (a+b) star z=(-2,0), while a star z+b star z=(0,0).

Boundary checks: trivial chi gives S=B; if Q is finite and the acted-on factor is finite, every element has (s); if ker chi is an additive lambda-invariant subgroup then this construction does not produce the stated additive failure. These are exact deductions, independent of numerical samples.

Priority interpretation: the unrestricted negative answer is a short composite consequence of an old finite brace, an old semidirect construction, and a public pre-cutoff finiteness characterization. This is evidence against presenting the construction or its mechanism as wholly new. It is not documentary evidence that the negative answer or the selected infinite brace was explicitly published before September 30, 2026.
