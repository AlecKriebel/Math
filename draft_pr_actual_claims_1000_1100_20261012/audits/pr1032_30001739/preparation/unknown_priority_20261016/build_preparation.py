#!/usr/bin/env python3
"""Owned preparation only. No network, Git, publication, or original-input writes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile

PREP = Path(__file__).resolve().parent
BASE = PREP.parents[1]
OUT = BASE / 'preprint_v1_0'
KIT = OUT / 'kit'
TITLE = 'An explicit noninduced Langlands quotient with vanishing unitary periods'
HEAD = '810d52306312623ecfe01ecbc5f5f0dd360972c3'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

VERIFY = r'''#!/usr/bin/env python3
"""Check allowlist and exact bytes, then finite diagnostics; no theorem/priority oracle.

Python 3.10+, standard library. No network, shell, package installation or file writes.
Run with -B to prevent interpreter caches if manually importing checker modules.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import stat
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
def require(value, message):
    if not value:
        raise RuntimeError(message)
def digest(data):
    return hashlib.sha256(data).hexdigest()
def safe_name(name):
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and '..' not in p.parts and '\\' not in name and p.as_posix() == name
def validate_bytes(items):
    names = list(items)
    require(len(set(names)) == len(names), 'duplicate members')
    require('MANIFEST.json' in items and 'ALLOWLIST.json' in items, 'missing inventory')
    manifest = json.loads(items['MANIFEST.json'])
    allow = json.loads(items['ALLOWLIST.json'])['files']
    require(allow == sorted(set(allow)), 'allowlist duplicate/order')
    require(all(safe_name(n) for n in allow), 'unsafe allowlist path')
    require(set(items) == set(allow), 'unlisted or missing package member')
    rows = manifest['files']
    require(len(rows) == len(allow)-1, 'manifest row count')
    require({r['path'] for r in rows} == set(allow)-{'MANIFEST.json'}, 'manifest member mismatch')
    require(len({r['path'] for r in rows}) == len(rows), 'duplicate manifest row')
    for r in rows:
        data = items[r['path']]
        require(len(data) == r['bytes'] and digest(data) == r['sha256'], 'content identity: '+r['path'])
    status = json.loads(items['STATUS.json'])
    require(status['priority_overlap_Luo_Zha'] == 'UNKNOWN', 'priority status')
    require(status['publication_ready'] is False, 'premature readiness')
    require(status['minimum_fresh_complete_independent_reviews'] == 2, 'review gate')
    return manifest
def validate_archive(archive):
    with zipfile.ZipFile(archive) as z:
        info = z.infolist()
        require(len({i.filename for i in info}) == len(info), 'duplicate archive member')
        require(all(safe_name(i.filename) and not i.is_dir() for i in info), 'unsafe archive member')
        require(all(stat.S_IFMT(i.external_attr >> 16) != stat.S_IFLNK for i in info), 'archive symlink')
        require(all(i.date_time == (2026,10,16,0,0,0) and i.compress_type == zipfile.ZIP_STORED for i in info), 'noncanonical archive member')
        return validate_bytes({i.filename:z.read(i) for i in info})
def run(root=ROOT, archive=None):
    files = [p for p in root.rglob('*') if p.is_file()]
    require(not any(p.is_symlink() for p in root.rglob('*')), 'symlink in package')
    items = {p.relative_to(root).as_posix():p.read_bytes() for p in files}
    manifest = validate_bytes(items)
    if archive is not None:
        validate_archive(archive)
        with zipfile.ZipFile(archive) as z:
            require(all(z.read(n) == d for n,d in items.items()), 'archive differs from kit')
    expected = json.loads(items['EXPECTED_RESULTS.json'])
    results=[]
    for mode in ([], ['-O'], ['-OO']):
        for script in expected:
            cmd = [sys.executable, '-I', '-B', *mode, str(root/'scripts'/script)]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
            require(proc.returncode == 0 and not proc.stderr, 'finite diagnostic failed: '+script+' '+repr(mode))
            require(digest(proc.stdout) == expected[script]['sha256'] and len(proc.stdout) == expected[script]['bytes'], 'diagnostic output mismatch: '+script)
            results.append({'script':script,'mode':mode or ['normal'],'stdout_bytes':len(proc.stdout),'sha256':digest(proc.stdout)})
    return {'status':'PASS','files':len(items),'diagnostic_runs':len(results),'results':results,
            'computes_Hom_space':False,'certifies_priority':False,'publication_ready':False}
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--archive',type=Path)
    args=parser.parse_args()
    print(json.dumps(run(archive=args.archive),indent=2,sort_keys=True))
'''

ARCHIVE = r'''#!/usr/bin/env python3
"""Build an allowlisted, uncompressed canonical ZIP. No archive recursion."""
from pathlib import Path
import argparse
import json
import stat
import zipfile
def build(root, target):
    allow = json.loads((root/'ALLOWLIST.json').read_text())['files']
    if sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()) != allow:
        raise RuntimeError('actual file set differs from explicit allowlist')
    if target.exists():
        raise RuntimeError('refusing to replace an existing archive')
    with zipfile.ZipFile(target,'x') as z:
        for name in allow:
            if (root/name).is_symlink():
                raise RuntimeError('symlink')
            i=zipfile.ZipInfo(name,(2026,10,16,0,0,0))
            i.create_system=3
            i.external_attr=(stat.S_IFREG|0o644)<<16
            i.compress_type=zipfile.ZIP_STORED
            z.writestr(i,(root/name).read_bytes())
if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('target',type=Path)
    a=p.parse_args()
    build(Path(__file__).resolve().parents[1],a.target)
'''

PARAMETERS = r'''#!/usr/bin/env python3
"""Finite equivalence comparisons; Luo-Zha parameters remain unknown."""
from collections import Counter
from fractions import Fraction as F
import json
def require(value,message):
    if not value: raise RuntimeError(message)
def dual(m): return [(-b,-a) for a,b in m]
def canonical(m):
    c=min(a for a,b in m)
    return sorted((a-c,b-c) for a,b in m)
def invariant(m):
    lengths=[b-a+1 for a,b in m]
    require(all(x.denominator==1 and x>0 for x in lengths),'invalid length')
    return {'degree':int(sum(lengths)),'lengths':sorted(map(int,lengths)),
            'canonical':[[str(a),str(b)] for a,b in canonical(m)],
            'occurrence_multiplicities':sorted(Counter(m).values())}
M=[(F(a),F(b)) for a,b in [(4,6),(2,5),(3,3),(1,4),(0,2)]]
EXAMPLES={
 'OWR_Minguez':[(F(1),F(2)),(F(-1),F(1)),(F(0),F(0))],
 'LM_Leclerc':[(F(3),F(4)),(F(1),F(3)),(F(2),F(2)),(F(0),F(1))],
 'MOS_Langlands':[(F(4),F(4)),(F(3),F(3)),(F(3),F(3)),(F(2),F(2)),(F(1),F(2)),(F(0),F(1))],
 'MOS_Zelevinsky_dual':[(F(2),F(3)),(F(1),F(4)),(F(0),F(1))],
 'GMM':[(F(1,2),F(3,2)),(F(-1,2),F(7,2)),(F(-3,2),F(-1,2)),(F(-5,2),F(5,2)),(F(-7,2),F(1,2))],
 'Sharma':[(F(0),F(0)),(F(0),F(1)),(F(0),F(1)),(F(1),F(1)),(F(1),F(2))]}
rows=[]
for name,n in EXAMPLES.items():
    equiv=canonical(M) in (canonical(n),canonical(dual(n)))
    require(not equiv,'inspected earlier construction equivalent')
    rows.append({'example':name,'invariant':invariant(n),'translation_dual_reordering_equivalent':equiv})
require(sorted((a+6,b+6) for a,b in dual(M))==sorted(M),'candidate dual identity')
print(json.dumps({'status':'PASS','candidate':invariant(M),'examples':rows,
 'Luo_Zha':{'parameters':'UNKNOWN','mechanism_overlap':'UNKNOWN','period_consequences':'UNKNOWN'},
 'novelty_certified':False},indent=2,sort_keys=True))
'''

TABLE = r'''#!/usr/bin/env python3
"""Check the actual TeX Hall/Y table against complete finite LC graphs."""
from pathlib import Path
import importlib.util
import json
import re
p=Path(__file__).resolve()
spec=importlib.util.spec_from_file_location('table_lc',p.with_name('independent_lc.py'))
lc=importlib.util.module_from_spec(spec)
spec.loader.exec_module(lc)
text=(p.parents[1]/'paper.tex').read_text()
rows=[]
for line in text.splitlines():
    if not re.match(r'^\$[ABCDT]+/[ABCDT]+\$ &',line): continue
    parts=line.split(' & ')
    partition=re.findall(r'[ABCDT]+',parts[0])
    direction=re.findall(r'[ABCDT]+',parts[1])
    m,n=[x.replace('T','E') for x in direction]
    witness=re.findall(r'\(([ABCDT]),([ABCDT])\)',parts[2])[0]
    witness=tuple(x.replace('T','E') for x in witness)
    wanted=[tuple(x.replace('T','E') for x in pair) for pair in re.findall(r'\(([ABCDT]),([ABCDT])\)',parts[3])]
    X,Y,edges=lc.graph(tuple(m),tuple(n))
    actual=[(m[i],n[j]) for i,j in Y]
    x=(m.index(witness[0]),n.index(witness[1]))
    lc.require(x in X and not edges[x],'paper isolated vertex invalid')
    lc.require(sorted(wanted)==sorted(actual),'paper entire Y mismatch')
    lc.require(set(m)|set(n)==set('ABCDE') and not set(m)&set(n),'paper partition invalid')
    lc.require(sorted([set(z.replace('T','E')) for z in partition],key=lambda s:sorted(s))==sorted([set(m),set(n)],key=lambda s:sorted(s)),'paper direction differs from partition')
    rows.append({'partition':partition,'direction':[m,n],'witness':witness,'entire_Y':actual})
lc.require(len(rows)==15,'paper must display fifteen rows')
keys={frozenset(frozenset(z.replace('T','E')) for z in r['partition']) for r in rows}
lc.require(len(keys)==15,'paper repeated partition')
print(json.dumps({'status':'PASS','manuscript_Hall_rows':rows,'computes_Hom_space':False},indent=2,sort_keys=True))
'''

def prepare():
    if (OUT/'PREPARATION_SEAL.json').exists():
        raise RuntimeError('sealed output; refusing mutation')
    KIT.mkdir(exist_ok=True)
    originals = [
        'submitted/current/PROOF.md','submitted/current/MODEL.json',
        'submitted/current/FULL_AUDIT.md','submitted/current/ANALYTIC_AUDIT.md',
        'ROOT_MATH_ACCEPTANCE.json','ROOT_MATH_AUDIT.md','ROOT_MATH_NOTES.md',
        'ROOT_PRIORITY_PENDING.json',
        'reviews/analytic_01/REPORT.md','reviews/analytic_01/INDEPENDENT_DERIVATION.md',
        'reviews/langlands_01/REPORT.md','reviews/langlands_01/DERIVATION.md',
        'reviews/priority_01/REPORT.md']
    copy_map=[]
    for name in originals:
        target=KIT/'historical'/name
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(BASE/name,target)
        copy_map.append({'original_relative_to_audit':name,'copy_relative_to_kit':target.relative_to(KIT).as_posix(),
                         'bytes':target.stat().st_size,'sha256':sha(target.read_bytes()),'copy_semantics':'byte-exact historical authored record; dated status is not this package readiness'})
    scripts=[('reviews/analytic_01/check_analytic_independent.py','check_analytic_independent.py'),
             ('reviews/langlands_01/checks/independent_lc.py','independent_lc.py'),
             ('reviews/langlands_01/checks/mutation_controls.py','mutation_controls.py')]
    for original,name in scripts:
        target=KIT/'scripts'/name
        target.parent.mkdir(exist_ok=True)
        shutil.copyfile(BASE/original,target)
        copy_map.append({'original_relative_to_audit':original,'copy_relative_to_kit':'scripts/'+name,
                         'bytes':target.stat().st_size,'sha256':sha(target.read_bytes()),'copy_semantics':'byte-exact standard-library finite diagnostic'})
    write(KIT/'scripts/verify_kit.py',VERIFY)
    write(KIT/'scripts/build_archive.py',ARCHIVE)
    write(KIT/'scripts/compare_parameters.py',PARAMETERS)
    write(KIT/'scripts/check_manuscript_table.py',TABLE)
    shutil.copyfile(OUT/'paper.tex',KIT/'paper.tex')
    write(KIT/'LICENSE.txt','Copyright 2026 Alec Kriebel. Authored text, code, and original research records in this kit are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/ . Cite the author, title, version and source; indicate changes. Third-party source papers are cited rather than redistributed and retain their own rights. No warranty.\n')
    status={'problem_id':30001739,'pr':1032,'accepted_math_head':HEAD,
        'mathematical_baseline':'ROOT_MATH_ACCEPTANCE.json PASS_COMPLETE_SCOPED_COUNTEREXAMPLE dated 2026-10-13; external published theorems remain dependencies',
        'priority_overlap_Luo_Zha':'UNKNOWN','full_body_Luo_Zha_inspected':False,
        'unrefereed':True,'extensive_AI_use':True,'external_human_peer_review':False,
        'publication_ready':False,'root_adoption':'PENDING',
        'minimum_fresh_complete_independent_reviews':2,'fresh_complete_whole_package_reviews':'PENDING',
        'human_policy':'Leave inaccessible source unknown and work around it; stop full-body retrieval. Historical pending priority gate is retained unchanged as dated evidence, superseded only in workflow by the human instruction.',
        'no_firstness_novelty_or_worldwide_open_claim':True,
        'no_separate_kernel_generation_disproof_claim':True}
    dump(KIT/'STATUS.json',status)
    dump(OUT/'STATUS.json',status)
    dump(KIT/'COPY_MAP.json',copy_map)
    catalog=json.loads((BASE/'reviews/priority_01/SOURCE_CATALOG.json').read_text())
    sources=catalog.get('sources',[]) if isinstance(catalog,dict) else catalog
    keep={'owr_ems','flo_pdf','lm2014_pdf','lm2016_pdf','mos_pdf','bp_pdf','lu_matringe_pdf','sharma_pdf','gmm_pdf','mo2022_pdf','moy_pdf','lz_hku_announcement','luo_zha'}
    credits=[]
    for row in sources:
        if row.get('id') in keep or 'owr' in row.get('id','').lower():
            credit={k:row[k] for k in ['id','title','url','doi','publisher_url','version','publication_vs_announcement','complete_relevant_body_locators','assessment','full_primary_body_retrieved','critical_gap','VOR_published_online','HEP_mirror_date','first_public_announcement_verified','inference_from_abstract_excluded'] if k in row}
            if 'body' in row:
                credit['retained_private_body_identity']={k:row['body'][k] for k in ['sha256','bytes']}
            credit['semantic_scope']='Historical source inspection recorded by priority_01; this preparation did not independently inspect the third-party body. Mathematical dependencies and source comparison are separated in the manuscript.'
            credits.append(credit)
    credits.append({'id':'JPSS','title':'Rankin-Selberg Convolutions','authors':['Herve Jacquet','I. I. Piatetski-Shapiro','Joseph A. Shalika'],
        'url':'https://www.math.columbia.edu/~hj/Rankin%20Selberg%20convolutions.pdf',
        'locators':'Theorem 8.2, (5), pp.444-445; epsilon units section2.9 p.396',
        'semantic_scope':'Published theorem interface authenticated in analytic_01 and root audit. Segment L-factors only; not a period-multiplicity theorem. No new third-party body inspection in preparation.'})
    dump(KIT/'SOURCE_CREDITS.json',{'scope':'Bounded source comparison and explicit attribution, not priority clearance','Luo_Zha_overlap':'UNKNOWN','sources':credits})
    dump(KIT/'OMISSIONS.json',{
        'selection':'Thirteen historical authored reports/models/root records and three byte-exact stdlib checkers, plus newly authored manuscript/metadata/portable verifier; no recursive custody closure claim.',
        'omitted_classes':[
          {'class':'All third-party raw PDF/HTML/API bodies, extracted/OCR texts, source images','reason':'private inspection evidence; third-party rights and portable lean scope'},
          {'class':'Historical archives, environmental harnesses, UID1000/permission fixtures, imported runtimes and SymPy-based original diagnostic programs','reason':'not needed for new stdlib replay; no historical environment or baseline replay claimed'},
          {'class':'Historical check stdout/stderr receipts, input/output pin trees and individual source retrieval attempts','reason':'retained unchanged in original audit, not recursively redistributed; selected report claims remain dated evidence'},
          {'class':'Original full audit tree except selected allowlisted files','reason':'lean support selection, not a complete archival custody export'},
          {'class':'New preparation scripts, raster page QA images and local receipts','reason':'preparation evidence remains outside release kit; output seal inventories it separately'}],
        'all_preexisting_original_files':'287 files pinned privately by preparation/unknown_priority_20261016/ORIGINAL_INPUT_PINS.json and rechecked before sealing',
        'selected_historical_policy':'Original ROOT_PRIORITY_PENDING and priority report are byte-exact dated historical decisions. Their old next gate is superseded only as workflow by the new human instruction; their UNKNOWN comparison findings remain applicable.',
        'replay_claim':'New standard-library finite runs only; neither mathematical Hom computation nor environmental-seal reproduction nor worldwide literature search'})
    readme='''# PR1032 / problem30001739 support kit, v1.0

The complete note is paper.pdf; its standalone source is paper.tex. The exact field is F=Q3 and E/F unramified quadratic. The five-segment GL15 Langlands quotient is tau invariant, is not an entire proper parabolic induction, and has Hom(U(V),pi,C)=0 for each Hermitian class, conditional on the explicitly cited established theorems. The standard module is not the quotient.

Historical priority, exact parameter/mechanism overlap, and any period consequences in Luo-Zha DOI10.1007/s11464-025-0256-0 are UNKNOWN. Their complete body was not inspected. Their documented prior kernel-generation claim is credited. No firstness, worldwide novelty/current-open claim, or separate kernel-generation disproof is made. The human has instructed that the inaccessible comparison remain unknown and preparation proceed. No further source retrieval or outreach was attempted.

Run `python3 scripts/verify_kit.py` with Python3.10+ standard library only. Add `--archive PATH` to verify the deterministic archive against the unpacked kit. It checks exact members and hashes, then five finite programs in normal/-O/-OO (15 runs), including the actual manuscript Hall table. No network or third-party Python packages. Do not add files inside this exact allowlist tree. Extract archive members into a fresh empty folder. Expected outputs are deterministic and optimization-safe; original checker imports can be avoided with `-B` when invoking manually. The verifier itself passes -I -B in subprocesses.

Finite scalar/order/parity, Hall/injection, positive-calibration and hostile-definition checks corroborate the proof. They do not compute Hom spaces, prove published dependency theorems, validate a universal matching algorithm, or certify priority. scripts/compare_parameters.py checks only six explicitly listed earlier parameter families and preserves multiplicities. Luo-Zha remains unknown.

scripts/build_archive.py TARGET reconstructs the stored canonical uncompressed ZIP from ALLOWLIST.json into a new target (refuses replacement); no timestamp or filesystem-order variation is introduced. The supplied PDF is pinned, but recompilation via `tectonic paper.tex` or another suitable TeX engine may change PDF bytes. The source requires amsmath/amssymb/amsthm, geometry, booktabs/array, lmodern, xurl and hyperref. No TeX runtime is bundled.

COPY_MAP.json identifies every historical copy. Historical report acceptances certify their assigned old scope, not this newly assembled paper/package. Their pending-priority policy remains byte-exact dated history and is superseded only in workflow by the latest human instruction; priority findings remain UNKNOWN. SOURCE_CREDITS.json records the bounded source theorem/comparison scope. OMISSIONS.json explicitly denies recursive archival closure. No third-party source bodies/images/API responses or runtime fixtures are included.

The authored text/code are CC BY4.0; Alec Kriebel, ORCID0009-0001-9320-500X. AI tools were used extensively for construction, source comparison, adversarial checks, code and writing. This is unrefereed, without external human peer review, journal acceptance or proof-assistant certification. Publication readiness is FALSE pending root adoption and at least TWO fresh independent COMPLETE whole-paper/package adversarial reviews. This package is preparation, not one of those reviews. No service action or deposit occurred. No DOI is assigned here.
'''
    write(KIT/'README.md',readme)
    write(OUT/'README.md',readme.replace('Run `python3 scripts/verify_kit.py`','Run `python3 kit/scripts/verify_kit.py`').replace('The complete note is paper.pdf','The release objects are paper.pdf and pr1032_supportkit_v1.0.zip. The complete note is paper.pdf'))
    bib='''@unpublished{Kriebel2026UnitaryPeriods,
  author = {Kriebel, Alec},
  title = {An explicit noninduced Langlands quotient with vanishing unitary periods},
  year = {2026},
  month = oct,
  version = {1.0},
  note = {Unrefereed, extensively AI-assisted preparation. Historical priority and overlap with Luo--Zha, DOI 10.1007/s11464-025-0256-0, UNKNOWN. No external human peer review or firstness claim},
  orcid = {0009-0001-9320-500X},
  license = {CC-BY-4.0}
}
'''
    write(OUT/'CITATION.bib',bib);write(KIT/'CITATION.bib',bib)
    description='''<p>This attributed mathematical note gives a complete checkable proof for F=Q3 and its unramified quadratic extension E: the GL15 Langlands quotient with segments [4,6],[2,5],[3,3],[1,4],[0,2] is tau invariant, is not an entire proper parabolic induction, and has no unitary-stabilizer period for either Hermitian isometry class. The total is zero instead of two in the historical OWR14/2011 Conjecture4 k=1 smooth-complex p-adic interpretation. The same example contradicts FLO Conjecture6.12 and the unrestricted local unitary Jacquet converse; it does not contradict generic or tempered positive results.</p><p>FLO supplies the complete period bases, normalization, functional equations and adjacent-label exclusion. JPSS supplies segment L-factors; Lapid-Minguez supplies classification, ladder-side matching, involution and prior kernel transport. Gurevich-Ma-Mitra and Mitra-Offen-Sayag supply earlier imprimitive negative-distinction and quotient-descent antecedents for different subgroups. Beuzart-Plessis and Lu-Matringe receive credit for established generic/tempered results; Sharma for a different five-segment combinatorial comparison.</p><p>Historical priority and every substantive overlap comparison with Luo-Zha, A Remark on Bernstein-Zelevinsky Classification for General Linear Groups, DOI10.1007/s11464-025-0256-0, are UNKNOWN. Their complete body was unavailable and uninspected. Their documented earlier kernel-generation counterexample claim is credited. This note may overlap or be superseded by it. No worldwide novelty, firstness, current-open-status or separate kernel-generation disproof claim is made.</p><p>AI tools were used extensively in construction, source comparison, adversarial checks, computations and writing. This is unrefereed, without external human peer review, journal acceptance or proof-assistant certification. The standard-library exact verification kit corroborates finite identities and conditions; the written argument and published theorem dependencies establish the representation-theoretic conclusion. Preparation readiness remains false pending root adoption and at least two fresh independent complete whole-package adversarial reviews. Authored text and code are CC BY4.0. No deposit or DOI assignment is asserted.</p>'''
    refs=[]
    for match in re.finditer(r'\\bibitem\{([^}]+)\}\s*(.*?)(?=\n\\bibitem|\n\\end\{thebibliography\})',(OUT/'paper.tex').read_text(),re.S):
        refs.append({'key':match.group(1),'tex_bibliographic_object':match.group(2).strip()})
    dump(KIT/'BIBLIOGRAPHIC_OBJECTS.json',{'source':'paper.tex thebibliography; exact same paper bibliography','items':refs})
    metadata={'title':TITLE,'upload_type':'publication','publication_type':'preprint','publication_date':'2026-10-16','version':'1.0',
       'creators':[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],
       'description':description,'access_right':'open','license':'cc-by-4.0','language':'eng',
       'keywords':['unitary periods','Langlands quotient','parabolic induction','multisegments','unknown historical priority','unrefereed preprint'],
       'notes':'Prepared locally. No deposit, DOI, publication, firstness or human peer review claimed. Luo-Zha body uninspected; overlap UNKNOWN. Publication readiness false pending root adoption and two fresh independent complete whole-package reviews.',
       'references':[
        'E. Lapid, OWR14/2011, EMS pp.729,731,734. DOI10.4171/OWR/2011/14.',
        'B. Feigon, E. Lapid, O. Offen, On representations distinguished by unitary groups, PMIHES115(2012),185-323. DOI10.1007/s10240-012-0040-z.',
        'H. Jacquet, I. I. Piatetski-Shapiro, J. A. Shalika, Rankin-Selberg Convolutions, AJM105(1983),367-464.',
        'E. Lapid, A. Minguez, On parabolic induction on inner forms of the general linear group over a non-archimedean local field, SelectaMath22(2016),2347-2400; arXiv1411.6310v3.',
        'E. Lapid, A. Minguez, On a determinantal formula of Tadic, AJM136(2014),111-142; undated 29-page author manuscript inspected.',
        'M. Gurevich, J.-J. Ma, A. Mitra, On two questions concerning representations distinguished by the Galois involution, ForumMath30(2018),141-157; arXiv1609.03155v1.',
        'A. Mitra, O. Offen, E. Sayag, Klyachko Models for Ladder Representations, DocumentaMath22(2017),611-657.',
        'R. Beuzart-Plessis, Multiplicities and Plancherel formula for the space of nondegenerate Hermitian matrices, JNT230(2022),5-63; arXiv2008.05036v2.',
        'H. Lu, N. Matringe, On completeness of local intertwining periods, JFA291(2026),111486; arXiv2503.11988v2.',
        'N. Matringe, O. Offen, Intertwining periods and distinction for p-adic Galois symmetric pairs, PLMS125(2022),1179-1252; arXiv2102.00480v2.',
        'N. Matringe, O. Offen, C. Yang, On local intertwining periods, JFA286(2024),110293; arXiv2303.03663v2.',
        'H. Sharma, Duality, rigidity, and peeling for multisegments: on hypotheses of Mitra, Offen, and Sayag, arXiv2609.21384v1 (2026).',
        'C. Luo, J. Zha, A Remark on Bernstein-Zelevinsky Classification for General Linear Groups, Front.Math online2026. DOI10.1007/s11464-025-0256-0. Full body uninspected; substantive overlap UNKNOWN.',
        'CUHK(SZ)-HKU Representation Theory WorkshopII program, May13,2025, pp.1,4. https://hkumath.hku.hk/MathWWW/event/2025/Workshop_Program.pdf']}
    dump(OUT/'.zenodo.json',metadata);dump(KIT/'.zenodo.json',metadata)
    dump(OUT/'zenodo-deposit.json',{'metadata':metadata,'files':[{'path':'paper.pdf','name':'paper.pdf'},{'path':'pr1032_supportkit_v1.0.zip','name':'pr1032_supportkit_v1.0.zip'}]})
    # The native repo uploader resolves paths relative to this manifest. It is only written if absent.
    native=BASE/'publication/zenodo-deposit.json'
    wanted={'metadata':metadata,'files':[{'path':'../preprint_v1_0/paper.pdf','name':'paper.pdf'},{'path':'../preprint_v1_0/pr1032_supportkit_v1.0.zip','name':'pr1032_supportkit_v1.0.zip'}]}
    if native.exists():
        if json.loads(native.read_text()) != wanted:
            raise RuntimeError('native manifest exists with different content; refusing replacement')
    else:
        dump(native,wanted)
    expected={}
    receipts=[]
    for script in ['check_analytic_independent.py','independent_lc.py','mutation_controls.py','compare_parameters.py','check_manuscript_table.py']:
        baseline=None
        for flags in ([],['-O'],['-OO']):
            cmd=[sys.executable,'-I','-B',*flags,str(KIT/'scripts'/script)]
            run=subprocess.run(cmd,capture_output=True,timeout=60)
            if run.returncode or run.stderr:
                raise RuntimeError(script+': '+repr(run.stderr))
            if baseline is None:baseline=run.stdout
            if run.stdout != baseline:raise RuntimeError('optimization output mismatch')
            receipts.append({'utc':datetime.now(timezone.utc).isoformat(),'command':cmd,'returncode':run.returncode,'stdout_bytes':len(run.stdout),'stdout_sha256':sha(run.stdout),'stderr_bytes':len(run.stderr)})
        expected[script]={'bytes':len(baseline),'sha256':sha(baseline)}
    dump(KIT/'EXPECTED_RESULTS.json',expected)
    dump(PREP/'CHECK_RUNS.json',{'scope':'new portable finite replay; not historical environmental harness or Hom computation','runs':receipts})
    dump(PREP/'PREPARATION_CHECKPOINT.json',{'utc':datetime.now(timezone.utc).isoformat(),'completion_percent':70,'publication_ready':False,'selected_historical_records':len(originals),'byte_exact_checker_copies':len(scripts),'finite_runs':len(receipts)})
    print(json.dumps({'prepared':str(OUT),'check_runs':len(receipts),'historical_records':len(originals),'credit_rows':len(credits)}))

if __name__=='__main__':
    prepare()
