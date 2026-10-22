# Adversarial review of the submitted PR1280 mathematics

Review target: problem 30003587, original OWR2017/42 p.2621 Question 1.
Current submitted PROOF.md: 16,892 bytes, SHA-256
`ebe1dd732d78950a4ff1de041b6d9575f45ba0041025e9cc42a60cb21a4ecc99`.
Review performed 18 October 2026 UTC; exact retrieval and sealing times are in
the accompanying metadata. This is an AI mathematical review.

## Disposition and exposure

**ACCEPT the current proof as an ordinary mathematical deduction from the
identified published inputs. No mathematical repair is required.** The proof
answers the full original question, including periodic matrices and actions
with nontrivial inner kernel. It proves strong approximate innerness with
unitaries fixed by the entire original action. It proves no coherence or
approximate-representation property for those unitaries.

This is a candidate-exposed adversarial review. I read all nine submitted
files, including their historic acceptance, audit, and aggregate check claims.
Those claims were treated as untrusted and were not used as evidence of the
mathematics or as executable inputs. I wrote and executed my own check program.
I did not inspect other review directories, other agents' reports, or root's
research files. I sent status messages only to the assigning root agent.

After I had independently stated a provisional no-gap conclusion, completed
fresh primary retrievals, and run my new checks, an unsolicited root message
arrived before this report was sealed. It exposed root's no-gap conclusion,
the counts of its separate graph/phase diagnostics, and a request to check
final-paper numbering. I did not read or execute those diagnostics and do not
count them as evidence here. This late exposure prevents describing this
report as completely blind to root's conclusion. No other review family's
mathematics has been read or requested. The numbering finding below was
already present in my own inspected final PDF before that message.

## Primary mathematical body

### Exact question and input theorem

I independently acquired the official [OWR report](https://ems.press/content/serial-article-files/46706)
and visually inspected printed p.2621/PDF p.21. The opening matrix assumption
excludes zero rows and columns. The question covers finite abelian actions on
simple purely infinite Cuntz-Krieger algebras, with neither outerness nor
aperiodicity imposed. Its automorphism definition preserves the generator
span and fixes each generator's range projection. Its desired implementers
belong to the fixed algebra of the full action.

I acquired [Barlak-Szabo arXiv v3](https://arxiv.org/pdf/1708.08258v3), checked
Definition 2.5 on p.10, Corollary 2.7 on pp.13-14, and Corollary 2.8 on
pp.14-15. The first defines exactly the property used here; the corollaries
require outer actions and primitive matrix/graph presentations. The graph
result permits multiple edges and requires at least two edges. I also
independently acquired the [final published PDF](https://journals.msp.org/mscand/article/download/221/220/245)
via the [DOI](https://doi.org/10.7146/math.scand.a-114823). Final Theorems 1/2
are stated on printed p.212; their body proofs begin on pp.222/223. Final
Definition 2.5 remains on p.219. The final body does not retain corollary
numbers 2.7/2.8. The candidate explicitly attributes those numbers to v3,
so this version distinction is an optional bibliographic clarification,
not a mathematical defect.

The substantive input is used only after proving its extra hypotheses for a
new return graph and quotient action. I found no attribution of the broader
deduction to the published theorem.

### Inner diagonal automorphisms: attempted cohomology obstruction

The relevant graph has no sinks and every cycle has an exit. An exitless
cycle in a strongly connected graph would force every vertex and edge to lie
on that directed cycle. The [Conti-Hong-Szymanski paper](https://arxiv.org/pdf/1101.4210v3),
p.5, gives the diagonal MASA fact in the candidate's convention. I separately
checked [Hopenwasser-Peters-Power](https://nyjm.albany.edu/j/2005/11-18.pdf),
Theorem 5.2 on printed p.360, and the convention reversal on p.354.

If Ad(h) fixes the diagonal pointwise, h belongs to its commutant and hence
to the diagonal. For a diagonal unitary the cylinder relation gives
`h(mu x) = z_mu h(x)`. At the periodic infinite path for any closed mu,
the two arguments coincide and h is nonzero. Thus every closed path has phase
one. This tests all closed paths, with no density assumption on any selected
periodic subset needed.

For base paths theta_v from b to v, comparison after appending the same return
path gives `z_theta_s z_e = z_theta_r`. Therefore
`t_v = z_theta_v^{-1}` has `t_s conjugate(t_r) = z_e`, with the correct
orientation and sign. Normalized potentials are unique by strong connectivity.
The converse is direct conjugation by the vertex-diagonal unitary. Thus an
inner edge phase is exactly a vertex coboundary, not merely cohomologous to
an unspecified diagonal function.

For the action, the same theta_v define D_g on all of G. Because each path
phase is already a character, the D_g multiply as an exact representation and
are fixed by all alpha_h. There is no subgroup-character extension, projective
representation, or unproved splitting step. On the inner kernel K their
conjugations equal alpha_k by the just-verified classification.

The formula `beta_g = Ad(D_g*) alpha_g` is an action: alpha fixes each D_h,
and these diagonal unitaries commute and multiply. Its edge coefficient is
`chi_theta_s chi_e chi_theta_r^{-1}`. It kills K exactly. If beta_g is inner,
so is alpha_g, so the induced G/K-action is pointwise outer. This also covers
a nonfaithful original action and the trivial quotient.

### Return graph: attempted loss of corner elements or uniqueness

For graph period d, vertices in the same cyclic class can be connected by
paths of every sufficiently large length divisible by d. One direct reason
is that finitely many based closed-walk lengths have gcd d; their divided
lengths generate a numerical semigroup with finite complement. Fixed incoming
and outgoing connecting paths transfer that fact to each pair of vertices
in the class. The length-d return matrix is therefore primitive. It is the
class block of the dth adjacency power, with multiplicity, not the dth power
of the full graph incorrectly declared primitive.

A branching vertex has a predecessor path from the chosen class of length
less than d. Take either branch and extend to total length d. No sinks ensure
both extensions exist. Their edge words differ, producing two distinct return
edges. Primitivity then excludes the directed-cycle exception in the return
graph. This reasoning includes a one-vertex return graph with multiple loops.

The graph family in pAp has nonzero vertex projections and path partial
isometries. Injectivity follows from the exit-condition uniqueness theorem;
the exact theorem was inspected in the [Kumjian-Pask-Raeburn author preprint](https://documents.uow.edu.au/~dpask/index_files/papers/ckaodg.pdf),
Theorem 3.7, p.12. Its nonzero-edge hypothesis follows from
`S_mu* S_mu = p_r(mu) != 0`.

Surjectivity is the nontrivial point: a corner spanning word S_mu S_nu* has
both starts in the chosen class and equal ends. Hence the two lengths have
the same residue mod d. The same complementary-length path tau can be appended
to both, using the exact CK expansion over all tau. Each resulting path
splits into d-blocks. Vertex paths, the k=0 expansion, unequal path lengths,
and multiple return edges all obey this formula. Thus the image is the full
corner, not just its gauge-fixed subalgebra. The identification intertwines
the action because each return path is an eigenvector.

The optional edge-matrix reduction also has the right exponent: an n-step
edge transition is an (n-1)-step vertex path from r(e) to s(f). It supplies a
primitive 0-1 matrix even when the return adjacency has integer entries.

### Full frames: attempted outerness and fixed-algebra failure

For full p in a unital B, finite sums y_i z_i* with entries in Bp approximate
1. Taking one invertible sum and the row inequality from the candidate shows
YY* is positive invertible. Left normalization produces a finite frame
`sum x_i x_i* = 1` in Bp. This uses ideal fullness, not equivalence of p and 1.

For Lemma 2, putting `b_ij = x_i* x_j` gives
`u b_ij u* = sigma(b_ij)`. In the two products of
`U = sum sigma(x_i) u x_i*`, this relation reduces U*U and UU* to the frame
identity. The same computation with `x_i* a x_j` gives UaU*=sigma(a).
It remains valid for a nonorthogonal frame and does not require its members
to be sigma-fixed. Thus the invariant full corner cannot turn an outer
automorphism into an inner one.

For Lemma 3, the stronger hypothesis is correctly used: fullness in A^alpha
supplies the frame there. Hence each Gram entry is fixed and both products
of `V_n = sum x_i u_n x_i*` converge to 1. For the inverse-conjugation claim,
for each b one has

`||Ad(u_n*) b - sigma^{-1}(b)|| = ||b - Ad(u_n) sigma^{-1}(b)|| -> 0`.

This justifies the second product, even if only forward implementation was
initially given. The frame expansion then gives V_n a V_n* -> alpha_g(a).
Two-sided near-unitarity is essential in an arbitrary C*-algebra: it gives
eventual invertibility. Continuous functional calculus in the unital fixed
subalgebra supplies the polar unitary and keeps fixed membership exact. Its
distance from V_n tends to zero.

For the outer action, p is full in A by simplicity. The graph simplicity
implicitly used for the more general graph statement is standard and also
follows from exit-condition uniqueness plus propagation of a zero vertex
through a strongly connected graph. The source matrix statement assumes
simplicity explicitly. Fixed-point simplicity does not require graph
aperiodicity: it follows from the finite crossed-product averaging corner
and Kishimoto's theorem. I inspected the simple-A/pointwise-outer
specialization in [the author-uploaded original OCR](https://www.researchgate.net/publication/225983054_Outer_automorphisms_and_reduced_crossed_products_of_simpleC-algebras),
Theorem 3.1, and independently checked the fixed-point consequence on
printed p.127 of [Echterhoff-Rordam's final paper](https://ems.press/content/serial-article-files/42588).

Concretely e=|G|^{-1}sum lambda_g is a nonzero projection and
`e a e = E_alpha(a) e`. The map c -> ce from A^alpha onto the corner is
injective because the coefficient expectation sends ce to c/|G|. A nonzero
corner of the simple crossed product is simple; thus the nonzero p is full
in A^alpha. No inference from fullness in A alone is made.

### Returning to the original fixed algebra

The last exterior-equivalence step is supplied, not assumed. From
Ad(v_n)(p_v) -> p_v one obtains ||[v_n,p_v]|| -> 0. Pinching
`z_n = sum p_v v_n p_v` is norm-close to v_n and lies exactly in both
A^beta and the commutant of all vertex projections. This intersection is a
unital C*-subalgebra. Its eventual invertibility and polar functional calculus
preserve both exact memberships.

The polar unitaries w_n therefore commute with every D_h, and
`alpha_h(w_n) = D_h beta_h(w_n) D_h* = w_n` for every h in G.
Also D_g itself is alpha-fixed. Thus D_g w_n is fixed by the whole original
action and implements alpha_g asymptotically. These are separate implementing
sequences for each g; no multiplication relation across g is used or obtained.

### Exact matrix presentation and boundary cases

Range-fixing in the original definition makes alpha_g(s_i) a scalar multiple
of s_i: multiplying its span expansion by p_j for j != i kills all other
coefficients, since each s_j is nonzero. Norm preservation makes the scalar
unimodular and the action law makes it a character.

For T_ij=s_i p_j, direct multiplication gives
`T_ij* T_kl = 0` for distinct edges, `T_ij* T_ij = p_j`, and outgoing ranges
sum to p_i. Conversely sums of outgoing T_ij satisfy the CK relations:
cross terms in s_i s_i* vanish through the orthogonal right supports p_j.
The two formulas undo one another. This is an actual equivariant isomorphism.

No zero columns is used essentially. If the finite component graph is
nontrivial, a source component contains a cycle because all its vertices have
an incoming edge within it. Choose a distinct terminal component. Saturation
of the latter's hereditary set cannot absorb that cycle: each cycle vertex
continues to emit to the next outside vertex. This gives a nonzero proper
ideal, contrary to simplicity. The resulting strongly connected graph cannot
be a directed cycle; its algebra would be a matrix algebra over C(T).

The trivial group, entirely inner actions, nonfaithful actions, period one,
period greater than one, a one-vertex multiloop return graph, and path length
zero were all checked in the argument. The one-vertex original 0-1 matrix
[1] cannot satisfy the simple purely infinite hypothesis. Empty/zero-algebra
conventions do not arise under the standard nonzero-simple convention.

## Independently authored finite checks

`checks.py` imports no candidate program and contains no assert statements.
Every validation raises an explicit RuntimeError, and a deliberate false
sentinel is caught in every run. Normal, -O, and -OO executions produce
byte-identical JSON, as recorded in REPRODUCIBILITY.json.

The graph universe contains every adjacency array with entries 0,1,2 on
one to three vertices: 19,767 arrays, including 16,122 with no zero rows or
columns. Among them, 4,852 reducible cases have a proper terminal hereditary
saturation, and 11,266 are strongly connected noncycles, including 65 periodic
cases. Two period computations are compared: distance differences and simple
cycle lengths. Explicit return paths (113,630 counted) are compared with the
appropriate matrix-power block and its finite primitivity test. This tests
multigraphs as well as 0-1 graphs.

Four explicit graphs are tested with groups Z2, Z3, Z4, Z2xZ2, Z2xZ3,
Z2xZ4. Across 18,148 edge-character labelings (17,060 for product groups),
129,492 element checks compare the directed-cycle criterion against an
independently enumerated set of normalized vertex potentials. They also
check the fixed-path sign, equality of the inner kernel to the untwisting
kernel, and absence of an inner element outside that kernel. There are
201,328 explicit quotient-descent comparisons. Product groups are not
assumed cyclic by the code, even in the Z2xZ3 case.

Three periodic examples, including a period-three graph and parallel edges,
supply 228 corner spanning pairs and 237 common extensions; the check
validates the residues and each d-block's composability and endpoints.
These finite word checks support the CK expansion argument, but do not
prove that analytic expansion or uniqueness numerically.

The mixed-kernel witness in CHECK_RESULTS.json is the two-vertex complete
0-1 graph with a Z4 action whose loop labels are 0 and cross-edge labels are
1. Its element 2 acts nontrivially by the vertex coboundary, while elements
1 and 3 have nonzero cycle obstruction. This exercises a genuinely nontrivial
inner automorphism inside an action with an outer quotient.

All checks pass. They are falsifiable finite diagnostics; the all-size graph,
MASA, corner, and approximation arguments above remain the mathematical proof.

## Metadata and historical claims, separate from mathematics

All current files listed by the submitted manifest match their claimed byte
counts and hashes. Every current output replacement span and every protected
current mathematical region matches its recorded hash. Those are byte
integrity findings only, recorded in PACKET_METADATA_CHECKS.json.

The older proof, audit, and supplement bytes named in ACCEPTANCE.json are not
present in the assigned submitted directory. I did not retrieve them from
other research folders. Consequently I cannot independently authenticate the
claimed editorial preservation against those older inputs or the earlier
audit's execution history. The current mathematical verdict does not rely
on those unavailable bytes or on any historic check count.

## Source limits and remaining gap

No mathematical gap was found in the stated deduction. The remaining
external dependency is the cited Barlak-Szabo theorem and the standard graph
and crossed-product background identified above. This audit does not reprove
those published results, formally certify the proof, or establish novelty,
priority, or human peer-review acceptance. The bounded search in the literal
query ledger is not a literature-completeness claim.

Fresh acquired PDFs and extracted text remain solely in `_local`. No source
documents, page images, provider excerpts, or provider search-result text are
part of the public authored output manifest. The Kishimoto original was
inspected through author-uploaded OCR, not through an acquired original PDF;
its DOI open failed in the web tool. The exact needed fixed-point fact was
also inspected in the final primary Echterhoff-Rordam PDF. A web screenshot
of the official OWR PDF timed out; fresh local acquisition, text extraction,
rendering, and visual inspection of the same page succeeded.

No candidate edit, branch/index change, commit, push, publication, or
communication with an external individual was performed. This directory is
the only place in the workspace to which this reviewer wrote.
