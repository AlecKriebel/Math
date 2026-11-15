#!/usr/bin/env python3
"""Bounded current-tree identity collection; no imports from earlier packets."""
from pathlib import Path
from html.parser import HTMLParser
import datetime
import hashlib
import json
import re
import subprocess
import unicodedata

O=Path(__file__).resolve().parent
P=O.parents[1]
REPO=P.parent
D=P/'redirects/three-paper-preflight-sol-20261115'
COMMIT='1ef94e0144b2b6a7f42868154d6c3f11b3ec6d41'
TREE='4b890b5e4f583ed562ba7291ae367c6ff70c5090'
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()


def need(ok,message):
    if not ok:raise RuntimeError(message)


def h(b):return hashlib.sha256(b).hexdigest()


def save(n,x):
    p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')


def git(*args):
    r=subprocess.run(['git',*args],cwd=REPO,capture_output=True)
    need(r.returncode==0,repr(args)+': '+r.stderr.decode(errors='replace'))
    return r.stdout


def native(kind,oid):
    b=git('cat-file',kind,oid)
    need(hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid,'Native Git object hash')
    out=O/'git-objects'/f'{kind}-{oid}.raw';out.parent.mkdir(exist_ok=True);out.write_bytes(b)
    return b


def binding(p):
    b=p.read_bytes();return {'path':str(p),'bytes':len(b),'SHA256':h(b)}


class HTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.visible=[];self.links=[];self.metas=[];self.title=[];self.in_title=False;self.hidden=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='title':self.in_title=True
        if tag in ['script','style']:self.hidden+=1
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag in ['meta','link']:self.metas.append({'tag':tag,'attributes':attrs})
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
        if tag in ['script','style']:self.hidden=max(0,self.hidden-1)
    def handle_data(self,data):
        if self.in_title:self.title.append(data)
        if not self.hidden:self.visible.append(data)


def normalized(t):return ' '.join(unicodedata.normalize('NFKC',t).replace('–','-').replace('—','-').casefold().split())


def main():
    # Authenticate selected metadata in the sealed reusable packet; no old code import/execution.
    seal=json.loads((D/'SEAL.json').read_text());om=json.loads((D/'OWNED_MANIFEST.json').read_text())
    need(h((D/'OWNED_MANIFEST.json').read_bytes())==seal['OWNED_MANIFEST_SHA256'],'Prior seal/manifest')
    old_owned={r['path']:r for r in om['files']}
    inputs=[binding(D/'SEAL.json'),binding(D/'OWNED_MANIFEST.json')]
    for name in ['HISTORICAL_DOCS_BINDINGS.json','CURRENT_DOCS_DELTA.json','REMOTE_DOCS_TREE_GET.json','REUSED_EXTRACT_BINDINGS.json']:
        p=D/name;r=old_owned[name];need(p.stat().st_size==r['bytes'] and h(p.read_bytes())==r['SHA256'],'Prior selected payload '+name);inputs.append(binding(p))
    raw=json.loads((D/'REMOTE_DOCS_TREE_GET.json').read_text());api=json.loads(raw['structuredContent']['content'])
    need(api['sha']==TREE and api.get('truncated') is False,'Prior complete current tree')
    prior_current={'docs/'+r['path']:(r['mode'],r['type'],r['sha'],r.get('size')) for r in api['tree'] if r['type']=='blob'}
    historic={r['path']:r for r in json.loads((D/'HISTORICAL_DOCS_BINDINGS.json').read_text())}
    raw_listing=(O/'raw/current-docs-listing.stdout').read_bytes();current={}
    for row in raw_listing.split(b'\0'):
        if not row:continue
        a,b=row.split(b'\t');mode,kind,oid=a.decode().split();current['docs/'+b.decode()]=(mode,kind,oid)
    need({k:v[:3] for k,v in prior_current.items()}==current,'Current tree leaf set differs from authenticated reusable corpus')
    b=native('commit',COMMIT);root=re.match(rb'tree ([0-9a-f]{40})\n',b).group(1).decode();native('tree',root);native('tree',TREE)
    for row in git('ls-tree','-r','-t','-z',COMMIT+':docs').split(b'\0'):
        if not row:continue
        a,name=row.split(b'\t');mode,kind,oid=a.decode().split()
        if kind=='tree':native('tree',oid)
    rows=[];representations=[];htmls=[];raw_text=0;decoded=0
    for name,(mode,kind,oid) in sorted(current.items()):
        old=historic[name]
        if old['blob']==oid:row=dict(old)
        else:
            b=git('cat-file','blob',oid);row={'path':name,'mode':mode,'kind':kind,'blob':oid,'bytes':len(b),'sha256':h(b)}
        rows.append(row)
        if name.lower().endswith(('.pdf','.zip','.png','.jpg','.jpeg','.ico','.woff','.woff2')):continue
        b=git('cat-file','blob',oid);need(len(b)==row['bytes'] and h(b)==row['sha256'],'Current text blob binding '+name)
        try:text=b.decode('utf-8')
        except UnicodeDecodeError:continue
        target=O/'corpus'/f'{oid}.raw';target.parent.mkdir(exist_ok=True);target.write_bytes(b)
        representations.append({'public_path':name,'representation':'raw_UTF8','path':str(target),'text':text});raw_text+=1
        if name.endswith('.html'):
            parser=HTML();parser.feed(text);visible=' '.join(parser.visible);out=O/'corpus'/f'{oid}.visible.txt';out.write_text(visible)
            representations.append({'public_path':name,'representation':'decoded_HTML','path':str(out),'text':visible});decoded+=1
            htmls.append({'path':name,'blob':oid,'title':' '.join(parser.title),'links':parser.links,'metas':parser.metas,'raw_snapshot':str(target),'visible_snapshot':str(out)})
    extracts=json.loads((D/'REUSED_EXTRACT_BINDINGS.json').read_text())
    for r in extracts:
        need(current[r['public_path']][2]==r['pdf_blob'],'Current PDF blob differs from reusable extract')
        need(historic[r['public_path']]['sha256']==r['pdf_sha256'],'Original PDF SHA binding')
        p=Path(r['path']);need(p.stat().st_size==r['bytes'] and h(p.read_bytes())==r['sha256'],'Exact reusable full PDF text')
        inputs.append(binding(p));representations.append({'public_path':r['public_path'],'representation':'reused_complete_PDF_text','path':str(p),'text':p.read_text()})
    queries={
      '118_record_DOI_concept':r'2338514[45]',
      '118_exact_title':r'multiplicatively weighted centers of median graphs in quasilinear time',
      '118_distinctive':r'multiplicativ\w* weighted|weighted.{0,70}median graph|median graph.{0,70}(?:center|centre)|weighted_centers',
      '118_broad':r'\bmedian\b|\bquasilinear\b',
      '119_record_DOI_concept':r'2298351[23]',
      '119_exact_title':r'nonattainment in the harrell[- ]stubbe dirichlet gap inequality',
      '119_distinctive':r'strict.dirichlet.gap|harrell.{0,12}stubbe|OWR.3389.016|dirichlet.{0,40}gap',
      '119_broad':r'\byang\b|nonattainment|dirichlet|spectral gap'}
    hits={};counts={}
    for q,pattern in queries.items():
        hits[q]=[]
        for r in representations:
            t=normalized(r['text']);matches=list(re.finditer(pattern.casefold(),t))
            if matches:hits[q].append({k:r[k] for k in ['public_path','representation','path']}|{'occurrences':len(matches),'contexts':[t[max(0,m.start()-140):m.end()+200] for m in matches[:8]]})
        counts[q]=len(hits[q])
    assets=[]
    for name in ['docs/papers/strict-dirichlet-gap/index.html','docs/papers/strict-dirichlet-gap/paper.pdf','docs/papers/strict-dirichlet-gap/source-and-verification.zip','docs/papers/strict-dirichlet-gap/SHA256SUMS.txt']:
        oid=current[name][2];b=native('blob',oid);out=O/'candidate-evidence'/Path(name).name;out.parent.mkdir(exist_ok=True);out.write_bytes(b);assets.append({'path':name,'blob':oid,'bytes':len(b),'SHA256':h(b),'snapshot':str(out)})
    identities=[]
    for rid in ['23385145','22983513']:
        p=P/'papers'/rid/'publication.json';b=p.read_bytes();x=json.loads(b);inputs.append(binding(p));out=O/'target-inputs'/rid/'publication.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
        fields=['title','slug','doi','publication_date','version','canonical_url','AA','native_sheet_aa_url','proposed_canonical_url','pdf_filename','pdf_pages','supplement_filename']
        identities.append({'record_id':rid,'original_config':binding(p),'literal_fields':{k:x[k] for k in fields if k in x},'fields_absent':[k for k in fields if k not in x],'prepared_snapshot':str(out),'frozen_historical_review_gate_fields':{k:v for k,v in x['review_metadata'].items() if isinstance(v,(bool,type(None)))}})
    save('TARGET_IDENTITIES.json',{'UTC':NOW,'targets':identities,'informed_prior_roles':{'23385145':'completed adversarial science review','22983513':'source acquisition, adversarial science review and editorial preparation'},'this_is_not_a_new_scientific_review':True,'root_adoption_is_additive_authority_historical_pending_flags_not_rewritten':True})
    save('CURRENT_BLOB_BINDINGS.json',rows);save('REUSED_EXTRACT_BINDINGS.json',extracts);save('CURRENT_HTML_IDENTITIES.json',htmls);save('SEARCH_RESULTS.json',{'queries':queries,'hit_representation_counts':counts,'hits':hits});save('CANDIDATE_ASSETS.json',assets)
    save('INPUT_MANIFEST.json',{'UTC':NOW,'files':inputs,'imports_or_execution_from_prior_packets':False})
    save('CORPUS_RECEIPT.json',{'UTC':NOW,'remote_commit':COMMIT,'docs_tree':TREE,'reusable_packet':str(D),'current_tree_exactly_equals_authenticated_previous_current_tree':True,'current_blobs':len(rows),'raw_UTF8_representations':raw_text,'decoded_HTML_representations':decoded,'reused_complete_PDF_texts':len(extracts),'reused_PDF_pages':sum(r['pages'] for r in extracts),'total_identity_search_representations':len(representations),'new_PDF_extractions':0,'support_archives_expanded_or_supplied_code_executed':False,'hit_representation_counts':counts})
    print(json.dumps({'counts':counts,'candidate_paths':sorted({r['public_path'] for q in hits for r in hits[q]}),'representations':len(representations)},indent=2))


if __name__=='__main__':main()
