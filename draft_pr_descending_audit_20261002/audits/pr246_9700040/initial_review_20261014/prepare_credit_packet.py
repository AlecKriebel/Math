"""Prepare a reviewable credit correction locally; performs no provider writes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

D = Path(__file__).resolve().parent
S = D / 'submitted/unsolved_math_prioritization/attempts/9700040'
C = D / 'corrected_packet'
C.mkdir(exist_ok=False)
utc = datetime.now(timezone.utc).isoformat()
intake = json.loads((D / 'INTAKE.json').read_text())
for pin in intake['original_source_files']:
    rel = pin['native_path'].split('unsolved_math_prioritization/attempts/9700040/', 1)[1]
    raw = (S / rel).read_bytes()
    assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256']
    target = C / 'original_submission' / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)

proof = (S / 'PROOF.md').read_text()
prefix, body = proof.split('## 1. Exact process and notation', 1)
credit = '''# An explicit joint stationary law for the drift–jump process

9700040 / AMR-096-0040. **Mathematics verified; classification already_solved
because the complete joint law is covered by earlier explicit constructions
and joint formulas.** Author turn 1/5. This is a credited classical consequence,
not a novel resolution of an unsolved problem. See [PRIORITY_AUDIT.md](PRIORITY_AUDIT.md)
for the exact equivalence, source chronology, and historical limits.

The derivation below is retained as a useful independent exposition and rational
verification implementation. Its mathematical Sections 1–7 are unchanged from
the original 20-file submission, preserved byte for byte under
`original_submission/`. The original independent reviews and their manifests
refer to that archived original input, not a later edited proof. The source asks
for a fairly explicit simultaneous stationary distribution; the displayed
positive determinant sums and exact rational enclosure provide one defensible
description. No proposer endorsement, worldwide historical firstness, or prior
appearance of the identical rational wrapper is asserted.

All solving and checking used AI tools extensively. This work is unrefereed;
AI adversarial checks do not constitute human peer review. There is no preprint,
Zenodo deposit or tracker entry for this credit correction.

## 1. Exact process and notation'''
(C / 'PROOF.md').write_text(credit + body)
for name in ('stationary_law.py', 'verify_exact.py', 'exact_receipt.json'):
    shutil.copyfile(S / name, C / name)

audit = '''# Priority audit and credited disposition

This records an audit deduction of **complete earlier mathematical coverage**.
It does not claim that an earlier author expressly announced an answer to the
February 2018 problem page, or that its proposer endorsed a particular level
of explicitness. Those historical/descriptive limits remain visible.

## Exact covering combination

Aldous–Diaconis's 1993 notes, printed 36–37, equation (42), already give the
simultaneous stationary positions as `Gamma(B_r)`: an independent unit-rate
Poisson arrival sequence evaluated at the compatible limiting pile-top ranks.
Their published 1999 account, printed 418, identifies the whole pile-top row
with the insertion tableau's first row under RSK. Restricting the tableau to
labels at most n is pathwise identical to inserting the subword of labels at
most n: high labels cannot alter lower entries. Uniform permutations therefore
give the coherent Plancherel tableau law, with each size-n tableau of shape
lambda having probability `f^lambda/n!`. This determines all joint B ranks.

If N(x) is the independent Poisson counting process, then, jointly for every
finite list of indices and thresholds,

`Gamma(B_r)>x <=> B_r>N(x) <=> lambda_1(x)<=r-1`.

The complete shape path is the horizontal ascending Poissonized Plancherel
process `C(x)=(x,1)` in Borodin–Olshanski (2004v2), equation (1.9), Remark 1.5
and Theorem 2.3. Its explicit one-box up probabilities telescope. From a shape
mu of size n to nu of size n+d over an increment Delta, the transition is

`e^-Delta Delta^d/d! * f^(nu/mu) * f^nu/f^mu * n!/(n+d)!`.

Multiplication across all thresholds cancels all intermediate ratios, giving
exactly the submitted weight

`e^-x_m D_1(lambda^m) product_j D_Delta_j(lambda^j/lambda^(j-1))`.

Summing its first-row barrier events gives the entire candidate formula,
including nonmonotone indices. This is a complete checked parameter bridge,
not inference from one-point marginals or mere availability of old tools.

## Earlier literal joint formula

Nica's Theorem 3.2 and Remark 3.3 already state the positive multi-time
skew-Schur product in arXiv1404.4015v1 (2014) and v3 (2015). Let M=x_m and
theta=sqrt(M). The area-preserving map `(u,v)->(u/theta,theta*v)` takes the
query rectangle to the square of side theta. Use Nica's positive branch in
reverse threshold order, `s=theta-x/theta`, with terminal shape at zero.
Its exact weight is

`e^-theta^2 D_theta(lambda^m) product_j D_(Delta_j/theta)(lambda^j/lambda^(j-1))`.

Homogeneity cancels theta because the skew sizes sum to the terminal size.
The result is precisely the submitted formula, with no asymptotic limit or
unidentified joint distribution. A coordinate swap gives the equivalent
negative-branch calculation. Fixed determinant dimension follows from standard
tableau transposition. The Poisson terminal-size mass supplies elementary
finite truncation. The identical shared-normalizer rational enclosure and
software may be a useful arrangement; their earlier exact appearance was not
established and is not claimed.

## Independent stationary bridge and source defects

The published 1995 Aldous–Diaconis paper, manuscript Section 2.2 pp5–6,
identifies the empty Hammersley count with the longest-chain count and gives
nearest-right dynamics; Lemma 4 p7 states simultaneous area-preserving scaling.
For inverse levels Z_i(t), the direct coordinate map
`Y_i(s)=e^s Z_i(e^s)`, `(u,v)->(uv,log v)`, has unit Jacobian and exactly the
positive linear drift and unit nearest-right jumps. Scaling gives stationarity;
finite-k uniqueness identifies the law. This verifies the old representation
without trusting the unfinished 1993 notes' erroneous scaling sign or unsafe
quantitative mean-coupling estimate.

The 2013 Borodin–Olshanski local tableau dynamics are expressly heuristic and
are **not** used as an established invariant-law theorem. The current Nica v3/v4
factorial display has a right-branch exponent typo; its correct Schur display,
full counting proof and v1 theorem resolve it. Later PDF title dates are
compilation dependent: the versioned 2015 source archive contains the actual
formula, uses the article class and has no explicit date declaration. Source
bytes, canonical version records and member pins were checked; late title dates
were not silently treated as earlier publication dates.

## What this classification means

The queue's `already_solved` disposition means that the candidate target is
already completely covered by identifiable earlier explicit constructions and
formulas. It is not a claim of an earlier expressly acknowledged answer to the
named 2018 posting. The open-page chronology and bounded absence of an explicit
closure cannot erase exact prior mathematical coverage or establish novelty.
The submitted packet itself already disclaimed novelty.

The valid proof and code are retained with credit. Under the active goal's
claimed_solved-only scope, the corrected open draft is skipped. No new paper,
deposit, tracker row, merge, closure or PR comment accompanies this disposition.
All original 20 files, including older review verdicts and manifests, remain
unchanged in `original_submission/`. The broader goal remains active.

The campaign's full analytic reviews, primary-source ledgers, exact replays,
and separate novelty-saving/coverage challenges are recorded in the dedicated
PR246 audit folder on main. Whole third-party reading copies are excluded.
'''
(C / 'PRIORITY_AUDIT.md').write_text(audit)
(C / 'README.md').write_text('''# 9700040 / AMR-096-0040

**already_solved: verified credited classical consequence.** The exact
simultaneous stationary law is covered by earlier constructions and explicit
joint formulas; see [priority audit](PRIORITY_AUDIT.md). Author turn 1/5.

[PROOF.md](PROOF.md) retains the valid mathematical derivation. Exact arithmetic
is in stationary_law.py and verify_exact.py. The original 20-file submission and
historical review/manifests are archived byte for byte in original_submission/.
Current manifests identify this corrected packet separately.

No new preprint, deposit, tracker row or merge is part of this scope skip.
AI tools were used extensively; unrefereed, without human peer review.
''')
(C / 'DISPOSITION.md').write_text('''# Credited scope disposition

Classification: **already_solved** after audit of an eligible claimed_solved
intake. Mathematics PASS; no mathematical repair. Complete earlier covering
combination and exact historical limits are in PRIORITY_AUDIT.md.

Preserve this valid proof and original 20-file archive. Skip this corrected
open draft under the active claimed_solved-only scope. No paper, Zenodo upload,
tracker append, merge, closure or PR comment. This is not a claim that an
earlier publication expressly announced an answer to the 2018 page.
''')
(C / 'PUBLICATION_STATUS.md').write_text('''# Current publication status

Status: **already_solved**; author turn 1/5; verified credited exposition.
Mathematical derivation accepted with exact scope and runtime qualifications.
Earlier all-law coverage is established by the explicit bridge in PRIORITY_AUDIT.md.
No preprint, DOI, Zenodo record or tracker entry is produced. Corrected open
draft is skipped under the active goal. No human peer review is claimed.
''')
(C / 'VERIFICATION.md').write_text('''# Verification and implementation scope

Run `python3 verify_exact.py` for the unchanged author receipt (49,618 exact
assertions). The original independent checker in original_submission/
independent_review/ independently passes 15,580 exact assertions; historical
42 coefficient comparisons and all original native hashes were reproduced.
Three new mathematical families and five distinct priority/coverage lanes are
preserved in the dedicated campaign audit. Their numerical diagnostics are
separately labeled and are not interval certificates.

The documented evaluator query domain is nonempty, strictly increasing positive
rational thresholds, positive integer indices and cutoff N with N+2>x_m.
Arbitrary mathematical queries can be normalized and combined by
inclusion-exclusion as explained in the proof. Exact fractions certify;
`display_only` floats may round inward, collapse or underflow and are not
outward enclosures. Default Python integer-to-string limits, recursive
partition enumeration, unbounded caches and finite memory/runtime limit
unbounded inputs. The mathematical effective finite evaluation argument does
not promise practical default-runtime execution at every precision or index.

The PROOF mathematical Sections 1–7, evaluator, checker and author receipt
are unchanged. Original manifests bind the archived original paths; current
FROZEN_MANIFEST and PUBLICATION_MANIFEST bind this current credited packet.
''')
(C / 'SOURCES.md').write_text('''# Primary sources and exact coverage

The exact target is [Aldous's drift-jump process](https://www.stat.berkeley.edu/~aldous/Research/OP/left_Hamm.html).
See PRIORITY_AUDIT.md for complete deductions, caveats and chronology.

- [Aldous–Diaconis 1993 notes](https://www.stat.berkeley.edu/~aldous/Research/OP/patience.pdf), printed36–39, especially(41)–(42): exact model, simultaneous stationary rank representation and known two-particle law. Unfinished draft, with unsafe scaling/mean-coupling displays; use the direct verified construction.
- [Aldous–Diaconis 1995](https://www.stat.berkeley.edu/~aldous/Papers/me71.pdf), Section2.2 manuscript5–6, Lemma4 manuscript7: empty-Hammersley longest-chain representation, nearest-right graphical rule and simultaneous scaling.
- [Aldous–Diaconis 1999](https://www.stat.berkeley.edu/~aldous/Papers/me86.pdf), printed418–419,427: full P-tableau pile-top row, RSK bijection and fixed-left-pile context.
- [Okounkov–Reshetikhin 2003v3](https://arxiv.org/pdf/math/0107056v3), Section2.2, equations(7)–(9), Definition2: factorial determinants and complete Schur path framework.
- [Borodin–Olshanski 2004v2](https://arxiv.org/pdf/math-ph/0402064v2), printed3 up probabilities, equation(1.9), Remark1.5 and Theorem2.3: exact horizontal ascending Poissonized Plancherel path, whose explicit transitions telescope to the full candidate sum.
- [Nica 2014v1](https://arxiv.org/pdf/1404.4015v1), Theorem3.2 and Remark3.3 printed5; [2015v3](https://arxiv.org/pdf/1404.4015v3), Theorem3.2/Remark3.3 printed6 and proofSection3.4: the literal positive joint shape product. Source-archive chronology and display typo caveats are in PRIORITY_AUDIT.md.
- [Betea et al., published2018](https://www.math.umb.edu/~vuletic/Site/Research_files/PSASP.pdf), **Section6**, equation(6.6), printed415–416: exponential specialization and Poissonized RSK. This corrects the original Section6.3 locator.

The original source audit and six byte pins remain unchanged under
original_submission/. The current source_manifest adds exact earlier covering
objects and the source archive. Full PDFs, source packages, extracted text,
images and provider responses are private reading copies, not redistributed.
''')
meta = json.loads((S / 'metadata.json').read_text())
meta.update(status='already_solved', mathematical_audit='PASS', author_turns=1,
            classification_basis='Complete exact earlier stationary-rank and explicit joint-law coverage; see PRIORITY_AUDIT.md',
            original_head=intake['head'], novelty_claim=False, preprint=None, DOI=None,
            human_peer_review=False, AI_tools_used_extensively=True,
            historical_acknowledged_answer_to_2018_question_established=False)
(C / 'metadata.json').write_text(json.dumps(meta, indent=2) + '\n')
sources = json.loads((S / 'source_manifest.json').read_text())
sources['original_six_source_pins_preserved'] = True
sources['accessed_utc_date'] = '2026-10-15'
for filename, pinname in [('plancherel_2004v2.pdf','ADDITIONAL_RETRIEVAL.json'), ('nica_v1.pdf','NICA_EARLIER_VERSION_RETRIEVAL.json'), ('nica_v3.pdf','NICA_EARLIER_VERSION_RETRIEVAL.json')]:
    candidates = json.loads((D / 'root_priority' / pinname).read_text())
    needle = {'plancherel_2004v2.pdf':'0402064v2','nica_v1.pdf':'4015v1','nica_v3.pdf':'4015v3'}[filename]
    item = next(x for x in candidates if x['url'].endswith(needle))
    sources['sources'].append({'reading_filename':filename, 'url':item['url'], 'bytes':item['bytes'], 'sha256':item['sha256']})
archive = json.loads((D / 'root_priority/NICA_SOURCE_ARCHIVE_RETRIEVAL.json').read_text())
sources['sources'].append({'reading_filename':'nica_v3_source.tar.gz','url':archive['url'],'bytes':archive['bytes'],'sha256':archive['sha256']})
(C / 'source_manifest.json').write_text(json.dumps(sources,indent=2)+'\n')
(C / 'RESEARCH_LOG.md').write_text('# Credited stationary-law audit log\n\n' + utc +
    ' — Prepared local credit correction for review; no native classification change yet. '
    'Full original mathematical proof/reproduction passes. Exact earlier all-law coverage '
    'is in PRIORITY_AUDIT.md; historical acknowledgement and identical certificate priority '
    'are not claimed. Author turn1/5. Best guess65% of eligible-intake scope disposition; '
    'final independent packet review and native guarded application/readback remain.\n')

def pin(path):
    data=path.read_bytes()
    return {'path':path.relative_to(C).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

files=[pin(x) for x in sorted(C.rglob('*')) if x.is_file()]
(C / 'FROZEN_MANIFEST.json').write_text(json.dumps({'problem_id':9700040,'status':'already_solved','author_turns':1,'utc':utc,
    'scope':'Current credited packet plus all20 immutable original input files; self hash excluded.','files':files},indent=2)+'\n')
files=[pin(x) for x in sorted(C.rglob('*')) if x.is_file()]
(C / 'PUBLICATION_MANIFEST.json').write_text(json.dumps({'problem_id':9700040,'status':'already_solved','author_turns':1,'utc':utc,
    'scope':'Credited audit packet only, not a preprint; current frozen manifest included, self hash excluded.','files':files},indent=2)+'\n')
assert (C/'PROOF.md').read_text().split('## 1. Exact process and notation',1)[1] == body
print(json.dumps({'utc':utc,'prepared_files':len(list(C.rglob('*'))),'original_archived_files':len(intake['original_source_files']),
                  'original_mathematical_body_unchanged':True,'native_mutations':0},indent=2))
