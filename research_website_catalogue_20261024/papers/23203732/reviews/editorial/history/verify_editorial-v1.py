#!/usr/bin/env python3
"""One-record, read-only custody/copy guard. No network, imports or execution
of project/scientific code, no subprocess and no filesystem writes.
Reads only this owned packet and the exact protected original input paths.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,os,re,stat,sys

R=Path(__file__).absolute().parent
TERMS={'OWNED_MANIFEST.json','CLOSURE.json','FINAL_SEAL.json'}
COUNT=0
OWNEDPINS={}
EXTERNAL={}
def need(ok,why):
    global COUNT
    COUNT+=1
    if not ok:raise ValueError(why)
def pin(b):return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}
def read(p):
    p=Path(p);need(p.is_relative_to(R) or str(p) in EXTERNAL,'explicit pinned input scope');a=p.lstat();need(stat.S_ISREG(a.st_mode),'regular '+str(p))
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        before=os.fstat(fd);need((a.st_dev,a.st_ino)==(before.st_dev,before.st_ino),'held identity')
        chunks=[]
        while True:
            b=os.read(fd,1048576)
            if not b:break
            chunks.append(b)
        after=os.fstat(fd);last=p.lstat()
        need((before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns),'stable held input')
        need((last.st_dev,last.st_ino)==(before.st_dev,before.st_ino),'pathname identity')
        b=b''.join(chunks);need(len(b)==before.st_size,'complete read')
        expected=OWNEDPINS.get(p.relative_to(R).as_posix()) if p.is_relative_to(R) else EXTERNAL[str(p)]
        if expected is not None:need(pin(b)==expected,'same-buffer input authentication')
        return b
    finally:os.close(fd)
def obj(p):return json.loads(read(p))
def bound(row):
    b=read(Path(row['path']));need(pin(b)=={k:row[k] for k in ['bytes','SHA256']},'whole pinned original '+row['path']);return b
def extent(root):
    files=[];dirs=[]
    def visit(d):
        before=d.lstat();need(stat.S_ISDIR(before.st_mode),'ordinary directory')
        for p in sorted(d.iterdir()):
            mode=p.lstat().st_mode;rel=p.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):dirs.append(rel);visit(p)
            elif stat.S_ISREG(mode):files.append({'path':rel,**pin(read(p))})
            else:raise ValueError('symlink/FIFO/special '+str(p))
        after=d.lstat();need((before.st_dev,before.st_ino,before.st_mtime_ns,before.st_ctime_ns)==(after.st_dev,after.st_ino,after.st_mtime_ns,after.st_ctime_ns),'stable directory extent')
    visit(root);return sorted(files,key=lambda x:x['path']),sorted(dirs)
class Page(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.tags=[];self.text=[]
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
    def handle_data(self,data):self.text.append(data)
def canon(t):return ' '.join(t.replace('’',"'").split())
def typed(a,b):
    need(type(a) is type(b),'literal type')
    if type(a) is dict:
        need(list(a)==list(b),'literal key order')
        for k in a:typed(a[k],b[k])
    elif type(a) is list:
        need(len(a)==len(b),'literal list length')
        for x,y in zip(a,b):typed(x,y)
    else:need(a==b,'literal value')
def main():
    need(sys.argv[1:]==[],'only designated default closure')
    inputs=obj(R/'AUTHORING_INPUTS_SEAL.json');OWNEDPINS.update(inputs['inputs'])
    for name,p in inputs['inputs'].items():need(pin(read(R/name))==p,'same-buffer authoring input '+name)
    protected=obj(R/'PROTECTED_INPUTS.json')
    for contract in protected['namespaces'].values():
        for row in contract['files']:EXTERNAL[row['path']]={k:row[k] for k in ['bytes','SHA256']}
    root_authority=protected['root_clearance_opaque_only_before_INITIAL'];core=protected['qualified_core']
    for row in [root_authority,core['reference'],*core['named17_original_plus_sole_authorized405b']]:EXTERNAL[row['path']]={k:row[k] for k in ['bytes','SHA256']}
    for label,contract in protected['namespaces'].items():
        actual,dirs=extent(Path(contract['root']));expected=[{'path':r['relative_path'],**{k:r[k] for k in ['bytes','SHA256']}} for r in contract['files']]
        typed(actual,sorted(expected,key=lambda r:r['path']));typed(dirs,contract['directories'])
    need(root_authority['SHA256']=='1bfac7edfb5ae34ba7c5c4d4078c025ee25bfc299d91c547702b15eca462eb09','actual frozen root authority')
    clearance=json.loads(bound(root_authority));need(clearance['record_id']==23203732 and clearance['status']=='PASS_FULL_ORIGINAL_SCIENTIFIC_CLAIM','actual root science clearance only')
    prior=json.loads(bound(core['reference']));need(core['reference']['SHA256']=='0f285e35daa206f53aa931946c4bcc6c5b01ae6b4b59a231a861b0a6fe11d104','qualified reference')
    typed(core['named17_original_plus_sole_authorized405b'],[{k:r[k] for k in ['path','bytes','SHA256']} for r in prior['files']])
    for row in core['named17_original_plus_sole_authorized405b']:bound(row)
    c=obj(R/'EDITORIAL_CONFIG.json');copy=obj(R/'COPY.json');expect=obj(R/'SOURCE_EXPECTATIONS.json');pub=c['publication'];promotion=c['promotion']
    need(c['record_id']==expect['record_id']==23203732 and c['sheet_row']==137,'exact record/row')
    need(c['title']==expect['native_title'] and copy['title']==c['display_title']==expect['display_title'],'native and printed title distinction')
    for k in ['canonical_url','AA','follow_up']:need(promotion[k] is None,'non-authority null '+k)
    for k in ['root_copy_adopted','production_install_authority','deployment_authority','native_tracker_mutation_authority','live_verified','browser_verified']:need(promotion[k] is False,'no invented authority '+k)
    native=obj(Path(protected['namespaces']['source']['root'])/'record.response.body');typed(expect['native_metadata_original_whole'],native['metadata'])
    typed(pub['all_original_assets'],expect['all_native_assets_whole_original_order'])
    typed(pub['native_version_field'],{'present':False,'original_value':None});need(pub['printed_version_present'] is False and pub['printed_version'] is None,'printed version absent')
    need(pub['datePublished']==expect['printed_and_declared_date']=='2026-10-06' and pub['native_created_separate']==native['created'],'declared/created distinction')
    raw=expect['printed_abstract_original_TeX_whole']
    substitutions=[('$L^2$','L²'),(r'$\betti n(\Gamma)=0$','βₙ⁽²⁾(Γ) = 0'),(r'$n\geq0$','n ≥ 0'),(r'$1+(100\cdot2^{61})^{-1}$','1 + (100·2⁶¹)⁻¹'),('cost--Betti','cost–Betti')]
    for old,new in substitutions:raw=raw.replace(old,new)
    need(canon(raw)==canon(expect['printed_abstract_readable_math_whole'])==canon(copy['printed_abstract']),'entire printed abstract mathematical transcription')
    typed(copy['printed_abstract'],pub['full_printed_abstract_readable_math'])
    typed(copy['native_description_HTML'],expect['native_description_HTML_original_whole']);typed(copy['native_description_HTML'],pub['native_description_HTML_exact'])
    need(pub['rights']['original_note_code_and_audit_text']=='CC-BY-4.0' and pub['rights']['MIT_instrument'] is False,'broad original CC BY code rights')
    need(pub['native_asset_order']==['paper.pdf','cost-betti-source-and-verification.zip'],'native order')
    outputs={}
    for mode in ['normal','optimized']:
        files,dirs=extent(R/mode);need(dirs==[],'flat bounded output')
        need([x['path'] for x in files]==sorted(['PUBLIC_MAIN.html','HEAD.html','style.css','citation.bib','COPY.md','index.html',*pub['native_asset_order']]),'exact eight outputs')
        outputs[mode]=files
        for a in pub['all_original_assets']:need(read(R/mode/a['original_api_file_object']['key'])==bound(a),'byte-identical native asset')
    typed(outputs['normal'],outputs['optimized'])
    mainbody=read(R/'normal/PUBLIC_MAIN.html').decode();page=Page();page.feed(mainbody);plain=' '.join(page.text)
    need([(t,a.get('id')) for t,a in page.tags if t=='main']==[('main','main')],'one semantic main idmain')
    need([a['src'] for t,a in page.tags if t=='iframe']==['paper.pdf#view=FitH'],'original upfront reader')
    need([a['href'] for t,a in page.tags if t=='a' and a.get('data-native-asset')=='true']==pub['native_asset_order'],'original download order')
    need(mainbody.index('paper.pdf#view=FitH')<mainbody.index('printed-abstract'),'upfront reader')
    for text in [copy['intro'],copy['printed_abstract'],copy['rights_paragraph']]:need(canon(text) in canon(plain),'whole authored paragraph')
    for sec in copy['sections']:
        for text in sec['paragraphs']:need(canon(text) in canon(plain),'whole scoped prose paragraph')
    need(copy['native_description_HTML'] in mainbody,'whole original native HTML separately rendered')
    for marker in ['101 generators and 100 relators','finite two-dimensional K(Γ, 1)','for every n ≥ 0','every essentially free','1 + 1/(100·2⁶¹)','M > 100','Cost_*(Γ) = 1','does not assert that any action attains cost one','use neither cost bound','substantial Bernoulli cost theorem','Gaboriau','first arXiv version from 2018','intermediate record','actual contributions','unrefereed']:
        if marker=='unrefereed':need('not undergone conventional human peer review or refereeing' in plain,'unrefereed status')
        else:need(marker in plain,'substantive copy boundary '+marker)
    need('MIT' not in plain and '20261115' not in plain and 'checks passed' not in plain,'no invented rights/internal audit replay')
    headbody=read(R/'normal/HEAD.html').decode();head=Page();head.feed(headbody)
    attrs=[a for t,a in head.tags if t=='meta'];need(any(a.get('name')=='DC.description' and a.get('content')==copy['printed_abstract'] for a in attrs),'full abstract metadata')
    need(not any(a.get('name')=='citation_version' or a.get('rel')=='canonical' for t,a in head.tags),'no invented version/live canonical')
    ld=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',headbody,re.S).group(1));typed(ld['abstract'],copy['printed_abstract']);need('version' not in ld and ld['datePublished']=='2026-10-06','scholarly metadata version/date')
    need('version =' not in read(R/'normal/citation.bib').decode().lower(),'no Bib version')
    need('font-family:Arial,Helvetica,sans-serif' in read(R/'normal/style.css').decode(),'white Arial style')
    whole=b'<!doctype html>\n<html lang="en">\n<head>\n'+read(R/'normal/HEAD.html')+b'</head>\n<body>\n'+read(R/'normal/PUBLIC_MAIN.html')+b'</body>\n</html>\n'
    need(read(R/'normal/index.html')==whole,'whole head/main/ending composition')
    finalized=False
    if (R/'OWNED_MANIFEST.json').exists():
        body=read(R/'OWNED_MANIFEST.json');manifest=json.loads(body);need(manifest['exact_root_terminal_exclusions']==sorted(TERMS),'exact root terminal exclusions')
        files,dirs=extent(R);need(TERMS<={x['path'] for x in files},'all terminals already ordinary')
        typed([x for x in files if x['path'] not in TERMS],manifest['files']);typed(dirs,manifest['directories'])
        seal=obj(R/'FINAL_SEAL.json');finalized=seal['status']=='EDITORIAL_PREPARATION_FINAL'
        if finalized:need(seal['manifest_SHA256']==pin(body)['SHA256'] and seal['closure_SHA256']==pin(read(R/'CLOSURE.json'))['SHA256'],'whole terminal hash binding')
        else:need(seal['status']=='FINALIZATION_IN_PROGRESS','literal pending phase')
    print(json.dumps({'status':'EDITORIAL_CUSTODY_COPY_PASS','record_id':23203732,'checks':COUNT,'normal_O_whole_outputs_identical':True,'native_assets':2,'original_PDF_pages':6,'original_TeX_lines':198,'protected_namespaces':{k:[v['file_count'],v['directory_count']] for k,v in protected['namespaces'].items()},'final_seal_bound':finalized,'scientific_execution':False,'new_independent_scientific_verdict':None,'production_authority':False,'writes':0,'network_requests':0},sort_keys=True))
if __name__=='__main__':main()
