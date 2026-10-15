# Independent audit: characteristic-two local-action counterexample

Date: 9 October 2026 UTC.

## Verdict

**ACCEPTED as a complete negative answer to the unrestricted source question.**

The counterexample uses the faithful weakly ramified action of the additive group of F4 on F4[[t]], with its order-two subgroup F2. It excludes every prorepresentable recipient F making the prescribed restriction–induction map to the fibre product smooth, regardless of the proposed tangent dimension of F.

This is one proof route. The introductory and refined formulations in the source describe the same question and the same counterexample. The result does not answer the modified question obtained by additionally requiring the subgroup and quotient deformation functors to be prorepresentable. It does not contradict the source's conditional obstruction-space theorem. No novelty or exhaustive-literature guarantee is made.

The mathematical proof under review has SHA256 `e6f3b0bb4135f7dace556ab674e880611c3f1ae6753f1984b4963d5032d3ff1a`. No substantive mathematical gap was found. Two separate corrections concern (i) composition-convention wording and (ii) optimization-safe auxiliary verification. Neither changes the argument. The original files were retained unchanged.

## 1. Exact source scope

[Byszewski's OWR contribution](https://ems.press/content/serial-article-files/46200), printed pp.3038–3040, begins with the unrestricted decomposition question. It specifies a perfect field of characteristic p>0 and local Artinian W(k)-algebras. The refined question on p.3039 requires F to be prorepresentable; it does not require D_N or D_Q to be prorepresentable. Theorem 3 on p.3040 states those additional assumptions separately. I inspected the complete three-page contribution and visually inspected the rendered question and neighboring pages. There is no exclusion of characteristic two or of groups of order two or four.

[Byszewski 2011](https://arxiv.org/abs/1112.0352), Definitions 1.1–1.2, uses faithful actions, local W(k)-algebra maps, and conjugation by automorphisms reducing to the identity. Question 4.4, p.13, is unrestricted; the adjacent Remark 4.5 adds prorepresentability hypotheses for its conditional ring formula. Theorem 4.9 states them again for its obstruction-space theorem. Section 1 and Proposition 2.4 provide the tangent/cohomology and restriction interfaces. The full definitions and surrounding sections were read; the question and remark were visually inspected.

[Byszewski–Cornelissen 2009](https://www.numdam.org/article/AIF_2009__59_3_877_0.pdf), §2.1 and Remark 2.2, explicitly permit nilpotent constant terms in coordinate automorphisms. Proposition 4.1, pp.895–896, contains the parameter-e versus parameter-(e+e²) conjugacy used here. Those pages were visually inspected. The original paper uses the reversed composition convention when expressing ring automorphisms as substitutions; the optional wording correction below makes the direction explicit.

Normality is required to speak of Q=G/N and is explicit in the 2011 source. Here G is abelian, so this condition is satisfied.

## 2. Category, automorphisms, and the action

Set k=F2[u]/(u²+u+1), G=(k,+), and N={0,1}. A finite field is perfect. The map

rho(a)(t)=t/(1+at)

is an automorphism with inverse itself. Composition gives rho(a+b), and the coefficient of t² distinguishes a, so the action is faithful. N is normal. Each nonidentity element has first nonzero displacement in degree two, although weak ramification is not needed as an additional theorem in the proof.

Put y=t²/(1+t). Direct substitution proves N-invariance. The equation t²+yt+y=0 is Eisenstein over k[[y]], and the standard complete-DVR power-series calculation gives a degree-two extension k((t))/k((y)). Its derivative with respect to t is y, which is nonzero in the field, so the extension is separable. Its nonidentity automorphism is rho(1). Thus the fixed field is k((y)); the valuation relation ord_t(y)=2 then gives k[[t]]^N=k[[y]]. Equivalently, formal division yields a free k[[y]]-module basis {1,t} for k[[t]].

Since u(u+1)=1,

rho(u)(y)=t²/((1+ut)(1+(u+1)t))=t²/(1+t+t²)=y/(1+y).

This is a nonidentity involution. Therefore the quotient local-action deformation functor is precisely that of sigma(y)=y/(1+y).

All test rings k[e]/e² and k[e]/e³ are local Artinian W(k)-algebras through W(k)→k. Their reduction maps and the map e↦e+e² preserve this structure and the specified residue field. The proof never requires the hypothetical representing ring R to be a k-algebra.

In an Artinian coefficient ring, a substitution with constant coefficient in the maximal ideal and unit linear coefficient defines a continuous automorphism of A[[y]]. Nilpotence of the maximal ideal makes substitution into an arbitrary power series well-defined. The t-adic and (m_A,t)-adic topologies are equivalent for this purpose. Thus the occurrence of e as a constant term in the deformation and conjugator is allowed by the actual deformation problem; a pointed version forbidding it would be a different problem.

## 3. An undetectable nonzero tangent direction

Let B=k[e]/e³, A=k[e]/e², and j:B→B be given by e↦e+e². It is an automorphism, with j²=id. Let

sigma_e(y)=(y+e)/(1+y),   M_e=[[1,e],[1,1]].

Its determinant 1+e is a unit, its constant term is nilpotent, and M_e²=(1+e)I. Hence it is a valid Q-action reducing to sigma. Write x for its class in D_Q(B) and v for its reduction in D_Q(A).

With C=[[1+e,e],[0,1]], exact multiplication in B gives

M_(e+e²) C=(1+e) C M_e.

C corresponds to a coordinate change reducing to the identity, and multiplication by a unit scalar does not change the fractional-linear map. Thus j_*x=x. In ordinary composition of fractional-linear functions, the conjugator is the function chi(y)=(1+e)y+e. In the source's ring-automorphism composition convention, the equality is sigma_(e+e²)=chi^(-1) sigma_e chi. Either formulation proves the same equivalence of deformation classes. This is the only precision change to the prose proof.

For any natural transformation eta:D_Q→h_R, let psi:R→B represent eta_B(x). Naturality and j_*x=x give j∘psi=psi. For every r∈R, write

psi(r)=c0+c1 e+c2 e², with ci∈k.

Applying j changes the coefficient of e² by c1. Therefore c1=0 for every r. Composing psi with B→A leaves only c0. As psi is local and induces the given residue map, its reduction to A is exactly R→k→A. Naturality once more proves eta_A(v)=0.

This is a direct representability argument at two Artinian rings, stronger in economy than invoking a pro-Yoneda theorem for an infinite formal family. It requires no choice of hull, no universal deformation of D_Q, no smoothness of eta, and no linearity assumption about its tangent map. An isomorphism F≅h_R can simply be composed with any proposed map to F.

To prove v≠0, every identity-reducing coordinate automorphism over A has the form y+e f(y), with f(y)∈k[[y]]. Its first-order conjugation perturbation of sigma is, up to the chosen composition convention,

f(sigma(y))−sigma'(y)f(y).

Its constant coefficient is zero since sigma(0)=0 and sigma'(0)=1. The perturbation sigma_e−sigma has coefficient series 1/(1+y), whose constant coefficient is one. This excludes every such conjugator, not merely affine or fractional-linear ones. Hence v is a genuinely nonzero point of the tangent space of the unframed, set-valued deformation functor.

## 4. Full equivariant derivation calculation

Let Theta=Der_k(k[[t]]) and Theta-sharp=Der_k(k[[y]]). These are the usual formal derivations. They are continuous automatically: a derivation sends t^n k[[t]] into t^(n−1) k[[t]], by Leibniz's rule. Each is determined by its value on the parameter.

Restriction of an N-invariant derivation is a derivation on k[[y]]. It is injective: in the separable field extension an extension of a derivation is unique, or directly the derivative dy/dt=t²/(1+t)² is nonzero. Conversely, for b(y)∂_y, differentiating t²+yt+y=0 forces

a(t)=b(y)(1+t)/y=b(y)(1+t)²/t².

This is its unique field extension. Uniqueness implies N-invariance. It preserves k[[t]] exactly when ord_t(a)≥0, equivalently 2 ord_y(b)−2≥0. Thus its coefficient b lies exactly in y k[[y]]. Consequently restriction identifies

Theta^N ≅ M=y k[[y]]∂_y.

Restriction commutes with conjugation by G because G normalizes N. This makes the identification Q-equivariant, rather than merely a vector-space isomorphism. For the order-two quotient generator the conjugation action on coefficient functions is

T(f)(y)=(1+y)² f(y/(1+y)).

This follows from sigma^(-1)=sigma and the chain rule: sigma'(sigma(y))=1/sigma'(y)=(1+y)². It agrees with the source's right-conjugation convention; all relevant group elements are involutions, so there is no inverse ambiguity in this formula.

Set z=y²/(1+y). As above, k((y))^Q=k((z)), and ord_y(z)=2. For f∈y k[[y]], the equation Tf=f is equivalent to f/y² being fixed by Q. Its y-valuation is at least −1. A nonzero element of k((z)) has even y-valuation; hence an invariant f/y² has nonnegative valuation and lies in k[[z]]. Therefore

M^Q=y² k[[z]]∂_y.

For every full formal power series h(z)∈k[[z]], not only polynomial h,

(T−1)(y h(z))=y² h(z).

This holds because h(z) is invariant and T(y)−y=y². Substitution and multiplication are continuous, so it also follows coefficientwise from the polynomial identity. Every invariant is therefore a coboundary. Since Q is cyclic of order two and the characteristic is two,

H¹(Q,M)=ker(1+T)/im(T−1)=M^Q/(T−1)M=0.

The finite-group cochains can be treated as ordinary or continuous cochains with t-adic coefficient modules: the domain G^n is finite discrete, so every cochain is continuous. No unproved passage from truncated cohomology to formal-series cohomology is used.

The inflation–restriction exact sequence now implies injectivity of

H¹(G,Theta)→H¹(N,Theta).

One can verify the relevant kernel statement directly: subtract a coboundary so that a cocycle whose restriction class is zero vanishes on N. The cocycle identity then shows its values are N-invariant and constant on cosets of N, so it is inflated from a Q-cocycle in Theta^N. The vanishing just proved makes it a coboundary. This argument uses only degree-one cochains and also checks the exact-sequence interface independently.

The tangent identification T D_H=H¹(H,Theta) comes from writing a first-order lift as (id+e d_g)rho(g). The group relation is the cocycle identity, and an identity-reducing coordinate conjugation changes d_g by a coboundary. Restriction of lifts restricts the cocycle. Therefore the actual tangent restriction D_G(A)→D_N(A) is injective. Since D_N^Q(A) is a subset of D_N(A), it is also injective with that fixed-subfunctor codomain. No map from D_N^Q to F is extended to D_N.

The proposed tangent obstruction group is indeed one-dimensional here: Theta-sharp/Theta^N is the constant-coefficient quotient k, on which T acts trivially, and H¹(C2,k)=k. The negative result does not depend on enforcing this dimension.

## 5. The fibre product and smoothness

Assume maps f:D_N^Q→F and g:D_Q→F, with F prorepresentable, make the prescribed restriction–induction map factor through E=D_N^Q×_F D_Q and be smooth. The basepoint 0∈D_N^Q(A) is obtained from the residual action by the map k→A. It belongs to the fixed functor, for example because it is the restriction of the constant G-action over A. Naturality gives f_A(0)=0 in F(A). Section 3 gives g_A(v)=0. Hence (0,v) is a point of E(A).

All residual functor values at k have one element. Smoothness for the small surjection A→k therefore requires a w∈D_G(A) mapping to (0,v). Its restriction is zero, so Section 4 gives w=0. Induction preserves the basepoint by naturality under k→A; hence ind(w)=0, contradicting v≠0.

The fibre product is evaluated pointwise in sets. Thus this final contradiction does not need an additional assertion that arbitrary maps f or g are linear on tangent spaces, nor does it require prorepresentability of either source factor. Only the restriction kernel calculation uses its explicit linear cohomological description. This verifies the potentially delicate source/target interface of the candidate.

## 6. Independent computational verification and corrections

The original `check_conjugacy.py` used Python `assert` for its two tests and then printed success flags. Both tests disappear under -O or -OO. An actual separate mutation removing the e² term from the target parameter fails normally but prints success in both optimized modes. This is an auxiliary-verification defect, not a defect in the hand-checked identities or proof.

The corrected script replaces both assertions with explicit conditional exceptions. A separate independent checker uses exact F4 polynomial rational functions and explicit triples for F4[e]/e³. It verifies all 16 group-composition cases, quotient/derivative identities, exact rational invariant and coboundary identities for z^0 through z^8, conjugacy/involution, and the fixed-ring criterion on all 64 elements of F4[e]/e³.

The independent checker passes normally, under -O, and under -OO. Six meaningful mutants are rejected in all three modes: wrong quotient action, wrong derivation weight, missing parameter shift, missing conjugator translation, missing projective scalar, and wrong fixed-ring automorphism. These are 18 rejected mutant runs. The same tests cannot replace the formal-series/cohomology/naturality arguments in Sections 3–5.

Frozen inputs were set read-only. Under the actual nonroot effective UID 1000, attempts to open the proof and original checker with O_WRONLY and to create a child in the frozen directory all raised PermissionError. Frozen and original hashes were rechecked unchanged. There was no chmod-only or root-writable simulation substituted for those probes.

## 7. Literature boundary

The 2009 nonprorepresentability result and its explicit conjugacy are prior results and are credited as such. Its §6 also gives related failures for the involution functor; those were inspected as literature context, not introduced as another proof route here. The 2011 preprint and the [author's Utrecht thesis](https://research-portal.uu.nl/en/publications/cohomological-aspects-of-equivariant-deformation-theory/) formulate the decomposition problem. The [Ghent talk abstract](https://cage.ugent.be/~kulrug/abstracts/abstract_byszewski_lorscheid.pdf) describes the same restriction/induction setting but supplies no solution.

Targeted searches combining the paper title, local deformation functors, fibre products, negative answers, counterexamples, and Question 4.4 found no exact prior negative factorization result. This is a bounded search finding only. The audit endorses mathematical correctness for the literal statement, not novelty or a claim that all later literature has been exhausted.

## Acceptance boundary

- Accepted: the full unrestricted nonexistence statement for this explicit local action, and therefore a negative instance for the refined requested tangent-space formulation.
- Unaffected: conditional obstruction-space theorems assuming prorepresentable subgroup and quotient functors.
- Not claimed: a result for pointed deformations, deformation groupoids, framed functors, or a revised question with extra prorepresentability assumptions.
- No original proof, source, dataset, repository, queue, or remote state was modified during this audit.
