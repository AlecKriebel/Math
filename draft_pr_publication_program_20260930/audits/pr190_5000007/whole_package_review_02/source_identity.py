"""Read-only independent HTTPS authentication; external bodies remain in memory."""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urljoin
import concurrent.futures,datetime,hashlib,io,json,re,zipfile
R=Path(__file__).resolve().parent;A=R.parent
rows=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def fetch(url):
    row={'UTC_start':now(),'URL':url,'method':'GET'}
    try:
        with urlopen(Request(url,headers={'User-Agent':'PR190 independent verification/2'}),timeout=35) as f:
            data=f.read(8000001);row.update({'status':f.status,'final_URL':f.url,'content_type':f.headers.get('Content-Type'),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'UTC_end':now()})
            if len(data)>8000000:raise ValueError('Body exceeds independent 8MB cap')
    except Exception as e:
        row.update({'error_type':type(e).__name__,'error':str(e),'UTC_end':now()});data=None
    rows.append(row);return data,row

def need(b,m):
    if not b:raise ValueError(m)
def localhash(p):
    b=p.read_bytes();return {'path':str(p.relative_to(A)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
result={'UTC_start':now(),'network':rows,'scope':'Current HTTPS body identity and stated dates only; no historical exact-byte public visibility, awareness, firstness or independence inference; no third-party code executed.'}
try:
    raw,recordrow=fetch('https://zenodo.org/api/records/23267641');need(raw,'record access failed');record=json.loads(raw)
    fs=record['files'];result['record_selected']={'id':record['id'],'doi':record.get('doi'),'title':record['metadata']['title'],'publication_date':record['metadata'].get('publication_date'),'version':record['metadata'].get('version'),'created':record.get('created'),'modified':record.get('modified')}
    expected={'AMR-049-paper.pdf':'ff6b9ba5f9bac0027a39d6e06319f04ff08bf24776a47cf7070213924d454707','AMR-049-source.zip':'d17acdd2a34f34685b3d854d3abfd4dbf19e253599c5c3f89f94e1ea078dd8d0','AMR-049-verification-report.md':'6f89f5ee24d11fa7bc0dbc7677bb883a8173160a2ca466708c6718f9d2b5f6a5'}
    result['DOI_files']=[]
    for f in fs:
        name=f['key'];need(name in expected,'unexpected DOI file')
        url=f['links'].get('self') or f['links'].get('content');b,row=fetch(url);need(b,'DOI file failed')
        checksum='md5:'+hashlib.md5(b).hexdigest();need(len(b)==f['size'] and checksum==f['checksum'] and hashlib.sha256(b).hexdigest()==expected[name],'DOI checksum mismatch')
        result['DOI_files'].append({'name':name,'record_size':f['size'],'record_checksum':f['checksum'],'computed_checksum':checksum,'matches_pinned_website_SHA256':True,**row})
        if name=='AMR-049-source.zip':
            local=A/'current_literature_priority_adversary/private_sources/ferudun_source_current.zip';need(b==local.read_bytes(),'source ZIP not equal locally read website copy')
            with zipfile.ZipFile(io.BytesIO(b)) as z:
                names=z.namelist(); main=next(n for n in names if n.endswith('/main.tex') or n=='main.tex');t=z.read(main).decode()
                result['source_archive_inspection']={'entries':len(names),'main_tex':main,'main_tex_SHA256':hashlib.sha256(z.read(main)).hexdigest(),'relevant_section_labels_present':{s:s in t for s in ['central symmetry','public record','The dodecahedron']},'external_programs_executed':False}
        if name=='AMR-049-paper.pdf':need(b==(A/'current_literature_priority_adversary/private_sources/ferudun_paper_current.pdf').read_bytes(),'PDF differs from inspected website copy')
    page,pagerow=fetch('https://eulersolve.org/papers/amr-049/');need(page,'website unavailable');html=page.decode()
    candidates=sorted(set(urljoin('https://eulersolve.org/papers/amr-049/',x) for x in re.findall(r'(?:href|src)=[\"\x27]([^\"\x27]+)',html) if any(w in x for w in ['paper.pdf','source.zip','verification-report.md','metadata.json'])))
    result['website_current_links']=candidates;result['current_website_retrievals']=[]
    for u in candidates:
        b,row=fetch(u);need(b,'website linked body failed');result['current_website_retrievals'].append(row)
        if 'paper.pdf' in u:need(hashlib.sha256(b).hexdigest()==expected['AMR-049-paper.pdf'],'website PDF changed')
        if 'source.zip' in u:need(hashlib.sha256(b).hexdigest()==expected['AMR-049-source.zip'],'website source changed')
        if 'verification-report.md' in u:need(hashlib.sha256(b).hexdigest()==expected['AMR-049-verification-report.md'],'website report changed')
    raw,row=fetch('https://api.datacite.org/dois/10.5281/zenodo.23267641');need(raw,'DataCite failed');attr=json.loads(raw)['data']['attributes'];result['datacite_selected']={k:attr.get(k) for k in ['doi','created','registered','published','publicationYear','version']}
    raw,row=fetch('https://api.github.com/repos/AlecKriebel/Math/pulls/190');need(raw,'GitHub PR failed');pr=json.loads(raw);need(pr['created_at']=='2026-10-01T04:03:35Z','PR creation mismatch');result['GitHub_PR_selected']={k:pr.get(k) for k in ['number','created_at','html_url','state','draft']}
    u='https://raw.githubusercontent.com/AlecKriebel/Math/c9162a45d30120b10b42b1f79c50bab417ed287b/unsolved_math_prioritization/attempts/5000007/PROOF_V2.md';raw,row=fetch(u);need(raw and hashlib.sha256(raw).hexdigest()=='f96288e95c946731091989cea3eb087829c94cf966898dae792122567da3f16b','initial proof identity failed');result['original_commit_body']=row
    u='https://raw.githubusercontent.com/DannyExperiments/dodecahedron-short-geodesic-counterexample/7b403decdc9317f6ba3dc2c4a91243a0bf0c9ff9/proof/PROBLEM_AND_PROOF.md';raw,row=fetch(u);need(raw and hashlib.sha256(raw).hexdigest()=='84baf6ab43b2c33c7a1b11e50e47fe2b48d891da981f44da9da18f4a5ba60513','pinned public certificate identity');text=raw.decode();result['pinned_public_primary']=row
    result['pinned_literal_fields_present']={label:bool(re.search(pattern,text)) for label,pattern in {'eta_pi_over_5':r'pi/5','coefficient31_13':r'31\s*\+\s*13','coefficient_minus17_minus8':r'-17\s*-\s*8','word16':r'1,\s*3,\s*11,\s*8,\s*6,\s*5,\s*1,\s*3,\s*11,\s*10,\s*8,\s*6,\s*4,\s*5,\s*2,\s*1'}.items()}
    result['primary_local_bodies']=[localhash(A/p) for p in ['root_primary_sources_private/fuchs2021.pdf','root_primary_sources_private/platonic181104131v2.pdf','current_literature_priority_adversary/private_sources/troub_2202.04892v3.pdf','current_literature_priority_adversary/private_sources/ferudun_paper_current.pdf','current_literature_priority_adversary/private_sources/ferudun_source_current.zip']]
    result['status']='PASS'
except Exception as e:
    result['status']='INCOMPLETE';result['error_type']=type(e).__name__;result['error']=str(e)
result['UTC_end']=now();(R/'SOURCE_IDENTITY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if result['status']!='PASS':raise SystemExit(1)
