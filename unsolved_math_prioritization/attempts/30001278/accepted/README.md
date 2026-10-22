# Sharper local ramification bounds: scoped partial investigation

Problem 30001278 / OWR-3480-009, queue rank 971. Prepared 2026-10-07.

**Disposition: unresolved by this investigation after five mathematical approaches.** No counterexample to the original inequality, complete proof, novelty claim, or independent-review claim is made here. This is a source-free author packet awaiting separate mathematical audit.

The source is Conjecture 3 in Xavier Caruso's contribution to *Algebraische Zahlentheorie*, Oberwolfach Report 30/2009, printed pp. 1709–1712, especially p. 1711. It concerns **semistable** representations. The supplied crystalline-only formulation is a subcase; the final paragraph of that contribution raises a separate question about further crystalline improvements. The two questions must not be conflated.

Write

\[
\frac r{p-1}=p^a b,\quad a\geq0,\quad p^{-1}<b\leq1,
\qquad B=1+e(n+a+b)-p^{-(n+a)}.
\]

The target is \(v_K(\mathcal D_{L/K})\leq B\). All positive results below actually give a strict inequality. They apply to the source's semistable setting unless a narrower class is explicitly stated.

## Results

1. Caruso's later upper-ramification theorem gives the desired different bound whenever \(r\geq p^a+1\). It does **not**, as a statement alone, give it throughout the complementary bands. The exact loss is calculated in `01_UPPER_BREAK.md`.
2. A Kummer-tower reduction isolates the missing relative different estimate, its required precision, and its endpoint. `02_KUMMER_TOWER.md` proves the reduction and an optimization identity; the missing estimate is expressly conditional.
3. The older Caruso–Liu method already yields the target if \(p^{n-1}\mid r\), including all \(n=1\). The binomial proof and an exact obstruction to simply replacing its monomial annihilator by \(u^{er}\) are in `03_HEIGHT_ANNIHILATORS.md`.
4. A direct cyclotomic calculation proves the target for arbitrary-rank integrally split sums of unramified twists of cyclotomic powers. An explicit crystalline lattice shows why rational splitting and semisimplification do not justify that reduction. See `04_CYCLOTOMIC_LATTICES.md`.
5. An elementary different estimate proves the target whenever \(v_p(e(L/K))\leq n+a\). In rank \(d\), a sufficient condition is \(d^2(n-1)+d(d-1)/2\leq n+a\). In particular, every rank-one case is covered. See `05_INERTIA_ORDER.md`.

These are overlapping sufficient conditions, not a classification. For example, the unrestricted lattice problem at \(p=3,e=1,n=2,r=7\) is not settled by these arguments: here \(a=2,b=7/18,B=871/162\), whereas the quoted upper-break theorem gives \(11/2\). An arbitrary crystalline lattice of rank at least two is not known, from the inputs used here, to satisfy either the inertia-order condition or the special splitting condition. This example identifies a gap in this packet; it does not assert that this exact subfamily is open in every part of the literature.

## Credit and literature boundary

- Caruso–Liu, *Some bounds for ramification of p^n-torsion semi-stable representations*, J. Algebra 325 (2011), 70–96: the original bound, its sharpened conjecture, the relative-field method, and useful annihilator bounds.
- Caruso, *Représentations galoisiennes p-adiques et (φ,τ)-modules*, Duke Math. J. 162 (2013), 2525–2607: the sharpened **upper-break** theorem, Theorem 3.28 in the inspected 2012 manuscript. Its proof sketches an adaptation of the earlier method. This packet neither disproves that adaptation nor upgrades the displayed theorem to the different claim without the bridge identified here.
- Hattori's 2009 theorem and Fontaine–Abrashkin results settle additional low-weight situations; they are credited in `SOURCE_MAP.md` and are not presented as new work.
- In particular, Fontaine's finite-flat bound covers every crystalline r=1 case, with arbitrary e and n. This separately credited literature input is stronger than the target there; it does not turn the five arguments into a complete higher-weight solution.
- Čoupek's 2026 published articles provide current crystalline/cohomological refinements in their stated scopes. The inspected Wach-module theorem is mod \(p\), absolutely unramified, not an unrestricted mod \(p^n\) theorem.

The search did not establish the global current status of the exact different conjecture. In particular, the absence of a separately displayed theorem in the sources inspected is not proof that no published argument implies it.

## Reproduction

Run `python3 -B verify.py` from this directory. It uses only the Python standard library and reproduces the exact finite-control summary in `CHECK_RESULTS.json`. Run `python3 -B negative_controls.py` for the boundary controls recorded in `NEGATIVE_RESULTS.json`. Both commands also work under `python3 -B -O` and from an isolated copy containing only this packet. The controls test formulas, independent polynomial reductions, parameter boundaries, lattice matrices, and rank/order arithmetic. They do not compute arbitrary ramification fields, verify p-adic Hodge-theoretic comparison theorems, or prove an infinite statement by sampling.

`SOURCE_METADATA.json` contains public source URLs, PDF sizes and SHA-256 fingerprints, inspected locations, and corpus fingerprint/match metadata. No downloaded PDF, source extract, dataset contents, or private coordination material belongs in this packet. `MANIFEST.json` binds all other public author files.

For an externally anchored check, pass `--expected-manifest-sha256 DIGEST` to `verify.py`, using the digest from the separately retained freeze receipt. A manifest stored beside its own files establishes internal consistency; by itself it cannot prove authenticity or prevent coordinated replacement of both files and manifest. The exact allowlist rejects additional source files, nested directories, and symlinks. `CLAIM_LEDGER.json` makes each conclusion and its missing extension explicit. No independent audit has yet been completed.

The five mathematical approaches are the five numbered notes, not the source retrieval, gate, verification, packaging, or any later audit. All were performed in this investigation; no historical turn count has been inferred from tool-call counts.
