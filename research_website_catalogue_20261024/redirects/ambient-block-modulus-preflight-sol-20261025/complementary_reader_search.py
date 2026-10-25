from pathlib import Path
from pypdf import PdfReader
from io import BytesIO
import re,json,subprocess,hashlib,time
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024');G=Path('/Users/alec/Documents/Math');O=P/'redirects/ambient-block-modulus-preflight-sol-20261025';pdfs=json.loads((O/'pdf-identity-inventory.json').read_text());queries={
 '97_exact_title':r'ambient dependence of extremal-exchangeable independence','97_record':r'23333353','97_distinctive':r'liebscher|extremal[- ]exchangeable|extreme exchangeable|quantum independence|state-preserving inclusion|free[- ]product state',
 '98_exact_title':r'an effective criterion for prescribed block-code extensions','98_record':r'23416806','98_distinctive':r'block[- ]code|sofic|steadiness|locally testable|van rooijen|zeitoun|symbolic dynamics|finite-type approximation',
 '99_exact_title':r'infinite modulus between a compact real set and its real complement','99_record':r'23441617','99_distinctive':r'real complement|compact real set|hayman|lingham|\bgon.car\b|\b7\.58\b|conformal.{0,30}capacity|planar.{0,20}modulus'}
compiled={k:re.compile(v,re.I) for k,v in queries.items()};results=[];first=[]
for x in pdfs:
 b=subprocess.run(['git','cat-file','blob',x['blob']],cwd=G,stdout=subprocess.PIPE,check=True,timeout=15).stdout;r=PdfReader(BytesIO(b));pages=[p.extract_text() or '' for p in r.pages];raw='\n'.join(pages);t=raw.replace('\u00ad','').replace('–','-').replace('—','-').replace('‐','-');t=re.sub(r'-\s+','-',t);t=' '.join(t.split())
 hits={k:[{'match':m.group(),'context':t[max(0,m.start()-120):min(len(t),m.end()+180)]} for m in pat.finditer(t)] for k,pat in compiled.items()}
 results.append({'path':x['path'],'blob':x['blob'],'sha256':x['sha256'],'PDF_pages':len(pages),'normalized_character_count':len(t),'hits':hits})
 first.append({'path':x['path'],'blob':x['blob'],'sha256':x['sha256'],'metadata_title':x['metadata'].get('/Title'),'first_page_text':pages[0]})
 if not x['metadata'].get('/Title'):print(x['path'],'FIRST_LINES',pages[0].splitlines()[:9])
(O/'PDF_COMPLEMENTARY_SEARCH.json').write_text(json.dumps({'normalization':'Remove soft hyphen; normalize Unicode dash; join hyphenated line breaks; fold whitespace; case-insensitive.','queries':queries,'results':results},indent=2)+'\n');(O/'cache/pdf-firstpage-identity.json').write_text(json.dumps(first,indent=2)+'\n')
print('ALL_TARGET_HITS',[(r['path'],{k:v for k,v in r['hits'].items() if v}) for r in results if any(r['hits'].values())])
