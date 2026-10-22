# Approach 3: a Jacobian-torsion lifting obstruction

Status: an exact local criterion and sufficient condition are proved. The geometric hypotheses of the original question do not imply that condition.

Work in the convergent power-series ring O=C{x_1,...,x_{n-1},z}, or its formal counterpart. Let f be reduced, with z not dividing f, and put f_0=f mod z and r=(f_0)_red. Write D(g) for derivations preserving the principal ideal (g). Define
M_f=O/(f,f_{x_1},...,f_{x_{n-1}},f_z).
Then there is a well-defined O/(z)-linear obstruction map
ob: D_{O/(z)}(r) -> (0:_{M_f} z),
and an exact sequence at every term except the last:
0 -> z D(f) -> D(fz) -> D_{O/(z)}(r) -> (0:_{M_f} z).
There is no assertion that ob is onto. The cokernel of restriction is precisely im(ob).

## Proof

In a characteristic-zero regular local factorial ring, a derivation preserves a nonzero principal ideal (u product_j p_j^{m_j}) if and only if it preserves every reduced factor ideal (p_j). To prove the nontrivial direction, reduce the identity for its derivative modulo p_j after dividing by p_j^{m_j-1}; the nonzero integer m_j and the other factors are invertible in the localization at (p_j), forcing p_j to divide the derivative of p_j. Divisibility in the ring follows. The reverse direction follows by the product rule. Thus D(f_0)=D(r).

Given eta in D(r), choose a lift delta tangent to z=0 (for example zero normal coefficient). There is a uniquely determined b_0 in O/(z) with eta(f_0)=b_0 f_0, since f_0 is a nonzero element of the domain O/(z). Choose any lift b and write
delta(f)-bf=zc.
Set ob(eta)=[c] in M_f. Since delta(f) and bf belong to the defining ideal of M_f, z[c]=0. Changing b by zb' changes c by -b'f, which has zero class. Changing delta by z nu changes c, modulo (f), by nu(f), also zero in M_f. Hence the construction is well-defined. Multiplication by a lift of an element of O/(z) multiplies [c] by that lift; the ambiguity is killed by z[c]=0. Additivity is immediate.

A lift can be corrected to a logarithmic derivation precisely when [c]=0. Indeed, if c=af+nu(f), replace delta by delta-z nu. Its derivative of f is (b+za)f, and its normal coefficient is still divisible by z. Conversely any corrected logarithmic lift gives c in (f,partials f). Because f and z are coprime, a derivation is in D(fz) precisely when it is in both D(f) and D(z).

Finally, a derivation restricting to zero has every coefficient divisible by z, so is z nu. If z nu is logarithmic for f, then f divides z nu(f), and coprimality gives f divides nu(f). Conversely every z nu with nu in D(f) is logarithmic for fz and restricts to zero. This proves the kernel and exactness claims.

## Consequences and gap

If multiplication by z is injective on M_f, restriction is surjective. Equivalently, a non-zero-divisor cut of the Tjurina/Jacobian quotient provides a sufficient condition. This includes the product cases of Approach 1 and the smooth-divisor case M_f=0. It is not necessary: only im(ob), not all of (0:z), controls the obstruction.

This directly isolates scheme-theoretic information discarded by reduced incidence data. It is a local presentation; no unproved globally untwisted identification of the target M_f is asserted. The globally canonical object used later is the actual cokernel Q. Neither quasihomogeneity alone nor a topological class identity is shown to kill im(ob). The counterexample in Approach 2 proves that such an inference would be false.
