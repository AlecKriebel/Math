# Algebraic obstruction audit for Kourovka 21.144

Scope: standard Thompson group F of finite dyadic piecewise linear maps. No claim of a counterexample or proof of the dichotomy. These are deductions from existing structure theorems; no novelty claim is made. Work and communication stayed within the research team; no outside individual was contacted.

## Research checkpoints

- 2026-10-17 20:59:51 UTC: started an independent audit of residual properties, simple and perfect subgroups, growth, and identities. Estimated completion toward resolving 21.144: 5%; completion of this route audit: 5%.
- 2026-10-17 21:02:18 UTC: found and checked the obstruction that a residually finite subgroup of PL_+(I) must be solvable, using Bleak's universal W and an explicit finite quotient argument for W_3. Estimated completion toward resolving 21.144: 5%; route audit: 65%. This removes a candidate family rather than constructing a counterexample.
- 2026-10-17 21:02:58 UTC: checked a stronger residual solvability obstruction using the finite generation theorem of Bleak–Brough–Hermiller and a direct commutator calculation in an ascending wreath limit. Estimated completion toward resolving 21.144: 5%; route audit: 90%, pending adversarial confirmation of that combination.
- 2026-10-17 21:04:25 UTC: independent parent audit confirmed the commutator identity, the natural base inclusions in the explicitly defined subgroup of B, passage of derived subgroups through the increasing union, and the residual solvability corollary. Replaced dissertation-only sourcing by published Bleak and Bleak–Brough–Hermiller results. Estimated completion toward resolving 21.144: 5%; completion of this bounded obstruction audit: 100%. No solution or novel-result claim.

## Exact target and notation

A negative answer requires an embedding H <= F, a proof that H is not elementary amenable, and a proof that H contains no subgroup isomorphic to F. An abstract non-elementary amenable group satisfying a forbidden-F certificate is insufficient without the embedding.

Write A wr Z for the standard restricted wreath product (direct sum of copies of A, indexed by Z, with the shift). Define

\[
W_0=1,\qquad W_{n+1}=W_n\wr\mathbb Z,\qquad
W=\bigoplus_{n\geq1}W_n.
\]

Thus W_1=Z, W_2=Z wr Z, and W_3=(Z wr Z) wr Z. Distinguish W from

\[
L=\bigcup_{n\geq1}W_n,
\]

where each inclusion W_n -> W_{n+1} places W_n in the coordinate-zero copy of the base. This L is the left-associated infinite wreath product denoted (Z wr)^infinity by Brin and Bleak. Both W and L are locally solvable and elementary amenable, but their residual behavior differs.

## Structure theorems used

The following exact inputs were checked in primary sources.

1. Every nonsolvable subgroup of PL_+(I), without a finite generation assumption, contains W. This is Theorem 1.1 of [Bleak, *A minimal non-solvable group of homeomorphisms*](https://ems.press/journals/ggd/articles/1916), *Groups Geom. Dyn.* 3 (2009), 1–37, DOI 10.4171/GGD/50. The [arXiv manuscript](https://arxiv.org/pdf/math/0608182), printed pp. 2–3, defines W_n and states the theorem.
2. The Brin–Navas group B contains L with exactly the standard base inclusions required here. In Section 1.2.4 of [Bleak's manuscript](https://arxiv.org/pdf/math/0608182), printed pp. 6–7, beta_i=beta_0^(alpha^i), the support of beta_(i−1) is in a fundamental domain of beta_i, and <beta_0,...,beta_(n−1)> is W_n. Adding beta_n adds the outer shift, placing the preceding W_n in a single bottom coordinate. The union of these subgroups is L. This avoids inferring a direct limit merely from abstract embeddings of finite W_n.
3. Every finitely generated nonsolvable subgroup of PL_+(I) contains B. This is Corollary 1.1 in the [arXiv version of Bleak–Brough–Hermiller](https://arxiv.org/pdf/1507.06908), printed p. 3. Its Theorem 3.2 proves the equivalent transition-chain condition. Published: *Transactions of the AMS* 374 (2021), 6815–6837, [DOI](https://doi.org/10.1090/tran/8421); [accepted manuscript](https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/21656/infiniteDescent33.pdf?isAllowed=y&sequence=1).

Consequently every finitely generated nonsolvable subgroup of PL_+(I) contains L. The finite generation hypothesis in this consequence is essential; W is a nonsolvable locally solvable example.

## Proposition 1: residual finiteness forces solvability

**Claim.** Every residually finite subgroup H of PL_+(I), in particular of F, is solvable. No finite generation assumption is needed.

**Explicit wreath obstruction.** Let A be any nonabelian group and B=A wr <t>. Denote its coordinate-j base subgroup by A_j, with A_j=A_0^{t^j}. For any homomorphism phi:B -> Q to a finite group, choose m>0 with phi(t)^m=1. For every a in A_0,

\[
\phi(a^{t^m})=\phi(a).
\]

Therefore phi(A_m)=phi(A_0). The distinct base subgroups A_0 and A_m commute elementwise, so phi(A_0) is abelian. In particular

\[
1\ne A_0'\ \leq\ \bigcap_{\phi:B\to Q,\ Q\text{ finite}}\ker\phi.
\]

Thus A wr Z is not residually finite whenever A is nonabelian. Taking A=W_2 proves W_3 is not residually finite. This proof needs neither finite generation of A nor a pre-existing wreath-product residual finiteness theorem.

**Conclusion.** If H were nonsolvable, structure input 1 would embed W_3 <= W <= H. Residual finiteness passes to subgroups, contradicting the calculation. Hence H is solvable and therefore elementary amenable.

**Candidate consequence.** A non-elementary amenable group faithfully acting on a locally finite rooted tree cannot embed in PL_+(I): its action on finite levels makes it residually finite. This excludes such automaton groups even when they are torsion free, orderable, or amenable. It also applies to every residually finite candidate obtained by a different mechanism. This is stronger than the elementary observation that residual finiteness excludes an embedded F.

**Independent adversarial check.** At 2026-10-17 21:02 UTC the parent agent independently checked the finite quotient calculation, the W_3 indexing, inheritance of residual finiteness, and the absence of a finite generation hypothesis in structure input 1; no gap was found.

## Proposition 2: residual solvability forces local solvability and elementary amenability

First, an algebraic calculation gives a perfect subgroup in L.

**Wreath commutator lemma.** In B=A wr <t>, the coordinate-zero copy of A' is contained in B''. Set x_j=x_0^{t^j} and y_j=y_0^{t^j}. With [a,b]=a^{-1}b^{-1}ab, the elements

\[
u=x_0x_1^{-1}=[x_0^{-1},t],\qquad
v=y_0y_2^{-1}=[y_0^{-1},t^2]
\]

belong to B'. Since different base coordinates commute,

\[
[u,v]=[x_0,y_0].
\]

The commutators [x_0,y_0] generate A_0', proving A_0' <= B''.

Apply this to each W_n <= W_{n+1}. It yields W_n' <= W_{n+1}''. Derived subgroups commute with increasing unions: every commutator, and every finite product of commutators, uses elements from some one stage. Hence

\[
L'=\bigcup_nW_n'
\ \leq\ \bigcup_nW_{n+1}''=L''\ \leq\ L'.
\]

Therefore L'=L'' is perfect. It is nontrivial because W_2 is nonabelian.

**Claim.** If H <= PL_+(I) has no nontrivial perfect subgroup, then H is locally solvable and elementary amenable.

**Proof.** Every finitely generated K <= H is solvable: otherwise structure inputs 2 and 3 embed L, and therefore its nontrivial perfect subgroup L', in K. Since H is the directed union of its finitely generated solvable subgroups, H is elementary amenable.

**Residual solvability corollary.** A residually solvable group has no nontrivial perfect subgroup. Indeed, any homomorphism from a perfect group to a solvable group has perfect image, and a perfect solvable group is trivial. Thus all separating maps kill every perfect subgroup, which residual solvability forbids. It follows that

\[
H\leq PL_+(I),\ H\text{ residually solvable}
\quad\Longrightarrow\quad
H\text{ locally solvable and elementary amenable}.
\]

If H is finitely generated, the conclusion strengthens to solvable. The argument also applies when every finitely generated subgroup of H is residually solvable, even without assuming global residual solvability.

**Boundary check.** The arbitrary-H conclusion cannot be strengthened to solvability by this argument. W is nonsolvable but residually solvable: a nonidentity element has a nonzero coordinate, and projection onto that finite-derived-length W_n separates it in a solvable quotient. This also shows why the older universal-W theorem alone does not eliminate residual solvability; the finite generation theorem supplies the missing ingredient.

**Another boundary check.** Perfect does not imply non-elementary amenable in this setting. L is a directed union of solvable groups, so L' is a nontrivial perfect elementary amenable subgroup of F. Thus no argument may promote the existence of a perfect subgroup to a proof of non-elementary amenability.

**Independent adversarial check.** At 2026-10-17 21:04:25 UTC the parent agent confirmed the coordinate commutator identity, verified directly from Bleak's beta-chain construction that the inclusions add an outer shift rather than the opposite wreath orientation, checked that W_2' remains nontrivial under the injections, and checked both quantifiers in the conclusion: arbitrary residually solvable H is locally solvable and elementary amenable; finitely generated such H is solvable. No gap was found in this deduction from the cited theorems.

## Remaining simple-subgroup and residual certificates

The usual facts that F' is infinite nonabelian simple, that every nontrivial normal subgroup of F contains F', and that F contains copies supported in proper dyadic subintervals imply the following certificates.

- If H has no infinite simple subgroup, it contains no F, because an embedded F carries an embedded F'. This certificate is valid; no construction satisfying it together with non-elementary amenability inside F has been established here.
- Residual solvability excludes F by perfectness, but Proposition 2 shows that this certificate cannot yield a counterexample inside F.
- Residual finiteness excludes F by the infinite simplicity of F', but Proposition 1 is stronger and blocks the entire non-elementary amenable residual-finite family.
- Residual elementary amenability excludes F: every nontrivial map from F' to an elementary amenable group would be injective by simplicity, impossible because F' contains a copy of the known non-elementary amenable group F. Thus every map F -> an elementary amenable group kills F'. No argument here shows that a residually elementary amenable subgroup of F is elementary amenable. This broader certificate survives the two obstructions above.

These residual properties are not interchangeable. In particular L' is perfect and elementary amenable, so a map to an elementary amenable target need not kill a perfect subgroup. The residual-solvability proof cannot simply be repeated with elementary amenable targets.

For classical background on F', proper quotients, and non-elementary amenability see [Cannon–Floyd–Parry, introductory notes](https://www.imo.universite-paris-saclay.fr/~emmanuel.breuillard/Cannon.pdf), especially Section 4 (Theorems 4.3, 4.5, and 4.10). These standard facts are used as background here; their proofs were not rederived in this audit.

## Growth and identities: valid certificates that are too restrictive

Every nonabelian subgroup of PL_+(I) contains Z wr Z, by Theorem 21 of [Guba–Sapir](https://arxiv.org/pdf/math/0005114). A direct elementary growth check suffices: if a is the coordinate-zero lamp and t the shift, the 2^n products

\[
a^{\epsilon_0}t a^{\epsilon_1}t\cdots a^{\epsilon_{n-1}}t,
\qquad \epsilon_i\in\{0,1\},
\]

have length at most 2n and distinct lamp configurations. Thus Z wr Z has exponential growth. An embedded finitely generated subgroup has generators of bounded length in a finitely generated ambient group, so its exponential growth gives exponential growth of the ambient group, regardless of distortion.

Consequently a finitely generated subgroup of F with subexponential growth is abelian. More generally a subgroup of F all of whose finitely generated subgroups have subexponential growth is abelian. Intermediate-growth groups cannot be the required H. Since Z wr Z contains a direct sum of infinitely many copies of Z, finite Prüfer rank or finite cohomological dimension would also force H to be abelian.

For group identities, [Navas, *Groups, orders, and laws*](https://ems.press/content/serial-article-files/29711), printed p. 867, explicitly explains that a subgroup of PL_+(I) satisfying a nontrivial law is solvable, using Bleak's W and the fact that W has no nontrivial law. Thus a law may exclude F, but it also forces elementary amenability. Conversely, being lawless or having exponential growth supplies no evidence of non-elementary amenability: W_2 has exponential growth and W is lawless, while both are elementary amenable.

## Independent checks of three parallel deductions

The following parent-proposed lemmas were independently checked for hidden assumptions.

1. **Disjoint fixed-coordinate intervals.** Suppose H fixes the complement of a family of disjoint open intervals pointwise. Continuity fixes every interval endpoint. A nontrivial restriction of f in finite PL to one of those intervals cannot be affine, since an affine map fixing both endpoints is the identity. Hence each active interval consumes an interior slope breakpoint. Every f is active on only finitely many intervals, and restriction embeds H into the restricted direct sum of its coordinate images. If all images are elementary amenable, H is elementary amenable. No finite generation assumption or uniform bound on active intervals is required. Pointwise fixed complement and preservation of the intervals are essential; an action permuting intervals is a different situation.
2. **Marked-group closure.** In a fixed finite-rank marked-group space, the groups containing F form an open set. Represent an embedded standard generating pair by two words. The finite presentation relators hold and their commutator is nontrivial; all are finite word checks and persist in nearby marked groups. The induced map from F has nonabelian image, so its kernel is trivial because every proper quotient of F is abelian. Therefore the F-free groups form a closed set. Fixed marking rank is part of the statement.
3. **Finite full subdirect products.** A subgroup H <= F^n surjecting onto every coordinate contains F, for finite n>=1. Project to the first n-1 coordinates. Its last-coordinate kernel is normal in the full last F by surjectivity. If nontrivial it contains F' and therefore F; if trivial H is isomorphic to its projected full subdirect product, and induction applies. No finite generation assumption is needed. This proves no statement for an infinite product by itself.

## Exact remaining gap

No counterexample was obtained. Residually finite and residually solvable constructions are blocked inside F by the proved implications above; identities and slow growth are also blocked. Residually elementary amenable groups and groups with no infinite simple subgroup remain certificates worth distinguishing, but an explicit non-elementary amenable subgroup of standard finite dyadic PL F with either property has not been constructed. An embedding into all homeomorphisms, an infinite-breakpoint PL group, a piecewise projective group, or a marked-group limit would not fill this gap.

This audit does not turn either remaining certificate into an equivalent formulation of 21.144, and it does not claim that the identified obstruction deductions are new.
