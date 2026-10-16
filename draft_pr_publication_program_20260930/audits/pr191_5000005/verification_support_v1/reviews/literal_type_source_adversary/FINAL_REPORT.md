# Independent source-first mathematical audit, PR191 / 5000005

**Verdict:** the exact imported unrestricted target is false as written. Its bare (A_0\iff\beta-\alpha=2\pi/n) characterization conflicts with its claimed signed angle rule at direct diagonals. There is an analytic counterexample family for every (n\geq5). The candidate explicitly replaces that bare convention with a parity-selected convention; its proof of the resulting repaired all-angle theorem is mathematically supported. These are different verdicts, and the latter must not be reported as solving the former without an explicit correction.

This is the final independent mathematical opinion of this approach family. No original review, gate opinion, sibling report, author checker, or other candidate code was read. The source-first assessment was sealed before the candidate was opened. Historical effort 2/5 has not been reset, and this audit does not make a novelty or priority finding.

## 1. Exact target and primary reading

The authenticated target selected from `ulamai/UnsolvedMath` revision `37e53eabe540fb458758e198be61634bd02ee008` is problem 5000005 / AMR-049-0005. I read the parent's authenticated selected statement only after sealing my independent source model. The relevant input is its conjunction of unique (A_k) labels modulo (n-2), the unqualified (A_0) characterization, and the transformation (k'=\varepsilon k-\ell) for admissible literal (\alpha'=\ell\pi/n+\varepsilon\alpha), with even (\ell) when (n) is even.

Primary [Fuchs paper](https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf): SHA-256 `9550009b3a903727a89abba863c520def9bf900b6bec779b63ef6cc82d43f01d`. I fully read the extracted text of pp.501-503,506-507,510-512, and §1.1-1.2 pp.494-495. I visually inspected the **complete** printed pp.502,503,504,505,510,511,512, including Figure 8, Figure 9, both definition tables, and the conjecture tables. Physical zero-based page index is printed page minus 493. I did not read every page of the paper. The source-first assessment correctly noticed the branch ambiguity independently, before seeing the candidate's explicit treatment of it.

The terminal interior angle is (\pi-\beta), not (\beta). Therefore (0\leq\alpha\leq(n-2)\pi/n) and (2\pi/n\leq\beta\leq\pi). The paragraph before Definition 2.1 selects the sum for an odd number of segments and the difference for an even number. Dropping that physical selector genuinely makes the printed disjunction assign multiple types on exceptional symmetry rays. A square diagonal, for example, satisfies both the raw (A_0) difference row and the (A_1) sum row; Figure 9 assigns (A_1).

## 2. Exact counterexample and its limits

Put (N=n-2). In Fuchs Figure 9's labeling the direct chord (X_0X_j) has

\[
\alpha_j=(n-1-j)\pi/n,\qquad
\beta_j=(n+1-j)\pi/n.
\]

Thus **every** direct chord satisfies the imported bare (A_0) criterion, although Figure 9 assigns (A_{j-1}). For each (n\geq5), choose (j=n-2): its angles are (\alpha=\pi/n\), (\beta=3\pi/n\), so the literal import says (k=0). With (\ell=2\), (\varepsilon=-1), the transformed angle equals (\alpha) exactly. The rule demands (A_{-2}), a different residue from (A_0) since (N\geq3). The same first-vertex chord cannot have both unique types. Even (\ell), literal admissibility, and all endpoint conventions hold.

This is not dependent on allowing the same trajectory on both sides of the rule. For odd (n\geq5), the shift (\ell=1,\varepsilon=1) takes the starting diagonal to the distinct interior chord of slope (2\pi/n); both satisfy the bare (A_0) condition, but the requested label is (A_{-1}). For even (n\geq6), use (\ell=2,\varepsilon=1), giving a distinct interior chord of slope (3\pi/n) and the similarly impossible bare label (A_{-2}). All open chord segments are interior by strict convexity, so there is no intermediate vertex or side hit.

**Scope limit:** §2.5 introduces its enumeration from (0<\alpha<\pi/(2n)) for odd (n) and (0<\alpha<\pi/n) for even (n). The counterexample start (\pi/n) is outside the odd fundamental sector and on the even sector's boundary. Consequently it refutes the dataset's unrestricted conjunction, and the unqualified global shorthand on p.506, **not** the original conjecture if it is interpreted only on the preceding open generic sector. It also does not refute the parity-selected theorem explicitly defined by the candidate. No angle was silently reduced modulo (\pi) or (2\pi).

The complete negative proof, including all-(n) formulas and both distinct-chord variants, is in `ANALYTIC_CERTIFICATE.md` Sections 1-2. This result is a deduction from regular-polygon geometry, not an inference from finite testing.

## 3. Candidate proof audit under its stated completion of the convention

I fully read `CANDIDATE.md`, and no other candidate implementation. Its equation (2) explicitly parity-selects types:

\[
q\text{ odd}:\quad k\equiv n-1-\frac{n(\alpha+\beta)}{2\pi};
\qquad
q\text{ even}:\quad k\equiv\frac{n(\beta-\alpha)}{2\pi}-1
\pmod N.
\]

For the obstructing chord this gives (A_{N-1}), which satisfies the self-reflection rule. The candidate is therefore not merely proving the imported bare shorthand by a different argument: it supplies a substantive convention at precisely the rays that obstruct the unrestricted import.

I independently checked the following central steps analytically. The checkable derivations are in `ANALYTIC_CERTIFICATE.md` Sections 3-4.

- The parity-selected modular type formulas follow from all the printed inequalities and the terminal-angle bounds. They are compatible with Figure 9 and the middle types. A boundary representative detail is identified below.
- On the double polygon, the corner cycles, cone angles, and physical direction offsets agree for both parities of (n). The global germ label covers all residues even when (N) is even.
- The intrinsic terminal-minus-initial label equals the source type with the correct final (\pi-\beta) convention. The integer congruences needed for division by (n) come from actual physical direction alignment.
- For even (n), the half-turn exchanging polygons is the hyperelliptic involution; its fixed-point count and genus give the sphere quotient. Conjugation by an affine map preserves the holomorphic derivative (-I); uniqueness makes it central. This justifies synchronizing the angular maps at both cones, rather than assuming a common shift.
- An affine map's angular lift respects antipodality. Consequently its effect on all forward and backward germ labels is one common residue. This is strong enough to transport the endpoint **sum** relation, not merely the type differences.
- In model symmetry directions, strict convexity gives the first-vertex chords and their endpoint-sum relation. One classical affine reduction acts on the entire direction, so inverse transport preserves the first-vertex property for every germ. This proves the central all-germ matching lemma rather than transferring the target difficulty to an equivalent unsupported assumption.
- The signed angle calculation uses (na=tN+\ell\), hence (2a\equiv\ell\pmod N), and never divides by two in an even cyclic group. The bisector reflection negates the type and supplies the negative sign case. All transformed angles remain literally admissible.
- The elementary (n=3,4,6) mechanisms are consistent with triangular, square, and honeycomb unfolding. The hexagon calculation recomputes the first allowed vertex, correctly treating its missing lattice residue.

I read the full relevant primary bodies of Finster §§3.1-3.2 pp.4-8 and the cusp statement on p.20, and Boulanger-Lanneau-Massart pp.791,793-794, including §1.4. These establish the imported reduction's stated scope and explicitly identify the even double-polygon group. I did **not** read all of either paper or the full original Veech (1989) paper; no such read depth is claimed. The analytic certificate gives the links and exact dependency use. Downloaded paper bodies and extracted records remain private.

**Repaired theorem finding:** subject to those explicitly credited classical theorems, no central proof gap remains in the candidate's all-(n\geq3), all-admissible-angle, parity-selected signed angle theorem. Its treatment of existence of all required first endpoints is substantive and valid. This positive finding neither rehabilitates the unqualified (A_0) shorthand nor constitutes a novelty finding.

## 4. Required repairs and exact remaining gap

1. **Correct the target/convention claim before marking the exact imported problem solved.** State that the global bare (A_0) characterization is false at direct diagonals. Either restrict the theorem to the source's preceding open generic sector or explicitly define the parity-selected extension and identify it as a correction/completion of the unrestricted import. A proof of a corrected theorem cannot prove the inconsistent original conjunction.
2. **Clarify the horizontal-side representative.** Candidate prose restricts representative indices to (0\leq k\leq n-3) before saying the inequalities choose them. For the odd one-segment horizontal side, (\alpha=0,\beta=2\pi/n\), the source sum row uses (k=n-2\equiv0), as Figure 9 explicitly identifies. State this endpoint representative before reduction, or define the side directly as (A_0). Candidate equation (2) already gives the right residue, so this is a small but real explanation repair, not a failure of its geometric proof.
3. **Preserve the distinction between proof and computation.** The universal counterexample and repaired proof mechanism are analytic; the finite checker is supplementary. No exact-target PASS should be inferred from the checker's intended-convention successes.

The exact literal target has no remaining positive-proof gap to fill: its assumptions are incompatible. For the explicitly repaired theorem I found no additional central mathematical gap. Novelty, independent assessment of the dependency proofs themselves, and publication status are outside this family's completed mathematical opinion.

## 5. Reproducible checks and artifact hygiene

I wrote a new stdlib-only exact checker from the primary formulas and my own derivations. It imports no author code and uses no numerical billiard tolerance. It checks 77,615 rational endpoint-angle/parity rows for (3\leq n\leq40), 143,956 oriented actual model chords for (3\leq n\leq60), 3,960,198 admissible literal direct-chord angle transformations for (3\leq n\leq200), and 15,728 primitive honeycomb vectors in a coordinate box of radius 80. It also checks the specialization of the analytic literal obstruction through (n=200), including its distinct-chord variants. The terminal run's status distinguishes the literal target's refutation from the parity-selected formula checks.

`independent_exact_checks.py` and `EXACT_CHECKS_OUTPUT.json` are the checkable artifacts. Recorded actual argv uses `/opt/homebrew/opt/python@3.14/bin/python3.14 -E -S -B -P`. The final run records UTC start/completion, exit, unchanged before/after source hashes, and stdout/stderr hashes. Earlier developmental run outputs are retained privately rather than silently overwritten. Source PDFs were fetched read-only using recorded exact URLs and their byte hashes were preserved. No packages were installed.

All writes for this family were confined to its dedicated folder. No protected original file was edited, no Git/index/ref/branch/remote mutation was performed, and no person was contacted or outreach drafted. `PUBLIC_ALLOWLIST.json` gives the exact own-authored files safe to consider for publication. It excludes the full papers, images, extracted text, private read/input records, and execution provenance containing host paths. The terminal seal makes each allowlisted file actually mode 0444 and records its content hash.

Audit completion estimate: **100%** for this family's source/type/scope and mathematical audit. The substantive finding is an exact negative result for the imported global conjunction, accompanied by a positively verified corrected theorem, rather than an unconditional solution claim.
