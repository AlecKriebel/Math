"""New corrective private author/finite controls/sealer. Never executes old code."""
import sys
sys.dont_write_bytecode=True
from datetime import datetime,timezone
from html import escape
import json
from pathlib import Path
import re
import os
import tempfile
import verify_v2 as V

N=V.N

def new(p,b):
    V.need(p.is_relative_to(N),'only owned new write')
    with p.open('xb') as f:V.need(f.write(b)==len(b),'complete exclusive write')

def article(old,main,pub,f):
    h,raw,g=V.parts(old);a=json.loads(json.dumps(g,ensure_ascii=False));url=pub['proposed_canonical_url']
    for encoding,asset in zip(a['encoding'],pub['native_assets_in_original_order']):
        native=encoding['contentUrl'];items=[]
        for k,v in encoding.items():
            items.append((k,url+asset['original_api_file_object']['key'] if k=='contentUrl' else v))
            if k=='contentUrl':items.append(('sameAs',native))
        encoding.clear();encoding.update(items)
    a['@id']=url+'#article';a['mainEntityOfPage']={'@id':url+'#page'};a['isAccessibleForFree']=True
    page=dict(f['webpage']);page.update({'@id':url+'#page','url':url,'name':pub['title'],'mainEntity':{'@id':url+'#article'}})
    graph={'@context':g['@context'],'@graph':[page,a]}
    h=h.replace(raw,json.dumps(graph,ensure_ascii=False).encode(),1)
    citation=rb'(<meta name="citation_pdf_url" content=")[^"]*(">)'
    V.need(len(re.findall(citation,h))==1,'one original citation PDF')
    h=re.sub(citation,lambda m:m[1]+escape(url+pub['pdf_filename'],quote=True).encode()+m[2],h)
    V.need(len(re.findall(rb'<style>.*?</style>',h,re.S))==1,'one original preview style')
    h=re.sub(rb'<style>.*?</style>',b'',h,flags=re.S)
    h=h.replace(b'</head>',b'<link rel="stylesheet" href="/research/research.css">'+f['style']+b'</head>',1)
    result=h+f['prefix']+main+f['suffix'];V.check_page(result,old,main,pub,f)
    return result

def author(mode):
    V.need((mode=='normal')==__debug__,'actual runtime mode match')
    inputs,base,rows=V.references();f=V.frame(base)
    V.need(json.loads(V.read(N/'PRE_GUARD.json'))['status']=='ALL_ACTUAL_READONLY_FENCES_UNCHANGED','fresh actual preguard before authoring')
    paths=[r['path'] for r in json.loads(V.read(V.OLD/'OVERLAY_MANIFEST.json'))['files']]
    output={p:V.read(V.OLD/'candidate-a/public'/p) for p in paths}
    for r in inputs['records']:
        e=V.P/'papers'/r['record_id']/'reviews/editorial';pub=json.loads(V.cached(rows,e/'publication.json'));main=V.cached(rows,e/'PUBLIC_MAIN.html');p='research/'+pub['slug']+'/index.html'
        output[p]=article(output[p],main,pub,f)
    dest=N/('candidate-a' if mode=='normal' else 'candidate-b');V.need(not dest.exists(),'new private candidate only')
    for name,b in output.items():
        p=dest/'public'/name;p.parent.mkdir(parents=True,exist_ok=True);new(p,b)
    print(json.dumps({'status':'CORRECTIVE_PRIVATE_EXACT10_RENDERED','mode':mode,'optimization_level':sys.flags.optimize,'files':[{'path':n,'bytes':len(b),'SHA256':V.digest(b)} for n,b in output.items()],'only2HTML_heads_frames_changed':True,'MAIN_transforms':0,'other8_whole_unchanged':True,'production_authority':False,'AA':None,'canonical_url':None},sort_keys=True))

def controls():
    inputs,base,rows=V.references();f=V.frame(base);rejected=[]
    for rec in inputs['records']:
        e=V.P/'papers'/rec['record_id']/'reviews/editorial';p=json.loads(V.cached(rows,e/'publication.json'));main=V.cached(rows,e/'PUBLIC_MAIN.html');name='research/'+p['slug']+'/index.html';old=V.read(V.OLD/'candidate-a/public'/name);b=V.read(N/'candidate-a/public'/name)
        h,raw,g=V.parts(b);broken=json.loads(raw);broken['@graph'][1]['encoding'][0].pop('sameAs')
        mutations=[('missing nativeCSS',b.replace(b'<link rel="stylesheet" href="/research/research.css">',b'')),('remote citationPDF',b.replace((p['proposed_canonical_url']+p['pdf_filename']).encode(),b'https://example.invalid/remote.pdf',1)),('lost native encoding alias',b.replace(raw,json.dumps(broken,ensure_ascii=False).encode(),1)),('MAIN byte change',b.replace(main,main.replace(b'<main id="main">',b'<main id="changed">',1),1))]
        for label,bad in mutations:
            try:V.check_page(bad,old,main,p,f)
            except (ValueError,KeyError):rejected.append(rec['record_id']+':'+label)
            else:raise ValueError('actual changed adapter escaped '+label)
    with tempfile.TemporaryDirectory(dir=N/'private',prefix='new-namespace-') as tmp:
        root=Path(tmp);(root/'declared-empty').mkdir();new(root/'ordinary',b'whole fixture body')
        V.close(root,['ordinary'],['declared-empty'])
        for kind in ('empty','FIFO','link'):
            q=root/'unexpected'
            if kind=='empty':q.mkdir()
            elif kind=='FIFO':os.mkfifo(q)
            else:q.symlink_to('ordinary')
            try:V.close(root,['ordinary'],['declared-empty'])
            except ValueError:rejected.append('namespace:'+kind)
            else:raise ValueError('namespace escaped')
            if kind=='empty':q.rmdir()
            else:q.unlink()
        V.close(root,['ordinary'],['declared-empty'])
    print(json.dumps({'status':'NEW_NARROW_ADAPTER_CONTROLS_PASSED','rejections':rejected,'original_campaigns_executed':False,'temporary_fixture_children_removed':True},sort_keys=True))

def seal():
    V.need(not (N/'OWNED_MANIFEST.json').exists(),'new exact root terminals only')
    fs,ds=V.extent(N);payloads={}
    for n in fs:
        b=V.read(N/n);payloads[n]={'bytes':len(b),'SHA256':V.digest(b)}
    for n in ('REPORT.md','VERDICT.json','CURRENT_CODE_MANIFEST.json','CORRECTIVE_DIFF.patch','EXECUTIONS.json'):V.need(n in payloads,'complete final reporting')
    mb=(json.dumps({'payloads':payloads,'directories':ds,'only_exact_root_terminals':['OWNED_MANIFEST.json','FINAL_SEAL.json'],'future_exclusions':[]},indent=2)+'\n').encode()
    new(N/'OWNED_MANIFEST.json',mb)
    s={'UTC':datetime.now(timezone.utc).isoformat(),'status':'FINAL_CORRECTIVE_PRIVATE_EXACT10_PENDING_NEW_INDEPENDENT_AUDIT_AND_ROOT_ADOPTION','manifest_SHA256':V.digest(mb),'payload_files':len(fs),'total_files_including2exact_root_terminals':len(fs)+2,'directories':ds,'root_authorization_SHA256':V.AUTH,'original_stage_SHA256':'edf8e4e64ea345e950f6d94e678b4d6c8530df37089e80ef6681a519b7fedf54','original_audit_SHA256':'780e71570c61a0604c582b2a851b4fe8165105652ddf46446c06182995f36412','original_NO_GO_literal_retained':True,'production_authority':False,'root_V2_adopted':False,'new_independent_audit':None,'AA':None,'canonical_url':None,'follow_up':None,'completion_percent':100,'postseal_writes_allowed':False}
    new(N/'FINAL_SEAL.json',(json.dumps(s,indent=2)+'\n').encode());V.close(N,fs,ds,['OWNED_MANIFEST.json','FINAL_SEAL.json'])
    print(json.dumps({'status':s['status'],'seal_SHA256':V.digest(V.read(N/'FINAL_SEAL.json')),'manifest_SHA256':V.digest(mb),'files':len(fs)+2,'directories':len(ds),'production_authority':False},sort_keys=True))

def main():
    V.need(not (N/'FINAL_SEAL.json').exists(),'immutable FINAL cannot be modified')
    V.need(sys.argv[1:] in [['normal'],['optimized'],['controls'],['seal']],'finite corrective operations')
    mode=sys.argv[1]
    if mode in ('normal','optimized'):author(mode)
    elif mode=='controls':controls()
    else:seal()

if __name__=='__main__':main()
