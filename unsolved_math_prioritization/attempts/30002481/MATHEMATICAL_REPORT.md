# Lightface determinacy over Z3: partial lemmas and model-transfer audit

Problem 30002481 / OWR-12862-007, queue rank 1242. First proof-search attempt, 1/5. Written 10 October 2026 UTC.

**Outcome: partial, not a proof or countermodel for the original implication.** The results below reconcile the two lightface pointclasses, identify a literal cardinal/power-set obstruction in the published hull argument, and rule out a broad elementary class of proposed countermodels. A separate conditional lemma isolates the countable-completeness step. No novelty claim is made for these elementary observations or for the cited results.

## 1. Exact target and coding convention

Use Cheng–Schindler's set theory

\[
Z_3=\mathrm{ZFC}^{-}+\mathcal P(\omega)\text{ exists}
       +\forall a\ (|a|\leq\beth_1),
\]

where Power Set is omitted and **Collection replaces Replacement**. Write \(R=\mathcal P(\omega)\). The cardinal bound in particular supplies an injection from every set into \(R\). When cardinal ordinals are used, \(\mathfrak c=\beth_1=|R|\) denotes the existing initial ordinal equinumerous with \(R\). We do not infer well-orderability from an unspecified weak presentation of Choice; the power-set obstruction and the CH assertions below need only the injection bound and, for CH, its explicit bijection. Do not replace this theory by a type-theoretic third-order system without proving an interpretation.

Games have length \(\omega\), with alternating natural-number moves; player I wins just when the resulting real belongs to the payoff. The determinacy hypothesis concerns parameter-free, lightface \(\Pi^1_1\) payoffs, with integer indices allowed. It does not assert determinacy for all real parameters.

The conclusion is the **full coded-sharp sentence used by Cheng–Schindler, section 2**: there is a real coding a countable iterable active premouse of the form \((L_\alpha,\in,U)\), with \(U\ne\varnothing\). A real code specifies a countable domain, its membership relation, and the active measure predicate; well-founded extensional membership is decoded by its transitive collapse. The premouse and iterability conditions are the source's standard conditions. In particular, “iterable” includes all countable iterations required by that convention, with well-foundedness at successor and direct-limit stages. It does not mean merely that the initial membership relation, first ultrapower, or every finite iterate is well-founded.

Cheng–Schindler explicitly give this existence statement as \(\Sigma^1_3\). Denote that fixed second-order-arithmetic sentence by \(\mathrm{Sharp}\). We use its projective definability as a cited coding fact; we do not construct a new fine-structural coding or claim a machine formalization of its equivalence with other definitions of \(0^\#\). The model-transfer proof below preserves **every** second-order-arithmetic formula, so it is independent of the choice among equivalent standard real codings and does not truncate the iterability quantifiers.

The question is whether

\[
Z_3\vdash\mathrm{Det}(\Pi^1_1)\longrightarrow\mathrm{Sharp}.
\]

The original report is Schindler's joint-work contribution with Cheng, OWR 02/2014, pp. 127–128. The set-theoretic definitions and coded-sharp convention are pinned to [CS], Definition 1.4 and section 2. The imported title “Projective Determinacy” must not be read as full projective determinacy.

## 2. Proven internal lemma: lightface duality needs only a dummy move

**Proposition 1.** Over \(Z_3\), lightface analytic determinacy and lightface coanalytic determinacy are equivalent, without adding real parameters.

**Proof.** For any payoff \(A\subseteq\omega^\omega\), define

\[
 B_A=\{z\in\omega^\omega:\operatorname{tail}(z)\notin A\},\qquad
 \operatorname{tail}(z)(n)=z(n+1).
\]

The initial move in \(G(B_A)\) has no effect on membership. Thereafter the players' turns are reversed relative to \(G(A)\). Complementation and this recursive substitution turn a lightface analytic formula for \(A\) into a lightface coanalytic formula for \(B_A\), and conversely.

Suppose \(\tau\) wins \(G(B_A)\) for player I. Put \(d=\tau(\varnothing)\). At an odd-length history \(s\) of \(G(A)\), let player II play \(\tau(d^\frown s)\). Every resulting complete play \(a\) gives a \(B_A\)-play \(d^\frown a\) consistent with \(\tau\). Therefore \(a\notin A\), so this is a winning strategy for player II in \(G(A)\).

Suppose instead \(\tau\) wins \(G(B_A)\) for player II. Fix \(d=0\). At an even-length history \(s\) of \(G(A)\), let player I play \(\tau(d^\frown s)\). The corresponding \(B_A\)-play is consistent with player II's strategy, so it is outside \(B_A\). Hence its tail belongs to \(A\), and the translated strategy wins \(G(A)\) for player I.

All strategy transformations are recursive relative to the supplied strategy; their graphs exist by Separation on a countable coding set. Applying the construction to each payoff proves both implications. No choice of an additional real parameter is involved. \(\square\)

The dummy move matters: merely complementing a payoff does not reverse which player moves first. This proposition justifies comparing the OWR \(\Pi^1_1\) notation with the \(\Sigma^1_1\) notation in [CS] and [Sami].

## 3. Proven internal lemma: the top power set and successor cardinal are absent

**Proposition 2.** The following are provable in \(Z_3\).

1. No set is the power set of \(R\).
2. Every ordinal admits an injection into \(R\); hence there is no Hartogs ordinal of \(R\) as a set.
3. In cardinal-ordinal notation, there is no cardinal strictly larger than \(\mathfrak c\), so \(\mathfrak c^+\) does not exist as a cardinal ordinal of the universe.
4. With CH, neither \(\mathcal P(\omega_1)\) nor the cardinal ordinal \(\omega_2\) exists as a set.

**Proof.** Suppose \(Q=\mathcal P(R)\) were a set. The size bound gives an injection \(i:Q\to R\). Define a function \(F:R\to Q\) by taking the unique preimage under \(i\) when one exists and taking \(\varnothing\) otherwise. Its graph is a set by Separation and Collection (or the Replacement consequence of Collection). It is surjective. Separation on \(R\) produces

\[
D=\{r\in R:r\notin F(r)\}\in Q.
\]

Choose \(d\in R\) with \(F(d)=D\). Then \(d\in D\iff d\notin D\), a contradiction. No unasserted power set was used in this diagonalization.

An ordinal is a set, so the size axiom itself gives its injection into \(R\). This proves (2). If a cardinal ordinal \(\lambda>\mathfrak c\) existed, that injection, composed with a bijection \(R\cong\mathfrak c\), would contradict its cardinality. This proves (3).

Under CH fix a bijection \(b:\omega_1\to R\). If a set \(Q_1=\mathcal P(\omega_1)\) existed, Collection applied to \(A\mapsto b[A]\), for \(A\in Q_1\), would give \(\mathcal P(R)\) as a set, contradicting (1). The absence of \(\omega_2=\mathfrak c^+\) follows from (3). \(\square\)

These are **internal** statements. They do not say that a transitive model has no larger ordinals in an ambient universe, or that its inner class \(L[x]\) cannot compute additional cardinals. One must distinguish \(\omega_2^V\) from \(\omega_2^{L[x]}\).

**Consequence for a proof route.** In a \(Z_3+\mathrm{CH}\) universe one cannot literally start an argument by taking a set-sized level above its \(\omega_2\). A countably closed elementary hull cannot be forced to be proper merely by saying it has size \(\mathfrak c\) inside a larger set: the axiom bounds every set by \(\mathfrak c\). This does not prove that every useful closed hull is absent. It pinpoints why the usual size argument is unavailable.

## 4. Proven external model-transfer theorem

The following is a metatheorem about models in an ambient set theory. It is not a claim that \(Z_3\) constructs the extension occurring in its hypothesis.

**Proposition 3 (same-reals transfer).** Let \(M\subseteq N\) be transitive models with the same natural numbers, and suppose

\[
\mathcal P(\omega)^M=\mathcal P(\omega)^N.
\]

Assume \(M\models Z_3\) and \(N\models\mathrm{ZF}\). Then

\[
M\models\mathrm{Det}(\Pi^1_1)\longrightarrow\mathrm{Sharp}.
\]

The argument also applies to class models under the corresponding ambient class formulation.

**Proof.** Arithmetic operations, number quantifiers and membership of numbers in real parameters agree between the two transitive models. Their real quantifiers range over exactly the same collection. Induction on formulas therefore proves agreement on every formula of second-order arithmetic, with shared real parameters. This includes arbitrary finite alternations of real quantifiers; there is no restriction to arithmetic or \(\Pi^1_1\) formulas.

For completeness, a strategy in a game on the natural numbers is a real, using a fixed recursive encoding of finite positions. A run and any analytic/coanalytic witness are likewise reals. Thus “this real is a winning strategy for the game with index \(e\)” is a second-order formula whose domains and arithmetic interpretation agree. The assertion of determinacy for every lightface index therefore agrees. One may either use an effective universal pointclass code or reason with each indexed instance; no uncountable family of payoff sets is required.

Suppose \(M\) satisfies the antecedent. Then \(N\) does. In \(N\), the classical Martin–Harrington theorem in ZF, together with Proposition 1, gives \(\mathrm{Sharp}\). The coded-sharp sentence of section 1 is a projective sentence, including its full iterability condition. The same induction transfers it back to \(M\). Its witness is a real of \(N\), hence is already in \(M\); all number and real quantifiers of the witness predicate also agree. \(\square\)

This is not an application of Shoenfield absoluteness. It uses identical complete second-order reducts. It does not apply to arbitrary nonstandard models, to a merely common subset of reals, or to models agreeing only on finite approximations to iteration.

**Corollary 3.1.** A transitive model of \(Z_3+\mathrm{Det}(\Pi^1_1)+\neg\mathrm{Sharp}\), if one exists, cannot be included in a transitive ZF model with exactly the same reals and naturals. Any such ZF extension must have an additional real.

**Corollary 3.2 (ordinary hereditary-size models).** In an ambient ZFC universe \(V\), put \(\mathfrak c=(2^{\aleph_0})^V\), \(\kappa=(\mathfrak c^+)^V\) and \(H=H_\kappa^V\). Then \(H\models Z_3\), it has all the reals of \(V\), and it satisfies the target implication.

**Proof.** The successor cardinal \(\kappa\) is regular in ambient ZFC. The usual hereditary-size argument gives Pairing, Union, Infinity, Foundation and Separation in \(H\). Here is the Collection check explicitly: if \(a\in H\) and \(H\models\forall x\in a\,\exists y\,\varphi(x,y,p)\), use ambient Choice to select one such \(y_x\in H\) for each \(x\in a\). The union of the transitive closures of these fewer-than-\(\kappa\) witnesses has size below \(\kappa\), by regularity. Thus their collection belongs to \(H\). A well-order of any \(a\in H\) also has hereditary size below \(\kappa\), giving Choice in \(H\).

The set \(\mathcal P(\omega)^V\) has hereditary size \(\mathfrak c<\kappa\), hence belongs to \(H\). Every \(a\in H\) has size at most \(\mathfrak c\); an injection \(a\to\mathcal P(\omega)^V\) can be chosen in \(V\) and has hereditary size at most \(\mathfrak c\), so belongs to \(H\). Therefore \(H\models Z_3\). All reals belong to \(H\), and Proposition 3 applies with \(N=V\). The same argument is internal to any transitive ambient ZFC model. \(\square\)

There is no contradiction with Proposition 2: \(\kappa\) is available in the ambient model but is not an element of \(H_\kappa\).

**Corollary 3.3 (no-new-real transformations).** If two transitive models of the relevant weak set theory have the same naturals and reals, they agree on both determinacy in the target and \(\mathrm{Sharp}\), even when neither satisfies ZF. Consequently a forcing extension verified to add no reals cannot turn a model of \(\neg\mathrm{Det}(\Pi^1_1)\) into a target countermodel. This is a conditional statement about a verified extension, not an assumption that all forcing or class forcing over \(Z_3\) has the usual preservation properties.

## 5. A conditional local bridge: where countable closure is used

The next lemma isolates an elementary part of the measure construction. It does not assert that determinacy supplies its hypotheses.

**Proposition 4.** Work in a universe satisfying ZFC minus Power Set, with Collection. Let \(M,N\) be transitive set models of that same theory and let \(j:M\to N\) be an elementary embedding, with critical point \(\kappa\). Suppose \(M\) is externally closed under countable sequences of its elements: every function \(\omega\to M\) in the working universe belongs to \(M\). Set

\[
\mathcal B=\{A\in M:A\subseteq\kappa\},\qquad
U=\{A\in\mathcal B:\kappa\in j(A)\}.
\]

Then \(U\) is a nonprincipal ultrafilter on the Boolean algebra \(\mathcal B\), is countably complete with respect to sequences in the working universe, and is normal for regressive functions belonging to \(M\). Every ultrapower built from a set of \(M\)-functions with domain \(\kappa\), using its ordinary membership relation modulo \(U\), is externally well-founded.

**Proof.** Both displayed collections are sets by Separation on \(M\). Elementarity gives \(j(\kappa)>\kappa\). Complements and finite intersections in \(\mathcal B\) are respected by \(j\), so exactly one of \(A\) and \(\kappa\setminus A\) belongs to \(U\), and \(U\) is closed under finite intersections and supersets in \(\mathcal B\). It is proper because \(j(\varnothing)=\varnothing\), and nonprincipal because \(j(\{\xi\})=\{\xi\}\) for \(\xi<\kappa\).

An elementary embedding between these transitive models fixes \(\omega\), so \(\kappa>\omega\). Let \(\langle A_n:n<\omega\rangle\) be any sequence in the working universe with every \(A_n\in U\). Closure puts the whole sequence in \(M\). Let \(A=\bigcap_{n<\omega}A_n\), computed in \(M\). Since \(j\) fixes the index set and each integer, \(\kappa\in j(A_n)\) for all \(n\) implies \(\kappa\in j(A)\). Hence \(A\in U\), in particular \(A\ne\varnothing\). This proves external countable completeness.

For normality, let \(A\in U\) and let \(f\in M\) be regressive on \(A\). Then \(j(f)(\kappa)<\kappa\). Write that ordinal as \(\xi\); it is fixed by \(j\). Therefore \(\{\eta\in A:f(\eta)=\xi\}\in U\).

Finally, suppose an ultrapower had an infinite descending membership chain \([f_0]\ni[f_1]\ni\cdots\). Choose representatives using countable choice. For each \(n\), the set \(A_n=\{\xi<\kappa:f_{n+1}(\xi)\in f_n(\xi)\}\) is an element of \(M\) and belongs to \(U\). Countable completeness gives \(\xi\in\bigcap_n A_n\). The sequence \(f_0(\xi)\ni f_1(\xi)\ni\cdots\) contradicts Foundation. With Choice, an ill-founded set relation has such a descending sequence, so the set ultrapower is well-founded. \(\square\)

The lemma intentionally stops short of asserting that a resulting structure is a fine-structural premouse or that all its iterates are well-founded. Those require their own hypotheses and verification. Its closure assumption refers to the working universe, not just to the domain's internal sequences. If only closure in \(L[x]\) is available, passage to a larger universe requires a separate argument. In particular, the externally closed domain \(M\) is not itself the countable coded premouse sought in the target: its closure already puts every binary omega-sequence of the working universe into \(M\). Taking a countable hull later does not by itself establish the resulting premouse's full iterability.

## 6. Route audit and remaining gap

- **Classical-proof import.** [CS], Theorem 1.1, states the classical ZF result; section 3.3 proves HP gives a sharp in \(Z_4\). Its hull construction uses a level above \(\omega_2\), a hull of size \(\omega_1\), and countable closure. Proposition 2 prevents importing the universe-level size argument verbatim into \(Z_3+\mathrm{CH}\). Proposition 4 identifies the use of closure, without proving the needed hull exists.
- **Forcing-free proof.** [Sami], Proposition 3.8 and Theorem 3.9, still go through HP and then invoke Silver's theorem. Removing forcing from the presentation does not remove the weak-base issue.
- **HP separation.** The remarkable-cardinal calibration and HP separation in [CS] do not determine the truth of the stronger determinacy antecedent in a candidate model. No reversal HP implies determinacy was established here.
- **Natural countermodels.** Proposition 3 rules out same-reals ZF extensions and ordinary \(H_{\mathfrak c^+}\) constructions. It does not exclude arbitrary transitive \(Z_3\) models, much less nonstandard ones.
- **Parameter strengthening.** Replacing lightface determinacy by its boldface, real-parameter-uniform version is not authorized. Neither a strategy parameter nor the HP witness may silently be added as a parameter to the determinacy hypothesis.
- **Unproved intermediate idea.** Existence of \(\omega_2^{L[x]}\) for an HP witness might support an inner-model hull argument. This attempt does not prove that conditional: existence of the appropriate level, closure in the right universe, and upward transfer of full iterability would all need explicit formalization. It is not included among the results.

A successful next mechanism must either extract the required iterable premouse from lightface strategies using axioms available in \(Z_3\), or construct a model satisfying the actual lightface determinacy assertion and failing full coded iterability. The partials above do neither. No full countermodel, proof, or current-open certification is claimed.

## Review status

The [mathematical audit](MATHEMATICAL_AUDIT.md) accepts precisely Propositions 1–4, Corollaries 3.1–3.3 and the qualified route conclusions. This AI-assisted, unrefereed proof-and-audit edition preserves the complete written mathematics and its cited premises. Acceptance is not external human peer review, journal acceptance or formal proof-assistant certification. The original implication remains unresolved by this work.

## References

[OWR] Ralf Schindler, joint work with Cheng Yong, *Does Pi-1-1 determinacy imply 0#?*, in *Set Theory*, Oberwolfach Reports 02/2014, pp. 127–128. https://doi.org/10.4171/owr/2014/02

[CS] Yong Cheng and Ralf Schindler, *Harrington's Principle in Higher Order Arithmetic*, arXiv:1503.04000v1 (2015); Journal of Symbolic Logic 80 (2015), 477–489. Definition 1.4, section 2, Theorem 1.1, Theorem 3.2, Corollary 3.5, Theorem 3.6. https://arxiv.org/abs/1503.04000 ; https://doi.org/10.1017/jsl.2014.31

[Sami] Ramez L. Sami, *Analytic determinacy and 0#: A forcing-free proof of Harrington's theorem*, Fundamenta Mathematicae 160 (1999), 153–159. Sections 1.4 and 3.8–3.9. https://doi.org/10.4064/fm-160-2-153-159 ; https://matwbn.icm.edu.pl/ksiazki/fm/fm160/fm16022.pdf
