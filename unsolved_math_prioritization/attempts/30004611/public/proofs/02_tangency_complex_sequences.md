# All-rank tangency-complex deletion–restriction constructions

14 October 2026 UTC. Row 1775 / 30004611, shared substantive pass 2. Authored mathematical development, unrefereed. This continues the specified pass-1 common-poset construction. It does not claim that failure of its canonical maps refutes Mücksch's broader Problem 6.3, and does not claim that a sequence of derived replacements is already the short exact sequence of the three original sheaves requested there.

## Result in brief

There are characteristic-free, functorial **short exact sequences of explicit two-term tangency complexes** on the original punctured lattice. Their degree-zero cohomology sheaves are the actual original, deletion, ordinary restriction, and Ziegler restriction derivation sheaves, with precisely specified transports and the geometric ideal twist from pass 1. They produce unconditional six-term exact sequences of sheaves. The correction terms have finite presentations by hyperplane equations and derivative matrices; they are not definitions that merely rename a restriction image or an arbitrary chosen resolution.

For ordinary restriction the sequence is

0 → I⊗F → D_A → i_*D_B → I⊗T' → T_A → i_*T_rep → 0.       (O6)

Here T' and T_A are independently defined simultaneous-tangency obstruction sheaves of the deletion and original arrangement. T_rep is the obstruction of the ordinary restriction with one row for each original hyperplane. Repeated ordinary rows are not Ziegler powers.

For Ziegler restriction the sequence is

0 → I⊗E → E → i_*Z → I⊗U → U → i_*T_Z → 0.                (Z6)

Here U has an explicit product-per-restriction-fiber presentation. At every X contained in H, the Ziegler restriction defect is canonically Tor_1^S(U_X,R), including its natural grading. This gives a separate, concrete all-rank correction, rather than incorrectly substituting the ordinary Ext description or Euler multiplicity.

Both short exact complex sequences give genuine long exact **hypercohomology** sequences, and two-row spectral sequences with the actual named lattice-sheaf cohomology on the E2 page. Their extension data must be retained; neither the normal-evaluation sequence nor these complexes are asserted globally split. A six-term exact sequence of sheaves must not be converted into a long exact sequence of their cohomology by simply concatenating its terms.

## 1. Conventions and comparison spaces

Let K be any field, A a finite central essential simple arrangement in V, dim V=ell>=2, and H a marked hyperplane with nonzero equation alpha. Set S=Sym(V*), R=S/(alpha), A'=A minus {H}, B=A^H, and m=m^H. Derivation degree means coefficient degree.

Let P be the nonzero flats of A, ordered by geometric inclusion, with upper Alexandrov topology. All sheaves below are covariant functors on P. Put Q={X in P:X contained in H}; its inclusion i:Q→P is closed, and i_* is exact extension by zero. Q is canonically the nonzero-flat lattice of B. For X in P set A_X={L in A:X contained in L}, and A'_X=A_X minus {H} when H contains X, or simply A_X otherwise.

Write D_X=D(A_X), F_X=D(A'_X), and E_X={theta in D(A_X):theta(alpha)=0}. Write D_B and Z=D(B,m) for the corresponding ordinary and multiarrangement lattice functors on Q. These have coefficient ring R; i_* views them as S-module sheaves.

The ideal sheaf I has I_X=alpha S on Q and I_X=S off Q, with inclusion structure maps. It is stalkwise flat but generally not an invertible sheaf or a global grading shift. All products I⊗(-) below use this sheaf, including its nonunit transition maps.

For deletion, let P'_geom=L(A') minus the literal zero subspace, when that subspace occurs. It retains a nonzero center. The closure c(X)=intersection{L in A':X contained in L} has A'_{c(X)}=A'_X, and F is the exact direct-image transport of the extended deletion functor along P'_geom→P. The same transport applies to the deletion tangency complex and T'. Thus their cohomology before the I twist is their cohomology on P'_geom. Section 8 separately recovers the source convention that deletes the center when A' is nonessential; the two conventions are not equated.

Choose one defining equation alpha_L for each L. Rescaling an equation rescales the associated target row by a unit, giving naturally isomorphic complexes. The construction can equivalently use the one-dimensional normal spaces V/L to avoid choosing those scalar identifications.

## 2. The independently defined tangency complexes

For any localized arrangement A_X define

K(A)_X = direct_sum over L in A_X of S/(alpha_L),

Phi(A)_X : Der_K(S) → K(A)_X,
            theta ↦ (theta(alpha_L) mod alpha_L)_L.

For X contained in Y the structure map of K(A) is projection, dropping the summands for hyperplanes absent from A_Y. The source Der_K(S) is constant. Hence Phi(A) is a sheaf map.

Define the two-term complex

C(A)=[Der_K(S) --Phi(A)→ K(A)]

in cohomological degrees 0 and 1, and define its independently presented tangency obstruction

T_A=coker(Phi(A)).

Then H^0(C(A))=D_A and H^1(C(A))=T_A, with no other cohomology sheaves. This is not a resolution claimed to be exact in degree 1. It is the universal complex of simultaneous first-order tangency conditions, specified before considering any restriction map.

Likewise put K'=K(A'), C'=[Der_K(S)→K'], and T'=coker(Der_K(S)→K'), evaluated at A'_X on P. Its degree-zero cohomology is the actual transported deletion F. A presentation matrix for T' consists of the constant normal vectors d alpha_L together with the diagonal relations alpha_L. In particular it is computable directly from the arrangement equations, independently of the ordinary restriction cokernel.

Define N=ker[Der_K(S)_P→i_*R_Q], where the map is theta↦theta(alpha) mod alpha on Q and zero outside. Thus N_X consists of derivations tangent to H on Q and is all Der_K(S) off Q. The map is pointwise surjective. Restricting the deletion tangency conditions to N gives

C_H(A)=[N→K'].

There is a canonical inclusion of complexes C_H(A)→C(A): degree zero is N→Der_K(S), and degree one inserts the zero H-component. Its quotient is the contractible complex [i_*R --id→ i_*R]. Therefore C_H(A)→C(A) is a natural quasi-isomorphism, identifying H^0 with D_A and H^1 with T_A. This is a quasi-isomorphism, not a global splitting assertion.

## 3. An ordinary short exact sequence of complexes

For X in Q let r_X:A'_X→B_X send L to L intersect H, retaining one index for each L even when several restrictions coincide. Define on Q

K_rep,X = direct_sum over L in A'_X of R/(alpha_L restricted to H),

C_rep=[Der_K(R)→K_rep],

where the map is derivative of the restricted equation. Structure maps again drop absent original hyperplanes. Its H^0 is exactly D_B: repeating an ordinary divisibility condition does not change its kernel. Write T_rep=H^1(C_rep).

There is a natural short exact sequence of complexes on P:

0 → I⊗C' → C_H(A) → i_*C_rep → 0.                         (OC)

Proof in degree zero: multiplication maps I⊗Der_K(S) injectively into N. On Q its image is alpha Der_K(S); restriction modulo alpha identifies N/alpha Der_K(S) with Der_K(R). Off Q the map is the identity and the quotient is zero.

Proof in degree one: multiplication maps I⊗K' injectively into K'. On Q, alpha is a nonzerodivisor on each S/(alpha_L), since L is different from H. The quotient summand is S/(alpha,alpha_L), equal to R/(alpha_L restricted to H). Off Q the map is the identity. These maps commute with every projection structure map and the cross-boundary maps of I.

The induced quotient differential is the derivative map for the restricted equations: a derivation in N has zero normal component modulo alpha. This proves (OC), including compatibility of its differential. It requires neither freeness nor a characteristic restriction.

Taking cohomology sheaves of (OC), and using C_H(A) quasi-isomorphic to C(A), proves the unconditional exact sequence (O6). Its first three maps are exactly the pass-1 multiplication and ordinary restriction maps. Its fourth map is the snake connecting map. Its fifth map has the explicit representative description

[a_L]_L in I⊗T'_X  ↦  [(0, alpha a_L)_L] in T_A,X

on Q after the usual local identification I_X⊗T'_X=T'_X(-1); off Q it is the identity. The zero is the H-row. Thus the ordinary restriction defect is canonically

C_ord = ker[I⊗T'→T_A].                                    (Odef)

This describes the same defect through a new explicit matrix construction, rather than taking its definition to be coker(D_A→i_*D_B). It is compatible with the pointwise Ext characterization established in pass 1, but no equality of pointwise Ext with functor-category Ext or lattice cohomology is used.

### Repeated ordinary rows versus multiplicity powers

After choosing a common equation beta_K for each K in B and normalizing its original equations to restrict to beta_K, there is a canonical diagonal inclusion

K(B) → K_rep,

one copy of R/(beta_K) into all m(K) copies in its fiber. It gives an exact sequence

0 → T_B → T_rep → W → 0,

where W is the direct sum over K of the diagonal quotient

(R/(beta_K))^{m(K)} / diagonal(R/(beta_K)).

This quotient is defined without dividing by m(K). Choosing a representative in each fiber gives a splitting, but no such noncanonical splitting is used. The formula is valid when the characteristic divides m(K). Crucially, neither K_rep nor T_rep uses R/(beta_K^{m(K)}). Those are the different Ziegler construction below.

## 4. The grouped normal-fixed complex

Let W_S={theta in Der_K(S):theta(alpha)=0}, a constant free S-module sheaf of rank ell-1. For each K in the global ordinary restriction B choose an equation beta_K in H*, and extend beta_K to V*. Normalize the equations of all original L lying over K as

l_L=beta_K+c_L alpha.

Such a normalization exists because the restrictions of alpha_L and beta_K to H are proportional. Changing the extension of beta_K only changes the constants c_L. The map theta↦theta(beta_K) on W_S is independent of that change.

For every X in P set

q_K,X = product over L in A'_X with L intersect H=K of l_L,

with empty product 1, and set

G_X = direct_sum over K in B of S/(q_K,X).

Zero summands S/(1) may be omitted. If X is contained in Y, then q_K,Y divides q_K,X, giving the natural quotient projection G_X→G_Y. Define

Psi_X:W_S→G_X,   theta↦(theta(beta_K) mod q_K,X)_K,

and let C_E=[W_S --Psi→G] in degrees 0,1, U=coker(Psi).

Because theta(alpha)=0, tangency to all distinct l_L in a fixed fiber is exactly divisibility of theta(beta_K) by their product. Distinct linear equations are pairwise coprime in S, over every field. It follows that

H^0(C_E)=E,   H^1(C_E)=U.

This identity holds on all P, not just Q. It does not use an expression theta(alpha)/alpha outside H. The presentation of U uses only the constant derivative rows d beta_K restricted to W_S and the diagonal relations q_K,X. It is therefore an independently specified grouped-tangency obstruction module.

At X in Q, either every original hyperplane in a global restriction fiber contains X or none does: X contained in L is equivalent to X contained in L intersect H. Consequently

q_K,X mod alpha = beta_K^{m(K)}

for K in B_X, with precisely the localized global Ziegler multiplicity. No partial multiplicity is introduced there. Outside Q partial fibers pose no problem for the definition of G or its structure maps.

## 5. The Ziegler short exact complex sequence and Tor correction

On Q define the genuine multiarrangement tangency complex

C_Z=[Der_K(R)→ direct_sum over K in B_X of R/(beta_K^{m(K)})],

and write T_Z=H^1(C_Z). Its H^0 is exactly the named Ziegler lattice sheaf Z.

There is a natural short exact sequence of complexes on P:

0 → I⊗C_E → C_E → i_*C_Z → 0.                            (ZC)

In degree zero, restriction identifies W_S/alpha W_S with Der_K(R). In degree one, alpha is a nonzerodivisor on every S/(q_K,X): each q_K,X is a product of equations of hyperplanes different from H. The quotient on Q is R/(beta_K^{m(K)}), by the full-fiber observation above. Off Q multiplication by I_X=S is the identity. Differentials and all structure maps commute. This proves (ZC), and its cohomology-sheaf sequence is exactly (Z6).

At X in Q, identify I_X⊗U_X with U_X(-1). The connecting map identifies the Ziegler restriction defect canonically with

ker[alpha:U_X(-1)→U_X] = Tor_1^S(U_X,R).                 (Zdef)

This equality uses the canonical length-one graded free resolution S(-1) --alpha→ S of R. It is ordinary module Tor at each stalk, naturally transported under the quotient maps in G. It is not internal sheaf Tor unless separately defined and identified. Moreover U_X/alpha U_X is canonically T_Z,X by right exactness of tensoring this presentation.

Equivalently, at each X in Q there is a canonical derived specialization

C_E,X tensor^L_S R  quasi-isomorphic to C_Z,X.

Indeed the two-term free resolution of R computes the left side as the cone of alpha on C_E,X; alpha is termwise injective, so its cone is quasi-isomorphic to the quotient complex. The latter has the actual Ziegler target as its H^0. This derived identification retains the Tor obstruction and does not falsely replace Z by E/alpha E.

The normal-evaluation exact sequence 0→E→D_A→I→0 from pass 1 still connects E to D_A. It is not asserted to split as a lattice sheaf. The pass-1 counterexample to global splitting is compatible with this construction.

### Concrete check on the credited four-plane factor

For the already credited arrangement with equation xyz(x+y+z), marked H={z=0}, take S=K[x,y,z]. The grouped complex has

G=S/(x) direct_sum S/(y) direct_sum S/(x+y+z),

and the two columns of Psi are (1,0,1) and (0,1,1). In its cokernel, e_1=-e_3 and e_2=-e_3, and the three diagonal relations then give x e_3=y e_3=z e_3=0. Consequently

U is canonically isomorphic to S/(x,y,z), after choosing the indicated generator.

The Tor formula proves that the **entire** Ziegler cokernel is K(-1), over every field. It is more than a single nonlifting witness. Adjoining a free variable w gives the bad nonzero-flat stalk K[w](-1). The ordinary deletion consists of the three independent forms x,y,x+y+z, so its tangency matrix is surjective and T'=0; (O6) gives ordinary surjectivity. This is a verification and refinement of the credited example already used in pass 1, not a newly discovered counterexample.

## 6. Actual lattice cohomology and the retained extension data

The finite Alexandrov category has enough injectives. Apply derived global sections to (OC) and (ZC). Their genuine long exact sequences include

... → hyperH^n(P,I⊗C') → hyperH^n(P,C(A))
    → hyperH^n(Q,C_rep) → hyperH^{n+1}(P,I⊗C') → ... ,

and

... → hyperH^n(P,I⊗C_E) → hyperH^n(P,C_E)
    → hyperH^n(Q,C_Z) → hyperH^{n+1}(P,I⊗C_E) → ... .

Exactness of i_* identifies the Q terms as written. The first uses the natural quasi-isomorphism C_H(A)→C(A). Neither sequence changes the original finite poset P to an unspecified scheme or identifies sheaf cohomology with pointwise Ext/Tor.

For every one of these two-term complexes C there is a functorial spectral sequence

E2^{p,q}=H^p(P,H^q(C))  =>  hyperH^{p+q}(P,C),  q=0,1,

using Q for the restriction terms. Its q=0 rows are exactly the named derivation lattice-sheaf cohomology:

- H^p(P,D_A);
- H^p(P,I⊗F), with F the explicit deletion transport;
- H^p(Q,D_B);
- H^p(P,E), H^p(P,I⊗E), and H^p(Q,Z).

The q=1 rows are, respectively, T_A, I⊗T', T_rep, U, I⊗U, and T_Z. The possibly nonzero d2:H^p(H^1(C))→H^{p+2}(H^0(C)) records extension data; discarding it or globally splitting the two rows is not allowed.

For an entirely finite computational model, a sheaf M on P has the standard cochain resolution

C^p(P,M)=product over strict chains X_0<...<X_p of M_{X_p}.

Its differential is alternating omission of vertices, with the final face using the structure map M_{X_{p-1}}→M_{X_p}. For example d(s)_{X<Y}=s_Y-M(X≤Y)s_X. Applying this to the two degrees of any displayed tangency complex and totalizing computes its hypercohomology. Thus (OC) and (ZC) induce explicit short exact sequences of finite total cochain complexes: products are finite and exact. This is an effective coefficient-and-incidence construction, not just an existence assertion about an arbitrary resolution.

There is also the pass-1 exact sequence

0→I⊗F→F→i_*(R⊗_S i^*F)→0,

whose middle cohomology is the extended deletion's actual cohomology. It connects the ideal-twisted deletion row to that deletion cohomology without dropping I or relabeling deletion reduction as D_B.

### 6a. Termwise acyclicity and explicit dimension shifting

In fact every term of every displayed two-term complex is acyclic for lattice global sections. Here is the proof, which is specific to these coefficient complexes and is stronger than invoking an arbitrary injective resolution.

- A constant sheaf on P or Q is acyclic because each poset has a maximum. The sequence 0→I→S_P→i_*R_Q→0 and surjectivity S→R show that I is acyclic. Similarly 0→N→Der(S)_P→i_*R_Q→0 has surjective global evaluation, so N is acyclic.
- The L-summand of K(A) or K' is exact closed extension of the constant module S/(alpha_L) from {0≠X in P:X contained in L}, which has maximum L. It is acyclic. The same argument applies to every ordinary repeated or Ziegler-power summand on Q, supported on {0≠X contained in K}, with maximum K whenever K is nonzero; when K=0 the support is empty.
- For I⊗K', use 0→I⊗K'→K'→i_*K_rep→0. If ell>=3, each L intersect H is nonzero, and the map on global sections is the surjection S/(alpha_L)→S/(alpha,alpha_L) in each row. If ell=2 the right-hand sheaf is zero and I⊗K'=K'. Thus I⊗K' is acyclic.
- For a fixed global restriction fiber K, its summand G_K is the exact direct-image transport from the arrangement of the hyperplanes lying in that fiber: its value at a flat is S divided by the product of the fiber equations containing that flat. The closure map supplies the least larger fiber-arrangement flat, exactly as for deletion. If ell>=3 this rank-at-most-two fiber arrangement has a nonzero center (K for a fiber with at least two members, or its single hyperplane), so its geometric nonzero-flat poset has a minimum and every sheaf on it is acyclic. If ell=2 and the fiber has at least two members, its punctured poset consists of its individual lines and V; the sheaf has values S/(l_L) on those lines and zero at V. Its cochain complex has no positive-degree terms. Thus G is acyclic in every dimension under consideration.
- Finally 0→I⊗G→G→i_*G_Z→0 proves acyclicity of I⊗G. For ell>=3 its global map is the direct sum of surjections S/(q_K)→R/(beta_K^{m(K)}). For ell=2 the right-hand sheaf is zero. The degree-zero terms W_S and I⊗W_S are finite free sums of the already treated constant sheaf and I.

It follows that hyperH^n(P,C) is the cohomology of the literal two-term global-section complex Γ(P,C), so vanishes for n>=2. For C(A), its degree-one group is the ordinary whole-arrangement matrix cokernel

T(A)=coker[Der(S)→direct_sum_{L in A} S/(alpha_L)].

The two-row spectral sequence therefore gives a natural exact sequence

0→H^1(P,D_A)→T(A)→H^0(P,T_A)→H^2(P,D_A)→0,

and natural isomorphisms

H^p(P,T_A) ≅ H^{p+2}(P,D_A),  p>=1.

More generally, for any displayed complex C with H^0(C)=M and H^1(C)=T, the same statement holds with hyperH^1(P,C)=coker[Γ(C^0)→Γ(C^1)] replacing T(A). In particular it applies to I⊗C', the actual ordinary restriction complex, C_E, I⊗C_E, and the actual Ziegler complex. For ell>=3 their global complexes are the corresponding whole-arrangement coefficient presentations, with the indicated alpha shifts on I-twisted terms. In ell=2 one must retain the literal global-section complexes: a rank-one restriction has lost its center, so replacing that complex by the whole-arrangement module presentation would be wrong.

This dimension shifting exhibits actual lattice-sheaf cohomology in the explicit tangency obstruction sheaves. It does not assert that the map T(A)→H^0(P,T_A) is an isomorphism, and it does not discard the d2 extension information.

The normal-evaluation sequence yields one additional simplification: H^k(P,E)→H^k(P,D_A) is a canonical isomorphism for every k>=1. Indeed I is acyclic as proved above, Γ(I)=alpha S, and the Euler derivation makes Γ(D_A)→alpha S surjective. This cohomological statement does not require or imply a global sheaf splitting of normal evaluation.

## 7. Where the corrections can live, and a genuine high-degree tail

Both ordinary and Ziegler restriction defects vanish at every X in Q with codim_V X<=2, by the characteristic-free explicit lifting calculation of pass 1. Hence each defect is supported on the closed subposet

Q_bad={X in Q:codim_V X>=3}.

For ell>=4 this poset has chains of length at most ell-4, since 1<=dim X<=ell-3. Extension by zero from this lower ideal is exact. The finite chain resolution therefore proves

H^p(P,C_def)=0 for p>ell-4.

When ell<=3 the defect itself is zero. No depth hypothesis is needed for this positional bound. In rank four the correction has only degree-zero lattice cohomology, although its modules can be nonzero and infinite-dimensional over K.

For ell>=4 set K_o=I⊗F, or K_z=I⊗E; set M_o=im(D_A→i_*D_B), or M_z=im(E→i_*Z). Using these images only for this proof, the two genuine short exact sequences 0→K→D_source→M→0 and 0→M→i_*D_target→C_def→0 give canonical isomorphisms

H^n(P,M)=H^n(Q,D_target) for n>=ell-2.

Substitution into the first long exact sequence gives the actual, uncorrected high-degree tail, beginning at the indicated place:

H^{ell-2}(P,K) → H^{ell-2}(P,D_source)
 → H^{ell-2}(Q,D_target) → H^{ell-1}(P,K)
 → H^{ell-1}(P,D_source) → H^{ell-1}(Q,D_target) → ... .

This tail is exact from the second displayed term onward. It must not be extended to lower degrees without the correction data. In rank<=3 the full ordinary/Ziegler long exact sequences are available from pass 1. In rank>=4 the correction affects the lower-degree range that contains many of the interesting freeness obstructions, so this tail alone is not a full addition–deletion theorem.

## 8. Nonessential deletion: recovering the actual center-deleted source

Because A is essential and only one hyperplane is deleted, nonessential A' has a one-dimensional center T', with V=H direct_sum T'. The marked equation alpha is nonzero on T'. Restriction along this product identifies A' with the pullback of B=A^H, and all Ziegler multiplicities are one.

The source-style poset is P'_src=L(A') minus {T'}, whereas the exact transport above uses P'_geom, which retains T'. The latter has a minimum, so its positive-degree sheaf cohomology is zero. This is not the source deletion cohomology.

There is an order isomorphism

Q → P'_src,    X ↦ X direct_sum T'.

Under it, the actual source deletion functor has a natural product decomposition

D'_src ≅ (S tensor_R D_B) direct_sum (S tensor_K T')_constant.

The embedding R→S here is supplied by the projection V→H along T'. A vector v in T' with alpha(v)=1 identifies the second summand with S partial_v. At a stalk, the defining forms of A' are independent of alpha, so the tangency equations affect only the first summand. This proves the decomposition on every stalk and for every structure map.

Because Q has the maximum H, its order complex is contractible, and the constant-sheaf summand has H^0=S tensor_K T' and no positive cohomology. Flatness of S over R, together with the finite chain resolution, now gives

H^k(P'_src,D'_src) ≅ S tensor_R H^k(Q,D_B),  k>0,

and

H^0(P'_src,D'_src) ≅ (S tensor_R H^0(Q,D_B)) direct_sum (S tensor_K T').

These equations explicitly connect the actual source deletion cohomology, rather than replacing it by the acyclic center-retaining extension. They hold also when ell=2 as statements about the defined finite-poset functors; no erroneous identification of H^0 with the full rank-one arrangement derivation module is used.

For ell>=3, the degree-zero source deletion global sections do equal D(A'): each hyperplane of A' is still present in P'_src, so global sections inside Der(S) satisfy every original tangency condition. In ell=2 the unique deletion hyperplane is the deleted center, and that assertion fails exactly as warned in pass 1.

## 9. Scope and remaining obstruction

The present theorem gives an unconditional, all-field, all-rank geometric coefficient construction. It connects the actual named sheaves by six-term exact sheaf sequences, supplies two genuine short exact sequences of canonical two-term complexes, and gives their long exact hypercohomology and spectral sequences on the original poset. The Ziegler correction has a concrete Tor presentation, and ordinary repeated rows have been separated from multiplicity powers. The source convention for nonessential deletion is handled explicitly.

What it does not prove is an unrestricted short exact sequence of only the original derivation sheaf, a natural deletion twist, and the full ordinary or Ziegler restriction sheaf. For the canonical maps, precisely identified kernels in (Odef) and (Zdef) can be nonzero at nonzero flats, as the credited rank-four examples from pass 1 already show. The construction also does not prove that all other comparison spaces or maps must fail. The unresolved source-level question is whether a more economical short exact sheaf construction can bypass these defects while still preserving and identifying the actual named lattice-sheaf cohomology, or whether the source intended and accepts this naturally corrected derived formulation.

It would overclaim to call the original broad Problem 6.3 solved solely because every morphism has a cone. The substantive content here is the explicit hyperplane-congruence complexes, their non-tautological short exact sequences, the ordinary-versus-Ziegler identification, the matrix/Tor correction formula, and the retained cohomological extension data. No novelty or exhaustive literature claim is made.

## Source context

The source and standard definitions were recovered in the existing verified packet. The target is Mücksch, arXiv:2008.13700v3, Problem 6.3: https://arxiv.org/abs/2008.13700v3 . The ordinary pointwise Ext framework credited in pass 1 is Abe–Denham, arXiv:2203.04816v3: https://arxiv.org/abs/2203.04816v3 . The existing rank-four promoted witnesses are credited to the module examples of Abe–Kawanoue, arXiv:2406.00305v2: https://arxiv.org/abs/2406.00305v2 . No new literature search or source novelty certificate is claimed by this pass-2 derivation.
