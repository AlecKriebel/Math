# Fresh independent adversarial review of the integrated candidate

Review checkpoint: **2026-10-24 18:49 UTC**. Review-task completion: **100%**.
Best-guess completion toward a verified original resolution: **75%**, because
primary target scope and extensive priority remain separate tasks. This report
does not assign `solved_verified` or certify originality.

## Verdict and scope

**Qualified mathematical pass.** I found no substantive mathematical objection
to the integrated construction. With the precise definitions supplied in
`PROBLEM.md`, and AAJZ Theorem 4.3's first clause as the external embedding
input, the proposed conclusion follows for every prime p. In particular, the
construction produces an embedding, which is stronger than the epimorphism
from a subgroup requested by the supplied formulation of 21.131.

This is a fresh reconstruction, not an adoption of previous reviewers' verdicts.
I read the two complete component proofs and the integration note, but treated
their acceptance claims as irrelevant to mathematical validity. I independently
checked the actual AAJZ primary statement. I have not independently settled the
original Notebook definition or the 1986 PDF scope; the parent assigned those
to a separate fresh reviewer. The present conclusion is explicitly conditional
on the supplied exact original-AT and literal-Golod definitions. No result here
establishes priority, residual finiteness, a homogeneous ideal, or a finitely
generated AT target.

## 1. Tree target reconstructed

Number coordinates from zero and let v_n=0^(n-1)1, n>=1. These vertices form an
antichain: for n<m, the length-n prefix of v_m is 0^n, whereas v_n ends in 1.
The rooted p-cycles supported immediately below them therefore commute and
have disjoint supports as permutations of tree vertices. A portrait assigning
one such cycle at each v_n of label i defines a legitimate tree automorphism
d_i. An infinite portrait causes no convergence issue: its restriction to each
finite tree is a compatible finite portrait.

Each d_i fixes 0-infinity. If the first nonzero coordinate of a tuple is j,
then it lies below a portrait vertex only when that coordinate is 1; the only
possible such vertex is v_(j+1). The only changed coordinate is then j+1,
provided it exists and its label is i. Thus d_i is a mutation changing at most
one coordinate of each tuple and has the exact prescribed longitudinal
geometry. Every label occurs in every sufficiently long row of the enumeration,
so d_i changes infinitely many levels. Distinct labels give independent
commuting order-p elements, since one may inspect a portrait vertex with each
label. In particular D is a countable set of nonidentity original longitudinal
mutations, and the target is already infinite from this independence.

The root subgroup <a> has accompanying group C_p. At every positive level n,
d_(i(n)) supplies the p-cycle at the off-ray symbol 1; all other accompanying
permutations are identities or that same cycle. The accompanying group is
exactly C_p, hence transitive. The supplied original AT definition therefore
applies. This includes p=2; its sole off-ray symbol is precisely 1.

For local finiteness, fix a finite label set I and choose N with i(N) outside I.
At depth N a chosen d_i has its infinite tail only at 0^N. The possible rooted
cycle at the other vertex v_N is absent because i(N) is outside I. Portraits at
smaller depths affect the finite top action but have trivial depth-N sections.
Portraits at greater depths all lie below 0^N. Consequently every depth-N
section of each selected generator is either identity or
t_i=d_i restricted to 0^N. The tails t_i again have disjoint antichain supports,
so B_N=<t_i:i in I> is a finite elementary abelian group.

The set of automorphisms with finite top action in Wr_N(C_p) and all depth-N
sections in B_N is the subgroup B_N^(p^N) semidirect Wr_N(C_p): the top action
only permutes the coordinates of the base. It is closed under both products
and inverses. Thus H_I embeds in this finite p-group. The faithful wreath
decomposition is an injection, since trivial top action and trivial sections
give the identity on every vertex. Every finite subset of H belongs to one
H_I, so H is countable, locally finite, infinite, and a p-group.

The antichain and common-zero conditions are essential, and are actually
satisfied. Local finiteness has not been inferred from finite truncations.
The assertion of unbounded level-transitive orbits also checks out, but is not
needed to prove infinitude because D is already independent.

## 2. Derived-subgroup overgroup and convention audit

For the constructed H use K=H^p semidirect <t>, with t of order p. A finite
set of coordinate values in H lies in a finite p-subgroup P. Therefore a finite
subset of K lies in P^p semidirect C_p. This proves local finiteness and the
p-group assertion without assuming finite generation of H.

Use the tree note's convention [x,y]_- = x^-1 y^-1 x y and orient t by
t^-1 (x_0,...,x_(p-1)) t=(x_1,...,x_(p-1),x_0). For h^p=1 set
w=(1,h,...,h^(p-1)). Then

    [w,t]_- = w^-1 (t^-1 w t) = (h,...,h).

At the wraparound coordinate the exponent difference is -(p-1), which is 1
modulo p. The diagonal map Delta is a homomorphism for noncommutative H too,
because multiplication is coordinatewise. Since a and every d_i have order p,
their diagonal images lie in K'; generation then gives Delta(H)<=K'. The proof
does not need, and does not claim, that every element of H has order p.

The algebra note's general proposition uses the opposite commutator convention
[x,y]_+=xyx^-1y^-1, explicitly stated there. Its direct-limit argument is also
valid: for an element h of order p^a choose a later cyclic wreath length m
divisible by p^a, and write f(i)=h^i. Then
f(i)f(i-1)^-1=h at every coordinate, including wraparound. The diagonal
identifications are injective homomorphisms and preserve orders. Thus every
element of the direct limit belongs to its derived subgroup. The switch in
commutator notation between the two notes is harmless, because the actual
formulas in each convention are correct and both generate the same derived
subgroup. No convention is silently needed to match the integration maps.

## 3. Augmentation algebra, stable nil, and unitalization

Let A be the augmentation ideal of F_p[K]. The finitely many group elements
supporting any finite subset of A lie in a finite p-subgroup P of K. Each of
these algebra elements has coefficient sum zero, so belongs to the augmentation
ideal A_P of F_p[P], not merely to the whole finite group algebra.

Here is the nilpotence argument independently checked. For nontrivial P choose
a central z of order p. The central ideal J=(z-1)F_p[P] satisfies J^p=0 in
characteristic p. The quotient by J identifies exactly the cosets modulo
<z>, hence is F_p[P/<z>]. By induction, if its augmentation ideal has power q
equal to zero, then A_P^q is contained in J, and A_P^(pq) is zero. The trivial
group begins the induction. Thus A is locally nilpotent and countable
dimensional. For a finite matrix over A, all entries lie in one A_P, and a
matrix power at least the nilpotence exponent of A_P is zero. This proves
stable nil directly and avoids the generally invalid inference that a matrix
algebra over an arbitrary nil algebra is automatically nil.

The map k |-> 1+(k-1) embeds K into the adjoint group of A because F_p[K] has
the group elements as an independent basis. More precisely, its unitalization
is F_p direct-sum A, identified with F_p[K] by (lambda,a) |-> lambda*1+a;
augmentation proves that this vector-space decomposition is direct.

AAJZ Theorem 4.3's first clause embeds a countable-dimensional stable nil
algebra into a finitely generated stable nil algebra over the same field.
All hypotheses have now been proved. The stable-nil conclusion, rather than
the weaker conclusion of its second clause, is indispensable below.

If phi:A->B is this algebra embedding, the map
(lambda,a) |-> (lambda,phi(a)) between formal unitalizations is injective.
It induces the group embedding K->U=1+B. Its restriction carries Delta(H)
into U', because homomorphisms carry commutators to commutators. There is no
requirement that the image of K already lie in the finitely generated canonical
unit subgroup of B; the next two steps supply that missing property.

## 4. Finite generation of the required elementary group

Put R=F_p direct-sum B and let s_1,...,s_d generate B as a nonunital algebra.
For each ordered pair i!=j in {1,2,3}, include e_ij(s_l) in X. Simultaneous
induction over monomial length, for every ordered pair, gives all e_ij(w):
write a monomial as w=v*s_l and choose the third index k, then use

    [e_ik(v),e_kj(s_l)]_+ = e_ij(v*s_l).

This identity holds over a noncommutative associative ring; the order of its
coefficients is exactly v*s_l. Addition of entries and integral powers give
all F_p-linear combinations, so <X> contains every e_ij(b), b in B.
Each e_ij(lambda+b) factors as e_ij(lambda)e_ij(b); hence
E_3(R)=<Q,X> with Q=E_3(F_p).

Q is a subgroup of the finite group GL_3(F_p). Let L be generated by qxq^-1
for all q in Q and x in X. This is a finite set. Conjugation by any element
of Q permutes this entire generating set, so Q normalizes L. L normalizes
itself, and E_3(R)=<Q,L>, proving that L is normal in E_3(R). It contains
<X>, hence every e_ij(b). Conversely each displayed generator is an
E_3(R)-conjugate of such an elementary matrix. These two inclusions establish
exactly the claimed normal closure E_3(R,B).

This step neither identifies L with an entire congruence kernel nor invokes
an unstated relative elementary-group theorem. Three indices and the finite
prime field are being used in the places the argument requires them.

## 5. Exact unit-derived-subgroup embedding

For every u in U its inverse lies in 1+B by a finite geometric series. Direct
multiplication, with the coefficient order retained, gives

    e12(u)e21(-u^-1)e12(u) = [[0,u],[-u^-1,0]]

in the leading block. Multiplying by the value of this block at u=-1,
namely e12(-1)e21(1)e12(-1), yields diag(u,u^-1,1)=D(u).

For b in B, e_ij(lambda+b) and e_ij(lambda) have the same coset modulo L.
All factors in the six-factor formula for D(u) therefore reduce to their
u=1 values in E_3(R)/L. Their product is identity, proving D(u) is in L.

The defect of multiplicativity is exactly

    D(u)D(v)D(uv)^-1 = diag(1,u^-1 v^-1 u v,1).

In particular, the inverse in the first entry of D(uv)^-1 is v^-1 u^-1,
not u^-1 v^-1. There is no commutativity assumption. The map
j:U->GL_3(R), h |-> diag(1,h,1), is an injective homomorphism. The identity
shows that it sends each commutator in U into L. Products and inverses of
these images give j(U')<=L. This proves the needed restriction is an embedding.
The proof never treats u |-> D(u) as a homomorphism.

## 6. Literal canonical Golod group and final maps

Write the finite generators of L as I_3+c_j, and let C be the nonunital
F_p-algebra generated by these c_j inside M_3(B). Each entry of c_j lies in
B. Since B is stable nil, every element of M_3(B), hence of C, is nilpotent.
Consequently 1+C is a group, with inverse given by the finite geometric
series for each element. The displayed generators generate precisely L in
this group.

The identification between the formal unitalization of C and its matrix
realization is injective: the scalar diagonal entries are in F_p and the
entries of C lie in the disjoint summand B of R. No collapse of the unit or
of C is possible. Also c_j=q(s_l E_ij)q^-1, so c_j^2=0. In particular every
nonidentity displayed generator has order exactly p, including when p=2.

The complete embedding is

    H --Delta--> K' --> (1+A)' --> U' --j--> L = G <= 1+C.

Every arrow is an injective homomorphism. In particular G contains infinite
H. If C were nilpotent, say C^m=0, all words of lengths 1,...,m-1 in its
finite algebra-generating list would span C. This would make C finite
dimensional and, since the field is finite, a finite set. Then G<=1+C would
be finite, a contradiction. Thus C is nil and nonnilpotent.

Delete identity entries and repetitions from the finite generating list.
This does not change G or the algebra generated by the differences. Every
element of 1+C has p-power order because for large e,
(1+c)^(p^e)=1+c^(p^e)=1. If the remaining list had at most one entry, G
would be finite cyclic, contradicting its infinite subgroup. Thus r>=2.
The free nonunital algebra F_p<x_1,...,x_r>_+ maps onto C by x_i |-> c_i,
and its kernel is an ideal I. This supplies precisely the required literal
presentation C=F/I and the canonical group generated by the images of 1+x_i.

Let S be the image of H under the displayed composite. The inverse of that
composite on S is an isomorphism S->H, hence is a surjective homomorphism.
Its kernel is trivial. This completes the supplied existential target; no
property of a preassigned Golod group has been asserted.

## 7. Independent computation and exact remaining qualifications

`independent_checks.py` does not import the component evaluators. It made
348,516 exact tree-word section comparisons over p=2,3,5, including words
with inverses and noninitial finite label sets. It separately detected the
false common-zero variant. Over the noncommutative seven-dimensional unital
algebra F_p<x,y>/(degree>=3), it made 1,172 named exact assertions per prime,
3,516 total, covering elementary multiplication, factorization, diagonal
defect, actual diagonal homomorphism, constant conjugation, and nil matrix
powers. It detected that D is not a homomorphism. Results and input hashes
are retained in `independent_results.json`. These computations supplement,
and do not substitute for, the universal arguments above.

The supplied root reproduction result was read as supplementary evidence
only; its reported successes were not used as proof premises.

AAJZ source verification was fresh via the primary author PDF at
<https://arxiv.org/pdf/1703.08734>, version 2, 3 April 2017: theorem on printed
p.2, proof on printed p.18 (with preparations on pp.16-17). Local PDF SHA-256:
`d0a57570ceeed1b960ee1a146acbed8a82e95b9cc3211b7295da55831186d369`.

**Exact remaining gap in this review's certification:** the construction is
mathematically sufficient under the supplied original definitions, but this
review alone has not certified the literal primary target scope or absence of
earlier equivalent results. These are source and priority questions, not a
new unsupported mathematical lemma replacing the central difficulty. I found
no blocked mathematical route in the presented integration. No publication or
originality status should be inferred from this pass.
