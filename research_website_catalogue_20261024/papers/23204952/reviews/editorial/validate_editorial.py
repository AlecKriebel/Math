"""Editorial consistency controls only; all hostile variants stay in memory."""
from pathlib import Path
from datetime import datetime, timezone
from copy import deepcopy
import hashlib, json, re, zipfile
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
def readj(f):return json.loads(f.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def binding(f):
    b=f.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def savej(f,o):f.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
def normalize_abstract(raw,id):
    s=' '.join(raw.split())
    replacements=[('Sch\\"utt','Schütt'),('K\\"ahler--Einstein','Kähler–Einstein'),('Druel--Guenancia--P\\u aun','Druel–Guenancia–Păun'),('$-K_X=rL$','−K_X = rL'),('$L$','L'),('$r>\\dim(X)/2+1$','r > dim(X)/2 + 1'),('$n$','n'),('$n\\geq5$','n ≥ 5'),('--','–')]
    for a,b in replacements:s=s.replace(a,b)
    assert '\\' not in s and '$' not in s
    return s
def expected_bib(pub,id):
    month='oct' if pub['publication_date'][5:7]=='10' else 'sep'
    return '@misc{kriebel2026_'+id+',\n  author = {Kriebel, Alec},\n  title = {'+pub['title']+'},\n  year = {2026},\n  month = '+month+',\n  doi = {'+pub['doi']+'},\n  url = {'+pub['canonical_url']+'},\n  version = {'+pub['version']+'},\n  publisher = {Zenodo},\n  note = {'+pub['bibtex_note']+'}\n}\n'

def validate(id,pub,promo,spec,adapter):
    d=P/'papers'/id;e=d/'reviews/editorial';root=readj(P/f'verification/root-clearance-{id}-20261025.json')
    receipt=readj(d/'sources/receipt.json');raw=readj(d/pub['source_binding']['record_path']);m=raw['metadata'];b=pub['source_binding'];fail=[];passed=[]
    def ck(label,ok):
        (passed if ok else fail).append(label)
    ck('exact title/author/ORCID',pub['title']==m['title'] and pub['author']=='Alec Kriebel' and pub['orcid']=='https://orcid.org/0009-0001-9320-500X')
    ck('exact edition/date',pub['version']==m['version']==root['reviewed_zenodo_version'] and pub['publication_date']==m['publication_date']==root['publication_date'])
    slug='metric-rigidity-cubic-compactifications' if id=='23204952' else 'fps-second-moment-equality'
    ck('canonical selected slug',pub['canonical_url']==f'https://aleckriebel.com/research/{slug}/' and pub['slug']==slug)
    ck('complete original normalized abstract',pub['abstract']==normalize_abstract(b['abstract_tex'],id) and pub['abstract_heading']=='Original abstract' and pub['abstract_is_original'] is True)
    tex=(d/b['source_tex_path']).read_text();at=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1).strip()
    ck('literal abstract/source binding',b['abstract_tex']==at and b['abstract_tex_sha256']==sha(at.encode()) and (e/'abstract-source.tex').read_text()==at+'\n')
    candidate=readj(d/b['frozen_scope_content_path'])
    ck('entire frozen scope abstract preserved',pub['abstract']==candidate[b['frozen_scope_abstract_field']] and b['frozen_scope_content_sha256']==binding(d/b['frozen_scope_content_path'])['sha256'])
    ck('later root authority complete and separate',promo['status']==root['status']=='PASS' and promo['disposition_by']=='root' and promo['root_clearance_record']==root and promo['approved_scope']==root['approved_scope'])
    ck('exact root authority hash',promo['root_clearance_sha256']==binding(P/promo['root_clearance_file'])['sha256']==pub['review_metadata']['root_clearance_sha256'])
    ck('complete original receipt preserved',promo['source_receipt_record']==receipt and promo['source_files']==receipt['files'] and b['files']==receipt['files'])
    ck('original receipt hash/path preserved',promo['source_receipt_path']==b['receipt_path']=='sources/receipt.json' and promo['source_receipt_sha256']==b['receipt_sha256']==binding(d/'sources/receipt.json')['sha256']==root['source_receipt_sha256'])
    for lane,r in promo['reviews'].items():
        a=root['reviews'][lane]
        ck('whole original '+lane+' verdict',r['verdict']==readj(d/r['verdict_file']) and r['verdict_sha256']==binding(d/r['verdict_file'])['sha256']==a['verdict_sha256'])
        ck('whole separate '+lane+' root disposition',r['root_authority_entry']==a)
        ck('complete '+lane+' report binding',r['sha256']==binding(d/r['report'])['sha256']==a['report_sha256'])
    ck('root scope-resolution history exact',promo['scope_gate_resolution']==root['scope_gate_resolution'])
    ck('metadata actual paths authenticated',b['metadata_path']==root['metadata_path'] and b['metadata_sha256']==binding(d/b['metadata_path'])['sha256']==root['metadata_sha256'] and b['record_sha256']==binding(d/b['record_path'])['sha256'])
    ck('exact UTC created/updated',b['record_created_utc']==raw['created']==root['record_created_utc'] and b['record_updated_utc']==raw['updated'])
    ck('one selected reader source',pub['pdf_filename']=='paper.pdf' and b['pdf_sha256']==binding(d/'sources/paper.pdf')['sha256']==root['pdf_sha256'] and pub['pdf_pages']==(8 if id=='23204952' else 4))
    ck('complete unchanged archive source',pub['supplement_filename']=='source-and-verification.zip' and b['supplement_sha256']==binding(d/'sources/source-and-verification.zip')['sha256']==root['supplement_sha256'])
    ck('no extra standalone page assets',pub['additional_assets']==[] and b['embedded_assets']==[] and b['additional_reader_pdfs']==[] and adapter['proposed_standalone_assets']==['paper.pdf','source-and-verification.zip'])
    ck('CC BY header and schema',pub['license']==spec['header']['license']=='CC BY 4.0' and spec['metadata']['license']=='https://creativecommons.org/licenses/by/4.0/')
    ck('metadata canonical/citation/abstract',all(spec['metadata'][a]==pub[b_] for a,b_ in [('canonical','canonical_url'),('description','description'),('citation_title','title'),('citation_author','author'),('citation_author_orcid','orcid'),('citation_doi','doi'),('abstract','abstract')]) and spec['metadata']['citation_publication_date']==pub['publication_date'].replace('-','/'))
    ck('ScholarlyArticle/preprint status',spec['metadata']['scholarly_type']=='ScholarlyArticle' and spec['metadata']['creativeWorkStatus']=='Unrefereed preprint')
    s={x['id']:x for x in spec['sections']}
    ck('all eleven indexable sections',len(s)==11 and len(spec['sections'])==11)
    for id_,key in [('abstract','abstract'),('plain-language','plain_language'),('result','result'),('proof','why_it_works'),('limits','limitations'),('collaborate','collaboration')]:
        expect=pub[key] if isinstance(pub[key],list) else [pub[key]]
        ck('full public '+id_+' prose',s[id_].get('paragraphs')==expect)
    ck('full public status/edition prose',s['status']['paragraphs']==[pub['ai_disclosure'],pub['edition_note']])
    ck('exact full prior-credit entries',s['background']['references']==pub['background'])
    reader=s['paper'];links=reader['links'];canonical=pub['canonical_url']
    ck('one source-bound iframe',sum('iframe' in x for x in spec['sections'])==1 and reader['iframe']['src']==canonical+'paper.pdf')
    ck('one direct-open PDF',sum(x.get('role')=='open' for x in links)==1 and links[0]['url']==canonical+'paper.pdf')
    downloads=[x for x in links if x.get('download') is True]
    ck('two explicit correct PDF downloads',len(downloads)==2 and [x['url'] for x in downloads]==[canonical+'paper.pdf',f'https://zenodo.org/records/{id}/files/paper.pdf'])
    ck('correct full reader page count',reader['paragraphs']==[f"Read the complete {pub['pdf_pages']}-page paper in the on-page PDF reader."])
    material_urls=[x['url'] for x in s['materials']['links']]
    ck('complete ZIP local and original links',canonical+'source-and-verification.zip' in material_urls and f'https://zenodo.org/records/{id}/files/source-and-verification.zip' in material_urls)
    ck('exact prepared BibTeX',spec['bibtex']==expected_bib(pub,id)==(e/'citation.bib').read_text())
    ck('no follow-up manufactured',pub['follow_up'] is None and promo['follow_up'] is None and spec['follow_up'] is None and spec['native_sheet_aa_url'] is None and promo['native_sheet_aa_url'] is None)
    ck('render/live/browser/native all pending',promo['rendered_copy_verified'] is False and promo['live_verified'] is False and promo['browser_verified'] is False and pub['review_metadata']['rendered'] is False and pub['review_metadata']['deployed'] is False and adapter['rendered'] is False and adapter['shared_scripts_changed'] is False)
    public='\n'.join(pub['plain_language']+pub['result']+pub['why_it_works']+pub['limitations']+[pub['abstract'],pub['ai_disclosure'],pub['edition_note'],pub['description']]+[str(x) for x in s.values()])
    ck('no private audit narrative or hashes',not any(word in public.lower() for word in ['root review','custody','checksum validation','seal bindings','2026-10-25','reviewer control','http 429','acquisition receipt','current catalogue429','121 exact','298 exact','audit completed']) and re.search(r'\b[0-9a-f]{64}\b',public) is None)
    ck('extensive AI and honest status',all(x in pub['ai_disclosure'].lower() for x in ['extensively','unrefereed','human','peer review','formal proof-assistant','responsible']))
    ck('passive substantive collaboration',all(x in pub['collaboration'].lower() for x in ['substantive','actual research and writing contributions','mutual agreement']) and not any(x in pub['collaboration'].lower() for x in ['contact me','email','correspond']))
    if id=='23204952':
        result=' '.join(pub['result']);proof=' '.join(pub['why_it_works']);limits=' '.join(pub['limitations']);plain=' '.join(pub['plain_language'])
        ck('Cubic full Cartier theorem retained',all(x in result for x in ['irreducible normal projective complex klt Fano','m≥1','bounded potentials','ample Cartier','positive integer r','ω_X^[−1]≅L^⊗r','r>m/2+1','every irreducible normal finite quasi-étale cover','No such cover','I','J or −J']))
        ck('Cubic full boundary application retained',all(x in result for x in ['n≥5','every dimension 2≤k≤n','G_n(ℂ)/⟨σ⟩','Q-Gorenstein smoothing locus','Every metric isometry','including across their singular loci','hyperplane Cartier','precisely conjugation orbits']))
        ck('Cubic complete dependency chain explicit',all(x in proof for x in ['vol̂(x,X)≤2(k−1)^k','all 2≤k≤n','all centered real valuations','vol̂(v_ξ)=k^kΘ(C)','2(1−1/k)^k','−K_Z=(n−1)L_Z','L_Z^n=3','Fujita','CM','Proposition 3 and Corollary 4','Spotti–Sun']))
        ck('Cubic external proof limits not hidden',all(x in limits for x in ['principal external inputs','complete proofs are not freshly recertified','full chapter proof has not been accessed','itself does not require the upper-gap']))
        ck('Cubic prior stronger comparison credited',all(x in plain for x in ['prior public work','stronger result of Kong, Shen, Zhao and Zhao','first priority is not certified']))
        ck('Cubic exclusions and sharpness correct',all(x in limits for x in ['n≥5','cubic-fourfold','scheme or stack','nonsmoothable']) and 'not an example among cubic fourfolds' in result)
        ck('Cubic original pending scope preserved',promo['reviews']['scope']['verdict'].get('mathematical_verdict','MISSING') is None and promo['reviews']['scope']['verdict'].get('promotion_decision','MISSING') is None)
    else:
        norm=readj(d/'sources/metadata.normalized.json');ck('FPS custom metadata no source alias',b['metadata_path']=='sources/metadata.normalized.json' and b['record_path']=='sources/zenodo-record.raw.json' and not (d/'sources/record.json').exists() and norm['complete_metadata']==m and norm['complete_actual_file_objects']==raw['files'])
        ck('FPS all three actual receipt file objects',len(receipt['files'])==len(b['files'])==3 and all(x['file_object']==next(y for y in raw['files'] if y['key']==x['filename']) and x['url_from_actual_file_object']==x['file_object']['links']['self'] and x['status']==200 for x in b['files']))
        checkdata=(d/'sources/SHA256SUMS').read_bytes();checkentry=next(x for x in receipt['files'] if x['filename']=='SHA256SUMS')
        ck('FPS checksum authenticated unchanged',len(checkdata)==170 and sha(checkdata)==root['additional_public_checksum_file_sha256']==b['published_checksum_sha256']==checkentry['sha256'] and hashlib.md5(checkdata).hexdigest()==checkentry['md5'])
        ck('FPS checksum named payload entries correct',all(sha((d/'sources'/line.split()[1]).read_bytes())==line.split()[0] for line in checkdata.decode().splitlines()) and len(checkdata.decode().splitlines())==2)
        checksumurl=f'https://zenodo.org/records/{id}/files/SHA256SUMS'
        ck('FPS checksum ordinary original link retained',checksumurl in material_urls and any(x['url']==checksumurl for x in pub['related_resources']) and adapter['ordinary_original_checksum_link']==checksumurl)
        result=' '.join(pub['result']);proof=' '.join(pub['why_it_works']);limits=' '.join(pub['limitations']);plain=' '.join(pub['plain_language'])
        ck('FPS universal nonstrict full theorem retained',all(x in result for x in ['n≥1 and r>0','compact and convex with nonempty interior','‖v‖₂≥r for every actual extreme point','C₂(K)≥[r²+(n+1)‖g_K‖₂²]/(n+2)','if and only if K is a nondegenerate n-simplex','all its vertices have norm r','strictly greater than r, equality is impossible']))
        ck('FPS no regularity/centering/origin restriction',all(x in plain for x in ['need not be regular','centroid need not be the origin','need not contain the origin']) and 'only for regular simplices' not in public)
        ck('FPS countable deficit retained',all(x in proof for x in ['actual extreme points','retaining all earlier cells','absolutely convergent','every displayed term is nonnegative','same centroid','fixed positive witness']))
        ck('FPS finite witness full coefficient retained','ab‖u−v_i‖₂²/[(n+1)(n+2)|K|(a+b)]' in result and 'body-dependent' in result)
        ck('FPS prior mechanism and historical scope credited',all(x in limits for x in ['FPS already proved the inequality, simplex moments, finite vertex decomposition and common-centroid rigidity for polytopes','historical question','does not certify','current worldwide openness']))
    return fail,passed

def variants(id,pub,promo,spec,adapter):
    actions=[]
    def add(name,func):actions.append((name,func))
    add('truncate abstract first sentence',lambda p,r,s,a:p.update(abstract=p['abstract'].split('. ',1)[1]))
    add('truncate abstract final qualification',lambda p,r,s,a:p.update(abstract=p['abstract'].rsplit('. ',1)[0]+'.'))
    add('alter abstract middle statement',lambda p,r,s,a:p.update(abstract=p['abstract'].replace('equality','strict equality',1) if 'equality' in p['abstract'] else p['abstract'].replace('stable','semistable',1)))
    add('wrong original-abstract heading',lambda p,r,s,a:p.update(abstract_heading='Summary'))
    add('wrong version',lambda p,r,s,a:p.update(version='9.0'))
    add('confuse creation and declared date',lambda p,r,s,a:p.update(publication_date=p['source_binding']['record_created_utc'][:10]))
    add('wrong ORCID',lambda p,r,s,a:p.update(orcid='https://orcid.org/0000-0000-0000-0000'))
    add('wrong canonical',lambda p,r,s,a:p.update(canonical_url='https://aleckriebel.com/research/wrong/'))
    add('rewrite original scope verdict',lambda p,r,s,a:r['reviews']['scope']['verdict'].update(editorial_manufactured_pass=True))
    add('truncate original analytic verdict',lambda p,r,s,a:r['reviews']['analytic'].update(verdict={}))
    add('truncate original adversarial verdict',lambda p,r,s,a:r['reviews']['adversarial'].update(verdict={}))
    add('rewrite exact root authority',lambda p,r,s,a:r['root_clearance_record'].update(status='EDITORIAL_PASS'))
    add('drop full original receipt file',lambda p,r,s,a:r['source_receipt_record']['files'].pop())
    add('mutate original receipt field',lambda p,r,s,a:r['source_receipt_record']['files'][0].update(invented_status=200))
    add('drop separate root lane authority',lambda p,r,s,a:r['reviews']['scope'].update(root_authority_entry={}))
    add('add standalone cache asset',lambda p,r,s,a:p['additional_assets'].append({'filename':'private-primary.pdf'}))
    add('lose license schema',lambda p,r,s,a:s['metadata'].update(license=''))
    add('lose prepared BibTeX',lambda p,r,s,a:s.update(bibtex=''))
    add('invent follow-up',lambda p,r,s,a:p.update(follow_up='new theorem campaign'))
    add('manufacture live PASS',lambda p,r,s,a:r.update(live_verified=True))
    add('wrong reader page count',lambda p,r,s,a:p.update(pdf_pages=99))
    add('lose Zenodo PDF download',lambda p,r,s,a:next(x for x in s['sections'] if x['id']=='paper')['links'].pop())
    add('wrong iframe reader',lambda p,r,s,a:next(x for x in s['sections'] if x['id']=='paper')['iframe'].update(src='historical.pdf'))
    add('drop ZIP original link',lambda p,r,s,a:next(x for x in s['sections'] if x['id']=='materials')['links'].pop(1))
    add('omit whole precise-result paragraph',lambda p,r,s,a:next(x for x in s['sections'] if x['id']=='result')['paragraphs'].pop())
    if id=='23204952':
        add('omit full boundary application in both views',lambda p,r,s,a:[p.update(result=p['result'][:2]),next(x for x in s['sections'] if x['id']=='result').update(paragraphs=p['result'])])
        add('hide external-theorem proof limit in both views',lambda p,r,s,a:[p['limitations'].pop(1),next(x for x in s['sections'] if x['id']=='limits').update(paragraphs=p['limitations'])])
        add('change every-cover theorem to one-cover',lambda p,r,s,a:[p.update(result=[x.replace('every irreducible normal finite quasi-étale cover','one finite quasi-étale cover') for x in p['result']]),next(x for x in s['sections'] if x['id']=='result').update(paragraphs=p['result'])])
        add('lose all-dimensional dependency chain',lambda p,r,s,a:[p.update(why_it_works=[x.replace('all 2≤k≤n','k=n') for x in p['why_it_works']]),next(x for x in s['sections'] if x['id']=='proof').update(paragraphs=p['why_it_works'])])
    else:
        add('lose original checksum link in both views',lambda p,r,s,a:[p.update(related_resources=[x for x in p['related_resources'] if not x['url'].endswith('/SHA256SUMS')]),next(x for x in s['sections'] if x['id']=='materials').update(links=[x for x in next(y for y in s['sections'] if y['id']=='materials')['links'] if not x['url'].endswith('/SHA256SUMS')])])
        add('strengthen equality to regular simplices in both views',lambda p,r,s,a:[p.update(result=[x.replace('nondegenerate n-simplex','regular simplex') for x in p['result']]),next(x for x in s['sections'] if x['id']=='result').update(paragraphs=p['result'])])
        add('drop centroid term in both views',lambda p,r,s,a:[p.update(result=[x.replace('[r²+(n+1)‖g_K‖₂²]/(n+2)','r²/(n+2)') for x in p['result']]),next(x for x in s['sections'] if x['id']=='result').update(paragraphs=p['result'])])
        add('make extreme-point hypothesis strict in both views',lambda p,r,s,a:[p.update(result=[x.replace('‖v‖₂≥r for every actual extreme point','‖v‖₂>r for every actual extreme point') for x in p['result']]),next(x for x in s['sections'] if x['id']=='result').update(paragraphs=p['result'])])
    results=[]
    for name,func in actions:
        p,r,s,a=map(deepcopy,(pub,promo,spec,adapter));func(p,r,s,a)
        failures,passed=validate(id,p,r,s,a)
        assert failures,('negative control wrongly accepted',id,name)
        results.append(dict(name=name,rejected=True,failed_invariants=failures))
    return results

if __name__=='__main__':
    for id in ['23204952','22983138']:
        d=P/'papers'/id;e=d/'reviews/editorial'
        pub=readj(d/'publication.json');promo=readj(d/'promotion.json');spec=readj(e/'public-sections.json');adapter=readj(e/'SCHEMA_ADAPTER.json')
        failed,passed=validate(id,pub,promo,spec,adapter)
        assert not failed,(id,failed)
        neg=variants(id,pub,promo,spec,adapter)
        archives=[]
        with zipfile.ZipFile(d/'sources/source-and-verification.zip') as z:
            for i in z.infolist():
                if i.is_dir():continue
                path=d/'sources/published-source'/i.filename
                # Cubic archive has no wrapper; FPS has a single wrapper.
                assert path.is_file() and path.read_bytes()==z.read(i),i.filename
                archives.append(dict(member=i.filename,bytes=i.file_size,sha256=sha(z.read(i))))
        for f in readj(d/'sources/receipt.json')['files']:
            name=f.get('filename',f.get('name'));data=(d/'sources'/name).read_bytes()
            assert len(data)==f['bytes'] and sha(data)==f['sha256']
            expected_md5=f.get('md5',f.get('zenodo_checksum','').split(':')[-1]);assert hashlib.md5(data).hexdigest()==expected_md5
        inputs=readj(e/'inputs-before.json')['input_bindings'];after={k:binding(P/k) for k in inputs};assert after==inputs
        savej(e/'editorial-validation.json',dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS_EDITORIAL_CONSISTENCY_ONLY',positive_invariants=passed,positive_count=len(passed),negative_controls=neg,negative_controls_rejected=len(neg),fixture_copies=0,archive_regular_members_compared=len(archives),archive_members=archives,all_original_bindings_preserved=True,original_binding_count=len(inputs),source_programs_run=False,rendered=False,live_verified=False,browser_verified=False,native_sheet_mutated=False,native_AA=None))
        savej(e/'custody-before-after.json',dict(utc=datetime.now(timezone.utc).isoformat(),before=inputs,after=after,all_unchanged=True,scope='Target original authorities and prior private owned artifacts only; no mutable unrelated website/core inputs.'))
        print(id,len(passed),'positive invariants;',len(neg),'altered-object controls rejected;',len(inputs),'original bindings unchanged')
