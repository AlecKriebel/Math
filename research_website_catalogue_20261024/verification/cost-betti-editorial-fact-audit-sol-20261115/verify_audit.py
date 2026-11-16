"""Pure fact-audit custody and independent exact abstract/native comparisons.
Stdlib reads only. No project imports, subprocess, network, science or writes.
"""
import hashlib
import html
import json
import os
from pathlib import Path
import re
import stat
import sys

N=Path(__file__).absolute().parent
P=N.parent.parent
E=P/'papers/23203732/reviews/editorial'
TERMINALS={'FINAL_SEAL.json','OWNED_MANIFEST.json'}
COUNT=0

def need(ok,why):
    global COUNT
    COUNT+=1
    if not ok:raise ValueError(why)

def sha(b):return hashlib.sha256(b).hexdigest()

def read(p):
    need(p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary real input '+str(p));return p.read_bytes()

def pin(p,d):
    b=read(p);need(len(b)==d['bytes'] and sha(b)==d['SHA256'],'whole body pin '+str(p));return b

def extent(root):
    need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary root')
    files,dirs=[],[]
    def walk(d):
        with os.scandir(d) as rows:
            for v in rows:
                q=Path(v.path);r=q.relative_to(root).as_posix();m=q.lstat().st_mode
                if stat.S_ISDIR(m):dirs.append(r);walk(q)
                else:need(stat.S_ISREG(m),'reject link/special');files.append(r)
    walk(root);return sorted(files),sorted(dirs)

def typed(a,b):
    need(type(a) is type(b),'exact JSON type')
    if type(a) is dict:
        need(list(a)==list(b),'exact native key order')
        for k in a:typed(a[k],b[k])
    elif type(a) is list:
        need(len(a)==len(b),'exact native list length')
        for x,y in zip(a,b):typed(x,y)
    else:need(a==b,'exact native scalar')

def normalized(s):return ' '.join(s.replace('’',"'").split())

def main():
    need(sys.argv[1:]==[],'only default pure custody')
    ib=read(N/'INITIAL_SEAL.json');need(sha(ib)=='1f460b47fb1a8a2488cd95a36b8cd04af087afebc80a0d866f1e2bf0fcbb4b5e','own source-only initial predates copy exposure');initial=json.loads(ib)
    source=json.loads(pin(N/'SOURCE_INPUTS.json',initial['SOURCE_INPUTS']))
    pin(N/'INITIAL_EXPECTATIONS.md',initial['INITIAL_EXPECTATIONS'])
    reading=json.loads(pin(N/'INITIAL_READ_RECEIPT.json',initial['INITIAL_READ_RECEIPT']))
    for name,d in reading['owned_read_inputs'].items():pin(N/name,d)
    need(initial['current_editorial_copy_or_results_exposed'] is False and len(source['files'])==555,'literal informed initial boundary')
    for d in source['files']:pin(Path(d['path']),d)
    for ns in source['namespaces']:need(extent(Path(ns['path']))==(ns['files'],ns['directories']),'whole frozen namespace '+ns['kind'])
    for k in ('core_contract_reference','prior_authenticated_oracle_reference'):pin(Path(source[k]['path']),source[k])
    need(sum(x['classification']=='one of17 original core files' for x in source['core_files'])==17 and sum(x['classification']=='sole separately authorized405b helper' for x in source['core_files'])==1,'17original plus sole405b distinction')
    r=json.loads(read(N/'WRITER_REFERENCE.json'));sb=pin(E/'FINAL_SEAL.json',r['seal']);s=json.loads(sb)
    need(sha(sb)=='8cf157403919b0d98b228dd80dae2f77e09fe5ff63cb361c63299cf4bf9e5193','exact current writer FINAL')
    mb=pin(E/'OWNED_MANIFEST.json',r['manifest']);need(sha(mb)==s['manifest_SHA256'],'same-buffer writer manifest authentication');m=json.loads(mb)
    need(extent(E)==(sorted(Path(x['path']).relative_to(E).as_posix() for x in r['files']),r['directories']),'all60 writer files and4dirs')
    need(len(r['files'])==60 and len(r['directories'])==4,'literal complete writer extent')
    for d in r['files']:pin(Path(d['path']),d)
    for d in m['files']:pin(E/d['path'],d)
    need(sha(read(E/'CLOSURE.json'))==s['closure_SHA256'],'whole writer closure binding')
    need(sum(x['bytes'] for x in r['whole_actual_current_code_read'])==26917,'whole current3body read extent')
    for d in r['whole_actual_current_code_read']:pin(Path(d['path']),d)
    c=json.loads(read(E/'EDITORIAL_CONFIG.json'));copy=json.loads(read(E/'COPY.json'));pub=c['publication']
    native=json.loads(read(P/'papers/23203732/sources/record.response.body'))
    ready=json.loads(read(P/'papers/23203732/sources/SOURCE_READY.json'))
    tex=read(P/'papers/23203732/sources/published-source/asset-002/main.tex').decode()
    original=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',tex,re.S).group(1)
    for old,new in [('$L^2$','L²'),(r'$\beta_n^{(2)}(\Gamma)=0$','βₙ⁽²⁾(Γ) = 0'),(r'$n\geq0$','n ≥ 0'),(r'$1+(100\cdot2^{61})^{-1}$','1 + (100·2⁶¹)⁻¹'),('cost--Betti','cost–Betti')]:original=original.replace(old,new)
    need(normalized(original)==normalized(copy['printed_abstract'])==normalized(pub['full_printed_abstract_readable_math']),'independent full actual TeX abstract transcription')
    typed(copy['native_description_HTML'],native['metadata']['description']);typed(pub['native_description_HTML_exact'],native['metadata']['description'])
    typed(pub['all_original_assets'],ready['all_native_assets_in_original_order'])
    need('version' not in native['metadata'] and pub['native_version_field']=={'present':False,'original_value':None} and pub['printed_version_present'] is False and pub['printed_version'] is None,'native/printed version absent')
    need(pub['datePublished']==native['metadata']['publication_date']=='2026-10-06' and pub['native_created_separate']==native['created'] and native['created'].startswith('2026-10-07'),'publication/created date distinction')
    need(pub['native_asset_order']==[a['key'] for a in native['files']]==['paper.pdf','cost-betti-source-and-verification.zip'],'complete original native order')
    for name in ['COPY.md','PUBLIC_MAIN.html','HEAD.html','index.html','style.css','citation.bib',*pub['native_asset_order']]:need(read(E/'normal'/name)==read(E/'optimized'/name),'paired whole output '+name)
    for a in ready['all_native_assets_in_original_order']:need(read(E/'normal'/a['original_api_file_object']['key'])==pin(Path(a['path']),a),'unchanged complete native asset')
    mainbody=read(E/'normal/PUBLIC_MAIN.html').decode();head=read(E/'normal/HEAD.html').decode();full=read(E/'normal/index.html')
    need(full==('<!doctype html>\n<html lang="en">\n<head>\n'+head+'</head>\n<body>\n'+mainbody+'</body>\n</html>\n').encode(),'complete head/main/ending composition')
    need('<main id="main">' in mainbody and 'paper.pdf#view=FitH' in mainbody and mainbody.index('paper.pdf#view=FitH')<mainbody.index('printed-abstract'),'semantic main/upfront original FitH reader')
    need(html.escape(copy['printed_abstract'],quote=True) in mainbody and copy['native_description_HTML'] in mainbody,'separate whole visible printed/native abstracts')
    ld=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',head,re.S).group(1));typed(ld['abstract'],copy['printed_abstract'])
    need('name="DC.description" content="'+html.escape(copy['printed_abstract'],quote=True)+'"' in head,'whole abstract in actual scholarly head')
    need('version' not in ld and 'citation_version' not in head and 'version =' not in read(E/'normal/citation.bib').decode().lower(),'no invented metadata edition')
    need(pub['rights']['original_note_code_and_audit_text']=='CC-BY-4.0' and pub['rights']['MIT_instrument'] is False and 'third-party works retain their respective rights' in copy['rights_paragraph'],'supported authored-code rights only')
    promotion=c['promotion']
    for key in ['root_copy_adopted','production_install_authority','deployment_authority','native_tracker_mutation_authority','live_verified','browser_verified']:need(promotion[key] is False,'current proposal authority false '+key)
    for key in ['canonical_url','AA','follow_up']:need(promotion[key] is None,'current null '+key)
    need(promotion['robots']=='noindex,nofollow,noarchive','private preview only')
    owner=json.loads(read(N/'OWNER_DEFAULT.stdout'));need(owner['checks']==10352 and owner['status']=='EDITORIAL_CUSTODY_COPY_PASS' and owner['final_seal_bound'] is True and read(N/'OWNER_DEFAULT.stderr')==b'','actual sole safe owner closure')
    sealed=(N/'FINAL_SEAL.json').exists()
    if sealed:
        ss=json.loads(read(N/'FINAL_SEAL.json'));mm=pin(N/'OWNED_MANIFEST.json',ss['manifest']);own=json.loads(mm)
        need(extent(N)==(sorted([*own['files'],*TERMINALS]),own['directories']),'exact audit ordinary-file AND directory closure; only2root terminals')
        for name,d in own['files'].items():pin(N/name,d)
    print(json.dumps({'status':'PASS_MINIMAL_INFORMED_EDITORIAL_CUSTODY_AND_ABSTRACT','checks':COUNT,'sealed':sealed,'source_root_core_files':555,'frozen_original_namespaces':5,'writer_files':60,'writer_current_code_bodies':3,'writer_current_code_bytes':26917,'actual_owner_default_checks':10352,'entire_printed_abstract_and_native_description_match':True,'native_assets_unchanged':2,'scientific_execution':False,'network_or_subprocess_or_writes':False,'root_copy_adoption':False,'production_authority':False},sort_keys=True))

if __name__=='__main__':main()
