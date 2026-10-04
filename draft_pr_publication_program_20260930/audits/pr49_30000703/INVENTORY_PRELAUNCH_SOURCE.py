"""Author a literal original-claim inventory, without mathematical or source acceptance."""
from pathlib import Path
import datetime as dt, hashlib, json, os
A = Path(__file__).resolve().parent
def sha(body): return hashlib.sha256(body).hexdigest()
def write(path, body):
    with path.open('xb') as stream: stream.write(body); stream.flush(); os.fsync(stream.fileno())
def main():
    source = Path(__file__).read_bytes(); write(A/'INVENTORY_PRELAUNCH_SOURCE.py', source)
    read = json.loads((A/'ORIGINAL_COMPLETE_READ_RECEIPT_V2.json').read_bytes())
    raw = json.loads((A/'ORIGINAL_COMPLETE_RAW_SQL_READ.json').read_bytes())
    assert len(read['complete_original_JSON_values']) == 9 and read['original_files_read_in_full'] == 16
    assert raw['selected']['upstream_report_presence'] == 'ABSENT' and raw['selected']['sqlite_report_literal'] == '{}'
    text = '''# PR49 original claim inventory — preservation only

This inventory attributes claims to the exact original PR49. It supplies no current mathematical verdict, current priority determination, native transition, merge or publication approval. All original source-read, PDF-render, PASS, model, runtime, branch/duplicate-search and literature-status claims are historical assertions. No submitted scientific helper has been executed by this source-preservation effort. Current independent review and ROOT acceptance remain pending.

## Exact target and original proposed disposition

Original plain source ID30000703, code OWR-1460-009, asks what follows at1 for a holomorphic disk self-map f satisfying the ordinary unrestricted limit

    (1-|z|²)|f'(z)|/(1-|f(z)|²) → 1 as z→1 within the open disk.

The original proposes already_solved0/5 with credit to Kraus–Roth–Ruscheweyh2007. It claims equivalence with a holomorphic Schwarz-reflection extension across an open unit-circle arc containing1, mapping that arc into the circle. It claims a finite nonzero derivative, local conformality and an unrestricted boundary value. It explicitly claims no campaign discovery or priority, no automorphism conclusion, no global finite-Blaschke conclusion, no extension over the whole circle, no radial/nontangential-only resolution, and no result on the adjacent OWR boundary-regularity problem.

The imported dated raw assessment calls the problem partially solved and discusses angular conclusions. Its factual status is a hypothesis requiring fresh source verification. The exact ordinary-limit quantifier in the printed primary report, the precise imported theorem and the distinction from angular/radial hypotheses are central review obligations.

## Every original mathematical route and gap

1. **Imported arc theorem.** Original OWR9/2007, Roth contribution printed528–530, Theorem1 printed528–529: for an open arcGamma, a positive unrestricted liminf of hyperbolic distortion at every fixed point ofGamma is claimed equivalent to holomorphic extension acrossGamma with unimodular boundary values and to distortion tending to1 at every arc point. Credited to Kraus, Roth and Ruscheweyh, Journal d'Analyse Mathématique101(2007)219–256, DOI10.1007/s11854-007-0009-x. This infinite analytic theorem is an import, not established by finite symbolic controls.
2. **Point-to-arc application.** The unrestricted limit at1 supplies a single uniform lower boundPhi>1/2 throughout D intersect B(1,delta). Choosing an open circle arc with |xi-1|<delta/2 gives, for each fixedxi, a full interior neighborhood inside the same ball and liminfPhi>=1/2. The imported arc theorem then applies. This is the claimed key deduction; it does not assume a uniform limit over the new arc. A strictly positive unrestricted liminf at1 would suffice for this application. The reverse implication is imported from the same theorem.
3. **Boundary derivative.** After local extension, choose a neighborhood with f nonzero and eta=f(1) unimodular. The original uses u=-log|f| harmonic, positive on the disk side and zero on the smooth boundary arc. Hopf's lemma is claimed to make its inward normal derivative positive. Differentiating |f(e^it)|=1 makes conjugate(eta)f'(1) real, with the normal derivative giving alpha=conjugate(eta)f'(1)>0. The resulting expansion is f(z)=eta+alpha eta(z-1)+O(|z-1|²). Nonconstantness, positivity, smooth interior-ball hypotheses, orientation/sign and local nonvanishing must be checked independently.
4. **Reflection formula.** After shrinking the neighborhood to avoid zeros, the exterior extension is claimed equal to1/conjugate(f(1/conjugate(z))). The local circle-mapping property supplies the matching boundary values. This gives local continuation, not a global formula over arbitrary zeros or singularities.
5. **Nonautomorphism control.** f(z)=z² has distortion2|z|/(1+|z|²) tending unrestrictedly to1 near1, while it is not a disk automorphism. The original uses this only to block an overstrong conclusion.
6. **Nonglobal control.** f(z)=exp(-(1-z)/(1+z)) is a disk self-map, extends across the circle near1, has f(1)=1 and f'(1)=1/2, and has an essential singularity at-1. Its Cayley-transform real part u=(1-|z|²)/|1+z|² is positive in the disk and tends to0 unrestrictedly near1. The distortion is claimed u/sinh(u)→1. It does not force a finite Blaschke product or extension across the whole circle.
7. **Later primary corroboration and weaker limits.** Gumenyuk–Kourou–Moucha–Roth arXiv2410.13965v1 Section8.2 p31 equation8.3 is claimed to state the exact single-point equivalence and credit2007. Original Theorems1–2 and Section8.4 are claimed to distinguish radial/nontangential weak conformality from finite angular derivative, the latter requiring extra conditions. The paper's full theorem hypotheses, version and scopes require fresh verification.

## Original artifacts and attributed finite checks

Sixteen scientific originals are preserved byte for byte with Git objects/modes. Full17-path diff includes QUEUE. SOURCE_STATUS.md retains its original hash7690840787fd9be528beb649dc6db4b77bc637867720765812ec4cb31d5a73ba, exactly matching readiness and historical verdict. REVIEW.md matches its recorded hashb46416df003894db42db970462fa79b2f11de9d8f8a2c63a46a4483432c35983. No artifact sentence reversal or fabricated earlier source is needed.

The original author verify.py and review/submitted_verify.py are byte-identical. Both saved verification.json receipts are byte-identical. Their69 named PASS assertions comprise7 exact Cayley/exponential/power formulas and limits,60 rational triangle margins, and2 singular-inner boundary value/derivative checks. The original independent checker has187 named PASS assertions:60 powers z^k for2<=k<=16,1 Cayley reflection identity,24 positive rational parameter-family checks,100 rational circle/disk/neighborhood geometry checks, and2 sign/Cayley identities. These counts and receipt shapes have been read and preserved; no original helper was executed here. The finite controls do not prove the imported analytic reflection theorem or Hopf's lemma.

Historical readiness/review says author/reviewer gpt-6-astra,xhigh; independent review PASS; full original OWR contribution and relevant2024 source portions read, key pages rendered; full38-page2007 journal proof unavailable and not independently certified. source_checksums.json records3 original PDF hashes/sizes/URLs. No foreign PDF, OCR, pixel body, or publisher response is copied into this original-preparer corpus, and none of those PDF hashes or source-read claims has been freshly authenticated here. Supplementary2010 boundary-Schwarz source is not the claimed resolution source. No current absence-of-newer-literature conclusion is given.

## Plain record, prior-report, native and chronology qualifications

Original source_record.json is the plain selected problem object, not the queue.py show wrapper. It matches the complete pinned raw record byte exactly under default pretty JSON. Complete upstream report keyOWR-1460-009 is ABSENT; the literal importer stores SQLite report'{}'. Original prior_report.json is exactly'null\\n', an administrative absence marker. These are distinct representations; null is not a present explicit upstream report. The correct readiness review/statement hashes match the raw/imported objects.

The source-preparer's first inspection guessed an explicit-null upstream report and failed after writing earlier complete-read/native receipts. Its unmodified source, actual exit1 capture, prelaunch source and full error are retained. A distinct V2 inspection reran full provenance and all15458 raw/SQL rows successfully, proving the ABSENT/empty-object distinction without copying raw foreign bodies. The missing-local-head exit128 is also retained; a subsequent git fetch --no-write-fetch-head populated local objects and preserved branch/main/HEAD/cached diff exactly across the observed fetch interval.

Head native catalog/history/assessment/state/group selections retain original scalar ID types and exact string dictionary key presence. Dated working13 canonical input bindings are read-only observations, not authority over future main. The current acceptance program/main may advance in parallel. Original turns.json has integer id30000703,count0,empty substantive_attempts. Source preservation uses0 new substantive turns, with a five-turn limit. Original control checks are administrative verification, not a new proof-search result.

All9 original JSON objects were read completely. The earlier V2 log's phrase 'complete10 original JSON values' is a clerical count error; actual inspection stdout and complete object dictionary give9. This qualification supersedes that phrase without editing the historical source or capture.

Original-source preservation is complete when ROOT executes and separately reads the explicit self-only closing manifest. Mathematical/source-claim validation remains0% for this preparation family. ROOT acceptance, independent adversarial review, native transition and merge remain pending. No paper, Zenodo record or DOI is prepared for this attributed already_solved source correction.
'''
    write(A/'ORIGINAL_CLAIM_INVENTORY.md', text.encode())
    at=dt.datetime.now(dt.timezone.utc).isoformat()
    with (A/'RESEARCH_LOG.md').open('a') as stream:
        stream.write('\n'+at+' — Actual inventory author PID'+str(os.getpid())+' recorded exact ordinary-limit target, every original theorem/application/derivative/reflection/control claim and precise imported-proof limitation. Clarified original prior null marker versus upstream ABSENT/SQL{} and preserved failed first inspection. Correct original JSON count is9, superseding the earlier log typo10; actual V2stdout/dictionary are authoritative. Own original-source preparation100% pending ROOT actual self-only closure; mathematical/source-claim validation0%; no helper execution; new substantive turns0; supplied program checkpoint35/180=19.444444444444446%, current46.\n')
        stream.flush();os.fsync(stream.fileno())
    assert Path(__file__).read_bytes()==source
    print(json.dumps(dict(status='ORIGINAL_CLAIM_INVENTORY_AUTHORED_ONLY',actual_pid=os.getpid(),inventory_bytes=(A/'ORIGINAL_CLAIM_INVENTORY.md').stat().st_size,inventory_sha256=sha((A/'ORIGINAL_CLAIM_INVENTORY.md').read_bytes()),original_files=16,original_JSON_values=9,helper_execution_performed=False,mathematical_verdict=None,source_validation_verdict=None,acceptance_verdict=None),sort_keys=True))
if __name__=='__main__':main()
