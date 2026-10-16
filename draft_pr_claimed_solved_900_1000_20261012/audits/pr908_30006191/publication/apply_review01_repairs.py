#!/usr/bin/env python3
"""Preserve candidate01, correct current prose, and repair the live PR body."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

P = Path(__file__).resolve().parent
A = P.parent
ROOT = A.parents[2]
OLD_BODY = '3b6678ba45571e86e44360e45cffd2e00d75b8f05c5d3a8a407c43c5680f708d'
HEAD = 'a35667b1bb0bafed69916709997a4684223ecc93'


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def gh(args):
    return subprocess.run(['gh', *args], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout


def main():
    freeze = json.loads((P/'PREPUBLICATION_FREEZE.json').read_text())
    require(freeze['revision_candidate'] == 1, 'Expected the sealed first candidate')
    review = json.loads((A/'reviews/full_package_01/RESULT.json').read_text())
    require({x['id'] for x in review['required_issues']} == {'R1'} and
            {x['id'] for x in review['optional_issues']} == {'O1'}, 'Unexpected review findings')
    history = P/'history/candidate01'
    require(not history.exists(), 'First candidate already preserved; reconcile before rerun')
    for name, record in freeze['files'].items():
        source = P/name
        require(source.stat().st_size == record['bytes'] and
                digest(source.read_bytes()) == record['sha256'], 'First candidate drift')
        dest = history/name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
    receipts = ['PREPUBLICATION_FREEZE.json', 'BUILD_RECEIPT.json', 'LOCAL_ZENODO_CHECK.json',
                'PDF_VISUAL_QA.json', 'COMPILATION_RECEIPT.json', 'PACKAGE_GUARD_CHALLENGES.json',
                'PACKAGE_REPLAY_normal.json', 'PACKAGE_REPLAY_O.json', 'PACKAGE_REPLAY_OO.json',
                'PACKAGE_REPLAY_env2.json']
    for name in receipts:
        shutil.copyfile(P/name, history/name)

    substitutions = {
        'value2': 'value 2', 'expectation4': 'expectation 4', 'norm2': 'norm 2',
        'all26': 'all 26', 'all26': 'all 26', 'All26': 'All 26', 'original1/5': 'original 1/5',
        'original26': 'original 26', 'PR908': 'PR #908', 'coefficient1': 'coefficient 1',
        'September2026': 'September 2026', 'submitted28': 'submitted 28',
        'February2025': 'February 2025', 'Physics115': 'Physics 115',
        'Theorem2.4': 'Theorem 2.4', 'Proposition2.6': 'Proposition 2.6',
        'Lemmas3.1-3.4': 'Lemmas 3.1-3.4', 'Section3.3': 'Section 3.3',
        'Python3.14.6': 'Python 3.14.6', 'NumPy2.3.5': 'NumPy 2.3.5',
        'SciPy1.17.0': 'SciPy 1.17.0', 'SymPy1.14.0': 'SymPy 1.14.0',
        'mpmath1.3.0': 'mpmath 1.3.0', 'tolerance3e-11': 'tolerance 3e-11',
        'tolerance2e-11': 'tolerance 2e-11', 'tolerance1e-9': 'tolerance 1e-9',
        'tolerance1e-10': 'tolerance 1e-10', 'checks8': 'checks 8',
        'cases,22952': 'cases, 22,952', 'identities,20000': 'identities, 20,000',
        'identities and15': 'identities and 15', 'has148': 'has 148',
        'has2668': 'has 2,668', 'and558': 'and 558', "author's4288": "author's 4,288",
        "B's16768": "B's 16,768", "A's5659": "A's 5,659", 'of5000': 'of 5,000',
        'predicates,2': 'predicates, 2', 'and657': 'and 657', 'of5659': 'of 5,659',
        'reproduces20': 'reproduces 20', 'executions,24': 'executions, 24',
        'and22': 'and 22', 'with104': 'with 104', 'and12': 'and 12',
        'SHA828280': 'SHA-256: 828280', 'BY4.0': 'BY 4.0', 'R3': 'R³',
    }
    def polish(text):
        for old, new in substitutions.items():
            text = text.replace(old, new)
        return text
    readme = polish((P/'README.md').read_text())
    (P/'README.md').write_text(readme)
    meta = json.loads((P/'zenodo-deposit.json').read_text())
    for key in ['description', 'notes']:
        meta['metadata'][key] = polish(meta['metadata'][key])
    meta['metadata']['references'] = [polish(x) for x in meta['metadata']['references']]
    (P/'zenodo-deposit.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2)+'\n')

    tex = (P/'note.tex').read_text()
    tex = tex.replace('unit Slaters $\\Psi_N', 'unit Slaters, indexed by $N\\geq1$, $\\Psi_N', 1)
    (P/'note.tex').write_text(tex)
    freezer = (P/'freeze_candidate.py').read_text().replace("'revision_candidate': 1", "'revision_candidate': 2", 1)
    (P/'freeze_candidate.py').write_text(freezer)

    before = json.loads(gh(['pr', 'view', '908', '--repo', 'AlecKriebel/Math',
                          '--json', 'state,isDraft,headRefOid,title,body,url']))
    require(before['state'] == 'OPEN' and before['isDraft'] is True and
            before['headRefOid'] == HEAD, 'Live draft/head changed')
    require(digest(before['body'].encode()) == OLD_BODY, 'Live body changed since review')
    body = polish((A/'PR_DESCRIPTION_CORRECTED_DRAFT.md').read_text())
    body = body.replace('version1.0', 'version 1.0').replace('September28,2026', 'September 28, 2026')
    body = body.replace('tending to2', 'tending to 2')
    path = A/'PR_DESCRIPTION_CORRECTED.md'
    path.write_text(body)
    gh(['pr', 'edit', '908', '--repo', 'AlecKriebel/Math', '--body-file', str(path)])
    after = json.loads(gh(['pr', 'view', '908', '--repo', 'AlecKriebel/Math',
                         '--json', 'state,isDraft,headRefOid,title,body,url']))
    require(after['body'] == body and after['state'] == 'OPEN' and after['isDraft'] is True
            and after['headRefOid'] == HEAD, 'Live body/head exact readback failed')
    now = datetime.now(timezone.utc).isoformat()
    receipt = {'utc': now, 'pr': 908, 'required_issue': 'R1', 'optional_issue': 'O1',
               'old_body_sha256': OLD_BODY, 'new_body_sha256': digest(body.encode()),
               'live_body_exact_readback': True, 'live_draft_and_head_unchanged': True,
               'candidate01_preserved_at': 'publication/history/candidate01',
               'original_26_files_unchanged': True, 'mathematical_proof_change': False,
               'extra_editorial_clarification': 'Positive sequence index N>=1 made explicit; original scope unchanged.',
               'new_candidate_compile_build_replay_freeze_and_fresh_review_required': True}
    (A/'REVIEW01_REPAIR_RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    corrections = A/'PUBLICATION_REVIEW_CORRECTIONS.md'
    with corrections.open('a') as f:
        f.write('\n## '+now+' — first full-package review repairs\n\n'
                'Review01 passes the mathematical/source/priority/computation/PDF/descriptor package. '
                'Required R1 is resolved in the live PR body: it links the current externally pinned '
                'isolated verifier, qualifies historical assertion/inventory limitations, and discloses '
                'the prior direct cutoff adaptation and later audit bootstrap. Exact live-body readback '
                'confirmed without changing the draft or original head. The old body anchor and sealed '
                'candidate01 are preserved as historical evidence. Optional O1 is resolved in current '
                'README/Zenodo human prose by ordinary word/number spacing. The paper also states the '
                'already-intended positive index N>=1 explicitly. Original26 bytes and1/5 remain unchanged. '
                'The revised candidate must be rebuilt/replayed/frozen and checked by a NEW second '
                'whole-package reviewer before acceptance. REVIEW01_REPAIR_RECEIPT.json binds the '
                'old/new live-body fingerprints; no merge/deposit/tracker write has occurred.\n')
    synthesis = json.loads((A/'MATH_AUDIT_SYNTHESIS.json').read_text())
    synthesis.update(first_whole_package_review={'manifest_sha256': digest((A/'reviews/full_package_01/MANIFEST.json').read_bytes()),
                     'substantive_package_verdict': 'PASS', 'required_R1_globally_resolved': True,
                     'optional_O1_globally_resolved': True, 'evidence': 'REVIEW01_REPAIR_RECEIPT.json'},
                     publication_acceptance='PENDING_SECOND_NEW_WHOLE_PACKAGE_REVIEW')
    (A/'MATH_AUDIT_SYNTHESIS.json').write_text(json.dumps(synthesis, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
