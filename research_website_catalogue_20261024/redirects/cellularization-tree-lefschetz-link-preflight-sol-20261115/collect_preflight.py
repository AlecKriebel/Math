#!/usr/bin/env python3
"""Read-only bounded source collection; writes only this new private packet."""
from pathlib import Path
from html.parser import HTMLParser
import datetime, hashlib, json, re, subprocess, unicodedata

O=Path(__file__).resolve().parent
P=O.parents[1]
REPO=P.parent
D=P/'redirects/median-gap-preflight-sol-20261115'
IDS=['23439582','23440389','23570763','23331295']
INPUTS={}
def need(v,m):
    if not v: raise RuntimeError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_text())
def save(n,v):
    p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def bind(p):
    p=p.resolve();b=p.read_bytes();r={'path':str(p),'bytes':len(b),'SHA256':sha(b)};INPUTS[str(p)]=r;return r
def check(row,base=None):
    p=(base/row['path']) if base else Path(row['path']);b=p.read_bytes()
    need(len(b)==row['bytes'] and sha(b)==row.get('SHA256',row.get('sha256')),'Binding: '+str(p));bind(p);return b
def git(kind,oid):
    r=subprocess.run(['git','cat-file',kind,oid],cwd=REPO,capture_output=True);need(r.returncode==0,'Missing existing local Git object '+oid)
    b=r.stdout;need(hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid,'Git object hash '+oid);return b
def api(n):
    x=load(O/'raw'/n);need(x.get('isError') is False,'GitHub tool error');return json.loads(x['structuredContent']['content'])
def norm(t): return ' '.join(unicodedata.normalize('NFKC',t).replace('–','-').replace('—','-').casefold().split())
class HTML(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True);self.visible=[];self.title=[];self.links=[];self.in_title=False;self.hidden=0
    def handle_starttag(self,t,a):
        d=dict(a)
        if t=='title':self.in_title=True
        if t in ['script','style']:self.hidden+=1
        if t in ['a','iframe','link']:
            for k in ['href','src']:
                if k in d:self.links.append({'tag':t,k:d[k]})
    def handle_endtag(self,t):
        if t=='title':self.in_title=False
        if t in ['script','style']:self.hidden=max(0,self.hidden-1)
    def handle_data(self,s):
        if self.in_title:self.title.append(s)
        if not self.hidden:self.visible.append(s)
def tree_sha(entries):
    out=b''
    for r in sorted(entries,key=lambda r:(r['path']+('/' if r['type']=='tree' else '')).encode()):
        mode=r['mode'].lstrip('0');out+=mode.encode()+b' '+r['path'].encode()+b'\0'+bytes.fromhex(r['sha'])
    return hashlib.sha1(b'tree '+str(len(out)).encode()+b'\0'+out).hexdigest()

def main():
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    seal=load(D/'FINAL_SEAL.json');m=load(D/'OWNED_MANIFEST.json');bind(D/'FINAL_SEAL.json')
    need(sha((D/'OWNED_MANIFEST.json').read_bytes())==seal['OWNED_MANIFEST_SHA256'],'Reusable final seal');bind(D/'OWNED_MANIFEST.json')
    for r in m['files']:check(r,D)
    need({r['path'] for r in m['files']}=={p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()}-set(m['excluded_terminal_files']),'Reusable whole custody inventory')
    for n in ['verify_readonly.py','collect.py','INPUT_MANIFEST.json']:bind(D/n)
    old=load(D/'CURRENT_BLOB_BINDINGS.json');oldmap={r['path']:r for r in old}
    ref=api('remote-main-start.json');commit=api('remote-commit-start.json');root=api('remote-root-start.json');docs=api('remote-docs-start.json')
    need(commit['sha']==ref['object']['sha'] and root['sha']==commit['tree']['sha'],'Remote ref/commit/root')
    need(root.get('truncated') is False and docs.get('truncated') is False,'Complete actual remote trees')
    need(tree_sha(root['tree'])==root['sha'],'Actual root tree native SHA')
    need(next(r['sha'] for r in root['tree'] if r['path']=='docs')==docs['sha'],'Actual root/docs binding')
    dirs={'':docs['sha']}|{r['path']:r['sha'] for r in docs['tree'] if r['type']=='tree'}
    for directory,oid in dirs.items():
        entries=[]
        for r in docs['tree']:
            q=Path(r['path']);parent='' if str(q.parent)=='.' else str(q.parent)
            if parent==directory:entries.append(dict(r,path=q.name))
        need(tree_sha(entries)==oid,'Actual recursive native tree '+directory)
    newmap={'docs/'+r['path']:r for r in docs['tree'] if r['type']=='blob'}
    need(len(newmap)==254 and set(newmap)==set(oldmap),'Current complete leaf set')
    delta=[{'path':n,'old_blob':oldmap[n]['blob'],'new_blob':newmap[n]['sha']} for n in newmap if oldmap[n]['blob']!=newmap[n]['sha']]
    need(delta==[{'path':'docs/papers/strict-dirichlet-gap/index.html','old_blob':'b9705a518f76839427ff4f1e0bded6bdf95a7894','new_blob':'7b7411fefe1638f4721bc2180486574497f69ab0'}],'Only authorized known strict-gap delta')
    strict=load(P/'redirects/root-strict-gap-final-disposition-20261115.json');bind(P/'redirects/root-strict-gap-final-disposition-20261115.json')
    change=strict['whole_literal_application_verdict'];need(change['new_blob']==delta[0]['new_blob'] and change['old_blob']==delta[0]['old_blob'],'Known delta authority identity')
    blob=load(O/'raw/current-strict-gap-blob.json')['structuredContent']['content'].encode();need(len(blob)==838 and sha(blob)==change['exact_candidate_SHA256'],'Whole delta response bytes')
    need(hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()==delta[0]['new_blob'],'Whole delta native blob')
    body=O/'private/current-strict-gap.html';body.parent.mkdir(exist_ok=True);body.write_bytes(blob)
    rows=[];representations=[];htmls=[]
    # Authenticate all old original blob bodies against native Git IDs and stored SHA256.
    # No fetch, checkout, object write, extraction, supplied code, or prior helper execution.
    for r in old:
        b=git('blob',r['blob']);need(len(b)==r['bytes'] and sha(b)==r['sha256'],'Original complete released blob '+r['path'])
        n=r['path'];current_blob=newmap[n]['sha'];cur=blob if n==delta[0]['path'] else b
        row={'path':n,'blob':current_blob,'bytes':len(cur),'SHA256':sha(cur),'original_blob':r['blob'],'original_bytes':r['bytes'],'original_SHA256':r['sha256']};rows.append(row)
        raw=D/'corpus'/f"{r['blob']}.raw"
        if raw.exists():
            need(raw.read_bytes()==b,'Original cached raw equality')
            path=body if n==delta[0]['path'] else raw
            text=cur.decode('utf-8');representations.append({'public_path':n,'representation':'raw_UTF8','path':str(path),'text':text})
            if n.endswith('.html'):
                p=HTML();p.feed(text);visible=' '.join(p.visible)
                vp=D/'corpus'/f"{r['blob']}.visible.txt"
                if n==delta[0]['path']:
                    vp=O/'private/current-strict-gap.visible.txt';vp.write_text(visible)
                else:need(vp.read_text()==visible,'Whole decoded HTML binding')
                representations.append({'public_path':n,'representation':'decoded_HTML','path':str(vp),'text':visible})
                htmls.append({'public_path':n,'title':' '.join(p.title),'links':p.links,'whole_HTML_bytes':len(cur),'SHA256':sha(cur),'blob':current_blob})
    extracts=load(D/'REUSED_EXTRACT_BINDINGS.json')
    for r in extracts:
        need(newmap[r['public_path']]['sha']==r['pdf_blob'],'Current PDF original ID');need(oldmap[r['public_path']]['sha256']==r['pdf_sha256'],'Current PDF whole SHA')
        check(r);representations.append({'public_path':r['public_path'],'representation':'reused_complete_PDF_text','path':r['path'],'text':Path(r['path']).read_text()})
    need(len(representations)==260 and len(extracts)==76 and sum(r['pages'] for r in extracts)==854,'Exact reused complete representations')
    queries={
      '121_record_concept':r'2343958[12]',
      '121_title':r'vanishing of the cellularization map for non-p-nilpotent component groups',
      '121_distinctive':r'cellulari[sz]ation|non.?p.?nilpotent|proxy.small|greenlees',
      '121_broad':r'hopf|compact lie|bosonization',
      '122_record_concept':r'2344038[89]',
      '122_title':r'a five-list obstruction on an eleven-vertex tree',
      '122_distinctive':r'five.list|eleven.vertex|tree.five.list|l\s*\(?\s*2\s*,\s*1\s*\)?.{0,20}(?:list|label)|kohl',
      '122_broad':r'list label|list.label|distance label|list colouring|list coloring',
      '127_record_concept':r'2357076[23]|30004534',
      '127_title':r'a symmetric ideal chain with periodic lefschetz behavior in positive characteristic',
      '127_distinctive':r'periodic.{0,50}lefschetz|lefschetz.{0,50}(?:periodic|symmetric|chain)|symmetric ideal chain|romer|römer|seceleanu|şega',
      '127_broad':r'lefschetz|artinian|weak lefschetz|strong lefschetz',
      '128_record_concept':r'2333129[45]',
      '128_title':r'an elementary counterexample to a nullstellensatz for finite-type link invariants',
      '128_distinctive':r'nullstellensatz|finite.type.{0,40}link|link.{0,40}finite.type|bar.natan|ohtsuki|stoimenow|stanford.{0,10}trapp',
      '128_broad':r'linking number|braiding sequence|vassiliev'}
    hits={}
    for name,pattern in queries.items():
        hits[name]=[]
        for r in representations:
            t=norm(r['text']);matches=list(re.finditer(pattern,t))
            if matches:hits[name].append({k:r[k] for k in ['public_path','representation','path']}|{'occurrences':len(matches),'contexts':[t[max(0,x.start()-160):x.end()+200] for x in matches[:8]]})
    save('SEARCH_RESULTS.json',{'queries':queries,'hit_representation_counts':{k:len(v) for k,v in hits.items()},'hits':hits})
    save('CURRENT_HTML_IDENTITIES.json',htmls);save('CURRENT_BLOB_BINDINGS.json',rows);save('REUSED_EXTRACT_BINDINGS.json',extracts)
    save('CORPUS_AUTHENTICATION.json',{'UTC':now,'prior_packet':str(D),'prior_seal':seal,'entire_prior_owned_payloads_authenticated':len(m['files']),'all_original_blobs_authenticated':len(old),'all_original_complete_bodies_total_bytes':sum(r['bytes'] for r in old),'actual_remote_commit':commit['sha'],'actual_root_tree':root['sha'],'actual_docs_tree':docs['sha'],'all_actual_recursive_docs_tree_objects_authenticated':len(dirs),'complete_blobs':254,'current_delta':delta,'raw_UTF8':sum(r['representation']=='raw_UTF8' for r in representations),'decoded_HTML':sum(r['representation']=='decoded_HTML' for r in representations),'reused_complete_PDF_texts':len(extracts),'PDF_pages':854,'representations':260,'new_PDF_extractions':0,'scientific_or_prior_helper_executions':0,'Git_mutation_commands':0,'network_in_collector':0})
    identities=[]
    for rid in IDS:
        e=P/'papers'/rid/'reviews/editorial';config=next(x for x in [e/'config/publication.json',e/'publication.json',P/'papers'/rid/'publication.json'] if x.exists());j=load(config);bind(config)
        sr=j['source_binding']['whole_original_source_ready'];rn=next(sr[k] for k in ['selected_actual_PDF'] if k in sr)
        native_pdf=Path(rn['path']);check(rn);prepared=e/'candidate/assets'/j['pdf_filename'];need(prepared.read_bytes()==native_pdf.read_bytes(),'Prepared/native PDF whole equality');bind(prepared)
        tex=sr['controlling_TeX'];
        if isinstance(tex,dict) and 'path' in tex:check(tex)
        for n in ['PUBLIC_COPY.md','VERDICT.json','REPORT.md','SEAL.json','MANIFEST.json','actual-published.txt']:
            if (e/n).exists():bind(e/n)
        root_review=P/'papers'/rid/'reviews/root/ROOT_REVIEW_20261115.md';bind(root_review)
        for n in [f'root-editorial-{rid}-20261115.json',f'root-clearance-{rid}-20261115.json']:
            p=P/'verification'/n
            if p.exists():bind(p)
        for q in sr.get('whole_native_API_objects',[]):
            if isinstance(q,dict) and 'path' in q:check(q)
        # All native assets are authenticated by both whole-source bindings and native MD5.
        assets=[]
        for q in sr.get('all_native_assets_in_original_order',[]):
            if isinstance(q,dict) and 'path' in q:
                b=check(q);a=q.get('original_api_file_object',{});expected=a.get('checksum')
                if expected and expected.startswith('md5:'):need(hashlib.md5(b).hexdigest()==expected[4:],'Native MD5')
                assets.append(q)
        text=e/'actual-published.txt';bind(text)
        identities.append({'record_id':rid,'config':bind(config),'fields':{k:j.get(k) for k in ['title','slug','version','printed_version','publication_date','doi','canonical_url','AA','proposed_canonical_url','pdf_filename','supplement_filename']},'native_source_ready_identity':{k:sr.get(k) for k in ['title','version','publication_date','DOI','created','updated']},'selected_actual_PDF':rn,'controlling_TeX':tex,'all_native_assets_in_original_order':assets,'actual_PDF_complete_text_read':bind(text),'root_scope_read':bind(root_review),'whole_approved_public_copy_read':bind(e/'PUBLIC_COPY.md'),'native_asset_equal_docs_paths':{p.name:[r['path'] for r in rows if r['SHA256']==sha(p.read_bytes())] for p in (e/'candidate/assets').iterdir() if p.suffix in ['.pdf','.zip','.tex']}})
    save('TARGET_IDENTITIES.json',identities)
    save('INPUT_MANIFEST.json',{'UTC':now,'files':list(INPUTS.values()),'reusable_packet_helpers_read_but_not_executed':True,'all_paths_read_only_outside_new_packet':True})
    save('RESEARCH_LOG.json',{'checkpoints':[{'UTC':now,'completion_percent_this_preflight':65,'finding':'Authenticated whole prior custody inventory, all254originalblob bodies, current254leaves/51tree objects and exact838-byte strict-gap delta; searched all260representations including76PDFpathoccurrences/854pages. Native wholePDF/config/scope identities bound. Candidate inspection and independent review remain.'}]})
    print(json.dumps({'hit_counts':{k:len(v) for k,v in hits.items()},'hit_paths':{k:sorted({x['public_path'] for x in v}) for k,v in hits.items()},'inputs':len(INPUTS)},indent=2))
if __name__=='__main__':main()
