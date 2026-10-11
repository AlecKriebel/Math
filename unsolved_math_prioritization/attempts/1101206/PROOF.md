# Proof: recursive bounds for based cyclic fixed subgroups

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance concerns only the recursive-bound consequence of the imported Bogopolski–Maslakova basis algorithm; it is not external human peer review or formal proof-assistant certification. This is a written proof/audit edition, not a computational reproduction package. Source inspection and elementary finite checks were performed during the preceding investigation on 11 October 2026. Edition preparation authenticates retained bytes without a fresh scholarly-source inspection or mathematical-program rerun.

This standalone proof edition reproduces the complete authored argument of the accepted mathematical audit, including its source-dependency and inspection limits. AUDIT.md preserves that same report under its audit heading; the two files are not separate independent derivations or audits.

## Conclusion and scope

Problem 1101206, AMR-010-1206, is Bestvina's Question 12.6. On the reading that asks for a computable bound, the requested bound follows from the established fixed-subgroup basis algorithm of Bogopolski and Maslakova. This report proves that consequence, including effective enumeration, automorphism recognition, the based-word convention, and changes of input measure.

The precise accepted conclusion is this: for the specified free basis of the free group of rank n, there is a total recursive function B(n,L) which is the exact largest reduced length of a generator of a nontrivial cyclic fixed subgroup among automorphisms whose basis images all have length at most L. An empty maximum is assigned the value zero. The function is uniform in the finite rank n. A bound in terms of total input length follows as well.

This is an application of an imported established theorem. It is not a new solution of the fixed-subgroup algorithm problem, not an independent verification of the complete Bogopolski–Maslakova proof, and not a polynomial, exponential, elementary, primitive-recursive, or other specified growth estimate. No claim that such stronger bounds are unknown in the literature is made. The source question does not specify one of those growth classes.

Recommended mathematical disposition: **PRIOR_RESULT_VERIFIED_SCOPED**, meaning that the computable-bound interpretation is covered by prior results, with the finite-maximum consequence proved here. Acceptance of an unspecified quantitative interpretation, or of the entire prior algorithm's proof, would exceed this report.

## Source statements and the imported theorem

Bestvina's [problem list, Question 12.6, PDF page 20](https://www.math.utah.edu/~bestvina/eprints/questions-updated.pdf) asks for a bound for the generator length of a cyclic fixed subgroup in terms of automorphism complexity. The same page separately identifies a relative-train-track-input variant as easier and records a computability assertion attributed to Maslakova. It does not define the complexity parameter or require a particular asymptotic rate. We therefore specify both the parameter and the accepted conclusion instead of identifying different formulations implicitly.

The sole imported mathematical theorem needed below is the following consequence of [Bogopolski–Maslakova, Theorem 1.1, arXiv:1204.6728v6, page 3](https://arxiv.org/abs/1204.6728v6): there is an algorithm A which, given the images of a finite free basis under an automorphism, halts and outputs words that freely generate its actual fixed subgroup. Its output is in the original basis. The paper defines the image norm by the maximum reduced length of a basis image. Its use of “efficient” means an effective recursive step bound, not polynomial time. On the same page the authors explicitly describe the earlier published Maslakova proof as incomplete.

The source is imported as an established theorem, including its correctness and termination, rather than certified anew. The published 2016 article is identified in Feighn–Handel's bibliography; the retained text actually inspected for the statement above is the 68-page arXiv v6 of 15 January 2014. No byte-for-byte or proof-for-proof equivalence between that preprint and the 2016 journal article is asserted.

[Feighn–Handel, Proposition 9.10, published PDF page 58, printed page 1216](https://ems.press/content/serial-article-files/29889?nt=1), corroborates the algorithmic conclusion by another construction. It is not needed for the finite-maximum proof. Its statement and complete short reduction were read, as were Section 9's component arguments. Their deep external dependencies and the preceding CT construction were not independently proved here. Calling this a complete independent correctness audit of either paper would be inaccurate.

## Definitions

For n at least one let F_n have the fixed ordered free basis X_n=(x_1,...,x_n). A word is a finite sequence of letters x_i or x_i^{-1}; free reduction cancels adjacent inverse letters. Write |w| for the length of the reduced representative of the group element w. This is based word length, with no conjugation or cyclic reduction.

For an automorphism alpha define

    M(alpha) = max_i |alpha(x_i)|.

An input for alpha is its n-tuple of reduced images, together with n. Every tuple specifies an endomorphism; not every tuple specifies an automorphism. An automorphism has no empty basis image. We use ordinary finite-word algorithms with explicit input and output words, not compressed straight-line programs.

If Fix(alpha) is nontrivial cyclic, its generators are g and g^{-1}, with equal reduced lengths. Write ell(alpha)=|g|. This number is independent of the chosen generator. If Fix(alpha) is trivial, record zero separately; the empty free basis and the one-element generating set containing the identity should not be confused. Noncyclic fixed subgroups are omitted from the cyclic maximum.

For n=0 the group is trivial and we define B(0,L)=0. For negative or malformed inputs a total implementation may reject them; the theorem's domain is pairs of nonnegative integers.

## Effective automorphism recognition

Here is a finite decision procedure for a tuple (w_1,...,w_n). We give the justification so the finite-maximum argument does not hide a promise problem or wait forever on nonautomorphisms.

Freely reduce the input. For n at least one, reject the tuple if any w_i is empty. Otherwise build a finite based graph K by taking n circles with their basepoints identified, subdividing the ith circle into |w_i| oriented edges and labelling its traversal by w_i. The reverse of a directed edge has the inverse label. K is connected and has fundamental-group rank n. Its based loop labels generate precisely the subgroup H=<w_1,...,w_n> of F_n.

Whenever two distinct oriented edges have the same initial vertex and the same label, identify them and their terminal vertices. Each such fold reduces the number of geometric edges by one, so the process terminates after finitely many folds. Labels are respected throughout. Call the resulting connected labelled graph K'. Its labelled map to the n-petal rose is locally injective: at any vertex, a specified letter labels at most one outgoing directed edge.

Folds preserve the subgroup of based loop labels. One inclusion follows by mapping a loop forward. For the converse, a path in the quotient can be lifted piece by piece, inserting, when necessary, the path e_1^{-1}e_2 between terminal vertices that were identified. That connecting path has freely trivial label. A based quotient loop therefore yields an original based loop with the same group label. If the original basepoint is among the identified vertices, the same zero-label connecting path adjusts its start or end. Repeating this argument proves that the based loop-label subgroup of K' is H.

In a locally injective labelled graph, cancellation of two adjacent inverse letters in a path is cancellation of an edge followed by its actual inverse. Thus, if the label of a based loop reduces to x_i, there is a based single-edge loop labelled x_i. Consequently H=F_n if and only if every x_i is the label of such a loop at the basepoint of K'. This is a finite check. In that case these n loops exhaust all directions at the basepoint, and connectedness implies that K' is exactly the n-petal rose.

It remains to justify that this surjectivity check really detects automorphisms. This can be proved within the graph construction, without importing a Hopficity test. For a connected graph its rank is E-V+1. A fold with distinct terminal vertices reduces E and V by one and preserves rank; a fold with equal terminal vertices reduces rank by one. The rank never increases. Since both initial K and final rose have rank n, an accepted folding sequence contains only folds with distinct terminal vertices.

Each such fold is a homotopy equivalence. For completeness, suppose e_1,e_2 have common initial vertex u and distinct terminal vertices v_1,v_2. Choose v_1 as the representative of the merged vertex; if one endpoint equals u, name it v_1. In K the path t=e_1^{-1}e_2 goes from v_1 to v_2 and maps in the quotient to the null-homotopic backtrack e^{-1}e. A reverse map sends the merged edge to e_1; each other edge is sent to its old edge, prefixed or suffixed by t or t^{-1} whenever needed to use the chosen representative endpoint. The two composites are homotopic to their respective identities, using t at the merged vertex. This also covers the case that e_1 is a loop. Therefore the fold induces an isomorphism on fundamental groups. Any basepoint adjustment in this description is a change-of-basepoint isomorphism.

The composite K -> K' -> rose, with its actual image of the basepoint, is the map taking the ith original circle to w_i. On acceptance it induces an isomorphism, so the tuple defines an automorphism. Conversely an automorphism is surjective and must pass the loop check. The recognition algorithm is correct and halts on every finite tuple.

## The finite maximum theorem

**Theorem.** There is a total recursive function B(n,L) with the exact-maximum property stated in the conclusion, conditional only on the imported algorithm A.

**Proof.** Fix integers n>=1 and L>=0. Generate the finite set W(n,L) of all freely reduced words of length at most L in X_n and its inverses. Enumerate W(n,L)^n, in any fixed computable order. There are finitely many tuples, including the nonautomorphisms. For reference, the number of words is

    |W(n,L)| = 1 + 2n * sum_{j=0}^{L-1} (2n-1)^j,

with the sum empty when L=0. For n=1 this is 2L+1. This formula is not used as an estimate for generator length.

Apply the terminating recognition algorithm to each tuple and discard every rejected tuple. Every accepted tuple represents exactly one automorphism with M(alpha)<=L, and every such automorphism appears: free reduced images uniquely determine a homomorphism. In particular the accepted list is complete, finite, and computable.

Run A on each accepted input, sequentially. It is invoked only on valid automorphisms, so every invocation halts. Freely reduce its output words. If its output basis is empty, the fixed subgroup is trivial and contributes zero. If its output basis has one member g, then g is nontrivial and generates the actual cyclic fixed subgroup, so record |g|. A basis with at least two members belongs to a noncyclic group: its first two free generators have a nontrivial commutator. Thus cardinality of the returned basis decides exactly the alternatives needed here; no separate cyclicity oracle is used.

Return the maximum of all recorded lengths and zero. There are finitely many terminating computations, so this procedure halts. It returns exactly

    B(n,L) = max({0} union
      {ell(alpha): alpha in Aut(F_n), M(alpha)<=L,
                         Fix(alpha) nontrivial cyclic}).

Both word enumeration and recognition are uniform in n, and the imported algorithm is for arbitrary finite-rank input. Hence this is a uniform algorithm for B(n,L), not merely a nonuniform selection of one function for each rank. This proves total recursiveness and the bound. The set inclusion for L<=L' also proves B(n,L)<=B(n,L').

For L=0 and n>=1 there is no automorphism in the list, and B(n,0)=0. For n=1 and L>=1 the two automorphisms are x_1 -> x_1 and x_1 -> x_1^{-1}; their fixed subgroups are respectively F_1 and trivial. Therefore B(1,L)=1 in this range. The convention for n=0 completes the proof. □

Several limits of this argument matter. Mere finiteness of the input class would give existence of a finite maximum, but not a computable maximum. Computability uses recognition and the halting basis algorithm. Enumerating fixed words until some appear would not suffice to certify that a generating list is complete, or to certify a trivial fixed subgroup. Conversely, the paper's additional recursive runtime assertion is stronger than the termination property actually needed for the argument above.

This proof describes a terminating program using the published basis algorithm as a subroutine. It does not implement that subroutine or compute numerical B(n,L) values beyond the elementary rank-zero and rank-one cases. A recursive description of the bound is not a closed-form rate estimate.

## Fixed rank and variable rank

For fixed n the answer is the one-variable recursive function B_n(L)=B(n,L). For variable n the proved maximum has two parameters. The finite enumeration above must not silently maximize over all ranks at a fixed maximum-image length L: such a union is infinite, so the same argument would not prove a rank-independent bound depending only on L. We make no claim of nonexistence of such a bound.

There is a rank-uniform bound in terms of the total number of letters in the explicit image tuple. Set

    S(alpha) = sum_i |alpha(x_i)|.

For an automorphism of positive rank, n<=S(alpha) and M(alpha)<=S(alpha). Define

    C(S) = max_{1<=r<=S} B(r,S),    C(0)=0.

This is a finite recursive maximum. If Fix(alpha) is nontrivial cyclic and S(alpha)<=S, then n<=S and ell(alpha)<=B(n,S)<=C(S). If an exact maximum for total-letter input is preferred, enumerate ranks n<=S and tuples with total length at most S, and perform the same recognition-and-basis computation; this too is finite and recursive.

An explicit finite-alphabet encoding also gives a recursive bound in its total bit length by enumerating all strings up to that length, rejecting invalid encodings and nonautomorphisms, and applying A. The encoding must include the rank, delimiters, and generator indices. It is not permissible to treat an unbounded generator index, an entire long word, or a program describing a word as a unit-cost letter and then claim the same finite-input count. The preceding total-letter bound is independently justified by n<=S, so it does not need a hidden fixed alphabet across all ranks.

## Justified changes of complexity parameter

The following comparisons are part of the authored argument; they are not attributed to the problem's undefined word “complexity.”

1. **Maximum and total forward-image lengths.** At fixed positive rank,

       M(alpha) <= S(alpha) <= n M(alpha).

   Therefore B(n,S) is a valid bound when only S(alpha)<=S is known. Conversely any bound stated using total length can be evaluated at nL when M(alpha)<=L. These inequalities preserve appropriate rate classes only after their dependence on n is specified.

2. **Including inverse images.** Let M_pm(alpha)=max(M(alpha),M(alpha^{-1})). Since M(alpha)<=M_pm(alpha), the already proved B(n,L) is a valid bound under the stronger assumption M_pm(alpha)<=L. No inverse-length estimate is needed for this direction.

   For the reverse comparison at the level of recursiveness, after recognizing an automorphism, enumerate all reduced words u until alpha(u)=x_i for each i. Such preimages exist, and substitution and free reduction decide each test. The tuple of found preimages is alpha^{-1}. This procedure is sequential and terminating on every recognized input. Thus

       J(n,L)=max({0} union {M(alpha^{-1}): M(alpha)<=L})

   is computable by the same finite input list. This proves a recursive conversion M_pm(alpha)<=max(L,J(n,L)). It proves no polynomial or exponential inverse-length comparison. If the parameter is instead the sum of forward and inverse image lengths, the corresponding elementary max/sum inequalities also apply.

3. **Word length in Aut(F_n).** Fix a specific finite symmetric generating set T for Aut(F_n), supplied by explicit basis images of its generators. Write |alpha|_T for word length and set c=max(1,max_{t in T} M(t)). For automorphisms beta,gamma, substitution and free reduction give

       M(beta composed with gamma) <= M(beta) M(gamma).

   Hence |alpha|_T<=k implies M(alpha)<=c^k, and

       ell(alpha) <= B(n,c^k)

   whenever the fixed subgroup is nontrivial cyclic. This conversion is proved; it is not a claim that the two complexity measures are linearly or polynomially equivalent.

   A recursive reverse conversion also exists: for each automorphism in the finite norm-L list, enumerate T-words in increasing length and evaluate their image tuples until that automorphism appears. Equality is decidable by free reduction of all basis images. Because T generates Aut(F_n), each search terminates, and taking their finite maximum gives a recursive bound for |alpha|_T in terms of n,L and the chosen T. No numerical rate is obtained. This paragraph assumes that T is a generating set; it does not attempt to recognize that property for an arbitrary collection of automorphisms. A uniform claim across ranks additionally requires an effective choice of T_n.

4. **Graph input and changes of basis.** A based marked graph map determines an automorphism only together with the marking and basepoint data. If a graph computation produces a based loop of m edges and a specified homomorphism back to F_n maps each traversed oriented edge, after any chosen tree collapse, to a word of length at most D, substitution bounds the resulting word length by Dm. For a loop first brought to the marking basepoint by an access path of length q in that edge encoding, the safe bound is D(m+2q). These inequalities follow by concatenation before reduction. An actual numerical application must provide those data and bounds. They cannot be discarded because a Nielsen circuit itself happens to be short.

## Why outer classes and circuits do not control based length

There is an elementary counterexample to an unqualified replacement of automorphism input by outer-class input. Work in F_2=<a,b>. For each k>=0 set

    g_k = b^k a b^{-k},
    alpha_k(w) = g_k w g_k^{-1}.

All alpha_k represent the identity outer automorphism. Nevertheless

    Fix(alpha_k) = <g_k>,     ell(alpha_k) = 2k+1.

Here is a proof of the fixed-subgroup assertion without a centralizer theorem as a hidden hypothesis. If a reduced word w is not a power of a, strip its maximal initial and terminal powers of a and write w=a^r v a^s where v is nonempty and begins and ends in b^{±1}. Then w a w^{-1}=a^r v a v^{-1} a^{-r} is freely reduced at all interfaces involving v and contains b-letters, so it cannot equal a. Therefore the centralizer of a is exactly <a>. Conjugating this equality by b^k gives the centralizer of g_k as <g_k>. The elements fixed by conjugation by g_k are exactly that centralizer.

The word g_k is reduced and has length 2k+1; its cyclic reduction is a and has length one. The only generators of <g_k> are g_k and its inverse. Thus both the outer class and the length of a representative circuit can remain constant while the length of the actual based subgroup generator tends to infinity.

This does not contradict the image-norm bound: for k>=1, direct free reduction gives M(alpha_k)=4k+3, and for k=0 it is 3. The example pinpoints information lost by passing to outer classes. It is not a lower-bound result in a new quantitative complexity class, nor an assertion that a suitably marked and based train-track input cannot support bounds.

## Inspection boundary and dependency record

The following reading supports source qualification. It does not turn the imported theorem into an independently audited theorem.

- Bestvina: PDF pages 19–21 read; page 20 visually inspected. The exact Question 12.6, editorial variant, and update were distinguished.
- Bogopolski–Maslakova v6: title and introduction read; Section 3's entire proof sketch read; Theorem 4.5 and Section 5, including the complete based-representation construction in Theorem 5.4, read; Theorem 6.1 and complete Corollaries 6.2–6.3 read; Section 20's complete finiteness/membership closing argument read. Page 3 visually inspected. The complete internal lemmas of Sections 7–19 and the external train-track and orbit-decision proofs were not re-audited.
- The inspected sketch points to a based representation, the finite core construction, and finiteness/membership decisions. Section 20 uses the perfect-path machinery of earlier sections and the auxiliary orbit results. These are dependencies inside the imported algorithm, not lemmas independently accepted by this report.
- Feighn–Handel: bibliographic first page and the complete Section 9 from its introductory purpose through Proposition 9.10 read, including Lemmas 9.1, 9.2, 9.6, 9.8, and 9.9 and their printed proofs. PDF page 58 visually inspected. Proposition 9.10 reduces to a rotationless power using Corollary 3.14, applies Lemma 9.9, and then computes the fixed subgroup of the resulting finite-order restriction via Lemma 9.2. The CT algorithm, lift algorithm in Lemma 6.4, and cited external results were not fully audited.

The elementary final reduction in that proposition can be checked directly: for K=Fix(alpha^m), alpha(K)=K and (alpha|_K)^m is the identity. Moreover Fix(alpha|_K)=Fix(alpha), since a fixed element is fixed by alpha^m. This observation alone does not supply the algorithms for finding K or solving the finite-order case. It is recorded as a checked reduction, not a substitute for their hypotheses.

The only accepted consequences beyond imported A are proved in this report: finite recognition and enumeration, exact recursive maximization, rank and encoding qualifications, the explicitly stated norm conversions, and the based-versus-outer counterexample. Reading a theorem statement and a closing reduction is not a blanket acceptance of its uninspected dependencies.

## Reproducible checks and limitations

The historical authored check program, which is not distributed in this edition, uses only the Python standard library. It tests free-word arithmetic, the finite folding recognizer, inverse certificates for every accepted tuple in a small exhaustive input class, signed permutations, and the inner-automorphism family. A determinant-one nonautomorphism is a negative control against replacing the recognizer with an abelianization test. It also checks that basing information is not lost in the example.

These are finite implementation checks of the elementary components. They do not execute source-author code, implement A, validate all cases of A, establish general numerical values of B, or upgrade a partial reading to a full proof audit. The mathematical proof of the consequence is the argument above.

## Bibliography

1. M. Bestvina, *Questions in geometric group theory*, updated problem-list PDF, Question 12.6, PDF page 20. [Retained public source](https://www.math.utah.edu/~bestvina/eprints/questions-updated.pdf).
2. O. Bogopolski and O. Maslakova, *An efficient algorithm for finding a basis of the fixed point subgroup of an automorphism of a free group*, arXiv:1204.6728v6, 15 January 2014, Theorem 1.1, page 3. [Version-specific record](https://arxiv.org/abs/1204.6728v6). The later journal item is *An algorithm for finding a basis of the fixed point subgroup of an automorphism of a free group*, International Journal of Algebra and Computation 26 (2016), no. 1, 29–67; bibliographic identification is corroborated by item [BM16] in reference 3, not by a full inspection of the journal text here.
3. M. Feighn and M. Handel, *Algorithmic constructions of relative train track maps and CTs*, Groups, Geometry, and Dynamics 12 (2018), no. 3, 1159–1238, DOI 10.4171/GGD/466. Proposition 9.10 is on printed page 1216, PDF page 58. [Publisher record](https://doi.org/10.4171/GGD/466); [retained published PDF](https://ems.press/content/serial-article-files/29889?nt=1).
