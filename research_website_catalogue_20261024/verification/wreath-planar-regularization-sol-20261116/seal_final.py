"""Data-only finite closure. No mathematics/native/project code, network or Git execution."""
from pathlib import Path
import hashlib,json,stat,datetime
R=Path(__file__).resolve().parent;P=R.parents[1];S=P/'papers/23203143/sources'
def pin(p,root=None):
    st=p.lstat()
    if not stat.S_ISREG(st.st_mode):raise RuntimeError('not regular: '+str(p))
    b=p.read_bytes()
    return dict(path=p.relative_to(root).as_posix() if root else str(p),bytes=len(b),SHA256=hashlib.sha256(b).hexdigest(),mode=oct(stat.S_IMODE(st.st_mode)))
def inv(root):
    fs=[];ds=[]
    for p in sorted(root.rglob('*')):
        st=p.lstat()
        if stat.S_ISREG(st.st_mode):fs.append(pin(p,root))
        elif stat.S_ISDIR(st.st_mode):ds.append(dict(path=p.relative_to(root).as_posix(),mode=oct(stat.S_IMODE(st.st_mode))))
        else:raise RuntimeError('unexpected topology '+str(p))
    return fs,ds
def create(n,x):
    with (R/n).open('x') as f:f.write(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
for n in ('CLOSING_GUARDS.json','MANIFEST.json','FINAL.json'):
    if (R/n).exists():raise RuntimeError('already sealed')
c=json.loads((R/'SOURCE_CUSTODY.json').read_text());sf,sd=inv(S)
if sf!=c['files'] or sd!=c['directories'] or oct(stat.S_IMODE(S.lstat().st_mode))!=c['root_mode']:raise RuntimeError('source drift')
for n,digest in [('INITIAL_SEAL.json','318bcf7d7714002b4890e5d076b4600e13ff4fc2c3dd49af59376b74785b9c97'),
    ('INITIAL_MANIFEST.json','d587887d0311689bddf15099d5680962c7e8a2079693a749b39050494cb60d75')]:
    if pin(R/n,R)['SHA256']!=digest:raise RuntimeError('INITIAL control drift')
im=json.loads((R/'INITIAL_MANIFEST.json').read_text())
for q in im['payload_files']:
    if pin(R/q['path'],R)!=q:raise RuntimeError('INITIAL payload drift '+q['path'])
for d in im['directories']:
    st=(R/d['path']).lstat()
    if not stat.S_ISDIR(st.st_mode) or oct(stat.S_IMODE(st.st_mode))!=d['mode']:raise RuntimeError('INITIAL directory drift')
for n in ('SOURCE_AUTH.stderr.txt','PDFINFO.stderr.txt','PDFTEXT.stderr.txt','RASTER.stdout.txt','RASTER.stderr.txt'):
    if (R/n).read_bytes()!=b'':raise RuntimeError('nonempty initial source stream')
external=[]
for path,expected_bytes,digest in [
 ('/Users/alec/Documents/Math/openai_wreath_planar_consequences/sources/triangle/cdls_2206.15373v1.pdf',607768,'8a98d3f2d55e859a364f5aa9448d17c3535d0f244aee644242872ea7aed023b5'),
 ('/Users/alec/Documents/Math/openai_wreath_planar_consequences/sources/triangle/de_laat_vallentin_1311.3789v3.html',585680,'29fcd745bfe4e11a422e3da0ad84e0079c43b38d84d1cf23dd809967a612cb43'),
 (str(P/'papers/23203143/reviews/scope-sol/primaries/cdls-v1.txt'),None,'b236e90db3394e825f333680ae284f67b7fe2259fa1b11b4a377777a575c58ff'),
 (str(P/'papers/23203143/reviews/scope-sol/primaries/dlv-v3.txt'),None,'0b18c5564e4f60160915a456155022fccc116182b44a4b83e21f11d269e0c1fb')]:
    q=pin(Path(path))
    if q['SHA256']!=digest or (expected_bytes is not None and q['bytes']!=expected_bytes):raise RuntimeError('primary reference drift '+path)
    external.append(q)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
create('CLOSING_GUARDS.json',dict(UTC=now,status='PASS_DATA_CUSTODY_ONLY',source_regular_files=len(sf),source_child_directories=len(sd),
    whole_source_bytes_modes_topology_unchanged=True,INITIAL23files1dir_unchanged=True,
    source_final=pin(S/'SOURCE_FINAL.json',S),source_manifest=pin(S/'SOURCE_MANIFEST.json',S),
    control_TeX=pin(S/'published-source/container-001/tree/publication/preprint.tex',S),native_PDF=pin(S/'assets/preprint.pdf',S),
    external_primary_reference_pins=external,no_live_cached_byte_equivalence_claim=True,
    own_data_utility_body_read_before_execution=True,mathematical_native_or_old_helper_executions=0,
    empty_source_tool_streams=[pin(R/n,R) for n in ('SOURCE_AUTH.stderr.txt','PDFINFO.stderr.txt','PDFTEXT.stderr.txt','RASTER.stdout.txt','RASTER.stderr.txt')]))
files,dirs=inv(R)
create('MANIFEST.json',dict(schema='focused-interface-whole-owned-manifest-v1',UTC=now,payload_files=files,directories=dirs,
    root_mode=oct(stat.S_IMODE(R.lstat().st_mode)),exact_excluded_terminal_controls=['MANIFEST.json','FINAL.json'],includes_all_ignored_empty_files_bytes_modes=True))
create('FINAL.json',dict(schema='focused-functional-analysis-interface-final-v1',UTC=now,record='23203143',row=164,
    status='FROZEN_PASS_FOCUSED_INTERFACES_ONLY',
    exact_disposition='CONTINUOUS_TO_SCHWARTZ_CLOSED_SIGN_SET_VALUE_COMPARISON_COMPACT_THETA_PRIME_DUALITY_AND_NATIVE_PRODUCT_COMPARISON_VERIFIED',
    focused_mathematical_gap_found=None,source_repair_or_narrowed_promotion=False,full_paper_certification=False,
    group_construction_or_imported_planar_certificate_newly_certified=False,
    report=pin(R/'REPORT.md',R),manifest=pin(R/'MANIFEST.json',R),primary_readset=pin(R/'PRIMARY_READSET.json',R),
    initial_seal=pin(R/'INITIAL_SEAL.json',R),initial_hand_checks=pin(R/'INITIAL_HAND_CHECKS.md',R),closing_guards=pin(R/'CLOSING_GUARDS.json',R),
    source_final=pin(S/'SOURCE_FINAL.json',S),source121files20dirs_and_INITIAL23files1dir_unchanged=True,
    full_actual212line_TeX_all8PDFtext_pages_and8fresh_pixels_read=True,
    prior164scope_exposure_disclosed_not_blank_slate=True,current_root_peer_or_old_scientific_reports_opened=False,
    exact_primary_editions='CDLS2206.15373v1 and corrected DLV1311.3789v3 selected actual interfaces',
    native_or_validated_mathematical_executions=0,software_install_or_campaign=False,
    literal_limits=['Selected primary interfaces, not both entire foreign papers',
        'One locator display truncated; relied-on proof spans reread untruncated',
        'Cached raw identity pinned; no live byte-equivalence claim',
        'Primaryv1 literal product-proof bookkeeping distinguished from unchanged native expanded proof',
        'No whole-paper, novelty, optimizer-attainment or formal-verification certificate'],
    follow_up=None,completion_percent_focused_task=100,publication_W_Git_Sheet_deploy_or_source_mutation_authority=False,
    external_primary_reference_pins=external,all_writes_confined_to_owned_folder=True,
    extent=dict(regular_files=len(files)+2,child_directories=len(dirs),payload_regular_files=len(files),all_paths=sorted([q['path'] for q in files]+['MANIFEST.json','FINAL.json']),directories=dirs),
    quiescent_after_seal=True,self_hash_excluded=True))
af,ad=inv(R)
if len(af)!=len(files)+2 or ad!=dirs:raise RuntimeError('finite extent mismatch')
for q in files:
    if pin(R/q['path'],R)!=q:raise RuntimeError('payload drift during seal')
print(json.dumps(dict(FINAL=pin(R/'FINAL.json',R),MANIFEST=pin(R/'MANIFEST.json',R),regular_files=len(af),child_directories=len(ad)),indent=2))
