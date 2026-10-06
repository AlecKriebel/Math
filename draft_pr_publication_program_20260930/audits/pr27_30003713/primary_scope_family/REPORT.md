# PR27 original-stage primary-source and provenance audit

Closed UTC: 2026-10-01T22:38:12.647023+00:00. Audit completion: 100%. This is validation of
a partial result, not progress toward a new solution. Original head:
`84d7f6103b087e431d7afb751501380ebd7ffd42`.

**Verdict: the known mathematical partial passes; retain UNSOLVED, one of five
substantive attempts used.** No full decomposition, novel result, worldwide
openness certificate, paper or DOI claim is verified. The original heuristic
15% estimate is not a proof and does not equal the 1/5 attempt count.

## Independence and scope

The primary target, source ranges, universal reconstruction and falsification
criteria were sealed before opening the original mathematical note, historical
review or scripts. The early reconstruction's SHA256 is
`547432c63085667e33263acd3aef25a3a8deec8ba77ebdfad4989c53acdd8f73`,
sealed at 2026-10-01T22:23:31.576341+00:00. The parent supplied the target head,
source URLs and proposed partial disposition; those were hypotheses. This is
a materially distinct original-stage family, not a reused final gate.

All work belongs to this family. Foreign PDFs, extracted source text, images,
API responses and isolated historical executions are in ignored tmp. There
were no outside individual contacts, installations, Git mutations, canonical
attempt edits, queue edits, PR edits or publication actions. Every sealed
artifact is preserved, including the append-only chronology correction.

## Exact primary target and prior ranges

[OWR 2018/2](https://ems.press/content/serial-article-files/46724), printed
p.118, Question 13 by Dan Petersen, fixes arbitrary finite-dimensional complex
E,V and asks for H_*(Lie(V) tensor (C direct sum E)), E squared zero, as a sum
of polynomial functors in both variables. The page was read with adjacent
context and visually checked. The exact success criterion is an evaluated,
natural Schur-functor decomposition for every homological degree, E weight,
V degree and finite dimension, including dimension vanishing. An unevaluated
family of kernels, a structural complex or bounded ranks fails that criterion.
Homogeneous pieces are polynomial; the full unbounded V-degree object need
not be a polynomial functor of a single finite degree.

The [2017 MathOverflow discussion](https://mathoverflow.net/questions/273196/homology-of-an-interesting-lie-algebra)
already contains the exterior-coefficient and two-term reformulations and
the cyclic-Lie case. All eight comments were checked through the read-only
StackExchange API. The July comments also expose a false general coinvariant
guess by a Sym² coefficient example in V degree three. These are prior work,
not discoveries of the attempt.

[Gadish–Hainaut](https://ahl.centre-mersenne.org/item/10.5802/ahl.213.pdf),
AHL 7 (2024), 841–902, §1.3, gives complete characters for particle count
n<=10 and part of n=11. Theorem 1.8 supplies the two unbounded columns
indexed by (m) and (1^m), all m>=1, for the associated graded configuration
cohomology. Section 4.4's dictionary involves duals and conjugate partitions;
these families and tables are not an unqualified all-partition Lie-homology
answer. Associated graded composition factors also do not erase extensions
of the outer-group action.

[Powell 2309.07607](https://arxiv.org/abs/2309.07607) adds a differential
graded category and syzygy structure to the two-term complex. It does not
evaluate all irreducible multiplicities. [Powell v4, 2507.03453](https://arxiv.org/abs/2507.03453v4)
computes the relative-degree-two diagonal, with the preceding diagonal in
Proposition 3.3 and the cyclic-Lie convention in Example 3.1. The tensor-count
one case is exceptional. Its sign labels transport exactly to the original
partial equations (4)–(5). The arXiv version is dated 16 December 2025;
[publisher metadata](https://www.tandfonline.com/doi/abs/10.1080/10586458.2025.2608243)
reports online publication on 4 March 2026. The mathematical text actually
inspected was v4; the final journal PDF was not compared.

A fresh bounded primary-only search and Powell's own publication list located
no additional full answer in the returned sources. The exact queries and
returned-source scope are recorded separately. This limited search gives no
certificate of global absence or openness.

## Strongest universally verified mathematics

The independently derived proof is in DERIVATION_VALIDATION.md. With
L=Lie(V), I=E tensor L, the current algebra is L semidirect I with I abelian.
The ordinary Chevalley–Eilenberg differential preserves the number q of ideal
factors, so the weight q complex is C_*(L; Lambda^q I)[q], an actual split of
complexes. First-letter decomposition proves the free right T(V) resolution
of the trivial module. The coefficient homology is therefore the kernel and
cokernel of the action V tensor N -> N, with no higher homology. This gives

    H_n(h) = coker(delta_n) direct sum ker(delta_(n-1)).

Distinct E weights make this split canonical. Each fixed E and V degree is
finite-dimensional, even though L and the full complex are unbounded. No
completion or infinite product is introduced. The Cauchy decomposition uses
conjugate partitions and the exterior sign. Characteristic-zero exact
coinvariants and flat Q-to-C extension justify transport of the cited Powell
formulas, including its separate q=1 case. The cyclic character subtraction
is valid because the bracket map in its exact sequence is onto.

All original mathematical layers agree with this universal reconstruction:
H_0=C, H_1=(C direct sum E) tensor V; the E-weight-one cyclic-Lie layer;
the quoted relative-degree-one and two formulas; and the E=0, V=0 and
dim V=1 boundaries. E weight one is not the entire case dim E=1. No new
mathematical counterexample to the stated partial claims was found.

The exact remaining gap is evaluation, for every partition mu and all V
degrees, of both the kernel and cokernel of

    V tensor S_mu(Lie(V)) -> S_mu(Lie(V)).

Equivalent unresolved maps do not solve the target. An Euler characteristic
only records the difference of the two representations.

## Reproduction and new falsifiers

All thirteen attempt files were compared against both the frozen manifest
and exact Git head, including Git blob identities. The actual PR has fourteen
changed paths: those thirteen plus QUEUE.md. Its frozen queue change is
precisely the selected row from queued 0/5 to unsolved 1/5 with a limited
partial note. At the 22:25 UTC check, current main had that row queued 0/5 because this
was an unmerged original draft; this is not a ledger inconsistency.

Unmodified original author and reviewer scripts were copied to ignored,
isolated directories, executed with /usr/bin/python3 and existing SymPy
1.14.0, and compared with their original adjacent receipts. Both exit zero
and reproduce byte for byte. The author receipt covers nine adjoint models
and 52 abelian identities; the reviewer covers nine models and three cyclic
characters. Present reproducibility does not attest past execution.

The new independent script passed 232 exact assertions using only the
standard library. Its mechanisms include actual rational permutation
projectors, exterior Cauchy dimensions, first/last-letter module bijections,
ordinary abelian homology boundaries, and the 2017 alternating-functional
counterexample. Eight negative controls are rejected: a dropped sign,
symmetric replacement for exterior Cauchy, doubled q=1, missing exterior
twist, confusing dim E=1 with q=1, symmetric abelian homology, the false
general coinvariant guess, and inference of a kernel from an Euler
difference. The Sym² degree-three action has rank 8 in a 9-dimensional
codomain, leaving a nonzero exterior-cube class. These finite controls test
conventions and overreach; the universal proof supplies the general
reduction, and neither supplies the missing general decomposition.

## Dataset, source bytes and attestation limits

The cached raw problems and reports match the declared pinned dataset
revision `37e53eabe540fb458758e198be61634bd02ee008`. Independent Hugging Face
LFS metadata at that exact revision confirms both sizes and SHA256 values.
The target ID occurs once among 15,458 records. The raw source, read-only
SQLite payload and frozen source_record agree exactly. The source's problem
number joins to no prior report, so the prior is the empty object. Full-target
searches of the dataset and recorded related-target groups found no second
matching target under the stated search criteria; this is not a theorem that
no differently worded duplicate can exist.

Actual queue.py semantics hash the source and prior context using
SHA256(json.dumps([source,prior], sort_keys=True).encode()). With an empty
prior this reproduces readiness.review_hash
`0fb4d607f5e9cce2db158be17ff5c02f3b64ff2510ea911ed9b5c18490812ca6`.
It is correctly a context digest, distinct from the mathematical review file
hash. The original review summary correctly binds its own note/review/script.
No hash repair is warranted for the readiness field.

Fresh Gadish–Hainaut and Powell v4 hashes equal the original source-checksum
records. The fresh OWR PDF differs from the recorded original hash; the old
PDF was not included, so historical byte identity is unverified. Current
literal source identity and target are independently established. Source
chronology is also qualified: the OWR workshop and journal volume are 2018,
but EMS reports publication on 5 January 2019. The raw 2019 citation need
not be an error. EARLY_CORRECTIONS.md preserves correction of this family's
overly categorical early sentence without changing its seal.

The thirteen files contain author/reviewer model and reasoning labels and a
one-turn timestamp ledger. They do not contain raw historical queries,
prompt/response transcripts or model telemetry. Those labels, historical
independence and complete historical search coverage remain attestations.
This audit records its current reads, proof, exact runs and byte identities;
it does not infer the missing history from successful replay.

## Actionable qualifications for the parent

1. Describe actual PR scope as thirteen attempt files plus the selected queue
   row. The original PR-body claim that all changes are inside the attempt
   folder is false.
2. Qualify historical PDF byte identity and historical execution/model/query
   claims as above. Keep the original receipts and add current evidence;
   do not silently replace history.
3. Limit phrases about “current literature” and “unrestricted decomposition
   remains unresolved” to this investigation and the checked sources. No
   global absence statement was established.
4. Distinguish 2018 workshop/volume, 2019 report publication, December 2025
   arXiv v4, and March 2026 journal publication. Preserve raw dataset bytes.

No canonical repair was performed by this family. The parent owns integration
and a fresh current-head gate after any changes. This report closes only the
original-head audit and does not bless future bytes.
