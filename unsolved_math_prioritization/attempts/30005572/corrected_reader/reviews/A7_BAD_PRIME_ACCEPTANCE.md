# Independent acceptance: actual restricted bad-prime arithmetic identity

Shared PASS2/5, row 1777 / 30005572. Audit date: 14 October 2026 UTC.

## Decision and exact accepted input

**ACCEPT the corrected restricted arithmetic theorem.** Final audited input: `pass2_bad_prime/BAD_PRIME_NORM_AND_RESTRICTED_IDENTITY.md`, SHA256 `7af38b596ee39ad4447a63eac17ea4c28e0c07177021e4f15277c2b2d5e29e5a`.

The theorem applies to the actual existing LSSW auxiliary maps, with p>=7, principal q=(pi), N=M q^n, q coprime to M, and M proper and admissible in the source's sense. All h class-group components are retained. For the declared dual unnormalized U* correspondence it proves

Cor_{F(N)/F(M)} f_{c,N}(U*−1)=0.

On a prime-to-p character component inflated from F(M), if p does not divide d=Q^(n−1)(Q−1), it proves the actual equation f_{c,N}^chi(U*−1)=0. At the components where source Corollary 4.3.2 supplies an invertible auxiliary factor, this gives the unaugmented equation as well. A separately established compactified map inherits it.

This is more than the conditional boundary mechanism of PASS1: the proof evaluates the actual geometric cocycle and obtains an arithmetic norm relation. Its restrictions are essential, and the full construction remains unsolved.

## 1. Defect found, repair, and verification history

The initially frozen input, SHA256 `96467b04e0be9943f096c8b1d1dc7bf513b16f68732a2b1b9e3afc8f8cdaa465`, used column-lattice entry ideals in §2 while using the source's row action in the CM specialization argument. With a=a_r, it had b in a and c in A a^{-1}. The source instead defines a_{r,s}=a_s a_r^{-1}; for its (r,1) component acting on E_r×E_1 by rows, b lies in a^{-1} and c in a. Its moving entry x belongs to Hom(E_1,E_r)=a, confirming this orientation. The initial text therefore did not justify an all-component theorem as written.

The author corrected the strict group to the row-lattice convention, the lower-unipotent coset parameter to N a/(pi N a), and the corresponding membership statements. The intermediate corrected hash was `3d11d83bca56a59b0c8b73cfcd177f8361478b056a7e6159e9ad15006facbf04`. The formal matrix algebra was unaffected, but the actual source component identification is now correct. This was a genuine convention defect, not merely a notation preference.

A second clarification was requested: equality of relative ray degrees alone does not imply the claimed intersection without identifying the compositum. The final text now invokes the CRT product decomposition of the relative ray kernels using admissibility of the common lower modulus A. It explicitly obtains both the compositum F(Nf)=F(N)F(Af) and the intersection F(N) cap F(Af)=F(A). The auxiliary definition prime is also required to avoid every fixed class representative a_r, as in the source's setup.

The final hash above includes both repairs. They were made by the author within the same shared pass; this audit did not edit the proof. There are no remaining defects in the stated theorem identified by this audit.

## 2. Groups, correspondence, and all components

For the row lattice a×O, the corrected group has b in a^{-1}, c in A a, determinant in O^times, and d=1 modulo A. The source allows d to reduce to a global unit. Under its unit-injectivity hypothesis, that unit is unique. Dividing by its central scalar matrix decomposes the source group as the product of the strict group and O^times. Their intersection is trivial. The central factor has order 2, 4, or 6 and contributes no H1 with Z_p coefficients for p>=7. It acts trivially on hyperbolic space. Thus the strict-group replacement is legitimate for the source maps and the correspondences used here.

Set alpha=diag(1,pi) and beta=diag(pi,1). The declared homology U* is transposed to the constant-coefficient Hecke sum of alpha. This is the dual of the beta correspondence: beta^{-1} differs from alpha by a scalar, whose geometric action is trivial. No factor Q is divided out. This convention must continue to be stated; the paper's expectation does not itself provide a full bad-prime normalization.

For N=Aq, conjugation by alpha^{-1} takes c to c/pi and b to pi b, so D maps the corrected strict group of level N into that of A. With ell_t representing N a/(pi N a), the matrices

h_t=[[1,0],[ell_t,pi]]=alpha k_t,
 k_t=[[1,0],[ell_t/pi,1]]

lie in the asserted double coset, and k_t lies in the low-level strict group. The intersection with alpha Gamma_N alpha^{-1} imposes c in qN a, and has index Q. Lower unipotents realize each coset. The count is local on the rank-one ideal a and does not assume a principal. Since q itself is principal, the determinant class does not shift the global component r. Hence the argument works separately on every one of the h components and then sums them.

The group-cochain transfer formula gamma h_t=h_s tau_t gives exactly the declared constant-target homology pairing. No Artin action of pi at the high, q-divisible modulus is inserted.

## 3. One-coordinate trace and moving primitives

The unspecialized primitive is

v_c = c theta_r exterior E_1[c] + Nc (0) exterior c theta_1.

Under alpha=id×[pi], the finite subscheme E_1[c] is permuted because c is coprime to q. The norm of the trace-fixed theta primitive has the same divisor as theta_1 and is trace-fixed. Source uniqueness therefore gives [pi]_* c theta_1=c theta_1. Pushforward fixes v_c and its boundary. This uses the one-curve trace-fixed normalization, not a claim that invariance under simultaneous scalar traces alone implies invariance under alpha.

Choose x in c Hom(E_1,E_r) prime to the lower level A. The matrices mu_A with lower entry x and mu_N with lower entry pi x satisfy the exact row-matrix equality

mu_N alpha = alpha mu_A.

The associated square is Cartesian because the moving matrices are automorphisms. Proper pushforward and pullback therefore give alpha_* mu_N^* v_c=mu_A^* v_c.

Every point (0,R) in the alpha-fiber over (0,P_A) satisfies pi R=P_A. Its moved first coordinate is (pi x)R=xP_A, which is nonzero since P_A has exact proper A-order and x is a torsion isomorphism at A. Moreover R is not c-torsion, since its image P_A is not. Thus both supports avoid the entire fiber. The key point is not that pi x is a high-level unit; it need not be. The proof correctly replaces that unnecessary condition by direct support avoidance.

For gamma at level N, gamma_A=alpha^{-1} gamma alpha is at level A, and alpha gamma_A=gamma alpha. Proper base change gives alpha_* gamma^*=gamma_A^* alpha_*. The residues of the two generic cocycles therefore agree. They are both trace-fixed, so the injective left map of the source's Gersten complex over Z[1/30] identifies them. This is also valid after passage to Z_p for p>=7.

The switch from these compatible moving matrices to the source's standard representatives is justified. The difference of moved primitives is a trace-fixed degree-one cycle with zero boundary. Its trace-fixed K2 primitive has residues supported away from the specialization orbit, hence is regular on an open containing that orbit. The two cocycles differ by its coboundary. On the strict subgroup the point is fixed, so the specialized coboundary is zero. This proves equality of the actual homomorphisms, not merely equality of generic symbols with an unspecified specialization.

This step uses the source's already established Z[1/30] Gersten exactness and one-curve theta uniqueness. It does not extend either foundational statement to Z[1/6].

## 4. Fiber arithmetic, lower-order branch, and descent

If q divides A, all Q points above P_A have exact N-order. The relative ray group has order Q and acts simply transitively on them. With a CM definition modulus f coprime to N and the stated admissibility hypotheses, this is the actual relative ray-field fiber. Specialization of the trace identity is therefore

Cor_{L_N/L_A} f_{c,N} = f_{c,A} D.

If q is coprime to A, the fiber consists of one A-torsion preimage R_0=pi^{-1}P_A and Q−1 exact-N-order points. The latter form the relative ray-field orbit. The lower-order branch is not discarded. Its specialization is sigma^{-1} f_{c,A} F, where sigma=R_A((pi)). To verify the sign, choose a representative congruent to pi modulo A and to 1 modulo f. Source Lemma 3.1.4 and Proposition 4.1.2 identify its direct Galois action with multiplication by pi on the marked torsion point. The preimage R_0 therefore carries the inverse action. Replacing the high moving matrix by a low-level admissible one changes no value on Gamma_N. Hence

Cor_{L_N/L_A} f_{c,N}=f_{c,A}D−sigma^{-1}f_{c,A}F.

All appearances of sigma are at the q-free lower modulus. R_N(q) is never defined.

The descent argument is sound after the final clarification. Choose a rational prime l=2 modulo p, l>3, avoiding the specified finite set, and a prime f above it. Dirichlet's theorem supplies such primes. The residue degree is 1 or 2; thus |(O/f)^times| is 1 or 3 modulo p, respectively. For p>=7 it is prime to p. The source's descent comparison therefore applies without losing p-information, and restriction to the auxiliary definition field is injective by transfer-restriction multiplication by its prime-to-p degree.

For completeness, the relevant ray-field CRT argument is as follows. A is admissible. A unit congruent to 1 modulo A is therefore the identity. Consequently the kernel of the ray map at Nf down to A is the direct product of the additional q-level local factor and (O/f)^times, with no residual diagonal-unit quotient. The two factors are exactly the kernels for the maps to Af and to N, respectively. Their intersection is trivial, proving the compositum assertion; their product is the whole relative group, proving the field intersection assertion. This verifies that the norm in the geometric fiber is the base change of Cor_{L_N/L_A}, rather than an altered-degree norm. The desired equalities descend to L_A.

Galois invariance alone would have been insufficient to supply this descent; the proof does not use it that way.

## 5. Three exact degeneracy identities and normalization

For any low-level constant-target homomorphism f, the relation h_t=alpha k_t gives

tau_t(gamma)=k_s^{-1} gamma_A k_t.

Summing f cancels all k terms because s is a permutation. Thus f F U*=Q f D, with the exact unnormalized index Q.

If q divides A, conjugating h_t by alpha gives [[1,0],[ell_t/pi,pi]], which is precisely the Q-branch lower-level bad double coset because ell_t/pi runs through A a/(pi A a). This proves D U*_{q,N}=U*_{q,A}D, with no index correction.

If q is coprime to A, the same Q conjugated representatives comprise Q of the Q+1 branches of the good alpha correspondence at A. Strong approximation in the determinant-one arithmetic lattice allows a matrix w in the strict low-level group whose upper-left entry is divisible by pi and whose local reduction is Weyl-type. With corrected row-ideal membership,

delta=beta^{-1} w alpha

is integral on a×O, has unit determinant, lies in Gamma_0(A), and has lower-right residue pi modulo A. The missing branch is h_infinity=w alpha=beta delta. Direct multiplication using alpha beta=pi times identity gives

h_infinity^{-1} gamma_A h_infinity=delta^{-1} gamma delta.

Since gamma acts trivially on the target and delta acts by sigma, the crossed-homomorphism identity is exactly

f(delta^{-1} gamma delta)=sigma^{-1}f(gamma).

The potential coboundary contribution is delta^{-1}(gamma−1)f(delta), which is zero here. This gives

f D U*_{q,N}=f T*_{q,A} D−sigma^{-1}f F.

The lower-level good Hecke normalization is crucial. The weighted motivic alpha operator has eigenvalue Q+[pi]^*, as follows from the full-level theorem and unchanged good-prime cosets on restriction; the corresponding Gamma_0(A) alpha and beta cosets are identified by the same w and delta. After specialization, every alpha coset has coefficient action sigma. The scalar [pi]^* specializes as sigma. Restricting to the strict group kills coboundaries and yields

sigma f T*_{q,A}=(Q+sigma)f,

so

f T*_{q,A}=(1+Q sigma^{-1})f.

This is not Q+sigma in the declared constant-coefficient dual convention. Both the lower-order torsion branch and the missing Hecke branch carry the same inverse Artin action, and the proof uses this consistently.

Writing C=fD−sigma^{-1}fF, the first-step computation is then

C U*=(1+Q sigma^{-1})fD−sigma^{-1}fF−Q sigma^{-1}fD=C.

At higher steps, the trace identity and conjugated double cosets give the recursive norm of the defect. Iterating down to the first q-step proves Theorem A. This establishes an arithmetic constraint on the actual cocycle defect, not a heuristic boundary eigenvalue argument.

## 6. Character projection, norm injectivity, and auxiliary cancellation

Because M is admissible and q is coprime to M, the relative ray degree is exactly d=Q^(n−1)(Q−1). If p does not divide d, I=Gal(L_N/L_M) is a subgroup of the prime-to-p part. A source character component trivial on I consequently has I acting trivially on its entire arithmetic module, including its retained class-group p-part. Therefore

res Cor(z)=sum_{g in I} g z=d z

and corestriction is injective there. This proves Theorem B from Theorem A. No norm injectivity on the whole target, no averaging over a p-group, and no cancellation by a nonunit is used.

For chi different from omega^2 in the source's exact convention, Corollary 4.3.2 supplies a proper auxiliary ideal c for which (Nc)^2−R_N(c) is a unit in the component group ring. Calibration and commutation with source precomposition permit cancellation. On exceptional components the source's Theorem 4.3.5 may instead prove the target component zero; the report only invokes that tautological case and does not cancel an arbitrary exceptional smoothing factor.

The original localized target injects into the field K2 group, so field-target vanishing proves vanishing in the original target. It does not improve that target by itself. A separately existing compactification inherits the identity because the rational correspondences preserve cusp subgroups and hence the homology quotient used to add cusps.

## 7. Scope that must not be widened

1. At n=1, only p not dividing Q−1 is needed; q may lie over p. At n>=2 the condition excludes q above p, because p then divides Q. The proof provides no wild-depth identity even on an ostensibly unramified residual character.
2. A character nontrivial on a prime-to-p relative ray subgroup can have its entire component killed by the norm. The norm-kernel identity has no vanishing content on that component.
3. If p divides the relative degree, retained p-group action and p-primary norm kernels remain. The identity res Cor=d is not an integral cancellation argument.
4. M must be proper and admissible. In particular, **Theorems A and B do not cover prime-power levels N=q^n**, for which M=O. The origin cannot replace the missing lower-level primitive specialization.
5. The one-coordinate trace identity extends intrinsically between nonprincipal marked CM product components. The final theorem on the source's standard (r,1) tuple has only been proved for principal q. The second CM component changes for a nonprincipal q; the associated determinant class shifts by [q]^{-1}. The text correctly does not assume this assembly has been carried out.
6. PASS1's boundary nilpotence remains a separate theorem. To remove the source's single-power restriction above p, an actual U*=1 identity is needed at those higher p-depths. The accepted restricted theorem does not supply it. The residual-character exclusions of the boundary argument are not removed either.
7. No 5-primary construction, small-level construction, integral relative theta prescription, or full compactified map is obtained. The pure prime-power integrality lane and this M-proper arithmetic theorem are separate partial advances; combining them does not close either missing case.

## 8. Reproducibility and source boundary

The supplied exact-rational matrix checker was read and independently replayed. It passed 825 samples, 3450 bad-coset/first-degeneracy identities, 550 higher-depth intertwinings, and 275 missing-branch conjugations, with 1425 good-coset equations. The checker uses explicit runtime conditions rather than removable assertions for these tests. Its computations are useful inverse/convention checks in a local rank-one basis. They do not compute CM K2 values, establish general fractional-ideal membership, or substitute for the proof above.

The source checks used the retained author manuscript of Lecouturier–Sharifi–Shih–Wang, particularly §§2.1–2.4 (row modules and Hecke transfer), §3.1 (torsion/Artin action), §§3.2–3.4 (trace-fixed primitives and regular specialization), §4.1 (descent and the good-prime theorem), §4.3 (character normalization and auxiliary cancellation), and §5.1–5.2 (homology and the bad-prime expectation). Official manuscript URL: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . The distinct arXiv v1 is https://arxiv.org/pdf/2504.19125v1 . Their retained PDF hashes are recorded in the audit manifest.

The cyclotomic comparison in the input is not used to prove the Bianchi theorem. No result is imported from that setting to fill a missing Bianchi degeneracy-surjectivity or higher-level bad-prime hypothesis. This audit is not a foundational reproof of all the established LSSW construction, and it makes no novelty claim.
