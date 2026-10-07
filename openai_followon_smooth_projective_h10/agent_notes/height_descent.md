# Non-CM height arithmetic audit

Checkpoint: 2026-10-06 22:13 PDT (2026-10-07 05:13 UTC).
Assigned-audit completion estimate at this historical checkpoint: 90%, not certification of the upstream theorem. See the correction and final checkpoint below.

Read-only source: /Users/alec/Desktop/math, commit adc7f1241b42e322a6451854ab7e4b4c146bf78a.
Target: preprints/Hilberts-tenth-problem-over-the-rational-numbers-September-24-2026/build/sections/04-height.tex:697–1326.
No source edits, Git mutations, releases, or external communications.

## Conclusion

No concrete internal gap or counterexample was found in the sign-splitting, representation construction, cross-prime compatibility, conductor, or final isogeny-height deductions. The modularity step depends on a separate companion theorem not independently audited here. Published Pan modularity at p=5 removes that dependency, assuming the earlier geometric and bounded-field inputs. The initially proposed direct von Kanel–Kret height shortcut was withdrawn after the counterexample recorded below.

## Exact claims and adversarial checks

1. Controlled splitting (766–779): chi has order m <= CM, ramification only T; beta:G_Q -> mu_(2m) satisfies beta^2=chi and delta(beta)=epsilon, is inertia-trivial outside T, and restricts to a conjugacy-invariant character on G_L. Local chi conductors are bounded at fixed primes, tame at odd primes.

The mechanism at 710–750 is sound: B-linear conjugacy quasi-isogenies have rational-scalar discrepancies, and surface degree c^4 allows positive fourth-root normalization to retain only sign(c). At 782–813, the local square-root obstruction is detected by chi(-1); odd characters modulo each offending odd prime and modulo 4 at 2 realize the required Brauer invariants. Brauer reciprocity supplies the real invariant. At 824–833 the inflated cocycle is exactly 1 whenever either input is in G_L, proving character and conjugacy invariance. At 835–849 one quadratic twist cancels the finitely many unwanted odd-prime inertia signs. This uses 2 in fixed S, stated at 846. Neither splitting nor cancellation requires bounded degrees for the mu_g.

2. Two-dimensional representations (862–899): R_ell(g)=beta(g)a_g mu_g g is a genuine representation commuting with B, hence R_ell=r_ell+r_ell after coefficient extension. The two sign discrepancies cancel. The field L' cut out by beta restricted to G_L is Galois with degree <= CM, and R_ell restricted to G_L' is V_ell(A).

Faltings semisimplicity and End theorem give absolute irreducibility of r_ell (915–923). Finite-extension descent of de Rham representations and the two-copy decomposition give cyclotomic exponents 0,1 (925–937). Complex conjugation exchanges nonzero Hodge subspaces, so is nonscalar and has eigenvalues 1,-1 on r_ell (939–947). Conditional on modularity, the exponents force weight two with Tate shift zero (956–978).

3. Modularity dependency (902–907): the invoked theorem covers all continuous irreducible odd regular-de-Rham finitely ramified two-dimensional 2-adic representations, without a residual-image hypothesis. The bibliography at references/references.bib:32–39 identifies the repository's own companion, Fontaine-Mazur-modularity-at-the-prime-2-September-23-2026. Its build/sections/introduction.tex:20–30 matches the quoted statement exactly. A separate audit is needed to certify its proof. The companion's introduction:40–44 refers back to H10 motivationally; no circular proof dependency is established by that reference alone.

4. Compatibility (986–989): r_3 is the 3-adic representation of the same algebraic conjugate of f as r_2. At 992–1038, red(mu_g) composed with relative Frobenius is a rational endomorphism of the good special fiber. Its Tate characteristic polynomial is rational and coefficient-prime independent. The same algebraic beta(g)a_g then gives a common r_2/r_3 trace alpha_q. Injectivity of the selected algebraic embedding, Chebotarev, and semisimplicity identify r_3. No coefficient-field-degree bound is needed.

5. Level bound (1043–1048): N <= CM^a; 1139–1143 allow a=2. At large q (1062–1072), wild inertia fixes L because q exceeds its degree. Good reduction kills its Tate action. Beta has tame square there and its wild restriction is sign-valued, hence trivial for odd q. A tame two-dimensional representation has conductor exponent at most 2.

At each fixed small q (1075–1137), bounded local degree gives finitely many local extensions. The square of beta restricted to G_F has bounded unit conductor. Deep principal-unit logarithms show beta is trivial sufficiently deep: squaring is surjective for odd q, and shifts the filtration by v_F(2) at q=2. Adjoining A[p_0], p_0>=3 and p_0!=q, has bounded degree and makes inertia unipotent. A compact unipotent ell-adic group has no nontrivial pro-q subgroup when q!=ell. Finite local-field choices and Herbrand subgroup/quotient rules give a uniform high-inertia cutoff over Q_q. Swan plus the dimension-two inertia contribution is bounded. This correctly uses L of bounded degree, not L' of degree O(M).

6. Modular factor (1170–1175): J_1(N) ~_(L') A x D_0. The extended-coefficient Hom descends because finitely many linear commutation equations determine its invariant subspace (1178–1192). Faltings supplies an actual nonzero Hom A -> J. Absolute simplicity makes its kernel finite (1194–1202). One shared constituent is sufficient; rational descent enforces any necessary multiplicity.

7. Height conclusion (1232–1295): Zarhin's trick provides a principally polarized complement over L'. The isogeny bound is applied to J^8, whose height is known, and taking logarithms preserves polynomial dependence on M. A dimension-proportional lower bound for the complement yields h_F(A) <= CM^C. No normalization defect affecting this polynomial conclusion was found, although individual normalization identities were not separately checked bibliographically.

## Published modularity replacement at 5

Pan, The Fontaine-Mazur conjecture in the residually reducible case, JAMS 35 (2022), 1031–1169, DOI https://doi.org/10.1090/jams/991; author version https://arxiv.org/pdf/1901.07166v2, Theorem 1.0.4, printed p.5.

Exact input: a continuous irreducible odd representation of G_Q, finitely ramified, potentially semistable at p, with distinct Hodge–Tate weights. For p>=5 there is no residual-image condition. The exceptional local residual condition in the theorem only applies at 3.

Apply this published theorem to r_5, constructed by the formula of source 862–899. The cochains beta,a_g and B-linear mu_g are prime independent. B splits over Qbar_5 regardless of its discriminant. Irreducibility, regularity, and oddness follow exactly as at 915–947. Potential semistability follows because after finite L' its restriction is a Tate constituent of A, which acquires semistable reduction over a further finite local extension. Weights 0,1 imply a weight-two eigenform and Tate shift zero by 956–978.

Repeat 992–1038 for r_5/r_2 to identify both with the same algebraic conjugate of this newform. Use r_5 to calculate conductors away from 5 and r_2 at 5, so coefficient prime differs from residue prime. The conductor arguments at 1062–1137 apply unchanged. Use the 5-adic Hom at 1178–1202; the modular-factor and final-height arguments remain unchanged.

This removes the target's new 2-adic modularity companion from the non-CM arithmetic route. It still requires upstream geometry, bounded Hom-field construction, and base-height comparison.

## Direct von Kanel–Kret shortcut: withdrawn

This supersedes the initial positive shortcut claim in the historical checkpoint. Proposition 7.13's numerical inequality is not falsified, but its fixed-field descent proof has the counterexample below. Use the direct Pan-at-5 route above, not this shortcut.

Primary source: https://arxiv.org/pdf/2307.06944, v1 dated 13 July 2023. Proposition 7.13 printed p.66 states h_F(A)<=(4gd)^(144gd)rad(D_K N_U)^24, where d=[K:Q] and N_U is the product of excluded residue norms. Its assumptions are non-CM, GL2 type with compatible G_Q-isogenies, and condition (*).

Definitions (§7.1.1–2, printed pp.52–53): GL2 type means a degree-g field F inside End^0(A), g=dim(A). Compatibility means mu_sigma:sigma A_Qbar -> A_Qbar obeys mu_sigma sigma(f)=f mu_sigma for f in F. Condition (*) means K/Q normal and all geometric endomorphisms and selected mu_sigma are K-defined.

The formal hypothesis checks in the target are valid: set K=L, g=2; bounded degree and prescribed ramification at 584–615; good reduction outside fixed S at 615; End^0(A)=B division at 682–687; maximal quadratic subfield F and B-linear L-defined mu at 710–720. B-linearity is necessary to obtain compatible conjugacy isogenies; mere isogeny of conjugates does not imply that condition. No CM follows because maximal commutative subfields of B have degree 2 below 2g=4. These inputs give rad(D_L N_U)<=C_S M.

However, Proposition 7.13 uses Proposition 7.2 / Lemma 7.4 to obtain a simple GL2 variety over Q with A as a factor over the fixed K. Lemma 7.4's proof (printed p.55, PDF text lines 2317–2321) specifically asserts Res_(K/Q)B has a simple GL2 factor. Both that claim and the fixed-K factor conclusion fail in the example below.

### Independently checked explicit counterexample

K=Q(i,sqrt(2)), a=1+sqrt(2), E_0/Q:y^2=x^3-x+1, and

B/K: y^2=x^3-a^2 x+a^3.

The rational j-invariant j(E_0)=-6912/23 is nonintegral, hence E_0 and its twist B are non-CM. Let sigma flip sqrt(2) and fix i, and tau flip i and fix sqrt(2). Since a sigma(a)=-1, t=ia satisfies t^2=a/sigma(a). Define

mu_sigma:sigma B -> B, (x,y) |-> (t^2 x,t^3 y), mu_tau=id.

All geometric endomorphisms are Z and all conjugacy isomorphisms are K-defined. Thus GL2 type with compatible G_Q-isogenies and (*) hold. Since t sigma(t)=1 and tau(t)=-t,

mu_sigma sigma(mu_sigma)=id,
mu_tau tau(mu_tau)=id,
mu_tau tau(mu_sigma)=-mu_sigma sigma(mu_tau).

Therefore End^0_Q(R), R=Res_(K/Q) B, is the twisted group algebra Q_c[V4] with u^2=v^2=1 and uv=-vu. It is M_2(Q), represented by u=diag(1,-1) and v=((0,1),(1,0)). Its dimension four equals the four one-dimensional rational Hom spaces among these non-CM conjugates. Semisimplicity gives R~_Q C^2, where C is a Q-simple surface with End^0_Q(C)=Q. Consequently R has no simple GL2-type factor.

A different Q-simple GL2 variety C_0 cannot save the fixed-K statement: if B were a K-isogeny factor of (C_0)_K, then Hom_K((C_0)_K,B) is nonzero. Weil-restriction adjunction gives Hom_Q(C_0,R) nonzero, so C_0 must be isogenous to C. But dim(C)=2 and End^0_Q(C)=Q exclude GL2 type. This refutes the fixed-K conclusions of Proposition 7.2 and Lemma 7.4, not only their selected construction.

The exhibited B has the same stable Faltings height as E_0, so this does not refute Proposition 7.13's numerical height bound. Nor does it refute a weaker geometric factor theorem after enlarging the field of definition of the factor. Wu's geometric existence theorem does not imply that a splitting cochain factors through Gal(K/Q); that is the missing finite-field step.

### Publication and proof-scope check

No corrected published version of arXiv:2307.06944 was located. The currently available file is v1. Author pages https://rafaelvonkanel.github.io/research/ and https://staff.fnwi.uva.nl/a.l.kret/ still label it submitted/preprint. The former expressly says the relevant 2013 preprint §9.4 was excluded from the 2021 publication and moved to the 2023 preprint. Thus 2013 Proposition 9.9 is not independent published support.

Published von Kanel, The effective Shafarevich conjecture for abelian varieties of GL2-type, Forum Math. Sigma 9 (2021), e39, DOI https://doi.org/10.1017/fms.2021.29, Theorem A, gives (3g)^(144g)N_S^24 over open subschemes of Spec(Z), for product GL2 type. Its proof uses established modularity over Q through Ribet/Serre/Faltings. That is the theorem invoked by Proposition 7.13's reduction. Its published scope does not itself cure the false fixed-K reduction.

## Final checkpoint

2026-10-06 22:25 PDT (2026-10-07 05:25 UTC).
Assigned-audit completion estimate: 100%; upstream theorem certification remains partial.

Strongest verified scope: no concrete defect found in the target non-CM sign/conductor/height deductions, and published Pan modularity at 5 supplies a replacement for the new companion at 2 under the same preceding geometric inputs. The direct von Kanel–Kret shortcut is blocked by the explicit fixed-field counterexample to its reduction. No numerical height inequality or H10 theorem is certified or falsified by that counterexample. No source edits, Git mutations, or external outreach occurred.

Storage briefly prevented saving the correction; the old note was explicitly superseded in internal messages. This file now contains that correction.
