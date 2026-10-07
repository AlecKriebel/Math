# Author approach 2: the once-punctured super-Kähler line test

Problem 30004711. 7 October 2026. This is the second directed mathematical approach. Approach 1 and its correction are preserved unchanged.

## Aim

Avoid the arbitrary connection-deformation step entirely in the smallest stable case (g,n)=(1,1), L=0. The corresponding complex supermoduli dimension is 1|1. In this dimension, a verified super-Kähler description of the actual torsion form would determine its Euler representative pointwise in a canonical holomorphic splitting.

The local calculation below succeeds, and the actual odd-spin bundle can be identified explicitly. Applying the calculation to the OWR torsion measure still requires a particular super-Kähler/odd-metric identification not established by the inspected punctured-surface sources. We do not infer it from the word “Weil–Petersson,” from negative-definiteness of the odd block, or from a bundle isomorphism.

## 1. Why odd complex rank one is special

Let X be a complex supermanifold of dimension 1|1 over the ordinary complex numbers. Its local structure sheaf is O_U[theta], theta^2=0. Every even holomorphic function has no nilpotent term: there is only one odd generator. Therefore changes of holomorphic coordinates have the form

z'=f(z), theta'=a(z)theta,

with a nowhere zero. The even subalgebra is canonically O_(X_red), giving a canonical holomorphic retraction. This statement also holds equivariantly in orbifold charts. In contrast, for odd rank at least two an even theta_1 theta_2 correction is possible.

On the associated smooth complex-supermanifold description the variables theta and conjugate(theta) are both present, so their product is nonzero. Nevertheless, the retraction induced by the holomorphic atlas is fixed; a non-holomorphic change z -> z+b theta conjugate(theta) is not another allowed holomorphic chart transition.

Thus a pointwise Berezin-density calculation in this holomorphic splitting does not require the exact-deformation invariance rejected in Approach 1.

## 2. Direct Berezinian calculation

Assume the actual even real super-symplectic form is locally a super-Kähler form with potential

K(z,bar z,theta,bar theta)=K_0(z,bar z)+h(z,bar z) bar theta theta,

where g=partial_z partial_barz K_0 is nonzero and h is the nonzero Hermitian line coefficient. A fixed overall odd sign can be absorbed into the orientation convention. There are no higher even odd monomials in this dimension.

Use left odd derivatives and order u=bar theta theta. The complex metric supermatrix is

G_zzbar = g+h_zbarz u,
G_zbartheta = h_z theta,
G_thetabarz = -h_barz bar theta,
G_thetabartheta = h.

Since theta bar theta=-bar theta theta,

(G_zbartheta)(G_thetabartheta)=h_z h_barz u.

The Schur-complement definition of the Berezinian therefore gives

Ber(G)=g/h + [h_zbarz/h-h_z h_barz/h^2] u
      =g/h + (partial_z partial_barz log h) u.

After Berezin integration, the body metric g cancels from the top odd coefficient. With the ordinary Euler normalization and the Berezin orientation fixed to the underlying complex orientation, the resulting two-form is the Chern form of the odd line with metric h. Reversing that orientation changes its sign. The 1/(2 pi) factor is the one in SW (A.6) for real odd rank two, not an adjustable genus-one factor.

This is a local identity of differential forms, not an equality only after passing to ordinary cohomology. It globalizes through the holomorphic line transition law because the mixed derivative of log|a(z)|^2 vanishes wherever a is nonzero. It introduces no comparison-boundary term of its own.

For an actual comparison, let h_tau and h_can denote the two Hermitian coefficients on the same identified holomorphic line. In this setting their Euler-density difference is, up to the already fixed curvature/orientation convention,

-(i/(2 pi)) partial barpartial log(h_tau/h_can).

It vanishes pointwise if the ratio is a positive constant, and more generally if its logarithm is pluriharmonic. A constant rescaling of the odd metric cannot repair a factor of two in this genus-one integral: it does not change the curvature. Nor does uniform scaling of the full super-symplectic form, since the real superdimension is 2|2 and its Berezin volume has scaling exponent (2-2)/2=0. Different stack, parity, or overall measure conventions remain separate possibilities.

## 3. The actual odd-spin bundle in genus one

This subsection concerns the canonical algebraic bundle and its standard compactification, not the torsion representative.

Let B be the odd-spin component of the compactified genus-one, one-marked spin stack. Write pi:C->B for its coarse universal stable curve, p for the section, and lambda=pi_*omega_(C/B) for the Hodge line. Every fibre is a smooth elliptic curve or an irreducible nodal genus-one curve. The odd theta characteristic is trivial on a smooth elliptic fibre; its stable degeneration is the Ramond-node, locally free trivial theta characteristic. This is the odd boundary type also specified in Norbury 2608.25237v2, p.40.

Let ell be the coarse theta line. Its restriction to each such fibre is trivial, so cohomology and base change and the evaluation map give ell=pi^*H for a line H on B. The genus-one relative dualizing sheaf is pi^*lambda; hence H^2=lambda. This is a relation on the spin stack (or a local chart carrying the square root), not a claim that lambda has a square root on the coarse modular curve.

At the NS marked stack point, invariant pushforward of theta^dual is ell^dual(-p). At the Ramond node the theta representation is trivial, so no additional nontrivial-character correction is inserted there. Consequently

F|B=R^1 pi_*(ell^dual(-p))
    =H^-1 tensor R^1 pi_*O_C(-p).

Apply pi_* to 0->O_C(-p)->O_C->O_p->0. The map pi_*O_C -> pi_*O_p is the identity on O_B, while pi_*O_C(-p)=0. It follows that

R^1 pi_*O_C(-p)=R^1 pi_*O_C=lambda^-1

by relative Serre duality. Thus

F|B=H^-1 tensor lambda^-1=H^-3,
F^dual|B=H^3,
c_1(F^dual|B)=(3/2)c_1(lambda).

The generic degree B->Mbar_(1,1) is 1/2: there is one odd theta characteristic and its scalar automorphism group has order two. Retaining this stack degree and integral_(Mbar_(1,1))lambda=1/24 yields

integral_B c_1(F^dual)= (3/2)(1/2)(1/24)=1/32.

This derives the odd contribution directly from the universal genus-one line bundles. It agrees with, but does not use the graph-sum arithmetic producing, the odd value in 2608.25237v2, pp.39–40. That source also gives the same canonical contribution from the even component. Their sum is the previously checked W_(1,1)=1/16.

If the actual torsion form satisfies the hypotheses of section 2 with this canonical metric and the same stack convention, its contribution on B is therefore +1/32 or -1/32 according to the verified orientation. No claim that those hypotheses hold has been inserted into this computation.

## 4. The harmonic-projection version of the same test

The Chern characterization gives another precise route. Let a Hermitian holomorphic line E be realized inside a Hermitian Hilbert bundle with a specified metric connection D, and let P be orthogonal projection. The projected connection nabla=P D is metric. It is the Chern connection on E if and only if its (0,1) part is the given holomorphic structure.

In a local holomorphic frame s with H=<s,s>, the condition is

P D^(0,1)s=0,

or equivalently <s,D^(0,1)s>=0. Metric compatibility then forces the (1,0) coefficient to be partial log H, the Chern coefficient. Conversely, the Chern connection has this vanishing (0,1) part. This proves the criterion, not just its necessity.

For the odd component above, s is a local frame of H^3=F^dual. Identifying the hyperbolic harmonic-projection line with H^3 is not enough: the base-direction derivative D^(0,1)s still has to be computed. Holomorphicity of a 3/2-differential in the *surface* coordinate does not imply its projected derivative vanishes in a *moduli* anti-holomorphic direction. Also, the derivative of a varying Hilbert space must first be specified as a metric connection; a bare derivative in an arbitrary smooth trivialization is not automatically metric.

These are the concrete checks needed to promote the projection construction of Norbury 2608.25237v2, section 4.1.3, into the Chern construction. The source itself calls the equality of the resulting measures conjectural. We have not computed that moduli-direction derivative or identified this connection with the torsion-induced one.

## 5. Source check and unresolved hypotheses

Norbury 2005.04378v4, p.36, equation (40), gives the canonical 3/2-differential Petersson metric and discusses a super extension. Stanford–Witten Appendix A.1, PDF p.111, footnote 67, relates the real odd block to the negative-definite block in Penner–Zeitlin's super symplectic construction. Neither statement alone proves that the entire actual form is type (1,1) in the canonical complex splitting of the once-NS-punctured torus.

A targeted primary-source check located Uehara–Yasui's [“On the symplectic geometry of the super Teichmüller space”](https://lib-extopc.kek.jp/preprints/PDF/1990/9010/9010555.pdf) (preprint YITP/U-90-16, later [Communications in Mathematical Physics 144 (1992), 53–86](https://doi.org/10.1007/BF02099191)). The inspected July 1990 preprint restricts its construction to compact super Riemann surfaces of genus at least two (printed p.2 / PDF p.2). It constructs a super-Hermitian pairing and proves closedness, while its conclusion explicitly leaves nondegeneracy unproved and refers elsewhere for integrability of the complex structure. The published abstract confirms closedness; the revised 1992 full text was not inspected, so these preprint caveats are not asserted of the final article. Neither source inspection establishes the once-punctured genus-one case or the Goldman/torsion identification. In the preprint, the closed-surface group presentation and all-elements-hyperbolic assumption occur on printed p.4 / PDF p.3; the harmonic reproducing calculation, equation (51), is on printed p.13 / PDF p.7. Extending the proof to NS cusps would require the relevant boundary and unfolding/variation hypotheses to be verified, not merely the same local formula to be written down.

Thus the successful local theorem is conditional on three actual identifications:

1. The genus-(1,1) NS torsion/Goldman form is super-Kähler for the stated complex supermoduli structure, including the correct treatment of its cusp.
2. Its odd Hermitian coefficient is the canonical metric (or has pluriharmonic logarithmic ratio to it) on the correctly dualized line.
3. The integration uses the same holomorphic retraction, spin-stack convention, and checked orientation/parity normalization.

None of these is replaced by matching a recurrence. Even accepting a super-Kähler theorem for closed genus>=2 would not prove item1 here.

## Outcome

This approach produces a pointwise representative-comparison mechanism specialized to the actual lowest stable genus, an explicit identification F_odd^dual=H^3 with H^2=lambda, its canonical 1/32 stack integral, and an exact (0,1)-connection test. The current source check does not establish the punctured super-Kähler/metric hypotheses or evaluate the hyperbolic projection derivative. Consequently it does not resolve the literal OWR formula, but reduces the prospective proof to these specific verifiable statements without the invalid arbitrary-connection shortcut.

Supported count: two directed mathematical approaches completed; original torsion statement still pending. No final unsuccessful disposition or solved-as-written claim is made.
