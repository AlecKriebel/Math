"""Read-only pre-render editorial checks; writes only a fresh owned result file."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re,subprocess,sys,tarfile,io,zipfile,csv,base64
R=Path(__file__).resolve().parents[4];P=R/'papers/22089807';E=P/'reviews/editorial'
parser=argparse.ArgumentParser();parser.add_argument('--output-stem',required=True);args=parser.parse_args()
assert re.fullmatch(r'[a-zA-Z0-9_-]+',args.output_stem)
out=E/(args.output_stem+'.json');assert not out.exists(),'Refuse to replace evidence'
sys.path.insert(0,str(R/'scripts'))
from published_assets import PublishedAssets,asset_name,normalized_receipt_view
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
c=json.loads((P/'publication.json').read_text());g=json.loads((P/'promotion.json').read_text())
receipt=json.loads((P/'sources/receipt.json').read_text());record=json.loads((P/'sources/record.json').read_text());clear=json.loads((R/g['root_clearance_file']).read_text())
checks={};details={}
def test(k,v):checks[k]=bool(v)
frozen=json.loads((E/'frozen-before.json').read_text())['files'];changed=[]
for name,b in frozen.items():
    f=R/name
    if not f.is_file() or sha(f)!=b['sha256'] or f.stat().st_size!=b['bytes']:changed.append(name)
test('all_frozen_inputs_unchanged',not changed);details['frozen_inputs_checked']=len(frozen);details['changed']=changed
# Resolve only unchanged deposited files; tar is a deposited download, not a ZIP-embedded-public asset.
assets=PublishedAssets(P/'sources',normalized_receipt_view(receipt),c['source_binding']['embedded_assets'])
for item in receipt['files']:
    name=asset_name(item);data=assets.resolve(name).read_bytes()
    test('deposited_asset_'+name,hashlib.sha256(data).hexdigest()==item['sha256'] and len(data)==item['bytes'] and 'md5:'+hashlib.md5(data).hexdigest()==item['zenodo_checksum'])
test('only_original_two_assets',len(receipt['files'])==2 and {asset_name(x) for x in receipt['files']}=={c['pdf_filename'],c['supplement_filename']} and c['additional_assets']==[] and c['source_binding']['embedded_assets']==[])
test('source_file_objects_preserved',g['source_files']==receipt['files']==c['source_binding']['files'])
test('standard_record_path',c['source_binding']['metadata_path']==c['source_binding']['record_path']==g['metadata_path']=='sources/record.json')
test('record_identity',str(record['id'])=='22089807' and all(c[k]==record['metadata'][k] for k in ['title','doi','publication_date','version']))
test('raw_record_identity',c['source_binding']['raw_record_sha256']==sha(P/'sources/record-raw.json')==receipt['api_sha256'])
test('metadata_binding',sha(P/'sources/record.json')==g['metadata_sha256']==c['source_binding']['metadata_sha256'])
test('receipt_binding',sha(P/'sources/receipt.json')==g['source_receipt_sha256']==c['source_binding']['source_receipt_sha256']==clear['source_receipt_sha256'])
test('root_clearance_binding',sha(R/g['root_clearance_file'])==g['root_clearance_sha256']==c['review_metadata']['root_clearance_sha256']=='547296ed820667dfb47b36f796631c23f5eae67be7fb5c2ad898fb5d0bb72125' and g['root_clearance_record']==clear and g['approved_scope']==clear['approved_scope'] and g['status']==clear['status']=='PASS' and g['disposition_by']==clear['disposition_by']=='root')
test('root_custody_binding',g['root_custody_receipt']==clear['root_custody_receipt'] and sha(R/g['root_custody_receipt'])==g['root_custody_receipt_sha256']==clear['root_custody_receipt_sha256'])
test('publication_binding',sha(P/'publication.json')==g['publication_sha256'])
for k,v in g['reviews'].items():
    test('review_exact_'+k,sha(P/v['report'])==v['sha256']==clear['reviews'][k]['report_sha256'] and sha(P/v['verdict_file'])==v['verdict_sha256']==clear['reviews'][k]['verdict_sha256'] and json.loads((P/v['verdict_file']).read_text())==v['verdict'])
for i,s in enumerate(g['review_seals']):test('original_review_seal_'+str(i),sha(R/s['path'])==s['sha256'])
test('three_review_lanes',set(g['reviews'])=={'scope','analytic','adversarial'})
test('scope_hold_unchanged',g['reviews']['scope']['verdict']['promotion_authorized'] is False and g['reviews']['scope']['verdict']['mathematical_gate']=='not_decided_by_this_scope_verdict' and g['reviews']['scope']['root_disposition']=='SCOPE_COMPLETE' and bool(g['scope_gate_resolution']))
test('custom_scientific_verdicts_unchanged',g['reviews']['analytic']['verdict']['verdict']=='PASS_STATED_CLAIMS' and g['reviews']['adversarial']['verdict']['verdict']=='supported_as_stated_no_substantive_fault_found')
sb=c['source_binding'];tex=P/sb['source_tex_path'];raw=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex.read_text(),re.S).group(1)
# Independent explicit typography map, preserving both original paragraphs.
body=raw.replace('\n\\[\n',' ').replace('\n\\]\n',' ')
for a,b in [('Birth--death','Birth–death'),('death--Birth','death–Birth'),('pair--pendant','pair–pendant'),('R^6-8R^5+22R^4-30R^3+21R^2-6R+1.','R⁶ − 8R⁵ + 22R⁴ − 30R³ + 21R² − 6R + 1.'),(r'\Rsim','R_sim'),(r'\Rhyb','R_hyb'),(r'\geq',' ≥ '),(r'\ldots','…'),(r'\in',' ∈ '),(r'\sigma','σ'),(r'\lambda','λ'),('1<r<R_hyb','1 < r < R_hyb'),('R_sim ≥ R_hyb=','R_sim ≥ R_hyb = '),('…>3/2','… > 3/2'),('\\[',''),('\\]',''),('$','')]:body=body.replace(a,b)
body=body.replace('r ∈ (1,R)','r ∈ (1,R)')
normalized='\n\n'.join(' '.join(x.split()) for x in re.split(r'\n\s*\n',body.strip()))
test('full_exact_two_paragraph_abstract',normalized==c['abstract'] and len(c['abstract'].split())==sb['abstract_word_count']==214 and len(c['abstract'].split('\n\n'))==sb['abstract_paragraphs']==2)
test('abstract_tex_binding',sha(tex)==sb['source_tex_sha256']==sb['abstract_source_sha256'] and hashlib.sha256(raw.strip().encode()).hexdigest()==sb['abstract_tex_sha256'] and (E/'ABSTRACT.tex').read_text()==raw and (E/'ABSTRACT.txt').read_text().strip()==c['abstract'])
scope=json.loads((P/'reviews/scope/content.json').read_text())
test('frozen_scope_content',sha(P/'reviews/scope/content.json')==sb['frozen_scope_content_sha256'] and ' '.join(scope['abstract'].split())==' '.join(c['abstract'].split()) and scope['held_candidate'] is True and scope['publication_gate']==sb['frozen_scope_gate'])
# Direct text extraction of deposited reader; content only, no rendered-page/browser pass.
pdf=P/'sources'/c['pdf_filename'];pdftext=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
pages=pdftext.split('\f');pages=pages[:-1] if pages[-1].strip()=='' else pages
test('21_searchable_standalone_pages',len(pages)==c['pdf_pages']==21 and all(len(p.strip())>100 for p in pages))
# Match PDF abstract after only display spacing/ligatures/subscript/superscript normalization.
pdfabstract=pages[0].split('Abstract',1)[1].split('Keywords:',1)[0]
def lex(t):
    import unicodedata
    t=unicodedata.normalize('NFKC',t).replace('R_sim','Rsim').replace('R_hyb','Rhyb').replace('. . .','…')
    t=re.sub(r'(?<=\w)-\s*\n\s*(?=\w)','',t)
    return re.findall(r'[A-Za-z0-9]+|[σλ]',t)
test('standalone_abstract_complete',lex(pdfabstract)==lex(c['abstract']))
# Re-read every tar payload, enforce 23 safe unique regular members, and compare actual extraction.
archive=P/'sources'/c['supplement_filename'];allmembers=[];members={};archive_mismatches=[]
with tarfile.open(archive,'r:gz') as tf:
    for m in tf.getmembers():
        assert m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts
        assert m.name not in members
        data=tf.extractfile(m).read();members[m.name]=data;allmembers.append({'path':m.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        path=P/'sources/published-source'/m.name
        if not path.is_file() or path.read_bytes()!=data:archive_mismatches.append(m.name)
test('23_tar_members_byte_identical_extraction',len(members)==23 and not archive_mismatches)
embedded=[(k,v) for k,v in members.items() if k.endswith('.pdf')]
test('distinct_embedded_reader_retained',len(embedded)==1 and hashlib.sha256(embedded[0][1]).hexdigest()==sb['embedded_pdf_sha256']==g['embedded_pdf_sha256']==clear['embedded_pdf_sha256'] and embedded[0][1]!=pdf.read_bytes())
# Replay wheel CRC and RECORD identities only; do not execute/import submitted wheel modules.
wheel_counts=[];wheel_record_checks=0
for name,data in members.items():
    if not name.endswith('.whl'):continue
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None
        wheel_counts.append(len(z.infolist()))
        rec=next(n for n in z.namelist() if n.endswith('.dist-info/RECORD'))
        for row in csv.reader(io.StringIO(z.read(rec).decode())):
            path,digest,size=row
            if not digest:continue
            alg,value=digest.split('=',1);assert alg=='sha256'
            b=z.read(path);assert base64.urlsafe_b64encode(hashlib.sha256(b).digest()).rstrip(b'=').decode()==value
            assert len(b)==int(size);wheel_record_checks+=1
test('both_nested_wheels_bound',sorted(wheel_counts)==[92,1570] and sum(wheel_counts)==sb['nested_wheel_member_count']==1662 and wheel_record_checks==1660)
details['archive_members']=allmembers;details['nested_wheel_counts']=wheel_counts;details['nested_record_checks']=wheel_record_checks
for field in ['pdf_sha256','supplement_sha256']:
    test(field,g[field]==clear[field]==sb[field])
test('date_version_not_backdated',c['publication_date']==c['reviewed_publication_date']=='2026-08-25' and c['original_publication_date']=='2026-08-08' and c['version']=='2.0.4' and sb['original_named_release']['record_id']==21852072 and sb['original_named_release']['same_work_version_not_additional_completion'] is True and 'earlier date is not the publication date of version 2.0.4' in c['edition_note'])
base='https://aleckriebel.com/research/'+c['slug']+'/'
test('canonical_is_proposed_slug_url',c['canonical_url']==base and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',c['slug']) is not None)
seo=json.loads((E/'PROPOSED_SEO.json').read_text());test('proposed_seo_identity',seo['canonical']==base and seo['citation_pdf_url']==base+c['pdf_filename'] and seo['citation_publication_date']=='2026/08/25' and seo['ScholarlyArticle']['abstract']==c['abstract'] and seo['ScholarlyArticle']['datePublished']==c['publication_date'] and seo['ScholarlyArticle']['version']==c['version'])
test('tar_gz_correctly_labelled',c['supplement_filename'].endswith('.tar.gz') and 'tar.gz' in c['supplement_label'] and 'ZIP' not in c['supplement_label'])
public=(E/'PUBLIC_COPY.md').read_text()
test('full_proposed_public_paragraphs',all(v in public for k in ['abstract','plain_language','result','why_it_works','limitations','ai_disclosure','edition_note','collaboration'] for v in (c[k] if isinstance(c[k],list) else [c[k]])) and all(b['title'] in public and b['url'] in public and b['note'] in public for b in c['background']))
test('no_private_audit_details_in_public_copy',not re.search(r'2026-10-25|sha256|SHA-256|CHECKPOINT|\b512\b|\b108\b|\b1662\b|\b1660\b|\b23 regular\b|quarantine|root.clearance|scope verdict|readiness51|live47',public,re.I))
test('null_followup',c['follow_up'] is None and g['follow_up'] is None and clear['follow_up'] is None)
test('ai_unrefereed_disclosure','extensively' in c['ai_disclosure'] and 'unrefereed preprint' in c['ai_disclosure'] and 'not independent human or journal peer review' in c['ai_disclosure'] and g['human_peer_review'] is False and g['formal_machine_verification'] is False)
test('pre_render_only',not c['review_metadata']['rendered'] and not c['review_metadata']['deployed'] and g['preparation_state']=='BINDINGS_READY_RENDERING_PENDING')
res={'status':'PASS' if all(checks.values()) else 'FAIL','scope':'PRE_RENDER_EDITORIAL_BINDINGS_ONLY','checks':checks,'details':details,'not_established':['actual rendered public-copy approval','local or live HTTP','browser/desktop/mobile','native spreadsheet AA URL','formal proof or human peer review']}
with out.open('x') as f:f.write(json.dumps(res,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':res['status'],'checks':len(checks),'failed':[k for k,v in checks.items() if not v],'report':str(out)},indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
