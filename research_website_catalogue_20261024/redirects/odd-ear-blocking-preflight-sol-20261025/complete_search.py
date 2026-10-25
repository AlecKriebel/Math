"""Complementary normalized full-identity and target-model searches of pinned texts."""
from pathlib import Path
import json,re,unicodedata,subprocess,datetime,hashlib
E=Path(__file__).resolve().parent;G=E.parents[2];PIN='ebd3c1c3040634fe0cff28765f86ed4b84dad488'
def norm(t):
 t=unicodedata.normalize('NFKC',t).replace('\u00ad','');t=re.sub('[‐‑‒–—−]','-',t);t=re.sub(r'-\s+','-',t);return ' '.join(t.split())
queries={'100_title':r'NP-completeness of the initial odd-ear prefix','100_id_DOI':r'23576280|10[.]5281/zenodo[.]23576280','100_exact_model':r'odd[- ]ear|open ear decomposition|consecutive odd ears|factor[- ]critical|Benchetrit|perfectly matchable|block[- ]loss','101_title':r'NP-completeness of three-terminal shortest-path blocking','101_id_DOI':r'23331258|10[.]5281/zenodo[.]23331258','101_exact_model':r'shortest[- ]path block|blocking shortest paths|three[- ]terminal shortest|terminal geodesic|Krause|Khachiyan|interdiction'}
compiled={k:re.compile(v,re.I) for k,v in queries.items()};rows=[];pdf=json.loads((E/'PDF_IDENTITIES.json').read_text());tree=json.loads((E/'docs-tree.json').read_text())
for x in pdf:
 t=norm((E/x['text_path']).read_text());rows.append({'kind':'complete_PDF_text','path':x['path'],'blob':x['blob'],'pages':x['pages'],'normalized_characters':len(t),'hits':{k:[{'match':m.group(),'context':t[max(0,m.start()-140):min(len(t),m.end()+220)]} for m in pat.finditer(t)] for k,pat in compiled.items()}})
textsuffix={'.html','.xml','.txt','.md','.tex','.json','.bib','.yml','.yaml','.cff','.py','.js','.css'}
for x in tree:
 if Path(x['path']).suffix.lower() not in textsuffix:continue
 b=subprocess.run(['git','cat-file','blob',x['blob']],cwd=G,capture_output=True,check=True).stdout;t=norm(b.decode('utf-8',errors='replace'));rows.append({'kind':'complete_tracked_text_blob','path':x['path'],'blob':x['blob'],'hits':{k:[{'match':m.group(),'context':t[max(0,m.start()-140):min(len(t),m.end()+220)]} for m in pat.finditer(t)] for k,pat in compiled.items()}})
x={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pin':PIN,'queries':queries,'normalization':'Unicode NFKC; remove soft hyphen; normalize dash/minus characters; join linewrapped hyphenations; fold whitespace; case insensitive','rows':rows,'nonempty_target_hits':[{'path':x['path'],'hits':{k:v for k,v in x['hits'].items() if v}} for x in rows if any(x['hits'].values())],'limits':'Search of literal complete extractable PDF text and tracked textual docs; no nested support archive extraction; not a human full semantic reading of every unrelated article.'}
(E/'NORMALIZED_IDENTITY_SEARCH.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'PDF_readers':len(pdf),'tracked_text_blobs':len(rows)-len(pdf),'nonempty_hits':x['nonempty_target_hits']},ensure_ascii=False,indent=2))
