# Positive Recurrence for Single-Linkage Bimolecular Weakly Reversible Stochastic Reaction Networks

## Publication-candidate status

This directory is the Version 1.0 publication candidate prepared on 9 August
2026. The manuscript is an unrefereed preprint prepared for expert audit. No
preprint deposit, journal submission, DOI registration, or external contact is
part of this release preparation.

Version 1.0 is separate from Version 0.3. The tagged Version 0.3 manuscript,
source, verification report, and release identifiers are preserved under
`preservation/`; their provenance is recorded in
`preservation/VERSION_0.3_PROVENANCE.md`. Version 1.0 does not alter the
`bimolecular-positive-recurrence-v0.3` tag or its tagged commit.

## Exact result

The manuscript proves:

> Every finite bimolecular weakly reversible stochastic mass-action network
> with one linkage class is nonexplosive on every closed communicating class,
> for every positive rate vector. Every nonabsorbing such class is positive
> recurrent; every absorbing singleton carries its point-mass stationary law.

Consequently, within each already-closed communicating class, the minimal
continuous-time Markov chain has a unique stationary probability
distribution. This supplies long-run state frequencies and
expectations of bounded observables within that class and excludes permanent
stochastic escape to infinity. Finite molecule-count moments require separate
integrability and are not implied by positive recurrence alone.

The result does **not** prove finite expected entrance into a closed component
from every nonclosed initial state. It also does not cover multiple linkage
classes or complexes of molecularity greater than two, and it does not provide
product-form stationary laws, tail bounds, mixing rates, exponential
ergodicity, bounded sample paths, or quantitative bounds on transient
excursions.

## Mathematical position

The log-factorial growth used in the proof belongs to the classical chemical
reaction network entropy tradition. For residual population \(r\), Stirling's
formula compares \(\sum_i\log(r_i!)\) with the pseudo-Helmholtz/Horn--Jackson
family. The new mechanism in this argument is to subtract the target complex
actually produced by the preceding reaction channel. That target shift gives
the exact increment

\[
  \Delta V=\log\frac{(x)_t}{(x)_s},
\]

so following the carried target as the next source has exactly zero reward.
Finite target-following paths, a scalar-envelope induction, and a
normalized-log top-complex alternative then yield the qualitative recurrence
criterion.

The theorem contains the binary one-linkage theorem of Anderson,
Cappelletti, and Kim (2020) as a special case and removes its additional
pure-species-complex hypothesis. The obstruction to the same proof for
multiple linkage classes is concrete: a target carried in one linkage class
need not have a directed path to a useful terminal complex in another.

## Systems-biology interpretation

Stochastic mass-action chains are standard models for low-copy-number
intracellular, signaling, enzymatic, gene-regulatory, and synthetic
biochemical networks. For a network that satisfies the theorem's exact
bimolecular and one-linkage assumptions, positive recurrence supplies a
stationary probability law for molecule-count noise within each closed class.
It justifies stationary probabilities and bounded steady-state observables;
unbounded molecule-count moments require additional integrability. The
criterion is structural and holds for every positive rate vector. It is not a
claim that all biochemical networks have the required structure, nor is the
motivating reaction cycle presented as a validated molecular mechanism.

## Directory map

- `preservation/`: immutable copies and provenance for the Version 0.3 release.
- `manuscript/paper_content.tex`: canonical mathematical and expository content.
- `manuscript/main_arxiv.tex`: thin arXiv wrapper.
- `manuscript/main_biorxiv.tex`: thin bioRxiv wrapper with identical canonical content.
- `manuscript/main_jap.tex`: thin Applied Probability initial-submission wrapper.
- `code/`: standalone deterministic verifier and exact regression tests.
- `supplement/publication_v1_targeted_proof_audit.md`: targeted proof-interface replay.
- `supplement/publication_v1_literature_audit.md`: source-verified literature and positioning audit.
- `supplement/quantitative_limitations.md`: exact rate-degeneration calculation.
- `supplement/ai_use_full_statement.md`: complete tool-by-tool AI disclosure.
- `supplement/reviewer_checklist.md`: ten load-bearing checks for expert readers.
- `supplement/verification_report.json`: canonical deterministic output.
- `supplement/MANIFEST.sha256`: hashes of the durable Version 1.0 files.
- `submission/`: prepared metadata, screening note, significance summary, and cover letter; none has been sent.
- `validation/`: clean-clone transcript, environment record, tag/commit record, and stable verification output.

The first-contact archive intentionally omits the abandoned discovery history.
That history remains preserved with Version 0.3 and in Git.

## Reproduce the deterministic checks

The universal theorem is proved analytically. The finite atlases, calibration
chains, exact-identity checks, and fixed-seed tests are falsification aids;
they do not establish recurrence, enumerate the exceptional set, or certify
its location or diameter.

From the Version 1.0 directory:

```bash
cd code
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
./reproduce.sh
```

The reproducer runs the test suite, generates the canonical report twice, and
requires byte-identical outputs. The clean replay and exact environment are
recorded in `validation/CLEAN_CLONE_TRANSCRIPT.txt`; the stable report is
retained in `validation/VERIFICATION_REPORT.json`.

Verify the release manifest from the Version 1.0 directory with:

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

The metadata files were checked on 9 August 2026 against the official arXiv,
bioRxiv, and Cambridge/Applied Probability instructions. arXiv category
selection remains subject to moderation and may require endorsement. bioRxiv
screens mathematical work for direct life-science relevance and does not
guarantee that this theorem will be accepted under Systems Biology. The two
preprint options are alternatives: before any deposit, recheck current
duplicate-posting, permanence, licensing, and journal-preprint rules and
choose one server deliberately.

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
dates, access routes, and uses. The human author determined the released scope
and claims and assumes responsibility for the manuscript and verification
materials. No prior independent expert human validation is claimed.

The standalone software in `code/` is MIT-licensed. Rights in the manuscript
and other materials are governed by `LICENSE.md`.
