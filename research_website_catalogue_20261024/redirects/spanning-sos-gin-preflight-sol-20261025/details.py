"""Bounded actual-body followup of weak hits; no redirect construction."""
from pathlib import Path
import json,re,subprocess,xml.etree.ElementTree as ET
from scan import O,P,G,C,PIN,git,blob,sha,HTML,save,checkpoint

inventory=json.loads((O/'html-identity-inventory.json').read_text())
for row in inventory['documents']:
    parser=HTML(blob(row['path']).decode());row['h1']=' '.join(parser.h1)
save('html-identity-inventory.json',inventory)

queries=json.loads((O/'text-inventory.json').read_text())['queries']
pdf=json.loads((O/'pdf-identity-inventory.json').read_text())['documents']
contexts=[]
for row in pdf:
    if not row.get('query_hits'):continue
    body=Path(row['ignored_full_text_cache_path']).read_text();hits=[]
    for name in row['query_hits']:
        for match in re.finditer(queries[name],body,re.I):
            hits.append({'query':name,'page':body.count('\f',0,match.start())+1,'matched':match.group(0),'context':' '.join(body[max(0,match.start()-140):match.end()+220].split())})
    contexts.append({'path':row['path'],'SHA256':row['SHA256'],'pages':row['pages'],'identity_prefix':row['first_page_identity_prefix'],'hits':hits})
# All rendered/full text bodies stay in this ignored cache, including hit contexts.
(C/'weak-hit-contexts.json').write_text(json.dumps(contexts,indent=2,ensure_ascii=False)+'\n')

for path in ['docs/papers/fps-equality/index.html','docs/papers/fps-equality/paper.pdf','docs/papers/fps-equality/paper.tex']:
    data=blob(path);out=C/path;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
for path in ['docs/papers/cyclic-bell-exact-values-and-randomness/index.html','docs/papers/equal-sum-product/index.html','docs/papers/no-universal-death-birth-amplifier/index.html','docs/papers/gamma-theta-order-12-frontier/index.html']:
    data=blob(path);out=C/path;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data);(out.with_suffix('.visible.txt')).write_text(' '.join(' '.join(HTML(data.decode()).parts).split()))

top=git('ls-tree','--name-only',PIN).decode().splitlines();matches=[p for p in top if re.search(r'spanning|convex|sos|seven|gin|jacobian|root.dependent',p,re.I)]
save('non-public-root-path-boundary.json',{'pin':PIN,'root_entry_count':len(top),'matching_top_level_names':matches,'scope':'Top-level project names are not GitHub Pages article routes; no such name is accepted as a correspondence.'})
raw=git('grep','-n','-I','-i','-E','-e',r'23181280|root.dependent|Kaibel|23442760|Lasserre|SOS|Lebesgue|23395703|generic.initial|revlex|Palezzato|Torielli|Hilbert.Burch|hyperplane',PIN,'--','docs')
(C/'supplemental-pinned-text-grep.txt').write_bytes(raw)
paths=sorted({line.split(':',2)[1] for line in raw.decode().splitlines()})
save('supplemental-search-boundary.json',{'pin':PIN,'command':'git grep -n -I -i -E exact-pin -- docs','regex':r'23181280|root.dependent|Kaibel|23442760|Lasserre|SOS|Lebesgue|23395703|generic.initial|revlex|Palezzato|Torielli|Hilbert.Burch|hyperplane','matching_paths':paths,'raw_results_ignored_cache':str(C/'supplemental-pinned-text-grep.txt')})
renders=[]
specs=[('23181280',P/'papers/23181280/sources/root_dependent_spanning_trees.pdf',4),('23442760',P/'papers/23442760/sources/Convex_Body_SOS_Density_Note_v1.0.pdf',5),('23395703',P/'papers/23395703/sources/seven_plane_gin.pdf',6),('excluded-fps',C/'docs/papers/fps-equality/paper.pdf',4)]
for rid,path,last in specs:
    for page in [1,last]:
        prefix=C/(rid+'-page'+str(page))
        subprocess.run(['/opt/homebrew/bin/pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1200','-singlefile','-png',str(path),str(prefix)],check=True,capture_output=True)
        out=prefix.with_suffix('.png');renders.append({'record_or_exclusion':rid,'PDF_path':str(path),'PDF_SHA256':sha(path.read_bytes()),'page':page,'render_path':str(out),'render_SHA256':sha(out.read_bytes())})
save('selected-render-custody.json',{'images':renders,'scope':'Identity/edition/last-page inspection; all actual current PDF text and controlling TeX read separately; not a full visual reading of every old PDF.'})
checkpoint('No record/title/core GIN or aggregate-root article found in pinned HTML/text. Only weak convex-body/SOS identities and one generic spanning-tree lemma remain to exclude; actual current manuscripts fully read and selected identity pixels ready.',80)
print(json.dumps({'status':'DETAILS_READY','supplemental_hit_paths':paths,'top_level_matches':matches,'selected_renders':len(renders)},indent=2))
