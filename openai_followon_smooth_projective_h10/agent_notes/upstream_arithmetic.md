# Independent upstream arithmetic audit

Checkpoint: 2026-10-06 PDT. Assigned arithmetic audit: about 90% complete; this is not certification of H10(Q) or the project core claim. Publication review: 0%.

Current route: the Pan-at-5 replacement proof in the correction below is the accepted candidate. The direct von Kanel–Kret shortcut is withdrawn after an independently checked counterexample to its restriction-of-scalars step.

Pinned read-only input: /Users/alec/Desktop/math, commit adc7f1241b42e322a6451854ab7e4b4c146bf78a. No source edits or Git mutations. Source prefix H = preprints/Hilberts-tenth-problem-over-the-rational-numbers-September-24-2026/build/sections/.

## Strongest checked result

No substantive arithmetic counterexample was found in H/05-elliptic.tex, H/06-primes.tex, or H/04-height.tex:1-696 after line-by-line audit. The five-point height bound can bypass the repository Fontaine–Mazur-at-2 companion by using the source controlled descent at coefficient prime5 and published Pan2022 modularity. The original long descent proof and its companion are not certified by this audit. The repaired route remains dependent on the stated geometric family construction, which was inspected here, and on the independently reviewed reduction/parity arguments elsewhere.

## Five-point geometry and height comparison

H/04-height.tex:40-175 constructs the discriminant-210 quaternionic quotient. Norm-one stabilizers would generate Q(i) or Q(sqrt(-3)), excluded by the splitting of ramified primes 5 or 7. Area/(2pi)=((2-1)(3-1)(5-1)(7-1))/6=8 gives genus 5. The 16-element Atkin–Lehner group has cyclic stabilizers of exponent two. Five explicitly distinct labels 30,42,70,105,210 force five branch values and quotient genus zero by 2g*-2+r/2=1/2. Each label has a unique branch value, hence it is individually Q-rational. These calculations agree with the primary Nualart thesis Propositions 4.1–4.2 and the existing Long–Maclachlan–Reid signature.

H/04-height.tex:184-280 constructs a faithful rational symplectic representation on B, a self-dual lattice, sufficiently small Siegel level, and a principally polarized abelian scheme over the compact finite-level curve. Its rational Hodge structures give left B endomorphisms and common-base geometric isogenies; changing finite adelic level changes lattices up to isogeny. Nonconstancy follows because a fixed rational Hodge structure has only countably many presentations, whereas the domain disk varies continuously.

H/04-height.tex:303-347: outside fixed bad primes, branch multiplicity two gives local t=z² after an unramified extension. Even contact therefore supplies unramified lifts. A finite fiber splitting field has bounded degree; properness and the spread abelian scheme imply good reduction outside fixed S, including places ramifying at odd-contact primes.

H/04-height.tex:364-548: a nonconstant theta-null map on a fixed finite curve cover pulls back O(1) to an ample line bundle. The coordinate normalization and finite Fourier basis changes preserve heights up to a level-dependent bounded term. Rational-characteristic density forces nonconstancy at some sufficiently divisible even level. Pazuki, Theta height and Faltings height, Corollary 1.3(2), gives the claimed bound between truncated positive theta/Faltings heights. Its actual statement was inspected at https://www.numdam.org/item/BSMF_2012__140_1_19_0.pdf pp.21–22. Thus the base height comparison has no degree-of-residue-field dependence. No defect was found in this application.

H/04-height.tex:584-615: the Galois transport action on the direct sum of Hom lattices has bounded finite image, so one Galois L/Q has bounded degree and defines all conjugacy Homs. At good places outside S and outside ramification of K0, Tate inertia acts trivially on the Homs; no new ramification occurs outside T=S union supp(M).

## Withdrawn proposed literature shortcut: exponent24

Primary source inspected: Rafael von Kanel and Arno Kret, Integral points on coarse Hilbert moduli schemes, arXiv:2307.06944v1, https://arxiv.org/pdf/2307.06944v1. Current arXiv metadata checked 2026-10-06 PDT shows only v1 (13 July 2023) and no journal reference. Cite as an existing primary preprint, without implying human refereeing.

Proposition 7.13, printed p.66 (PDF index 65), bounds stable Faltings height of a non-CM relative-dimension-g abelian scheme over an open U in Spec O_K by
h_F(A) <= (4g[K:Q])^(144g[K:Q]) rad(D_K N_U)^24.
Definitions in Section 7.1.1, equation (7.1), require a degree-g number field E in End0(A) and E-compatible isogenies from every G_Q conjugate. Condition (*) in Section 7.1.2 requires K/Q normal and all geometric endomorphisms and those isogenies K-defined.

Application proof:
1. For the non-CM fiber, End0(A)=B and B is division (H/04-height.tex:682-687). Every quadratic maximal subfield E in B supplies the required degree-two field. Division excludes a degree-four commutative semisimple CM algebra.
2. Let K=L from the Hom-field lemma and U=Spec O_L with primes above fixed S removed. Good reduction extends A over U. The field degree is uniformly bounded; all geometric endomorphisms and conjugacy Homs are L-defined.
3. For each g in Gal(L/Q), transport the B-action along any common-base isogeny. This is an automorphism of B, inner by Skolem–Noether. Composing with the inner correction yields the B-compatible quasi-isogeny at H/04-height.tex:710-720; clear its rational denominator to make an actual isogeny. This is E-compatible. Since A and all its endomorphisms are defined over L, all G_Q conjugacies reduce to this finite list. Condition (*) holds.
4. Rational primes dividing N_U belong to fixed S; rational primes dividing D_L belong to T. Hence rad(D_L N_U) <= (product of p in S) M.
5. Apply Proposition 7.13 and take the maximum over bounded degrees [L:Q]. This gives h_F(A)<=C M^24 with fixed C. The checked base-height comparison gives h(s)<=H M^24. The source CM argument at lines657-680 gives a uniform bound and therefore the same bound because M>=1.
6. Alternatively, source geometric CM fibers have End0=M2(k), all endomorphisms defined over L. Proposition 7.14, printed p.67, directly gives h_F<=C rad(D_L)^10<=C M^10. It also avoids CM class-number ineffectivity.

The paragraph above describes the initially proposed shortcut, now withdrawn due to the counterexample below. The child report agent_notes/height_descent.md independently checked the same application. The existing source itself mentions related vK/vK–Kret bounds at H/04-height.tex:1311-1326, so this is an exact streamlined application of known machinery rather than a new Shafarevich theorem.

## Rank, formal logarithms, prime patterns

H/05-elliptic.tex:21-111: O_F=Z[sqrt2] is principal by Minkowski. The 2-isogeny images have sizes 8 and 1. The first upper bound follows from even valuations away from (d); four two-torsion classes plus Q with mixed real signs reach 8. The second image is trivial: x is totally positive; odd valuation at the dyadic prime is ruled out by v(4d²)=4; the remaining case v_(d)(x)=1 would require -4 square in F7, impossible. The index formula therefore gives rank1. No arithmetic flaw was found.

H/05-elliptic.tex:136-183: at unramified odd good places, invariant-differential integrality gives v(c_t)>=-v_p(t). Hence the log preserves valuations on the full formal kernel. The group identity [n']nP=[n]n'P proves the quotient-of-indices equality. For p>K+1, t>K implies t-1-v_p(t)>=K, which proves the truncation precision uniformly, including zero numerator. No infinite series is transferred to the nonstandard model.

H/06-primes.tex:145-191: r=1 mod8, r=3 mod7 splits in Q(sqrt2) and makes conjugate twists opposite. Frobenius in Z[i] gives orders r+1±2a, a²+b²=r. Their gcd has 2-part exactly4; a common odd prime l forces a=0 modl and b²=-1 modl. Hasse plus divisibility by4 proves r does not divide either order.

H/06-primes.tex:193-319: pairwise independence holds uniformly in A outside fixed primes. The finite multiplier catalogue is genuinely chosen before A; p-adic valuations are bounded, signed units are matched by fixed Dirichlet primes, and CRT ensures divided forms are integral, locally nonzero, and never -1 at controlled odd primes.

H/06-primes.tex:327-421: all coefficients and L are fixed before X grows. Pairwise nonproportional linear parts imply finite complexity; the primary Green–Tao theorem plus its cited inverse/Mobius inputs applies. The 2024 erratum was inspected and retains the needed inverse theorem. The singular-product lower bound is uniform in L because new primes have factors 1+O(p^-2); only the CRT density costs a power of log L. Prime-power removal is o(X³).

H/06-primes.tex:425-704: the explicit Selberg weights and O(nZ^6+Z^8) remainder are coherent. The bad-prime count has X/(L log X)+X^(7/8)+sqrt(X)logX. On an affine fiber, the remaining zero lines are distinct even when three ambient forms are jointly dependent, because the fiber constant is nonzero. Its sieve retains all t-1 logarithmic factors. Thus total loss is at most C X³/(L(logX)^t)+o(X³/(logX)^t), dominated by the lower bound after L then X are chosen. No circular uniformity claim was found.

## Finite exact computational checks

A direct in-memory Python check (no upstream writes) verified:
d d^sigma=7; w=d(1+sqrt2)^3; w³-w=-8d; Q=(799-565sqrt2,-31800+22486sqrt2) satisfies E.
For all 26 primes r<5000 with r=1 mod8 and r=3 mod7, exhaustive point counting verified the opposite-order sum, full two-torsion divisibility, absence of r factors, Gaussian trace representation, and the common-odd-factor congruences. Bad gcd examples were r=1249 (orders1280,1220,gcd20), r=2089 (2000,2180,20), r=3769 (3796,3744,52), r=4049 (4160,3940,20). These examples confirm that removing bad primes is substantive. Finite samples do not prove the asymptotic prime-pattern theorem.

## Companion and formalization boundary

The original modularity input is the repository Fontaine–Mazur-at-2 Theorem1.1, identified at H/04-height.tex:902-908. Child audited its correct invocation and downstream deductions but not its full proof. My additional spot audit read the companion deformation.tex:1-210 and patching.tex:23-104,267-914. The uniform Artin–Rees lemma has a correct fixed-presentation proof; no concrete patching counterexample emerged. This does not certify the 5000-line companion. The repaired height route makes that companion unnecessary here.

No lean/docs/004.md exists at the pin; catalogue searches found no family004 formalization. Absence is not a proof failure, but there is no checked Lean artifact validating the H10 theorem.


## Correction after deeper dependency audit: use Pan at p=5

The direct vK–Kret route above is NOT accepted as an independently validated repair. Its theorem statement matches the application, but its proof has a concrete restriction-of-scalars counterexample described below. The correct replacement is the source own controlled sign descent combined with published Pan modularity at p=5. This correction supersedes every earlier description of the vK–Kret route as verified.

### Exact replacement proof

Use the fixed geometric cover, common-base family, bounded Hom field L, dichotomy End0(A)=B versus M2(k), and base-height comparison already inspected at H/04-height.tex:1-696. Keep the existing CM argument. In the non-CM case keep H/04-height.tex:710-849 verbatim: Skolem–Noether produces B-compatible conjugacy quasi-isogenies, degree normalization reduces discrepancies to a sign cocycle epsilon, and the controlled splitting lemma produces a finite cochain beta with delta(beta)=epsilon. It has the source ramification control and L-prime degree at most CM. No modularity result enters these steps.

Choose coefficient embeddings of Qbar into Q5bar and Q2bar. The source formula at lines865-883 defines R_l(g)=beta(g) a_g mu_(g|L) g for l=5,2. Two sign factors cancel, so it is a genuine continuous representation. All scalar coefficients and the splitting of B lie in a finite coefficient extension. Its commuting B-action gives R_l=r_l direct-sum r_l. At G_(L-prime), R_l is the rational Tate module of A.

The source lines915-947 apply to either coefficient prime:
- Faltings identifies the endomorphism algebra of the Tate module over L-prime with B. After splitting B, r_l is semisimple with scalar commutant, therefore absolutely irreducible.
- Smooth-proper comparison makes the Tate module de Rham with cyclotomic exponents0,1, twice each; finite-local-extension descent and the repeated-factor decomposition give exponents0,1 once each for r_l.
- Complex conjugation followed by a holomorphic quasi-isogeny exchanges the nonzero Betti Hodge subspaces. Thus its action on r_l cannot be scalar. It is an involution and has eigenvalues1,-1, so r_l is odd.
- At q outside T union {l}, inertia fixes L, A has good reduction, and beta is trivial. Thus r_l has finite ramification.
- For r5, potential semistability follows either from the p-adic monodromy theorem applied to de Rham r5 or from semistable reduction of A after a finite local extension and the direct-summand property. This explicitly supplies Pan hypothesis, rather than replacing it by an unstated de Rham equivalence.

Primary published theorem: Lue Pan, The Fontaine–Mazur conjecture in the residually reducible case, Journal of the American Mathematical Society35(4) (2022),1031–1169, DOI https://doi.org/10.1090/jams/991. The exact Theorem1.0.4 and Conjecture1.0.1 hypotheses were inspected in https://arxiv.org/pdf/1901.07166v2, printed pp.2,5. For p>=5 it asserts modularity up to twist of every continuous irreducible odd finitely ramified potentially semistable two-dimensional p-adic representation with distinct Hodge–Tate weights. Its extra residual restriction concerns p=3 only. It therefore applies at5 without any residual-image or ordinarity requirement.

Apply Pan to r5. Its exponents0,1 force weight2 and zero Tate shift by the same comparison as source lines956-978. The same newform realizes r2: for each good Frobenius g at q outside T union {2,5}, source lines992-1038 construct the rational special-fiber endomorphism red(mu_g) composed with relative Frobenius. Its coefficient-prime-independent Tate trace gives the single algebraic number alpha_q=(beta(g)a_g/2)Tr(u_q). Injectivity at5 identifies alpha_q with the Hecke eigenvalue; injectivity at2 and Chebotarev identify r2 with the corresponding2-adic member.

For the level bound at source1043-1143, use r5 at every residue prime q except5, and use r2 at5. Both are members of this same compatible system. The tame and wild-inertia proofs use only l!=q, not l=2 specifically. At q=2 choose l=5, at q=5 choose l=2. The fixed small-prime argument uses bounded local degrees over L, and the independently chosen torsion prime p0>=3 differs from q. All constants remain independent of s. Therefore N<=CM^a holds with the source fixed exponent.

Use Tate coefficient5 in the Faltings Hom argument at1178-1202. It gives A as an L-prime isogeny factor of the modular Jacobian. The source final Jacobian/isogeny/Faltings-height bounds1232-1308 are unaffected. They give h_F(A)<=CM^C, and the checked base-height comparison gives h(s)<=H M^c. This establishes the required five-point polynomial bound using the source arithmetic descent and published odd-prime modularity, independently of the dyadic companion and independently of vK–Kret Proposition7.13.

The new modulus5 is harmless even though5 ramifies in B: B becomes M2 after the finite coefficient extension already used. It does not have to split over Q5 itself. All substitutions are coefficient-prime changes, with exactly the explicit potentially-semistable and conductor checks above.

### Counterexample to the vK–Kret restriction-of-scalars claim

This is an independently checked proof defect in the optional external shortcut, not a counterexample to its numerical height inequality or to family004.

Let K=Q(i,sqrt2), a=1+sqrt2, and E0/Q:y²=x³-x+1. Its j-invariant is -6912/23, nonintegral, so E0 is non-CM. Let B/K be its quadratic twist
y²=x³-a²x+a³.
Take sigma(sqrt2)=-sqrt2, sigma(i)=i; take tau(sqrt2)=sqrt2, tau(i)=-i. Because a sigma(a)=-1, the isomorphism mu_sigma:B^sigma -> B uses t=i a and scales (x,y) by (t²,t³). Let mu_tau be the identity. Then t sigma(t)=1, tau(t)=-t, so the rational Hom cocycle has generators u,v with u²=v²=1 and uv=-vu.

All geometric endomorphisms of B are integers and K-defined; all conjugacy isogenies are these K-defined isomorphisms. Thus the literal condition(*) holds. Over the open O_K[1/(2*23)], B is an abelian scheme and satisfies dimension-one GL2 type and G_Q-isogenies.

R=Res_(K/Q) B has End0_Q(R)=Q_c[V4], by the usual descent/Weil-restriction Hom calculation. The displayed generators give Q_c[V4]=M2(Q). Hence R is isogenous over Q to C² with C Q-simple, dim C=2, and End0_Q(C)=Q. Its only simple isogeny class has no degree-two field in its endomorphism algebra, hence no simple GL2-type factor.

This directly contradicts the proof of vK–Kret Lemma7.4 (printed pp.55–56), which claims Res_(K/Q)B has a GL2-type simple factor solely from(*). It also contradicts the stated K-factor conclusion of Proposition7.2: any Q-simple C0 of GL2 type with B a K-isogeny factor of (C0)_K supplies a nonzero K-Hom (C0)_K -> B; Weil-restriction adjunction gives a nonzero Q-Hom C0 -> R, making C0 the simple class C just excluded. This argument was checked independently by the height_descent child.

The missing requirement is descent of the scalar cocycle splitting to the finite group, often expressed through strong modularity. A splitting on G_Q need not factor through Gal(K/Q). The Pan5 repair avoids needing this claim.


## Saved reproducibility artifact

Run python3 reproducibility/arithmetic_checks.py from the project folder. Output is checked byte-for-byte against arithmetic_checks.expected.json, with the reproduced arithmetic_checks.json saved. The compact script uses exact integer/isqrt arithmetic for all26 primes and field arithmetic in Z[sqrt2]. Script SHA256:9006a7056a0f26bffacf64e60e7bb2ad3d2d02332233b51b3397a7aaedd131ac. Expected/output SHA256:7fa2f1f7af9fd88ec824744b4922204145d6389eb51a3a406848939279a1d5bb. This artifact does not test global/asymptotic statements.
