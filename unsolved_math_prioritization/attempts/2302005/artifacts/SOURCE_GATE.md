# Source and status gate

## Exact formulation

The catalogue entry is **2302005 / AMR-022-2005**, *Research Problems in Function Theory — Problem 2.5*. Its live page was inaccessible during this check, so a pinned record supplied the statement, then the mathematical statement and update were checked directly against the source edition.

The class is entire functions on the complex plane. There is no growth-order restriction, finite-order assumption, derivative normalization, univalence assumption, or prescribed Taylor coefficient. Values are finite complex numbers. An angle is an open sector of positive aperture, with vertex at zero; each such angle must contain infinitely many distinct preimages. Equivalently, for every angular interval and every radius there is a preimage outside that radius, for nonconstant entire functions.

The explicit terminal question asks whether exactly two values can have this property. The preceding invitation to describe possible sets does not supply a separate, precise classification conjecture. This record settles the terminal question by an existing theorem and gives its verified realization class. It does not present a full classification.

## Primary source trail

1. **Original question.** Gol’dberg's reference [1], p.199, identifies C. Rényi, Problem 3, lecture notes for the Summer Institute on Entire Functions, University of California, American Mathematical Society, 1966, p.P-1. The original lecture-note leaf was not independently retrieved. Gol’dberg's p.191 explicitly identifies Rényi's two-point question and says that his theorem answers it affirmatively.
2. **Original solution.** A. A. Gol’dberg, *О распределении значений целой функции по аргументам*, *Acta Mathematica Academiae Scientiarum Hungaricae* **19** (1–2), 1968, pp.191–199. [Archive record](https://real-j.mtak.hu/7416/), [journal-volume scan](https://real-j.mtak.hu/7416/1/MTA_ActaMathHung_19.pdf). The theorem is on p.191, its construction on pp.192–194, the interpolation lemma proof on pp.194–198, and the references on p.199. The paper was received on 24 April 1967; its proof-added note is dated 4 December 1967. These dates do not change the publication year 1968.
3. **Problem-list source.** W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), 21 September 2018. Problem and Update 2.5 are on printed p.24; references [310] and [311] on p.221 point to the same 1968 volume/pages under English and German title descriptions. The original article is in Russian.
4. **Approximation dependency.** The original proof invokes M. V. Keldysh, *О приближении голоморфных функций целыми функциями*, Doklady AN SSSR **47** (4), 1945, pp.243–245, and S. N. Mergelyan, *Uniform approximations of functions of a complex variable*, Uspekhi Mat. Nauk **7** (2), 1952, pp.31–122. [Mergelyan bibliographic record](https://www.mathnet.ru/eng/rm8302). The relevant classical approximation step is identified in the proof verification. It is an external theorem, not reproved here.

## A necessary scope correction

Gol’dberg's main theorem states: a **bounded, closed, at-most-countable** set \(A\) can be realized exactly. His proof-added note on p.198 broadens this to **bounded at-most-countable** \(A\), obtaining
\[
 A\subseteq D(G)\subseteq\overline A.
\]
The 2018 update summarizes a countable-set sandwich without repeating boundedness. No unbounded version is inferred from that summary. The main theorem alone applies to \(A=\{0,1\}\), so this discrepancy does not affect the answer to the concrete question.

The notation \(D(G)\) in the original paper uses density of the arguments of preimages. Its exact equivalence to \(E(G)\) for nonconstant entire functions is proved in the verification note; the difference in wording is not a gap.

## Prior work and related targets

The available initial triage said only that the statement was read and a web search found nothing. The main-branch row was still queued at 0/5. Bounded repository file and commit searches for the identifier and relevant Rényi/Gol’dberg terms found no earlier substantive attempt. The main attempt-directory listing had no directory for this ID. The repository's related-target groups had no match. Local matches outside this investigation were queue snapshots rather than mathematical treatments.

Catalogue **2302004 / AMR-022-2004**, Problem 2.4, concerns different exceptional values at different Julia lines. It is related and the same 1968 article is cited in that source update, but it has different quantifiers and is not a duplicate of the two-value realization problem. No status change or resolution of that other target is included here. The disc lacunary-series problem 2305036 also contains the phrase “every angle” but is mathematically different.

## Current-status conclusion

A bounded search of later sources was performed on 3 October 2026. It did not locate a later correction invalidating the published two-value construction. More importantly, no recent result is needed: the original 1968 theorem directly answers the exact question. This is a correction of stale source triage, not a claim that a previously open problem has now been solved.

Full source PDFs, source-page images, corpus records, and private operational material are not part of this public package.
