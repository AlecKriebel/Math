# Hecke compatibility at five from exact norms and kernel incidence

Authored proof, 14 October 2026. Shared PASS 4/5; row 1777 / 30005572. This note proves the missing geometric Hecke identities at primes above five for the accepted normalized auxiliary family. It does not extend the T5-fixed coefficient subsystem to arbitrary isogeny pullbacks. No claim of a complete arithmetic construction is made.

## 1. Statement and inputs

Put R=Z[1/6]. Use the entire LSSW system of CM products A_i=E_i1 x E_i2, indexed by i in I^2 over the source model number field L, with its arithmetic groups Gamma_i and product-isogeny component changes. Let

M_i=K2(L(A_i)) tensor R,

and let M_i^tf denote eventual full-CM trace invariance. Let c be prime to (5), and write z_c,i for the accepted PASS 3 cocycle with prescribed residue gamma eta_c,i-eta_c,i. Its values are eventual trace-fixed and fixed by scalar pushforward S_i=[5]_*.

The inputs used below are exactly these accepted facts:

1. The normalized cocycles exist on every component, with no class-number or ramification restriction.
2. For every product of O-linear isogenies f:A_i -> A_j whose two kernel ideals are prime to c, the product primitives satisfy f_*eta_c,i=eta_c,j. Proper pushforward commutes with all scalar traces. On any intertwined subgroup this gives the literal identity

   f_* z_c,i(gamma)=z_c,j(f^(-1) gamma f).

   We use the source's row-vector convention throughout: an automorphism gamma acts on coefficients by gamma^*. This is a left coefficient action, because right multiplication on points reverses geometric composition before pullback. The displayed conjugation is exactly LSSW (2.7).
3. A closed C1 element which is eventual trace-fixed and S-fixed has a unique normalized M_i lift. Its residue determines where that lift is regular.
4. Eventual trace-fixed M_i, without the additional S condition, form an isogeny-pullback module system. In the pull-push base-change argument one enlarges the exceptional scalar ideal to exclude the isogeny kernel.

**Theorem.** If p is any prime ideal prime to c, then the ordinary geometric cocycle classes satisfy

T_p [z_c] = (Np + [p]^*) [z_c]                                       (1.1)

in the full component system of H^1(Gamma_i,M_i^tf). In particular (1.1) holds for every p above five for the PASS 3 family. Together with the already accepted geometric identities away from five, this gives the full all-prime geometric Hecke identity for every auxiliary c prime to five.

If N is a proper ideal prime to c and p is prime to N as well as c, the same identity holds after restriction to Gamma_0(N)_i in the coefficient modules of classes regular at the primitive N-torsion orbit. In particular the geometric good-prime identity at p above five is valid in the coefficient system used for specialization. This remains distinct from arithmetic ray-field descent, auxiliary removal, and a bad-level U_p^*=1 assertion.

## 2. Intrinsic translation traces and the non-Cartesian defect

For a finite etale subgroup scheme K of an abelian variety A, let

N_K = (pr_2)_* a^*

on its Gersten complex or motivic coefficient groups, where a:K x A -> A is addition and pr_2:K x A -> A is projection. This is defined over L even if K does not split over L. Over a splitting field it has the familiar expression sum_{k in K} t_k^*. The equality with that expression is a description of an algebraic correspondence, not an inference requiring restriction on K2 to be injective.

If f:A -> B is an isogeny with kernel K, finite-flat base change in the genuinely Cartesian fiber square A x_B A gives

f^* f_* = N_K,                  f_* f^* = deg(f) Id.                   (2.1)

These equalities hold integrally. The scheme A x_B A is identified with K x A by (k,x) -> (x+k,x).

Now suppose K is contained in A[5]. There is a unique complementary isogeny g:B -> A with gf=[5]_A and fg=[5]_B. Therefore

S_A f^* = deg(f) g_*,
f^* S_B = N_K g_*,
S_A f^* - f^* S_B = (deg(f) Id - N_K) g_*.                            (2.2)

This computes the non-Cartesian pull-push defect exactly, with no division by deg(f). It applies both to cyclic p-kernel isogenies and to simultaneous p-kernel product isogenies for every p above five, since A[p] is contained in A[5].

The defect need not vanish. Already on zero-cycles, if f has nontrivial K contained in A[5], then

S_A f^*[0_B] = deg(f)[0_A],
f^* S_B[0_B] = [K].                                                    (2.3)

These are different cycles. Thus individual pullbacks genuinely need not preserve the S-fixed coefficient submodule. Equations (2.2)-(2.3) do not produce a nonzero constant-valued cocycle and are not a counterexample to (1.1), or to the original construction target.

For scalar alpha prime to the order of K, multiplication by alpha permutes K. The corresponding Cartesian base-change calculation shows that N_K preserves eventual trace invariance. No assertion is made that it preserves S-fixedness.

## 3. An integral transfer identity, including its coboundary

Let G be a group, H a finite-index subgroup, M a left R[G]-module, and N an H-equivariant R-linear endomorphism of M. Put

A_N = sum_{r in G/H} r N r^(-1).

Then for any z in Z^1(G,M),

cor_H^G (N res_H^G [z]) = A_N [z].                                   (3.1)

Here G/H denotes left cosets, represented by r. The sum A_N is independent of representatives and is G-equivariant. This is the ordinary transfer projection formula, with no division by [G:H].

For completeness choose representatives R0, and for gamma in G write gamma r=r' h, h in H. One standard inhomogeneous corestriction representative is

cor(N res z)(gamma)=sum_r r' N z(h).

Since z(gamma r)=z(gamma)+gamma z(r)=z(r')+r' z(h), and N commutes with h, direct substitution gives

cor(N res z)(gamma)=A_N z(gamma)+gamma u-u,
u=sum_r (r N r^(-1)) z(r).                                                     (3.2)

In particular the transfer statement is a cohomology identity. It does not assert a false pointwise equality that discards inner-conjugation coboundaries. Formula (3.2) also identifies the specific correction to be checked when coefficients are required to be regular on an open neighborhood.

## 4. Norm compatibility changes Hecke pullbacks into kernel traces

Fix a component i and p prime to c. Choose the source's product isogeny

f:A_i -> A_j,

with kernel K=E_i1[p] x {0}, where j2=i2 and the first component changes by the ideal class of p. This is exactly the isogeny underlying the component T_p in LSSW Lemma 3.3.2. Let H=Gamma_i intersect f Gamma_j f^(-1), the subgroup of Gamma_i preserving K. Its element gamma descends to f^(-1) gamma f in Gamma_j.

Restrict z_c,i to H. Exact product-norm compatibility gives the target cocycle, pulled back in its group argument, as f_*res z_c,i. Pulling back coefficients by f and then corestricting gives the Hecke class. Thus (2.1) yields

(T_p [z_c])_i = cor_H^Gamma_i (N_K res_H^Gamma_i [z_c,i]).              (4.1)

This is precisely the restriction-conjugation-corestriction convention of LSSW Proposition 2.1.4: the middle cochain sends gamma to f^*z_c,j(f^(-1) gamma f). In particular, no assertion that f^* commutes with S has entered (4.1).

The group H has index q+1, q=Np. Its conjugate kernels are exactly the q+1 rank-one O/p submodule schemes of A_i[p]. One does not need reduction of Gamma_i onto all of GL2(O/p): its reduction contains SL2(O/p), which is transitive on the projective line. To see the needed containment for a possibly nonprincipal lattice, locally trivialize each rank-one lattice at p. The two off-diagonal Hom ideals reduce surjectively to their one-dimensional residue spaces; the corresponding integral upper and lower unipotents supply every elementary matrix over O/p. Those elementary matrices generate SL2(O/p).

Each line subgroup scheme is defined over L: choose an O-linear isogeny between the two elliptic factors with degree prime to p (an element of the relevant invertible Hom ideal with p-adic valuation zero). It identifies their p-torsion representations, so the Galois action is scalar on the rank-two O/p module, and fixes every line. Alternatively the Gamma_i orbit of the L-defined K already supplies all lines as L-defined subgroup schemes.

By (3.1), (4.1) is therefore the class of

(sum_{lines D in A_i[p]} N_D) z_c,i.                                  (4.2)

## 5. Kernel incidence kills the entire Hecke defect

As finite correspondences over L, the translation traces satisfy

sum_{lines D in A_i[p]} N_D = q Id + N_A_i[p].                         (5.1)

Indeed, zero belongs to every one of the q+1 lines, and each nonzero point of the two-dimensional O/p vector space belongs to exactly one line. This proves equality of the integral cycles defining the correspondences, hence equality of their actions on the Gersten complex and K2. Checking geometric points here verifies the correspondence itself; it does not use K2 descent or divide a torsion-field degree.

Choose the simultaneous ideal isogeny

f0:A_i -> A_k,

with kernel A_i[p], changing both component indices by p as in the definition of [p]^*. It has f0^(-1) Gamma_i f0=Gamma_k. The product norm law gives (f0)_*z_c,i(gamma)=z_c,k(f0^(-1) gamma f0), exactly the transport in LSSW Definition 2.4.3. Consequently

N_A_i[p] [z_c,i]=(f0)^*(f0)_*[z_c,i]=([p]^*[z_c])_i.                   (5.2)

Substitute (5.1)-(5.2) into (4.2) to obtain (1.1) on each component, without dropping any class-group component.

This proves more than annihilation of a possible constant defect after inverting five. The complete difference T_p[z_c]-(q+[p]^*)[z_c] is zero already over R. A representative may differ by the explicit transfer coboundary (3.2), and by primitive-change coboundaries if different shears were chosen. There is no residual H^1(Gamma_i,K2(L)[5]) class in this Hecke relation.

The proof requires p prime to c because it uses the exact product-norm law. This covers every p above five under the standing c-prime-to-five hypothesis. At p away from five which divides c, use the accepted PASS 3 zero-cycle/normalized-connecting-map argument instead; no coprimality is silently removed from the norm proof.

## 6. The regular coefficient system and good-prime specialization

Fix proper N prime to c. Let S_i be {0} times the primitive N-torsion orbit on the second factor. Write M_i(S_i) for the R-valued K2 classes regular in some open neighborhood of S_i. Take the accepted sheared primitive eta_c,i^mu with shear coefficient x in the appropriate c-Hom ideal and a unit modulo N, and its normalized cocycle z_i^mu on Gamma_0(N)_i.

Assume p is prime to cN. We claim that eta_c,i^mu and every Gamma_0(N)_i translate of it have support disjoint from

S_i + A_i[p].                                                        (6.1)

To check the claim, decompose pN-torsion into its N-primary and p-primary factors using coprimality. Every point of (6.1) has N-primary component (0,uP) with u a unit modulo N. The horizontal support E_i1 x E_i2[c] cannot contain such a point: its second N-primary component would have to vanish. On the sheared graph the equation is z1+xz2=0, whose N-primary part would require xuP=0, impossible. For a Gamma_0(N)_i translate, the relevant coefficients on this N-primary component are d and c_gamma+d x. Both are units modulo N, just as in the accepted ordinary regularity proof. Thus the entire translate support also avoids (6.1).

By its exact Gersten residue, z_i^mu(gamma) is regular near (6.1) for every gamma in Gamma_0(N)_i. In particular N_D z_i^mu(gamma) is regular at S_i for every subgroup D of A_i[p]. This establishes regularity of every term in the transfer correction u in (3.2), because all its coset representatives belong to Gamma_0(N)_i and this group preserves S_i.

We must also justify replacing the literal unsheared norm law by the chosen sheared representatives. For either f or f0 above, f maps S_i onto S_j, and

f^(-1)(S_j) is contained in S_i+A_i[p].                               (6.2)

The primitive f_*eta_i^mu is therefore supported away from S_j. Its boundary is e_c,j, as is that of eta_j^nu for any eligible target shear. Their difference is a closed C1 element which is both eventual trace-fixed and S-fixed: pushforwards commute with scalar traces, and c is prime to five. The accepted normalized lifting theorem supplies b_f with

partial b_f=f_*eta_i^mu-eta_j^nu.

Its residues have support away from S_j, so b_f lies in M_j(S_j). Thus on the intertwining subgroup

f_*z_i^mu-z_j^nu=delta b_f                                          (6.3)

as an equality in the coefficient module regular at S_j. The same is true for f0. Pullback, conjugation, and corestriction of these corrections are regular at the source orbit, by (6.2) and the preceding support calculation.

The double-coset decomposition still has q+1 terms for p prime to N. Concretely the upper root ideals and lower root ideals constrained by N still reduce surjectively modulo p, so the previous SL2(O/p) argument applies inside Gamma_0(N)_i. Therefore (4.1)-(5.2), including their displayed coboundaries, prove (1.1) in

H^1(Gamma_0(N)_i, M_i(S_i)^tf).

This is exactly the geometric regularity strength needed before one applies an authorized arithmetic specialization. It does not prove that such specialization lands in the intended ray field, nor that its values are integral at vertical primes. No bad-level U assertion is obtained by setting p|N in this argument: coprimality in (6.1)-(6.2) is essential.

## 7. What remains unresolved

The accepted normalized submodule is still not stable under every pullback. We do not assign a normalized auxiliary cocycle to p or pc when p divides five, and we do not assert the formal class identity [p]^*Theta_c=Theta_pc-(Nc)^2 Theta_p in a family whose right side has not been constructed. Formula (2.2) is the exact pull-push identity needed at five; Sections 3-6 establish the actual Hecke relation without that stronger extension.

This closes the missing geometric Hecke-at-five step for c prime to five, including the regular-at-N coefficient refinement at good primes. Arithmetic ray descent, all-character auxiliary removal, vertical integrality, unrestricted bad-level U, compactification, and relative theta-symbol calibration are separate obligations. The original construction remains UNSOLVED.

## Sources and verification boundary

The source conventions and incidence calculation were checked in the retained author version of E. Lecouturier, R. Sharifi, S.-C. Shih, J. Wang, *Eisenstein cocycles for imaginary quadratic fields*: Proposition 2.1.4 (pp.10-11), Section 2.4 (pp.18-19), Lemmas 3.3.1-3.3.2 and Proposition 3.3.3 (pp.23-24), and Remark 3.4.2 (p.26). Public source: https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf . Their statements over Z[1/30] are not imported as R-coefficient theorems; the proof above uses the accepted R-valued norm law and an integral transfer/correspondence computation.

Dependence: PASS 3 SCALAR_FIVE_NORMALIZATION.md, especially Sections 4, 6.2 and 7; its independent TRACE_NORMALIZATION_ACCEPTANCE.md; PASS 2 RIGHT_END_LIFTING.md, Sections 5-6; and the accepted Gersten constants-quotient exactness. The accompanying finite computations check representative line-incidence and transfer cases, not the geometric theorem by themselves.
