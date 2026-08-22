# Independent referee report

**Manuscript:** *Positive Recurrence for Single-Linkage Bimolecular Weakly
Reversible Stochastic Reaction Networks*  
**Author:** Alec Kriebel  
**Packet reviewed:** Version 1.2.4 standalone AI-referee packet  
**Review date:** 21 August 2026 (America/Los_Angeles)

## 1. Recommendation

**Journal recommendation: minor revision.**

**Final mathematical status: CORE RESULT SOUND, REVISION REQUIRED.**

I find the main theorem established. Every load-bearing analytic implication
listed in the referee instructions survives direct reconstruction, including
the boundary, limiting, stopping, trace, and physical-time interfaces. No
counterexample or circular mathematical dependency was found. The finite
software checks are correctly auxiliary and independently reproduce.

Revision is nevertheless required because the manuscript and validation
records claim an available tagged Version 1.2.4 release, but the tag is absent
from the public remote, both exact manuscript links return 404, and the Git
release replay fails open when the expected tag is absent. The standalone
packet's bytes and rebuilds are internally coherent; Git-tag provenance is
not established. This is a material supporting-package defect but not a defect
in the theorem.

### Evidence freeze and independence protocol

Before substantive review I recorded:

- packet root:
  `/Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4`;
- submission root:
  `/Users/alec/Documents/Math/bimolecular_positive_recurrence_ai_referee_packet_v1_2_4/bimolecular_positive_recurrence_submission_v1_2_4`;
- macOS 26.5.2 build 25F84, Darwin 25.5.0 arm64;
- `python3` 3.14.6, `python` 3.9.6, Tectonic 0.16.9, and Poppler 26.08.0;
- journal PDF: 16 US-letter pages, 156,340 bytes, SHA-256
  `77b4f098a1f0655ed4e04423caccec79a051cf11297b17d5fa2d630d539e7c4d`;
- `paper_content.tex`:
  `00c0d9f2b281d6f36a388ff45776d9f90f9d6388dce0e83d9eb7b6aa80a4deba`;
- `references.bib`:
  `00bd5723e1c518841e94e8bd02637c709b0295891f191ed65dffbcc10a034e61`;
- supplied release ZIP:
  `66e1f89f97840650f400ae917ccb76ce5f08a9291a3a7692fe7bf2222d8af54f`;
- outer packet ZIP:
  `77f9a3641e19f702aeadf05e8ad0eb84fad46e2482d4cddf1c12d826fddb3522`;
  and
- deterministic digest of the unpacked packet's sorted per-file hash listing:
  `65860b70007afc68d685eb242e1b9e119aa4e08040b0af341bc85f2a14723309`.

The packet has no internal Git metadata. I visually inspected all 16 journal
PDF pages before using the TeX source and found no clipping, overlap, missing
glyph, or unreadable equation.

Three separated tracks then produced timestamped preliminary reports before
their conclusions were merged: analytic proof without code/author records;
software source and tests without execution/golden outputs; and adversarial
mathematics/counterexamples/citations without code/author records. A separate
main-referee proof and static-code pass observed the same barrier. The merged
provisional assessment was frozen before any author audit, preservation log,
reviewer checklist, or committed report was opened.

## 2. Exact theorem audited

Let the species set and the labelled reaction-channel set be finite. A channel
$r:y_r\to y'_r$ has a strictly positive rate constant $\kappa_r$, and at
population $x\in\mathbb N_0^d$ has stochastic mass-action propensity

\[
\lambda_r(x)=\kappa_r(x)_{y_r},\qquad
(x)_y=\prod_i\frac{x_i!}{(x_i-y_i)!},
\]

when $x\ge y$, and zero otherwise. Exact parallel channels may be combined;
channels with equal displacement but different source/target pairs remain
labelled. Population-null self-channels are deleted without changing the
minimal population CTMC.

The hypotheses are:

1. every source and target complex has molecularity at most two;
2. the reaction graph is weakly reversible;
3. it has one linkage class, so its full complex graph is strongly connected;
   and
4. every channel rate is fixed and strictly positive.

For any initial population $x_0$, define

\[
\Gamma(x_0)=\{z\in\mathbb N_0^d:x_0\leadsto z\},
\]

where reachability uses finite sequences of actually enabled population
jumps. The claim is that $\Gamma(x_0)$ is exactly one closed communicating
class. If it is nonabsorbing, the minimal CTMC on it is nonexplosive and has
finite expected positive physical return time

\[
T_x^+=\inf\{t\ge\tau_1:X(t)=x\}
\]

to one, hence every, state. It therefore has a unique stationary probability
law. If the class is an absorbing singleton, its unique stationary law is the
point mass. This is Theorem 2.1 and Corollary 2.3 (PDF p. 3;
`paper_content.tex` lines 220--247 and 293--299). No conclusion is claimed for
multiple linkage classes or molecularity above two.

## 3. Proof audit

| # | Load-bearing item | Status | Concrete reason and location |
|---:|---|---|---|
| 1 | Lifted state-return paths and closure | **PASS** | If $x=\rho+y$ fires $y\to y'$, a directed return path $y'=z_0\to\cdots\to z_m=y$ lifts to enabled states $\rho+z_j$. Reversing population edges makes reachability symmetric; its definition gives closure. This includes zero/boundary/parity cases. PDF p. 4, Lemma 2.2; TeX 249--291. |
| 2 | Labelled-channel augmentation | **PASS** | The next-channel law depends only on population, so projection is the ordinary jump kernel. The actual new target is the mark. A witnessed last channel into any marked state, preceded by population irreducibility, proves augmented irreducibility. PDF pp. 4--5, (8)--(9); TeX 332--378. |
| 3 | Proper potential and exact increment | **PASS** | The carried target is enabled, hence $\rho=x-t\ge0$. Finite target set and divergence of $\log(n!)$ give finite sublevels. Direct cancellation gives $\Delta V=\log((x)_t/(x)_s)$, including $0$, $2S_i$, and mixed sources. PDF pp. 5--6, (10), (13); TeX 369--378, 453--470. |
| 4 | Episode, deviations, recursion | **PASS** | A designated target edge keeps the residual fixed and has exactly zero reward; every other labelled channel stops the episode and its reward is already in the first-jump mean. Thus $J_k=\delta_k+q_kp_kJ_{k+1}$. A zero-length path still takes the terminal ordinary jump. PDF p. 7, (18)--(21); TeX 520--566. |
| 5 | Scalar envelope | **PASS** | Maximizing the concave function $\log p+C_0+qpM$ gives $p=1$ for $M\ge-1/q$ and $p=(-qM)^{-1}$ otherwise. The envelope is nondecreasing and tends to $-\infty$ with $M$; finite backward composition therefore preserves terminal negative divergence for any fixed positive rates. PDF pp. 7--8, (22); TeX 571--621. |
| 6 | Normalized-log compactification | **PASS** | A diagonal subsequence makes residual coordinates fixed or divergent. The normalized weights lie in the simplex; all divergent coordinates remain in $I$, even if their limiting weight is zero. Direct binary falling-factorial expansion gives $\log(\rho+c)_y=R_nw\cdot y+o(R_n)$. PDF p. 8, (23)--(25); TeX 630--684. |
| 7 | Bimolecular top-complex trichotomy | **PASS** | The three cases are exhaustive: all top gives an exact nonnegative invariant; a top complex with two divergent particles is eventually enabled; otherwise top complexes contain one leading divergent particle and give unary availability, bounded-companion availability, or an exact signed invariant. Zero-weight divergent species remain in $I$. PDF pp. 8--10, Lemmas 5.3--5.4, (26)--(29); TeX 686--810. |
| 8 | Exceptional Foster set | **PASS** | An infinite bad set would, by properness, contain a divergent sequence; the top alternative gives either an impossible class invariant or a fixed terminal whose episode drift tends to $-\infty$. A global minimizer of $V$ belongs to the set because every episode endpoint has at least its potential. PDF p. 10, Proposition 6.1, (30); TeX 814--841. |
| 9 | Random-time Foster argument | **PASS** | Episodes have at most $|\mathcal C|$ jumps and bounded coordinate overshoot. Hence every bounded-horizon stopped potential is integrable. The supermartingale inequality is used only at deterministic $N$; monotone convergence gives $E\sigma_K\le V(z)$. PDF p. 11, (34)--(36); TeX 892--940. |
| 10 | Finite trace and population projection | **PASS** | From finite $K$, positive return to $K$ has finite mean. The finite irreducible trace has geometrically controlled return count. Conditional excursion means plus Tonelli convert trace transitions to original jumps. Population return occurs no later than marked return. PDF pp. 11--12, Proposition 7.1; TeX 946--1000. |
| 11 | CTMC and regenerative law | **PASS** | Embedded positive recurrence forces infinitely many visits to an anchor; the independent exponential holding-time subseries there diverges almost surely, excluding explosion. Since every nonabsorbing state enables a genuine channel, $\Lambda(x)\ge\kappa_{\min}>0$, converting finite jump return to finite physical return. The finite-mean return cycle yields the normalized stationary occupation law. PDF pp. 12--13, Proposition 7.2, (37)--(38); TeX 1003--1071. |
| 12 | Uniqueness and absorbing classes | **PASS** | Irreducibility gives uniqueness of the regenerative stationary law. A state with no genuine enabled population jump has singleton reachability and carries its point mass; self-events do not alter the minimal population process. PDF pp. 3--4, 13; TeX 229--238, 301--320, 1071--1073. |

### Boundary attacks and rederived examples

I specifically tested the zero complex, coordinate faces, self and parallel
channels, equal displacements, parity/lattice classes, $2S_i$, absent
species, zero-weight but divergent coordinates, zero-length paths, arbitrarily
separated positive rates, finite shells, and absorbing states. None defeats
the theorem; every failed counterexample is excluded by an explicit
hypothesis or by the exact residual/path algebra, not by software filtering.

For $0\to A+B\to B\to0$, the terminal marked drift at $((n,1),B)$ is

\[
-\frac{\kappa_1n}{\kappa_0+\kappa_2+\kappa_1n}\log n.
\]

For the Anderson--Cappelletti--Kim five-edge example, direct channel
enumeration reproduces the three denominators and gives
$J_n=-\alpha\log n+O(1)$ with the manuscript's positive product $\alpha$.
For $0\to A\to A+B\to0$, direct expansion gives

\[
D_0(m,A)=-\frac{\kappa_2}{\kappa_1+\kappa_2}\log m
+O(\log m/m),
\]

whereas for fixed $m$, $\kappa_2\downarrow0$ gives
$D_0(m,A)\to a_m(1+p_m)>0$. This confirms that the proof is qualitative and
its finite exceptional set may move arbitrarily far with the rates.

## 4. Findings by severity

### Blocker

None.

### Major artifact/provenance findings

**M1. The claimed public Version 1.2.4 tag and tagged directory are absent.**

- Locations: PDF p. 14; `paper_content.tex` 1139--1146 and 1182;
  `validation/GIT_TAG_AND_COMMIT.txt` 1--20;
  `validation/REPRODUCTION_RECORD.md` 1--22; top-level `CITATION.cff` 9--12.
- Independent result: the packet has no internal `.git`; the exact local and
  remote tag query returned no v1.2.4 ref; matching public tags stop at v1.2.3;
  both exact manuscript GitHub URLs returned 404.
- The package's own `research_log.md` says only public release sequencing
  remained, while the manuscript and metadata use present-tense release
  language. Internal hashes therefore verify content, not Git provenance.
- Repair: publish an annotated v1.2.4 tag resolving to the exact audited tree
  and record/verify its tag object and peeled commit, or revise all availability
  and release-date statements to describe an untagged standalone candidate.

**M2. The Git release replay fails open on a missing or wrong tag.**

- Locations: `validation/replay_release.sh` 12--18 and 49--56; packet
  `README.md` 52--54.
- The script prints the result of `git describe --tags --exact-match`; on
  failure it prints `Exact tag: none` and continues. It never requires equality
  with `bimolecular-positive-recurrence-v1.2.4`.
- Reproduction: in a clean disposable Git repository containing the exact
  package and ZIP but no tag, the script printed `Exact tag: none`, ran all
  57+4 tests and all artifact checks, exited 0, and printed
  `PASS: complete Version 1.2.4 release replay`.
- This contradicts the packet README's claim that the standalone runner omits
  an exact-tag assertion present in the release replay.
- Repair: require exact-match resolution and literal equality with the
  expected tag before running any other step; test both no-tag and wrong-tag
  cases; then replay from a fresh detached checkout of the published tag.

I classify M1--M2 as major within artifact provenance because the advertised
release identity is not merely unverified: its purported fail-closed check is
absent. The repairs are localized and do not touch the mathematics, so they
support minor rather than major journal revision overall.

### Minor findings

**m1. All-self-channel reduction is not represented by the helper model.**
`combined_parallel()` deletes self-channels and then rejects an empty reduced
channel tuple (`network.py` 50--53, 82--92). Tests cover a self-channel only
when genuine birth/death channels remain (`test_network.py` 58--68). This is
not a theorem error; document the absorbing bypass or permit and test an empty
reduced network.

**m2. Scalar-envelope and zero-length episode tests are narrower than the
analytic lemmas.** The scalar code checks the maximizing branch and pointwise
monotonicity, not both exact envelope values, branch continuity, the
$-\infty$ limit, or backward composition (`episode_bounds.py` 13--45;
`verification.py` 241--271). The zero-length calibration checks only that an
empty path-product equals one, not the terminal ordinary jump
(`episode_bounds.py` 54--68; `verification.py` 729--730). The canonical report
describes the scalar scope accurately, and the omitted pieces were verified
analytically.

**m3. Historical large stress counts are not reproducible from the packet.**
`audit/publication_v1_2_submission_audit.md` 35--41 reports 1,687 graphs,
149,058 return witnesses, 366,324 transitions, and 7,168 episode cases, but
those counts appear only in prose; no script, inputs, seed, or transcript is
included. Do not credit these as evidence unless a reproducible artifact is
added.

**m4. The expert-note audit pointer is stale.** `expert_audit_note.md` 229--234
calls the Version 1.2 submission audit current despite later 1.2.1--1.2.4 audit
records. Clarify that it is the last full submission audit or point to the
current editorial audit.

### Notes

1. The author-generated audits, expert note, checklist, canonical report, and
   duplicate records are internally consistent but not independent evidence.
   The AI-use statement discloses that the same author-directed AI workflow
   contributed to proof development, counterexample search, verifier/tests,
   drafting, and audits. No prior independent human expert review is claimed.
2. The package's internal verifier version 1.2.0 within outer release 1.2.4 is
   explicitly documented as an unchanged component and is not a discrepancy.
3. The inner source allowlist rejects unexpected Python files; the outer
   manifest supplies the broader durable-tree boundary. Their different scopes
   are documented and behaved as designed.

## 5. Computation and artifact audit

### Static inspection

Before execution or opening any committed expected report, the software track
read all nine mathematical/verifier modules (1,846 lines), all seven test files
(868 lines; 57 tests), and the packaging, report, manifest, PDF, and archive
tooling. The inspected modules were `network.py`, `state_cycle.py`,
`target_augmented.py`, `episode_bounds.py`, `top_complex_dichotomy.py`, both
publication-calibration modules, `verification.py`, and `__init__.py`; every
file under `code/tests/` was read. The canonical report is genuinely
regenerated twice into temporary
files and compared with the committed bytes; it is not copied.

The code exactly checks selected finite identities and examples. It does not
implement general augmented-chain irreducibility, properness, arbitrary
episode recursion, compactification, the exceptional set, stopped-process
integrability, trace conversion, nonexplosion, or regeneration. The manuscript
and README accurately say that finite computation does not prove the universal
theorem.

### Canonical replay

From the packet root, the exact command

```bash
./RUN_ALL_CHECKS.sh
```

ran on macOS 26.5.2 / Darwin 25.5.0 arm64 with CPython 3.14.6 and Tectonic
0.16.9. It exited 0 in 26.556 seconds. No step or test was skipped.
The complete verbatim output is retained in Appendix A of
`software/final_report.md`.

| Stage | Outcome |
|---|---|
| Packet integrity | 89-file checksum passed |
| Mathematical/verifier suite | 57/57 passed in 6.920 seconds; 0 failures/errors/skips |
| Canonical report | Two fresh copies and all three committed copies byte-identical |
| Release-tool suite | 4/4 passed in 0.003 seconds; 0 failures/errors/skips |
| Durable manifests | Both 82-entry copies passed and are byte-identical |
| PDF build | Four Tectonic rebuilds matched supplied bytes |
| Release ZIP | Fresh 84-member ZIP matched supplied bytes |

Canonical hashes:

- report: `dc14127494eaa6ccf3b36a91f5d714ba6f79e76476f8d199760bd3b5faeed586`;
- manifest: `e8562cfb54fd411e4c1926bd2e15cf394a1ece014def06d3621e12a0fcce5caf`;
- journal PDF: `77b4f098a1f0655ed4e04423caccec79a051cf11297b17d5fa2d630d539e7c4d`;
- arXiv PDF: `e68130c3c38024a1e88b47cfa2cf06b8ebbead46665e82903d5bc6f2ff61bbe9`;
- bioRxiv PDF: `78373226d868c7067c172e329e63535bc5ff5ee317fbdb8eeb8eaede7be0a371`;
- supplementary PDF: `85223b8099fc179b368e372be4e9fa1bda7d4e754421d8d10e78d436d977aa9e`;
- release ZIP: `66e1f89f97840650f400ae917ccb76ce5f08a9291a3a7692fe7bf2222d8af54f`;
- printed Tectonic-bundle digest:
  `6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c`.

The committed report records 3,318 factorial identities, 172 entropy
identities, 36 scalar cases, 58 lifted-edge witnesses, 24 ACK checks, a
98,261-case three-species atlas, and 5,000 fixed-seed four-species cases. Its
classification correctly says these are finite/stress checks, not proof.

### Independent oracles

Fresh standard-library oracles imported no production module and found zero
failures in:

- 528,810 exact factorial comparisons in dimensions one through four;
- 1,153 exact entropy rewrites with independently aggregated rational rates;
- 40,537 lifted-edge witnesses from 400 independently generated strongly
  connected graphs;
- all 98,261 production-atlas top inputs using an independent brute-force
  certificate search, plus 20,000 separately generated four-species cases;
- 2,900 direct rate-degeneration and 2,900 direct ACK episode calculations;
- 700 exact directed-cycle stationary normalizations/flux balances; and
- 37,587 exact scalar branch/domain checks.

These provide falsification evidence for finite algebraic interfaces only.

### Mutation tests

Every mutation was made in a disposable copy. Corrupting the golden report,
adding an unlisted Python file, reversing the factorial-ratio implementation,
changing a durable source file, altering TeX/PDF bytes, or changing the ZIP
caused the intended report, source-allowlist, unit-test/wheel, manifest,
PDF-byte, packet-checksum, or archive comparison to exit nonzero. Adding an
unlisted non-Python source-like file passed the narrower inner allowlist but
failed the outer manifest as documented. Only the missing-tag mutation failed
open, as described in M2.

### Artifact consistency

The pinned source build reproduced all PDF bytes, establishing agreement of
the PDFs with their TeX/bibliography inputs along the supplied build route.
Both manifests agree and cover every durable package file: 82 entries for the
84-file tree, excluding the two manifests themselves. The archive contains
those 82 entries plus both manifests. All three report copies agree. The ZIP
extracts to the supplied 84-file tree and rebuilds byte-identically. The outer
packet checksum independently covers 89 of its 90 files, excluding itself.

Thus content consistency passes; only Git identity/provenance fails.

## 6. Author-record and literature comparison

Only after the three blind preliminary reports were frozen did I read the
existing audits, preservation records, logs, expert note, reviewer checklist,
validation summaries, and golden reports.

They agree with all twelve proof findings and add useful history about earlier
repairs, especially the ACK locator correction, explicit top trichotomy,
properness selection, projection autonomy, integrability sentence, CTMC proof
order, and stationary-balance explanation. No current mathematical
disagreement was found.

Their evidentiary role is limited. The Version 1.1 focused mathematical audit
explicitly did not reopen the central marked-target proof; later summaries do
not preserve a second full derivation; the reviewer checklist is a prompt; the
expert note is derivative; and three canonical reports are copies of one
generated object. They are claim inventories, not independent corroboration.

Primary/official-source checks support the material positioning:

- Anderson and Kim formulate the weak-reversibility positive-recurrence
  conjecture and structural sufficient conditions:
  <https://epubs.siam.org/doi/10.1137/17M1161427>.
- Anderson, Cappelletti, and Kim prove the one-linkage binary theorem with the
  additional pure-species condition and use the described Section 6.1 boundary
  branch: <https://doi.org/10.1017/jpr.2020.28> and
  <https://arxiv.org/abs/1904.08967>.
- Pauleve, Craciun, and Koeppl's Lemmas 4.5--4.6 use ``recurrence'' for the
  symmetric reachability property, not stochastic positive recurrence:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3835780/>.
- Xu's current Version 2, specifically Theorem 4.6(v), proves the broader
  bimolecular weakly reversible nonexplosion result and still records positive
  recurrence as open (its introductory reference to item (iv) is a source-side
  typo, not a manuscript error):
  <https://arxiv.org/abs/2409.05340>.
- Official Geneva and SIAM programs and the ConStRAINeD results page support
  the public two-species announcement and the statement that the five-author
  manuscript remains in preparation:
  <https://www.unige.ch/jpe75conference/program.html>,
  <https://www.siam.org/media/13rgukxr/ag25_abstracts.pdf>, and
  <https://constrained.polito.it/publications/>.
- The deterministic boundedness and permanence comparisons match their
  primary records: <https://doi.org/10.1007/s10910-011-9886-4> and
  <https://doi.org/10.1137/19M1248431>.

Exact-title and topic searches found no public manuscript duplicating the
present arbitrary-species, one-linkage, bimolecular result. This is a
time-bounded priority check, not proof of absolute novelty or absence of
unpublished work.

## 7. Residual uncertainty

1. Only CPython 3.14.6 was independently executed here; the claimed hosted
   3.11--3.13 runs and CI artifact were not verified. The code is standard-
   library-only and its 3.14 replay passed, but historical matrix claims remain
   author-generated.
2. The build prints the configured Tectonic bundle-content digest but does not
   itself hash the downloaded/cache bundle. Exact PDF byte reproduction is the
   direct output-level evidence.
3. The absent v1.2.4 tag prevents verification of its intended tag object,
   commit, clean detached checkout, or hosted tag workflow.
4. Standard Norris/Meyn--Tweedie/Asmussen interfaces were checked against
   official book records and against the manuscript's largely self-contained
   special arguments. Exact page/theorem pinpoints were not all available;
   the supplementary note supplies an elementary stationary-balance route.
5. Novelty searching cannot rule out unpublished, unindexed, or newly posted
   work, especially the announced two-species manuscript.
6. No finite computation establishes compactification, the Foster set,
   optional-stopping integrability, trace conversion, nonexplosion, or
   universal recurrence. The affirmative conclusion rests on the analytic
   audit in Section 3.

## Final validity conclusion

The universal theorem is established by the manuscript's analytic argument:
every necessary implication survived explicit derivation, the boundary cases
are covered, and no substantive proof obligation remains. The software
accurately provides finite falsification evidence and the supplied packet
content reproduces byte-for-byte. The narrow defect is that these bytes cannot
yet be represented as a verified tagged Version 1.2.4 Git release, because the
tag is absent and the release replay does not enforce it.

Acceptance should follow after the author either (i) publishes the exact
annotated tag, repairs the replay to fail on no/wrong tag, and reruns it from a
fresh detached checkout, or (ii) removes the tagged-release claims and labels
the materials as an untagged standalone candidate. The small verifier-coverage
and navigation corrections should be made at the same time.
