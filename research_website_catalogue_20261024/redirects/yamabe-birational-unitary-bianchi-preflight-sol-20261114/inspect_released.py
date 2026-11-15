"""Write only this new preflight's evidence; core operations are read-only."""
from preflight_core import *
from datetime import datetime,timezone
def w(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
need(not (O/'SEARCH_RESULTS.json').exists(),'Refusing overwrite of completed scan')
utc=datetime.now(timezone.utc).isoformat()
bindings,extracts,reps,html,data,listing=corpus()
target,external=targets();q=queries(target);s=search(reps,q);cs=controls(reps,target)
remote=git('ls-remote','origin','refs/heads/main').decode()
need(remote.split()[0]==COMMIT,'Remote checkpoint moved; assess before proceeding')
pin={'UTC':utc,'released_remote_advertisement':remote,'released_commit':COMMIT,'released_docs_tree':TREE,
     'local_HEAD_preserved':git('rev-parse','HEAD').decode().strip(),
     'local_HEAD_docs_tree':git('rev-parse','HEAD:docs').decode().strip(),
     'git_dir':git('rev-parse','--absolute-git-dir').decode().strip(),
     'scope':'Released checkpoint objects, not local HEAD/worktree; no fetch, ref update, checkout, reset or index operation.'}
for n,x in [('PIN.json',pin),('DOCS_OBJECT_BINDINGS.json',bindings),('REUSED_EXTRACT_BINDINGS.json',extracts),
            ('PRIOR_PACKET_BINDINGS.json',prior_authenticate()),('TARGET_IDENTITIES.json',target),('SOURCE_BINDINGS.json',external),
            ('HTML_IDENTITIES.json',html),('QUERY_CONTROLS.json',cs),('SEARCH_RESULTS.json',{'queries':q,'representations':s})]:w(n,x)
(O/'docs-tree.raw.z').write_bytes(listing)
sel=O/'selected-released-blobs';sel.mkdir()
for path in ['docs/index.html','docs/sitemap.xml',*sorted(k for k in data if k.startswith('docs/papers/gromov-unitary-lipschitz/') and not k.endswith(('.pdf','.zip')))]:
    (sel/path.replace('/','__')).write_bytes(data[path])
hashes={a['sha256']:r for r,t in target.items() for a in t['assets_in_native_order']}
matches=[{'public_path':x['path'],'record':hashes[x['sha256']],**x} for x in bindings if x['sha256'] in hashes]
w('CORPUS_RECEIPT.json',{'UTC':utc,'released_commit':COMMIT,'docs_tree':TREE,'public_blobs':len(bindings),'HTML':len(html),'PDFs':len(extracts),
  'complete_reused_PDF_pages':sum(x['pages'] for x in extracts),'search_representations':len(reps),'raw_UTF8_blobs':sum(x['kind']=='raw_UTF8_blob' for x in reps),
  'new_old_PDF_extractions':0,'new_target_PDF_extractions':0,'binary_archive_texts_recursively_expanded':False,'exact_full_asset_matches':matches,
  'hit_representation_counts':{g:sum(bool(x['groups'][g]) for x in s) for g in q}})
print(json.dumps({'remote':remote.strip(),'counts':{g:sum(bool(x['groups'][g]) for x in s) for g in q},
 'candidate_paths':sorted({x['path'] for x in s if any(x['groups'].values())}),'full_asset_matches':matches},indent=2))
