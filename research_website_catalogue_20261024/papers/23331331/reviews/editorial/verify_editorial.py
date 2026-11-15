#!/usr/bin/env python3
"""Default: sealed, offline, read-only custody/copy closure using stdlib only."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import stat

E=Path(__file__).absolute().parent
checks=0
typed_nodes=0

def need(ok,why):
    global checks
    checks+=1
    if not ok:
        raise ValueError(why)

def read(p):
    need(stat.S_ISREG(p.lstat().st_mode),'not ordinary file '+str(p))
    return p.read_bytes()

def pin(b):
    return {'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest()}

def scan(root):
    need(stat.S_ISDIR(root.lstat().st_mode),'not ordinary directory')
    files,dirs=[],[]
    def walk(d):
        for ent in sorted(os.scandir(d),key=lambda x:x.name):
            q=Path(ent.path);rel=q.relative_to(root).as_posix();mode=q.lstat().st_mode
            if stat.S_ISDIR(mode):
                dirs.append(rel);walk(q)
            else:
                need(stat.S_ISREG(mode),'link or special '+str(q))
                files.append({'path':rel,**pin(read(q))})
    walk(root)
    return {'root':str(root),'files':sorted(files,key=lambda x:x['path']),'directories':sorted(dirs)}

def close_namespace(root,expected):
    actual=scan(root)
    need(actual==expected,'exact files/directories/content namespace mismatch '+str(root))
    return actual

def typed(a,b,path='$'):
    global typed_nodes
    typed_nodes+=1
    need(type(a) is type(b),'type '+path)
    if isinstance(a,dict):
        need(list(a)==list(b),'key/order '+path)
        for k in a:
            typed(a[k],b[k],path+'/'+k)
    elif isinstance(a,list):
        need(len(a)==len(b),'list length '+path)
        for i,(x,y) in enumerate(zip(a,b)):
            typed(x,y,path+'/'+str(i))
    else:
        need(a==b,'value '+path)

class Doc(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids=[];self.tags=[];self.attrs=[];self.texts={};self.capture=None
    def handle_starttag(self,tag,attrs):
        d=dict(attrs);self.tags.append(tag);self.attrs.append((tag,d))
        if 'id' in d:self.ids.append(d['id'])
        if tag=='p' and d.get('id') in ('printed-abstract','native-description'):
            self.capture=d['id'];self.texts[self.capture]=''
    def handle_endtag(self,tag):
        if tag=='p':self.capture=None
    def handle_data(self,s):
        if self.capture is not None:self.texts[self.capture]+=s

def copy_gate(body):
    required=[
      'a &gt; b &gt; 0','0 &lt; λ &lt; b²','least period','Primitive self-intersecting star',
      'full tangent line','C(Q) = T(Q)/(6S(Q)),  only when S(Q) ≠ 0.',
      'v = −4eλd/(F² − e²d²), G = 2F + d|z|².',
      '+ conj(z)[2Fv + 3ed + (vd/2)|z|²]',
      '/ {3(2F + d|z|²)},       provided G ≠ 0.',
      'S(M) = S(0)(2F + d|z|²)/(2F).',
      'is not asserted to be phase invariant','|M|² = −2F/d','if and only if',
      'C(Q(M)) = M/3','simple winding-one even family','Repeating an even least-period',
      'repeating an odd primitive orbit','Reversing the trajectory',
      'signed-area centroid with multiplicity','cubic moments',
      '123539/20736','221√21930/10368','winding number three',
      'nonremovable pole at every point of that circle is not claimed',
      'k307','k306','Schwartz and Tabachnikov','Historical priority and exclusive firstness are not established',
      'AI tools were used extensively','unrefereed preprint','external human peer review',
      'professional collaborations',
      'Creative Commons Attribution 4.0 International']
    for s in required:need(s in body,'copy loss '+s)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--preseal',action='store_true',help='source/copy checks only; no final namespace assertion')
    args=ap.parse_args()
    if not args.preseal:
        seal_buffer=read(E/'FINAL_SEAL.json');seal=json.loads(seal_buffer)
        manifest_buffer=read(E/'OWNED_MANIFEST.json')
        need(pin(manifest_buffer)==seal['OWNED_MANIFEST'],'same-buffer manifest authentication')
        manifest=json.loads(manifest_buffer)
        actual=scan(E)
        terminals={'OWNED_MANIFEST.json','FINAL_SEAL.json'}
        need(terminals <= {x['path'] for x in actual['files']},'exact root terminals present')
        actual['files']=[x for x in actual['files'] if x['path'] not in terminals]
        need(actual==manifest,'closed ordinary own files and exact directories')
        need(seal['publication_authority'] is False and seal['canonical_url'] is None and seal['AA'] is None,'final authority separation')
    ib=read(E/'INPUTS_SEAL.json')
    need(pin(ib)['SHA256']=='da2d2c58e3fc723197118823e64e7d9ce1f3b46c015be176d0e3accebc55f7dc','fixed inputs seal')
    inputs_seal=json.loads(ib);sb=read(E/'SOURCE_INPUTS.json')
    need(pin(sb)==inputs_seal['SOURCE_INPUTS'],'source same-buffer hash')
    source=json.loads(sb)
    for ns in source['namespaces']:close_namespace(Path(ns['root']),ns)
    copies={}
    for row in source['original_files']:
        b=read(Path(row['path']));cb=read(E/row['copy'])
        need(pin(b)=={k:row[k] for k in ('bytes','SHA256')} and b==cb,'whole original and private copy '+row['path'])
        copies[row['path']]=b
    need(len(copies)==421,'whole original count')
    for row in source['qualified_core']:
        need(pin(read(Path(row['path'])))=={k:row[k] for k in ('bytes','SHA256')},'qualified core unchanged')
    need(sum(x['role']=='original core' for x in source['qualified_core'])==17,'17 original core')
    need(sum(x['role']=='sole authorized additive helper' for x in source['qualified_core'])==1,'one additive helper')
    P=E.parents[3];S=P/'papers/23331331/sources'
    ready=json.loads(copies[str(S/'SOURCE_READY.json')])
    authority=json.loads(copies[str(P/'verification/root-clearance-23331331-20261115.json')])
    typed(ready,source['whole_original_SOURCE_READY'])
    typed(authority,source['whole_root_authority'])
    typed(ready,authority['whole_original_SOURCE_READY'])
    for name,filename,field in [('scope','VERDICT.json','whole_literal_scope_VERDICT'),('adversarial','CUSTOM_VERDICT.json','whole_literal_adversarial_VERDICT')]:
        typed(json.loads(copies[str(P/f'papers/23331331/reviews/{name}/{filename}')]),authority[field])
    json_bodies=0
    for row in source['original_files']:
        if row['path'].startswith(str(S)+'/') and row['path'].endswith('.json'):
            typed(json.loads(copies[row['path']]),json.loads(read(E/row['copy'])))
            json_bodies+=1
    for row in ready['whole_native_API_objects']:
        b=copies[row['path']];need(pin(b)=={k:row[k] for k in ('bytes','SHA256')},'native wrapper pin')
        typed(json.loads(b),json.loads(read(E/next(x['copy'] for x in source['original_files'] if x['path']==row['path']))))
    need(json_bodies==39,'all source JSON objects')
    record=json.loads(copies[str(S/'record.response.body')])
    version=json.loads(copies[str(S/'versions-page001.response.body')])
    files=json.loads(copies[str(S/'files.response.body')])
    need(record['swh']=={} and version['hits']['hits'][0]['swh'] is None,'native empty versus null')
    need(type(files['entries']) is list and files['order']==[],'native list and empty order')
    need([x['key'] for x in record['files']]==['outer-pedal-centroid-verification.zip','outer_pedal_centroid.pdf'],'ZIP PDF native order')
    need(authority['nativeTrackerUpdatePending'] is True and source['current_context_outside_immutable_history']['parent_reported_native_science_count']==106,'historical versus contextual current native')
    cfg=json.loads(read(E/'EDITORIAL_CONFIG.json'))
    need(cfg['publication']['native_version_field']=={'present':True,'original_value':'1.0'},'native version')
    need(cfg['publication']['native_created_separate']==ready['created'] and cfg['publication']['datePublished']==ready['publication_date'],'distinct date fields')
    for k in ('production_install_authority','deployment_authority','native_tracker_mutation_authority','live_verified','browser_verified','root_editorial_copy_adopted'):
        need(cfg['promotion'][k] is False,'private flag '+k)
    for k in ('canonical_url','AA','follow_up'):need(cfg['promotion'][k] is None,'private null '+k)
    body=read(E/'PUBLIC_MAIN.html').decode();copy_gate(body)
    tex=copies[ready['controlling_TeX']['extracted_path']].decode()
    abstract=' '.join(tex.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0].split())
    doc=Doc();doc.feed(body);doc.close()
    need(len(doc.ids)==len(set(doc.ids)) and 'main' in doc.ids,'unique main/section IDs')
    need(doc.texts['printed-abstract']==abstract,'whole exact printed abstract')
    need(doc.texts['native-description']==record['metadata']['description'],'whole separate native description')
    need(doc.texts['printed-abstract']!=doc.texts['native-description'],'no native/printed substitution')
    need(body.index('<iframe')<body.index('<h2 id="abstract">'),'reader upfront')
    frames=[d for t,d in doc.attrs if t=='iframe']
    need(len(frames)==1 and frames[0]['src']=='outer_pedal_centroid.pdf#view=FitH' and bool(frames[0]['title']),'accessible FitH reader')
    need(not any(t in ('form','input','button') for t in doc.tags),'passive page')
    need(not re.search(r'mailto:|tel:|<script|2026-11-15|40115|1984|63 assertions|\bMIT\b',body,re.I),'no public contact/internal counters/MIT')
    negatives=0
    for old,new in [('+ conj(z)[2Fv + 3ed + (vd/2)|z|²]','+ z[2Fv + 3ed + (vd/2)|z|²]'),('provided G ≠ 0.','provided G = 0.'),('is not asserted to be phase invariant','is asserted to be phase invariant')]:
        try:copy_gate(body.replace(old,new))
        except ValueError:negatives+=1
        else:raise ValueError('copy-loss control escaped')
    need(negatives==3,'three distinct in-memory copy losses rejected')
    names=sorted(q.name for q in (E/'candidate').iterdir())
    need(names==sorted(['PUBLIC_HEAD.html','PUBLIC_MAIN.html','PUBLIC_COPY.md','SCHOLARLY_METADATA.json','citation.bib','index.html','outer-pedal-centroid-verification.zip','outer_pedal_centroid.pdf']),'exact8 candidate leaves')
    for n in names:need(read(E/'candidate'/n)==read(E/'optimized-candidate'/n),'whole paired render '+n)
    need(read(E/'candidate/PUBLIC_MAIN.html')==body.encode(),'zero main transformations')
    page=read(E/'candidate/index.html').decode();head=read(E/'candidate/PUBLIC_HEAD.html').decode()
    need(page.count(body)==1 and head in page,'complete actual head and main in page')
    need('font-family:Arial,Helvetica,sans-serif' in page and 'background:#fff' in page and '@media(max-width:600px)' in page,'white Arial responsive layout')
    need('name="robots" content="noindex,nofollow,noarchive"' in head and 'rel="canonical"' not in head,'private noindex without installed canonical')
    ld=json.loads(read(E/'candidate/SCHOLARLY_METADATA.json'))
    inline=json.loads(head.split('<script type="application/ld+json">',1)[1].split('</script>',1)[0]);typed(ld,inline)
    need(ld['abstract']==abstract and ld['version']=='1.0' and ld['datePublished']=='2026-10-13','scholarly full abstract/date/version')
    need(ld['license']=='https://creativecommons.org/licenses/by/4.0/','broad rights')
    for asset in ready['all_native_assets_in_original_order']:
        name=asset['original_api_file_object']['key'];need(read(E/'candidate'/name)==copies[asset['path']],'unchanged native download')
    for t,d in doc.attrs:
        if t=='a' and 'href' in d and not d['href'].startswith(('https://','#')):
            need(d['href'] in names,'local link target '+d['href'])
    for mode in ('normal','optimized'):
        rb=read(E/f'RENDER_EDITORIAL-{mode}.stdout');receipt=json.loads(rb)
        need(receipt['mode']==mode and receipt['assertions_enabled'] is (mode=='normal'),'actual separate mode stream')
        need(read(E/f'RENDER_EDITORIAL-{mode}.stderr')==b'','renderer empty stderr')
        for n,p in receipt['buffers'].items():need(pin(read(E/receipt['output_directory']/n))==p,'whole output receipt')
    print(json.dumps({'status':'SOURCE_COPY_CUSTODY_PASSED','mode':'ordinary' if __debug__ else 'optimized-O',
      'strict_final_namespace':not args.preseal,'checks':checks,'typed_nodes':typed_nodes,'source_JSON_bodies':json_bodies,
      'original_files':len(copies),'paired_render_buffers':8,'in_memory_copy_loss_rejections':negatives,
      'scientific_replay':False,'publication_authority':False,'canonical_url':None,'AA':None},sort_keys=True))

if __name__=='__main__':
    main()
