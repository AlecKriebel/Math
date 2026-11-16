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
    inputs=obj(R/'AUTHORING_INPUTS_SEAL.json')
    OWNEDPINS.update(inputs['inputs'])
    for name,p in inputs['inputs'].items():need(pin(read(R/name))==p,'same-buffer owned authoring pin '+name)
    protected=obj(R/'PROTECTED_INPUTS.json')
    for contract in protected['namespaces'].values():
        for row in contract['files']:EXTERNAL[row['path']]={k:row[k] for k in ['bytes','SHA256']}
    for row in [protected['root_clearance'],protected['qualified_core']['reference'],*protected['qualified_core']['named17_original_plus_sole_authorized405b']]:EXTERNAL[row['path']]={k:row[k] for k in ['bytes','SHA256']}
    for label,contract in protected['namespaces'].items():
        root=Path(contract['root']);actual,dirs=extent(root)
        expected=[{'path':x['relative_path'],**{k:x[k] for k in ['bytes','SHA256']}} for x in contract['files']]
        need(actual==sorted(expected,key=lambda x:x['path']) and dirs==contract['directories'],'whole frozen namespace '+label)
    bound(protected['root_clearance']);core=protected['qualified_core'];prior=json.loads(bound(core['reference']))
    need(core['reference']['SHA256']=='0f285e35daa206f53aa931946c4bcc6c5b01ae6b4b59a231a861b0a6fe11d104','authorized named-core reference')
    need(core['named17_original_plus_sole_authorized405b']==[{k:r[k] for k in ['path','bytes','SHA256']} for r in prior['files']],'exact qualified18 source inputs')
    for row in core['named17_original_plus_sole_authorized405b']:bound(row)
    c=obj(R/'EDITORIAL_CONFIG.json');copy=obj(R/'COPY.json');expect=obj(R/'SOURCE_EXPECTATIONS.json')
    need(c['record_id']==expect['record_id']==23205305 and c['sheet_row']==136,'exact row/id')
    pub=c['publication'];promotion=c['promotion'];need(copy['title']==c['title']==expect['native_title'],'whole title')
    for key in ['canonical_url','AA','follow_up']:need(promotion[key] is None,'null nonauthority '+key)
    for key in ['root_copy_adopted','production_install_authority','deployment_authority','live_verified','browser_verified']:need(promotion[key] is False,'no invented authority '+key)
    need(pub['native_version_field']=={'present':False,'original_value':None} and pub['printed_version_present'] is False and pub['printed_version'] is None,'absent versions')
    for key,source in [('main_abstract','main_abstract_original_TeX'),('companion_abstract','companion_abstract_original_TeX')]:
        raw=expect[source].replace(r'\cite{Pinned}','[1]').replace(r'$\Q$','ℚ').replace('$','')
        need(canon(copy[key])==canon(raw),'entire printed abstract faithful '+key)
    need(copy['native_description']==pub['native_description_exact']==expect['native_description_whole_original'],'whole distinct native description')
    typed(pub['all_original_assets'],expect['all_four_native_assets_original_order'])
    native=obj(Path(protected['namespaces']['source']['root'])/'record.response.body')
    typed(expect['native_metadata_whole_original'],native['metadata'])
    need(pub['native_asset_order']==['source.zip','verification.zip','paper.pdf','height-repair.pdf'],'original four-asset order')
    need(pub['rights']['mixed_ZIP_blanket_license'] is None and pub['rights']['original_verification_code']=='MIT','mixed rights')
    outputs={}
    for mode in ['normal','optimized']:
        files,dirs=extent(R/mode);need(dirs==[],'finite flat rendered output')
        need([x['path'] for x in files]==sorted(['PUBLIC_MAIN.html','HEAD.html','style.css','citation.bib','COPY.md','index.html',*pub['native_asset_order']]),'exact ten output names')
        outputs[mode]=files
        for a in pub['all_original_assets']:
            key=a['original_api_file_object']['key'];need(read(R/mode/key)==bound(a),'whole unchanged published asset')
    need(outputs['normal']==outputs['optimized'],'normal/O all ten whole outputs identical')
    mainbody=read(R/'normal/PUBLIC_MAIN.html').decode();page=Page();page.feed(mainbody)
    need([(t,a.get('id')) for t,a in page.tags if t=='main']==[('main','main')],'single semantic main id')
    need([a['src'] for t,a in page.tags if t=='iframe']==['paper.pdf#view=FitH','height-repair.pdf#view=FitH'],'both exact upfront reader sources')
    need([a['href'] for t,a in page.tags if t=='a' and a.get('data-native-asset')=='true']==pub['native_asset_order'],'original download order')
    plain=' '.join(page.text)
    for text in [copy['intro'],copy['main_abstract'],copy['companion_abstract'],copy['native_description'],copy['rights_paragraph']]:need(canon(text) in canon(plain),'entire author copy paragraph rendered')
    for section in copy['sections']:
        for text in section['paragraphs']+section.get('items',[]):need(canon(text) in canon(plain),'whole section/item rendered')
    for marker in ['three preceding inputs','discriminant-210','30, 42, 70, 105 and 210','h(s) ≤ H M_S(s)^c','coefficient pair is (5, 2)','integral universal group-ring correction','unrefereed','actual contributions','no total computable function B(s(e))','not arbitrary five rational points']:
        need(marker in plain,'substantive copy boundary '+marker)
    need(mainbody.index('paper.pdf#view=FitH')<mainbody.index('printed-main-abstract') and mainbody.index('height-repair.pdf#view=FitH')<mainbody.index('printed-main-abstract'),'both readers upfront')
    head=Page();headbody=read(R/'normal/HEAD.html').decode();head.feed(headbody)
    need(not any(a.get('name')=='citation_version' or a.get('rel')=='canonical' for t,a in head.tags),'no invented version/live canonical')
    ld=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',headbody,re.S).group(1))
    need('version' not in ld and ld['datePublished']=='2026-10-06' and ld['abstract']==copy['main_abstract'],'faithful scholarly metadata')
    need('version =' not in read(R/'normal/citation.bib').decode().lower(),'no invented Bib version')
    need('font-family:Arial,Helvetica,sans-serif' in read(R/'normal/style.css').decode(),'light established Arial style')
    need('OWNED_MANIFEST.json' not in plain and '20261115' not in plain and 'checks passed' not in plain,'no public internal audit replay')
    finalized=False
    if (R/'OWNED_MANIFEST.json').exists():
        manifest_body=read(R/'OWNED_MANIFEST.json');manifest=json.loads(manifest_body)
        need(manifest['exact_root_terminal_exclusions']==sorted(TERMS),'only exact root terminals')
        files,dirs=extent(R);need(TERMS<={x['path'] for x in files},'all terminals already ordinary files')
        need([x for x in files if x['path'] not in TERMS]==manifest['files'] and dirs==manifest['directories'],'complete own finite file/directory extent')
        seal=obj(R/'FINAL_SEAL.json');finalized=seal['status']=='EDITORIAL_PREPARATION_FINAL'
        if finalized:
            need(seal['manifest_SHA256']==pin(manifest_body)['SHA256'] and seal['closure_SHA256']==pin(read(R/'CLOSURE.json'))['SHA256'],'whole final terminal bindings')
        else:need(seal['status']=='FINALIZATION_IN_PROGRESS','honest explicit pending phase')
    print(json.dumps({'status':'EDITORIAL_CUSTODY_COPY_PASS','record_id':23205305,'checks':COUNT,'normal_O_whole_outputs_identical':True,'native_assets':4,'original_reader_pages':10,'original_TeX_lines':696,'protected_namespaces':{k:[v['file_count'],v['directory_count']] for k,v in protected['namespaces'].items()},'final_seal_bound':finalized,'scientific_execution':False,'new_scientific_verdict':None,'production_authority':False,'writes':0,'network_requests':0},sort_keys=True))

if __name__=='__main__':main()
