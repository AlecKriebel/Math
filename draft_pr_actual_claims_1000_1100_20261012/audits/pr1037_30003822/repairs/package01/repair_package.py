#!/usr/bin/env python3
"""Local P3 release-prose repair and provenance; no network or Git operations.

Run with python3 -B. Phases are intentionally separate from saved-source compile,
disk export and visual inspection. The final phase seals actual exported bytes.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import argparse, hashlib, io, json, shutil, stat, zipfile

ROOT = Path(__file__).resolve().parents[2]
PRE = ROOT / 'preprint'
OWN = Path(__file__).resolve().parent
SKIP = {'raw','private','rawprivate','render','extracted','extractedcache',
        'tmp','cache','__pycache__','.venv'}

def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': sha(b)}
def write(p, v):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(v, indent=2, ensure_ascii=False)+'\n')
def authored(p, parent):
    rel = p.relative_to(parent)
    return (p.is_file() and not p.is_symlink() and not any(s in SKIP for s in rel.parts)
            and p.suffix not in {'.pyc','.aux','.out','.log','.pdf','.png','.jpg','.html','.txt'})
def durable_candidate():
    return sorted(p for p in PRE.rglob('*') if p.is_file() and not p.is_symlink()
                  and not any(s in SKIP for s in p.relative_to(PRE).parts)
                  and p.suffix not in {'.pyc','.aux','.out','.log'})
def replace_once(path, old, new):
    s = path.read_text(); assert s.count(old) == 1, (path, s.count(old))
    path.write_text(s.replace(old, new))
def copy_exact(src, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    assert src.read_bytes() == dest.read_bytes()
    return {'source_path': src.relative_to(ROOT).as_posix(),
            'package_path': dest.relative_to(PRE).as_posix(), **pin(dest),
            'byte_equal': True}
def log(msg, percent):
    with (OWN/'REPAIR_LOG.md').open('a') as f:
        f.write(f'\n{utc()} — {msg} Completion estimate for assigned P3 repair: {percent}%.\n')

def baseline():
    assert not (OWN/'BASELINE_PIN.json').exists()
    candidates = durable_candidate()
    fixed = list((ROOT/'submitted').rglob('*'))
    for family in ('invariant_01','transfer_01','priority_01','package_01'):
        base = ROOT/'reviews'/family
        fixed += [p for p in base.rglob('*') if authored(p, base)]
    # Include the two authored symbolic-result .txt files already in the index;
    # do not include any full third-party text extraction.
    index=json.loads((PRE/'EVIDENCE_INDEX.json').read_text())
    fixed += [ROOT/rec['source_path'] for rec in index['entries']]
    fixed += [p for p in ROOT.iterdir() if p.is_file() and
              (p.name.startswith('ROOT_') or p.name in {'SUBMITTED_PINS.json','LIVE_PR_CAPTURE.json'})]
    fixed = sorted(set(p for p in fixed if p.is_file()))
    write(OWN/'BASELINE_PIN.json', {'utc': utc(), 'scope': 'Immediate current durable preprint, all ten original files, and frozen authored whole/family/root stages; renders and raw/private bodies excluded.',
          'candidate': [{'path': p.relative_to(ROOT).as_posix(), **pin(p)} for p in candidates],
          'immutable': [{'path': p.relative_to(ROOT).as_posix(), **pin(p)} for p in fixed]})
    for p in candidates:
        dest = OWN/'frozen_input'/p.relative_to(PRE)
        dest.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, dest)
        assert p.read_bytes() == dest.read_bytes()
    (OWN/'.gitignore').write_text('raw/\nrender/\nfrozen_input/\n__pycache__/\n')
    (OWN/'REPAIR_LOG.md').write_text('# P3 release wording repair — package01\n\nExact assignment: P3_RELEASE_WORDING_01 only; preserve mathematical prose, originals and historical stage records; build and inspect the complete new candidate for NEW whole review 02.\n')
    log('Pinned current inputs and all original/frozen authored stages before candidate mutation. Saved byte-exact old current candidate files, including the old ZIP, outside the new package.', 15)

def edit():
    assert (OWN/'BASELINE_PIN.json').exists()
    copies=[]
    for name in ('BUILD_RECEIPT.json','CURRENT_REVIEW_STATE.json','MANIFEST.json','ARCHIVE_PIN.json','EVIDENCE_INDEX.json'):
        copies.append(copy_exact(PRE/name, PRE/'history/preparation_20261013_01'/name))
    tex = PRE/'paper/forest_transfer_catalan.tex'
    old = 'Version 1.0 is an unrefereed exposition; the current whole-paper and whole-package review is pending and no publication approval is recorded here. No new external contact, submission, DOI registration or publication is performed by this preparation.'
    new = 'Version 1.0 is an unrefereed exposition. The supportkit records dated preparation checks and stage-specific AI reviews, each identified by its scope and frozen input identities in \\url{REVIEW_HISTORY.json} and \\url{EVIDENCE_INDEX.json}; those records are not human refereeing or submission or publication records.'
    replace_once(tex, old, new)
    replace_once(PRE/'README.md', '- `CURRENT_REVIEW_STATE.json` records pending NEW whole-paper/whole-package review; family PASS records are stage-specific evidence.', '- `REVIEW_HISTORY.json` identifies dated preparation and AI review stages and frozen inputs; `CURRENT_REVIEW_STATE.json` records the operational state of the corresponding candidate. Family PASS records concern their own stages.')
    replace_once(PRE/'README.md', '- `zenodo_metadata.json` is a local request-wrapper draft; `.zenodo.json` is its unwrapped form. No deposit or DOI for this package has been created.', '- `zenodo_metadata.json` preserves the exact `{metadata: ...}` request wrapper; `.zenodo.json` contains the same metadata object. External `zenodo-deposit.json` lists the paper PDF and supportkit; it is excluded from the ZIP to avoid an archive self-reference.')
    replace_once(PRE/'README.md', 'Current preparation status: concrete manuscript and supportkit prepared for fresh review. Publication/submission approval remains pending. No service, Git/index, PR, release or external individual was changed or contacted by this preparation.', 'Version 1.0 is an unrefereed exposition. The supportkit records dated preparation checks and stage-specific AI reviews, each identified by its scope and frozen inputs in `REVIEW_HISTORY.json` and `EVIDENCE_INDEX.json`. Those records do not constitute human refereeing, journal acceptance, formal certification or submission/publication records.')
    replace_once(PRE/'SUPPLEMENT.md', 'NEW whole-paper/package review is pending.', 'The dated preparation checks and stage-specific AI reviews are identified by their scope and frozen inputs in `REVIEW_HISTORY.json` and `EVIDENCE_INDEX.json`; they are not human refereeing, journal acceptance, formal certification or submission/publication records.')
    obj=json.loads((PRE/'zenodo_metadata.json').read_text())
    prior='Current whole-paper/whole-package review is pending; this metadata is a local draft and is not a submission or publication record.'
    assert obj['metadata']['description'].count(prior)==1
    obj['metadata']['description']=obj['metadata']['description'].replace(prior, 'The supportkit records dated preparation checks and stage-specific AI reviews, each identified by scope and frozen inputs in REVIEW_HISTORY.json and EVIDENCE_INDEX.json. Those records are not human refereeing, journal acceptance, formal certification or submission/publication records.')
    write(PRE/'zenodo_metadata.json', obj);write(PRE/'.zenodo.json', obj['metadata'])
    write(PRE/'zenodo-deposit.json', {'metadata': obj['metadata'], 'files': [{'path':'paper/forest_transfer_catalan.pdf'}, {'path':'pr1037_supportkit_v1.0.zip'}]})
    (PRE/'METADATA_NOTES.md').write_text('# Metadata forms and external file manifest\n\n`zenodo_metadata.json` uses the exact request wrapper `{"metadata": {...}}`; `.zenodo.json` is the corresponding unwrapped metadata object. External `zenodo-deposit.json` contains exactly that same metadata object and a `files` list with `paper/forest_transfer_catalan.pdf` and `pr1037_supportkit_v1.0.zip`, relative to its location. It is excluded from the ZIP to avoid an archive self-reference. These local metadata/configuration files are not deposit, assigned-DOI, release or submission/publication records.\n\nAll three metadata objects carry the same neutral title, theorem limits, exact-match Ferudun credit, qualified chronology, sole author/ORCID, CC BY 4.0 and extensive AI/unrefereed disclosure. The publication date and version describe this authored exposition, not a claimed first discovery date. Source authors are credited sources, not coauthors. REVIEW_HISTORY.json distinguishes dated preparation and AI reviews by scope and frozen inputs; those records are not human refereeing, journal acceptance, formal certification or submission/publication records. CURRENT_REVIEW_STATE.json records the corresponding candidate operational state.\n')
    state=json.loads((PRE/'CURRENT_REVIEW_STATE.json').read_text())
    state.update({'utc':utc(), 'new_paper_and_package_review':'PENDING_NEW_WHOLE_02',
                  'publication_ready':False, 'all_issues_resolved':False,
                  'whole_review_01':{'record':'evidence/whole_20261013/package_01/VERDICT.json',
                    'status':'REQUIRES_ONE_P3_RELEASE_WORDING_REPAIR','issue':'P3_RELEASE_WORDING_01'},
                  'repair_01':'P3 prose repair and candidate rebuild; no terminal review clearance'})
    write(PRE/'CURRENT_REVIEW_STATE.json',state)
    src=ROOT/'reviews/package_01'
    new_entries=[]
    for p in sorted(src.rglob('*')):
        if authored(p,src):
            c=copy_exact(p, PRE/'evidence/whole_20261013/package_01'/p.relative_to(src))
            copies.append(c)
            new_entries.append({k:v for k,v in c.items() if k!='byte_equal'} | {'stage':'whole current candidate AI review 01; frozen pre-repair inputs, one P3 issue; not approval of changed candidate'})
    c=copy_exact(ROOT/'ROOT_PREPRINT_REVIEW_01.json',PRE/'evidence/root/ROOT_PREPRINT_REVIEW_01.json')
    copies.append(c);new_entries.append({k:v for k,v in c.items() if k!='byte_equal'} | {'stage':'root whole source/PDF review 01 on frozen pre-repair bytes; not terminal clearance'})
    idx=json.loads((PRE/'EVIDENCE_INDEX.json').read_text())
    idx['utc']=utc();idx['entries']+=new_entries
    idx['entries'].sort(key=lambda x:x['package_path'])
    idx['stage_navigation']='REVIEW_HISTORY.json maps original, preparation, family, whole-review01 and repair stages; historical pins apply only to their explicitly frozen inputs, never automatically to changed current bytes.'
    write(PRE/'EVIDENCE_INDEX.json',idx)
    write(OWN/'BYTE_COPY_RECEIPTS.json',{'utc':utc(),'copies':copies, 'all_bytes_equal':True})
    for p in (PRE/'history/preparation_20261013_01').iterdir():
        assert p.read_bytes()==(OWN/'frozen_input'/p.name).read_bytes()
    builder=PRE/'build_supportkit.py'
    replace_once(builder,"GENERATED={'MANIFEST.json','ARCHIVE_PIN.json',ARCHIVE.name}","GENERATED={'MANIFEST.json','ARCHIVE_PIN.json',ARCHIVE.name,'zenodo-deposit.json'}")
    replace_once(builder,"'review_state':'PENDING_NEW_WHOLE_01; no publication approval'","'review_state':'PENDING_NEW_WHOLE_02; publication_ready=false; all_issues_resolved=false; no publication approval'")
    replace_once(builder,'ARCHIVE_PIN.json externally pins manifest and archive and is excluded from the ZIP. ZIPs, raw/private/render/extracted caches, environments and compiler intermediates are excluded.', 'ARCHIVE_PIN.json externally pins manifest and archive and is excluded from the ZIP. zenodo-deposit.json externally lists the PDF and ZIP with identical metadata and is excluded to avoid an archive self-reference. ZIPs, raw/private/render/extracted caches, environments and compiler intermediates are excluded.')
    oldpins=json.loads((OWN/'BASELINE_PIN.json').read_text())
    oldkey={x['path'].removeprefix('preprint/'): {k:x[k] for k in ('bytes','sha256')} for x in oldpins['candidate'] if x['path'] in {'preprint/paper/forest_transfer_catalan.tex','preprint/paper/forest_transfer_catalan.pdf','preprint/pr1037_supportkit_v1.0.zip'}}
    history={'utc':utc(), 'interpretation':'Dated AI/preparation records retain their exact historical wording and verdicts. Each is evidence only for its stated frozen stage. No human refereeing, journal acceptance, formal certification or publication record is inferred.',
       'stages':[
         {'stage':'original_20261009','head':'e87236a97c4b87818d2768cd5789043c7c3f4e39','identities':'HISTORICAL_PIN_MAP.json','records':'evidence/original_20261009','immutable':True},
         {'stage':'fresh_family_20261013','records':'evidence/fresh_20261013','scope':'Separate invariant, transfer and priority interfaces, each with its own frozen INPUT/OUTPUT pins; not whole-paper approval.'},
         {'stage':'preparation_20261013_01','records':['PREPARATION_LOG.md','PREPARATION_REPORT.md'], 'frozen_identity_records':'history/preparation_20261013_01','candidate_key_pins':oldkey,'scope':'Original authored paper/supportkit preparation and layout checks. Historical present-tense pending labels describe this stage only.'},
         {'stage':'root_review_20261013_01','records':'evidence/root/ROOT_PREPRINT_REVIEW_01.json','candidate_key_pins':oldkey,'scope':'Full original current TeX and 12-page visual review; no terminal clearance.'},
         {'stage':'whole_review_20261013_01','records':'evidence/whole_20261013/package_01','input_pin':'evidence/whole_20261013/package_01/INPUT_PIN.json','final_input_pin':'evidence/whole_20261013/package_01/FINAL_INPUT_PIN.json','output_pin':'evidence/whole_20261013/package_01/OUTPUT_PIN.json','candidate_key_pins':oldkey,'verdict':'REQUIRES_ONE_P3_RELEASE_WORDING_REPAIR','issue':'P3_RELEASE_WORDING_01','scope':'Complete frozen paper and package review; mathematics/source/render/archive passed, one durable release wording repair remained.'},
         {'stage':'repair_20261013_package01','records':'REPAIR_STAGE_20261013.md','scope':'Only P3 release prose plus rebuilt PDF, dated provenance navigation, authored whole-review01 copies, metadata equality, external file manifest and package pins. Current BUILD_RECEIPT pins the new source/PDF; current MANIFEST and external ARCHIVE_PIN pin the new complete package. Changed bytes require NEW whole review02.'}
       ],
       'current_operational_state':'CURRENT_REVIEW_STATE.json',
       'next_review':'PENDING_NEW_WHOLE_02; publication_ready=false; all_issues_resolved=false',
       'external_sidecars':['ARCHIVE_PIN.json','zenodo-deposit.json'],
       'prior_current_bytes':'Frozen old ZIP and changed input byte copies retained outside package under repairs/package01/frozen_input; old build/state/manifest/archive/index copies inside history/preparation_20261013_01 are byte exact.'}
    write(PRE/'REVIEW_HISTORY.json',history)
    (PRE/'REPAIR_STAGE_20261013.md').write_text('# Dated P3 release wording repair stage\n\n'+utc()+' — P3_RELEASE_WORDING_01 replaced present-tense pending/draft release prose in the paper, README, supplement and both equal metadata descriptions with stable dated AI-review history and frozen-input navigation. Extensive AI assistance, unrefereed status, no human/journal/formal certification, exact same-theorem Ferudun credit and qualified chronology, inherited credits, priority unknowns and every mathematical paragraph remain intact.\n\nThe original ten-file edition, old preparation log/report, original/family/root review records and whole-review01 source bytes remain unchanged. Whole-review01 authored outputs and pins are copied byte-for-byte under evidence/whole_20261013/package_01; raw/private/extracted/render/tmp/cache/full third-party bodies are excluded. Its one-P3 verdict remains historical and does not approve changed bytes. Historical current build/state/manifest/archive/index copies are preserved under history/preparation_20261013_01. REVIEW_HISTORY.json distinguishes those stages explicitly.\n\nBUILD_RECEIPT.json records the new saved-source compile, disk PDF export and all-page visual check. EVIDENCE_INDEX.json records authored source-copy pins. The current manifest and external ARCHIVE_PIN.json describe the current ZIP. External zenodo-deposit.json contains exactly the current metadata object and the two upload file paths, and is excluded from the ZIP to avoid an archive self-reference. These local files are no evidence of an external submission, deposit, DOI, release or publication.\n\nAssigned repair completion is recorded in repairs/package01/REPAIR_LOG.md outside this supportkit. CURRENT_REVIEW_STATE.json remains PENDING_NEW_WHOLE_02 with publication_ready=false and all_issues_resolved=false until a new full artifact review. This repair is not an independent mathematical review or terminal clearance.\n')
    log('Repaired the six current durable prose surfaces; preserved exact old receipt/state/manifest/index pins; copied 27 authored whole-review01 outputs and root01 receipt; added dated stage navigation and external repository-tool file manifest.',55)

def seal():
    before=json.loads((OWN/'BASELINE_PIN.json').read_text())
    for rec in before['immutable']:
        assert pin(ROOT/rec['path'])=={k:rec[k] for k in ('bytes','sha256')},rec['path']
    old=(OWN/'frozen_input/paper/forest_transfer_catalan.tex').read_text()
    new=(PRE/'paper/forest_transfer_catalan.tex').read_text()
    old_start=old.index('Version 1.0 is an unrefereed exposition;')
    old_end=old.index('\n',old_start)
    new_start=new.index('Version 1.0 is an unrefereed exposition.')
    new_end=new.index('\n',new_start)
    assert old[:old_start]==new[:new_start] and old[old_end:]==new[new_end:]
    oldwrap=json.loads((OWN/'frozen_input/zenodo_metadata.json').read_text())
    wrap=json.loads((PRE/'zenodo_metadata.json').read_text())
    assert set(wrap)=={'metadata'}
    assert json.loads((PRE/'.zenodo.json').read_text())==wrap['metadata']
    dep=json.loads((PRE/'zenodo-deposit.json').read_text())
    assert set(dep)=={'metadata','files'} and dep['metadata']==wrap['metadata']
    assert dep['files']==[{'path':'paper/forest_transfer_catalan.pdf'},{'path':'pr1037_supportkit_v1.0.zip'}]
    ow=oldwrap['metadata'].copy(); nw=wrap['metadata'].copy();ow.pop('description');nw.pop('description');assert ow==nw
    idx=json.loads((PRE/'EVIDENCE_INDEX.json').read_text())
    for rec in idx['entries']:
        pp=PRE/rec['package_path'];src=ROOT/rec['source_path']
        assert pp.read_bytes()==src.read_bytes()
        assert pin(pp)=={k:rec[k] for k in ('bytes','sha256')}
    payload=json.loads((PRE/'MANIFEST.json').read_text())
    manifestpins={rec['path']:rec for rec in payload['files']}
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
        for name in sorted(list(manifestpins)+['MANIFEST.json']):
            info=zipfile.ZipInfo(name,(2026,10,13,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,(PRE/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    archive=PRE/'pr1037_supportkit_v1.0.zip';assert buf.getvalue()==archive.read_bytes()
    scan=[]
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();assert names==sorted(names) and len(names)==len(set(names)) and z.testzip() is None
        assert {'ARCHIVE_PIN.json','zenodo-deposit.json'}.isdisjoint(names)
        for info in z.infolist():
            name=info.filename;parts=PurePosixPath(name).parts
            assert name.isascii() and not name.startswith('/') and '..' not in parts and '\\' not in name
            assert info.create_system==3 and stat.S_ISREG(info.external_attr>>16) and (info.external_attr>>16)&0o777==0o644
            assert info.date_time==(2026,10,13,0,0,0)
            assert not any(x in SKIP for x in parts) and Path(name).suffix not in {'.zip','.pyc','.png','.jpg','.html'}
            data=z.read(name);assert data==(PRE/name).read_bytes()
            if name!='MANIFEST.json':assert {'bytes':len(data),'sha256':sha(data)}=={k:manifestpins[name][k] for k in ('bytes','sha256')}
            if Path(name).suffix=='.pdf':assert name=='paper/forest_transfer_catalan.pdf' and data.startswith(b'%PDF-')
            else:data.decode('utf-8')
            scan.append({'path':name,'bytes':len(data),'sha256':sha(data),'crc32':f'{info.CRC:08x}','kind':'authored PDF' if name.endswith('.pdf') else 'UTF-8 authored or stage provenance record'})
    state=json.loads((PRE/'CURRENT_REVIEW_STATE.json').read_text());assert state['new_paper_and_package_review']=='PENDING_NEW_WHOLE_02' and not state['publication_ready'] and not state['all_issues_resolved']
    bp={r['path']:r for r in before['candidate']};ap={p.relative_to(ROOT).as_posix():pin(p) for p in durable_candidate()}
    changes=[]
    for name in sorted(set(bp)|set(ap)):
        prior={k:bp[name][k] for k in ('bytes','sha256')} if name in bp else None
        after=ap.get(name)
        if prior!=after:changes.append({'path':name,'before':prior,'after':after})
    write(OWN/'CHANGED_PATHS_AND_HASHES.json',{'utc':utc(),'files':changes,'unchanged_immutable_files':len(before['immutable']),'paper_exact_change':'Only final two sentences of Section7 replaced; every other byte of the TeX is identical.'})
    write(OWN/'INTEGRITY_RESULTS.json',{'utc':utc(),'all_immutable_input_pins_unchanged':True,'original_file_count':10,'all_original_and_authored_source_copies_equal':True,'evidence_index_entries':len(idx['entries']),'metadata_three_objects_exact_equal':True,'metadata_non_description_fields_unchanged':True,'tex_every_byte_outside_exact_release_sentence_change_unchanged':True,'zip_independent_reassembly_identical':True,'zip_all_payloads_roundtrip_and_manifest_valid':True,'zip_crc_safe_names_regular_0644_fixed_time':True,'external_sidecars_excluded':True,'actual_payload_members':scan,'current_review_state':'PENDING_NEW_WHOLE_02','publication_ready':False,'all_issues_resolved':False})
    write(OWN/'NEW_CANDIDATE_PIN.json',{'utc':utc(),'scope':'Complete current durable candidate including external archive/file sidecars; frozen for NEW whole review02','files':[{'path':name,**data} for name,data in sorted(ap.items())],'key_pins':{name:ap['preprint/'+name] for name in ['paper/forest_transfer_catalan.tex','paper/forest_transfer_catalan.pdf','pr1037_supportkit_v1.0.zip','MANIFEST.json','ARCHIVE_PIN.json','zenodo-deposit.json']}})
    log('New source compiled/exported; all 12 pages individually viewed. Reverified every immutable original/frozen stage, all 104 authored source copies, metadata equality, exact restricted TeX change, actual ZIP bytes/manifest/CRC/safe regular-file paths and identical independent ZIP reassembly. Sealed current candidate for NEW whole review02; readiness flags remain false.',100)
    outputs=[p for p in sorted(OWN.iterdir()) if p.is_file() and p.name!='OUTPUT_PIN.json']
    write(OWN/'OUTPUT_PIN.json',{'utc':utc(),'files':[{'path':p.relative_to(ROOT).as_posix(),**pin(p)} for p in outputs],'pin_self_policy':'Output pin excluded from its own list; current candidate complete pins are in NEW_CANDIDATE_PIN.json.'})
    print(json.dumps({'key_pins':json.loads((OWN/'NEW_CANDIDATE_PIN.json').read_text())['key_pins'],'changed_paths':len(changes),'evidence_entries':len(idx['entries']),'zip_members':len(scan)},indent=2))

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('phase',choices=['baseline','edit','seal']);args=a.parse_args()
    globals()[args.phase]()
