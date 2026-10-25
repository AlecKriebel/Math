from pathlib import Path
import json,re,unicodedata,datetime
E=Path(__file__).resolve().parent
def norm(t):
 t=unicodedata.normalize('NFKC',t).replace('\u00ad','');t=re.sub('[‐‑‒–—−]','-',t);t=re.sub(r'-\s+','-',t);return ' '.join(t.split()).casefold()
pdf=json.loads((E/'PDF_IDENTITIES.json').read_text());targets=json.loads((E/'TARGET_IDENTITIES.json').read_text());rows=[]
for rid,x in targets.items():
 t=norm((E/'cache'/('target-'+rid+'.txt')).read_text());title=norm(x['metadata']['title']);rows.append({'case':'actual_target_full_title_control','record_id':rid,'pass':title in t,'title':x['metadata']['title']})
for path,term in [('docs/papers/odd-part-slow-variation/paper.pdf','odd-part ratio under slow variation'),('docs/papers/knudson-gradient-path/paper.pdf','persistence-gradient conjecture'),('docs/papers/eternal-domination-lovasz-theta/paper.pdf','Lovász theta function')]:
 x=next(v for v in pdf if v['path']==path);rows.append({'case':'known_legacy_positive_identity_control','path':path,'query':term,'pass':norm(term) in norm((E/x['text_path']).read_text())})
q={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if all(x['pass'] for x in rows) else 'ISSUES_FOUND','rows':rows,'limits':'Controls establish that exact normalized known identities are found; they do not turn empty target results into a worldwide absence theorem.'};(E/'QUERY_CONTROLS.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(q,ensure_ascii=False,indent=2))
