#!/usr/bin/env python3
"""Independent byte and source-receipt inspection, without candidate execution."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, stat, subprocess, zipfile

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
ASSEMBLY=AUDIT.parents[1]/'work/pr822_revision_r2'

def need(ok,label):
    if not ok:raise RuntimeError(label)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def load(p):return json.loads(p.read_bytes())

def row(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}

def main():
    seal=load(AUDIT/'PACKAGE_SEAL_R2.json')
    for r in seal['core_files']:
        p=AUDIT/'preprint'/r['path']
        need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'core seal '+r['path'])
    mapping=load(AUDIT/'PREPARED_PR_MAPPING_R2.json')
    actual={str(p.relative_to(ASSEMBLY)) for p in ASSEMBLY.rglob('*') if p.is_file()}
    mapped=set()
    for r in mapping['files']:
        p=Path(r['local_path']);mapped.add(str(p.relative_to(ASSEMBLY)))
        need(p.stat().st_size==r.get('bytes',p.stat().st_size) and sha(p)==r['sha256'],'prepared mapping '+str(p))
    need(mapped==actual and len(actual)==163,'closed assembly 163')
    source=load(AUDIT/'SOURCE_MANIFEST.json')
    need(source['original_head']=='c9fd5a0462d1fa98f21aa7037f7a5e061fbbee9c' and source['original_exact_queue_status']=='claimed_solved' and '| 1/5 |' in source['head_queue_row'],'original status/head/effort')
    frozen=ASSEMBLY/'publication_20261013/verification_package/source'
    need(len(source['files'])==42,'original count')
    for r in source['files']:
        p=frozen/r['path']
        need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'frozen identity '+r['path'])
        need((AUDIT/'source'/r['path']).read_bytes()==p.read_bytes(),'audit frozen identity')
    archives=[]
    for p in sorted((frozen/'archives').glob('*.zip')):
        if 'AUTHOR' in p.name:folder='author'
        elif 'INDEPENDENT' in p.name:folder='audit'
        else:folder='second_review'
        with zipfile.ZipFile(p) as z:
            infos=z.infolist();names=[i.filename for i in infos]
            expected={str(q.relative_to(frozen/folder)) for q in (frozen/folder).rglob('*') if q.is_file()}
            need(len(names)==len(set(names)) and set(names)==expected,'frozen archive inventory')
            for i in infos:
                n=PurePosixPath(i.filename)
                need(str(n)==i.filename and not n.is_absolute() and '..' not in n.parts and stat.S_ISREG(i.external_attr>>16) and not i.is_dir() and not i.flag_bits&1,'frozen archive member safety')
                need(z.read(i)==(frozen/folder/i.filename).read_bytes(),'frozen archive member bytes')
            need(z.testzip() is None,'frozen archive CRC')
            archives.append({**row(p),'members':len(names),'member_names':names,'all_safe_and_identical':True})
    need(len(archives)==3 and sum(x['members'] for x in archives)==32,'frozen archive 3/32 count')
    pre=ASSEMBLY/'publication_20261013/preprint';pack=pre.parent/'verification_package'
    index=load(pack/'package_index.json');names=[x['path'] for x in index['files']]
    need(len(names)==109 and len(set(names))==109,'portable indexed payload 109')
    with zipfile.ZipFile(pre/'verification.zip') as z:
        need(len(z.infolist())==110,'portable archive count')
        for i in z.infolist():
            n=PurePosixPath(i.filename)
            need(str(n)==i.filename and not n.is_absolute() and '..' not in n.parts and stat.S_ISREG(i.external_attr>>16),'portable ZIP safety')
            need(z.read(i)==(pack/i.filename).read_bytes(),'portable/extracted identity')
        need(z.testzip() is None,'portable CRC')
    need(set(names)|{'package_index.json'}=={str(p.relative_to(pack)) for p in pack.rglob('*') if p.is_file()},'portable closed inventory')
    need(not any('private_sources' in PurePosixPath(n).parts or n.endswith('.html') for n in names),'raw primaries excluded')
    pdfs=[n for n in names if n.endswith('.pdf')];need(pdfs==['note.pdf'],'only authored note PDF in portable inventory')
    metadata=load(pre/'metadata.json'); outermeta=load(ASSEMBLY/'PUBLICATION_METADATA.json')
    need(metadata==load(pack/'metadata.json')==load(pre/'zenodo-deposit.json')['metadata']==outermeta['zenodo_metadata'],'all publication metadata identical')
    need(metadata['creators'][0]['orcid']=='0009-0001-9320-500X' and metadata['license']=='cc-by-4.0' and metadata['publication_type']=='preprint','author/license/preprint')
    need((pre/'note.tex').read_bytes()==(pack/'note.tex').read_bytes()==(AUDIT/'preprint/note.tex').read_bytes(),'current source identity')
    need((pre/'output/pdf/note.pdf').read_bytes()==(pack/'note.pdf').read_bytes()==(AUDIT/'preprint/output/pdf/note.pdf').read_bytes(),'current PDF identity')
    priority=AUDIT/'priority_audit_01';corpus=load(priority/'CORPUS_MANIFEST.json')
    for r in corpus['files']:
        p=priority/r['relative_private_path']
        need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'retained corpus hash '+str(p))
    pdfrows=[r for r in corpus['files'] if r.get('kind')=='PDF']
    need(len(pdfrows)==26 and len({r['sha256'] for r in pdfrows})==25,'retained PDF counts')
    search=load(priority/'SEARCH_LEDGER.json')
    def count_queries(o):
        if isinstance(o,dict):return sum(len(v) if k=='queries' and isinstance(v,list) else count_queries(v) for k,v in o.items())
        if isinstance(o,list):return sum(count_queries(x) for x in o)
        return 0
    query_count=count_queries(search)
    need(query_count==107,'overlapping query record count')
    sources=[('private_sources/OWR_2009_06.pdf','Printed 421–422, item (16), Conjectures 1 and 2; inspected two actual page images and extracted text. Exact weight power, round L2, positive potential and universal dimensions agree.'),
      ('private_sources/OWR_2009_06.txt','Text lines 3298–3357; original source statement and adjacent context.'),
      ('private_sources/Ammann_Jammes_author_20081208.pdf','Author manuscript dated 2008-12-08; printed pp. 1–2,7–10; section 3.2 and Theorem 4.1. Construction is material, fixed-index theorem alone is insufficient.'),
      ('private_sources/Ammann_Jammes_author_20081208.txt','Inspected lines 1–134,410–472,530–555: Pinocchio attribution, inverse-radius nose, smooth cap condition, fixed-index theorem.'),
      ('private_sources/AJ_Crossref_metadata.json','Chapter title, 2011 date, pages 1–23 and DOI agree; no assertion that final chapter is byte-identical to author manuscript.'),
      ('priority_audit_01/private_sources/historical/morpurgo_2002_inspected_web_sections.txt','Partial online author-text capture, not final Duke full text. Definition (16), Theorem 4.1, Corollary 4.2, Theorem 5.10. Convex continuous transform and integrability conditions do not allow a delta heat-time mass or nonlinear maximum transfer.'),
      ('priority_audit_01/private_sources/broader/sire_xu_arxiv_v3.txt','Theorem 1.1, printed pp. 1–2: different first-power weight normalization, not this volume-normalized maximum.'),
      ('priority_audit_01/private_sources/broader/humbert_petrides_premoselli_arxiv_v2.txt','Theorems 1.6–1.8, printed pp. 8–9. Fixed-index extrema, and n>=2s+5 for nonround sphere attainment; no dimension-three heat maximum conclusion.')]
    source_receipts=[{**row(AUDIT/p),'inspection':note} for p,note in sources]
    out={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'seal_core_files_verified':len(seal['core_files']),'mapped_assembly_files':len(mapped),'original_files':42,
      'archives':archives,'portable_files':110,'portable_index_sha256':sha(pack/'package_index.json'),'portable_zip_sha256':sha(pre/'verification.zip'),
      'pdf_sha256':sha(pre/'output/pdf/note.pdf'),'outer_manifest_sha256':sha(ASSEMBLY/'PUBLICATION_MANIFEST.json'),
      'downloaded_raw_primary_material_in_portable_package':False,'metadata_identity':True,
      'priority_corpus_verified_files':len(corpus['files']),'priority_pdf_copies':26,'priority_distinct_pdf_versions':25,'overlapping_search_records':query_count,
      'priority_claim':'bounded non-detection only; no historical priority/worldwide firstness/current openness certification',
      'source_inspection_receipts':source_receipts,'new_external_retrieval_or_communication':False}
    (HERE/'BINDINGS_AND_SOURCE_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('archives','source_inspection_receipts')},indent=2))

if __name__=='__main__':main()
