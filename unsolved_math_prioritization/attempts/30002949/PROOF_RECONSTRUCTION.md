# Coxeter stratification proof audit and reconstruction

## Result and credit

The statement attached to problem 30002949, is Chen–Viehmann Conjecture 4.2. Görtz explicitly credits and states that result as Theorem 0.1 and, for the basic representative relevant here, Theorem 3.4 of arXiv:1802.02225v1. The article was published in Transactions of the AMS 372 (2019), 4675–4699, DOI 10.1090/tran/7715. This is prior-theorem coverage, not a new theorem or novelty claim.

The inspected arXiv proof contains a false auxiliary escape assertion in Lemma 3.10, and a too-narrow case description near the end of §3.6. Neither is a counterexample to the stratification theorem. Below is a complete replacement for the escape argument and a checked version of the needed support argument. It uses only actual rational group elements. The final publisher PDF has not been retrieved, so no claim is made about whether its proof has the same wording or a correction. Read this proof together with [INVARIANT_SUBSET_CORRECTION.md](INVARIANT_SUBSET_CORRECTION.md). The reductive stabilizer argument and every use of Q = I(K,w,σ) are accepted only with that note's corrected general formula: the largest θ-stable subset of the commutant outside P contained in K. The note proves that this is S\(P∪Σ) for all thirteen classified rows, including empty support. This explicit dependency replaces reliance on the overbroad commutant sentence in the inspected Görtz–He author copy. The proof reconstruction, correction, and separate mathematical audit are AI-assisted; this is not external human peer review or formal proof-assistant certification.

## Exact statement being audited

Let F be a nonarchimedean local field with finite residue field, L the completion of its maximal unramified extension, and σ its Frobenius. Let G be connected reductive. We work in its reduced building, assume that its reduced affine Dynkin diagram S is connected, and take data whose affine Coxeter quadruple is one of the thirteen GH quadruples listed below. These are the quadruples underlying the nineteen cases in GH's displayed classification. The original GH hypotheses include tame splitting and minuscule cocharacter data. We retain these hypotheses rather than enlarge the classification on the strength of a title.

Fix a σ-stable alcove a with Iwahori I. Let K=S\{v} be σ-stable and let P_K be its connected parahoric. Thus one removes one σ-fixed vertex; merely removing a larger σ-orbit is outside the asserted range. Let μ be the datum of Coxeter type. Choose a lift τ of the unique length-zero element with t^μ in W_a τ. Set θ=Int(τ)σ and J=G(L)^θ. This is the basic representative. On the reduced apartment θ has finite order and preserves a, even when a reductive center makes τ infinite-order in the extended Weyl group.

For gP_K define f_g(j)=P_K j^{-1}gP_K, for j in J. Equivalently this takes values in W_K\W̃/W_K. Two points belong to the same J-piece exactly when these functions agree. In the original hyperspecial minuscule setting this is Chen–Viehmann's dominant-coweight function.

For an EO Coxeter element w, write P=supp_σ(w), so wτ^{-1} is a twisted Coxeter element in the finite W_P. Let Y(w) be the image in G(L)/P_K of its classical Deligne–Lusztig variety in P_P/I. This projection is an isomorphism on Y(w). Put Σ_w equal to the vertices adjacent to P but outside P; for P empty put Σ_w equal to the θ-orbit of v. The pieces to compare are precisely

    iY(w),  w in EO^K_{σ,cox},  i in J/(J∩P_{S\Σ_w}).

These are the refined Bruhat–Tits pieces, not entire EO unions π(X_w(τ)). The conclusion is equality of the two partitions on X(μ,τ)_K. In the original hyperspecial minuscule case X(μ,τ)_K=X_μ(τ). Equality with the BT partition also transfers its known closure-stratification properties; the proof below does not independently reprove the GH closure theorem.

A different arbitrary σ-conjugate representative cannot silently be substituted for τ: Chen–Viehmann Remark 2.1 explains that the J-partition can change. Lifts of the same τ are T(L)_1-σ-conjugate by Lang's theorem, and the resulting K-transport preserves both partitions (Görtz Lemma 3.3).

## A concrete failure of the literal escape lemma

Use Görtz Example 1.3, which is also the n=4 instance of Example 3.1: the quasi-split unitary affine diagram Ã3, with σ=(13), τ=(0123), and θ=(01)(23). This has positive rational reduced rank one and connected affine diagram.

Use simple-root coordinates x_i=α_i(x) in the standard A3 apartment. The base alcove has vertices

    p_0=(0,0,0), p_1=(1,0,0), p_2=(0,1,0), p_3=(0,0,1).

The vertex permutation gives the affine map

    θ(x_1,x_2,x_3)=(1−x_1−x_2−x_3, x_3, x_2).

Consequently its fixed apartment E is

    x_2=x_3,  x_1+x_2=1/2.

The alcove barycenter is b=(1/4,1/4,1/4); the rational endpoint chosen in the source proof is b'=(1/2,0,0). For the genuine finite root β=α_1+α_2,

    β(b)=β(b')=1/2,  β(b−b')=0.

Indeed β is identically 1/2 on all of E. Every rational alcove barycenter belongs to E and remains at distance 1/(2||β||) from the wall β=0. This contradicts the claimed ability to get arbitrarily far from every ambient finite-root wall. Since p_0 is hyperspecial and β(p_0)=0, this is also a K-wall. Replacing “all ambient walls” by “all K-walls” therefore does not fix the lemma.

The invariant direction can even be chosen in the coroot lattice: in these coordinates λ=(−1,1,1)=α_2^∨+α_3^∨. It is fixed by the linear part of θ, but β(λ)=0. The obstruction is geometric, not the absence of rational translations.

This does not contradict Theorem 3.4. The unitary family was already proved by direct lattice arguments in Chen–Viehmann §4.2.2. The proof only needs to distinguish finitely many particular vertex orbits after passing to K-double cosets. It does not need to escape all walls.

## Replacement for Lemmas 3.10 through 3.13

Write A for the reduced ambient apartment, E=A^θ, D for its translation vector space, and H=W_a^θ. Write Q^∨ for the translation lattice of the reduced affine Coxeter group W_a (so any scaling convention is built into this notation). Choose a W_a-invariant Euclidean inner product, also θ-invariant. Let p be the vertex of a of type v, so its stabilizer in W_a is W_K. No assertion that p or K is θ-fixed is needed; in general they are not.

### Lemma A  Projection distinguishes the required right cosets

Orthogonal projection q:A→E is injective on H·p.

Proof. Let m be the order of θ on A. The affine average m^{-1}Σ_{r=0}^{m−1}θ^r(x) is the orthogonal projection q(x). If u∈H, then

    q(up)=u q(p)=m^{-1}Σ_r uθ^r(p).

The distinct vertices θ^r(p) form a subset of the vertices of the simplex a. Their convex hull is a face. The average has positive coefficient on each distinct vertex, so lies in the relative interior of that face. After applying u the same holds in u a. If q(up)=q(u'p), uniqueness of the minimal face of the ambient affine Coxeter complex containing the common point implies that the two faces coincide. The affine Weyl group is type preserving. Each face has at most one vertex of any given ambient vertex type; both up and u'p have type v and belong to that face. Hence up=u'p. Conversely this equality plainly gives equal projections. Finally up=u'p is equivalent to uW_K=u'W_K, because Stab_{W_a}(p)=W_K. ∎

This is a minimal-face argument in the full ambient Coxeter complex, not an assertion that projection is injective on every point of A. In particular it remains valid when D is parallel to some ambient root walls.

### Lemma B  Finite separation by invariant translations

Let (u_i,u'_i) be finitely many pairs in H with u_iW_K≠u'_iW_K. Let C be any nonempty open rational Weyl chamber cone in D. There exists λ in C∩Q^∨ fixed by the linear part of θ such that, for all sufficiently large positive integers N, simultaneously

    W_K t_{−Nλ}u_i W_K ≠ W_K t_{−Nλ}u'_i W_K.

Proof. The linear action of θ preserves Q^∨; hence its fixed lattice has full rank in D. By Lemma A,

    pr_D(u_i p−u'_i p)=q(u_i p)−q(u'_i p)≠0.

For each i the condition ⟨λ,u_i p−u'_i p⟩=0 is therefore a proper linear hyperplane in D. A finite union of such hyperplanes does not contain the open cone C. Rational points are dense and a sufficiently divisible multiple of a rational point is in the fixed lattice. Choose λ avoiding them all.

Equality of the displayed double cosets would give k∈W_K taking t_{−Nλ}u_i p to t_{−Nλ}u'_i p, since right W_K fixes p. As k fixes p and is an isometry it would imply equality of squared distances to p. Their difference is

    −2N⟨λ,u_i p−u'_i p⟩ + ||u_i p−p||² − ||u'_i p−p||².

This is a nonconstant affine function of N. It has at most one zero for each pair. For N larger than all these finitely many possible exceptional values none of the double-coset equalities can hold. ∎

Only a finite set of projected vertex differences is avoided. No avoidance of every ambient root hyperplane, or even every K-wall, occurs in this argument.

### Lemma C  The translations have rational group representatives

Every t_λ above is in H and is represented by an element n_λ of the rational normalizer in J, which can be chosen in the parahoric-generated subgroup J^1. In particular it is represented in the ambient Kottwitz-zero subgroup of G(L).

Proof. Conjugation by θ sends t_λ to t_{dθ(λ)}, so t_λ∈W_a^θ. Apply Richarz, “On the Iwahori-Weyl group”, §1.2, to the F-group J, identified with G over L. His Lemma 1.6 identifies the rational Iwahori-Weyl group with the fixed subgroup of the unramified one; its proof explicitly identifies the affine subgroups. In terms of normalizers it uses vanishing of H¹ for the connected torus parahoric, not surjectivity J(F)→J_ad(F). Thus t_λ has a rational normalizer lift in J^1. Richarz §1.1 defines J^1 as generated by rational parahorics, gives its affine BN-pair, and identifies it with the rational Kottwitz kernel. Each such parahoric embeds in an ambient parahoric, hence has zero ambient κ_G. There is also a direct check of the ambient component, independent of any identification of rational kernels. Choose n_0∈N(L)∩ker κ_G representing a given h∈W_a^θ. Then c=n_0^{-1}θ(n_0) belongs to T(L)_1. Lang surjectivity on the θ-stable torus parahoric gives t∈T(L)_1 with tθ(t)^{-1}=c. Hence n_0t is θ-fixed, represents h, and has ambient κ_G=0. ∎

This remains valid for reductive J. Central directions are omitted from the reduced apartment, whereas their discrete information is retained by κ_G below.

### Lemma D  Separation can be imposed along a gallery extension

Let z∈H. A minimal gallery of ambient Weyl type z^{-1} ending at a can be extended to an alcove t_{Nλ}a with λ as in Lemma B, so that the concatenation remains minimal. One can impose any finite list of Lemma B conditions at the same time.

Proof. In the rational apartment E, take a minimal rational gallery from z a to a. H is its affine Weyl group by Lemma C. By Haines–Ngô §5, Lemma 5.3 and Corollary 5.6, this gallery goes in one rational finite-Weyl direction. Proposition 5.5 says the corresponding acute cone from a contains a translate of that direction's open Weyl chamber. Choose λ in the interior of that chamber, additionally avoiding the finitely many hyperplanes in Lemma B. For large N, t_{Nλ}a belongs to the acute cone. A gallery a→t_{Nλ}a in the same direction concatenates minimally with z a→a.

Reduced products in the rational affine Weyl group remain length-additive in the ambient affine Weyl group: this is Richarz Proposition 1.11 and Sublemma 1.12. Thus ℓ(z^{-1}t_{Nλ})=ℓ(z^{-1})+ℓ(t_{Nλ}) for ambient length. Replace the first segment by any ambient gallery of Weyl type z^{-1} ending at a. A gallery of reduced total type is minimal, so the conclusion holds in the entire building, without requiring that its initial alcove be rational. ∎

## The finite support check

The following lists all affine quadruples in GH §6.2 and the supports computed in §§6.3–6.6. The omitted vertex is v. Braces and intervals describe subsets of the affine nodes; the empty set occurs in every row. For Ã_{n−1} node numbers are modulo n. For B̃_n the two short arms at one end are 0 and 1, attached to 2; for D̃_n there are two fork ends 0,1 and n−1,n. Multiplicities on Dynkin edges do not affect the path argument.

| Affine datum | v | θ | Nonempty supports |
|---|---:|---|---|
| Ã_{n−1}, ω1, σ=id | 0 | n-cycle | none |
| Ã_{n−1}, ω1, σ=σ0 | 0 | i↦1−i | {1−l,…,l}, 1≤l≤floor((n−1)/2) |
| B̃_n, ω1, σ=id | 0 | (01) | {0,1,…,l}, 1≤l≤n−1 |
| B̃_n, ω1, σ=id | n | (01) | {n−l+1,…,n}, 1≤l≤n−1 |
| B̃_n, ω1, σ=τ1 | n | id | preceding chain, then S\{0}, S\{1} |
| C̃_n, ω1, σ=id | 0 | id | {0,…,l−1}, 1≤l≤n |
| D̃_n, ω1, σ=id | 0 | (01)(n−1,n) | {0,1,…,l}, 1≤l≤n−2 |
| D̃_n, ω1, σ=σ0 | 0 | (01) | preceding chain, then S\{n}, S\{n−1} |
| Ã3, ω2, σ=id | 0 | (02)(13) | {0,2} |
| Ã3, ω2, σ=σ0 | 0 | (02) | {0,2}, S\{3}, S\{1} |
| C̃2, ω2, σ=id | 0 | (02) | {0,2} |
| C̃2, ω2, σ=id | 1 | (02) | {1} |
| C̃2, ω2, σ=τ2 | 1 | id | {1}, S\{0}, S\{2} |

The old GH v1 says “21” in its introductory count, but its displayed table has the same nineteen group-level entries as the later author version, which corrects the count to nineteen. Nothing in this audit removes two actual entries on that basis.

Direct consequences of this table are: (i) every nonempty support contains v; (ii) its components are transitively permuted by θ, and each can be carried to the component containing v; (iii) supports form a chain except possibly for two terminal supports, each with singleton complement; (iv) if P'=P or P' is not contained in P, and Σ'∩P is nonempty, then P,P' are exactly those two terminal supports. In that event the node outside P lies in P' and is joined inside P' to v.

To see (iv) explicitly in a chain, either P=P', in which case Σ' is disjoint from P, or P is a proper subset of P', again disjoint from its boundary. At a fork, any nonterminal P is contained in P', so the same reasoning applies. The only remaining case is the pair of incomparable terminal supports. The four fork rows are B̃_n with σ=τ1, D̃_n with σ=σ0, Ã3 with (ω2,σ0), and C̃2 with v=1 and σ=τ2. Görtz's sentence restricting this situation to the displayed B example is therefore too narrow, but the singleton-complement proof works for all four rows.

### Lemma E  A path subword survives multiplication from P

Suppose t_0,…,t_r are distinct nodes, consecutive nodes do not commute, and t_0…t_r≤x in Bruhat order. If y∈W_P and t_0∉P, then t_0…t_r≤yx. In particular t_r belongs to supp(yx).

Proof. The word t_0…t_r has a unique reduced expression: no adjacent pair commutes and a braid of length at least three would require a repeated letter. By the braid theorem and the subword criterion, every reduced expression of x contains this exact ordered subword. On multiplying x on the left by a simple s≠t_0, an increasing multiplication preserves the inequality. In a decreasing multiplication choose a reduced expression of x beginning with s and delete that first letter. The indicated subword cannot have used that first letter, since its first letter is t_0. Induct on a word for y, all of whose letters lie in P. ∎

### Lemma F  The right cosets required in the separation proof differ

Let P,P' be supports with P=P' or P' not contained in P. Let w_1 be the minimal element of W_P w_1 W_{P'}, fixed by θ. Set z=w_1 w_{0,P'}. Suppose either

1. w_1=1 and P≠P'; or
2. w_1≠1 and supp(w_1)∩Σ'≠∅.

Then, for every s∈W_P,

    s w_{0,P} W_K ≠ z W_K.

Proof. It is enough to show that v belongs to the support of w_{0,P}s^{-1}z. We construct a path word t_0…t_r with t_r=v, t_0∉P, and t_0…t_r≤z; Lemma E then applies to w_{0,P}s^{-1}∈W_P.

In case 1, P'\P is nonempty. Move a component by θ if necessary, choose a path in P' from v to a node outside P, and stop at its first exit from P. Read this path in reverse, starting with the first node t_0 outside P. Every later node lies in P. Since its word belongs to finite W_{P'}, it is below w_{0,P'}=z. If v itself lies outside P, the one-letter path suffices.

In case 2 with Σ'∩P empty, take t_0 in supp(w_1)∩Σ'. If P' is nonempty, it is adjacent to a component of P'. Since the supports and supp(w_1) are θ-stable, apply a power of θ so that this component contains v. Connect the adjacent node through that component to v. The tail word belongs to W_{P'} and is below its longest element; t_0≤w_1 and the product w_1 w_{0,P'} is length-additive. The concatenated path word is therefore below z. If P' is empty, Σ' is the θ-orbit of v. θ-stability implies v∈supp(w_1); take t_0=v. Here also P is empty by the imposed ordering.

In case 2 with Σ'∩P nonempty, consequence (iv) of the table applies. Write S\P={t_0}. A nonidentity minimal representative of W_P\W_a/W_{P'} cannot belong to W_P, since then its double coset would contain 1. Thus t_0∈supp(w_1). Moreover t_0∈P', and there is a simple path in P' from t_0 to v. Its tail is below w_{0,P'}, and length additivity again supplies the desired subword of z. ∎

## Proof of equality of the partitions

We use the following standard building and Deligne–Lusztig facts, with their precise dependencies described in SOURCE_AUDIT.md. A spherical residue is gated: for each alcove c there is a unique gate g in the residue, and δ(c,h)=δ(c,g)δ(g,h) length-additively for every h in it. Gates to θ-stable residues from θ-fixed alcoves are θ-fixed by uniqueness. Projections of two residues have corresponding closest alcoves and a common minimal Weyl distance. Rational parahoric groups act transitively on rational alcoves in their residues; J^1 acts strongly transitively on the rational building. Finally, a twisted Coxeter DL variety is opposite every rational alcove of its finite residue, by Lusztig Corollary 2.5 and rational-group equivariance.

### Constancy on each BT piece

By J-equivariance it suffices to prove constancy on Y(w). Given j∈J, choose j_0∈J^1 with j a=j_0 a. Then j^{-1}j_0 normalizes I, and

    I j^{-1}h I=(j^{-1}j_0) I j_0^{-1}h I.

Thus multiplication by the fixed length-zero normalizer component reduces constancy to j_0. Let g be the gate of j_0 a to P_P/I. It is rational. Lusztig's result gives δ(g,h)=w_{0,P} for every h∈Y(w). Hence

    δ(j_0 a,h)=δ(j_0 a,g) w_{0,P}

is independent of h. This proves constancy at Iwahori level, and therefore at K level. The same argument works for every iY(w).

### Separation of distinct BT pieces

The full ambient Kottwitz invariant κ_G is constant on each iY(w), with value κ_G(i). If two pieces have different κ_G values, inv_K(1,−) separates them. Otherwise left translate by the inverse of the first representative to reduce to Y(w) and j'Y(w') with κ_G(j')=0. Reverse the pair if necessary so that P=P' or P' is not contained in P.

Here is an explicit normalization of the residue argument. Let R=P_P/I and R'=j'P_{P'}/I. Both are θ-stable. Gate the rational alcove j'a to R; this gives a rational alcove b in proj_R(R'). Its corresponding closest alcove b' in R' is rational. Choose an element of J∩P_P carrying b to a; it preserves Y(w), since the finite rational reductive group preserves the corresponding DL variety. After this translation, choose a rational apartment through a and b'. Strong transitivity gives an element of the rational Iwahori carrying that apartment to the standard one, again preserving Y(w). The resulting b' is w_1 a in the standard apartment, with w_1∈H the minimal representative of W_P w_1 W_{P'}. The representative of the second stratum can be replaced on the right by an element of J∩P_{P'} to have base alcove b'; equivalently it can be replaced by a rational normalizer lift n of w_1, since their quotient fixes a and lies in the rational Iwahori. All these elements have ambient Kottwitz value zero. We are now comparing Y(w) and nY(w').

If nY(w')=Y(w'), replace n by 1 and w_1 by 1. The pieces are distinct, so their supports differ, since the support determines the EO element. This is case 1 of Lemma F.

Otherwise n∉P_{S\Σ'}, by the exact BT stabilizer. For a normalizer element of ambient affine Weyl class w_1 this is equivalent to supp(w_1) meeting Σ'. Necessarily w_1≠1. This is case 2 of Lemma F. In either case n a is a gate from a to the second residue, and for h' in its DL variety,

    δ(a,h')=w_1 w_{0,P'}=:z,

with length additivity. The element z lies in H.

For every s∈W_P^θ put u_s=s w_{0,P}∈H. Lemma F gives u_s W_K≠z W_K. Apply Lemmas B and D to this finite collection of pairs, using the gallery h'→a of type z^{-1}. We obtain λ and a sufficiently large N such that j_N=t_{Nλ} has an actual representative in J^1 and

    δ(j_N a,h')=t_{−Nλ}z

for all h' in the second piece. The gallery extension only depends on z, not on the individual h'. Let g_N be the gate of j_N a to R. Since both alcoves and the standard residue lie in the standard apartment, so does the gate. Since it is rational, g_N=s_N a for some s_N∈W_P^θ. For h∈Y(w), the gate identity and Lusztig give

    δ(j_N a,h)=t_{−Nλ}s_N w_{0,P}=t_{−Nλ}u_{s_N}.

Lemma B now says that the K-double cosets of these two relative positions differ. Therefore the actual rational element representing j_N separates the two pieces. This proves the reverse refinement and hence equality.

### Zero dimensional and superbasic case

The preceding construction is only needed if dim D>0. If dim D=0, θ acts transitively on the vertices of the irreducible alcove. A proper θ-stable support must then be empty, so the only EO Coxeter element is τ and Y(τ) is a point. Every BT piece is a point jP_K with j∈J. The function inv_K(j,−) takes the identity double-coset value only at jP_K, so distinct points are separated immediately. This includes the split Ã_{n−1}, ω1 superbasic row. The source statement that the rational rank is positive in every Coxeter-type situation cannot be used to omit it.

## Reductive groups and central isogenies

The proof above is intentionally carried out in G and its actual J, rather than deduced by assuming rational-point surjectivity to the adjoint group.

1. Passing from G to its adjoint group does not change the reduced building, its ambient affine Weyl group, its affine reflection hyperplanes, or the diagram action of θ. It can change the extended group Ω=W̃/W_a and rational-point images. The reduced affine Weyl group is identified via the simply connected derived group (Richarz Remark 1.5), so all the geometric and support calculations remain valid.

2. The map κ_G:G(L)→π_1(G)_I, including torsion, is retained throughout. Connected parahorics are in its kernel. Consequently the label κ_G(i) of iY(w) is well defined. Distinct such labels are separated by inv_K(1,−). This step keeps both central translations and finite isogeny component information; reducing only modulo the real vector space of the center would be insufficient.

3. In a common component, the residue argument uses rational parahorics and J^1 only. These are subgroups of the actual G(L), have zero ambient κ_G, and provide the needed chamber transitivity, apartment normalization, and translation lifts by the affine BN-pair and Richarz Lemma 1.6. No step asks to lift an arbitrary element of J_ad(F).

4. For constancy with an arbitrary j∈J, replace its rational alcove by one reached by J^1. The residual element stabilizes a and normalizes I, so it changes the full Iwahori relative position by one fixed extended-Weyl factor. It does not destroy constancy or erase a central component. This also avoids assuming that J∩ker κ_G has been identified with J^1 in advance.

5. The BT decomposition and its stabilizers extend in this root datum directly. If x^{-1}θ(x) lies in the θ-stable parahoric P_P, Lang surjectivity on that connected parahoric gives p∈P_P with θ(p)=p(x^{-1}θ(x)) (or its equivalent inverse convention), so xp^{-1}∈J. Thus the same decomposition into J/(J∩P_P) translates holds. The connected reductive quotient of the parahoric has the same finite root data; a central isogeny does not change its flag variety or its Bruhat cells. GH's Coxeter projection argument is the same finite-Weyl/partial-conjugation calculation, and the commuting complement I(K,w,σ)=S\(P∪Σ) gives the stabilizer J∩P_{S\Σ}. Hence all central labels stay in the rational coset index instead of being accidentally collapsed into an unlabelled building. Lang also proves independence of the normalizer lift of τ. These facts use connected parahorics; replacing them by full facet stabilizers without Kottwitz restrictions would be a different level convention.

The exact stabilizer in item 5 can be checked without an adjoint-group inference. Put Q=I(K,w,σ)=S\(P∪Σ), R=P∪Q. The sets P and Q commute, Q is θ-stable, and R is spherical. GH Theorem 4.1.2 constructs a J-equivariant isomorphism from the fine K-level piece to the coarse piece at level Q. Its construction iterates the canonical operation P_0↦(P_0∩θ(P_0))U_{P_0}, with the corresponding relative-position refinements, until the subset stabilizes at Q. These are parahoric intersection, pro-unipotent radical, and Weyl double-coset operations; they apply to connected reductive groups without alteration. On the κ_G=0 component, parahorics are self-normalizing in G(L)^1, so the parahoric-conjugacy description loses no coset. On other components the source's §4.5 separately carries the Ω label. Thus the construction is not identifying distinct central cosets.

At Q-level the condition has the form g^{-1}θ(g)∈P_Q xP_Q with x=wτ^{-1}∈W_P. Lang on P_R then gives g∈J P_R. Consequently this coarse piece is a disjoint union, indexed by J/(J∩P_R), of subsets inside the distinct residues iP_R/P_Q. The finite quotient splits its P and Q flag directions, since their diagrams are disconnected; its DL subset in P_R/P_Q is exactly the P-Coxeter DL variety. The J-equivariant isomorphism identifies this subset with Y(w) at K-level (GH Corollary 4.6.2). Elements of J∩P_R preserve it by rational equivariance of the DL condition; elements outside P_R take it to a disjoint residue. Nonemptiness gives the exact stabilizer J∩P_R=J∩P_{S\Σ}. This is the required reductive stabilizer statement, with full components retained.

6. A pure torus has no root-theoretic part. Its connected parahoric quotient is the Kottwitz group, so a fixed κ fiber in its affine flag set is a point, and inv_K(1,−) already distinguishes points. This accounts for any root-free central part without adding a fictitious gallery argument.

This reconstructs the “easy” reductive extension for reductive groups with the same connected reduced affine datum in the original GH list. It is stronger than merely quoting Chen–Viehmann Lemma 2.4, whose converse explicitly assumes J(F)→J_ad(F) surjective and whose Remark 2.5 warns against assuming that in general.

Literal direct products of covered data factor both the varieties and both partitions, so equality follows factor by factor. Arbitrary disconnected diagrams with Frobenius permuting factors, or arbitrary maximal rational parahorics obtained by removing an orbit, are not claimed here. GH Remark 6.1.1 requires additional checks of its Coxeter-straight condition and support assertions for such generalizations. Those are outside the original classified case range, not silently absorbed into the phrase “all Coxeter type.”

## Acceptance boundary

The prior theorem is an exact match to the original basic, τ-representative, hyperspecial minuscule conjecture, and covers the original GH rational maximal extensions with the hypotheses above. The reconstruction supplies a complete finite-separation replacement, the actual rational normalizer lifts, the missing zero-dimensional branch, the four fork cases, and a direct reductive argument preserving components.

There remains a source-version limitation: the final journal proof was not retrieved. The inspected v1 proof cannot be accepted unmodified because Lemma 3.10 is literally false. Accepting the mathematical conclusion on this audit requires accepting the reconstruction and the named standard/source dependencies; it is not an assertion that every line of an unavailable final text was checked. No theorem counterexample, no new solution claim, and no independent publication claim is made.
