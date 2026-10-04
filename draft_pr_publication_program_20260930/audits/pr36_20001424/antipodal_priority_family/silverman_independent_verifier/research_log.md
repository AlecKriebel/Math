# Independent Silverman-source verification log

Scope: reconstruct consequences of Silverman's old printed class for live AIM Problem 2.6. New candidate attempts: **0**. No original PR36 report or other priority opinions were read before the proof seal. All writes remain inside this directory; no Git commit, push, remote edit, or external communication is performed by this delegated verifier.

## 2026-10-02 06:37:53 UTC - source checkpoint (35%)

- The required first source read was the literal live URL `http://aimpl.org/finitedynamics/2/`. The web fetch timed out; direct HTTP retrieval succeeded. Its Problem 2.6 asks: "Are all PCF maps defined over their field of moduli?"
- Root `AGENTS.md` read; `main` confirmed. No descendant `AGENTS.md` found in the research-program subtree.
- Independently hashed the parent-retrieved primary PDF: SHA-256 `0a405ab1fbe4fc04e73439ecc31db4afaae3d8e38ce58bfd49f65442c6e88116`.
- Rendered and visually read printed p. 271, Eq. (1), and printed pp. 295-298 (PDF pages 4 and 28-31), including Proposition 6.2, Corollary 6.3 and their operative proofs. Printed class: `phi_d(z) = i ((z-1)/(z+1))^d`, odd d. No audit opinion was used.
- Success criterion: independently prove algebraicity, degree >=2, PCF, absolute field of moduli contained in R, and absence of every real model for a map already printed there. Merely a descent-obstructed map without PCF would fail.

## 2026-10-02 06:39:09 UTC - deduction checkpoint (65%)

- Independent substitution for d=3 gives `1 -> 0 -> -i -> -1 -> infinity -> i -> 1`.
- Proposed centralizer argument uses the critical points `{1,-1}` and their values `{0,infinity}`; it reduces a possible nonidentity automorphism to `z -> -1/z`, whose commutation sign fails for odd d.
- Proposed descent obstruction: the only commuting antiholomorphic Mobius map is the fixed-point-free antipodal involution `J(z)=-1/conjugate(z)`. Any real model would produce a commuting reflection with fixed points.
- These remain deductions to be checked, not assumptions of source correctness. Exact identity and orbit controls are next.

## 2026-10-02 06:42:38 UTC - independent retrieval and execution checkpoint (80%)

- Independently fetched the primary archive PDF from `https://www.numdam.org/item/CM_1995__98_3_269_0.pdf`; its SHA-256 is exactly the same as above. Metadata checked at the primary Numdam article landing page.
- Live AIM HTML captured in this verifier directory. Source and operative-page visual checks completed before report writing.
- Default and bundled Python lack SymPy. Exact checks will instead use Python standard-library Gaussian rational arithmetic, without installing dependencies.
- First exact-check execution reached the real-phase control and failed an incorrectly specified expected value: for the real-phase cubic, `g(z)=-1/z` commutes, so it also conjugates the map to its coefficient conjugate. This expectation was corrected from false to true. The failed run is not reported as passing evidence.
- The second execution exposed the matching antiholomorphic control expectation: a real map can commute with both ordinary conjugation and the antipodal involution because its holomorphic centralizer is nontrivial. Corrected that control expectation too. This independently confirms that antipodal symmetry alone is insufficient; the trivial-centralizer proof is essential.

## 2026-10-02 06:43:17 UTC - exact verification checkpoint (90%)

- Final exact-check execution passed, exit code 0. It used only Gaussian rational arithmetic built from standard-library `Fraction` and homogeneous evaluations, including infinity.
- Main cases d=3,5,7,9 checked exact critical orbits, derivative identities and the holomorphic/antiholomorphic symmetry identities. Degree 2, degree 1, real coefficient phase, and the wrong-sign orbit were actually executed as controls/mutants.
- A general symbolic argument, rather than the finite checked degree list, supplies the all-odd-d proof.

## 2026-10-02 06:45:23 UTC - report checkpoint (98%)

- Wrote the independent proof in `report.md`: exact degree and PCF, trivial Mobius centralizer, absolute field of moduli exactly Q, unique antipodal antiholomorphic symmetry, and fixed-point contradiction for every hypothetical real model.
- Verdict is PASS for the old-source lead. Strongest priority consequence: the literal AIM question already has a negative answer obtainable from Silverman's printed 1995 example. Explicit PCF attribution, earliest worldwide priority, acceptance, and details of an unread PR36 manuscript remain outside this audit.
- New candidate attempts remain 0. No new route or repair was pursued. Final seal and self-excluding file manifest are next.

## 2026-10-02 06:47:12 UTC - sealed completion checkpoint (100%)

- Independent proof, source checks, exact execution and deliberate controls are complete. The report is sealed before any original PR36 report or other priority opinion is read.
- Final verdict: PASS. New candidate attempts: 0. Strongest result: every printed odd-degree member with d >= 3 is algebraic PCF with field of moduli Q and no real model.
- Prepared a hash seal and self-excluding manifest. Parent agent owns any repository checkpoint or publication decision; this verifier made no shared or remote edits.

## 2026-10-02 06:53:33 UTC - foreign-source retention correction checkpoint (100%)

- Moved the independently retrieved primary PDF and live AIM HTML into this directory's `tmp/`; foreign extracted text and page renders already resided in `tmp/pdfs/`. Confirmed every foreign-source path is git-ignored by the program-level `tmp/` rule. Current authored manifest excludes `tmp/**`.
- Added `reading_ledger.json` with corrected paths, source URLs/hashes, printed/PDF page locators and the ignore receipt. Preserved the initial proof seal in `historical_seals/20261002T064712Z_proof_seal.json` and the initial closure snapshot in ignored `tmp/historical_initial_closure/`. All initial seal component hashes were verified using preserved or relocated files. Earlier control failures remain preserved in this log.
- First retention verification caught a terminal blank line removed by the report-path patch; restored it. The full report suffix beginning with the exact-claim section is now byte-identical to the initial sealed report. Scientific proof and priority limitations are unchanged. Refreshed seal/manifest/verification receipt; verdict remains PASS, 0 new candidate attempts.
