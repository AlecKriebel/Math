# Turn 5: effective bounded reconstruction and the missing topological measurements

**Result:** an explicit finite-jet reconstruction theorem and a weighted
root-grid reconstruction theorem for a numerator with a known genus bound.
These explain exactly how to remove the algebraic ambiguity, but the
required measurements have not been independently constructed from the
knot topology. The original problem remains unresolved after 5/5
substantive attempts.

## 1. A degree bound changes the problem

Ohtsuki (2007), Theorem 4.7, proves deg_x Theta_K(x,y)<=2g(K).
Simultaneous inversion supplies the corresponding lower bound; permutation
symmetry gives the same bound for y. The distinction between a summed and
averaged numerator is a nonzero scalar and does not affect this support
bound. Any known Seifert-surface genus g is an admissible upper bound.

Thus the relevant numerator is supported inside

[-d,d]^2 ∩ Z^2, where d=2g.

Theta symmetry actually restricts it further to |a-b|<=d, giving a hexagon.
For a simple rigorous reconstruction we use the larger square. The
unbounded-degree examples in Turn 3 do not contradict this bounded claim.

## 2. Explicit reconstruction from logarithmic derivatives

Let F(x,y)=sum_{a,b=-d}^d c_ab x^a y^b. Define the exact logarithmic moments

M_ij = (partial_h^i partial_k^j F(e^h,e^k)) at h=k=0
     = sum_{a,b=-d}^d c_ab a^i b^j.

**Proposition 4.** The moments with 0<=i,j<=2d determine all c_ab.
For a in {-d,...,d}, let

L_a(T)=product_{s=-d,...,d; s != a} (T-s)/(a-s)
      =sum_{i=0}^{2d} ell_(a,i) T^i.

Then the reconstruction formula is

c_ab=sum_{i,j=0}^{2d} ell_(a,i) ell_(b,j) M_ij.

Proof. Substitute the moment expression and interchange the finite sums.
The coefficient multiplying c_rs is L_a(r)L_b(s), which is 1 for
(r,s)=(a,b) and 0 otherwise. ∎

In particular a total logarithmic Taylor jet through degree 4d=8g is
sufficient, since it contains this rectangular collection of derivatives.
This is a sufficient bound, not an optimal one. It does not require an
exhaustive search over knots or unknown coefficients.

For the rational function R_K=F/[Delta(x)Delta(y)Delta((xy)^-1)], a jet
of the same total order of R_K is sufficient once Delta is known: multiply
the formal jet by the known denominator. That denominator has constant
term 1. This is exact formal-power-series algebra, with no analytic
continuation or convergence assumption.

## 3. A finite weighted residue transform also works

Choose an integer N>2d and put zeta=e^(2 pi i/N). For residues r,s mod N
define

B_(r,s)(F)=1/N^2 sum_{u,v=0}^{N-1}
                   zeta^(-r u-s v) F(zeta^u,zeta^v).

Character orthogonality gives

B_(r,s)(F)=sum_{a=r mod N, b=s mod N} c_ab.

Because N>2d, distinct integers in [-d,d] have distinct residues mod N.
Thus c_ab=B_(a mod N,b mod N)(F). All coefficients are recovered at a
single grid size once the weighted data are known.

For rational-function samples, take a prime N>max(2d,deg(Delta)+1),
where deg(Delta) means the degree after clearing its Laurent monomial.
Then a nontrivial N-th root has minimal polynomial of degree N-1 greater
than deg(Delta), so Delta cannot vanish there. It also does not vanish at
1. Multiplying each sample by the known denominator gives the samples of F.

The ordinary branched-cover Casson–Walker formula supplies an unweighted
sum, not these individually character-weighted observations. It is invalid
to infer the B_(r,s) from the one unweighted sum by Fourier inversion.
Fourier inversion is available only *after* the weighted data have been
obtained from an additional construction.

## 4. Why this is not yet the requested construction

Two potential implementations remain incomplete:

1. Supply the finite moments by a direct geometric construction and prove
   that they are the coefficients of the exact theta component in source
   equation (26). Merely obtaining them from the Kontsevich integral is
   a finite evaluation algorithm for the invariant already defined there.
2. Construct the weighted observations B_(r,s) using extra topological
   structures on covers or a genuinely equivariant configuration count,
   then prove the required equality. Ordinary cover Casson invariants
   do not include the missing character labels. We have not built such
   a refined invariant or proved its comparison.

The relative-comparison formula in Turn 4 is another useful reduction,
but it leaves its own reference-class constants. No argument here turns
these constants or weighted moments into known topological quantities.

## 5. Exact checks and final disposition

`verify_reconstruction.py` constructs the Lagrange polynomials using
rational arithmetic, verifies their interpolation identities, reconstructs
deterministic Laurent polynomials on bounded hexagonal supports, and
checks the modular no-alias condition. The written proof establishes the
result for all d; the finite controls guard the implementation.

**Final disposition: unsolved, 5/5.** The packet contains scoped algebraic
obstructions, a credited relative comparison, and finite reconstruction
criteria. It contains neither a new topological construction of P_K^theta
for arbitrary knots nor a counterexample to its existence. No priority or
novelty claim is made for the auxiliary results.
