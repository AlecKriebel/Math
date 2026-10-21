# Positive partial twists can destroy parity permanently

## Status and scope

This is a proved partial result for AIM problem 2.1, corpus ID 20000079 / AIM-ALGEBRAIC_GEOMETRY-0079. It does not solve the general characterization problem or the question about sufficiently many central full twists. Its contribution is an explicit operation counterexample, with a whole infinite family and an exact Euler-characteristic certificate. Novelty is unconfirmed. The first nonparity knot is already the known example 10_139; neither that identification nor the positive-torus parity theorem is claimed as new.

Throughout the coefficient field is C. On three strands write s=σ1 and r=σ2, and set

γ = r s r² s² r²,       γ_k = γ s^(2k),       k≥0.

Here s² is the positive full twist on the first TWO strands. It is not the central full twist FT3=(sr)³ on all three strands.

**Theorem.**

1. HHH(γ_0) is supported in even Rouquier homological degrees.
2. For every k≥1, HHH(γ_k) has nonzero groups of both Rouquier homological parities. Thus multiplying a parity braid by any positive power of this fixed positive partial full twist destroys parity, and continuing the same twisting never repairs it.
3. Nevertheless, the ordinary unreduced graded Euler series of every γ_k has only nonnegative coefficients when expanded in q at zero, with the grading convention below. Thus nonnegativity of that unreduced series is not a sufficient parity criterion, even among positive three-strand knot braids.

The third assertion concerns the UNREDUCED series. Its reduced counterpart has explicitly negative coefficients, and distinguishes this family immediately. A change between these two versions must not be suppressed.

## Exact normalization and credited inputs

Use the Hogancamp–Mellit convention [HM, §§2.2–2.3]: R_n=C[x1,...,xn], deg(xi)=Q²; the positive crossing complex is [R⊗_(R^si)R → R], with R in Rouquier degree 0 and the left term in degree −1. The differential raises Rouquier degree by 1. Hochschild cohomology supplies an independent degree A. Put

q=Q²,    a=AQ^(−2),    t=T²Q^(−2).

HHH means the homology of termwise Hochschild cohomology of that Rouquier complex, without the additional link-normalizing monomial. In particular T, not t, is the homological variable, and a does not change its parity. The unknot factor is

U=(1+a)/(1−q),

with polynomial generator of q-degree 1 and exterior generator of a-degree 1, both in T-degree 0. Positive Markov stabilization and braid conjugation give no homological shift in this convention [HM, (2.2)–(2.4)]. Negative stabilization does shift T and is not used.

The only prior parity theorem used is that positive torus braids have even HHH in this convention [HM, Corollary 1.4]. This is a credited result, not a new theorem of this report. The structural reduction needed for the signed obstruction has the following direct proof, so it does not depend on choosing between several conventions called reduced or middle homology.

**Invariant-coordinate splitting.** Let z=(x1+x2+x3)/3, u=x1−x2, v=x2−x3, and R0=C[u,v]. The change of coordinates is invertible over C: x1=z+(2u+v)/3, x2=z+(v−u)/3, x3=z−(u+2v)/3. Consequently R=C[z]⊗R0. Each simple reflection fixes z and preserves R0, so R^si=C[z]⊗R0^si. It follows directly from the tensor-product definition that D_i=C[z]⊗D_i^0, where D_i^0=R0⊗_(R0^si)R0. Multiplication maps in the positive Rouquier complexes are the identity on C[z] tensored with the multiplication maps over R0. Tensoring the crossings over R therefore gives an equality of complexes F(β)=C[z]⊗F0(β) for every positive braid used here.

The tensor product of the Koszul resolution of C[z] as a C[z]-bimodule with the Koszul resolution of R0 gives Hochschild Künneth, termwise and naturally in the differentials:

HH_R(F(β)) = HH_(C[z])(C[z]) ⊗ HH_(R0)(F0(β)).

In the first factor the Koszul differential becomes zero because left and right multiplication by z agree. This factor is C[z]⊗Λ(θ), with deg(z)=Q²=q and deg(θ)=AQ^(−2)=a. Both have Rouquier T-degree zero. Over the field C, taking Rouquier homology yields

HHH_R(β) ≅ C[z]⊗Λ(θ) ⊗ HHH0(β).

Here HHH0 is defined by this reflection-representation construction. It is the only reduction needed in this proof. Below, “reduced” always means this explicitly defined reflection reduction; no comparison with another version is required. Its graded Euler characteristic is exactly χ(β)/U, and its two Rouquier parities occur if and only if both occur in ordinary HHH. This is also consistent with the standard knot-factorization statement [HM, Remark 1.13], but that identification is not needed.

All γ_k close to knots: their symmetric-group permutation is (23)(12), a 3-cycle, because all other factors are squares. Define χ(β)=Σ_(i,j,h)(−1)^h dim HHH^(i,j,h)(β) Q^i A^j, with coefficientwise locally finite expansion. Write χ(γ_k)=U P_k(q,a). The proved splitting identifies P_k with the actual graded Euler characteristic of HHH0, not merely a formal division. A negative and a positive coefficient of P_k force odd and even HHH0 groups, respectively. Tensoring with the T-even nonzero factor above preserves both.

## 1. The parity input is a positive torus braid up to conjugation

There is the following explicit sequence, using sr s=r s r, and one cyclic rotation (which is braid conjugation):

(sr)^4 = s r s r s r s r
       = r s r r s r s r
       ~ s r r s r s r r
       = s r s r s s r r
       = r s r r s s r r = γ.

In the third line, move the first r to the end. In the fourth, replace the three letters r s r in positions 3–5 by s r s. In the fifth, replace the first three letters s r s by r s r. Thus HHH(γ)=HHH((sr)^4), without a grading shift. The latter is the positive (3,4) torus knot, so the credited torus theorem proves assertion 1.

## 2. Hecke/Euler calculation, including its normalization

Let g_i be the Euler class of the positive crossing complex. If d_i is the class of D_i=R⊗_(R^si)R, then g_i=1−d_i. The graded bimodule splitting D_i⊗D_i≅D_i⊕qD_i gives

(g_i−1)(g_i+q)=0,   or equivalently g_i²=(1−q)g_i+q.

Thus this calculation uses eigenvalues 1 and −q. Replacing this relation with a different standard Hecke normalization without changing the trace would give wrong signs.

On the three-strand Hecke algebra, the six permutation-braid basis elements are

1, g1, g2, g1g2, g2g1, g1g2g1.

The Hochschild Euler trace τ is cyclic. The unlink value is τ(1)=U³, and positive Markov stabilization gives the values

τ(g1)=τ(g2)=U²,
τ(g1g2)=τ(g2g1)=U,
τ(g1g2g1)=(1−q)U+qU².

For the last identity use cyclicity followed by the quadratic relation: τ(g1g2g1)=τ(g1²g2). These values and the quadratic and braid relations suffice to reproduce every polynomial below. There is no numerical interpolation or assumption that Euler positivity implies parity.

An explicit multiplication of the words γ and γs² in this six-element algebra, followed by τ and substitution U=(1+a)/(1−q), gives

P_0 = 1+q²+q³+q⁴+q⁶
      +a(q+q²+q³+q⁴+q⁵)+a²q³,

P_1 = 1+q²+q³+q⁵+q⁶+q⁸
      +a(q+q²+2q⁴+q⁶+q⁷)+a²(q³−q⁴+q⁵).

Here is a complete finite multiplication certificate for the two initial values. Put d=q−1 and c=q²−q+1. In the ordered basis above, the six coefficients of Γ=g2 g1 g2² g1² g2² and Γg1² are respectively

| Basis element | Γ coefficient | Γg1² coefficient |
|---|---|---|
| 1 | q³d² | q³d²c |
| g1 | −q²d³ | −q²d³(q²+1) |
| g2 | −q²dc | −q²d(q²+1)c |
| g1g2 | qd²c | qd²c(q²+q+1) |
| g2g1 | qc² | qc(q⁴−q³+q²−q+1) |
| g1g2g1 | −d(q²+1)c | −d(q⁴+1)c |

These expansions follow by successively replacing every g_i² with (1−q)g_i+q and every g2g1g2 with g1g2g1. One can also check the second column directly from the first by multiplying each of the six basis elements by g1² using those two identities. Applying the explicitly stated trace gives

τ(Γ)/U = (q⁵−2q⁴+q³)U²
          +(−q⁶+2q⁴−2q³+q)U
          +q⁶−q⁵+q³−q+1,

τ(Γg1²)/U = (q⁷−3q⁶+4q⁵−3q⁴+q³)U²
             +(−q⁸+3q⁶−6q⁵+6q⁴−3q³+q)U
             +q⁸−q⁷+2q⁵−3q⁴+2q³−q+1.

Substituting U=(1+a)/(1−q), multiplying by (1−q)², and comparing coefficients of a⁰,a¹,a² yields exactly the displayed P_0 and P_1. Thus these initial conditions are entirely hand-checkable polynomial identities; no computational output is a premise of the proof.

Squaring a Hecke generator gives an operator h=g1² with

(h−1)(h−q²)=0.

For completeness, substitution g1²=(1−q)g1+q verifies this identity directly; it does not require semisimplicity or inverting 1−q². Multiplying the identity by the fixed γ and by h^k, then tracing, gives for every k≥0

P_(k+2)=(1+q²)P_(k+1)−q²P_k.

Hence, with H_k=Σ_(j=0)^(k−1)q^(2j), and H_0=0,

P_k=P_0+H_k D,
D=(q⁸+q⁵−q⁴)
  +a(q⁷+q⁶−q⁵+q⁴−q³)
  +a²(q⁵−q⁴).

This formula is a polynomial identity for each k, proved by the recurrence and two initial values; the displayed finite sum never entails a specialization or a division by a possibly zero scalar.

In particular

[a²]P_k = q³+(q⁵−q⁴)H_k
          = q³ Σ_(j=0)^(2k)(−q)^j.

For every k≥1, [a²q³]P_k=+1 and [a²q⁴]P_k=−1. In terms of the original independent degrees these are A²Q² and A²Q⁴, respectively, so they are distinct well-defined bidegrees. At the first bidegree there must be an even-homological class; at the second there must be an odd-homological class. Extra cancellation can only add classes and cannot eliminate the need for these two parities. The invariant-coordinate splitting then establishes assertion 2 for the ordinary unreduced HHH requested in the original question.

## 3. Why the ordinary unreduced sign test misses every member

Write P_k=F_(0,k)+aF_(1,k)+a²F_(2,k). At k=0 all three polynomials have nonnegative coefficients. For k≥1 the formula above can be reorganized as

F_(0,k)=1+q²+Σ_(j=1)^(k+1)q^(2j+1)+q^(2k+4)+q^(2k+6),

F_(1,k)=q+q²+2q^(2k+2)+q^(2k+4)+q^(2k+5)
        +Σ_(j=2)^k (2q^(2j)−q^(2j+1)),

F_(2,k)=q³ Σ_(j=0)^(2k)(−q)^j.

Empty sums are zero. Every F_(i,k)/(1−q) has nonnegative formal-series coefficients. This is immediate for F_(0,k). For the possible negative terms in F_(1,k), use

(2q^m−q^(m+1))/(1−q)=q^m(2+q+q²+...).

For F_(2,k), pair consecutive terms to obtain

F_(2,k)/(1−q)=q³Σ_(j=0)^(k−1)q^(2j)+q^(2k+3)/(1−q).

Finally χ(γ_k)=(1+a)P_k/(1−q) is a positive sum of these nonnegative series. This proves assertion 3. It also explains why ignoring the proved invariant-coordinate tensor factor would invalidate the mixedness argument: the unreduced Euler series alone has lost the obstruction.

## 4. Additional operation and identification

The k=1 braid is a cyclic rotation of

s r (s r² s)²,

the explicit positive 10_139 braid in [K3, p.38]. Our calculation certifies its nonparity independently of that source's assertion.

There is also a Jucys–Murphy operation counterexample. Put L=s r² s, the reflection of the conventional JM3=r s² r. The braid srL=s r s r² s equals s³rs² by two braid relations and is conjugate to s⁵r. Positive destabilization identifies its HHH with the positive (2,5) torus knot without a homological shift. But (srL)L=srL² is the k=1 nonparity example. Thus multiplication by this fixed positive reflected Jucys–Murphy braid also fails to preserve parity. Conjugating the complete example by the Garside half twist swaps s and r and supplies the same statement for conventional JM3. No assertion is made about arbitrarily high powers of L. The all-k theorem concerns powers of s², a different operation.

## Boundaries and relevance

- This is a counterexample to preservation, and to eventual production, for a specified PROPER partial full twist in B3. It is not a counterexample for central FT3, and does not answer eventual central twisting of an arbitrary braid.
- The initial γ is positive and conjugate to a torus braid, but γ_k need not be a nonnegative product of nested initial full twists. In fact γ_k has 3-cycle permutation, whereas such full-twist products are pure. Thus this does not refute the neighboring pure-Coxeter/nested-full-twist conjecture (20000081).
- No assertion that these knots are algebraic is needed or made. Therefore the algebraic-link conjecture (20000080) is not refuted.
- The family has writhe 8+2k and three strands. Its reduced Euler a^0 term has top q-degree 2k+6, so these are infinitely many distinct reduced graded polynomials in this fixed raw convention. We do not rely on this alone for a normalization-independent claim that all their knot types are distinct.
- Ordinary Euler sign coherence is only necessary; reduced sign coherence is a stronger available obstruction for knots. A nonnegative reduced series would still not prove parity.
- No full homology calculation, integral torsion theorem, new general sufficient criterion, or resolution of AIM 2.1 is claimed.

## References

[HM] Matthew Hogancamp and Anton Mellit, Torus link homology, arXiv:1909.00418v1, 1 September 2019. https://arxiv.org/abs/1909.00418 . Exact conventions §§2.2–2.3; knot factorization Remark 1.13; positive-torus parity Corollary 1.4. The cited public PDF has SHA-256 96fff9921ff6694ab83e3959d8995c8af1df040952f01a1c9c5e5b07c89a996b.

[K3] R. İnanç Baykur, Robion Kirby and Daniel Ruberman (editors), K3 – A New Problem List in Low-Dimensional Topology, 2026 preliminary author version, p.38, contribution scribed by E. Gorsky. https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf . Used for the prior 10_139 identification and open-problem context only, not as the proof of the Euler calculation.

[Turner] Joshua P. Turner, Triply graded link homology for Coxeter braids on 4 strands, arXiv:2410.03068v1, 4 October 2024. https://arxiv.org/abs/2410.03068 . Used to confirm terminology and delimit the neighboring pure-Coxeter family, not as an input to our calculation.
