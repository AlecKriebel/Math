# Independent adversarial automata audit — PR 781 / problem 4600024

Frozen target: `4a38c3ccc4cac918fb75fd4b97449f3ebd2e0f7f`. The parent confirmed this target's queue eligibility (`claimed_solved3/5`). This report audits only the automata family for that frozen target. It makes no novelty or current-literature-status claim.

**Verdict: PASS within the assigned mathematical scope.** I found no unsupported step in the claimed effective criterion, assuming the published PRZ theorem. The exact remaining mathematical gap in this family is **none identified**. This is independent deductive verification of the reduction plus finite diagnostics, not a new proof of PRZ or empirical certification of all inputs. Overall publication and full-project decisions remain with the parent auditor.

The initial assessment was recorded before consulting primary-source results or any historical/sibling audit. Only the selected public record and the author's `PROOF.md` and `verify_math.py` were initially read. No historical audit, sibling review, or parent conclusion was consulted at any point.

## Exact claim and assumptions

Input: a nonempty two-sided irreducible sofic shift T over a finite alphabet A, a specified surjective block map f:T→T, a finite memory/anticipation window of length ell, and an arbitrary total completion F of that local rule on A^ell. Mixing is a sufficient stronger assumption. Containment of T in an SFT is non-strict.

Let L be its finite-word language, including epsilon, and B={w:F_*(w)∉L}, with F_*(w)=epsilon for |w|<ell. For any common finite recognizing monoid M, put k=4(|M|+1) and N=max(2,ell,k). The audited claim is:

`an SFT-neighborhood extension exists ⇔ L and B are LT-separable ⇔ L(T[N])∩B=∅ ⇔ F(T[N])=T`.

Failure of this one finite test excludes extensions with other completions, other finite radii, and larger ambient alphabets. Surjectivity is needed for the final equality; it is not needed for the other existence implications.

## Primary-source check

[Boyle, original problem list](https://www.math.umd.edu/~mboyle/papers/openfinalsub3nov2007.pdf), printed page 17, Problem 16.3, agrees with the prescribed-map target. Its neighboring Problem 16.2 has different quantifiers and an extra fixed-point hypothesis; neither is silently imported here.

[Place–van Rooijen–Zeitoun, LMCS 2014](https://lmcs.episciences.org/1163/pdf), printed pages 8–9, Theorem 4.2, supplies LT separation at k=4(|M|+1) when a finite morphism recognizes both input regular languages. Printed pages 4 and 6 specify actual-letter positions, a left half of floor(k/2), a right half including the current letter, truncation at endpoints, and profile presence rather than counts. The author's convention matches. Printed page 5 confirms the common-monoid construction.

`SOURCE_CUSTODY.json` records URLs, response-body SHA-256, retrieval times, and page locators. Both actual PDF bodies were fetched and read in memory. No third-party PDF or full extracted text is retained in this package. This direct source inspection was not a fresh unfinished-proof or literature search.

## Independent deductive verification

1. **Regular ideal and common monoid.** Factoriality of L makes B a two-sided ideal: the output block from w survives inside the output from uwv, with only a coordinate translation. Empty and short words cause no exception because T is nonempty. A complete DFA for L, coupled to the last at most ell−1 input symbols, gives a complete DFA for B. The total transition maps on the disjoint union of the two DFAs form a finite monoid recognizing both languages: evaluate each transformation at the corresponding initial state and test that DFA's final-state set. Thus the required common morphism is supplied, rather than merely two unrelated recognizing monoids.

2. **All radii and completions.** If G:S→T is any extension, restrict S to A^Z when necessary. A sufficiently high canonical approximation T[q] lies in S because every word forbidden in S is absent from T. Pad F's and G's windows to one interval J. Their rules agree on every J-word in T. For n at least q and |J|, every J-word in T[n] occurs in T, so F=G on T[n]. This is a finite local argument, without an assumed convergence/stabilization bound. Conversely, any such canonical witness is an extension. Bad finite words are equivalent to bad output points by the definition of a shift language.

3. **Graph language and separator.** Irreducibility connects any two (n−1)-words and hence makes the canonical overlap graph strongly connected. Every finite path therefore extends on both sides. Labeling edges by their appended symbol and taking every vertex initial/final gives exactly L(T[n]), including short words: a finite path label is a factor of a bi-infinite label path, and every point of T[n] has that presentation. It is not necessary to emit the initial vertex's word. Long words are accepted precisely by their allowed n-factors; short words are the finite allowed exceptions. This language is LT and supplies a separator whenever a canonical extension exists.

4. **Saturation, checked directly.** Suppose an LT[k] separator exists and a bad w appears in T[n], n≥max(2,k). Irreducibility produces U∈L containing every n-word and long enough to contain both endpoint regions. Strong connectivity in T[n] produces W=UcwdU in its language; the ideal property puts W in B. Irreducibility in T produces V=UeU∈L. Both have exactly L_n(T) as n-factors. Consequently both have exactly L_k(T) as k-factors, and share prefix/suffix of length k−1. Every full profile is a split k-factor; every truncated profile lies in the common boundary words. V and W therefore have identical published profile sets. Their lengths exclude simultaneous truncation at both endpoints. The separator cannot distinguish them, a contradiction. This proves saturation at every n≥max(2,k), rather than at a sampled cutoff.

5. **Finite termination.** For a d-state allowed-language DFA, the bad-language DFA has at most `d * sum(|A|^i for 0≤i<ell)` states. If the disjoint DFA union has D states, its transition monoid has at most D^D elements; closure from identity under letter transformations terminates. After computing N, enumerate the finitely many length-N words and build the overlap graph. It has at most |A|^(N−1) vertices. Reachability in its product with the B-DFA is a finite exact emptiness decision. There is no input-word cutoff or unbounded radius search in this algorithm. These bounds are existence/termination bounds, with no practical efficiency claim.

## Diagnostics and falsification controls

`independent_automata.py` is independently authored and imports no author code. Its recorded output contains 38,652 passing assertions:

- 64 width-two local-rule cases compare a separately built bad DFA against direct output words through length eight. These include arbitrary rules outside the self-map hypothesis solely to test the transducer.
- Canonical graph languages through n=4 agree on all binary words through length seven for the full shift, even shift, golden mean, singleton, and irreducible nonmixing period-two shift.
- Common transition monoids recognize both allowed and bad identity languages. Sizes are 7 for the even shift, 6 for golden mean and period two, 2 for the singleton over the binary alphabet, and 1 for the full shift.
- An exact finite closure over LT[3] signatures and the two input DFAs finds the even-shift collision good `011110`, bad `01110`. The other identity controls have no collision. This diagnostic explores a finite state space to exhaustion on the no-collision cases; it is not a bounded word search.
- Explicit saturation checks cover odd/even k=2,3,4. All eight completions of the width-three identity on the golden mean pass its canonical witness test.
- Negative controls detect dropping endpoint data (`01010` versus `010101`), using an untrimmed graph, and using only one initial vertex. A nononto constant map passes extension emptiness, exposing why output equality needs surjectivity.

The separate original-author replay passed 3,456 checks. None of these finite diagnostics establishes the general theorem; the independent deductions above and the imported theorem do that work. Hypothesis boundaries tested or inspected include nonempty/short words, unused alphabet symbols, periodic irreducibility, SFT identity positives, non-SFT identity negatives, changed completion, larger radius, and ambient alphabet restriction. Reducible inputs and empty shifts are outside the audited theorem.

## Reproduction and custody

From this folder, using any Python 3 with the standard library:

```text
python3 -I -B independent_automata.py
python3 -I -B ../original/unsolved_math_prioritization/attempts/4600024/author/verify_math.py
python3 -I -B verify_custody.py --selftest
python3 -I -B verify_custody.py
python3 -I -B verify_custody.py --sources
```

The last command optionally refetches and compares the primary PDF response hashes in memory. It may fail if those upstream response bodies later change. The frozen manifest covers every authored file except itself, rejects additions/deletions/content changes and nonregular objects, and checks the three initially read source snapshot hashes. Integrity controls use only disposable descendants of this folder and include a symlink and FIFO without following/opening them. The supplied Git head is parent-confirmed; this subaudit verifies source content hashes and makes no independent Git object-provenance claim. No Git mutations or external communications were made.
