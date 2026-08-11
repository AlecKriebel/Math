# Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks

## Submission-candidate status

This directory is the Version 1.1 submission candidate prepared on 10 August
2026. The manuscript is an unrefereed preprint prepared for expert audit. No
preprint upload, journal submission, DOI registration, or external contact is
part of this release.

Version 1.1 is separate from the public Version 1.0 package. The Version 1.0
PDFs, canonical source, verification report, manifest, Git tag, tagged commit,
and package archive are preserved without modification. Their identifiers and
SHA-256 values are recorded in
`preservation/PRE_REVISION_PROVENANCE.md`. Earlier Version 0.3 artifacts remain
preserved separately as described in
`preservation/VERSION_0.3_PROVENANCE.md`.

## Exact result

Weak reversibility first gives an elementary state-space fact. If an enabled
reaction takes $x=r+y$ to $x'=r+y'$, a directed complex path from $y'$
back to $y$ lifts, with the same residual $r\geq0$, to enabled population
transitions from $x'$ back to $x$. Accessibility is therefore symmetric,
and the set reachable from any initial population is already a closed
communicating class. This fact does not require one linkage class or
bimolecularity.

On those automatically closed reachability classes, the manuscript proves:

> For every positive rate vector, every nonabsorbing communicating class of a
> finite bimolecular weakly reversible stochastic mass-action network with one
> linkage class is nonexplosive and positive recurrent. Every absorbing
> singleton carries its point-mass stationary law.

Consequently, every initial population belongs from time zero to a unique
closed reachability class, and that class has a unique stationary probability
distribution. This supplies long-run state frequencies and expectations of
bounded observables within the class. Finite molecule-count moments require
separate integrability and are not implied by positive recurrence.

The result does not cover multiple linkage classes or complexes of
molecularity greater than two. It does not provide product-form or explicit
stationary laws, tail or moment bounds, mixing rates, exponential ergodicity,
bounded sample paths, or quantitative bounds on transient excursions. The
proof recovers nonexplosion directly for its subclass; nonexplosion is already
known for the broader bimolecular weakly reversible class.

## Mathematical position

The log-factorial growth used in the proof belongs to the classical chemical
reaction network entropy tradition. For residual population $r$, Stirling's
formula compares \(\sum_i\log(r_i!)\) with the pseudo-Helmholtz/Horn--Jackson
family. The new mechanism here is to subtract the target complex actually
produced by the preceding labelled reaction channel. That target shift gives
the exact increment

\[
  \Delta V=\log\frac{(x)_t}{(x)_s},
\]

so following the carried target as the next source has exactly zero reward.
Finite target-following paths, a scalar-envelope induction, and a
normalized-log top-complex alternative then yield the qualitative recurrence
criterion.

The theorem removes the pure unary/pure-double complex hypothesis used by
Anderson, Cappelletti, and Kim (2020), and therefore contains their
binary one-linkage positive-recurrence conclusion as a special case. In their
Section 6 proof, Theorem 6.1 reduces recurrence to the tier inclusion (11),
Lemma 6.5 constructs a finite reaction word, Lemma 6.3(ii) supplies the strict
D-tier descent, and Lemma 6.4 assembles the sampled-chain argument. In Section
6.1, equations (19)--(20), the additional assumption first supplies either
$S_v$ or $2S_v$; D-tier maximality excludes $2S_v$, forcing $S_v$, whose
source propensity supplies the needed comparison. The present marked-target
argument replaces that comparison without assigning an unsupported broader
interpretation to the earlier assumption.

## Systems-biology interpretation

Stochastic mass-action chains model molecule-count noise in low-copy-number
biochemical networks. Under the theorem's exact structural hypotheses,
positive recurrence supplies a stationary molecule-count law and long-run
bounded-observable statistics for every positive rate vector. The theorem
does not give an explicit stationary formula, moment, tail, or mixing
guarantee, and it does not claim that all biological networks satisfy the
hypotheses.

## Directory map

- `preservation/`: immutable provenance for the Version 1.0 pre-revision
  snapshot and earlier Version 0.3 artifacts.
- `manuscript/paper_content.tex`: canonical mathematical and expository content.
- `manuscript/main_arxiv.tex`: thin arXiv wrapper.
- `manuscript/main_biorxiv.tex`: thin bioRxiv wrapper with identical canonical content.
- `manuscript/main_jap.tex`: thin Applied Probability initial-submission wrapper.
- `code/`: standalone deterministic verifier and exact regression tests.
- `supplement/v1_1_mathematical_audit.md`: exact audit of state-space closure,
  the rate limit, and the ACK Example 4.1 comparison included in the paper.
- `supplement/publication_v1_1_literature_audit.md`: primary-source literature,
  metadata, and bibliography audit dated 10 August 2026.
- `supplement/quantitative_limitations.md`: exact rate-sensitive Foster-set
  calculation and its limited conclusion.
- `supplement/reviewer_appendices.md`: technical trace-chain, physical-time,
  and computational details moved out of the main paper.
- `supplement/ai_use_full_statement.md`: complete tool-by-tool generative-AI disclosure.
- `supplement/reviewer_checklist.md`: load-bearing checks for expert readers.
- `supplement/verification_report.json`: canonical deterministic output.
- `supplement/MANIFEST.sha256`: hashes of the durable Version 1.1 files.
- `submission/`: prepared metadata, screening note, significance summary, and
  cover letter; none has been sent.
- `validation/`: clean-clone transcript, environment record, tag/commit record,
  and stable verification output.

## Reproduce the deterministic checks

The universal theorem is analytic. The finite atlases, calibration chains,
exact-identity checks, and fixed-seed tests are falsification aids: they do not
prove recurrence, enumerate the Foster set $K$, or certify a useful bound on
its location or diameter.

From the Version 1.1 directory:

```bash
cd code
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
./reproduce.sh
```

The reproducer runs the full test suite, generates the canonical report twice,
and requires byte-identical outputs. The clean replay and exact environment
are recorded in `validation/CLEAN_CLONE_TRANSCRIPT.txt`; the stable report is
retained in `validation/VERIFICATION_REPORT.json`.

Verify the release manifest from the Version 1.1 directory with:

```bash
python3 supplement/verify_manifest.py
```

## Build the manuscripts

```bash
cd manuscript
./build.sh
```

The three wrappers input the same `paper_content.tex`; front matter and
submission formatting are the only intended differences. Build and toolchain
details are recorded in the validation transcript.

## Submission-policy status

The metadata files were checked on 10 August 2026 against the official arXiv,
bioRxiv, and Cambridge/Applied Probability instructions. arXiv category
selection remains subject to moderation and may require endorsement. bioRxiv
screens mathematical work for direct life-science relevance and does not
guarantee acceptance under Systems Biology. Before any deposit, recheck the
current server, licensing, duplicate-posting, and journal-preprint rules and
choose the posting route deliberately.

## Author and declarations

- **Author:** Alec Kriebel
- **Affiliation:** Independent researcher
- **Correspondence:** <me@aleckriebel.com>
- **ORCID:** <https://orcid.org/0009-0001-9320-500X>

The research received no specific grant from any funding agency in the public,
commercial, or not-for-profit sectors. The author declares no competing
interests. No empirical biological dataset is associated with this work.

Generative-AI systems were used substantively in the research and preparation
workflow. The manuscript contains a concise declaration, and
`supplement/ai_use_full_statement.md` records the known systems, models,
dates, access routes, and uses through 10 August 2026. Rejected approaches are
not part of the final proof. The human author determined the released scope
and claims and assumes responsibility for the manuscript and verification
materials. No AI system is an author, and no independent expert human
validation is claimed.

The standalone software in `code/` is MIT-licensed. Rights in the manuscript
and other materials are governed by `LICENSE.md`.
