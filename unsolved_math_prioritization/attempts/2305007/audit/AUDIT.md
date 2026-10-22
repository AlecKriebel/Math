# Independent audit of Function Theory Problem 5.7

Problem 2305007 / AMR-022-5007. Audit date: 2026-10-06.

## Decision and exact scope

**Accept as a credited historical resolution, with the original-paper verification limit preserved.** The disposition `already_solved` is justified for the actual request for a nontrivial omitted-value sufficient condition, together with the proposed shrinking-inradius implication. Positive sufficient conditions are known; the proposed implication is false for general holomorphic maps. This packet does not establish a necessary-and-sufficient classification of every omitted-value set, claim a new solution, or independently reconstruct the analytic counterexample theorem.

The author used one substantive historical-result route, within the stated limit of five. The elementary supporting arguments are valid. No mathematical correction to the frozen author packet is required. Acceptance of the historical negative conclusion relies on an explicitly identified literature attribution; the proof in Fernández's original 1984 paper remains uninspected.

If a downstream classification requires an independently re-proved counterexample theorem, this packet does not meet that stronger requirement. The machine-readable acceptance record separates historical resolution from original-proof verification.

## Evidence and the apparent status conflict

[Hayman and Lingham, Research Problems in Function Theory, arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200v2), printed pages 86, 87 and 100, was inspected in text and page images. Update 5.5 reports Fernández's obstruction for polar complements and Pommerenke's sufficient condition for Bloch domains with positive-capacity complements. Update 5.7 gives a positive result for universal covering functions but retains an open-status line for subordinate maps. Update 5.40 explicitly reports Fernández counterexamples for arbitrary maps into domains whose inradius shrinks at infinity and whose complements have capacity zero. Thus the open-status line cannot consistently describe that same unrestricted suggestion.

The [publisher record for Fernández's article](https://annals.math.princeton.edu/1984/120-3/p04) confirms the title, volume 120, year 1984, pages 505–516 and DOI [10.2307/1971085](https://doi.org/10.2307/1971085). It supplies no theorem or proof text. Direct publisher/JSTOR inspection and bounded exact-title searches did not yield the original full article. No theorem number, original-paper theorem page, or inspection of its construction is claimed. The source collection is primary evidence for its own problem/update wording and a secondary attribution of the original theorem.

## Quantifiers and the imported dependency

Let Delta denote the open unit disk. The precise external assertion used by the author is:

For every planar domain D with polar complement, there exists a holomorphic map f from Delta into D such that its Taylor coefficients fail to tend to zero.

This is an existential counterexample for each permitted D. It is not a claim that every map into D has nonvanishing coefficients; constant functions alone would refute that interpretation. The author uses the correct quantifier order.

A universal covering map F of D is a particular holomorphic function. A theorem giving vanishing coefficients for F need not give the same conclusion for every holomorphic f into D. With a compatible choice of base point, the lifting property expresses such an f as F composed with a disk self-map, but coefficient decay has no automatic preservation under that composition. The author never assumes such preservation and does not confuse range containment with surjectivity.

Capacity means logarithmic capacity/polarity here, not area or analytic capacity. A domain can be a Bloch domain while having a polar complement. The reported positive-capacity sufficient condition therefore cannot be applied to the author's punctured domain.

## Independent check of the punctured domain

For m at least 1, take the m equally spaced points on the circle of radius sqrt(m), and let E be their union. A closed disk of radius R meets only shells with m at most R squared. Consequently E is nonempty, countable, closed and locally finite. Its complement D is open and unbounded.

To verify connectedness, start with a segment between two points outside E. The segment meets only finitely many E-points. Choose small pairwise disjoint disks around those points, avoiding the endpoints and all other E-points, and replace the corresponding segment pieces by boundary arcs. This produces a path in D. Thus D really is a planar domain, as required by the imported theorem.

Every compact subset of E is finite. For a nonempty finite set, each probability measure has an atom, so its logarithmic energy has an infinite positive diagonal contribution. The negative part of the kernel is bounded below on that compact set and cannot cancel it. Hence every such compact set has logarithmic capacity zero. Equivalently, E is a countable union of polar singletons and is polar. This is the appropriate capacity-zero interpretation for the unbounded E.

Now fix w with r = |w| at least 1. Set m = ceil(r squared), R = sqrt(m), and choose a nearest angular point e in the m-th shell. Its angular separation from w is at most pi/m, including the wraparound interval. Therefore

    |w-e| <= (R-r) + pi R/m.

Since 0 <= m-r squared < 1 and R >= r,

    R-r = (m-r squared)/(R+r) <= 1/r,
    R/m = 1/R <= 1/r.

Thus dist(w,E) <= (1+pi)/r uniformly in the argument of w. If r squared is an integer, the radial term is zero, so shell thresholds create no exceptional case. A slightly sharper constant is possible but unnecessary.

For |w| at most 1, the puncture 1 belongs to E and gives dist(w,E) <= 2. Accordingly D contains no disks of arbitrarily large radius and is a Bloch domain. Its circlewise inradius tends to zero.

For an f furnished by the imported assertion, its range Omega is open because f cannot be constant. Since Omega is contained in D, its circlewise inradius is bounded by that of D. Centers outside Omega contribute zero, so circles missing the range cause no definition problem. The result is

    d_f(r) <= (1+pi)/r for r >= 1,

although the Taylor coefficients do not tend to zero. No explicit formula for this f has been constructed, and the elementary geometry does not replace the analytic existence theorem.

## Independent check of the positive condition

Suppose the image of f lies in a horizontal strip |Im f-c| <= M, where M is nonnegative and finite. Put v = Im(f-ic). On every input circle of radius t less than 1, the power series converges uniformly. The positive and negative n-th Fourier modes of v have respective coefficients a_n t^n/(2i) and -conjugate(a_n)t^n/(2i). Parseval therefore gives

    mean(v squared) = (Im a_0-c) squared
                     + (1/2) sum_{n>=1} |a_n| squared t^(2n)
                     <= M squared.

Monotone convergence of the nonnegative series as t increases to 1 gives square summability of the positive-index Taylor coefficients and hence their convergence to zero. This requires no continuous boundary extension. When M = 0 the same formula forces every positive-index coefficient to vanish. The strip condition is not simply boundedness of f: the principal logarithm of (1+z)/(1-z) has bounded imaginary part and unbounded real part.

The source's positive-capacity Bloch-domain criterion supplies a substantially broader historical sufficient condition. The strip argument is an independent elementary check, not a priority claim and not a substitute for inspecting that broader theorem's proof.

## Independent check of the rate limitation

Given any positive null sequence epsilon_n, choose strictly increasing n_k such that epsilon_(n_k) <= 4^(-k). This is possible at every stage because the sequence tends to zero. The series with coefficient 2^(-k) at n_k and zero elsewhere converges absolutely and uniformly on the closed disk, with modulus at most 1. Its coefficient-to-epsilon ratio at n_k is at least 2^k and is therefore unbounded.

This defeats any prescribed pointwise null rate shared by all bounded functions, even allowing a multiplicative constant depending on the individual function. It does not deny square summability of bounded-function coefficients, stronger conclusions under special omitted-value restrictions, or the possibility of restrictions forcing constancy. The author states the limitation with the appropriate scope.

## Wording and classification safeguards

The target is coefficient convergence to zero, equation (5.11), rather than merely bounded coefficients, equation (5.10). The geometric variable tends to infinity in the value plane. The Fourier variable tends to one in the input disk. A correct radial Parseval formula includes the factor t^(2n).

The original question asks for a nontrivial sufficient condition and suggests one candidate; it does not explicitly ask for a classification of all possible omitted sets. Both parts are addressed at their actual level: a classical positive criterion is reported, an elementary nonbounded-image criterion is proved, and the proposed general implication is negatively settled by an attributed older theorem. A hypothetical request for a full omitted-set characterization would remain outside this acceptance.

The audit makes no exhaustive modern-literature, all-repository, or novelty claim. It does not count metadata inspection as proof inspection. Historical credit stays with the cited authors.

## Integrity and reproducibility checks

The exact author ZIP and its seven static members matched the externally supplied archive and manifest digests. The six payloads matched the internal manifest, and all seven members matched the frozen disk bytes. Inventory checks rejected additional or missing files, duplicate names, unsafe paths, links, executable modes, corruption and inconsistent metadata. The complete three input JSON corpora were independently parsed; the target record, statement digest and complete review-pair digest matched. Only hashes, sizes, record counts and match results are recorded publicly.

A reviewer-owned data-only checker passed six clean modes: isolated normal and optimized Python, relocation in both modes, and hostile working-directory/import-path conditions in both modes. Thirteen negative-control cases were rejected in each mode, for 26 rejected runs. No archive member was executed. These are integrity tests, not computational evidence for the infinite mathematical assertions. Cache/entrypoint tests of an author certificate are inapplicable because no such executable certificate is shipped.

The original author freeze was left unchanged. This audit packet contains authored analysis and verification metadata only. It excludes source documents, extracted source text, source images, dataset records, and private coordination. No correction patch or replacement author artifact is needed, and no publication was performed in this audit.
