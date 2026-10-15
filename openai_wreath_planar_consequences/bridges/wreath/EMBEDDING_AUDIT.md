# Embedding and original-source audit

Checkpoint: 2026-10-06 PDT (2026-10-07 UTC). The independent algebraic bridge
is complete; this audit does not establish OpenAI's group-ring premise.

## Original problem and PR packet

PR389 head was freshly retrieved as
`fcb661d172c182d0437a07c3714ad4e113278d3b`. Its exact input is the standard
restricted regular wreath-product Hopficity question for two finitely
generated Hopfian factors. Its SOURCE_SCOPE.md, FINAL_RESULT.md, REVIEW.md,
REVIEWED_DISPOSITION.md, source/publication manifests, and all five TURN files
were retrieved at that immutable head; hashes are in
pr389_source_receipt.json. The review accepts scoped partial results and
retains the original problem as unsolved. Nothing in that status prevents
using its mathematical packet as research input.

The relevant pinned QUEUE entry is rank 415, problem 2531 / KOU-21.22,
status unsolved, turns 5/5. No unrelated queue rows were analyzed. The full
queue was fetched only to bind the exact source version and select this row;
its ignored local copy is not a deliverable.

PR389 turn 4 already displays the hypothetical matrix-defect wreath map and
credits Bradford--Fournier-Facio. Its nonabelian direct-factor extension does
not produce an actual forbidden group-ring pair. The PR packet neither
settles the question nor proves the new imported premise. Its assertion
that finite-ring computations do not supply an infinite group-ring defect
is correct. The prior independent review explicitly distinguishes the
nonfree permutational example of Kochloukova from the regular action here.

The old notebook URL ending 21tkt.pdf now returns 404. The editors' live
October 6, 2026 update-2 page instead links 21tkt-1.pdf and 21upd-1.pdf.
Both new files were retrieved and hashed (literature_source_receipt.json).
Page 180 was independently extracted, rendered and visually inspected.
Problem 21.22 retains the original standard-restricted formulation, credits
Bradford and Fournier-Facio, and has neither a solved asterisk nor an
unverified-AI marker. The update-only document contains no 21.22 entry.
Absence of a notebook marker is a source-state observation, not proof of
historical priority or absence of a later solution.

## Bradford--Fournier-Facio

Source: *Hopfian wreath products and the stable finiteness conjecture*,
Mathematische Zeitschrift 308 (2024), Paper 58, DOI
10.1007/s00209-024-03589-3, published PDF at
https://d-nb.info/1355447615/34 . Its 470979 bytes freshly matched SHA256
15e658ecaa49b8f6189527beec84df038086a357226fff4bee743851e0daebdf,
also matching PR389's source manifest. PDF pages 2--3, 5--6, and 18--22 were
read for statements, convention, and the relevant construction.

- Definition 2.1 uses finite-support functions and left translation by H;
  this matches PROOF.md exactly.
- Theorem 1.3/4.11 gives the universal equivalence with direct finiteness.
  The last sentence of its proof uses Miller--Schupp [39] specifically for
  the embedding of a finitely generated group in a finitely generated
  Hopfian group.
- Theorem 1.5 has a maximum multiplicity for each prime-power layer, not a
  sum. At A=C_2 it asks for direct finiteness of F_2[H], together with
  Hopficity of H. No field-change or matrix-size reduction is needed for
  our scalar characteristic-two defect.
- Theorem 4.2's counterexample direction uses a surjective noninjective
  left R-module map, extended by the identity on H. That direction is
  exactly the independently written bridge and is elementary.
- The reverse direction of the full criterion requires their earlier
  basicity and relabeling results. Our explicit negative construction does
  not depend on that reverse direction. The hypothesis qualification on
  their Proposition 2.15 noted in PR389's review is therefore not imported
  into the proof above.

Status: exact relevant statements and the counterexample construction
checked. No new mathematical concern was found in the construction.
Not every theorem of the paper was independently reproved, and none of
its statements establishes a group-ring counterexample.

## The original Miller--Schupp input

Bibliography: C. F. Miller III and P. E. Schupp, *Embeddings into Hopfian
groups*, Journal of Algebra 17 (1971), 171--176, DOI
10.1016/0021-8693(71)90028-7. Bradford--Fournier-Facio cite the embedding
statement directly. Bridson--Short's 2024 introduction additionally
describes the original construction as a small-cancellation quotient of
G * U(p,q), with U(p,q) a free product of finite cyclic groups. It produces
finitely generated Hopfian complete overgroups and can introduce torsion.

The original primary paper's ScienceDirect article/PDF and Elsevier API
URLs were attempted; access failed (403 or unavailable). Therefore this
audit **has not read or reconstructed the original 1971 proof**. It must
not be described as an independent full validation of its small-
cancellation presentation, its torsion-order rigidity, or every embedding
claim. This is a retrieval/coverage limitation. The theorem is a long-
established published input, and an independently published alternative
with an accessible full proof is available below. No individual was
contacted to obtain the paper.

## Accessible independent embedding route

Source: M. R. Bridson and H. Short, *Complete embeddings of groups*,
Bulletin of the Australian Mathematical Society 110 (2024), 136--144, DOI
10.1017/S0004972723001442. Published full PDF:
https://www.cambridge.org/core/services/aop-cambridge-core/content/view/FF2C38C907DC9FDF75BE27869011A6D9/S0004972723001442a.pdf/complete-embeddings-of-groups.pdf .
The retrieved 266956 bytes have SHA256
fbf74f6015f6dd7b06d99d978b68a47afcec42b242a21da61db09217c8d8a06f.

Theorem A embeds every countable group into a finitely generated Hopfian
complete group. This applies immediately to finitely generated G.
Theorem A's additional preservation conclusions are not required or
claimed for our wreath theorem. The accessible proof was read, with focus
on Corollary 2.2, Lemmas 2.3/4.2, and Proposition 5.1.

Its mechanism differs from Miller--Schupp: enlarge G by free products so
the intermediate group Gamma is generated by free subgroups F_1,F_2 with
noncyclic intersection K and trivial centralizer of K. Attach rigid
hyperbolic 3-manifold groups A_1,A_2 by amalgamating malnormal free
subgroups L_i<A_i with F_i. Normal-form embeddings preserve the original
G. The next lemma independently spells out the epimorphism rigidity
needed here and exposes each premise instead of assuming Gamma Hopfian.

### Audited rigidity lemma

Suppose Gamma=<F_1,F_2>, where each F_i is a finitely generated nonabelian
free group and the centralizer of K=F_1 intersect F_2 in Gamma is trivial.
Suppose A_1,A_2 are finitely generated nonisomorphic groups satisfying:

1. each A_i has property FA (every action on a simplicial tree fixes a
   vertex), trivial center, and only inner automorphisms;
2. every nontrivial self-homomorphism of A_i is an automorphism;
3. each contains a malnormal subgroup L_i isomorphic to F_i;
4. each quotient Q_i=A_i/normal-closure(L_i) is nontrivial.

Form H=A_1 *_{F_1=L_1} Gamma *_{F_2=L_2} A_2. The amalgam normal form makes
all three vertex groups injective, and H=<A_1,A_2> because
Gamma=<F_1,F_2>. Hence H is finitely generated and contains Gamma.

Let phi:H->H be onto. Each phi(A_i) fixes a vertex of the Bass--Serre tree,
because it is an image of a group with FA, so it is contained in a conjugate
of A_1, Gamma, or A_2. Killing Gamma and A_2 gives the nontrivial quotient
Q_1, and killing Gamma and A_1 gives Q_2. If neither of the two containing
vertices has type A_j, both images are killed in Q_j and cannot generate
H. Thus their types are A_1,A_2 in some order. In particular the images of
both A_i are nontrivial. Applying the same argument to phi^2 shows its two
images are nontrivial; the type permutation squares to the identity, so
phi^2(A_i) is contained in a conjugate of A_i. Premise 2, after conjugating
back, makes phi^2 restricted to A_i an isomorphism onto that whole
conjugate. Consequently phi restricted to A_i is injective. If phi
exchanged the two types, injectivity on A_j together with surjectivity of
the composition on A_i forces phi(A_i) to equal the whole containing
conjugate of A_j. That would give A_1 isomorphic to A_2, a contradiction.
Therefore phi maps each A_i isomorphically onto a conjugate of itself.

After composing phi with an inner automorphism of H, premise 1 makes phi
the identity on A_1. The restriction to A_2 is conjugation by some c in H.
Because K is contained in both A_1 and A_2, c centralizes K. Malnormality
of L_i in A_i implies that any arc of length three in the Bass--Serre tree
has trivial stabilizer: it contains two distinct edges meeting at an
A_i-vertex. The subtree fixed by nontrivial K contains the length-two
path from A_1 through Gamma to A_2 and has diameter exactly two, with
unique center the Gamma-vertex. Every centralizer of K fixes that center,
so c belongs to Gamma. Its centralizer there is trivial by hypothesis,
so c=1. Both restrictions of phi are now the identity. Since A_1,A_2
generate H, phi is the identity. Undoing the conjugation proves that every
epimorphism of H is an inner automorphism, hence H is Hopfian.

### Existence-premise coverage

The published preparation of Gamma uses free-product normal forms; no
assumption on Hopficity of G is present. The A_i are nonisomorphic
fundamental groups of asymmetric, non-Haken, closed hyperbolic
3-manifolds. Their FA follows from the non-Haken condition. The
malnormal free subgroups with nontrivial quotient come from the cited
hyperbolic-subgroup construction. Lemma 4.2 proves premise 2 from finite
abelianization: compact-core homology excludes nontrivial infinite-index
images; the cited finite-index-image injectivity theorem and Mostow
rigidity exclude proper finite-index images.

The centralizer, type-permutation, possible trivial-image, and
surjectivity steps in Proposition 5.1 were checked independently as
above. FA is essential for an epimorphism, because lack of a free
splitting only controls injective images and would not suffice before
injectivity is known. No such confusion is present in Proposition 5.1.

Status: full accessible embedding proof inspected and its group-theoretic
rigidity mechanism reproduced with explicit hypotheses. Deep published
geometric and hyperbolic inputs (Mostow rigidity, compact cores,
non-Haken asymmetric manifold existence, malnormal subgroup existence,
finite-index-image injectivity) remain standard cited dependencies; the
knot-census computations were not independently rerun in this subaudit.
No substantive concern was found in this alternative route. This route
can replace an inaccessible original proof; it does not replace or repair
the unvalidated central OpenAI group-ring theorem.

## Promotion boundary

The bridge proof can be retained unconditionally as an implication using
established embedding theorems. It does not justify publishing Target A
as an unconditional existence theorem until an actual group-ring defect
passes the separate central audit. No formal proof-assistant artifact is
claimed. No external outreach occurred.
