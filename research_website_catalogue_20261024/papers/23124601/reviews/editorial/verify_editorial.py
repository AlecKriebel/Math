"""Read-only editorial/static custody checks; no source programme execution.

Mutated-input controls use independent deep copies in memory. This is neither a
mathematical proof replay nor a renderer/browser/native acceptance check.
"""
from pathlib import Path, PurePosixPath
import copy, gzip, hashlib, json, re, zipfile
from pypdf import PdfReader

O=Path(__file__).resolve().parent
T=O.parent.parent
P=T.parent.parent
ROOT=P/'verification/root-clearance-23124601-20261025.json'
STATUS='PASS_WITH_CLASSICAL_IMPORTS_AND_EXPLICIT_CHECKER_RUNTIME_LIMITS'
ROOT_SHA='61b359b6474c370fa985cac952d391134815e7af8ae243f025417343b470b626'
FALSE_GATES=['rendered','deployed','rendered_public_copy_approved','local_http_verified',
             'live_http_verified','browser_verified','native_sheet_publication_verified',
             'public_page_published','root_editorial_clearance_received']

def need(test,message):
    if not test: raise RuntimeError(message)
def load(p): return json.loads(p.read_text())
def sha(b): return hashlib.sha256(b).hexdigest()
def binding(p):
    b=p.read_bytes()
    return dict(bytes=len(b),sha256=sha(b))

def validate(pub,prom,sec,req,ready,root,transport,raw):
    need(root==load(ROOT) and root['status']==STATUS,'Qualified root authority changed')
    need(pub['title']==raw['metadata']['title']==ready['title'] and raw['id']==23124601,'Title/record')
    need(pub['author']=='Alec Kriebel' and pub['orcid']=='https://orcid.org/0009-0001-9320-500X','Author/ORCID')
    need(pub['doi']==raw['doi']=='10.5281/zenodo.23124601','Selected DOI')
    need(pub['version']==ready['metadata_version']=='1.0' and pub['version_field_present'] is True,'Actual API version')
    need(pub['publication_date']==ready['declared_publication_date']=='2026-10-03','Declared date')
    need(pub['license']=='CC BY 4.0' and pub['license_url']=='https://creativecommons.org/licenses/by/4.0/'
         and raw['metadata']['license']['id']=='cc-by-4.0','Actual deposit license')
    sb=pub['source_binding']
    need(sb['source_assets_field']=='assets' and sb['assets']==ready['assets'],'Native assets shape')
    need('all_assets' not in sb and 'metadata_path' not in sb,'Source schema alias')
    need(sb['source_receipt_original']==ready==prom['source_receipt_original'],'Whole original readiness')
    need([x['native_file_object'] for x in ready['assets']]==raw['files']==sb['published_file_objects'],
         'Whole native compact file objects')
    need([x['path'] for x in ready['assets']]==['wajnryb-artin-a5-verification.zip','fixed_generator_classification.pdf'],
         'Actual source order/relative paths')
    need(sb['transport_receipt_original']==transport==prom['transport_receipt_original'] and len(transport)==6,
         'Whole six actual transport receipts')
    need(all(x['status']==200 for x in transport) and 'elapsed_seconds' not in transport[-1],
         'Original transport facts/schema')
    need(sb['source_receipt_sha256']==prom['source_receipt_sha256']==sha((T/'sources/SOURCE_READY.json').read_bytes()),
         'Readiness bytes')
    need(sb['raw_record_path']=='sources/record.raw.json' and
         sb['raw_record_sha256']==sha((T/'sources/record.raw.json').read_bytes()),'Raw native metadata')
    need(sb['manuscript_version'] is None and sb['manuscript_version_printed'] is False and
         sb['zenodo_version']=='1.0','Unprinted manuscript version')
    need(sb['record_created_utc']==ready['actual_created']==raw['created'] and
         sb['record_updated_utc']==ready['actual_updated']==raw['updated'],'Native creation/update')
    need(pub['edition_label']==pub['citation_edition_label']=='Zenodo version 1.0' and
         pub['edition_note']=='Manuscript and declared publication date: 3 October 2026. Zenodo records version 1.0; the manuscript prints no version number.',
         'Visible date/edition')
    need(pub['pdf_filename']==ready['assets'][1]['path'] and pub['supplement_filename']==ready['assets'][0]['path'],
         'Selected complete assets')
    need(pub['pdf_pages']==ready['actual_reader_pages']==6 and sb['public_page_reader_pdf_count']==1,'Reader count/pages')
    need(sb['pdf_sha256']==prom['pdf_sha256']==ready['assets'][1]['sha256'] and
         sb['supplement_sha256']==prom['supplement_sha256']==ready['assets'][0]['sha256'],'Asset bindings')
    need((sb['archive_outer_regular_file_count'],sb['archive_regular_member_occurrences'],
          sb['archive_container_count'],sb['nested_gzip_stream_count'],sb['nested_zip_tar_count'],
          sb['archive_embedded_pdf_count'],sb['total_distinct_reader_pdf_count'])==(60,67,8,7,0,0,1),
         'Recursive archive and distinct reader accounting')
    need(prom['status']==pub['review_metadata']['scientific_clearance_status']==STATUS and
         prom['root_clearance_record']==root,'Separate whole root adoption')
    need(prom['root_clearance_sha256']==pub['review_metadata']['root_clearance_sha256']==ROOT_SHA,'Authority hash')
    for family,entry in root['reviews'].items():
        original=load(P/entry['verdict'])
        adopted=prom['reviews'][family]
        need(entry['whole_original_custom_verdict']==original==adopted['verdict'],
             'Whole original custom verdict: '+family)
        need(adopted['root_authority_entry']==entry,'Whole root review entry: '+family)
        need(sha((P/entry['report']).read_bytes())==entry['report_sha256'] and
             sha((P/entry['verdict']).read_bytes())==entry['verdict_sha256'],'Actual report/verdict hashes')
    for obj in [pub,prom]:
        need(obj['AA'] is None and obj['canonical_url'] is None and obj['follow_up'] is None,'Null later authority/follow-up')
    for obj in [pub['review_metadata'],prom]:
        need(all(obj[k] is False for k in FALSE_GATES) and obj['native_sheet_aa_url'] is None,
             'Later publication gates')
    need(pub['review_metadata']['scientific_clearance_received'] is True,'Separate received science')
    for key in ['title','description','status','edition_label','edition_note','abstract_heading','abstract',
                'plain_language','result','why_it_works','limitations','background','ai_disclosure',
                'collaboration','reader_intro']:
        need(pub[key]==sec[key],'Public paragraph binding: '+key)
    need(70<=len(pub['description'])<=200 and pub['description']==sec['description'],'SEO description')
    tex=(T/'sources'/ready['controlling_TeX']['path']).read_text()
    original=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
    need((O/'ORIGINAL_ABSTRACT.tex').read_text()==sb['abstract_tex']==original,'Entire original abstract substring')
    normalized=original
    for a,b in sb['abstract_normalization']['exact_presentational_replacements'].items():
        normalized=normalized.replace(a,b)
    need(pub['abstract']==' '.join(normalized.split()) and '\\' not in pub['abstract'] and
         pub['abstract_heading']=='Original abstract' and pub['abstract_is_original'] is True,'Full indexable original abstract')
    result=' '.join(pub['result'])
    for text in ['G=B₆/⟨⟨ch⁻¹⟩⟩','c=(a₁a₂a₃a₄)⁵','h=a₅a₄a₃a₂a₁²a₂a₃a₄a₅',
                 'For every literal positive word in these five fixed generators whose product in G is c²',
                 'At length 20 there is one strict Hurwitz class','At length 30 there is one',
                 'At length 40 there are exactly two','(a₁a₂a₃a₄)¹⁰ and (a₂a₃a₄a₅)¹⁰',
                 'exactly the ten distinct cyclic rotations of h² as literal words',
                 'Simultaneous conjugation identifies the two length-40 classes',
                 'exactly one class at each of the three lengths',
                 'Intermediate tuples may contain conjugates of generators']:
        need(text in result,'Full literal theorem missing: '+text)
    need('arbitrary products of conjugates' in ' '.join(pub['limitations']) and
         'historical priority' in ' '.join(pub['limitations']).lower(),'Scope/priority limits')
    need(len(pub['background'])==7 and all(x in json.dumps(pub['background'],ensure_ascii=False)
         for x in ['Wajnryb','Auroux','Matsumoto','Sato','Baykur','González-Meneses','Casson','Perron–Vannier']),
         'Substantive prior credit')
    for phrase in ['AI tools were used extensively','unrefereed preprint','without external human peer review',
                   'formal proof-assistant certification','actual research contributions and mutual agreement']:
        need(phrase in pub['ai_disclosure']+' '+pub['collaboration'],'Disclosure/collaboration')
    bib=(O/'CITATION.bib').read_text()
    need(pub['prepared_bibtex']==req['prepared_bibtex']==bib and sb['prepared_bibtex_sha256']==sha(bib.encode()),
         'Exact prepared BibTeX')
    for phrase in [pub['title'],'date = {2026-10-03}','version = {1.0}',pub['doi'],'0009-0001-9320-500X']:
        need(phrase in bib,'Prepared citation identity')
    path='/research/'+pub['slug']+'/'
    pdf=ready['assets'][1];archive=ready['assets'][0]
    pu=pdf['native_file_object']['links']['self'];zu=archive['native_file_object']['links']['self']
    need(req['planned_path']==path and req['pdf_iframe_count']==1 and
         req['pdf_local_href']==path+pdf['path'] and req['zip_local_href']==path+archive['path'] and
         req['pdf_original_href']==pu and req['zip_original_href']==zu,'One exact reader and original assets')
    expected=[('Open PDF',path+pdf['path'],False),('Download PDF',path+pdf['path'],True),
              ('Download original PDF from Zenodo',pu,True),('Download complete ZIP',path+archive['path'],True),
              ('Download original complete ZIP from Zenodo',zu,True),('Download BibTeX',path+'citation.bib',True)]
    need([(x['label'],x['href'],x['download']) for x in req['required_links']]==expected,
         'Exact open/download links and semantics')
    need(req['article_assets']==['index.html',pdf['path'],archive['path'],'citation.bib'] and
         req['extra_assets']==pub['additional_assets']==[],'Complete unchanged article assets only')
    need(pub['related_resources']==[{'label':'Zenodo original PDF','url':pu},
                                    {'label':'Zenodo original complete ZIP','url':zu}],'Original resource links')
    return True

def controls(values):
    tests=[]
    def reject(name,mutate):
        v=copy.deepcopy(values)
        mutate(v)
        try: validate(*v)
        except (RuntimeError,KeyError,TypeError,IndexError): tests.append(dict(name=name,rejected=True))
        else: raise RuntimeError('Accepted changed input: '+name)
    reject('generic root status',lambda v:v[1].__setitem__('status','PASS'))
    reject('altered whole family verdict',lambda v:v[1]['reviews']['scope']['verdict'].__setitem__('complete',False))
    reject('dropped analytic runtime limits',lambda v:v[1]['reviews']['analytic']['verdict'].pop('limits'))
    reject('manufactured original authority',lambda v:v[1]['reviews']['adversarial']['verdict'].__setitem__('publication_clearance',True))
    reject('altered root entry',lambda v:v[1]['reviews']['scope']['root_authority_entry'].pop('whole_original_custom_verdict'))
    reject('wrong declared date',lambda v:v[0].__setitem__('publication_date','2026-10-04'))
    reject('invented manuscript edition',lambda v:v[0]['source_binding'].__setitem__('manuscript_version','1.0'))
    reject('wrong API version',lambda v:v[0].__setitem__('version','1.1'))
    reject('source schema alias',lambda v:v[0]['source_binding'].__setitem__('all_assets',v[0]['source_binding']['assets']))
    reject('changed native asset order',lambda v:v[0]['source_binding']['assets'].reverse())
    reject('invented transport field',lambda v:v[0]['source_binding']['transport_receipt_original'][-1].__setitem__('elapsed_seconds',1))
    reject('altered native content URL',lambda v:v[0]['source_binding']['assets'][1]['native_file_object']['links'].__setitem__('self','https://example.invalid/paper.pdf'))
    reject('missing gzip occurrences',lambda v:v[0]['source_binding'].__setitem__('archive_regular_member_occurrences',60))
    reject('invented embedded PDF',lambda v:v[0]['source_binding'].__setitem__('archive_embedded_pdf_count',1))
    reject('wrong reader pages',lambda v:v[0].__setitem__('pdf_pages',5))
    reject('truncated original abstract',lambda v:v[0].__setitem__('abstract',v[0]['abstract'].split('.')[0]+'.'))
    def strict(v):
        v[0]['result'][1]=v[0]['result'][1].replace('At length 40 there are exactly two','At length 40 there is exactly one')
        v[2]['result']=copy.deepcopy(v[0]['result'])
    reject('collapsed strict length40 split in both copies',strict)
    def ten(v):
        v[0]['result'][2]=v[0]['result'][2].replace('ten distinct','nine distinct')
        v[2]['result']=copy.deepcopy(v[0]['result'])
    reject('wrong exact literal length20 set in both copies',ten)
    def universe(v):
        v[0]['result'][1]=v[0]['result'][1].replace('literal positive word in these five fixed generators','product of arbitrary generator conjugates')
        v[2]['result']=copy.deepcopy(v[0]['result'])
    reject('broadened input universe in both copies',universe)
    reject('wrong license',lambda v:v[0].__setitem__('license','CC0'))
    reject('omitted prior credit',lambda v:v[0]['background'].pop())
    reject('second reader iframe',lambda v:v[3].__setitem__('pdf_iframe_count',2))
    reject('missing original PDF download',lambda v:v[3]['required_links'].pop(2))
    reject('PDF download loses download semantics',lambda v:v[3]['required_links'][1].__setitem__('download',False))
    reject('wrong ZIP destination',lambda v:v[3]['required_links'][3].__setitem__('href','subset.zip'))
    reject('wrong prepared citation',lambda v:v[0].__setitem__('prepared_bibtex',v[0]['prepared_bibtex'].replace('version = {1.0}','version = {1.1}')))
    reject('native AA manufactured',lambda v:v[1].__setitem__('AA','https://example.invalid/'))
    reject('publication gate advanced',lambda v:v[1].__setitem__('public_page_published',True))
    reject('unsanctioned follow-up',lambda v:v[0].__setitem__('follow_up','Extend to all ranks'))
    return tests

def main():
    need(sha(ROOT.read_bytes())==ROOT_SHA,'Wrong root source bytes')
    before=load(O/'ORIGINAL_INPUTS_BEFORE.json')['bindings']
    for path,expected in before.items(): need(binding(Path(path))==expected,'Original changed: '+path)
    need(all(not (T/'sources'/name).exists() for name in
             ['record.json','receipt.json','normalized-metadata.json','metadata.normalized.json']),
         'Invented persisted source alias')
    prior=load(O/'PROTECTED_PRIOR_PACKAGES.json')['bindings']
    for path,expected in prior.items(): need(binding(Path(path))==expected,'Prior package changed: '+path)
    for entry in load(O/'ORIGINAL_OBJECT_COPIES.json')['objects']:
        expected={k:entry[k] for k in ['bytes','sha256']}
        need(binding(Path(entry['original']))==binding(O/entry['copy'])==expected,'Whole original object copy')
    pub=load(T/'publication.json');prom=load(T/'promotion.json')
    sec=load(O/'public-sections.json');req=load(O/'READER_REQUIREMENTS.json')
    ready=load(T/'sources/SOURCE_READY.json');root=load(ROOT)
    transport=load(T/'sources/transport-receipts.json');raw=load(T/'sources/record.raw.json')
    values=[pub,prom,sec,req,ready,root,transport,raw]
    validate(*values)
    need(prom['publication_sha256']==sha((T/'publication.json').read_bytes()),'Exact publication hash')
    need(len(PdfReader(T/'sources/fixed_generator_classification.pdf').pages)==6,'Actual PDF page count')
    for asset in ready['assets']:
        data=(T/'sources'/asset['path']).read_bytes()
        need(len(data)==asset['bytes']==asset['native_file_object']['size'] and sha(data)==asset['sha256']
             and hashlib.md5(data).hexdigest()==asset['md5']==asset['native_file_object']['checksum'].split(':',1)[1],
             'Original full published asset')
    members=load(T/'sources/archive-custody.json')['members']
    need(len(members)==67,'Full recursive custody count')
    with zipfile.ZipFile(T/'sources/wajnryb-artin-a5-verification.zip') as z:
        need(len([x for x in z.infolist() if not x.is_dir()])==60,'All original outer members')
        for entry in members:
            path=PurePosixPath(entry['member'])
            need(not path.is_absolute() and '..' not in path.parts,'Safe original member')
            data=z.read(entry['member']) if entry['container']=='zip' else gzip.decompress(z.read(entry['archive'].split('!',1)[1]))
            need(len(data)==entry['bytes'] and sha(data)==entry['sha256'] and
                 data==(T/'sources'/entry['path']).read_bytes(),'Complete original payload bytes')
    public=(O/'PUBLIC_COPY.md').read_text()
    for key in ['abstract','status','edition_note','ai_disclosure','collaboration','reader_intro']:
        need(pub[key] in public,'Complete actual public copy: '+key)
    for key in ['plain_language','result','why_it_works','limitations']:
        need(all(x in public for x in pub[key]),'Public paragraph omission: '+key)
    need(pub['prepared_bibtex'].rstrip() in public,'Prepared public citation')
    need(not re.search(r'\b(?:SHA256|custody|checkpoint|replay|root-clearance|assert)\b|20261025|261[,.]?810|90[,.]?921',public,re.I),
         'Private audit detail in public copy')
    changed=controls(values)
    manifest_checked=False
    if (O/'SEAL.json').exists():
        seal=load(O/'SEAL.json');manifest=load(O/'MANIFEST.json')
        need(sha((O/'MANIFEST.json').read_bytes())==seal['manifest_sha256'],'Editorial manifest seal')
        for x in manifest['files']:
            need(binding(O/x['path'])=={k:x[k] for k in ['bytes','sha256']},'Owned sealed file changed')
        need({str(p.relative_to(O)) for p in O.rglob('*') if p.is_file() and p.name not in ['MANIFEST.json','SEAL.json']}==
             {x['path'] for x in manifest['files']},'Owned sealed inventory')
        need(binding(T/'publication.json')==manifest['configs']['publication.json'] and
             binding(T/'promotion.json')==manifest['configs']['promotion.json'],'Sealed configs')
        manifest_checked=True
    return dict(status='PASS',original_bindings=len(before),prior_bindings=len(prior),
                original_object_copies=15,recursive_original_payloads=67,actual_reader_pages=6,
                changed_input_controls=changed,manifest_checked=manifest_checked,
                source_programs_executed=0,mathematical_replays=0,rendering=False,
                network=False,native=False,writes=0)

if __name__=='__main__':
    print(json.dumps(main(),indent=2))
