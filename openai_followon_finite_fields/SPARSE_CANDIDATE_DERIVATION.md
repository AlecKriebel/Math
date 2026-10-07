# All-multiplicity sparse factorization: current derivation

Candidate status, 2026-10-07 05:32 UTC. This is outside the frozen version-3
fileset. The mathematical reduction has independent proof and computation
checks in progress; priority and complete-package review are not finished.

## Exact claim and model

Let K=F_p[T]/h, with p supplied in binary and promised prime, m=deg h>=1,
and h monic irreducible (promised or verified by the previous deterministic
Frobenius criterion). Set L=ceil(log_2 p). Supply a nonzero polynomial

    f(X) = sum_{i=1}^t a_i X^{n_i}

as distinct nonnegative binary exponents and nonzero m-coordinate coefficients.
N=max n_i, b=max(1,ceil(log_2(N+1))). The requested output is the leading
coefficient and all distinct monic irreducibles densely, with positive binary
multiplicities. Let D be their total unweighted degree. The claim is a
deterministic reduction to dense factorization with bit complexity polynomial
in t,b,D,m,L, including arbitrary p-divisible multiplicities. It therefore
becomes an unconditional deterministic bit-polynomial algorithm on the audited
family142/029 cited-source basis. The reduction itself is independent of that
input theorem. Zero is excluded; constants and monomials are handled directly.

The input size is O((m+1)L+t(mL+b)); output size includes at least DmL and
the binary multiplicities. No dependence polynomial in numeric N or p is
permitted. This is an extension of, not a replacement for, the inherited dense
core and prescribed-degree construction target.

## Known-factor valuation (constructive residue argument)

For an irreducible g!=X of degree delta, E=K[X]/g has dimension delta over K
and m*delta over F_p. Its formal root alpha is nonzero. Since finite fields
are perfect and g is separable, g's exponent in f is the valuation at Y=0 of
f(alpha*(1+Y)). Normalize weights w_i=a_i*alpha^{n_i} and preserve the actual
integer exponents, even if powering alpha reduces an exponent internally.

For any node's distinct exponents write n=pq+r, 0<=r<p. Then

    F(Y) = sum_r (1+Y)^r H_r(Y^p).

Recursively compute each child's initial order nu_r and coefficient c_r. Put
v=min nu_r and P(Y)=sum_{nu_r=v} c_r(1+Y)^r. Distinct residues and nonzero
coefficients ensure P is nonzero. If s residues are active, the matrix
[binom(r,j)] with 0<=j<s is invertible: its determinant is a nonzero
Vandermonde divided by product j!, because s<=p. Thus the first nonzero
coefficient occurs at j<s<=p. Terms from inactive children start at order
at least p(v+1), above pv+j. The parent initial order is pv+j and its
coefficient is P_j. A single monomial has initial order zero. Induction proves
the algorithm, including zero valuation and arbitrarily large multiplicity.

Use an explicit postorder stack. Depth is at most ceil(log_p(N+1)); each
level partitions the original t terms, so total nodes <=t(b+1), and the sum
of squared node support sizes over all levels is <=t^2(b+1). Low binomial
columns use j<p, so denominators are invertible; scan s coefficients, never p.
Initial powers cost O(tb) E multiplications; all other arithmetic is bounded
by O(t^2(b+1)) E additions and prime-scalar multiplications. A conservative
bound is O((t+t^2)(b+1)delta^2) K operations plus polynomial integer work.
The g=X valuation is simply min n_i.

The residue structure and sparsity bound are inherited from Mattarei's
Theorem 2 (2005/2006), with earlier repeated-root coding results. In particular
the algorithm itself shows that every known-factor multiplicity mu satisfies
mu mod p <= t-1. No new multiplicity/sparsity bound is claimed.

## Visible-factor discovery

For a sparse U with U(0)!=0, the reduced logarithmic derivative U'/U=P/G
has deg P<deg G and G equal to the product of the irreducibles whose
multiplicities in U are not divisible by p. G is squarefree and G(0)!=0.
This is standard logarithmic-derivative machinery, including the rad_p scope.

For B=1,2,4,... compute the first 2B Taylor coefficients of U'/U by formal
division at zero. Only coefficients of U through index 2B are needed, obtained
directly from its sparse list. Solve B equations for Q_1,...,Q_B with Q_0=1,
deg Q<=B, and coefficient (Q*series)_j=0 for B<=j<2B. The augmented
matrix has B rows and B+1 columns over K, or dimension at most mB in F_p.
Let A be the first B coefficients of Q*series. Test the exact sparse identity
U'Q=UA: multiplying a t-term sparse input by a degree-B dense polynomial
produces at most t(B+1) terms with binary exponents. Combine equal exponents
and compare exact coefficients. A prefix agreement alone is insufficient.

At B>=deg G, a solution exists. Any solution with the stated degrees has
(AG-PQ) vanishing to order 2B, while deg(AG-PQ)<2B; hence it is the true
rational function. After acceptance cancel gcd(A,Q) and make the denominator
monic. With d=deg G, the accepted B<=2max(1,d), and earlier trials have
geometrically bounded total cost. Factor only the dense polynomial G and use
the known-factor valuation routine to obtain its exact multiplicities.
This is a classical Padé reduction, not a new reconstruction theorem.

## Full pth-root descent with a rational representation

Strip X^a from the initial input, recording a=min n_i. Maintain a *polynomial*
F=U/V with U sparse, U(0)!=0, V dense, V(0)!=0, and V|U. Initially V=1.
Let e_U(g),e_V(g) be exact nonnegative multiplicities. Construct densely

    A_U = product_g g^{e_U(g) mod p},
    A_V = product_g g^{e_V(g) mod p}.

The factors in A_U are exactly those discovered by the logarithmic derivative;
factor V by the dense algorithm. U=A_U H_U^p and V=A_V H_V^p for unique
polynomials H_U,H_V, including scalar pth roots. H_V is obtained by exact
dense division followed by inverse coefficient Frobenius. Because V|U,
floor(e_U/p)>=floor(e_V/p), so H=H_U/H_V is also a polynomial. Its radical
is contained in the radical of F. Also

    F = (A_U/A_V) H^p.

Residue contributions in A_U/A_V may be negative. They must be retained as
signed integers and combined with the later p-times contributions.

Take the constant Cartier section C_0(sum c_n X^n)=sum c_{pn}Y^n.
The standard pull-out identity gives C_0(U)=C_0(A_U)*(H_U coefficient-Frobenius).
Both constant terms are nonzero. Apply coefficient inverse Frobenius to *both*
sections: U_new=Frob^{-1}(C_0(U)), W=Frob^{-1}(C_0(A_U)). Then H_U=U_new/W.
Set V_new=W H_V. This represents H as U_new/V_new and maintains V_new|U_new.
U_new has at most t terms and degree at most floor(deg U/p).

## The bounded-denominator invariant

Let D_F be the radical degree of F, v=deg V, and D_U the radical degree of U.
Since U=F V,

    D_U <= D_F+v.

Every exponent in A_U is at most p-1, hence deg A_U <= (p-1)D_U. Therefore

    deg V_new <= deg A_U/p + deg V/p
               <= ((p-1)(D_F+v)+v)/p
               = v+(1-1/p)D_F <= v+D_F.

Furthermore e_U(g) mod p <= t-1 from the sparse residue argument, so
deg A_U <= min(p-1,t-1)D_U. Creating A_U densely costs polynomial in
t,D_U; the displayed division by p does not authorize a numeric-p loop.

Since radical(H) is contained in radical(F), D_F never exceeds the original
non-X radical degree D. After k descents v<=kD. The sparse numerator degree
shrinks by p, so at most b descents occur; termination uses this numerator
degree, not a claim that deg F shrinks by p. At termination U is constant,
and V|U forces V constant.

At each step add p^k(e_U mod p-e_V mod p) to the factor ledger. The relation
e_F=(e_U mod p-e_V mod p)+p e_H telescopes, proving exact final multiplicities.
Intermediate factors can be absent from the original polynomial and must
cancel. Finally retain the original leading coefficient. Verify each output
factor's irreducibility, its valuation in the *original* sparse polynomial,
and sum multiplicity*degree=N. These checks certify completeness without
expanding any huge powers.

## Complexity ledger

At level k<b: v<=kD, d=deg G<=D+v<=(k+1)D. There are at most two dense
factorization calls per level (G and V), hence at most 2b calls, each degree
at most (b+1)D. The aggregate dense input degree is O(b^2D). The previous
Berlekamp reduction gives at most O(b^2D) prime-field oracle calls when using
the direct p-fixed algebra, and oracle degree at most (b+1)D; alternatively
the trace-coordinate reduction has its documented extra m factor.

Padé matrices have size at most 2max(1,(b+1)D) by that quantity plus one.
Their entries have exactly m prime coordinates, each at most L bits. The
largest residue product has degree C=(t-1)(b+1)D; all remaining dense
linear algebra and polynomial products have dimensions polynomial in C.
Known-root quotient fields have delta<=(b+1)D and m*delta prime coordinates.
All exponents, signed weights, and final multiplicities have O(b+log(b+1))
bits. Coefficient inverse Frobenius is powering by p^(m-1), using O(mL)
field multiplications. No integer factorization, primitive root, random point,
GRH, or field-element enumeration occurs in the reduction.

For a deliberately loose explicit bookkeeping bound, put
M=1+t+b+D+m+L. Excluding dense factorization and the representation check,
M^20 schoolbook bit operations suffice for the operations just listed. The
total is at most 2b times the dense-factor bound at degree (b+1)D plus this
polynomial (with a larger absolute constant). Substituting the audited prime
bound gives an enormous polynomial, with no practical-efficiency promise.

## Reproducible current checks and limitations

code/sparse_cartier.py implements the reduction with a bounded exhaustive
prime oracle. code/test_sparse_cartier.py has seven check families, including
960 exhaustive small monic dense comparisons, extension coefficients,
1026-bit degrees, p-divisible multiplicities, and signed cancellations. The
example over F_2 with U=X^3+X^2+1 introduces W=X+1 although X+1 is absent
from the original polynomial; the factor ledger cancels it. In F_3,
(X-1)^(7+3^(k+1))(X+1)^2 forces a negative residue even for huge k.

Independent scripts and notes remain separate evidence. Neither these checks
nor a clean agent review establish priority. Exact attribution of the bounded
denominator invariant, applicability to previous sparse squarefree methods,
and the final paper/package are still under audit. No publication eligibility
or practical runtime claim follows at this candidate stage.
