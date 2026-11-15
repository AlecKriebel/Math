# Binary consequences of relation-liveness automata lower bounds

Alec Kriebel — ORCID https://orcid.org/0009-0001-9320-500X
Preprint date: October 6, 2026. License for this new note and its original
supplementary materials: Creative Commons Attribution 4.0 International,
https://creativecommons.org/licenses/by/4.0/ . Upstream source copies retained
for local audit have their own Apache-2.0 license and are not in the deposit ZIP.

The explicit binary language K_h is the row-major h²-bit encoding of nonempty
products of relations on h points. It rejects every incomplete block and
accepts the empty word. There is an endmarked one-way NFA with exactly
N_h=(3h³−h)/2+2 states and an ordinary epsilon-free 1NFA with N_h−1 states.
Every ordinary one-way NFA for this particular language needs at least h³ states.
The source expansion is therefore of optimal cubic order for this convention.

Using the two independently inspected OpenAI relation-alphabet theorems,
every equivalent s-state binary 2DFA satisfies
2^floor((h−2)/31) ≤ 4(sh²+2)². Every binary 2NFA for the complement in all
binary words satisfies 2^floor((h−2)/127) ≤ 2(sh²+1), under zero-step finite
acceptance. Thus both target costs are 2^Ω(N_h^(1/3)). All counts include
initial and accepting states; targets have two distinct markers, partial
transitions, stays, unrestricted left/right motion and finite-run acceptance.
Infinite nonaccepting computations reject. The manuscript supplies the
positive-run complementation variant and explains disabled outward moves.
The machine-checking code expects outward transition entries removed first;
this normalization costs no states and matches the disabled-boundary convention.

The exponential lower-bound engines are inherited from OpenAI family 129.
The original liveness family is due to Sakoda and Sipser. Binary adjacency
coding is established machinery appearing in Kapoutsis 2011/2013. The
paper is an explicit fixed-binary consequence, with complete compilers,
complement-universe accounting and a strict-alignment source lower bound.
There is no claim of being first, an independent base-conjecture proof,
2^Ω(n) in binary source states, or L≠NL. Alternative total encodings can
have different source costs. The priority audit records relevant previous
coding disclosures and the distinction between manuscript dates and public
release dates.

`main.tex` is standalone and contains its bibliography. `paper.pdf` is the
actual exported six-page paper. `verification.zip` contains original
compiler code, independent checks, audit reports and pinned source hashes.
The exact deposit file list and metadata are in `zenodo-deposit.json`.
Published-state receipts and tracker readback are retained separately in the
project repository after their operations; a reserved draft DOI is not publication.

Reproduce from the extracted verification package using Python 3.10+:

```text
python3 code/binary_compiler.py --output compiler-results.json
python3 reviews/reduction_adversary_check.py
python3 agent_notes/determinization_algebra_check.py
python3 agent_notes/upstream_algebra_check.py
```

All scripts use only the standard library. The recorded run used Python 3.14.6.
Compiler checks include 1,534 exhaustive source words, 288 exhaustive partial
one-state deterministic targets, 128 seeded nondeterministic targets, and
227,136 pullback comparisons. A separate independent implementation also
checks the ordinary source and disabled outward entries: 4,472,832 pullback
comparisons, 20,515 fooling crosses and 4,369 complement identities. These
finite checks support, and do not replace, the uniform proofs in the paper.
Original upstream algebraic counterexample checks cover Brauer diagrams
through degree 4 and all width-one / sampled width-two relation diagrams.

Build the PDF with a current LaTeX distribution (amsmath, amssymb, amsthm,
lmodern, geometry, hyperref), or with Tectonic 0.16.9:

```text
tectonic main.tex
```

The output main.pdf is equivalent to paper.pdf. PDF bytes can differ because
build timestamps differ. The built-in Codex standalone compiler also reported
success. All pages of the deposited PDF were rendered and visually inspected;
no missing references, overfull text or omitted formulas were found.

The source pin is openai/math adc7f1241b42e322a6451854ab7e4b4c146bf78a.
Exact source hashes and manuscript-specific BibTeX are recorded in the
verification package. Both original proof mechanisms and actual Lean
statements/semantics received separate independent automated audits.
A byte-identical 41-module reduced import kit is retained locally under
sources/lean_check with reproduction instructions. Lean 4.34.1 was present,
but the upstream build, axiom printing and Comparator execution were not
reproduced because dependency fetching exhausted local disk capacity.
Source scans and matching signatures do not establish kernel verification.
The new binary results have not been formalized. Manual proof audits, not
a claimed successful Lean build, are the dependency validation basis here.

AI tools were used extensively in research, drafting and verification.
Automated adversarial reviews are not human peer review. This preprint has
not undergone conventional human peer review or refereeing. No affiliations
or coauthors are asserted, and no external individuals were contacted.
