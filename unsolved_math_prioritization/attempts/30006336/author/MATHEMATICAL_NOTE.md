# What follows, and what does not

Use A,d,I,m,X,U and Δ as specified in SOURCE_GATE.md. Set C_Y=RΓ_Δ(Ŷ/A)
and M_Y^i=Hⁱ(C_Y). All groups below are integral unless explicitly localized.

## 1. A first-order deduction

**Proposition.** Under the source hypotheses, the restriction map satisfies

    image(M_X^i → M_U^i) ⊂ d M_U^i.

**Proof.** Write F=Ωⁱ_{X/Z_p}. It is a vector bundle because X is smooth.
Properness makes H⁰(X,F) a finite Z_p-module. The sequence
0→F --p→ F→F|_{X_Fp}→0 shows that H⁰(X,F)/p injects into
H⁰(X_Fp,F|_{X_Fp})=0. Nakayama's lemma gives H⁰(X,F)=0;
formal functions gives H⁰(X̂,Ωⁱ_{X̂/Z_p})=0 as well.

The Hodge–Tate comparison for a smooth p-adic formal scheme identifies the
cohomology sheaves of Δ/d with Ωʲ{−j}; the brace is the Breuil–Kisin twist,
an invertible module pulled back from the base. The local-to-global spectral
sequence is functorial under restriction. Since Û is affine and these sheaves
are coherent, its target in degree i is Ωⁱ(Û){−i}. The restriction map

    Hⁱ(C_X ⊗ᴸ_A A/d) → Hⁱ(C_U ⊗ᴸ_A A/d)

therefore factors through the edge term H⁰(X̂,Ωⁱ{−i})=0.
The long exact sequence of C_U --d→ C_U→C_U⊗ᴸ_A A/d now gives
ker[M_U^i→Hⁱ(C_U⊗ᴸ_A A/d)]=dM_U^i. This proves the inclusion. ∎

The comparison input is Bhatt–Scholze, Theorem 1.8(2)/Theorem 6.3; the
proposition is an elementary consequence of that known theorem, not a proposed
new theorem. It gives one divisibility step, not arbitrarily many.

## 2. Why lifting through Bocksteins needs additional work

For any A-complex C and r≥1 there is a triangle

    C⊗ᴸ A/d^r --d→ C⊗ᴸ A/d^(r+1) → C⊗ᴸ A/d.

The associated long exact sequence contains connecting maps from degree i−1
and i. Knowing that the last restriction map is zero supplies local or
cohomological lifts into the left-hand term. It does not assert that a chosen
lift is itself a restriction of a global class. Those lifts are not canonical:
the connecting maps control their ambiguity and obstruction.

There is a useful abstract criterion that makes the missing assumptions visible.
Let K be a complex of sheaves of A-modules on a space T, F=Hⁱ(K), and suppose:
(a) multiplication by d on F is injective; (b) H⁰(T,F/dF)=0; and
(c) the edge map Hⁱ(RΓ(V,K))→H⁰(V,F) is an isomorphism for the open V in question.
Then every restriction from Hⁱ(RΓ(T,K)) to Hⁱ(RΓ(V,K)) lies in dⁿ times the
target for every n. Indeed, 0→F --d→F→F/dF→0 makes multiplication by d
surjective on H⁰(T,F); iterate and then restrict using (c).

For integral prismatic K neither (a) nor (c) was established here. Affineness
alone gives (c) for the Hodge–Tate reduction because its cohomology sheaves are
coherent, but it does not give (c) for an arbitrary integral sheaf complex.
Without injectivity, global division has an obstruction in H¹(T,F[d]). This
is a specific lifting gap, not an additional hypothesis of the original question.

## 3. Frobenius and Nygaard: an attractive but unfinished route

For smooth affine formal schemes Bhatt–Scholze, Theorem 15.3, gives

    φ_A^* C_U ≃ Lη_d C_U,

and the Frobenius isogeny admits inverse maps up to d^i in degree i
(Theorem 1.8(6)/Corollary 15.5). These structures suggest transporting the
first-order divisibility through Frobenius and obtaining higher m-adic
orders. However, cancellation of d^i in an equality of cohomology classes
requires controlling d-power torsion. Moreover, the divisor changes to
φ_A^r(d)=u^(p^r)−p; it is not legitimate to replace every such factor by d.

Even divisibility by every individual φ_A^r(d) is not a purely module-theoretic
substitute for higher m-adic divisibility. In the complete module M=A/(u)≅Z_p,
all these elements act as −p. Thus p∈φ_A^r(d)M for every r≥0 but p∉m²M.
This is a counterexample to that *algebraic inference*, not a geometric
counterexample or a module equipped with all prismatic axioms.

An actual proof along this route must combine the full semilinear/Nygaard
structure with integral torsion control and a growing m-adic divisibility
estimate. Neither the required estimate nor a counterexample to it was obtained.

## 4. Finite thickenings and specializations do not detect zero maps

Here are exact free-module controls over the same A.

(a) Multiplication by d^N on A is nonzero. It becomes zero after reduction
modulo (d^N,p^n) for every n. It is not zero in the separated module A, and
its image is not contained in m^(N+1), since d^N=(u−p)^N has nonzero initial
form (ū−p̄)^N in gr_m A≅F_p[p̄,ū]. Thus even all p-adic levels at one fixed
I-adic thickness do not prove the target.

(b) Multiplication by u(u−p) vanishes after each specialization u=0 and u=p,
but is nonzero over A. Its initial form has degree two. Therefore two
specialization vanishings are not a conservative test for vanishing of a map,
even for perfect complexes concentrated in degree zero.

(c) The identity of A/(p) is nonzero, but becomes zero after inverting p.
Thus a rational or localized comparison cannot recover an integral conclusion
without a separate torsion argument.

None of these free-module/toy-module maps is asserted to arise from the
geometric restriction in the target. Their purpose is to falsify formal
shortcuts before they are promoted into a proof.

## 5. A complete complex can have non-separated cohomology

This elementary model explains why the word 'separated' cannot be discarded.
Let R=Z_p⟨T⟩, the restricted power-series ring: its coefficients tend to zero
p-adically. Consider the continuous de Rham complex

    C=[R --∂/∂T→ R dT]

in degrees 0 and 1. Its terms are p-adically complete and p-torsion-free;
C is derived p-complete. Set

    ω=Σ_{n≥1} p^n T^(p^n−1) dT.

This series belongs to R dT. If ∂f=ω with f∈R, coefficient comparison in
characteristic zero forces the coefficient of T^(p^n) in f to equal 1 for
every n. Such coefficients do not tend to zero, a contradiction. More
generally, ∂f=aω for nonzero a∈Z_p would force all those coefficients to be a,
again impossible. Hence [ω] is nonzero and Z_p-torsion-free as an element of H¹(C).

For each k≥1 the finite sum
Σ_{1≤n<k}p^n T^(p^n−1)dT is the derivative of Σ_{1≤n<k}T^(p^n).
The remaining tail is p^k times an element of R dT. Consequently

    0≠[ω] ∈ ⋂_{k≥1} p^k H¹(C).

Thus derived completeness of a bounded complex of flat modules does not imply
separatedness of its individual cohomology groups. The argument is an infinite
coefficient proof; finite checks only verify its displayed identities. This is
not a target counterexample: no proper source restriction producing [ω] has
been supplied. It also does not assert compatible successive p-divisions.

## Exact remaining mathematical gap

The source target requires, for every restricted integral class y and every
n≥1, an equality y∈mⁿM_U^i. Section 1 proves only y∈dM_U^i. An all-order
Bockstein descent or a torsion-sensitive Frobenius/Nygaard estimate must bridge
that gap. The announcement by Esnault–Kisin–Petrov is important prior evidence
that such an argument exists, but it is not reconstructed or verified here.

One must also avoid identifying M_U^i/(⋂mⁿM_U^i) with an inverse limit of
derived-coefficient cohomology groups without proving the relevant comparison;
a two-generator ideal can introduce Tor and inverse-limit terms. No conclusion
about the full, non-separated M_U^i, the full generalized Hodge conjecture,
or arbitrary absolute/étale coefficients follows from this packet.
