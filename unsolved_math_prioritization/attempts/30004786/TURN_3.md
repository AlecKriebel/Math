# Author turn 3: extracting theta inversion from bilateral normalization

**A complete implication for a precisely stated refinement, not a silent interpretation of the weaker source conjecture.**

Turn1 assumed a genuine theta identity. This turn removes that assumption when the two Poisson functionals have the appropriate explicit theta normalization on both sides. It also tracks the Fourier square needed for the restricted test space.

## 1. Local Fourier square and compact support

Let b=(-1)^n in a local field F and let omega_pi be the central character of pi. In the source's fiber model, phi=phi_(xi,varphi) with xi(g)=|det g|^(n/2)f(g). Proposition2.6 and the classical additive Fourier square give

F_(dual pi,psi) F_(pi,psi) phi = phi_(xi(-·),varphi).

Changing variables h=-g in the determinant fiber has det h=b det g and preserves its Haar measure. Since varphi(-h)=omega_pi(-1)varphi(h),

F_(dual pi,psi) F_(pi,psi)=omega_pi(-1) R_b.       (1)

This derivation uses the actual source construction and not an unstated normalization of the local epsilon factor. The nonzero scalar and reflection preserve compact support in F×.

Consequently F_pi maps the source subspace S_pi-double-circle into the corresponding dual subspace: a compact local factor of phi becomes a compact local factor after applying the dual Fourier transform to F phi, by(1), while the compact local factor of F phi is already present by definition. The reverse inclusion follows by the inverse transform. The global scalar in the tensor product is well-defined, since unramified central characters are trivial at-1 at almost all finite places.

Translations R_x preserve the local Schwartz spaces. This follows directly by changing a determinant fiber representative and translating the original Schwartz function and matrix coefficient; equivalently it follows from the source local Mellin characterization. They preserve local compact support as well. With the covariance F R_x=R_(x^-1)F from turn2, they preserve S-double-circle globally.

## 2. State the added normalization precisely

Suppose E on S_sigma,rho and E_dual on its dual space satisfy:

(a) E(phi)=E_dual(F phi) for all phi in S_sigma,rho;

(b) E(eta)=Theta_eta(1) for every eta in S_sigma,rho-double-circle;

(c) E_dual(zeta)=Theta_zeta(1) for every zeta in the dual double-circle space.

These are bilateral theta restrictions. Their distributional extensions outside the indicated spaces need not be computed. This is the informative reading of the published refinement needed here. If only one of(b),(c) is assumed, or if the two functionals are chosen independently without this normalization, the conclusion below is not obtained by the argument.

For phi in S-double-circle and any x in A×, translation stability, Fourier covariance, and(a)–(c) give

Theta_phi(x)=E(R_x phi)
            =E_dual(F R_x phi)
            =E_dual(R_(x^-1)F phi)
            =Theta_(F phi)(x^-1).

Thus the restricted theta inversion required by turn1 follows with no boundary calculation. All domain changes are justified by Section1.

## 3. Conditional continuation and functional equation

Combining this identity with turn1 proves the desired completed-L meromorphic continuation and global epsilon functional equation under(a)–(c), the source local transfer assumptions, and its uniform growth bounds. The special test can have its two compactness conditions at distinct finite places, leaving the Archimedean factors free to provide ordinary nonzero Mellin integrals. No global automorphic transfer is used.

The result is stronger than a purely formal statement that a Poisson formula ought to imply continuation: it specifies the sufficient normalization, proves the necessary subspace stability, tracks the half shift and Fourier square, and supplies a test whose meromorphic multiplier can be canceled.

## 4. What this does not settle

The OWR Conjecture1.3 does not state(b) or(c). The published Conjecture7.4 introduces theta agreement on the restricted space; its paired notation is naturally intended symmetrically, but the proof here makes both sides explicit instead of using a one-sided sentence to infer an unstated condition. A formulation that literally supplies only one normalized functional would still need the other identification.

No argument in this turn constructs(b)–(c) from the weak transported functionals of turn2. Their orbit behavior is generally a single power of the norm, so they do not automatically satisfy the theta restrictions. The distinction is genuine: translation invariance under k× alone is much weaker than the prescribed values on this test-function space.

Three substantive author turns complete. The precise bilateral-refinement implication is proved, but the original weak-premise implication remains unresolved. Completion estimate40%. Next route: test whether identifying the two functionals in a self-dual situation salvages the weak premise, rather than assuming that extra symmetry supplies theta normalization.
