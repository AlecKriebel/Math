"""Apply all seven findings to current presentation, preserving version-one evidence.

Local authoring only. No provider, Git, Queue, publication or tracker access.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess

B=Path(__file__).resolve().parent
D=B.parent/'initial_review_20261015'
V=B/'verification'
N=B/'pr_update/5100033'
PY='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python'


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,data): p.write_text(json.dumps(data,indent=2)+'\n')
def change(p,old,new):
    text=p.read_text()
    assert old in text, (str(p),old)
    p.write_text(text.replace(old,new))


def main():
    assert sha(B/'k605a-source-verification.zip')=='6324b31294ed313e523f85454ba4c4b82b412d0942432e7cae7ef611140bea6b'
    assert not (B/'history/review01_frozen').exists(), 'Revision already started: reconcile local outcomes, do not repeat.'
    now=datetime.now(timezone.utc).isoformat()
    old=B/'history/review01_frozen';old.mkdir(parents=True)
    for name in ['manuscript.tex','manuscript.pdf','metadata.json','k605a-source-verification.zip','SOURCE_MANIFEST.json','PACKAGE_MANIFEST.json']:
        shutil.copyfile(B/name,old/name)
    shutil.copyfile(V/'MANIFEST.json',old/'VERIFICATION_MANIFEST.json')
    save(old/'HISTORICAL_STATUS.json',dict(utc=now,role='Exact first whole-manuscript review input, superseded by explicit review01 revision; never relabel the first review as accepting revised bytes',review_report_sha256='acd3f1751af73a3902d0f6d31ecc6d9d9dcb8d60ed020ff86e99dd3ff203ea99',input_zip_sha256=sha(old/'k605a-source-verification.zip')))
    # Preserve the older negative-center control whose LIMITATION prose was stale.
    hist=V/'forensic_history/review01_projective_limits';hist.mkdir(parents=True)
    for name in ['root_priority_projective_control.py','ROOT_PRIORITY_PROJECTIVE_CONTROL.json']:
        shutil.copyfile(V/'scope_controls'/name,hist/name)
    old_script=(hist/'root_priority_projective_control.py').read_bytes()
    old_result=json.loads((hist/'ROOT_PRIORITY_PROJECTIVE_CONTROL.json').read_text())
    old_lim='Algebraic equivalence used to examine prior general Poncelet theorems. No new invariant proof, claim of novelty, bicentric circle/circle reduction, or prior-coverage conclusion.'
    new_lim='Exact focal projectivity gives a circle/noncircular-ellipse pair; the additional stated polarity gives a genuine bicentric circle pair with the displayed negative center. These geometric correspondences alone do not prove the area invariant or historical priority; the separately written contact-area/phase reduction supplies the additional work. No novelty or first-proof claim.'
    assert old_result['limits']==old_lim
    change(D/'root_priority_projective_control.py',old_lim,new_lim)
    run=subprocess.run([PY,'-B',str(D/'root_priority_projective_control.py')],capture_output=True,check=True)
    current=json.loads(run.stdout)
    assert {k:v for k,v in current.items() if k!='limits'}=={k:v for k,v in old_result.items() if k!='limits'}
    assert old_script.replace(old_lim.encode(),new_lim.encode())==(D/'root_priority_projective_control.py').read_bytes()
    (D/'ROOT_PRIORITY_PROJECTIVE_CONTROL.json').write_bytes(run.stdout)
    for name in ['root_priority_projective_control.py','ROOT_PRIORITY_PROJECTIVE_CONTROL.json']:
        shutil.copyfile(D/name,V/'scope_controls'/name)
    reconciliation=dict(utc=now,finding='R3',role='Current interpretation-only reconciliation; original polarity-sign correction remains dated and unchanged',
        historical_correction='audit_receipts/ROOT_POLARITY_SIGN_CORRECTION.json',
        old_program=dict(path='forensic_history/review01_projective_limits/root_priority_projective_control.py',sha256=sha(hist/'root_priority_projective_control.py')),
        old_result=dict(path='forensic_history/review01_projective_limits/ROOT_PRIORITY_PROJECTIVE_CONTROL.json',sha256=sha(hist/'ROOT_PRIORITY_PROJECTIVE_CONTROL.json')),
        current_program=dict(path='scope_controls/root_priority_projective_control.py',sha256=sha(V/'scope_controls/root_priority_projective_control.py')),
        current_result=dict(path='scope_controls/ROOT_PRIORITY_PROJECTIVE_CONTROL.json',sha256=sha(V/'scope_controls/ROOT_PRIORITY_PROJECTIVE_CONTROL.json')),
        changed_result_fields=['limits'],scientific_algebra_unchanged=True,all10exact_identities_replayed=True,
        script_changed_only_the_exact_limitation_literal=True)
    save(D/'ROOT_PROJECTIVE_PRESENTATION_RECONCILIATION.json',reconciliation)
    save(V/'audit_receipts/ROOT_PROJECTIVE_PRESENTATION_RECONCILIATION.json',reconciliation)
    save(hist/'HISTORICAL_STATUS.json',dict(utc=now,role='Superseded current-interpretation prose; negative-center algebra remains correct. Neither file is a current replay target.',current_reconciliation='../../audit_receipts/ROOT_PROJECTIVE_PRESENTATION_RECONCILIATION.json'))
    # R1: independent direct Cartesian parity proof, with the source fixture error separated.
    for name in ['root_exact_even_control.py','ROOT_EXACT_EVEN_CONTROL.json']:
        shutil.copyfile(D/name,V/'scope_controls'/name)
    shutil.copyfile(D/'ROOT_EVEN_BOUNDARY_AND_SOURCE_CORRECTION.json',V/'audit_receipts/ROOT_EVEN_BOUNDARY_AND_SOURCE_CORRECTION.json')
    change(B/'manuscript.tex','The even countercontrols below show that the odd hypothesis is essential.','The exact counterexample in Section~6 shows that the odd hypothesis is essential for primitive families.')
    marker='The portable archive preserves the original submission, independent\n'
    parity=r'''Oddness cannot be dropped for primitive families. On $x^2/4+y^2=1$
with $\lambda=4/5$, put $t=1/\sqrt5$. The two primitive four-periodic phases
\[
 D=((2,0),(0,1),(-2,0),(0,-1)),\qquad
 C=((4t,t),(-4t,t),(-4t,-t),(4t,-t))
\]
satisfy the same caustic equation $x^2/(16/5)+y^2/(1/5)=1$ and the unit
reflection law. Direct substitution in the focal-foot formula and shoelace
sum gives $B_\pm(D)=4$ and $B_\pm(C)=5$, hence products $16$ and $25$.
The archive supplies 96 exact zero residuals for boundary, reflection,
caustic and actual outer-side projection checks. The rectangle coordinates
printed in \cite[Section 6, p.~6]{F62} differ from $C$ and fail reflection;
its printed inverse-product values fit the corrected rectangle $C$.
The supporting source-correction note documents this local fixture error;
the cited all-odd proof and credited triangular inputs remain valid.

'''
    # Raw authoring string uses doubled slashes only to make this patch readable.
    parity=parity.replace('\\\\','\\')
    change(B/'manuscript.tex',marker,parity+marker)
    # R2 and O4: current human-authorship claims and current/historical bases.
    unsupported='The present author did not coauthor those candidates. '
    change(N/'PROOF.md',unsupported,'')
    change(B/'prepare_native_presentation.py',"    proof += '''", "    proof = proof.replace('The present author did not coauthor those candidates. ', '')\n    proof += '''")
    (N/'PROOF.md').open('a').write('\n## 9. Exact primitive-even boundary and current notation\n\nFor E:x²/4+y²=1 and lambda4/5, D=((2,0),(0,1),(-2,0),(0,-1)) and C=((4/sqrt5,1/sqrt5),(-4/sqrt5,1/sqrt5),(-4/sqrt5,-1/sqrt5),(4/sqrt5,-1/sqrt5)) are genuine primitive4periodic phases of the same family. Direct exact unit reflection/caustic/outer projection gives B_e(D)=4 and B_e(C)=5, products16and25 (96 zero residuals in the new standalone control). Thus the primitive-even extension is false. Fixed repeats of an odd primitive family retain the repetition corollary. Ferudun0062p6 prints a different, invalid square; current source notes distinguish its corrected rectangle from literal source coordinates without questioning its valid all-odd proof. In the historical bicentric bridge, K_N=K(m_N) uses parameter notation; in modulus notation it means K_N=K(sqrt(m_N)).\n')
    (N/'SOURCES.md').open('a').write('\nCurrent source correction after first whole-package review: Ferudun0062v1.0p6 prints rectangle(+-2/sqrt5,+-2/sqrt5). It is on the ellipse but fails unit reflection with residual(9/17,-15/17) and has alternating confocal parameters1/5,16/5. Correct common-lambda4/5 rectangle is(+-4/sqrt5,+-1/sqrt5), whose unit-inverse products fit the printed values1and25/16; its outer focal-pedal products are25 versus diamond16. The source all-odd proof and H/Vtriangles survive independent checking. See portable CURRENT_CONVENTIONS_AND_CORRECTIONS.md and exact96-residual control. No outreach was prepared.\n')
    v1_note='\nThe top-level `MANIFEST_V1.json` is a retained historical copy. Interpret its entries against `history/original_submission_20261015/`, with the one documented superseded SOURCES.md hash explained by the historical metadata correction. It is not an active manifest for edited current files; use CURRENT_PACKET_MANIFEST.json and the current MANIFEST/PUBLICATION_MANIFEST.\n'
    (N/'README.md').open('a').write(v1_note)
    # Ensure the one-time preparation utility documents the same historical role.
    change(B/'prepare_native_presentation.py','Current top-level manifests bind the reconciled presentation, while old manifests, pending-review statements, old source-only checkpoint and worktree paths are preserved as dated history.',
        'Current top-level manifests bind the reconciled presentation. The top-level MANIFEST_V1.json is historical: evaluate its entries against history/original_submission_20261015/, allowing the one documented superseded SOURCES.md hash, never against edited current files. Old pending-review statements, source-only checkpoint and worktree paths are preserved as dated history.')
    # O1: both corrected references must resolve in the relocated package.
    change(B/'README.md','`history/original_submission_20261015/`','`pr_update/5100033/history/original_submission_20261015/`')
    hp=V/'forensic_history/polarity_sign_intermediate_20261015/HISTORICAL_STATUS.json'
    status=json.loads(hp.read_text());status['current_correction']='../../audit_receipts/ROOT_POLARITY_SIGN_CORRECTION.json';save(hp,status)
    assert (hp.parent/status['current_correction']).resolve().is_file()
    # Ten current jobs, adding a new exact control without touching the five sealed families.
    change(V/'run_verification.py','"""Portable nine-job replay,','"""Portable ten-job replay,')
    change(V/'run_verification.py'," 'root_projective':('scope_controls/root_priority_projective_control.py'", " 'root_exact_even':('scope_controls/root_exact_even_control.py','scope_controls/ROOT_EXACT_EVEN_CONTROL.json','stdout'),\n 'root_projective':('scope_controls/root_priority_projective_control.py'")
    old_checks="""    require(digest(BASE/'scope_controls/root_priority_projective_control.py')==correction['corrected_program_sha256'],'corrected projective script')
    require(digest(BASE/'scope_controls/ROOT_PRIORITY_PROJECTIVE_CONTROL.json')==correction['corrected_result_sha256'],'corrected projective result')"""
    new_checks="""    current=load('audit_receipts/ROOT_PROJECTIVE_PRESENTATION_RECONCILIATION.json')
    require(current['old_program']['sha256']==correction['corrected_program_sha256'],'historical corrected program binding')
    require(current['old_result']['sha256']==correction['corrected_result_sha256'],'historical corrected result binding')
    for item in ['old_program','old_result','current_program','current_result']:
        require(digest(BASE/current[item]['path'])==current[item]['sha256'],'projective reconciliation '+item)
    a=load(current['old_result']['path']);b=load(current['current_result']['path'])
    require({k:v for k,v in a.items() if k!='limits'}=={k:v for k,v in b.items() if k!='limits'},'unchanged projective algebra')
    require(current['changed_result_fields']==['limits'],'limited interpretation correction')"""
    change(V/'validate_payloads.py',old_checks,new_checks)
    new_job="""    if job=='root_exact_even':
        require(d['primitive_period']==4 and d['caustic_lambda']=='4/5' and d['exact_zero_count']==96,'exact even parameters/count')
        require([x['outer_pedal_product'] for x in d['cases']]==['16','25'],'exact even products')
        require([x['original_unit_inverse_product'] for x in d['cases']]==['1','25/16'],'corrected source inverse products')
        for r in d['cases']:
            require(r['exact_zero_count']==48 and len(r['zero_residuals'])==48 and set(r['zero_residuals'].values())=={'0'},'exact even residuals')
        require(d['literal_printed_Ferudun0062_p6_rectangle']['genuine_billiard'] is False,'source false fixture labelled')
        return {'exact_zero_residuals':96,'genuine_primitive_even_phases':2,'source_false_fixture':1}
"""
    change(V/'validate_payloads.py',"    if job=='root_projective':",new_job+"    if job=='root_projective':")
    # O2/O3 plus accurate versioned preparation receipts.
    for old_word,new_word in [('nine-job','ten-job'),('all nine current jobs','all ten current jobs'),('other five jobs','other six jobs'),('all-period theorem','all-period theorem')]:
        if old_word!=new_word and old_word in (V/'README.md').read_text():change(V/'README.md',old_word,new_word)
    # Already changed by the preceding version-wording loop.
    change(V/'README.md','Even-period products vary in the negative','Even primitive-period products vary in the negative')
    change(V/'README.md','| `root_projective` |','| `root_exact_even` | 96 exact zero residuals; genuine N4 products16 and25, corrected source fixture | None |\n| `root_projective` |')
    (V/'README.md').open('a').write('''

## Current review01 revision and conventions

The current harness has ten jobs, including the new exact primitive-even control. The earlier embedded preparation/replay receipts describe the dated nine-job version; their frozen inputs and scientific hashes must not be relabelled as the revised ten-job result. Final current-package root replays and subsequent whole-manuscript reviews are recorded alongside the case, outside this ZIP, to avoid a self-referential approval archive.

`CURRENT_CONVENTIONS_AND_CORRECTIONS.md` explains the exact parity example, related primary-source fixture error, parameter notation and current versus historical interpretation bindings. In the sealed earlier bicentric bridge, section6's `K(m_N)` uses the complete-integral parameter convention: with the modulus convention of its section1 and the current manuscript, this is `K_N=K(sqrt(m_N))`. The `dn(x,m_N)` in that comparison also uses parameter syntax. The historical family document is preserved byte-for-byte.

The original polarity erratum still binds the then-current negative-center program/result. Their stale limits sentence was subsequently corrected under R3; `audit_receipts/ROOT_PROJECTIVE_PRESENTATION_RECONCILIATION.json` binds both preserved older files and the current pair. Only interpretation text changed; all ten symbolic identities and geometric fields are identical. Old receipts are historical, not silently rebound. The relocated old-sign status pointer now correctly resolves to `audit_receipts/ROOT_POLARITY_SIGN_CORRECTION.json`; its wrong-sign program/result bytes remain unchanged. No forensic program is in the current JOBS table.
''')
    (V/'CURRENT_CONVENTIONS_AND_CORRECTIONS.md').write_text('''# Current mathematical conventions and source corrections

This current companion resolves first whole-manuscript findings R1-R3 and O1-O4 without rewriting any of the20 original submission files or five sealed earlier audit families.

For E:x²/4+y²=1 and lambda4/5, D=((2,0),(0,1),(-2,0),(0,-1)) and C=((4/sqrt5,1/sqrt5),(-4/sqrt5,1/sqrt5),(-4/sqrt5,-1/sqrt5),(4/sqrt5,-1/sqrt5)) are genuine primitive4-periodic phases. The standalone exact Cartesian control validates boundary/unit-reflection/common-caustic/actual-outer-side feet with96 zero residuals. Areas at both original foci are4 for D and5 for C, hence products16 and25. Even primitive periods cannot be added to the theorem; even repeated lists with odd least period retain the separate repetition deduction.

Ferudun, Products of the Two Focal Inversion Areas in Elliptic Billiards,v1.0,2October2026,DOI10.5281/zenodo.23096994, printedp6, instead prints(+-2/sqrt5,+-2/sqrt5). This square lies on E but fails unit reflection with residual(9/17,-15/17) and has alternating caustic parameters1/5,16/5. Its printed inverse-product values1and25/16 fit the corrected rectangleC above. Root and the first new adversary independently encountered this error; both read the actual primary page. The all-odd inverse proof and credited H/V triangular inputs remain valid. This is a corrected example, not the literal coordinates of that source or a refutation of its odd theorem. Source hash/reading evidence and exact negative control are retained; no outreach was prepared.

All Jacobi functions in the direct proof use modulus k. In the historical bicentric companion, m_b and m_N are parameters; K(m_N) in section6 means the parameter convention. In consistent modulus notation K_N=K(sqrt(m_N)); dn(x,m_N) there likewise uses parameter syntax. The numerical implementation uses mpmath's parameter interface. This clarification preserves the sealed earlier family and does not alter an equation mathematically.

The focal projectivity alone maps the confocal pair to a circle/noncircular-ellipse pair. The additional stated polarity gives a genuine bicentric pair with the correct negative center. Those geometric correspondences alone are not an area-product proof or historical-priority certificate. The current script/result limitation now says this; the older otherwise-correct negative-center control and its stale prose are explicitly forensic, with old/current hashes in ROOT_PROJECTIVE_PRESENTATION_RECONCILIATION.json. The separate old positive-center error and its erratum remain preserved too.

Current native authorship wording no longer asserts that the human author did not coauthor other campaign candidates. Independent internal AI review approaches do not establish human authorship or public-priority independence. The original unsupported sentence remains only in explicitly preserved original history. The top-level native MANIFEST_V1 copy is historical and based on that history, with its one documented superseded SOURCES.md hash; active manifests bind current files. Current top README and forensic-status links use their actual relocated paths.

Historical novelty/public proof priority remain undetermined. Extensive AI assistance and unrefereed/no-human-peer-review/no-formal-proof-assistant limitations remain in force. This revision does not grant publication authorization; a different second NEW full-package adversary is still required.
''')
    # Keep future helpers consistent with the actual ten-job package.
    for p in [B.parent/'publication/append_verified_tracker.py',D/'ROOT_PUBLICATION_LOCAL_PREPARATION.json']:
        if p.exists():p.write_text(p.read_text().replace('Portable nine-job','Portable ten-job'))
    change(B/'build_bundle.py',"'NATIVE_RELEASE_PLAN.json', 'RENDER_QA.json'", "'NATIVE_RELEASE_PLAN.json', 'RENDER_QA.json', 'apply_review01_fixes.py', 'REVIEW01_RESOLUTION.json'")
    # Verify that all original20 inputs still match in every required location.
    intake=json.loads((D/'INTAKE.json').read_text())
    for row in intake['original_source_files']:
        rel=Path(row['native_path']).relative_to('unsolved_math_prioritization/attempts/5100033')
        for p in [V/'original_submission'/rel,N/'history/original_submission_20261015'/rel]:
            assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
    resolution=dict(utc=now,review_report_sha256='acd3f1751af73a3902d0f6d31ecc6d9d9dcb8d60ed020ff86e99dd3ff203ea99',
        reviewed_input_zip_sha256='6324b31294ed313e523f85454ba4c4b82b412d0942432e7cae7ef611140bea6b',
        findings={k:'Implemented in current presentation; full replay/render/reseal validation pending' for k in ['R1','R2','R3','O1','O2','O3','O4']},
        original20_and_five_sealed_families_preserved=True,current_jobs=10,
        current_projective_algebra_unchanged_except_limits=True,
        second_new_review_assigned=False,publication_cleared=False)
    save(B/'REVIEW01_RESOLUTION.json',resolution)
    save(D/'REVIEW01_RESOLUTION_PROGRESS.json',resolution)
    print(json.dumps(dict(all7current_changes_applied=True,next_steps='Seal/replay/compile/render/rebuild/independent validation, then different second NEW review'),indent=2))


if __name__=='__main__': main()
