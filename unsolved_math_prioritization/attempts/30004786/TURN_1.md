# Author turn 1: the precise Mellin implication under genuine theta inversion

**Conditional partial theorem. The weak invariant-functional premise printed in OWR is not silently strengthened.**

The first route attempts the expected Tate-style argument using the actual source-defined spaces. It succeeds under a genuine theta inversion identity, as intended in the published restricted-space refinement, but leaves the gap between that identity and the weaker OWR statement explicit.

## 1. Input and conventions

Let k be a number field of degree d, let A be its adeles, and let G,rho,sigma and the local transferred GL_n representations pi_v be as in SOURCE_CHECKPOINT.md. Assume the local reciprocity/contragredient compatibility needed for those definitions, and the uniform Satake bounds of Jiang–Luo Assumption5.1 for pi and its dual. Their Theorem6.2 supplies the latter bounds in the stated unitary-sigma setting. No global automorphy of pi is assumed.

Use the source's local Haar, additive-character, basic-function and Fourier conventions. In particular,

Z_v(s,phi_v)=integral_(k_v×) phi_v(x)|x|_v^(s-1/2) d×x,

Z_v(1-s,F_v phi_v)=gamma_v(s) Z_v(s,phi_v),

gamma_v(s)=epsilon_v(s) L_v(1-s,dual pi_v)/L_v(s,pi_v).

These are the cited local Godement–Jacquet consequences, not conclusions of this attempt. At all but finitely many finite places the basic function has Z_v=L_v and its Fourier transform is the dual basic function.

The added global hypothesis for this theorem is the **actual identity**

Theta_phi(x)=Theta_(F phi)(x^-1)

for every x in A× and every pure tensor phi with a compactly supported local component at one chosen finite place v1 and a compactly supported Fourier-transformed component at another finite place v2. The components elsewhere belong to the prescribed restricted Schwartz space. It suffices to assume the identity for one such nonzero-Mellin pure tensor constructed below. This is an explicitly stronger input than mere existence of two unspecified intertwined invariant functionals.

## 2. Rapid decay at the large-norm end

The local estimates in Jiang–Luo Lemmas5.2–5.3 and the proof of Theorem5.4 give, for a fixed pure tensor phi, a real b and a fractional ideal Lambda in k such that:

- the finite-adelic part, multiplied by |x_f|^b, is uniformly bounded and supported in a product fractional ideal
- the Archimedean function Psi(y)=|phi_infinity(y)| |y|_infinity^b is bounded near coordinate zeros and decreases faster than every inverse polynomial in the Euclidean norm at infinity

The same facts hold for F phi with its dual local data. Only value bounds, not an assertion of smoothness across Archimedean coordinate zeros, are needed here.

The norm-one idele class group C_k^1 is compact. Choose a compact set of representatives in A^1; its existence follows from finiteness of the ideal class group and the Dirichlet unit theorem, as in the classical adelic theory. Choose the norm section a(r) with finite coordinates1 and each Archimedean embedding multiplied by r^(1/d). Its adelic norm is r, with the usual squared absolute value at complex places.

For representatives c in that compact set, the relevant rational elements alpha have their Archimedean images in one fixed fractional-ideal lattice Lambda; allowing all such alpha only enlarges the bound. The finite weighted-function bounds are uniform in c. The product formula gives

|Theta_phi(c a(r))| ≤ C r^(-b) sum_(alpha in Lambda minus{0}) Psi(r^(1/d)c_infinity alpha).

Multiplication by c_infinity has a uniform positive lower singular-value bound on this compact set. For every integer M>d, the last sum is at most

C_M r^(-M/d) sum_(alpha in Lambda minus{0}) ||alpha||^(-M),

which is finite. Taking M arbitrarily large proves uniform decay O(r^-A) for every A as r increases to infinity. This is the same elementary lattice bound underlying the cited theta-convergence proof, with the radial parameter retained. It does not use global automorphic transfer.

## 3. Entire theta Mellin integrals

Under the added theta inversion hypothesis, rapid large-norm decay for F phi implies rapid small-norm decay for Theta_phi, uniformly over C_k^1. The same identity, with x inverted, gives both tails for Theta_(F phi).

Therefore

Z_global(s,phi)=integral_(k×\\A×) Theta_phi(x)|x|_A^(s-1/2) d×x

is entire in s, and likewise for F phi. Uniform rapid bounds on compact s-strips justify differentiation under the integral, including every logarithmic factor. The quotient Haar measure is induced by the product local multiplicative Haar measure and counting measure on k×; its normalization is not arbitrarily changed.

For Re(s) sufficiently large, absolute convergence permits unfolding:

Z_global(s,phi)=integral_(A×) phi(x)|x|_A^(s-1/2)d×x
              =product_v Z_v(s,phi_v).

For the dual integral the analogous equality holds in its own right half-plane. Inversion on the abelian idele class group preserves Haar measure and changes the exponent to1/2-s. The genuine theta identity thus gives the entire identity

Z_global(s,phi)=Z_global(1-s,F phi).

## 4. A permitted test with nonzero Mellin multiplier

Choose distinct finite places v1,v2 and a finite set S containing them, all Archimedean places, and every ramified representation or additive-character place. At v1 use the characteristic function of the local unit group, which belongs to C_c^infinity(k_v1×) and has nonzero constant Mellin integral. At v2 choose eta_v2 in C_c^infinity(k_v2×), again the unit characteristic function, and set

phi_v2=F_(dual pi_v2,psi_v2^-1)(eta_v2).

The local inverse identity makes F_v2 phi_v2=eta_v2. Its Mellin integral is the nonzero meromorphic function Z_v2(1-s,eta_v2)/gamma_v2(s); no nonvanishing at every individual s is needed.

At the remaining exceptional finite places choose compactly supported unit functions; at Archimedean places choose nonnegative nonzero compactly supported smooth functions on k_v×. Their Mellin integrals are not identically zero. These functions belong to the source Schwartz spaces because C_c^infinity is a subspace. At all remaining places take the basic functions. The resulting phi satisfies the two-place condition, and every exceptional Mellin factor is nonzero as a meromorphic function.

Write

P_phi(s)=product_(v in S) Z_v(s,phi_v)/L_v(s,pi_v).

It is a finite nonzero meromorphic product. In the original convergence half-plane,

Z_global(s,phi)=L(s,sigma,rho) P_phi(s).

Thus the quotient of the entire theta Mellin integral by P_phi supplies meromorphic continuation of the completed automorphic L-function to C. Local factors are included; this is not merely a continuation of an incomplete Euler product. The corresponding dual statement follows from the entire integral for F phi. Zeros of the finite multipliers are handled by meromorphic division, not by asserting they never vanish.

## 5. Epsilon normalization and global functional equation

Local functional equations give

P_(F phi)(1-s)=epsilon(s,sigma,rho) P_phi(s),

where the global epsilon factor is the finite product of the exceptional local factors; the unramified normalized factors equal1. Combining this with the entire theta-Mellin identity yields

L(s,sigma,rho)P_phi(s)
 =L(1-s,dual sigma,rho) epsilon(s,sigma,rho)P_phi(s).

Cancellation of the nonzero meromorphic multiplier proves the expected meromorphic functional equation. Cancellation is an identity in the meromorphic function field and remains valid at its isolated zeros and poles by continuation.

## 6. Exact scope and remaining original gap

This supplies the analytic implication from genuine restricted theta inversion, with standard local data and source growth bounds, by a direct generalization of the classical Tate mechanism. Those classical/local ingredients are credited; no novelty is claimed.

OWR Conjecture1.3, as actually printed, only posits unspecified nontrivial k×-invariant linear functionals related by Fourier transform. It gives neither their agreement with Theta nor finite boundary asymptotics. The proof above does not derive the genuine theta identity from that weak premise. The published Conjecture7.4 is a more informative refinement, and converting its functional notation to the displayed theta identity also requires retaining its translation and two-place conditions. That distinction is the next substantive target, rather than being hidden inside the word Poisson.

One substantive author turn complete. Original weak-premise implication remains unresolved; four turns remain unless a complete source-scoped resolution is obtained sooner. Completion estimate25%.
