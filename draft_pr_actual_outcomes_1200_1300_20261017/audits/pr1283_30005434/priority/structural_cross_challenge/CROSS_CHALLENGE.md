# Reverse cross-challenge: structural family versus direct lineage

The initial structural audit was sealed at 2026-10-18T04:06:59.925610Z before this review. Root then authorized this cross-challenge. The direct-lineage manifest was authenticated against SHA256 `99584fc89e51d8ce29009e7cfe6010437015fba539f9c76e8d3b27fe37c9c095`, and every listed file was authenticated before use. Its report, source register, query ledger, and provenance were inspected. No unrelated shard or outside individual was contacted. Initial outputs and seals remain unchanged.

## Findings requiring action or qualification

1. **Retain the 2016 exact-operation credit.** The direct-lineage initial report's bounded negative observation about finding no exact formula is superseded by the independently verified Castiglioni–San Martín precedent. It was a properly bounded independent search result, not a contradiction requiring alteration of that sealed history. Current paper/metadata must use the combined evidence.
2. **The stronger convention predates the workshop.** The authenticated 2022v1 PDF, extraction, and p.5 image were separately authenticated against the sibling's provenance; the image was visually inspected. Definition 3.1 requires a commutative monoid with neutral e. The [arXiv version record](https://arxiv.org/abs/2206.04955v1) gives 10 June 2022, before the February–March 2023 workshop. “Earliest downloaded version-dated attestation in that family” is defensible. “First convention,” “later repair,” or attributing its invention to this candidate is not.
3. **The N5 example is canonically meet-closed, and does not contradict the discrete-case theorem.** Do not resolve the apparent conflict by claiming this specific L-reduct acquires different/new canonical meets. The precise proof is below. Lower semimodularity and the associated closure exchange property in the cited enumeration result assume that the generating L-algebra is discrete. N5's target L-algebra is not discrete.
4. **Preserve the original-body and recent-body gaps.** The sibling correctly distinguishes full bodies from metadata, indexed passages, and first-page previews. Normal access failure to the 2008 sources is not exclusion of their statements or consequences. Screening recent paper introductions and complete text scans does not exclude every implicit result. The root's stated removal of firstness/new-solution/new-mechanism/current-openness claims remains necessary.
5. **Register only the new durable program as a portable automatic diagnostic.** The initial `STRUCTURAL_CHECKS.py` uses assertions, which Python removes under optimization, and writes a result file. It remains historical evidence of its actual normal run. The new detached program below uses explicit exceptions and stdout-only deterministic JSON; it must not be conflated with the initial checker.

## Canonical-closure scope, resolved precisely

Let X be the target L-algebra on a top meet-semilattice, and embed it in its self-similar closure S(X). Write F_r(z)=r·z on the entire S(X). Let t be the canonical meet of x,y in S(X).

If x≤y in X, then that order relation is preserved in S(X), so t=x. Otherwise put a=x∧_X y. Then a<x, and the exact formula gives three relations in X:

\[
x\cdot y=a,\qquad x\cdot a=a,\qquad a\cdot x=e.
\]

They persist in S(X). Applying cycloid to the pair (x,a), for every z∈S(X), gives

\[
a\cdot(x\cdot z)=e\cdot(a\cdot z)=a\cdot z.
\]

Thus F_aF_x=F_a on the whole extension. The canonical mixed identity in S(X) now gives

\[
F_t=F_{x\cdot y}F_x=F_aF_x=F_a.
\]

Translation indices in an L-algebra are injective when the maps agree on the entire carrier: evaluate F_t=F_a at a and at t to obtain t·a=e and a·t=e, then apply separation. Hence t=a. Therefore the supplied meet is preserved in S(X), and its meet closure C(X) is exactly the embedded X. This argument does not infer equality of indices merely from agreement of restricted maps on the original X.

There is also a direct application of an older published criterion. In Rump, *The category of L-algebras*, TAC 39 (2023), printed p.604, Proposition 3.4 equates a partial-product greatest-element condition with preservation of meets by every L-algebra morphism out of X. The actual p.604 was downloaded and visually inspected. Partial multiplication is defined on p.601: ry=w when w≤y and y·w=r. For the target, with u=y∧z, one has y·u=y·z and u≤y,z; hence (y·z)y=u exists. If ry=w≤z exists, monotonicity of left multiplication yields r=y·w≤y·z. Thus y·z is the required greatest r and Proposition 3.4 applies. This gives the stronger conclusion that every L-morphism from this target preserves its meets. It is an application of Rump's criterion after L-algebra verification; the criterion does not by itself establish those L-algebra axioms from hemiimplicative membership. [Actual TAC primary PDF](https://tac.mta.ca/tac/volumes/39/21/39-21.pdf).

The older framework therefore deserves positive credit, not just a statement that closure is a separate concept. It also does not establish a priority claim for the exact arbitrary-semilattice application without checking the 2016 operation and the additional identities.

## Why N5 is consistent with the cited theorem

Use N5 with 0<a<b<e and 0<c<e, where c is incomparable with a,b. The target multiplication satisfies every listed L-algebra/semibrace equation; the new diagnostic checks all tuples. The logical order equals this lattice order and is not discrete, since 0<a<b are distinct non-top comparable elements.

N5 is not lower semimodular: b∨c=e covers c, while b does not cover b∧c=0 because 0<a<b. Equivalently, for the semilattice closure on X'=N5\{e},

\[
\operatorname{cl}(A)=\{u\in X':\bigwedge A\le u\},\qquad\bigwedge\varnothing=e,
\]

one has cl({b})={b}, cl({a})={a,b}, and cl({b,c})={0,a,b,c}. These exhibit a proper intermediate closed set between cl({b}) and cl({b,c}). The standard exchange formulation also fails: a∈cl({b,c})\cl({b}), whereas c∉cl({b,a}). This is permitted because X is not discrete.

The actual enumeration v4, printed p.8, Theorem 3.6, explicitly assumes a discrete L-algebra X before concluding lower semimodularity of C(X). Its source attribution is to Rump 2015, Proposition 18. The [indexed primary poster](https://www.impan.pl/konferencje/bcc/2021/21-algebraybaxter/l_algebras_size_8.pdf) places the corresponding statement under the discrete-case discussion, after specifying that case and its C(X) approach. Another poster passage explicitly discusses the lack of a useful analogous restriction for non-discrete algebras. Multi-column extraction interleaves those paragraphs, so an isolated unqualified sentence is misleading. The 2021 directory name does not date the poster, which cites arXiv:2206.04955.

The right qualification is therefore **discrete-generating-L-algebra hypothesis**, not a claim that N5's supplied meet differs from its canonical meet. Neither universal lower semimodularity of all C(X), nor arbitrary exchange for all these semilattice expansions, is supported by these sources. [Version-pinned enumeration v4](https://arxiv.org/pdf/2206.04955v4).

## Chronology and source-gap challenge

The direct-lineage report separates workshop dates, repository accession, journal publication metadata, and actual version-pinned content. That treatment survives this challenge. The exact printed workshop axioms remain the target; neither a bibliography pointer nor a stronger older convention proves an unprinted authorial intention. Conversely, the omission of a neutral-e axiom must not be described as evidence that the stronger convention was invented later.

The 2008 semidirect-products Definition 3/Theorem 3 pages remain uninspected in both initial families. Later primary attributions are useful credits, but are not complete inspection of all earlier examples. The 2008 self-similarity and 2015 right-ℓ-group complete bodies are also gaps. No access controls were bypassed and no copy was requested.

Properzi–Qin [arXiv:2512.08579v1](https://arxiv.org/abs/2512.08579v1), dated 9 December 2025, concerns ideals, semidirect products, and simple/linear families in the inspected material. This family's initial audit also inspected relevant actual body sections and examples. This supports a scoped screening statement, not absence of every implicit consequence. The [publisher record for Rump's decomposition paper](https://link.springer.com/article/10.1007/s11083-025-09719-8), newly accessible during this challenge, gives version-of-record publication 23 December 2025 and issue 43 (2026), article 8. Its abstract describes decomposition/cancellation/centres; the complete body remains subscription-only and uninspected here. That concrete metadata refinement does not close its body gap.

The strongest current supported framing is: a complete proof under precisely stated printed axioms, applying an operation already explicit in 2016 and using established L-algebra/closure theory. Mathematical validity and historical firstness are separate. Do not replace the actual positive construction precedent with a generic “priority unestablished” disclaimer alone.

## Detached durable diagnostic

`durable_structural_checks.py` has no assertions, private inputs, filesystem reads, or explicit filesystem writes. It prints deterministic JSON to stdout. All checks use `require`, which explicitly raises `DiagnosticFailure`. The optional `--inject-failure` deliberately evaluates a false predicate, prints a failure object, and exits 1.

Actual runs were performed normally, with `-O`, and with `-OO`, each both with and without the injected failure. All normal runs exited 0 with identical stdout SHA256 `f9735e422e3205d01a916ce1759e8c0c35b9d44bfa2025e6e409b633362e16f4`; all injected runs exited 1 with identical stdout SHA256 `a0d69bc47818f73be0379f20246664270dd182fdc11f68d9fd7ea4bd59eda634`. Stderr was empty in all six runs. The test harness alone saved the stdout and execution receipts.

The program checks the target on a singleton, a four-chain, Boolean four, Boolean eight, M3, and N5; checks the partial-product condition used in Proposition 3.4 on all these fixtures; checks right projection at all four prescribed points of a chain; and validates the different-old-order-implication and hIS4 counterexamples. The N5 cover/closure witnesses are explicit. It is a portable finite diagnostic, not a computation of S(X), an exhaustive model census, a proof of the universal theorem, or a novelty certification.

The initial assertion-based checker is preserved exactly as historical evidence of its normal execution. It is not durable under optimization and must not be registered as the portable automatic validator.

## Completion and recommendation

The assigned reverse challenge is complete. Retain the root's stated old-operation credit and historical qualifications. Add or retain the precise canonical-meet/discrete-case explanation above wherever closure/lower-semimodularity is discussed; remove any suggestion that this target needs different canonical meets to explain N5. Update only the current artifact editions through root, leaving the two initial sealed audits untouched. Register the detached durable program and its actual run receipts as the automatic diagnostic.

No additional firstness qualification is needed beyond these concrete corrections and the existing source gaps; adding broad unsupported claims in either direction would weaken the evidence. No external contact or publication mutation occurred.
