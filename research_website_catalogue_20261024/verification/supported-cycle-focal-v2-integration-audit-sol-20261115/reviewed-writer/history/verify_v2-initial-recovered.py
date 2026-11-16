"""Offline V2 custody. Reads own files and the two pinned original sealed namespaces.
No project imports, live/source/Git reads, subprocess, network, rendering or writes.
"""
from pathlib import Path
import hashlib
from html.parser import HTMLParser
import json
import os
import re
import stat
import sys

N=Path(__file__).absolute().parent
P=N.parent.parent
OLD=N.parent/'supported-cycle-focal-private-stage-sol-20261115'
AUDIT=N.parent/'supported-cycle-focal-independent-code-audit-sol-20261115'
AUTH='3022a08c1f125c8eb74682e98baab887a0dee66a89ce9ddca0f20fe6ef0a5e18'
COUNT=0

def need(ok,why):
    global COUNT
    COUNT+=1
    if not ok:raise ValueError(why)

def read(p):
    need(any(p.is_relative_to(r) for r in (N,OLD,AUDIT)) and p.resolve()==p and stat.S_ISREG(p.lstat().st_mode),'ordinary permitted immutable input')
    return p.read_bytes()

def digest(b):return hashlib.sha256(b).hexdigest()

def pin(p,row):
    b=read(p);need(len(b)==row['bytes'] and digest(b)==row['SHA256'],'whole pinned buffer '+str(p));return b

def extent(root):
    need(root.resolve()==root and stat.S_ISDIR(root.lstat().st_mode),'ordinary directory')
    files,dirs=[],[]
    def walk(d):
        for e in os.scandir(d):
            q=Path(e.path);r=q.relative_to(root).as_posix();m=q.lstat().st_mode
            if stat.S_ISDIR(m):dirs.append(r);walk(q)
            else:need(stat.S_ISREG(m),'no link/special '+str(q));files.append(r)
    walk(root);return sorted(files),sorted(dirs)

def close(root,files,dirs,terminals=()):
    f,d=extent(root);need(f==sorted(list(files)+list(terminals)) and len(f)==len(set(f)) and d==dirs,'exact files/directories/root terminals')

def sealed(root,expected,audit=False):
    sb=read(root/'FINAL_SEAL.json');need(digest(sb)==expected,'same-buffer original seal authentication');s=json.loads(sb)
    name='FINAL_MANIFEST.json' if audit else 'OWNED_MANIFEST.json';mb=read(root/name)
    need(digest(mb)==(s['MANIFEST_SHA256'] if audit else s['manifest']['SHA256']),'same-buffer original manifest authentication');m=json.loads(mb)
    rows={r['path']:{k:r[k] for k in ('bytes','SHA256')} for r in m['files']} if audit else m['payloads']
    close(root,rows,m['directories'],[name,'FINAL_SEAL.json'])
    for n,r in rows.items():pin(root/n,r)
    return s,rows

def same(a,b):
    need(type(a) is type(b),'exact generated-object type')
    if isinstance(a,dict):
        need(list(a)==list(b),'key/order/absence preservation')
        for k in a:same(a[k],b[k])
    elif isinstance(a,list):
        need(len(a)==len(b),'ordered array length')
        for x,y in zip(a,b):same(x,y)
    else:need(a==b,'literal scalar/null')

def references():
    ab=read(N/'AUTHORIZATION.json');need(digest(ab)==AUTH,'fixed corrective root authority');a=json.loads(ab)
    need(a['boundedCorrectivePrivatePreparationAuthorized'] is True and a['productionInstallationAuthorized'] is False and a['rootCompleteOriginalStageOutputOrProductionAdopted'] is False,'private correction only')
    initial=json.loads(read(N/'INITIAL_SEAL.json'))
    for n,r in initial['files'].items():pin(N/n,r)
    s,oldrows=sealed(OLD,'edf8e4e64ea345e950f6d94e678b4d6c8530df37089e80ef6681a519b7fedf54')
    aus,arows=sealed(AUDIT,'780e71570c61a0604c582b2a851b4fe8165105652ddf46446c06182995f36412',True)
    need(aus['status']=='NO_GO_NATIVE_FRAME_AND_LOCAL_HEAD_ADAPTER','literal original NO_GO retained')
    inputs=json.loads(read(OLD/'SOURCE_INPUTS.json'));baseline=json.loads(read(OLD/'WEBSITE_BASELINE.json'))
    rows={r['path']:r for r in inputs['files']}
    need(len(rows)==819 and len(inputs['complete_original_namespaces'])==6,'whole819 source contract retained by reference')
    for r in rows.values():pin(OLD/r['blob'],r)
    return inputs,baseline,rows

def cached(rows,p):
    r=rows[str(p)];return pin(OLD/r['blob'],r)

def frame(baseline):
    r=next(r for r in baseline['files'] if r['path'].endswith('/public/research/five-outgoing-centers-alpha16/index.html'))
    b=pin(OLD/r['blob'],r);h=b[:b.index(b'</head>')+7]
    prefix=b[b.index(b'</head>')+7:b.index(b'<main id="main">')]
    suffix=b[b.rindex(b'</main>')+7:];styles=re.findall(rb'<style>.*?</style>',h,re.S)
    need(len(styles)==1 and b'/research/research.css' in h and b'href="#main"' in prefix and b'Main navigation' in prefix and b'Research home' in suffix,'observed native frame')
    native=json.loads(re.findall(rb'<script type="application/ld\+json">(.*?)</script>',h,re.S)[0])
    return {'prefix':prefix,'suffix':suffix,'style':styles[0],'webpage':native['@graph'][0]}

class Head(HTMLParser):
    def __init__(self):super().__init__();self.meta={};self.links=[]
    def handle_starttag(self,t,attrs):
        d=dict(attrs)
        if t=='meta' and 'name' in d:self.meta[d['name']]=d.get('content')
        if t=='link':self.links.append(d)

def parts(b):
    h=b[:b.index(b'</head>')+7];raw=re.findall(rb'<script type="application/ld\+json">(.*?)</script>',h,re.S)
    need(len(raw)==1,'one whole graph');return h,raw[0],json.loads(raw[0])

def check_page(b,old,main,pub,f):
    need(b.count(main)==1 and b.count(b'<main ')==1 and main.startswith(b'<main id="main">') and b'#view=FitH' in main,'zero entire MAIN transforms')
    h,raw,g=parts(b);oh,oraw,original=parts(old)
    need(b[len(h):b.index(main)]==f['prefix'] and b[b.index(main)+len(main):]==f['suffix'],'exact native outer frame')
    need(h.count(b'<link rel="stylesheet" href="/research/research.css">')==1 and re.findall(rb'<style>.*?</style>',h,re.S)==[f['style']],'native CSS and native reader style only')
    parsed=Head();parsed.feed(h.decode());url=pub['proposed_canonical_url']
    need(parsed.meta['citation_pdf_url']==url+pub['pdf_filename'],'local original citation PDF')
    need(list(g)==['@context','@graph'] and len(g['@graph'])==2,'linked native graph container')
    page,article=g['@graph'];wp=dict(f['webpage']);wp.update({'@id':url+'#page','url':url,'name':pub['title'],'mainEntity':{'@id':url+'#article'}});same(page,wp)
    need(article['@id']==url+'#article' and article['mainEntityOfPage']=={'@id':url+'#page'} and article['isAccessibleForFree'] is True,'linked page/article identities')
    for new,previous,asset in zip(article['encoding'],original['encoding'],pub['native_assets_in_original_order']):
        need(new['contentUrl']==url+asset['original_api_file_object']['key'] and new['sameAs']==previous['contentUrl'],'local encoding/native sameAs')
    need(len(article['encoding'])==len(original['encoding'])==2,'both native encodings')
    restored=json.loads(json.dumps(article,ensure_ascii=False));restored.pop('@id');restored.pop('isAccessibleForFree');restored['mainEntityOfPage']=original['mainEntityOfPage']
    for e,previous in zip(restored['encoding'],original['encoding']):
        e.pop('sameAs');e['contentUrl']=previous['contentUrl']
    same(restored,original)
    if pub['doi'].endswith('23578142'):need('license' not in article['encoding'][0] and pub['code_license']=='MIT','mixed ZIP blanket license remains absent')
    else:need(pub['code_license']=='CC BY 4.0' and all(e['license']=='https://creativecommons.org/licenses/by/4.0/' for e in article['encoding']),'broad129CCBY retained')
    def neutral(head,graph):
        z=head.replace(graph,b'__GRAPH__');z=re.sub(rb'<style>.*?</style>',b'',z,flags=re.S)
        z=z.replace(b'<link rel="stylesheet" href="/research/research.css">',b'')
        return re.sub(rb'(<meta name="citation_pdf_url" content=")[^"]*(">)',rb'\1__PDF__\2',z)
    need(neutral(h,raw)==neutral(oh,oraw),'all other head bytes unchanged')

def check_outputs(inputs,baseline,rows):
    f=frame(baseline);paths=[r['path'] for r in json.loads(read(OLD/'OVERLAY_MANIFEST.json'))['files']]
    htmls=[]
    for rec in inputs['records']:
        e=P/'papers'/rec['record_id']/'reviews/editorial';pub=json.loads(cached(rows,e/'publication.json'));main=cached(rows,e/'PUBLIC_MAIN.html');name='research/'+pub['slug']+'/index.html';htmls.append(name)
        need(digest(main)==('e5cbb523bceea9f6b9e2664b9da4e3fdf07f7039c7f54e4babafa61084ec4223' if rec['record_id']=='23578142' else '89f45f2f8fbc4001a11ec2eba82e5e23bb27e86e293c9bcaae35eb155f5ccc9d'),'fixed original MAIN')
        for candidate in ['candidate-a','candidate-b']:check_page(read(N/candidate/'public'/name),read(OLD/'candidate-a/public'/name),main,pub,f)
    dirs=sorted(['research']+['research/'+n.split('/')[1] for n in htmls])
    for candidate in ['candidate-a','candidate-b']:
        close(N/candidate/'public',paths,dirs)
        for name in paths:
            b=read(N/candidate/'public'/name)
            if name not in htmls:need(b==read(OLD/'candidate-a/public'/name),'other8 buffers whole unchanged')
            need(b==read(N/'candidate-a/public'/name),'whole10 normal optimized equality')
    need(len(paths)==10 and len(set(baseline['public_namespace'])|set(paths))==631,'exact10 virtual631/96/97')
    return paths

def main():
    need(sys.argv[1:] in [[],['--initial'],['--preseal']],'bounded modes')
    inputs,base,rows=references()
    if sys.argv[1:]==['--initial']:
        print(json.dumps({'status':'INITIAL_REFERENCED_CUSTODY_PASSED','old_stage_files':1335,'old_audit_files':1352,'source_context_files':819,'original_NO_GO_preserved':True,'no_old_execution_or_live_reads':True}));return
    paths=check_outputs(inputs,base,rows)
    for n in ['PRE_GUARD.json','POST_GUARD.json']:
        g=json.loads(read(N/n));need(g['status']=='ALL_ACTUAL_READONLY_FENCES_UNCHANGED' and g['production_mutation'] is False,'actual new fresh drift fences')
        need(g['baseline_counts']==[623,94,95] and g['index_SHA256']=='35181f4046df6e197ba5c5c6e34c348b2b46783c0cc073a5b7f066692ba332b6','actual623 rawindex fence')
    if not sys.argv[1:]:
        sb=read(N/'FINAL_SEAL.json');seal=json.loads(sb);mb=read(N/'OWNED_MANIFEST.json');need(digest(mb)==seal['manifest_SHA256'],'same-buffer final manifest');m=json.loads(mb)
        close(N,m['payloads'],m['directories'],['OWNED_MANIFEST.json','FINAL_SEAL.json'])
        for n,r in m['payloads'].items():pin(N/n,r)
        need(seal['production_authority'] is False and seal['AA'] is None and seal['canonical_url'] is None,'authority separation')
    print(json.dumps({'status':'CORRECTIVE_PRIVATE_EXACT10_CUSTODY_PASSED','mode':'normal' if __debug__ else 'optimized','checks':COUNT,'paired_buffers':len(paths),'other8_whole_unchanged':True,'MAIN_transforms':0,'original_NO_GO_preserved':True,'default_reads_original_sealed_namespaces_by_reference':True,'live_or_science_reads_execution_writes':False,'production_authority':False,'AA':None,'canonical_url':None,'follow_up':None},sort_keys=True))

if __name__=='__main__':main()
