# First Voronoi intersection numbers: audited partial results

Problem 30001017 / OWR-2049-004, rank 662. **Unsolved; five of five approaches exhausted.**

This package preserves all 14 frozen author files and all eight independent audit files byte for byte. The audit accepts only an unresolved partial-results packet, subject to both additive clarifications reproduced below. The original author README and STATUS record the historical pre-audit state; the completed audit and this guide supply the later disposition without rewriting that history.

## Controlling reading order

Read this guide and `audit/CORRECTIONS.md` together with `author/PROOF.md` and `author/SOURCE_ISSUES.md`. The projection-formula proof below replaces the proof of Lemma 6.1 for its general statement, eliminating the unstated positivity hypothesis. The OWR warning supplements the source normalization notes. These clarifications control wherever the frozen author discussion differs. The full report is `audit/AUDIT.md`; `audit/AUDIT_BINDING.json` identifies the exact frozen author archive.

The genus-five stack intersection L^2 D^13 remains unevaluated. Finite calculations for N=9 do not evaluate N=13. The known strict EGH range does not cover this missing zero. No full proof, geometric counterexample, new geometric value, or novelty is claimed. Numerical inconsistencies reported for the inspected arXiv:0707.1274v1 are not transferred to the uninspected 2010 journal text. Formula evaluations in genera 6 through 10 are diagnostic arithmetic comparisons, not certified new geometric intersection values.

## Offline verification

Run `python3 -B verify_release.py` from any working directory, using the script's path if needed. Only Python's standard library is required. The verifier rejects unexpected paths, altered bytes, symlinks, changed correction binding, and archive/member mismatches. It replays both independent arithmetic programs, requires byte-identical saved outputs, and checks the frozen manifests and author-archive binding. `python3 -O -B verify_release.py` also retains the release integrity checks; the frozen assertion-based programs are deliberately executed without optimization.

The two ZIP archives contain only the corresponding authored safe subpackets. No third-party PDFs, extracted source text, dataset records, or private coordination files are distributed. Public source titles, URLs, hashes, sizes and inspection limits are in the author and audit source-verification files.

## Controlling clarifications (verbatim)

# Additive audit clarifications

These clarifications accompany, and do not alter, the frozen author packet.

## 1. Proof of the numerical birational-support lemma

In PROOF.md Lemma 6.1, the abstract statement does not assume that ell has a globally generated positive multiple. The hyperplane proof therefore uses an unstated hypothesis if applied to arbitrary bases. The numerical conclusion nonetheless follows directly from proper pushforward, without positivity.

Write q=p composed with f and let

    Delta_N = ((D')^N - (f^*D)^N) cap [X'].

This is a cycle of dimension n=G-N represented on Z, because every term of the binomial expansion contains E. For each n-dimensional component V of a representative, the image q(V) has dimension at most s<n. By the definition of proper pushforward of cycles, q_*[V]=0. Therefore q_*Delta_N=0. The projection formula then gives

    degree ((q^*ell)^n cap Delta_N)
      = degree (ell^n cap q_*Delta_N) = 0.

The remaining pullback term has the required degree on X because f_*[X']=[X]. This proves the stated equality of degrees for rational Cartier ell, D, and D'. Degrees can be taken on the proper image of X if necessary. The analogous argument applies in the stipulated rational stack intersection theory.

For the actual Satake/Hodge application, a positive multiple of ell is globally generated, so the author's hyperplane argument also applies. The correction removes the unnecessary mismatch between the general lemma's wording and its proof; it does not strengthen the genus-five result.

## 2. Additional OWR rank-one normalization warning

Add to SOURCE_ISSUES.md's OWR cautions: the displayed rank-one recurrence on printed p.2188 omits a factor 1/2 when the Hodge degrees and boundary are interpreted with the stack conventions used in the packet. The degree-two Kummer cover requires

    a_g^(g) = (1/2)(-2)^(g-1)(g-1)! H_(g-1).

For genus three this is 1/720, in agreement with the report's own p.2187 table; the displayed recurrence without 1/2 would give 1/360. The author packet already uses the correct formula, so its computations are unchanged. This observation concerns the inspected OWR report and is not a claim about another version of EGH.
