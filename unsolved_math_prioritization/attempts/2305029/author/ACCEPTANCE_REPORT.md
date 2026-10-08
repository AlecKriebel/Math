# Prescribed null boundary zero sets: prior-solution acceptance

Problem: **2305029 / AMR-022-5029**, Hayman Problem 5.29.  
Verdict: **Resolved affirmatively by prior published literature.**  
New substantive research turns: **0**. Verification date: **2026-10-08 UTC**.

## Exact mathematical target, in our notation

Write D = {z in C : |z| < 1} and T = {z in C : |z| = 1}. For each set E contained in T that is a countable intersection of relatively open subsets of T and has arc-length measure zero, the target asks for a bounded holomorphic function f on D, not identically zero, with a finite boundary limit at every point of T and boundary value zero at every point of E.

The problem uses the Hardy space H-infinity(D), not the disk algebra. It prescribes inclusion in the boundary zero set, not equality. Boundary evaluation means limits from inside D, not values assigned arbitrarily to a representative defined only almost everywhere. Normalizing arc length by 1/(2 pi) does not change the null sets. No hypothesis of closedness, countability, or zero logarithmic capacity is present.

## Source and theorem match

Hayman–Lingham's versioned 2018 source has Problem 5.29 and its affirmative Update 5.29 together on printed page 95 (PDF page 96); the update cites Danielyan as reference 181. Thus the imported “open as of 2018” assessment conflicts with its own cited source. [H]

Danielyan's published Theorem 1 provides, for every such E, an f in H-infinity(D) with positive real part in D, finite radial limits at all points of T, and radial zero set exactly E. His definition of a Fatou point on page 813 is existence of the radial limit. The theorem and proof are on pages 813–815. [D]

## Complete deduction of the requested conclusion

Apply [D, Theorem 1] with its set F equal to our E. The two set hypotheses coincide. Its resulting function belongs to the required function class. Since Re f(0) > 0, f is not identically zero. Its limits exist at every point of T; exact equality of the zero set with E implies the requested inclusion. This proves the target, conditional only on the expressly imported published theorem. For E empty, f = 1 also gives a direct witness.

The appendix below independently checks that replacing the radial convention with the usual finite nontangential convention would not change this verdict for bounded holomorphic functions. Unrestricted approach limits at every boundary point and membership in the disk algebra are not required or asserted here.

## Dependency and evidence separation

- **Imported mathematical result:** [D, Theorem 1]. Its construction uses Kolesnikov's Lemma 2, identified as [K]. That lemma is not independently reproved in this packet.
- **Independently proved here:** the exact hypothesis/conclusion deduction above and the radial-to-nontangential reduction below. The latter uses the standard normal-family theorem for uniformly bounded holomorphic functions and the identity theorem.
- **Inspected primary proof:** pages 814–815 of [D], including the positive-real-part series construction and reciprocal step. This inspection found no scope mismatch. It is not a formal proof certificate or a claim of independently reproving Kolesnikov's lemma.
- **Finite evidence:** three public PDFs were retrieved, hash-identified, and checked against the relevant theorem, update, and bibliographic locations. Packet integrity and deliberate-tamper controls check bytes and inventory only; they cannot prove an analytic existence theorem.
- **Stopping condition:** the direct prior theorem resolves the target before any new research approach. Literature review, source checks, and packaging consume zero substantive turns.

## Independent boundary-convention check

**Lemma.** Let f be bounded and holomorphic on D. If the finite radial limit of f at a point of T is L, its nontangential limit there is also L.

**Proof.** A rotation reduces the point to 1. Put

F(w) = f((w - 1)/(w + 1)), for Re w > 0.

F is bounded and holomorphic on the right half-plane, and F(t) tends to L as the real number t tends to positive infinity. For any positive sequence t_n tending to infinity, the functions F_n(w) = F(t_n w) are uniformly bounded. The normal-family theorem gives locally uniformly convergent subsequences. On each positive real x, F_n(x) tends to L. Every holomorphic subsequential limit is therefore identically L by the identity theorem. It follows that the full sequence F_n tends locally uniformly to L: otherwise a subsequence staying a positive distance from L on some compact set would itself have a convergent subsubsequence, a contradiction.

Now let z_n tend to 1 nontangentially, so |1-z_n| <= C(1-|z_n|) for one finite C. Set w_n = (1+z_n)/(1-z_n) and t_n = Re w_n. Direct calculation gives

t_n = (1-|z_n|^2)/|1-z_n|^2
    >= (1+|z_n|)/(C |1-z_n|),

so t_n tends to infinity. Moreover,

|Im w_n|/t_n = 2|Im z_n|/(1-|z_n|^2)
             <= 2C/(1+|z_n|).

Thus w_n/t_n belongs to a fixed compact vertical segment of the right half-plane for all sufficiently large n. The locally uniform convergence just proved yields

f(z_n) = F_n(w_n/t_n) -> L.

This holds for every nontangential sequence, establishing the lemma. The reverse implication follows because a radius is a nontangential approach. QED.

## References

[H] W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, 21 September 2018, Problem and Update 5.29, printed p. 95. Versioned source: https://arxiv.org/abs/1809.07200v2 ; PDF: https://arxiv.org/pdf/1809.07200v2 .

[D] Arthur A. Danielyan, *Rubel's problem on bounded analytic functions*, Annales Academiae Scientiarum Fennicae Mathematica 41 (2016), 813–816. DOI: https://doi.org/10.5186/aasfm.2016.4151 . Published PDF: https://www.acadsci.fi/mathematica/Vol41/vol41pp813-816.pdf . Versioned author preprint: https://arxiv.org/abs/1606.03116v1 .

[K] S. V. Kolesnikov, *On sets of nonexistence of radial limits of bounded analytic functions*, Russian Academy of Sciences Sbornik Mathematics 81:2 (1995), 477–485; Russian original, Matematicheskii Sbornik 185:4 (1994), 91–100. DOI: https://doi.org/10.1070/SM1995v081n02ABEH003547 . Primary bibliographic record: https://www.mathnet.ru/php/archive.phtml?jrnid=sm&option_lang=eng&paperid=892&wshow=paper .

The authored contribution of this packet is the acceptance audit and convention reduction, not a new solution of Rubel's problem. No source document, source passage, PDF, or dataset is redistributed.
