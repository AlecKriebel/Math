"""ROOT records its actual bounded mathematical adjudication; no native mutation."""
from pathlib import Path
import datetime, hashlib, json, os, stat

A = Path(__file__).absolute().parent
R = A.parents[2]
O = A / 'original_preparation_family'
F = A / 'symplectic_geometry_adversary_family'
K = A / 'knot_invariant_relation_adversary_family'
C = A.parent / 'pr45_9900007'

def ref(p):
    b = p.read_bytes(); s = p.stat()
    assert p.is_file() and not p.is_symlink()
    return dict(path=str(p.relative_to(R)), bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), full_mode=stat.S_IMODE(s.st_mode))

def main():
    assert __debug__
    ops = []
    for name, pid in [
        ('root_pr61_original_SOURCE_verify_actual_capture', 91483),
        ('root_pr61_original_SOURCE_close_actual_capture', 91487),
        ('root_pr61_original_SOURCE_readback_actual_capture', 91951),
        ('root_pr61_symplectic_SOURCE_close_actual_capture', 91953),
        ('root_pr61_symplectic_SOURCE_readback_actual_capture', 92189),
        ('root_pr61_knot_SOURCE_close_actual_capture', 92194),
        ('root_pr61_knot_SOURCE_readback_actual_capture', 92415),
    ]:
        d = C / name; c = json.loads((d / 'CAPTURE.json').read_bytes())
        assert c['pid'] == pid and c['actual_execution'] is True and c['completed'] is True
        assert c['status'] == 'PASS' and c['exit_code'] == 0
        assert {p.name for p in d.iterdir()} == {'CAPTURE.json', 'prelaunch_operator.py', 'stdout.bin', 'stderr.bin'}
        for key in ['stdout', 'stderr']:
            b = (d / (key + '.bin')).read_bytes()
            assert len(b) == c[key]['bytes'] and hashlib.sha256(b).hexdigest() == c[key]['sha256']
        assert (d / 'stderr.bin').read_bytes() == b''
        ops.append(dict(capture=ref(d / 'CAPTURE.json'), actual_pid=pid,
            started_utc=c['started_utc'], finished_utc=c['finished_utc'],
            whole_capture_files=[ref(p) for p in sorted(d.iterdir())]))
    files = [O / 'SOURCE.json', O / 'READY.json', O / 'ORIGINAL_INTAKE_REPORT.md',
        O / 'SOURCE_ACCOUNTING.json', O / 'original/KNOWN_RESULT.md', O / 'original/README.md',
        O / 'original/source_record.json', A / 'ROOT_ORIGINAL_SOURCE_CLOSE_20261003.json',
        F / 'REPORT.md', F / 'INDEPENDENT_CONSTRUCTION_AND_SCOPE.md', F / 'INDEPENDENCE_SEQUENCE.json',
        F / 'ROOT_SOURCE_CLOSURE.json', F / 'controls.py', F / 'controls_actual/CAPTURE.json',
        F / 'controls_actual/stdout.bin', K / 'REPORT.md', K / 'PROOF.md', K / 'INDEPENDENT_CORE.md',
        K / 'FRAMED_PLANES.md', K / 'VERDICT.json', K / 'MANIFEST.json', K / 'relation_controls.py',
        K / 'captures/relation_controls.stdout']
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    record = dict(
        schema='ROOT-pr61-scientific-known-result-adjudication/v1', actual_writer_pid=os.getpid(), utc=now,
        PR=61, problem_id=2725, problem_code='KP-1.66', head='b5a4829365f2a0bd5f42b7653c5cfacfa6b01d85',
        scientific_verdict='VALID_ATTRIBUTED_ALREADY_SOLVED_NEGATIVE_ANSWER', status='already_solved',
        original_budget='0/5', new_attempts=0, audit_attempts=0, novelty_credit=0,
        ROOT_bounded_mathematical_applicability_audit_percent=100,
        full_imported_construction_independently_recertified=False,
        native_acceptance_completed=False, paper_DOI_tracker=False,
        original_author_executable_checker_present=False, original_science_bodies_unchanged=10,
        claims_and_scope=dict(
            literal_target='Unrestricted exact Lagrangian cobordism of Legendrian links in standard contact R3; partial-order question.',
            object_equivalence='Legendrian isotopy; the witness has distinct underlying smooth knot types, avoiding ambiguity about object equality.',
            imported_existence='Dimitroglou Rizell and Golovko arXiv2409.00290v4 Corollary1.5/Theorems1.4,5.7: the same sufficiently both-sign-stabilized pair of a decomposable-disc-fillable mirror9_46 representative and standard unknot has exact embedded cylindrical concordances both ways in R x R3.',
            deduction='Legendrian stabilization preserves smooth knot type; Legendrian isotopy implies smooth isotopy. The mutually concordant pair stays distinct, violating antisymmetry. Knots are eligible links. Non-symmetry alone would not suffice.',
            independent_exactness='Restricted e^t alpha on a Lagrangian cylindrical annulus is closed. An end circle generates H1 and has zero period; all periods vanish, giving a primitive constant separately at each cylindrical end. This is not asserted for positive-genus surfaces or one common zero end constant.',
            classical_checks='Same both-sign stabilization yields compatible tb and rotation. Two connected oriented two-knot cobordisms force genus0 by tb differences. These are necessary constraints, not existence certificates.',
            limitations=['No numeric or minimal stabilization threshold.',
                'No restricted regular/decomposable/unstabilized/fixed-smooth-knot-type variant.',
                'No full independent relative immersion/totally-real h-principle or approximation proof.',
                'Non-regularity is attributed to primary section1.2/theorem5.1; its gauge-theory input is not newly recertified.']),
        source_precision=[
            'Unframed oriented Lagrangian planes U(2)/SO(2) have pi2=Z, while framed U(2) has pi2=0. Annular tangent framing supplies the interpretation; compatible relative framing remains an explicit requirement of any full reconstruction. No theorem refutation is established.',
            'C0-small interpolation endpoints alone do not control time derivatives; the time mesh must be included. This detects an invalid shortcut, not a counterexample to the published existence theorem. Complete approximation estimates remain an attributed import.'],
        primary_reading=dict(ROOT_literally_read_KP_question_and_all_four_remarks=True,
            private_LF_locator=[3307, 3331],
            private_text_sha256='3f42d6ebef41f9c4112638f001f16f1bc45e720231b18bc3a8b4f936a51ff790',
            ROOT_primary_DRG_selected_sections='Official versioned HTML: sections1.2-1.3, end conventions2.1, theorem5.3, full propositions5.4-5.5/theorem5.7/example5.8 and AppendixA; no full PDF or diagram reconstruction.'),
        credited_authors=['Georgios Dimitroglou Rizell', 'Roman Golovko'],
        priority='Attributed existing theorem; no campaign discovery or worldwide earliest-priority claim.',
        historical_source_limits='Historical PDF hashes, visual inspection, publisher and Crossref receipts remain historical; no fresh ROOT PDF/pixel/publisher/Crossref verification is inferred.',
        proof_artifacts=[ref(p) for p in files], actual_ROOT_custody_operations=ops,
        independent_controls=dict(symplectic_geometry=973, knot_invariant_relation=774,
            scope='Finite exact diagnostics and logic only. Universal deductions rest on written proofs; existence is an attributed primary theorem.'),
        accounting='Raw upstream KP-1.66 report ABSENT; selected null; importer SQL TEXT literal {} is missing-report fallback; original prior_report.json is a present dictionary placeholder. Original source_record matches raw problem. No original turn ledger or runnable math checker.',
        AI_used_extensively=True, unrefereed=True, human_peer_reviewed=False, external_individuals_contacted=False,
        prior_write_failure='Earlier inline writer failed at Python parsing before any instruction executed or receipt was written; no child execution or partial scientific receipt is inferred.',
        remaining_program_gap='Later ordered native acceptance after PR48 recovery and intervening PRs; no new paper for already_solved.')
    out = A / 'ROOT_SCIENTIFIC_ADJUDICATION_20261003.json'
    with out.open('xb') as stream:
        stream.write((json.dumps(record, indent=2, sort_keys=True) + '\n').encode())
        stream.flush(); os.fsync(stream.fileno()); os.fchmod(stream.fileno(), 0o444)
    print(json.dumps(dict(status='ROOT_BOUNDED_ALREADY_SOLVED_ADJUDICATION_RECORDED', record=ref(out), actual_pid=os.getpid())))

if __name__ == '__main__': main()
