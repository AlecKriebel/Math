# Arithmetic descent of the scalar-five normalized family

Authored proof, 14 October 2026. Shared PASS 4/5, row 1777 / 30005572. This is a restricted arithmetic theorem, not a solution of the construction contract. No novelty claim is made.

## 1. Statement, assumptions, and scope

Let F be an imaginary quadratic field with maximal order O, R=Z[1/6], and N a nonzero proper ideal. In Sections 1–8 assume that O^× → (O/N)^× is injective. Put L=F(N), Q=Gal(L/F), and

O'(N)=O_L[1/N] if N is a power of one prime ideal, and O'(N)=O_L otherwise.

Use the source's h² indexed CM product system, source row-lattice groups Γ₀(N)_i, source markings, and its Artin convention R_N. A matrix with lower-right entry d acts on the coefficient group by R_N(d), not its inverse. Its chosen representatives of homothety classes and compatible primitive N-points are fixed throughout. Let c be an auxiliary ideal prime to 5N.

The accepted PASS 3 geometric cocycle Θ_c is the unique representative with the specified moved Gersten residue which is eventually trace-fixed and literally T₅-fixed. All references below to normalization mean this representative, not an arbitrary ordinary lift.

**Gersten sign convention.** This arithmetic paper uses the source reciprocal tame differential d₂,src=−d₂,std, where the standard tame symbol is (−1)^(v(a)v(b)) a^v(b)/b^v(a) after reduction. The next differential is the ordinary divisor map. If the frozen PASS 2–3 representatives are read with their explicit standard differential, transport them here by −Id in degree two and Id in degrees one and zero. Thus Θ_c here and every K₂ correction are the negatives of those standard-sign representatives, with the same degree-one primitive. This chain isomorphism commutes with all operations used below. The arithmetic comparison with the LSSW/ShVe-sign family is therefore literal after this declared transport, rather than an unnamed sign identification. It does not settle the orientation of a prescribed relative Cremona symbol.

**Restricted arithmetic theorem.** For every component i and every such c there is a canonically compatible arithmetic cocycle

z_{c,i,N}: Γ₀(N)_i → K₂(O'(N))⊗R.

For every admissible model-definition modulus f prime to N and c, it specializes to the normalized geometric cocycle over F(Nf) after inverting |(O/f)^×|. This assertion retains the entire five-primary part. Changing f or the CM model does not change the resulting cocycle. Changing the eligible moved primitive changes its class by an integral coboundary.

For c,d prime to 5N its classes satisfy the integral auxiliary exchange identity

s_d [z_c] = s_c [z_d],       s_a=(Na)²−R_N(a).                         (1.1)

The tuple over all components satisfies the source's good-prime Eisenstein identity at primes q not dividing 5N. No Hecke identity at five is deduced here.

For every rational p≥5, decompose Q=Q_p×Q', and let χ be a p-adic character of Q', extended trivially over Q_p, exactly as in source §4.3. There is a unique unaugmented χ-class whenever the residual character χ̄∘R_N differs from the square of the mod-p cyclotomic character on G_F. Equivalently, it exists by unit cancellation on every χ-block except possibly the single block cut out by the squared-cyclotomic extension when that extension lies in L. This includes p=5 with its actual exceptional character, described in Section 7.

The theorem does **not** assert integer-ring values at a prime-power N, compactification, unrestricted small-level descent, relative theta-symbol calibration, or removal on a surviving exceptional block. Its cocycles live on arithmetic groups; no new coarse-space comparison is needed for this result.

## 2. Integral transfer and an explicit supply of definition moduli

For a finite Galois extension K/L of degree d, restriction and transfer on K₂ satisfy

Cor Res=d,       Res Cor=Σ_{g∈Gal(K/L)}g.                             (2.1)

These equalities also hold with the compatible arithmetic Γ-actions used here. On p-primary groups, if p∤d, restriction is injective and is an isomorphism onto invariants with inverse d⁻¹Cor. Here d⁻¹ is a genuine automorphism of a p-primary group; this is never division by p, by a class number, or by a nonunit of its coefficient ring.

Fix p≥5 and a finite list of forbidden primes. Choose a sufficiently large rational prime ℓ≡2 mod p outside that list, and a prime f above ℓ. Dirichlet's theorem supplies infinitely many choices. The residue degree of f is 1 or 2, so

|(O/f)^×|=ℓ^e−1 ≡ 1 or 3 (mod p).

Thus this number is prime to p, also for p=5. Taking ℓ sufficiently large gives injective unit reduction at f, and f may avoid N, c, all fixed ideal representatives, a prescribed arithmetic prime, and any other finite set. The relative degree

[F(Nf):F(N)] divides |(O/f)^×|

is consequently prime to p. No assertion is made that [F(f):F], or h, is prime to p. A p-primary class group and a p-divisible target modulus do not obstruct this choice.

The same observation applies to the compositum of finitely many such relative extensions. In particular, two p-good definition moduli can be compared in a common field whose degree over L remains prime to p.

## 3. Actual image membership before descent

This section is the R-coefficient replacement for source Lemmas 3.4.3 and 4.1.1, not an inference that Galois invariance alone is descent.

For unit-injective N, use the marked CM models A_u over L supplied by the same CM theorem used in source Lemma 4.1.1. Their N-torsion is L-rational, and their compatible O-actions and markings become isomorphic over F(Nf) to the models E_{i_u} defined using f. Let ψ=(ψ₁,ψ₂) be this marked product isomorphism and P=ψ₂⁻¹(P_{i₂}).

The accepted PASS 3 model/base-field transport is an exact equality of the normalized representatives:

Θ_{c,A}=ψ*Θ_{c,E}.

The specified moved residue primitive is regular at the primitive N-orbit, and its normalized cocycle is regular there. Pullback by (0,P) therefore gives an actual element of K₂(L)⊗R whose restriction equals the geometric specialization λ_i*Θ_{c,E} over F(Nf). This proves image membership, not merely invariance. It also checks that the geometric arithmetic Galois action, rather than the trivial geometric action on constants, is the action relevant after evaluation.

To remove the possible kernel of restriction, work p-primary and choose the p-good f of Section 2. Define the descended value by d_f⁻¹Cor of this specialization. Equation (2.1), together with the proved image membership, identifies it with the unique preimage. Thus a possible five-primary kernel in a poorly chosen model extension never enters the definition.

For two p-good choices f and f', exact transport to a common marked model identifies their specializations over the common field. Prime-to-p injectivity identifies the descended values in K₂(L)⊗Z_p. The same argument compares all eligible isomorphisms and compatible model systems. This is stronger than equality after inverting five.

## 4. The crossed-homomorphism law and patching all primes

For g=(a b; c d) in the source's Δ₀(N) system, choose d' satisfying d'≡d mod N and d'≡1 mod f. Source CM reciprocity for the actual markings gives

g∘λ_i=(0,dP_{i₂}),       dP_{i₂}=R(d')P_{j₂}.

The geometric coefficient classes are defined over F(f), which R(d') fixes. Pullback therefore gives the exact identity

λ_i* g* Θ_{c,j}=R_N(d) λ_j* Θ_{c,j}                                (4.1)

after the image identification above. Thus the descended map satisfies

z_c(γδ)=z_c(γ)+R_N(d_γ)z_c(δ),

with the source's left cocycle convention. If a source equivalent convention reverses composition, all operations are transported together; no inverse Artin map is substituted in (4.1).

For each p≥5 the preceding construction gives a canonical p-primary cocycle. They assemble in K₂(L)⊗R, rather than only in a product of completions. Indeed K₂ of a number field is torsion, by localization and finiteness of its integer-ring K₂. Fix one definition modulus f₀. For every p not dividing d_{f₀}, the p-primary descended value is recovered from the one torsion specialization over F(Nf₀); hence only finitely many such p can occur in the value at a fixed γ. There are only finitely many remaining p dividing d_{f₀}. The pointwise sum is therefore finite. The cocycle equations hold componentwise and hence over R.

For an arbitrary admissible f, discard only the prime divisors of |(O/f)^×|. The remaining p-primary comparisons give precisely the stated equality after that number is inverted. Conversely, comparisons for all f characterize the R-valued cocycle uniquely: for any possible nonzero p-part choose p-good f and use injectivity. This is the precise meaning of varying the definition modulus.

## 5. Vertical integrality, including the previously lost five-part

### 5.1 One-curve theta chains have no vertical divisor

At a prime of good reduction away from the model conductor, the one-curve theta functions in the source's residue primitive extend as units on the corresponding complement of their horizontal torsion divisors, as used in source Lemma 4.2.2. The accepted R-valued one-curve primitive has this same property.

Here is a way to check the coefficient issue without importing a K₂ theorem backwards through inversion of five. Its image after inverting five equals the source's normalized function. A vertical divisor coefficient before localization belongs to Z⊗R; that group embeds in Z[1/30]. Since the corresponding source coefficient is zero, the coefficient before localization is zero. The same holds componentwise for the finite torsion support. Horizontal support has been removed, so the R-function is a unit on the needed normal open. Possible torsion constants do not change any divisor. Shears, finite flat pullbacks, product norms, and finite sums of these chains preserve this unit property on the corresponding open subschemes.

### 5.2 The constant-unit kernel is handled exactly

Let v be a good-reduction prime of the model field with residue characteristic l, and let z be one value of a normalized surface cocycle. The horizontal/vertical residue square of source Lemma 4.2.1 works over R. Its horizontal residue is the difference of theta chains considered in 5.1. Consequently the vertical residue r of z has zero divisor on the special-fiber surface. As the latter is geometrically connected and projective, r is a constant unit:

r ∈ k_v^×⊗R.

For a scalar integer n prime to the fixed exceptional data and to l, compatibility of residue with finite étale trace gives

(n⁴−1)r=0.                                                         (5.1)

The exponent is n⁴, the degree of scalar multiplication on a product of two elliptic curves. One must not use the single-curve degree or assume that every constant unit is already killed after inverting six.

The ideal of R generated by these n⁴−1 contains 5. To verify this, for every rational q≥7 choose by CRT an n prime to the exceptional set whose nonzero residue mod q is not a fourth root of unity; this excludes q from the common divisor. Choose additionally n≡2 mod 25, still prime to the exceptional set, to make the common 5-adic valuation at most one. Since at least one n⁴−1 is nonzero, the generated ideal is finitely generated and these local checks prove that it is either R or 5R. In particular,

5r=0.                                                              (5.2)

If l=5, the finite field unit group has order prime to five, so r=0. If l≠5, literal T₅-invariance and the same residue compatibility give 625r=r. Together with 5r=0 this forces r=0. This is the missing five-primary argument. It does not use pullback compatibility at five; only the actual trace equation T₅z=z is used.

The same proof applies to any normalized K₂ correction whose horizontal residue is a finite combination of the theta chains in 5.1. This strengthened form will be used in Section 6.

### 5.3 Specializing and varying f

The source's reduced-point avoidance argument is coefficient-independent. At every arithmetic prime not dividing f, the primitive N-point avoids the reduced moved support, provided we work in O'(Nf). Thus evaluation of the zero vertical residue in 5.2 proves that the specialization is integral at that prime.

Fix a prime w of L belonging to Spec O'(N), and a rational p≥5. Choose p-good f additionally avoiding the prime below w. Every prime of F(Nf) above w is covered by the preceding argument. Transfer sends classes integral at these primes to classes integral at w. Multiplication by d_f⁻¹ on the p-primary group preserves that subgroup. Hence the canonical descended p-value has zero tame residue at w. Varying w and p gives

z_c(γ) ∈ K₂(O'(N))⊗R.

This reasoning uses actual transfer and local integrality, not Galois invariance as a substitute for integral descent. At a prime-power N it says nothing about the omitted primes above N. The surviving prime-power residue problem is unchanged.

## 6. Integral auxiliary exchange and Hecke scope

The accepted geometric pullback/auxiliary-exchange proof applies to c,d prime to 5: every pullback kernel involved here is prime to five, so it preserves the normalized submodule. The corresponding zero-cycle identity has the form

f* e_c=e_{cd}−(Nc)² e_d.

Subtracting the prescribed degree-one primitives gives a closed theta chain. All primitives in this assertion are the moved/sheared primitives regular at the N-orbit, or their explicitly transported versions; the unshifted coordinate axes are not used for this comparison. Its unique normalized K₂ lift is the correction witnessing the class identity. The support of each summand avoids the primitive N-orbit when (cd,N)=1; pullback by the relevant ideal isogeny permutes that orbit. Consequently the correction is regular there.

The correction's horizontal residue is a finite sum of pulled-back normalized theta chains. By Section 5.1 its vertical divisor is zero, and by Section 5.2 the correction itself has zero vertical residue. Repeating the definition-field transfer and varying-f argument shows that its specialization belongs to K₂(O'(N))⊗R. Thus this is an integral coboundary, not merely a field-valued coboundary.

The source's product norm/model reciprocity comparison identifies the component-changing ideal operator with R_N(a) for a prime to 5N. To cover a meeting c, first choose an integral a' in the same ideal class as a and prime to 5Nc, as in source Proposition 4.1.8. Such a representative exists by ideal-class prime avoidance. Use the exact product norm law for a', then compare a and a' by their scalar ratio with the source's compatible generators. No Artin symbol is taken at a prime dividing N. The norm of a moved source primitive and the moved target primitive have the same boundary; their difference has a unique normalized K₂ comparator. Its support is disjoint from the target N-orbit because the product isogeny is prime to N, and its inverse-image orbit is disjoint from the transported source support. Thus this comparator is regular before evaluation. Its vertical integrality follows from Section 5, exactly as for the auxiliary-exchange comparator. The scalar/pullback comparison is prime to five and N in this section, so the transported correction has the same properties. This proves the required regular, integral norm/reciprocity comparison, rather than applying an unshifted norm identity at a point on its divisor. The exact product norm compatibility required here is part of the accepted PASS 3 input. In particular the convention is

[a]*[z_{c,j}]=R_N(a)[z_{c,i}].

Combining this with the normalized pullback identity, and interchanging c,d, proves (1.1) in the cohomology with the integral localized coefficient module. This argument does not require a new general injectivity theorem for H¹ with integer-ring coefficients mapping to field coefficients.

For completeness, the geometric good-prime Hecke proof away from five is an identity of the same zero-cycle construction. Its cochain correction is obtained by lifting the corresponding closed finite sum of normed/pulled-back theta chains. The same regularity and vertical argument makes its specialization integral. Together with the source's unchanged good-prime double cosets and (4.1), it yields

(T_q−Nq−R_N(q))[z_c]=0,       q∤5N.

This invokes only the accepted prime-to-five geometric identities and their theta-chain corrections. It does not promote a field identity to an integral identity by unproved coefficient injection. No assertion about q|5 is made; a separate proof may enlarge that scope.

## 7. Exact character conventions and the exceptional character at five

Let p≥5. Write Q=Q_p×Q', let χ:Q'→Z_p-bar^×, and let O_χ be the unramified extension of Z_p generated by its image. The χ-block of Z_p[Q] is O_χ[Q_p]. A smoothing factor s_c is a unit in this local ring exactly when

(Nc)²−χ(c) is nonzero modulo p.                                    (7.1)

This is a character of the full ray group Q', not just a character of (O/N)^× or of a chosen principal ray subgroup. Requiring c prime to 5N does not change the unit-existence test: Chebotarev allows avoidance of this finite set.

Let κ̄_p:G_F→F_p^× be the mod-p cyclotomic character, and let M_p/F be the finite abelian extension cut out by κ̄_p². There is no invertible smoothing factor on the χ-block precisely when

M_p⊂L and χ is the unique Teichmüller lift of κ̄_p² factored through Q. (7.2)

Indeed equality χ̄(R_N(c))=(Nc)² for every auxiliary prime c is equality of two finite Galois characters on Frobenius elements outside a finite set. Chebotarev makes it equality on G_F. Conversely that equality plainly makes every smoothing factor belong to the maximal ideal. The unique lift has order prime to p and is therefore a character of Q'.

For p≥7 this reproduces exactly the source's exceptional ω² and its automatic exclusion when (p)∤N². We do not replace the ideal divisibility (p)|N² by p|Norm N.

For p=5, however, the correct statement is different:

- M₅=F(√5), because the kernel of the square of the mod-five cyclotomic character fixes the quadratic subfield Q(√5) of Q(μ₅).
- If 5 is unramified in F, the relative conductor of F(√5)/F is the product of all primes above five. Thus its exceptional character occurs precisely when (5)|N².
- If 5 ramifies in F, F(√5)/F is everywhere unramified, hence contained in the Hilbert class field and in every ray field L. Its quadratic exceptional character therefore occurs at every N, even when N is prime to five.

The last conductor assertion can be verified locally. At a ramified prime over five, reduction of the norm of a local unit from the quadratic field is a square in F₅^×. Applying κ̄₅² gives the fourth power of a nonzero residue, which is one. The character is thus trivial on inertia. Away from five it is already unramified, and F has no real places. The extension is nontrivial because an imaginary quadratic F cannot contain √5.

For example, F=Q(√−5) and the unit-injective level N=(3) already have an exceptional five-character: F(√5) is the Hilbert quadratic extension. In biquadratic discriminant terms its absolute discriminant is (−20)·5·(−4)=400, equal to Disc(F)², confirming relative discriminant one. Thus copying the source's p≥7 phrase “automatic if (p)∤N²” to p=5 would be false.

## 8. What can genuinely be canceled

Put B_N=K₂(O'(N))⊗Z_p and M_i,χ=H¹(Γ₀(N)_i,B_N^(χ)). Projection to χ uses the same O_χ[Q_p]-block as the source. On a nonexceptional block choose an auxiliary d prime to 5N satisfying (7.1). Define

u_i,χ=s_d⁻¹[z_{d,i,N}]^(χ).                                        (8.1)

This inverse exists as a ring unit acting on M_i,χ. Equation (1.1) proves s_c u_i,χ=[z_c]^(χ) for every allowed c and proves independence of d. If two classes satisfy all these equations, multiplication by the invertible s_d proves equality. The component tuple inherits the away-from-five Hecke identity, since every operator in that identity commutes with the coefficient group-ring action.

On the exceptional block, every s_c is a nonunit. No analogous division is made. For an exact formulation of the remaining obstruction, let J be the ideal generated by the allowed s_c in the local group ring A_χ. Let

E(M)={ (a_c)_c ∈ ∏_c M : s_d a_c=s_c a_d for all c,d },
δ:M→E(M),       δ(u)=(s_c u)_c.

The actual smoothed family defines an element of E(M). An unaugmented class exists exactly when its image in E(M)/δ(M) is zero. If it exists, its ambiguity is exactly M[J]. This formulation retains both existence and uniqueness; exchange alone proves neither on the exceptional block. In particular, on any nonzero module killed by J arbitrary nonzero compatible smoothing data can satisfy every exchange identity and fail to be in δ(M).

There is a sharper elementary check at five when 5 ramifies in F and N is prime to five. On its exceptional block J is the maximal ideal (5, augmentation of Q₅). To see 5∈J, choose a principal auxiliary c=(α), with α≡1 mod N, whose local norm square is 1+5u mod 25 for u a unit; ramified quadratic local coordinates and CRT permit this choice. Then R_N(c)=1 and s_c=5 times a 5-adic unit. Modulo five the remaining s_c are, up to nonzero scalar factors, 1−g for every g∈Q₅; Chebotarev realizes every ray class while avoiding 5N. This verifies the asserted ideal. In this case the common ambiguity is exactly M[5]^{Q₅}, and a possible obstruction is genuinely concentrated at the maximal ideal; it is not removed by the availability of prime-to-five auxiliaries.

A global sufficient condition that uses no exceptional vanishing theorem is the following: if M_p is not contained in L for every p≥5, then the ideal generated by all s_c in R[Q] is the unit ideal. Every maximal ideal of this finite R-algebra lies above some p≥5 and has one of the character descriptions above, so Section 7 excludes every maximal ideal containing J. A finite Bézout combination of smoothing factors is therefore 1, and gives one unique unaugmented R-class directly. For example, this applies to unit-injective N supported on primes over 2 and 3 when 5 is unramified in F.

One may also combine the new nonexceptional five-component with the already published p≥7 exceptional-vanishing theorem. In particular, if

5 is unramified in F, (5)∤N², and no p≥7 has both (p)|N² and p|h,

then there is a unique full unaugmented R-class satisfying the smoothing equations for c prime to 5N. For p≥7 it is the source class, because coefficient extension of the geometric and arithmetic construction has already been checked exactly. For p=5 every block is nonexceptional by Section 7. The coefficient group K₂(O'(N)) is finite, so only finitely many primary pieces occur. This corollary remains restricted to unit-injective N, the localized target at prime-power level, and Hecke operators away from 5N. No exceptional five-block vanishing follows from a generic-character theorem.

## 9. Unit stabilizers and the explicit small-level boundary

Let U_N={u∈O^×:u≡1 mod N}. Its order divides 2, 4, or 6 and is therefore invertible in R, so finite-group averaging and the vanishing of higher cohomology of U_N with R-coefficients are legitimate. That fact is not the same as producing a coherently marked CM model over F(N).

Sections 3–4 used the marked-model theorem under U_N=1. When U_N≠1 the corresponding moduli object has a stabilizer. The present proof does not provide compatible descent data for all its marked CM products, nor prove that changing such data has only the identified unit action on the specialized arithmetic cocycle. Consequently the arithmetic theorem is not asserted at these levels. A stack/coarse descent or a separate norm-compatible small-level construction is still required; “the unit order is invertible” alone would skip that task.

This is a small-level limitation rather than an arbitrary character deletion. If O^×={±1}, failure means N divides (2). In Q(i) and Q(√−3), failure is described exactly by N dividing (1−u) for a nonidentity unit u; these ideals are supported over 2 or 3. In particular, every non-unit-injective proper level is supported over 2 or 3. The unit ideal remains excluded, since the prescribed point would be the origin.

The h² CM component system has been retained everywhere it is defined above; no class-number-one assumption and no division by h occurs. Restriction to the h Bianchi components can be performed with the source's conventions, but it does not repair the listed small-level, compactification, five-Hecke, or relative-symbol issues.

## 10. Verification boundary and sources

Accepted geometric inputs are PASS 1–3 as frozen in their independent acceptances, especially PASS 3 SCALAR_FIVE_NORMALIZATION.md and TRACE_NORMALIZATION_ACCEPTANCE.md. The present proof uses exact model transport, normalized prime-to-five pullbacks, and exact product norms; ordinary cocycle existence alone would not suffice.

Primary public source: E. Lecouturier, R. Sharifi, S.-C. Shih, J. Wang, *Eisenstein cocycles for imaginary quadratic fields*, author manuscript, §§3.1, 3.4, 4.1–4.3, https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . Retained PDF SHA-256: 3c50732ecd6f44ad448a9d6d77e7543421ea9c12b4ba497a1ebfc1665df6dcb5.

The retained source was inspected directly. Its CM model-existence and reciprocity theorems are used with their stated admissibility hypotheses. Its R[1/5] arithmetic theorem is not used as a substitute for the new five-primary descent or vertical-integrality arguments. Its p≥7 exceptional-vanishing theorem is used only in the explicitly identified final corollary. The original full problem remains UNSOLVED.
