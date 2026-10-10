# 30003688: source reconciliation and credited finite-family result

**Target:** rank 363, OWR-15986-003, imported title “Finite Families with Two-Element Rogers Semilattices.”

**Author proof turns used: 0/5.** This is a source/literature gate, not an exhausted research attempt or a new solution claim. Any later well-defined unresolved target retains all five author turns.

## 1. What the primary workshop source actually supplies

S. S. Goncharov's contribution “Rogers Semilattices of Generalized computable numberings” appears on printed pp. 18–19 of *Computability Theory*, Oberwolfach Reports 15 (2018), no. 1, pp. 5–41, DOI [10.4171/OWR/2018/1](https://doi.org/10.4171/OWR/2018/1). The publisher records publication on 5 January 2019, so the imported 2019 publication date is not an error. The workshop was held on 7–13 January 2018.

The full [primary PDF](https://ems.press/content/serial-article-files/46723) was downloaded, its text read, and printed p. 19 visually inspected. Physical PDF page 15 is printed p. 19.

The relevant paragraph explicitly concerns the **Ershov hierarchy** Σ⁻¹_n, n≥2, and numberings computable at that same level. The imported record instead writes the arithmetical hierarchy Σ⁰_n. This replacement changes the mathematics. Ordinary computable reducibility of numberings also must not be replaced by reducibility relative to an oracle.

The workshop paragraph states a result for an infinite family and discusses distinguished numberings α, β, with α Friedberg and the condition γ≢α ⇒ β≤γ. Its compressed wording includes “with exactly two different elements α and β”. The following sentence is “The question is open about finite family with these properties”. The closing sentence additionally alludes to existence of a family, without specifying a different formal target.

These sentences do not provide a reliable basis for conflating:

1. exactly two degrees in the **entire** Rogers semilattice;
2. exactly two minimal/Friedberg degrees, with other degrees above them;
3. a decomposition into one singled-out degree and a principal filter;
4. existence of a finite underlying family;
5. the unspecified additional existence question.

No claim about the original author's intended repair is made here. In particular, this packet does not silently insert the word “minimal” into the workshop text.

## 2. Definitions verified in a reference cited by the workshop

Goncharov–Lempp–Solomon, *Friedberg numberings of families of n-computably enumerable sets*, Algebra and Logic 41 (2002), 81–86, DOI [10.1023/A:1015352513117](https://doi.org/10.1023/A:1015352513117), has an [author-hosted complete PDF](https://people.math.wisc.edu/~slempp/papers/fried.pdf). Page 2 of that preprint was visually inspected. It defines:

- a numbering of S as a surjection ν:ω→S;
- a Friedberg numbering as an injective such numbering;
- ν≤μ by ν=μ∘f for a total computable f;
- an n-c.e. set through a computable zero-start approximation changing each bit at most n times;
- an n-c.e. numbering by a uniformly n-c.e. membership relation.

Consequently no finite S has a Friedberg numbering under these definitions: if |S|=k, injectivity already fails on the k+1 indices 0,…,k. The empty family has no numbering at all. This is a definitional obstruction to the literal imported finite-family/Friedberg conjunction, not a new research theorem and not evidence that a substantive intended open problem has been solved. It is independent of which hierarchy is used.

A useful elementary distinction is that two distinct minimal elements of an upper semilattice cannot exhaust it: their join is a third element. This explains why counting two Friedberg minimal degrees cannot be substituted for counting the whole semilattice. The argument does not assume that the workshop's β is Friedberg; that stronger fact belongs to the predecessor below.

## 3. A primary predecessor clarifies the distinction, without determining intent

Badaev–Lempp, *A decomposition of the Rogers semilattice of a family of d.c.e. sets*, Journal of Symbolic Logic 74 (2009), 618–640, [author PDF](https://people.math.wisc.edu/~lempp/papers/Khutoret.pdf), gives its Main Theorem on preprint p. 3. The abstract, definitions, and Main Theorem were read from the complete PDF.

It constructs a family F of c.e. sets, considered with d.c.e. numberings, and two inequivalent Friedberg numberings μ,ν. Every d.c.e. numbering π of F satisfies π≡ν or μ≤π. The abstract specifies that precisely two equivalence classes have Friedberg representatives. It explicitly leaves the larger cardinality problem open at the time. Thus this result is compatible with an infinite entire semilattice; it is not a two-element-semilattice construction. The exact theorem is credited to Badaev and Lempp, not reassigned to the workshop's named collaborators.

The complete 2009 priority construction was retrieved but **not independently re-proved or fully audited** in this source gate. Only its relevant definitions, statement, and distinction of scopes are used.

## 4. The finite-Ershov cardinality question has a published negative answer

Keng Meng Ng, Nikolay Bazhenov, Birzhan Kalmurzayev, and Dias Nurlanbek, *On cardinalities of Rogers semilattices for families in the Ershov hierarchy*, Information and Computation 307 (2025), article 105354, DOI [10.1016/j.ic.2025.105354](https://doi.org/10.1016/j.ic.2025.105354).

The publisher's [indexed primary article](https://www.sciencedirect.com/science/article/abs/pii/S0890540125000902), **Theorem 3.1**, gives:

For each integer n≥2 and each finite nonempty family S of n-c.e. sets,

    |R⁻¹_n(S)| ∈ {1, ℵ₀}.

In particular |R⁻¹_n(S)|≠2. No Friedberg assumption is needed for this exclusion. Every finite nonempty family is uniformly numberable at its level by cycling through its finitely many fixed approximations, so emptiness of the class of numberings is not a missing case.

The theorem's exact finite-family hypothesis and whole-semilattice conclusion are available in the publisher excerpt, followed by the beginning of its proof. The introduction identifies the finite-cardinality question and states that Theorem 3.1 rules it out for finite families. The abstract additionally says its later theorem shows that the Badaev–Lempp example's Rogers semilattice is infinite. The finite-family theorem is independently corroborated as a result of this paper on [Ng's publication page](https://personal.ntu.edu.sg/kmng/publications.html); [Bazhenov's publication page](https://bazhenov.droppages.site/publications.html) confirms the paper and metadata.

**Access and validation limit:** the full 2025 proof was not recovered. Both author pages link the DOI, rather than an accessible preprint of this article. The public publisher excerpt stops within the proof. Direct article/PDF web retrieval did not return the complete paper; exact-title, DOI, author-site, institutional-repository, and arXiv searches did not locate a lawful open copy. Accordingly this is a verified attribution and statement match, **not an independent mathematical audit of the 2025 priority argument**. No claim to have checked its omitted steps is made.

## 5. Exact scope of the conclusion

- The literal imported finite-family/Friedberg conjunction is inconsistent with the source's standard definition, by the finite pigeonhole principle.
- The separate, coherent **finite-Ershov-family / two-element entire Rogers semilattice** question has the credited published negative answer in 2025 Theorem 3.1.
- This 2025 theorem is not automatically a theorem about arithmetical Σ⁰_n numberings. This packet does not use it that way.
- The 2025 finite-family theorem does not settle a corresponding unrestricted infinite-family cardinality question, or identify the intended meaning of the workshop's vague final sentence.
- The workshop paragraph and imported formulation must not be promoted together as a completely resolved, unambiguous original conjecture.

**Review request:** independently verify this source match, the hierarchy distinction, the two different cardinality notions, and the precise limits above. A credited `already_solved` record is supportable for the finite-Ershov cardinality subquestion, but final disposition of the malformed aggregate record requires an explicit source-scope decision. No QUEUE/PR change or solved promotion is part of this frozen source packet.
