# Coherent descent of local-system Jones models: a bounded obstruction and the missing bridge

14 October 2026. Authored research in shared mathematical pass 1 for Roberts Problem 1.7, identifier 10400007. This report does not claim an intrinsic construction, a resolution, a novelty theorem, or a general impossibility theorem.

## Result

The full twisted chain complexes of the configuration spaces underlying the Bigelow plat model cannot descend through plat stabilization by quasi-isomorphisms, even after arbitrary homological shifts, monomial normalizations, or the Jones specialization. The obstruction is their Euler characteristic:

\[
\chi\bigl(\operatorname{UConf}_{n}(\mathbb R^2\setminus\{2n\text{ points}\});\mathcal L\bigr)
=(-1)^n\binom{3n-2}{n}
\]

for every rank-one local system over a field. Its absolute values begin

\[
1,6,35,210,1287,8008,50388,319770.
\]

A homotopy colimit of non-equivalence maps is not ruled out. Such a construction still needs geometric stabilization correspondences, coherent local-system transport, compatible supported classes and pairings, and a proof that its extraction is the entire Jones polynomial. Merely forming a presentation category or declaring a scalar constant does not supply those data.

## 1. Concrete starting data, with conventions kept separate

For a chosen oriented plat presentation \(p=(n,\beta)\), use a punctured disc \(S_n\) with \(2n\) punctures and set \(X_p=\operatorname{UConf}_n(S_n)\). For the Euler-characteristic argument we take the interior of the disc, homeomorphic to the plane. Allowing the outer boundary has the same ordinary homotopy type, but a statement about Borel–Moore homology below refers specifically to the interior model.

Let \(R=\mathbb Z[Q^{\pm1},D^{\pm1}]\). The standard character of \(\pi_1(X_p)\) records total puncture winding as \(Q\), and a positive exchange of two moving particles as \(D\). The corresponding rank-one local system is \(\mathcal L_p\). For one particle the exchange generator is absent. An explicit description of the exchange exponent is the winding of the discriminant \(\prod_{i<j}(z_i-z_j)^2\); puncture winding is the winding of \(\prod_{i,a}(z_i-p_a)\).

The known plat formula pairs a locally finite fork class with a compact torus class, with compatible lifts to the character cover. After \(D=-Q^{-1}\), its writhe/exponent/unknot normalization gives the full source-normalized Jones polynomial. This is Bigelow's existing theorem, not the contribution of this report. [Bigelow, definitions 2.1–2.7 and Theorem 2.8](https://web.math.ucsb.edu/~bigelow/publications/06.pdf)

In local-coefficient notation an ordinary middle-dimensional intersection pairing has the form

\[
H_n^{\mathrm{BM}}(X_p;\mathcal L_p)\otimes_R
H_n(X_p;\mathcal L_p^{\vee})\longrightarrow R,
\]

when the support, finiteness, and dual-coefficient conditions needed for this pairing are imposed. The covering-space convention instead writes an equivalent sesquilinear equivariant pairing using the involution on deck variables. Identifying these conventions, keeping track of lifts and units, and carrying the distinguished fork/torus classes are part of any proposed descent, not optional bookkeeping.

The field-level obstruction may use \(k=\mathbb Q(Q,D)\), or the specialized character over \(k=\mathbb Q(Q)\) with \(D=-Q^{-1}\). It does not require genericity, a concentration theorem, or identification of middle-dimensional homology with a Lawrence module.

## 2. Euler-characteristic obstruction

### Proposition 2.1

Let \(X_n=\operatorname{UConf}_n(\mathbb R^2\setminus P_{2n})\), where \(P_{2n}\) is any set of \(2n\) points. For any field \(k\) and any rank-\(r\) local system \(\mathcal E\) on \(X_n\),

\[
\chi(X_n;\mathcal E)=r(-1)^n\binom{3n-2}{n}.
\]

Here the left side is the alternating sum of the finite dimensions of ordinary twisted homology. The same formula holds for Borel–Moore twisted homology of this interior model.

**Proof.** The ordered configuration space \(F_j(S)\), with \(S=\mathbb R^2\setminus P_{2n}\), forgets its last point by a locally trivial fibration whose fiber is \(S\) minus \(j-1\) further points. Its Euler characteristic is \(1-2n-(j-1)\). Iterating Euler multiplicativity gives

\[
\chi(F_n(S))=\prod_{j=0}^{n-1}(1-2n-j).
\]

The symmetric group acts freely, with \(F_n(S)\to X_n\) a covering of degree \(n!\). Consequently

\[
\chi(X_n)=\frac{1}{n!}\prod_{j=0}^{n-1}(1-2n-j)
=(-1)^n\frac{(3n-2)!}{n!(2n-2)!}.
\]

These configuration spaces have finite CW homotopy type. One way to ensure the required finiteness is to regard ordered configurations as a complex hyperplane-arrangement complement and use a finite semialgebraic triangulation model; the free finite quotient is again of finite CW type. In a finite cellular model each cell contributes an \(r\)-dimensional twisted chain group. The alternating dimension of chains is therefore \(r\chi(X_n)\), independently of all monodromy. Euler–Poincaré proves the ordinary formula. Finally \(X_n\) is an oriented real \(2n\)-manifold: swapping two real two-dimensional coordinate blocks preserves orientation. Local-coefficient Poincaré duality and finite-dimensionality identify the Borel–Moore Euler characteristic with the cohomological Euler characteristic, up to the sign \((-1)^{2n}=1\). This gives the same formula. ∎

The forgetful fibration is the classical configuration-space fibration of [Fadell–Neuwirth, *Configuration Spaces*, Math. Scand. 10 (1962), 111–118](https://doi.org/10.7146/math.scand.a-10517). The calculation and obstruction above are supplied explicitly here rather than attributed to that article as a Jones theorem.

### Corollary 2.2: no full-complex stabilization equivalence

Choose any rank-one field local system \(\mathcal E_n\) on each \(X_n\), and arbitrary integers \(s_n\). There is no system of quasi-isomorphisms

\[
C_*(X_n;\mathcal E_n)[s_n]\simeq C_*(X_{n+1};\mathcal E_{n+1})[s_{n+1}]
\]

implementing every plat stabilization. This remains true for the full Borel–Moore complexes of the interior model. Multiplying classes or maps by Laurent monomials does not change the conclusion.

**Proof.** A quasi-isomorphism preserves Euler characteristic. A shift changes only its sign. The absolute Euler characteristics are \(a_n=\binom{3n-2}{n}\), with

\[
\frac{a_{n+1}}{a_n}=\frac{3(3n-1)(3n+1)}{2(n+1)(2n-1)}>1
\quad(n\ge1).
\]

Thus even neighboring presentations cannot have equivalent shifted full complexes. Monomial normalizations do not change their dimensions over the coefficient field. ∎

The standard stabilization of plats adds two strands and one particle. It can be iterated for a fixed knot. Hence this mismatch is present among presentations of the same knot, including repeated stabilizations of an unknot; it is not a comparison of different knot types.

### Corollary 2.3: a finite tensor factor cannot repair this particular tower

Even allowing a new finite-dimensional homology complex \(E\) at the \(n=2\) stabilization cannot give

\[
C_*(X_3;\mathcal E_3)\simeq C_*(X_2;\mathcal E_2)\otimes_k E
\]

up to any shift: the equality of Euler characteristics would require \(|\chi(E)|=35/6\), whereas \(\chi(E)\) is an integer. This rules out that finite tensor-factor repair for the **full** complexes, not more general correspondences, cones, subquotients, or categories.

### Scope boundaries

- This is not a no-go theorem for Roberts's problem.
- It is not a no-go theorem for all local systems, all relative theories, all particle numbers, or all spaces derived from a knot.
- It does not establish the ranks of individual middle-dimensional homology groups. No concentration theorem was used.
- It does not rule out extracting and stabilizing a geometrically defined subquotient, adding a differential, using correspondences, or constructing a non-equivalence homotopy colimit.
- An arbitrary relative pair can change Euler characteristic; the argument cannot be transferred to such a pair without calculating that pair.
- The Jones specialization cannot remove this full-complex obstruction: the specialized character is still rank one, and the same cellular Euler calculation applies.

## 3. What a genuine descent construction would have to contain

A useful geometric indexing proposal starts with the actual oriented knot pair \((S^3,K)\). Its objects are embedded bridge/Heegaard presentations, including whatever collar, ordering, meridian, basepoint, or framing data the coefficient construction needs. Its morphisms and relations come from geometric isotopies, local bridge changes, handleslides, stabilizations, and families of those changes. Ambient diffeomorphisms act by transporting these objects and families. This describes a research program, not a completely constructed indexing category in this report.

There are two materially different routes.

### Route A: descent of an already equivalent homological object

For every presentation, supply supported local-system homology objects \(A_p,B_p\), geometric distinguished classes \(a_p,b_p\), and a pairing \(\mu_p\). Every elementary geometric change must induce isomorphisms on the actual retained objects, preserve the classes after explicit normalizations, and preserve the pairing. Composites representing the same ambient identification must agree. Then the objects form a transitive system and the classes/pairing descend. This argument can be made at the homology level; a full infinity-categorical construction is not necessary merely to obtain natural homology groups and a pairing.

If one instead claims a chain-level homotopy colimit or an actual glued space, compatible chain maps or space maps and the coherences that this stronger claim needs must be supplied. For a diagram of spaces with compatible local systems and homotopy-equivalence structure maps over a contractible indexing nerve, the homotopy colimit provides a familiar sufficient mechanism. That mechanism cannot use the unmodified \(X_n\) or their full twisted chains, by Section 2.

Importantly, a canonical algebraic object alone does not complete the adopted intrinsic-local-system contract. The construction must retain a geometric local-system realization associated naturally to the ambient pair. One cannot conclude this simply by labeling an abstract algebraic colimit “intrinsic.”

### Route B: a new object from non-equivalence correspondences

Allow stabilization to be a genuine non-equivalence. Then a homotopy colimit might produce a different invariant. To make this a construction rather than a name, at least the following must be furnished:

1. Actual geometric maps or correspondences, with local-coefficient identifications. A correspondence needs justified pushforward/pullback or Gysin operations and their degree/support hypotheses; it is not automatically a map of configuration spaces.
2. A choice category and coherence relations derived from the ambient knot pair. A free category on a list of moves is insufficient if different move sequences represent the same geometric event.
3. A compatible extraction operation on the resulting object. The two inputs to an intersection pairing may have different variance and support requirements, so they do not automatically pair after taking separate covariant colimits.
4. Distinguished classes or cycles genuinely assembled by geometry, including their behavior when particle number changes.
5. Finiteness or an alternative precisely defined operation that produces a Laurent polynomial rather than an infinite series or an undefined Euler characteristic.
6. An independent proof of source-normalized Jones equality. If this proof invokes the known plat pairing, it must prove that the colimit operation computes that pairing, including its writhe, mirror, variable and unknot conventions.

None of these missing structures is supplied merely by equality of the normalized scalar before and after a Markov move.

## 4. Two elementary tests against formal repairs

### 4.1 A homotopy colimit retains indexing topology

Let \(\mathcal G\) be the one-object groupoid with automorphism group \(\mathbb Z\), and let the diagram be constantly \(k\) in degree zero, with the identity on every arrow. Then

\[
\operatorname{hocolim}_{\mathcal G} k\simeq C_*(B\mathbb Z;k)\simeq C_*(S^1;k),
\]

so it has both \(H_0=k\) and \(H_1=k\). The individual fibers had only \(H_0=k\). Even perfect coherence and trivial monodromy do not make an arbitrary indexing nerve contractible.

This example does not prove that a geometrically defined colimit is invalid. It proves that its extra homology and extraction cannot be ignored. Conversely, replacing the presentation category by a thin category, with a unique arrow between every pair, removes this topology only after one has actually supplied the corresponding path-independent transport; declaring it does not prove it.

### 4.2 Equality of one pairing is weaker than chain transport

Take \(A=k\) and \(B=k\oplus k\), both in degree zero. Let \(s(v)=(v,0)\), \(a=1\), \(b=(1,0)\), and evaluation maps \(e_A(v)=v\), \(e_B(v,w)=v\). Then \(s(a)=b\) and \(e_A(a)=e_B(b)=1\), with \(e_Bs=e_A\), although \(s\) is not a quasi-isomorphism. Its complementary summand is invisible to the selected evaluation.

Thus scalar invariance can coexist with a genuine obstruction to full-complex equivalence. Formally killing complementary summands or stabilization cones requires proving that the desired homological operation factors through that quotient and that the quotient retains the required geometric interpretation. It cannot be justified only by the selected scalar's equality.

## 5. Heegaard naturality supplies a template, not the Jones bridge

The relevant existing model for this type of descent is Juhász–Thurston–Zemke's naturality framework. In their v4, Definition 2.32 gives the strong-invariant requirements and Theorem 2.38 proves path independence for the specified diagram graph; the resulting transitive system then gives canonical transport. [Primary manuscript, arXiv:1210.4996v4](https://arxiv.org/pdf/1210.4996v4)

This is an exact methodological bridge **if** one first supplies a local-system Jones object satisfying those geometric hypotheses. It does not prove that a braid-local-system model satisfies them. In particular, the current quantum braid Floer theory is explicitly not invariant under stabilization or conjugation before specialization. Its scalar Jones specialization does not manufacture homology isomorphisms. [Anghel–Juhász, *Quantum braid Floer homology*, v4, §9.2](https://arxiv.org/html/2601.08805v4#S9.SS2)

There is also an important prior-art limit: Lawrence's 1993 paper already gives a twisted-homology representation of the tangle category, using Turaev's presentation. Consequently, “add cup/cap maps and make a tangle functor” is not by itself a new answer to the contextual intrinsic problem. [Lawrence, *A functorial approach to the one-variable Jones Polynomial*, author abstract](https://www.ma.huji.ac.il/~ruthel/papers/93funapo.html)

## 6. Decision and smallest substantive next target

The attempted raw-complex descent fails by a proved, coefficient-independent stabilization obstruction. A non-equivalence geometric descent remains a possible direction, but no complete object or extraction has been constructed here.

The smallest useful next mathematical target would be a **geometrically specified relative/subquotient object and a single stabilization correspondence** which:

- transports the relevant local systems and supports;
- produces the correctly degree-shifted distinguished classes;
- preserves the full specialized pairing with its explicit normalization;
- is compatible with ambient isotopies and an initial nontrivial relation between move sequences; and
- is not merely a restatement of the existing homological tangle representation.

One must then extend this to all required moves and coherence relations, and exhibit its ambient geometric realization. No such target is claimed achieved in this pass. The broad problem remains unresolved by this approach.
