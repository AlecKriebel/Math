"""Read-only bounded replay: no network, PDF extraction, writes, or source execution."""
import sys,io,zipfile
sys.dont_write_bytecode=True
from preflight_core import *

preseal=sys.argv[1:]==['--preseal']
need(preseal or not sys.argv[1:],'Usage: verify_read_only.py [--preseal]')
if not preseal:
    seal=load(O/'FINAL_SEAL.json');m=load(O/'OWNED_MANIFEST.json')
    need(sha((O/'OWNED_MANIFEST.json').read_bytes())==seal['manifest_sha256'],'Owned manifest seal')
    expected={x['path'] for x in m['files']}|{'OWNED_MANIFEST.json','FINAL_SEAL.json'}
    actual={str(p.relative_to(O)) for p in O.rglob('*') if p.is_file()}
    need(actual==expected,'Exact closed owned inventory')
    for x in m['files']:
        p=O/x['path'];need(not p.is_symlink(),'Owned symlink')
        need(binding(p)=={k:x[k] for k in ['bytes','sha256']},'Owned payload '+x['path'])
    need(len(m['files'])==seal['owned_payloads'],'Owned payload count')

pin=load(O/'PIN.json')
need(pin['released_commit']==COMMIT and pin['released_docs_tree']==TREE,'Released pin')
need(pin['local_HEAD_preserved']=='a4ce3c37dad209339e490d18dcced6c48cf912d2','Local/released distinction')
for typ,oid in [('commit',COMMIT),('tree',TREE)]:
    b=(O/('git-object-'+oid+'.raw')).read_bytes()
    need(hashlib.sha1((typ+' '+str(len(b))+'\0').encode()+b).hexdigest()==oid,'Saved Git object SHA1')
    need(git('cat-file',typ,oid)==b,'Actual immutable Git object')
bindings,extracts,reps,html,data,listing=corpus()
need(bindings==load(O/'DOCS_OBJECT_BINDINGS.json'),'Complete public blob bindings')
need(extracts==load(O/'REUSED_EXTRACT_BINDINGS.json'),'Reused extract bindings')
need(html==load(O/'HTML_IDENTITIES.json'),'Actual HTML identity inventory')
need(listing==(O/'docs-tree.raw.z').read_bytes(),'Exact recursive released listing')
for p in (O/'selected-released-blobs').iterdir():
    path=p.name.replace('__','/');need(data[path]==p.read_bytes(),'Selected actual article blob '+path)

source=load(O/'SOURCE_BINDINGS.json')
for x in source:need(binding(x['path'])=={k:x[k] for k in ['bytes','sha256']},'Selected original input '+x['path'])
for x in load(O/'EDITORIAL_PUBLICATION_BINDINGS.json')['records']:
    for k in ['manifest','seal','publication']:
        y=x[k];need(binding(y['path'])=={k:y[k] for k in ['bytes','sha256']},'Final selected editorial '+k)
    s=load(x['seal']['path'])
    need(s['manifest_sha256']==x['manifest']['sha256'] and s['publication_sha256']==x['publication']['sha256'],'Final editorial publication seal')
    p=load(x['publication']['path'])
    need(p['canonical_url'] is None and p['slug']==x['proposed_slug'] and p['proposed_canonical_url']==x['proposed_canonical_url'],'Proposed private slug/canonical distinction')
auth=load(O/'NATIVE_SOURCE_AUTHENTICATION.json')
for x in auth['additional_external_bindings']:
    need(binding(x['path'])=={k:x[k] for k in ['bytes','sha256']},'Native source seal/manifest')
for x in auth['records']:
    s=load(x['native_seal']['path']);m=load(x['native_manifest']['path'])
    need(sha(Path(x['native_manifest']['path']).read_bytes())==s[x['original_manifest_digest_selector']],'Native original manifest seal')
    T=P/'papers'/x['record'];ready=T/'sources/SOURCE_READY.json'
    need(sha(ready.read_bytes())==s[x['original_readiness_digest_selector']],'Native readiness seal')
    for y in x['selected_originals_authenticated']:
        e=next(e for e in m['files'] if e['path']==y['native_relative_path'])
        need(binding(y['path'])=={'bytes':e['bytes'],'sha256':e[y['original_manifest_digest_field']]},'Native selected member')

target=load(O/'TARGET_IDENTITIES.json');q=queries(target)
for r,x in target.items():
    raw=load(P/'papers'/r/'sources/record.raw.json')
    need((x['title'],x['DOI'],x['native_version'])==(raw['title'],raw['doi'],raw['metadata'].get('version')),'Native target identity')
    need(x['canonical_url'] is None and x['AA'] is None,'No invented published canonical/AA')
    for i,a in enumerate(x['assets_in_native_order']):
        b=Path(a['path']).read_bytes();f=raw['files'][i]
        need(len(b)==f['size'] and hashlib.md5(b).hexdigest()==f['checksum'].split(':',1)[1],'Native asset order and MD5')
        need(sha(b)==a['sha256'],'Native selected full asset SHA256')
    for t in x['native_TeX_link_bindings']:
        need(re.findall(r'https?://[^\s<>}]+',Path(t['path']).read_text())==t['literal_urls_in_order'],'Native literal TeX URLs')
saved=load(O/'SEARCH_RESULTS.json')
need(q==saved['queries'] and search(reps,q)==saved['representations'],'Complete search replay')
need(controls(reps,target)==load(O/'QUERY_CONTROLS.json'),'Positive controls')
# Recompute the independently selected additional alias families without executing
# its writer program. Preserve every raw-HTML attribute hit as a separate route.
ind=load(O/'independent-check/ALIAS_IDENTITY_EVIDENCE.json')
by={x['path']:x for x in bindings};ihits={'hits':[],'raw_HTML_hits':[]}
for group,pattern in ind['queries'].items():
    for item in reps:
        text=norm(item['text'])
        hits=[{'match':m.group(),'offset':m.start(),'context':text[max(0,m.start()-100):m.end()+160]} for m in re.finditer(pattern,text,re.I)]
        if hits:
            row={'group':group,'path':item['path'],'kind':item['kind'],'released_binding':by[item['path']],'hits':hits}
            key='raw_HTML_hits' if item['kind']=='raw_UTF8_blob' and item['path'].endswith('.html') else 'hits'
            ihits[key].append(row)
need(all(ihits[k]==ind[k] for k in ihits),'Independent additional alias full replay')
need(ind['article_identities']==html,'Independent all HTML identities')
need(not any(x['group'] in ['yamabe_aliases','bianchi_aliases'] for v in ihits.values() for x in v),'Independent extra Yamabe/Bianchi aliases')
birational_excluded={'docs/papers/hadamard-668-lp333/paper.pdf','docs/papers/knudson-gradient-path/independent_check.py',
 'docs/papers/knudson-gradient-path/verification-report.md','docs/papers/reversible-mass-action-continuum/files/manuscript-v1.0.0.pdf',
 'docs/research/reversible-mass-action-realization-theory/index.html','docs/papers/reversible-mass-action-continuum/index.html'}
need({x['path'] for v in ihits.values() for x in v if x['group']=='birational_aliases'}==birational_excluded,'Every extra generic prime-field candidate explicitly excluded')
for r in ['23383952','23539734','23320818']:
    for suffix in ['record_or_DOI','exact_title','distinctive']:
        need(not any(x['groups'][r+'_'+suffix] for x in saved['representations']),'Negative identity/differentiating term hit')
for r in ['23539734','23320818']:
    need(not any(x['groups'][r+'_broad'] for x in saved['representations']),'Unresolved broad candidate')
ex=load(O/'EXCLUSIONS.json')
allowed={x['path'] for x in ex['weighted_Yamabe_false_positive_readers']}|{'docs/papers/unified-consequences/index.html'}
need({x['path'] for x in saved['representations'] if x['groups']['23383952_broad']}==allowed,'Every broad Yamabe candidate excluded explicitly')
e=load(O/'SELECTED_IDENTITY_EVIDENCE.json');path=e['current_article']['path']
need(e['current_article']==next(x for x in bindings if x['path']==path),'Exact positive actual article')
article=data[path].decode();h=HTMLIdentity();h.feed(article)
legacy='https://aleckriebel.github.io/Math/papers/gromov-unitary-lipschitz/'
need(h.canonicals==[legacy] and target['22929857']['title'] in article,'Positive title/self canonical')
need('https://zenodo.org/records/22929857' in h.links and target['22929857']['DOI'] in article,'Positive native record/DOI link')
need('Version 1.1' in article and '23 September 2026' in article,'Positive declared version/date')
need('paper.pdf' in h.links and 'reproducibility.zip' in h.links,'Positive actual download links')
need(any(x.get('identifier')==legacy and x.get('relation')=='isDocumentedBy' for x in target['22929857']['native_related_identifiers']),'Native explicit project relation')
for name in ['paper.pdf','reproducibility.zip']:
    native=next(x for x in target['22929857']['assets_in_native_order'] if Path(x['path']).name==name)
    need(data['docs/papers/gromov-unitary-lipschitz/'+name]==Path(native['path']).read_bytes(),'Public/native exact same asset '+name)
z=zipfile.ZipFile(io.BytesIO(data['docs/papers/gromov-unitary-lipschitz/zenodo-upload.zip']))
need(z.testzip() is None,'Selected kit CRC')
need([{'name':x.filename,'bytes':len(z.read(x)),'sha256':sha(z.read(x))} for x in z.infolist()]==e['predeposit_upload_kit']['members'],'Selected kit payload identities')
need(json.loads(z.read('metadata.json'))['version']=='1.1','Same version kit')
for name in ['paper.pdf','reproducibility.zip']:need(z.read(name)==data['docs/papers/gromov-unitary-lipschitz/'+name],'Same version kit payload')
from pypdf import PdfReader
reader=PdfReader(P/'papers/22929857/sources/paper.pdf')
uris=[]
for i,p in enumerate(reader.pages):
    for a in p.get('/Annots',[]):
        action=a.get_object().get('/A')
        if action and action.get('/URI'):uris.append((i+1,str(action.get('/URI'))))
need(len(reader.pages)==4 and (4,legacy) in uris,'Native actual PDF project annotation')
cr=load(O/'CORPUS_RECEIPT.json')
need((cr['public_blobs'],cr['HTML'],cr['PDFs'],cr['complete_reused_PDF_pages'],cr['search_representations'],cr['raw_UTF8_blobs'])==
     (len(bindings),len(html),len(extracts),sum(x['pages'] for x in extracts),len(reps),sum(x['kind']=='raw_UTF8_blob' for x in reps)),'Exact corpus receipt counts')
hashes={a['sha256']:r for r,t in target.items() for a in t['assets_in_native_order']}
matches=[{'public_path':x['path'],'record':hashes[x['sha256']],**x} for x in bindings if x['sha256'] in hashes]
need(matches==cr['exact_full_asset_matches'] and len(matches)==2 and {x['record'] for x in matches}=={'22929857'},'All8 native full assets compared to all254 blobs')
need(cr['hit_representation_counts']=={g:sum(bool(x['groups'][g]) for x in saved['representations']) for g in q},'Exact hit counts')

v=load(O/'VERDICT.json');rec=v['records']
need(v['literal_custom_verdict']=='COMPLETE_BOUNDED_PREFLIGHT_ONE_EXACT_CORRESPONDENCE_THREE_CORPUS_NEGATIVES','Overall literal verdict')
need(set(rec)==set(RECORDS),'Four selected works only')
for r in RECORDS:
    expected='EXACT_CORRESPONDING_LEGACY_ARTICLE_SAME_PUBLISHED_VERSION' if r=='22929857' else 'NO_MATCH_FOUND_IN_EXACT_RELEASED_PUBLIC_DOCS_CORPUS'
    need(rec[r]['literal_custom_verdict']==expected,'Literal per-record verdict')
    need(rec[r]['canonical_url'] is None and rec[r]['AA'] is None,'No canonical/AA promotion')
need(v['root_only_authority'] and not v['redirect_authorized'] and not v['redirect_written'],'Root authority/no redirect')
need(v['new_old_PDF_extractions']==0 and not v['live_verified'],'No invented extraction/live gate')
closing=load(O/'CLOSING_RELEASE_PIN.json')
need(closing['released_docs_tree']==TREE,'Closing released docs scope')
print(json.dumps({'status':'PASS','public_blobs':len(bindings),'search_representations':len(reps),'reused_complete_PDFs':len(extracts),
 'reused_complete_PDF_pages':sum(x['pages'] for x in extracts),'native_selected_source_inputs':len(source),'native_source_packets':len(auth['records']),
 'positive_correspondences':1,'bounded_corpus_negatives':3,'old_PDF_extractions':0,'network_requests':0,'writes':0},sort_keys=True))
