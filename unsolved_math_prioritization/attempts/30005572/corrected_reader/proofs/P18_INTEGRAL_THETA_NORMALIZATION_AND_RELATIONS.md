# Integral theta normalization and genuine torsion relations

**Shared PASS 3/5, row 1777 / 30005572. Partial result. The full construction remains UNSOLVED.**

The coefficient ring is always R = Z[1/6]. No assertion below divides by a level prime in K₂. In particular a relation for powered theta values is not promoted to a relation for their roots. The arguments are not claimed to be new.

## 1. Results and precise scope

1. Genuine normalized auxiliary theta functions give canonical **powered** theta values U_n(P) in k×⊗R for every nonzero rational n-torsion point on an elliptic curve. Their definition uses an integral Bezout identity, not a chosen algebraic root. They satisfy f_m(P) = ((m²−1)/n) U_n(P) for m≡1 mod n.
2. CM endomorphisms improve this normalization. If the annihilating ideal N has no rational prime p≥5 with (p)|N², they give canonical **unpowered** theta values in k×⊗R. This includes arbitrary powers of one member of a split conjugate pair. The norm-coefficient ideal is proper at every excluded p, so this particular Bezout construction cannot remove those primes. That failure is not a counterexample to another normalization.
3. These actual values satisfy an exact cross-ratio identity. For four distinct points modulo sign, an eight-value theta monomial equals the geometric cross-ratio, or its specified power. This yields a genuine torsion-specialized relation: |G|² annihilates the theta triangle for every finite subgroup G on which the construction is defined. When |G| is a unit of R, the triangle itself is zero. Thus for 2,3-primary torsion the unpowered triangle holds over R, with no additional coefficient localization.
4. The first nontrivial cyclic odd case also has an exact result: the scalar-powered order-seven values U_7 obey the unmultiplied triangle. The proof cancels seven only in a torsion-free **universal unit group**, not in K₂. It does not cancel 49 on an unpowered K₂ triangle.
5. At the −23, q²|4 test studied in the residue lane, the genuine theta value is f_5(P)/24. The pair has smoothing factor 624, whereas the raw auxiliary pair has factor 576. The missing 48 comes from the two mixed Steinberg terms. This is an exact algebraic normalization check, not an identification with the accepted geometric cocycle.

No all-level ray-field root construction, all-component face presentation, agreement on endpoint-balanced absolute cycles, or geometric-cocycle calibration is asserted. No accepted proof, ledger, queue, or remote was changed.

## 2. Auxiliary theta functions over R

Use additive notation for multiplicative groups tensored with R. If E/k is an elliptic curve in characteristic zero and α is a nonzero endomorphism defined over k, put

m_α = deg(α),    D_α = m_α(0) − E[α].

There is a unique normalized f_α ∈ k(E)×⊗R with divisor D_α which is fixed by the norm maps [r]_* for all positive integers r relatively prime to deg(α). The usual normalized auxiliary theta is this element. The same convention gives f_m for the scalar endomorphism [m], of degree m².

Here is an elementary verification that this one-dimensional normalization needs only R, independently of the separate two-dimensional five-primary issue.

The sum of the elements of a finite abelian group is killed by two. Consequently the degree-zero divisor class of D_α in Pic⁰(E) is killed by two. Thus 2D_α is principal over k, and there is f₀ ∈ k(E)×⊗Z[1/2] with divisor D_α. Rationality follows from the rational zero section and descent of a principal divisor (equivalently Hilbert 90).

For r coprime to deg(α), multiplication by r permutes E[α], hence [r]_*D_α=D_α. Write c_r=[r]_*f₀−f₀ ∈ k×⊗R. Commuting norms gives

(s²−1)c_r = (r²−1)c_s.

The ideal generated in R by r²−1 for such r is R. Indeed, for any prime l≥5 one can choose r coprime to deg(α) with r²≠1 mod l: use r≡2 mod l when l divides deg(α), and r≡0 mod l otherwise, adjusting by CRT at the other primes. Thus a finite relation Σ b_r(r²−1)=1 exists in R. Put c=Σ b_r c_r and f_α=f₀−c. Then [s]_*f_α=f_α for every permissible s. Any two choices differ by a constant annihilated by all s²−1 and hence are equal.

This also proves functoriality under field extension and isomorphisms. If β is a CM endomorphism prime to α, then [β]_*f_α−f_α is constant; it is fixed by all scalar traces prime to αβ, so is zero. Thus the scalar normalization is also the full-CM norm normalization. All uses of pullback/norm commutation below use scalar r prime to the degrees involved, where the corresponding finite-isogeny square is Cartesian.

In particular f_α(−P)=f_α(P) in k×⊗R, and f_α(εP)=f_α(P) for a CM unit ε. This can also be seen from the divisor and uniqueness. No value at P=0 is assigned.

### Exact compatibility

For commuting endomorphisms α,β, divisor comparison gives

m_β f_α − β* f_α = m_α f_β − α* f_β.                 (2.1)

Indeed, both divisors are

m_αm_β(0) − m_β E[α] − m_α E[β] + E[αβ].

Their difference is a trace-fixed constant, hence zero by the preceding uniqueness argument. If αP=βP=P≠0, evaluation is defined and gives

(m_β−1) f_α(P) = (m_α−1) f_β(P).                   (2.2)

## 3. Canonical scalar-powered values

Let nP=0 and P≠0. For positive integers m>1 with m≡1 mod n, set a_m=(m²−1)/n. The a_m generate R. To check this, for a prime l≥5 dividing n choose m=1+tn with t≠0 mod l; then a_m=t(2+tn) is nonzero mod l. For l not dividing n choose m≡1 mod n and m≡0 mod l. Extra coprimality to 6 can be imposed if desired and does not change the argument at primes ≥5.

There is a torsion issue that must be settled **before** making a Bezout definition: (2.2) initially gives only n(a_l f_m(P)−a_m f_l(P))=0. It is not legitimate to cancel n in an arbitrary specialized unit group.

The required canceled exchange

a_l f_m(P)=a_m f_l(P)                              (3.0)

is instead proved before specialization. If P has exact order e≥4, use the universal elliptic curve and its exact order-e point over Q(Y₁(e)). This modular curve is geometrically integral over Q, so its function field has constant field Q. Its multiplicative group, after tensoring with R, is torsion-free. For m,l≡1 mod n, where e|n, (2.2) therefore implies (3.0) in this universal unit group. The normalized auxiliary theta evaluations are genuine units on Y₁(e): their zero/pole divisors are auxiliary torsion, disjoint from the e-torsion section. Thus the identity specializes to every characteristic-zero (E,P), including fields with level-primary roots of unity. No cancellation after specialization is being made.

If e=2 or 3, first use e∈R× and (2.2) to construct θ(P) by a Bezout combination of the coefficients m²−1 for m≡1 mod e; these coefficients generate eR=R by the preceding elementary argument. Then f_m(P)=(m²−1)θ(P) for this whole family. Formula (3.0) follows directly for its subset m≡1 mod n. This also handles nonexact annihilating integers n in the small-order cases.

Now choose finitely many r_m∈R with Σr_m a_m=1 and define

U_n(P) = Σ r_m f_m(P) ∈ k×⊗R.                     (3.1)

The proved universal exchange (3.0), rather than uncanceled (2.2), proves

f_m(P)=a_m U_n(P),                                 (3.2)

for every permissible m. These equations uniquely determine U_n(P), so the definition is independent of the Bezout choices. It is functorial, even, and invariant under automorphisms of the marked elliptic curve.

If n|n′ and nP=0, then

U_{n′}(P)=(n′/n)U_n(P).                            (3.3)

To prove this, apply (3.2) to the subset m≡1 mod n′ and use that the corresponding a_m for n′ generate R. Thus U_n(P)/n is independent of n after that division is permissible. For n having only prime factors 2 and 3, it gives an actual canonical value

θ_E(P)=U_n(P)/n ∈ k×⊗R.                            (3.4)

At other levels, (3.1) defines a powered theta and does not define its n-th root over R.

Here is a direct justification of the family-unit assertion used above. On the smooth universal elliptic surface over Y₁(e), a generic normalized f_m has the prescribed horizontal divisor m²(0)−E[m], together with possible vertical fiber divisors. Every fiber is smooth and irreducible. Under [r]_* for r coprime to m, the horizontal divisor is unchanged, whereas each vertical fiber coefficient is multiplied by r². Norm invariance therefore forces every vertical coefficient to be zero. After clearing only powers of 2 and 3, the rational function is consequently an actual unit away from E[m]. Restriction at the disjoint e-torsion section is defined everywhere on Y₁(e). Norms commute with this smooth-family base change, and uniqueness identifies each specialized function with the normalized fiber function. Thus the universal identities used for scalar U_n and for order seven really do specialize at every elliptic moduli point. This is also the standard family form of auxiliary theta used in [SV, §§6.3,7.3].

## 4. CM removes some level denominators without division

Assume End_k(E) contains the maximal imaginary quadratic order O, and N is a nonzero proper ideal annihilating P. Let I_N be the ideal of R generated by

Norm(α)−1,    0≠α∈O, α≡1 mod N.                  (4.1)

Suppose first that I_N=R. Choose finitely many r_α∈R with Σr_α(Norm(α)−1)=1 and define

θ_E(P)=Σr_α f_α(P) ∈ k×⊗R.                        (4.2)

Equation (2.2), without any canceled nonunit factor, gives

f_α(P)=(Norm(α)−1)θ_E(P) for all α≡1 mod N.         (4.3)

These equations uniquely determine θ_E(P), so its definition is independent of all Bezout choices. If n is a multiple of the exponent of O/N, comparison with the scalar family and (3.2) gives

U_n(P)=n θ_E(P).                                   (4.4)

Indeed, for m≡1 mod n, a_m(U_n−nθ)=0, and the a_m generate R. This equality is proved without dividing the specialized group by n.

If I_N=dR with d a nonunit, (2.2) only gives the exchange relation multiplied by d. A Bezout combination of (Norm(α)−1)/d does **not** automatically give a canonical powered CM value: specialized unit groups may have d-primary roots of unity. We make no such claim. The scalar-powered U_n of §3 remains available through its separate universal argument. This distinction corrects the initial frozen draft's cancellation gap.

### Exact unit-ideal criterion

I_N=R if and only if no rational prime p≥5 satisfies (p)|N².

For necessity, such a p is either inert and divides N, ramified with its prime dividing N, or split with both conjugate primes dividing N. Every α≡1 mod N then has Norm(α)≡1 mod p. Thus I_N⊆pR.

For sufficiency, fix p≥5 not satisfying (p)|N². If p does not divide Norm(N), CRT permits α≡1 mod N and α≡0 mod pO. If p divides Norm(N), it must split as q q̄ with only one of q,q̄ dividing N; CRT permits α≡1 mod N and α≡0 at the other prime. In both cases Norm(α)≡0 mod p, so p does not contain I_N. A nonzero ideal in R lying in no maximal ideal is R. The criterion follows.

This explicitly includes arbitrarily deep one-sided split levels. It does not assume class number one, because all α used are actual elements of O and no nonprincipal ideal is represented by a nonexistent scalar. The construction is carried out independently on each CM curve and is compatible with isomorphisms. It does **not** establish all nonprincipal-isogeny distribution laws needed for the contract.

At an excluded p, the proper ideal I_N is a proved obstruction to this specific unit-coefficient Bezout method. It is not proof that a theta root in k×⊗R, or an integral K₂ symbol, cannot exist by another construction.

### Unit descent, as distinct from K₂ descent

Let M/L be a finite Galois field of definition for a CM marked pair (E,P). Suppose every σ∈Gal(M/L) identifies (σE,σP) with (E,P) by an O-linear isomorphism. Then the valid unpowered value θ_E(P) when I_N=R, and the separately constructed scalar-powered U_n(P), descend uniquely to L×⊗R.

Indeed, functoriality makes the value Galois-fixed, and

(M×⊗R)^Gal(M/L) = L×⊗R.                            (4.5)

This equality uses flat localization commuting with the kernel of the finitely many maps σ−1. Equivalently, clear the finitely many powers of 6 in an invariant representative. No division by [M:L] occurs. The statement is a K₁ descent lemma; it does not assert analogous integral descent for K₂.

For application to the ray field one must supply the CM marking and its field-of-moduli identification with that ray field. The lemma explains precisely why, once that standard identification is made, this normalization needs no separate K₂ descent at the levels with d=1. This report does not replace the all-component CM-marking work in the contract by a claim of Galois invariance alone.

## 5. Exact specialized cross-ratio identity

Let a,b,c,d be torsion points whose images modulo ±1 are pairwise distinct. On a Weierstrass model put

u(a,b,c,d) = ((x(c)−x(a))(x(d)−x(b)))/((x(c)−x(b))(x(d)−x(a))),

with x(0)=∞ interpreted by the usual limiting cross-ratio. Thus u and 1−u are nonzero, and 1−u=u(a,c,b,d). No theta value at zero enters the formulas below.

For an even system h on the nonzero points, write

M_h(a,b,c,d) = h(c+a)+h(c−a)+h(d+b)+h(d−b)
              −h(c+b)−h(c−b)−h(d+a)−h(d−a),        (5.1)

in additive unit notation. All eight arguments are nonzero.

### Auxiliary identity

For an endomorphism α of degree m,

M_{f_α}(a,b,c,d) = m u(a,b,c,d) − u(αa,αb,αc,αd),  (5.2)

provided both cross-ratios are nondegenerate and the evaluations are defined.

Here is a divisor proof that retains constants. For variable z and fixed y, compare

f_α(z+y)+f_α(z−y)−2f_α(z)−2f_α(y)

with m(x(z)−x(y))−(x(αz)−x(αy)), in additive function notation. Their divisors in z agree. The quotient is constant in z. At z=0, use a local parameter t with x=t⁻²+O(t⁻¹), and leading term f_α=C t^{m−1} (after clearing powers of 6). Evenness shows that the resulting constant is independent of y: in multiplicative notation it is C⁻² times the inverse square of the tangent multiplier of α. Possible sign terms vanish in R. Taking this identity for (z,y)=(c,a),(d,b),(c,b),(d,a), with signs +,+,−,−, cancels all four constants and proves (5.2). The identity when one point is zero follows by the regular limit of the already-cancelled expression.

If α fixes all four points, (5.2) becomes M_f=(m−1)u. Consequently the Bezout definitions give the exact identities

M_{U_n}=n u,    M_θ=u when I_N=R.                   (5.3)

They hold in the actual specialized unit group, including its retained level-primary torsion. No root of unity was discarded at a level prime. This distinguishes (5.3) from an identity for analytically chosen theta roots only modulo roots of unity.

## 6. Genuine specialized triangle relations

Let G be a finite subgroup of E(k) annihilated by the level in question. Use one common valid system h=U_n or θ on G−{0}, as applicable. For algebraic bookkeeping only put h(0)=0 in the additive unit group; this is the multiplicative identity, not an evaluation at the theta origin. Define

Ψ(a,b)={h(a),h(b)}+{h(b),h(−a−b)}+{h(−a−b),h(a)}.

The intended nondegenerate triangle has a,b,a+b nonzero. We prove

|G|² Ψ(a,b)=0 in K₂(k)⊗R.                          (6.1)

In particular, if |G| has only factors 2 and 3, Ψ(a,b)=0. Together with §3, this proves an unpowered theta triangle over R for every 2,3-primary torsion subgroup on every characteristic-zero elliptic curve. It applies to actual CM torsion and is not a specialization inferred from a generic identity.

For completeness, the finite algebra giving (6.1) is recorded here. Work first in the exterior square of the additive unit group, and then map to K₂(k)⊗R. Set B(x,y)=h(x+y)+h(x−y), and

φ(x,y,z)=B(z,x)∧B(y,x)+B(y,x)∧B(z,y)+B(z,y)∧B(z,x).

Let δ(a,b,c,d) be M_h(a,b,c,d)∧M_h(a,c,b,d). For distinct points modulo sign, (5.3) makes this a scalar multiple of u∧(1−u), so its image in K₂ is zero. For repeated sign classes it is zero by direct expansion and evenness. Expanding the two monomials gives

δ(a,b,c,d)=φ(a,b,c)+φ(c,d,a)+φ(b,a,d)+φ(d,c,b).      (6.2)

For fixed y,z, Σ_{x∈G}φ(x,y,z)=0: the terms linear in the fixed B(y,z) cancel under translation; the remaining sums are negated by x↦−y−z−x and x↦y−z−x. Two is invertible. Summing (6.2) over d therefore shows |G|φ(a,b,c)=0 in K₂.

Put R_u(v)=Σ_{x∈G}Ψ(u+2x,v). Direct bilinear expansion gives, with c=−a−b,

Σ_x φ(x,−b−x,a−x)=|G|Ψ(a,b)+R_c(a)+R_b(c)+R_a(b),
4R_u(v)=Σ_x φ(0,v,u+2x).                           (6.3)

Multiply the first identity by |G| and use the second and |G|φ=0. Since 4 is a unit of R, (6.1) follows. These calculations use no cancellation of |G| in a torsion target. The included checker verifies every expansion and every degenerate case on several finite groups; the argument above is the general proof.

### An exact order-seven powered triangle

There is a stronger statement for U_7 on a cyclic subgroup of order seven:

Ψ_{U_7}(P,2P)=0.                                   (6.4)

The degenerate or repeated-sign triangles already vanish; the remaining triangles follow from this one by cyclic relabeling, evenness, and antisymmetry.

Prove this first on the universal elliptic curve over the function field K=Q(Y₁(7)). Put A=U_7(P), B=U_7(2P), C=U_7(3P) and u=u(0,P,2P,3P). Formula (5.3) says, multiplicatively,

B³/(AC²)=u⁷,    A²B/C³=(1−u)⁷.                     (6.5)

For r=B/A and s=C/A, it follows that

(r/(u³/(1−u)²))⁷=1,    (s/(u/(1−u)³))⁷=1.

The regular function field K has constant field Q and no nontrivial seventh roots of unity. Therefore K×⊗R has no seven-torsion, and

r=u³/(1−u)²,    s=u/(1−u)³.                        (6.6)

Thus Ψ(A,B,C)={r,s}=−7{u,1−u}=0. These are identities of universal units, so they specialize to any characteristic-zero field and any exact order-seven point, even when the specialized field contains μ₇. This use of a universal identity is important: absence of μ₇ was used in the generic unit group, not assumed for the specialized field.

For unpowered CM theta values satisfying M_θ=u, the same direct cross-ratio computation gives only 7Ψ=0. Equation (6.4) does not permit cancellation of 49 to prove Ψ_θ=0. This distinction is retained throughout.

## 7. The level-four calibration check and its limitation

For a point annihilated by four, m=5 gives a_5=(25−1)/4=6, a unit of R. Consequently

U_4(P)=f_5(P)/6,    θ(P)=f_5(P)/24.                 (7.1)

The same holds for every nonzero coordinate cP. Thus the genuine triangle of f_5-values at these torsion points vanishes: it is 24² times the theta triangle of §6. This is compatible with the previously proved nonzero generic auxiliary-theta triangle; a generic nonzero symbol need not have a nonzero torsion specialization.

For S={θ(cP),θ(dP)}, let A=f_5(cP)=24θ(cP) and B=f_5(dP)=24θ(dP). At this level the scalar 5 fixes the marking and its ray-class Artin action is trivial. The correct three-term smoothing is

{A,B}+{A,θ(dP)}+{θ(cP),B}
  =(24²+24+24)S=624S=(5⁴−1)S.                     (7.2)

The raw pair alone is 576S. Therefore replacing the full smoothing by the raw pair gives the wrong factor, even at this favorable level where the unpowered values themselves are integral over R.

The residue lane's separate −23, q²|4 calculation uses f_5=Δ²/ψ₅ in this normalization over R. Its source addendum identifies the Robert function with this expression up to a twelfth root of unity, which vanishes in the localized unit group; no level-primary root is discarded. Its raw pair residue is j̄⁴∈F₈×. Since 576≡2 mod 7, the normalized theta pair residue is j̄². The correct 624-fold smoothing has the same j̄² residue because 624≡1 mod 7. This is a consistency calculation with that lane's local result, not an independent audit of its division-polynomial computation.

None of (7.1)–(7.2) identifies the three-symbol expression with specialization of the accepted geometric cocycle on a global absolute cycle. That calibration remains a separate missing theorem. A nontrivial relative-edge residue is permitted by the contract's field-valued relative target and is not an obstruction to the required integral absolute map.

## 8. Remaining work and source boundary

The normalization above supplies actual unpowered values on a substantial but restricted family of levels. At levels with a retained common rational prime between N and its conjugate, the scalar construction produces powered U_n values and the CM coefficient calculation gives an exact failed Bezout ideal, not a canonical root. The more ambitious divided-coefficient CM powered construction is withdrawn because its exchange relation retains d-primary torsion. At favorable levels with odd torsion in G, the cross-ratio proof retains genuine K₂ torsion and does not prove all triangles. Even complete triangle relations would leave polygonal faces, non-Euclidean components, and agreement on all endpoint-balanced absolute cycles to be proved.

The accepted geometric auxiliary cocycle remains the calibration target. Its ordinary existence, and the scalar coefficient match (7.2), are not substitutes for equality with these relative symbols. No full map Π_N or Π̃_N has been constructed in this lane.

Primary sources used:

- Lecouturier–Sharifi–Shih–Wang, *Eisenstein cocycles for imaginary quadratic fields*, retained author PDF, §3.4; https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . Supplies the intended auxiliary theta and geometric-cocycle setting. Its published coefficient range is not silently changed by citation; §2 above supplies the one-dimensional R argument used here.
- Sharifi–Venkatesh, *Eisenstein cocycles in motivic cohomology*, §§6.3,7.3; https://math.ucla.edu/~sharifi/eisensymbol.pdf . Supplies the family form of normalized theta units. Its later localized comparison does not prove our missing geometric calibration.
- Goncharov, *Euler complexes and geometry of modular varieties*, Corollary 2.6 and Theorem 2.10; https://arxiv.org/pdf/math/0510310v5 . Its intrinsic roots are level-localized, and its rational triangle theorem is not used as an integral specialization theorem.
- Brunault, *On the K₄ group of modular curves*, arXiv:2009.07614v3, §§2–3; https://arxiv.org/pdf/2009.07614v3 . The cross-ratio strategy and finite algebra are closely related to this primary construction. His theorem is over Z[1/(6N)]; the present proof keeps the integral norm normalization and the remaining torsion explicitly. The retrieved PDF is recorded separately; no unsupported revision identity is inferred from the HTML rendering.

Executable checks: check_theta_relations.py; exact output: CHECK_RESULTS.json. These are finite algebra checks and cannot certify a K₂ nonvanishing assertion or the absent geometric calibration.
