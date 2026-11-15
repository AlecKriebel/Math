"""Read-only cross-source editorial audit. No supplied code, builders or campaigns run."""
from pathlib import Path
from fractions import Fraction as Q
from urllib.parse import urlparse
import copy
import hashlib
import json
import re

A=Path(__file__).resolve().parent
P=A.parent.parent
IDS=['23124601','23333046','23383952','23539734','22929857','23320818']

def require(x,m):
    if not x:raise RuntimeError(m)
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def same(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
def checkentry(e,base):
    p=Path(e['path']);p=p if p.is_absolute() else base/p
    require(p.is_file() and p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'input identity '+str(p))
def normalize_abstract(raw,binding,rid):
    spec=binding['abstract_normalization']
    out=raw
    if isinstance(spec,dict) and 'exact_presentational_replacements' in spec:
        for old,new in spec['exact_presentational_replacements'].items():out=out.replace(old,new)
    elif rid=='23539734':
        for old,new in spec['replacement_order']:out=out.replace(old,new)
    elif rid=='23383952':
        out=out.replace('\\(','').replace('\\)','').replace("Morpurgo's",'Morpurgo’s').replace('min--max','min–max')
    else:raise RuntimeError('unhandled actual normalization schema')
    return ' '.join(out.split())

def resolved(path,B):
    p=Path(path)
    for candidate in [p] if p.is_absolute() else [P/p,B/p,B/'reviews/editorial'/p]:
        if candidate.is_file():return candidate
    raise RuntimeError('bound original path absent '+path)

def change_first_headers(obj):
    if isinstance(obj,dict):
        for k,v in obj.items():
            if 'header' in k.lower() and isinstance(v,(list,dict)) and v:
                if isinstance(v,list):v.pop(0)
                else:v.pop(next(iter(v)))
                return True
            if change_first_headers(v):return True
    elif isinstance(obj,list):
        return any(change_first_headers(v) for v in obj)
    return False

GUARDS={
'23124601':['five fixed','length 20','length 30','length 40','exactly two','ten distinct cyclic rotations',
            'simultaneous conjugation','Intermediate tuples may contain conjugates','Sato','Casson','priority'],
'23333046':['nilpotent constant terms','actual fixed subfunctor','complete Noetherian local W(k)',
            'every tangent dimension','assuming that both the subgroup and quotient','prorepresentable',
            'hulls','established antecedents','worldwide openness'],
'23383952':['positive Laplacian','W^(3/2)','1106714561/1700054750','13/20','321/500','L = 10000',
            't* = 4a','witness time is a maximizing time','n ≥ 4','classical','not authenticated'],
'23539734':['uniform point weights','T_p(z)/p','fixed x∈[1/2,1)','1/p+64p^(−1/4)',
            'limsup','23/24','upper relative density','weakly','all regular points','finite nonnegative',
            'Assigned periods can exceed p','unrecovered','Neumärker','polynomial-automorphism','zero-density'],
'22929857':['unnormalized Hilbert–Schmidt','operator norm','induced length metric','finite n ≥ 2 and N ≥ 1',
            '(1 − t²)/(1 + t²)','strong deformation retraction','strict L < 1/2','nonsmooth',
            'angular distance π','any topological parameter space','constant Q,R',
            'one prescribed point','classical Cayley','priority'],
'23320818':['natural static','retains the entire boundary sphere','contravariant vector fields',
            'normal boundary trace may be nonzero','complete scalar contraction','every test',
            '−(2/a²)','−8π','A,B ≥ 0 with A + B > 0','exactly when A = 0','B = 0',
            'null energy condition','tilted','collapsing','classical','O((ρ − a)^(−5+κ))']}

def semantic_guard(rid,public):
    text=public
    for phrase in GUARDS[rid]:require(phrase.casefold() in text.casefold(),'lost scope guard '+rid+': '+phrase)


def main():
    out=[];negative=0;manifest_entries=0;native_compares=0;literal_verdicts=0;fidelity_falsifiers=0
    for rid in IDS:
        B=P/'papers'/rid;E=B/'reviews/editorial';pub=read(B/'publication.json');pro=read(B/'promotion.json');binding=pub['source_binding']
        public=(E/'PUBLIC_COPY.md').read_text();rootpath=P/pro['root_clearance_file'];root=read(rootpath)
        require(sha(rootpath)==pro['root_clearance_sha256'],'exact root authority')
        rootcopy=pro.get('whole_root_scientific_clearance_record',pro.get('root_clearance_record'))
        require(same(rootcopy,root),'whole root object/types/order preserved')
        for lane,entry in pro['reviews'].items():
            path=entry.get('verdict_path',entry.get('verdict_file'))
            vf=resolved(path,B);actual=read(vf)
            saved=entry.get('whole_original_custom_verdict',entry.get('verdict_original',entry.get('verdict')))
            require(sha(vf)==entry['verdict_sha256'] and same(saved,actual),'whole literal custom verdict '+rid+lane)
            if 'root_authority_entry' in entry:
                require(same(entry['root_authority_entry'],root['reviews'][lane]),'whole original root family entry')
            if 'root_clearance_review_object' in entry:
                require(same(entry['root_clearance_review_object'],root['reviews'][lane]),'whole original root family entry')
            literal_verdicts+=1
        require(pro['publication_sha256']==sha(B/'publication.json'),'promotion exact publication binding')
        source=read(B/'sources/SOURCE_READY.json')
        readycopy=binding.get('whole_original_source_ready',binding.get('source_receipt_original'))
        require(same(readycopy,source),'whole mixed readiness schema '+rid);native_compares+=1
        # Every distinct native transport schema is compared against its actual file, without coercion.
        if 'transport_receipt_original' in binding:
            require(same(binding['transport_receipt_original'],read(B/binding['transport_receipt_path'])),'native transport list')
            native_compares+=1
        elif rid in ['23383952','23539734']:
            field='whole_native_transport_receipts' if rid=='23383952' else 'whole_original_native_transport_receipts'
            require(same(binding[field],read(B/'sources/api-receipts.json')),'actual API receipt list');native_compares+=1
        elif rid=='22929857':
            for field,path in [('whole_native_acquisition_transport_receipt','sources/acquisition.transport.json'),
                               ('whole_native_record_transport_receipt','sources/record.transport.json')]:
                require(same(binding[field],read(B/path)),'distinct actual native transport object');native_compares+=1
        elif rid=='23320818':
            for path,obj in zip(binding['transport_receipt_paths'],binding['whole_native_transport_objects']):
                # This actual packet wraps each literal object with path/hash; inspect that wrapper faithfully.
                if isinstance(obj,dict) and 'object' in obj:literal=obj['object']
                elif isinstance(obj,dict) and 'original' in obj:literal=obj['original']
                else:literal=obj
                require(same(literal,read(B/path)),'heterogeneous original transport '+path);native_compares+=1
        if 'whole_native_record' in binding:
            require(same(binding['whole_native_record'],read(B/'sources/record.raw.json')),'whole native record');native_compares+=1
        raw=read(B/'sources/record.raw.json')
        wrong=copy.deepcopy(root);wrong['status']='PASS'
        require(not same(wrong,root),'generic status substitution must differ');fidelity_falsifiers+=1
        wrong=copy.deepcopy(source)
        array=next(k for k in ['assets','all_assets_in_original_order','all_native_assets_in_original_order'] if k in wrong)
        wrong[array].reverse();require(not same(wrong,source),'native asset reversal must differ');fidelity_falsifiers+=1
        require(raw['swh']=={},'actual empty native object')
        wrong=copy.deepcopy(raw);wrong['swh']=None
        require(not same(wrong,raw),'native empty/null collapse must differ');fidelity_falsifiers+=1
        native_transport=binding.get('transport_receipt_original',binding.get('whole_native_transport_receipts',
                         binding.get('whole_original_native_transport_receipts',binding.get('whole_native_acquisition_transport_receipt',
                         binding.get('whole_native_transport_objects')))))
        wrong=copy.deepcopy(native_transport);require(change_first_headers(wrong),'actual native headers found')
        require(not same(wrong,native_transport),'opaque header deletion must differ');fidelity_falsifiers+=1
        require(pub['doi']==raw['doi'] and pub['version']==raw['metadata']['version']
                and pub['publication_date']==raw['metadata']['publication_date'],'DOI/version/declared date')
        require(pub['license']=='CC BY 4.0' and raw['metadata']['license']['id']=='cc-by-4.0','actual license')
        require(pub.get('code_license')==('MIT' if rid=='22929857' else 'CC BY 4.0')
                if rid in ['22929857','23539734'] else True,'separate exact code rights')
        texpath=B/binding['source_tex_path'];require(sha(texpath)==binding['source_tex_sha256'],'actual controlling TeX')
        tex=texpath.read_text();abstract=tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
        require(abstract.strip()==binding['abstract_tex'].strip(),'complete source abstract; outer whitespace only')
        require(normalize_abstract(abstract,binding,rid)==pub['abstract'],'no omitted abstract words')
        require(pub['abstract'] in public and 'Original abstract' in public,'whole indexable abstract draft')
        require(pub['follow_up'] is None and pro['follow_up'] is None,'follow-up null')
        require(pub['canonical_url'] is None and pro['canonical_url'] is None and pro['AA'] is None,'canonical/AA null')
        for obj in [pro,pub.get('review_metadata',{})]:
            for key in ['rendered','deployed','publication_clearance','ready_to_publish','browser_verified','native_verified',
                        'public_page_published','root_editorial_clearance_received','production_integration_authorized']:
                if key in obj:require(obj[key] is False,'premature gate '+rid+': '+key)
        require('extensive' in pub['ai_disclosure'].lower() and 'unrefereed' in pub['ai_disclosure'].lower()
                and 'human' in pub['ai_disclosure'].lower() and 'formal' in pub['ai_disclosure'].lower(),'concise truthful AI/status')
        require('contribution' in pub['collaboration'].lower() and 'agreement' in pub['collaboration'].lower(),'passive contribution collaboration')
        for asset in raw['files']:
            f=B/'sources'/asset['key'];algo,wanted=asset['checksum'].split(':',1)
            require(f.is_file() and f.stat().st_size==asset['size'] and hashlib.new(algo,f.read_bytes()).hexdigest()==wanted,'unchanged whole native asset')
        for assetkey,hashkey in [('pdf_filename','pdf_sha256'),('supplement_filename','supplement_sha256')]:
            require(sha(B/'sources'/pub[assetkey])==binding[hashkey],'exact public full asset binding')
        for item in pub['related_resources']:
            u=urlparse(item['url']);require(u.scheme=='https' and u.netloc=='zenodo.org' and rid in u.path,'correct original Zenodo link')
        for title,url in re.findall(r'\[([^\]]+)\]\(([^\s)]+)\)',public):
            if url.startswith(('http://','https://')):require(url.startswith('https://'),'public HTTPS link')
            if url.endswith('.pdf') and not url.startswith('http'):require(Path(url).name==pub['pdf_filename'],'local PDF filename')
            if url.endswith('.zip') and not url.startswith('http'):require(Path(url).name==pub['supplement_filename'],'local complete ZIP filename')
        require(pub['doi'] in public,'actual citation DOI')
        semantic_guard(rid,public)
        # Each omission is an in-memory false draft, not an edit of the actual file.
        for phrase in GUARDS[rid][:3]:
            mutated=re.sub(re.escape(phrase),'[OMITTED]',public,flags=re.I)
            try:semantic_guard(rid,mutated)
            except RuntimeError:negative+=1
            else:raise RuntimeError('scope omission not rejected')
        # Actual sealed manifests are authenticated directly; no existing verifier or scientific campaign runs.
        seal=read(E/'SEAL.json');mp=E/'MANIFEST.json';m=read(mp)
        require(sha(mp)==seal['manifest_sha256'],'existing editorial manifest seal')
        entries=m.get('files',m.get('owned_files'))
        for entry in entries:checkentry(entry,E);manifest_entries+=1
        out.append({'record_id':rid,'title':pub['title'],'root_status':root['status'],'full_abstract_verified':True,
                    'public_scope_guards':len(GUARDS[rid]),'native_schema_fidelity':True,'native_assets':len(raw['files']),
                    'editorial_seal_sha256':sha(E/'SEAL.json'),'public_copy_sha256':sha(E/'PUBLIC_COPY.md'),
                    'publication_sha256':sha(B/'publication.json'),'promotion_sha256':sha(B/'promotion.json'),
                    'audit_independence':'adversarial self-audit; same agent authored110 editorial' if rid=='23539734' else 'independent of editorial author',
                    'live_HTTP_or_UI_verification':False,'publication_authority':False})
    for e in read(A/'PROTECTED_INPUTS.json')['files']:checkentry(e,P)
    # Four tiny exact boundary diagnostics; these do not replay any proof campaign.
    h=(5,4,3,2,1,1,2,3,4,5);hh=h+h
    require(len(hh)==20 and len({hh[i:]+hh[:i] for i in range(20)})==10,'literal20-word rotation sanity')
    require(Q(13,20)-Q(321,500)==Q(1,125) and Q(1106714561,1700054750)>Q(13,20),'finite Yamabe gap')
    points=[(u,v) for u in range(3) for v in range(3)]
    periods=[]
    for u,v in points:
        cur=(u,v);n=0
        while True:
            cur=(cur[0],((cur[0]**2+1)*cur[1])%3);n+=1
            if cur==(u,v):break
            require(n<=9,'toy orbit bound')
        periods.append(n)
    require(Q(sum(2*t<=3 for t in periods),9)==Q(5,9)
            and Q(sum(4*t<=9 for t in periods),9)==1,'fixed-x cutoff witness atp3')
    require(-16*Q(1,2)==-8 and -16*Q(0)==0,'affine-lapse radial flux coefficients')
    print(json.dumps({'status':'PASS_SIX_PRIVATE_EDITORIAL_SOURCE_SCOPE_AUDIT_WITH_DISCLOSED_SELF_AUDIT110',
                      'records':out,'scope_omission_falsifiers_rejected':negative,
                      'whole_literal_custom_verdicts_verified':literal_verdicts,
                      'native_authority_fidelity_falsifiers_rejected':fidelity_falsifiers,
                      'literal_native_schema_comparisons':native_compares,'existing_manifest_entries_verified':manifest_entries,
                      'small_exact_boundary_diagnostics':4,'supplied_or_existing_programs_executed':False,
                      'file_writes':False,'publication_authority':False},ensure_ascii=False,sort_keys=True))

if __name__=='__main__':main()
