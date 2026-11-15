"""Record selected identity evidence, only inside the new owned folder."""
from preflight_core import *
from datetime import datetime,timezone
from urllib.parse import urljoin
import io,zipfile
def w(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
need(not (O/'SELECTED_IDENTITY_EVIDENCE.json').exists(),'Refusing overwrite')
inventory=load(O/'DOCS_OBJECT_BINDINGS.json');by={x['path']:x for x in inventory}
article='docs/papers/gromov-unitary-lipschitz/index.html';a=git('show',COMMIT+':'+article).decode()
h=HTMLIdentity();h.feed(a)
base='https://aleckriebel.github.io/Math/papers/gromov-unitary-lipschitz/'
resolved=[{'literal_href':x,'resolved_URL':urljoin(base,x)} for x in h.links]
kitpath='docs/papers/gromov-unitary-lipschitz/zenodo-upload.zip';kit=git('show',COMMIT+':'+kitpath)
z=zipfile.ZipFile(io.BytesIO(kit));need(z.testzip() is None,'Selected six-member upload kit CRC')
members=[]
for x in z.infolist():
    b=z.read(x);members.append({'name':x.filename,'bytes':len(b),'sha256':sha(b)})
    if x.filename in ['paper.pdf','reproducibility.zip']:
        need(b==git('show',COMMIT+':docs/papers/gromov-unitary-lipschitz/'+x.filename),'Upload kit same manuscript/package')
meta=json.loads(z.read('metadata.json'))
need(meta['version']=='1.1' and meta['title']==load(O/'TARGET_IDENTITIES.json')['22929857']['title'],'Kit version/title')
idx=HTMLIdentity();idx.feed(git('show',COMMIT+':docs/index.html').decode())
sitemap=git('show',COMMIT+':docs/sitemap.xml').decode()
pdf_extract=next(x for x in load(O/'REUSED_EXTRACT_BINDINGS.json') if x['public_path']=='docs/papers/gromov-unitary-lipschitz/paper.pdf')
w('SELECTED_IDENTITY_EVIDENCE.json',{'UTC':datetime.now(timezone.utc).isoformat(),'record':'22929857','current_article':by[article],
 'article_entire_source_personally_read':True,'canonical':h.canonicals,'article_anchor_ids':h.ids,'all_article_links_resolved':resolved,
 'native_record_related_identifier_relation':'isDocumentedBy','native_TeX_literal_project_URL':base,
 'PDF_native_annotation_read':{'method':'bundled-runtime pypdf PdfReader; annotations only, no new text extraction','pages':4,'project_URI_page':4,'project_URI':base},
 'exact_same_public_and_native_assets':[by['docs/papers/gromov-unitary-lipschitz/paper.pdf'],by['docs/papers/gromov-unitary-lipschitz/reproducibility.zip']],
 'public_full_reader_extract':pdf_extract,'byline_version':'1.1','byline_date':'23 September 2026',
 'predeposit_upload_kit':{'blob_binding':by[kitpath],'CRC_valid':True,'members':members,'metadata_version':meta['version'],
 'metadata_title':meta['title'],'metadata_DOI_absent':not bool(meta.get('doi')),'PDF_and_reproducibility_identical_to_current_assets':True,
 'classification':'Predeposit preparation snapshot of this same v1.1 work; not a second work, older PDF, additional canonical, or different published Zenodo version.'},
 'index_links_to_article':[x for x in idx.links if 'gromov-unitary-lipschitz' in x],
 'sitemap_contains_article':base in sitemap,'index_and_sitemap_absence_does_not_erase_actual_article':True,
 'no_live_HTTP_or_browser_verification':True,'redirect_authorized_or_written':False})
ex=[]
for path,pages,title,reason in [
 ('docs/papers/unified-consequences/paper.pdf',[1,7],'A 14-variable unipotent Keller map and every-order image and vanishing obstructions','The only Yamabe hit is dynamical Markus–Yamabe in the consequence discussion. The title, abstract and surrounding context concern polynomial Keller maps, Special Image/Vanishing obstructions and exact fibers, not weighted conformal heat traces or the Yamabe operator.'),
 ('docs/papers/unipotent-three-point/paper.pdf',[1,4],'A 14-variable polynomial map with everywhere unipotent Jacobian and a three-point fiber','The only Yamabe hit explicitly distinguishes classical dynamical Markus–Yamabe from algebraic injectivity. This polynomial-map precursor is a different work, not a version or legacy article of the weighted Yamabe heat-trace manuscript.')]:
    e=next(x for x in load(O/'REUSED_EXTRACT_BINDINGS.json') if x['public_path']==path)
    ex.append({'path':path,'source_blob_binding':by[path],'complete_extract_binding':e,'personally_read_PDF_text_pages':pages,'title':title,'exact_exclusion_reason':reason,
               'scientific_validity_not_assessed':True,'redirect_target':None})
other='docs/papers/unified-consequences/index.html'
b=git('show',COMMIT+':'+other);(O/'selected-released-blobs'/other.replace('/','__')).write_bytes(b)
w('EXCLUSIONS.json',{'weighted_Yamabe_false_positive_readers':ex,'related_entire_actual_article_read':by[other],
 'other_records_nonunitary_candidates':[],'no_unresolved_positive_candidate':True,'no_relabeling_of_distinct_works_as_versions':True})
w('READ_LEDGER.json',{'UTC':datetime.now(timezone.utc).isoformat(),
 'personally_read':[{'path':article,'extent':'entire actual released HTML, including all head/body/links/version/date/Zenodo section'},
 {'path':'docs/papers/gromov-unitary-lipschitz/zenodo-metadata.json','extent':'entire actual current JSON'},
 {'path':'docs/index.html','extent':'entire decoded visible index,15671 characters, plus raw link search'},
 {'path':'docs/sitemap.xml','extent':'entire34URL actual sitemap'},
 {'path':other,'extent':'entire actual HTML'},*ex],
 'source_link_inspection':'Four exact native record metadata objects and selected controlling TeX literal URL lists; unitary native PDF actual annotation page4.',
 'automated_search':'All260 full representations, including76 authenticated completePDF extracts/854pages; not a personal reread of all854pages.',
 'archive_boundary':'All254 public blobs hash-authenticated; support archives not recursively searched. Only selected six-member public unitary upload kit CRC/identity metadata and payload equality inspected, no nested programs or audits executed.'})
print(json.dumps({'selected_article':by[article],'index_link_count':len([x for x in idx.links if 'gromov-unitary-lipschitz' in x]),'sitemap_contains':base in sitemap,'kit_members':len(members),'exclusions':len(ex)},indent=2))
