# Independent obstruction-theory audit

Audit date: 2026-10-21 UTC. Scope: authored mathematics and public sources. No publication actions.

## Verdict

The finite stage-3 matching lemma is correct with its rigidification, local-monodromy, all-global-stage-2-components, and point-realization qualifications. Its initial inverse-limit warning needs a substantive correction: for **any countable inverse system of finite continuous Galois modules** over a field of torsion cohomological dimension at most 3, the relevant `lim^1 H^3` vanishes. This does not by itself identify the actual étale section spaces with a chosen continuous-cohomology model.

Tian's 2026 example is not a source of a nonzero geometric pi_3. A characteristic-zero comparison argument, supplied below, proves its first three geometric profinite étale homotopy groups vanish. Thus it cannot give a strict stage-2/stage-3 separation. A claim excluding every possible full-tower effect should additionally state the applicable truncation/convergence theorem rather than hide it inside this calculation.

## 1. Finite coefficients: existence is not matching

Let F be K or a completion K_v at a closed point of the smooth projective p-adic base curve. Then cd(F)=3. In a fixed Postnikov fibration with geometric fibre K(B,3), let s be an actual stage-2 section and B_s its pulled-back finite local coefficient module. The obstruction to lifting s is in H^4(F,B_s), hence zero. The components of its homotopy fibre, with a chosen homotopy identifying the projection with s, form a torsor under H^3(F,B_s).

Consequently a stage-3 separation cannot be proved by exhibiting a nonzero degree-4 obstruction with finite coefficients. Rather, for a fixed global lift t and fixed local projection homotopies, prescribed local differences delta_v must fail to lie in the localization image of H^3(K,B_s).

The phrase “fixed local projection homotopies” matters. Forgetting those homotopies divides the homotopy-fibre components by the monodromy action of pi_1 of the local stage-2 section space. Therefore an obstruction for actual local section components requires the product of the relevant local orbits to miss the global localization image. A representative delta outside the image does not suffice when a different representative in its local orbit can lie in the image. In a split K(A,2) model this acting group is H^1(F,A), but the action is governed by the k-invariant and is not automatically trivial.

One must also test every global stage-2 section component matching the local tuple, not merely a convenient one. Finally, abstract cohomology classes are not automatically images of actual local algebraic points, and restricted-product conditions must be established before invoking arithmetic duality. These are substantive construction requirements, not notation choices.

## 2. Correct countable inverse-limit lemma

**Lemma.** Let Gamma be a profinite group with torsion cohomological dimension at most d, and let `(B_m)_{m>=1}` be an inverse sequence of finite discrete continuous Gamma-modules. No surjectivity of its transition maps is required. Then the inverse sequence H^d(Gamma,B_m) is Mittag-Leffler, and its first derived inverse limit is zero.

**Proof.** Fix m. For n>=m put I_nm = image(B_n -> B_m). This is a descending family of Gamma-submodules of the finite group B_m, so it stabilizes for sufficiently large n. The exact sequence

    0 -> ker(B_n -> I_nm) -> B_n -> I_nm -> 0

has finite, hence torsion, kernel. Its long exact cohomology sequence and the vanishing of H^(d+1) of that kernel show that H^d(Gamma,B_n) -> H^d(Gamma,I_nm) is surjective. It follows that

    image[H^d(Gamma,B_n) -> H^d(Gamma,B_m)]
      = image[H^d(Gamma,I_nm) -> H^d(Gamma,B_m)].

The expression on the right is constant once I_nm stabilizes. This proves the Mittag-Leffler condition for H^d. For inverse sequences indexed by the natural numbers, Mittag-Leffler implies lim^1=0. QED.

In particular, in the derived inverse-limit continuous cohomology model with the standard Milnor exact sequence

    0 -> lim^1 H^(q-1)(Gamma,B_m)
      -> H^q_cont(Gamma,(B_m))
      -> lim H^q(Gamma,B_m) -> 0,

we obtain H^4_cont(G_K,(B_m))=0. The same holds over K_v. This conclusion does not require the groups H^3(K,B_m) themselves to be finite. For surjective coefficient transitions, there is a shorter proof: the H^3 transition maps are surjective because H^4 of each finite kernel is zero.

By contrast, the exact sequence in degree 3 contains lim^1 H^2. The preceding argument says nothing about its vanishing: H^2 need not map onto H^2 of an image module, because the connecting H^3 of the kernel need not vanish. Therefore one must not silently identify H^3_cont with lim H^3 without another hypothesis or calculation. No nonzero lim^1 H^2 example is asserted here.

**Model boundary.** The lemma concerns finite modules, a countable indexing tower, and the displayed derived-limit definition. It does not identify arbitrary pro-objects with an inverse sequence, supply compatible quotient Postnikov k-invariants, interchange pi_0 with a homotopy inverse limit, or prove a global/local section-classification theorem. Those are separate issues. Conversely, one must not cite a merely hypothetical lim^1 H^3 as a genuine degree-4 obstruction in this finite-tower model: it is provably zero.

The Milnor sequence and its continuous-cohomology context are treated in Jannsen, *Continuous étale cohomology*, introduction (0.2), Sections 1–2: https://epub.uni-regensburg.de/26684/1/jannsen12.pdf . The image-stabilization proof above is our explicit deduction, not a quoted theorem from that source.

## 3. Tian geometry: the missing pi_3 is provable

Source input: Tian, *Cohomological Obstructions for Varieties over p-adic Function Fields*, arXiv:2606.27699v1, Construction 5.1, uses a semisimple simply connected group G and a G-torsor Y -> X, where Y is affine space minus a closed subset of codimension at least 3. The construction has a K-point. Theorem 1.2 separates unramified degree-3 and étale degree-3 cohomological obstructions. Source: https://arxiv.org/html/2606.27699v1 .

Here is an independent geometric calculation, rather than an inference from the names of those obstructions or from vanishing of a single cohomology group.

1. Descend the finite-type data, torsor identity, smoothness, codimension bound, and semisimple simply connected geometric group to a finitely generated characteristic-zero subfield L. Embed L into C. Comparison of geometric profinite étale homotopy types under algebraically closed characteristic-zero field extensions permits calculation using the resulting complex variety. This does not posit a canonical complex embedding of the p-adic field, nor preserve its arithmetic Galois action; only geometric homotopy groups are being calculated.

2. Let Z(C) carry a finite Whitney stratification. Each stratum has real codimension at least 6 in C^N. A sphere map S^i -> Y(C), i<=4, extends into contractible C^N over D^(i+1). Relative transversality to all strata, with the boundary kept in Y(C), perturbs this extension off every stratum because i+1<=5<6. Thus Y(C) is path connected and pi_i(Y(C))=0 for 1<=i<=4. This proves the required connectivity even for singular Z.

3. The analytification of the smooth G-torsor is locally analytically trivial: smoothness provides local analytic sections, and the torsor identity gives product trivializations. Thus G(C) -> Y(C) -> X(C) is a topological fibre bundle and has a homotopy long exact sequence.

4. For a connected semisimple simply connected complex algebraic group, G(C) is connected and topologically simply connected. Also pi_2(G(C))=0. One standard explanation of the latter uses deformation retraction to its compact form U and the maximal-torus fibration T -> U -> U/T: the flag manifold has its even-dimensional Bruhat cells, pi_2(U/T) has rank rank(T), and the connecting map to pi_1(T) is an isomorphism for simply connected U. The exact sequence then gives pi_2(U)=0. These statements concern the group G, not the quotient X; the shift in the next step is essential.

5. The fibre-bundle exact sequence and the vanishing in step 2 give pi_i(X(C)) = pi_(i-1)(G(C)) for i=2,3 and pi_1(X(C))=0. Therefore pi_1, pi_2, pi_3 of X(C) all vanish. In fact pi_4(X(C))=pi_3(G(C)); this last group is generally nonzero. Confusing pi_3(G) with pi_3(X) would shift the mechanism by one degree.

6. Complex algebraic varieties have finite CW homotopy type. For the simply connected X(C), the characteristic-zero étale/topological comparison and finite-type profinite completion theorem identify its geometric profinite étale homotopy groups with the completions of these topological groups. In particular pi_i^et(X_barK)=0 for 1<=i<=3. A classical reference for the comparison formulation is Sullivan, *Geometric Topology*, Theorem 5.2 and the following discussion: https://webhomes.maths.ed.ac.uk/~v1ranick/surgery/gtop.pdf .

It follows that the geometric stage-2 and stage-3 truncations in this example are both contractible. The rational point supplies sections. Therefore their homotopy obstruction sets coincide with the whole adelic set; no stage-3 local matching defect is available here. The theorem about the unramified obstruction must not be relabeled a higher étale homotopy theorem. Its use of a motivic degree-4 complex is likewise not the same object as a finite discrete geometric pi_3-module.

This proves exclusion as a stage-3 witness. To upgrade the sentence to “the full homotopy obstruction is trivial,” cite and check the relevant cd=3 truncation/convergence theorem in the precise étale homotopy framework. Neither a bare connectivity slogan nor the mere fact X(K) is nonempty proves triviality of an adelic obstruction.

## 4. Acceptance conditions remaining

A resolution still requires an explicit X and an actual adelic tuple, a global stage-2 match, and a stage-3 failure surviving all local monodromy choices and all possible global stage-2 matches. A compatible finite quotient that detects this failure suffices to exclude a full lift. No such witness has been constructed in this audit. Neither Tian's different separation theorem nor the finite existence calculation closes the original question.
