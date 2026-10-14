# Independent acceptance: nonprincipal inverse-U assembly

14 October 2026 UTC. Row 1777 / 30005572. This is independent review within shared PASS 4/5, not a new mathematical pass. No proof, ledger, queue, or remote file was changed by this reviewer. The original construction remains **UNSOLVED**. No novelty claim is made.

## Verdict and frozen package

**ACCEPT the corrected frozen package**, consisting of:

- `pass4_bad_prime_assembly/NONPRINCIPAL_DUAL_BAD_U.md`, SHA-256 `89757a18ca035d1f72cdf2ae6c63b6f987d01c3468eee3b766d38c5f2071a6fa`;
- `pass4_bad_prime_assembly/GEOMETRIC_CENTRAL_TRANSPORT_DETAIL.md`, SHA-256 `29242dbd60de40165c77c3b98f3a5899a6048abaa8cc12abb7aa68b74a3ae314`;
- `pass4_bad_prime_assembly/CONVENTION_AND_PRINCIPAL_RECOVERY.md`, SHA-256 `df00d9b385dc1d78c6d767ded31fa7f4d35805b203242a0e5fbf1dbfe4c0c592`.

The acceptance is for their combined argument, not the initial main-note pin `5f0ff04eade54b74abf44cfff02fb0ce17591a201785584785adf16c762c5b3c` read in isolation. Review required explicit principal marking recovery and clarification of the low-level central transport. In particular, weighted geometric diamond invariance must not be read as constant-coefficient diamond eigenvalue one. The revised package keeps that coefficient factor and identifies the exact central adelic double coset. These clarifications close the identified proof-presentation gaps; this review found no remaining mathematical error in the restricted theorem.

The theorem removes the principal-prime hypothesis from the accepted PASS 2/3 norm theorem. For every prime ideal q, with N=Mq^n admissible, M proper and prime to q, and p>=7, it proves

    Cor_(F(N)/F(M)) f_(c,N)(U_q^vee-1)=0.

Here U_q^vee is the true inverse of the first-coordinate local double coset, with no degree normalization. Actual vanishing of the defect is proved only on characters inflated from F(M), when p does not divide Q^(n-1)(Q-1)/u_M. Existing auxiliary cancellation and an independently available compactified map may be used only in their previously accepted scope.

## 1. Operator, determinant classes, and principal recovery

Take y=diag(nu,1) at q and identity elsewhere. The strict level group contains diag(u,1) for every local unit u, including at q. Thus the double cosets of y and y^-1 are independent of nu. The source convention identifies the homology component shift of y^-1 with [a_r] -> [a_r q].

The integral opposite matrix v=diag(1,nu) satisfies v=z_q y^-1, with z_q=nu I. Its component shift is [a_r q^-1]. Since z_q has shift [q]^-2, these are consistent. The central factor cannot be discarded for nonprincipal q. Nor does the theorem claim the opposite matrix has eigenvalue one.

When q=(pi), rational beta=diag(pi,1) and the local y differ at every prime only by first-coordinate units. Those units lie in the strict level group, even at primes dividing M. Consequently their inverse double cosets agree. The rational identity diag(1,pi)=pi beta^-1 gives exactly the earlier transfer correspondence: the global rational scalar acts trivially on the symmetric space and in the conjugation. This argument does not mistake the local central idele z_q for the rational scalar pi.

The new first-step norm formula has sigma g_A D-g_A F, while the old one has g_A D-kappa^-1 g_A F. The recovery supplement correctly explains the difference. With the low point fixed, the new high marking has A-primary component P_A, whereas the pi-coherent old marking has A-primary component pi^-1 P_A. Their ratio d has residue pi modulo A and unit residue modulo q. The resulting tau=R_(Aqf)((d')) has low restriction kappa, where d'=1 modulo f. Exact factorwise transport through the principal CM isogeny gives sigma g_A=kappa g_A without assuming descent at A. Undoing tau recovers the old formula, including its inverse Artin factor. This verifies both the admissible PASS 2 and nonadmissible-lower-level PASS 3 conventions.

## 2. Semilinear isogenies and standard-component assembly

The CM definition modulus f is prime to q, N, c, and the class representatives. The reciprocity lift sigma is chosen using a local uniformizer, with its q-free restrictions the ordinary Frobenius actions. The q-isogeny phi_r:E_r -> E_r^sigma agrees with sigma on prime-to-q torsion. This is the actual CM isogeny input, not an ideal Artin symbol at the bad modulus.

Naturality follows by evaluating both t^sigma phi_r and phi_s t on all prime-to-q torsion. The equality on this infinite torsion set identifies the morphisms. It applies to every matrix entry, including off-diagonal Hom modules, and does not require unrelated scalar generators to be chosen compatibly.

The curve E_r^(sigma^-1) has class [a_r q]. With s the corresponding standard index, it is F(f)-isogenous to E_s and has the same complex CM isomorphism class. Source Lemma 3.1.1 therefore supplies the required F(f)-isomorphism iota_r. The composite b_r=phi_r^(sigma^-1) iota_r, in the stated row-composition convention, has scalar eta_r with eta_r a_s=q a_r. Thus beta_r=diag(b_r,1) is exactly a first-coordinate q-isogeny from the s product to the r product, and beta_r^-1 has the desired inverse correspondence class.

The semilinear identities beta_r A_r=Phi_s and A_r beta_r^sigma=Phi_r are type-consistent in row convention. Naturality gives

    (A_r^-1 gamma A_r)^(sigma^-1)=beta_r gamma beta_r^-1.

The lower-left entry changes from c to c/eta_r. If c lies in Aq a_r, then c/eta_r lies in A a_s. The bottom-right entry is unchanged. Hence the induced D really maps the high strict group on r to the low strict group on s. The first coordinate alone is reidentified after sigma^-1; this part uses factorwise isomorphisms, not an unsupported invariance of axis primitives under a mixed Steinitz map.

Changing iota_r by a global unit introduces only a first-coordinate unit, contained in the strict level group. The correspondence and specialized map are unchanged.

## 3. Representatives, complete fibers, and the omitted torsion point

One-coordinate pushforward norms the theta primitive on the second curve and permutes its c-torsion, since q is prime to c. After the factorwise model transport, the resulting primitive is sigma of the standard low primitive, with the shear transported. This is stronger than abstract simultaneous-scalar trace invariance, and the proof uses the one-curve normalization to obtain it.

For x:E_1^sigma -> E_r chosen in the required Hom module and prime to A, every point R in the fiber satisfies

    (x phi_1)(R)=x sigma(P_A) != 0.

Also R is not c-torsion. The moved primitives and the relevant group translates therefore avoid the complete fiber. This verifies the regular specialization needed for proper pushforward/base change. It uses the fact that A is proper; the origin would invalidate it.

Any comparison with independently chosen moving primitives is justified at the level actually needed. The difference is a trace-fixed closed degree-one chain with support disjoint from the marked orbit. Trace-fixed Gersten exactness over Z[1/30] gives its primitive b. The support condition makes b regular near the orbit. After restriction to the strict point stabilizer, evaluation of its coboundary is zero. Generic cohomological equality alone would not have sufficed.

Because Af is admissible, the relative ray orbit has its full size. At q|A all Q fiber points are primitive Aq-points. At q not dividing A there are Q-1 primitive points and the unique A-torsion point. Under the new recursion phi_1(P_(Aq))=sigma(P_A), the latter point is P_A itself. Thus the extra term is exactly -g_A F. It has not been dropped or inadvertently given the old marking's inverse Artin factor. The resulting identities are the stated (5.2) and (5.3).

## 4. Exact degeneracies and the low central transport

Writing the inverse representatives as beta_r^-1 k_t, with the lower entries of k_t ranging over A a_s/q A a_s, yields

    tau_t=k_(s(t))^-1 D_r(gamma) k_t.

For any low constant-target homomorphism, the two k-sums cancel. There are exactly Q branches, so F U^vee=Q D. At higher depth conjugation gives the lower-level Q branches and D U^vee=U^vee D, with the component indices composed rather than artificially fixed.

At the first step, the omitted branch of the good inverse correspondence is diag(1,nu^-1). With the degeneracy it yields the central inverse, hence

    D U^vee=T_q^vee D-Z_q^-1 F.

Both sides land in component [a_r q^2]. The omitted term is a genuine inverse central/diamond correspondence, not an identity term on arbitrary low homology. The principal checker independently recovers its conjugation by the matrix with lower-right residue pi.

The low central calculation is justified before arithmetic descent. On the h^2 product tuple, the simultaneous q-isogeny factors rho through the sigma-conjugate product. The low marked-point discrepancy is kappa=R_(Af)((eta_2')), with eta_2'=eta_2 modulo A and 1 modulo f. Pushforward specialization gives kappa^-1 sigma, while pullback specialization gives kappa. Their product proves the weighted scalar-ideal action is sigma, retaining all factors upstairs.

Passing to standard components requires the diamond comparison. Its geometric class is invariant, but its constant-coefficient transfer has the inverse marking factor. The final package explicitly keeps this distinction. Taking delta with the same lower-right residue as rho makes delta^-1 rho have lower-right residue 1. Its coefficient factors cancel. The determinant class alone would not identify this operator: the supplement also checks the local elementary divisors (q,q) at q, lattice isomorphisms away from q, and bottom row (0,1) at every level prime. These are precisely the local conditions for the fixed central adelic coset Z_q.

The marked Steinitz adjustment exists: an initial lattice isomorphism maps the distinguished primitive vector to a primitive vector modulo A; the determinant-one finite group acts transitively on these vectors, and strong approximation lifts the required correction. Only the lower row is prescribed. No impossible determinant congruence is imposed. Its use on specialized homomorphisms is licensed by the regular comparison argument, not by literal preservation of separately chosen axis primitives.

The same orbit-regular geometric Hecke relation supplies the good eigenvalue Q+sigma. Since T_q^vee=Z_q^-1 T_q, the inverse eigenvalue is 1+Q sigma^-1. This remains valid for proper nonadmissible A over K_A. The source's descent theorem is not invoked at that A.

Substituting these identities into C=sigma g_A D-g_A F gives C U^vee=C by exact cancellation. Higher-level corestrictions propagate the defect to the first step, and Galois automorphisms commute with these corestrictions. There is no division by Q in this argument.

## 5. Fixed source markings and local-uniformizer dependence

Primitive N-points on E_1 form a torsor for (O/N)^times. Taking d with the prescribed ratio modulo N and d=1 modulo f gives the source marking comparison g_new=R_(Nf)((d))g_source. This is an actual target automorphism; it commutes with precomposition by the constant-coefficient U^vee, and its low restriction commutes with the corestriction. Norm-zero therefore transfers to the original source map. The statement does not secretly replace that map by a specially normalized new one.

A change of local uniformizer changes the reciprocity lift at the bad tower by q-inertia. It leaves the first-coordinate inverse double coset unchanged and is trivial on q-free K_M. Its possible change to the recursive q-primary markings is removed by the preceding comparison. Consequently the final norm-zero identity is independent of this choice. All ideal Artin symbols in the proof are at prime-to-ideal moduli; sigma at a bad modulus is only the restriction of a chosen automorphism.

## 6. Low-unit correction and permitted cancellation

The accepted PASS 3 ray-group calculation is independent of q being principal. With V=U_M, X=(O/q^n)^times, and Y=(O/f)^times, the relative group is (X x Y)/diag(V). Both projections of V are injective, respectively by high-level and definition-modulus admissibility. Therefore

    L_N intersect K_M=L_M,
    [K_N:L_N K_M]=u_M,
    [K_M:L_M]=b_f/u_M.

The generally non-Cartesian top square must retain its multiplicity. Factoring through the compositum yields

    Cor_(K_N/K_M) res_(L_N)^(K_N)(z)
      =u_M res_(L_M)^(K_M) Cor_(L_N/L_M)(z).

The chosen definition prime makes b_f prime to p; u_M divides 6. Thus u_M and [K_M:L_M] can be cancelled at p>=7, and restriction is injective by transfer. High admissibility identifies g_source with the restriction of the actual arithmetic map. These facts prove the descended norm-zero theorem, without equating invariants with descent.

For an inflated character and p not dividing d=[L_N:L_M], the entire relative group acts trivially on its component and res Cor=d. Cancelling this p-adic unit proves actual U^vee=1 there. The retained class-group p-part is not averaged away. On other character components a norm may be identically zero; at wild depth its degree may have a p-factor. Neither case permits the desired cancellation. The proof makes no such inference.

## 7. Reproducibility and acceptance boundary

The author checker was inspected and independently replayed under Python optimization: 6,528 inverse-coset equations, 1,536 semilinear conjugations, 960 higher-depth parameters, 1,536 principal scalar comparisons, and 240 class permutations passed.

The separately written `check_transport_conventions.py` passed 2,280 transfer equations, 2,280 principal scalar comparisons, 1,520 higher-depth conjugations, 128 omitted-branch conjugations, and 505 finite class-shift checks, also under optimization. The tests use explicit runtime checks, not removable assertions. They verify exact local matrix conventions and abstract class bookkeeping. They do not compute CM K2 values, principalize arbitrary global ideals, prove regularity, or replace the arithmetic argument.

This acceptance does **not** establish:

1. the pure prime-power case M=O;
2. any high nonadmissible-level arithmetic map;
3. actual vanishing on noninflated characters or inside wild norm kernels;
4. the five-primary arithmetic construction or unrestricted R-valued theorem;
5. new compactification, integer-ring integrality, or relative theta-symbol prescription;
6. eigenvalue one for the integral opposite local correspondence.

The new content is the nonprincipal standard-component assembly for the restricted inverse-U norm theorem. It is not a completion of the construction contract.

## Sources and previously accepted inputs

The retained author manuscript of Lecouturier, Sharifi, Shih and Wang, *Eisenstein cocycles for imaginary quadratic fields*, was directly inspected at Sections 2.1-2.4, 3.1, 3.3-3.4, 4.1, and 5.1. Relevant points include Lemmas 2.3.8, 3.1.1, 3.1.4, 3.4.3, and 4.1.7; Remark 3.4.2; and Propositions 4.1.8 and 5.1.2. Public author manuscript: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . The distinct arXiv v1 is https://arxiv.org/pdf/2504.19125v1 . The author manuscript is not relabeled arXiv v2.

The review uses the accepted PASS 2 principal proof and PASS 3 proper-lower-level extension, together with their independent audits, in exactly their frozen coefficient and scope ranges. Input and source-byte pins are recorded separately in this directory's manifest.
