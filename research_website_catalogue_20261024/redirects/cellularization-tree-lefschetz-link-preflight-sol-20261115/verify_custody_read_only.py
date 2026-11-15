#!/usr/bin/env python3
"""Pure offline custody only: no writes, subprocesses, network or foreign code."""
from pathlib import Path, PurePosixPath
from html.parser import HTMLParser
import hashlib, json, re, sys, unicodedata
O=Path(__file__).resolve().parent
EXCLUDED={'OWNED_MANIFEST.json','FINAL_SEAL.json'}
N=0
def need(v,m):
 global N
 N+=1
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def native(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def bound(r,base=None):
 if base:
  q=PurePosixPath(r['path']);need(not q.is_absolute() and '..' not in q.parts and str(q)==r['path'],'Unsafe owned path');p=base/r['path'];need(p.resolve().is_relative_to(base),'Owned path escape')
 else:p=Path(r['path']);need(p.is_absolute(),'External path not absolute')
 need(p.is_file() and not p.is_symlink(),'Missing or symlink input '+str(p));b=p.read_bytes()
 need(len(b)==r['bytes'] and sha(b)==r.get('SHA256',r.get('sha256')),'Changed byte binding '+str(p));return b
def api(n):
 x=load(O/'raw'/n);need(x.get('isError') is False,'Native tool error');return json.loads(x['structuredContent']['content'])
def tree_sha(entries):
 b=b''
 for r in sorted(entries,key=lambda r:(r['path']+('/' if r['type']=='tree' else '')).encode()):b+=r['mode'].lstrip('0').encode()+b' '+r['path'].encode()+b'\0'+bytes.fromhex(r['sha'])
 return native('tree',b)
def normalized(s):return ' '.join(unicodedata.normalize('NFKC',s).replace('–','-').replace('—','-').casefold().split())
class HTML(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.visible=[];self.hidden=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.hidden+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.hidden=max(0,self.hidden-1)
 def handle_data(self,t):
  if not self.hidden:self.visible.append(t)

def main(preseal):
 m=load(O/'OWNED_MANIFEST.json');need(m['excluded_terminal_files']==sorted(EXCLUDED),'Terminal exclusions')
 paths=set()
 for r in m['files']:bound(r,O);need(r['path'] not in paths,'Duplicate owned path');paths.add(r['path'])
 need(paths=={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()}-EXCLUDED,'Owned inventory completeness')
 inputs=load(O/'INPUT_MANIFEST.json')['files'];external=set()
 for r in inputs:bound(r);need(r['path'] not in external,'Duplicate external path');external.add(r['path'])
 c=load(O/'CORPUS_AUTHENTICATION.json');D=Path(c['prior_packet'])
 oldseal=load(D/'FINAL_SEAL.json');oldm=load(D/'OWNED_MANIFEST.json')
 need(sha((D/'OWNED_MANIFEST.json').read_bytes())==oldseal['OWNED_MANIFEST_SHA256'],'Prior final seal')
 for r in oldm['files']:bound(r,D)
 need(len(oldm['files'])==299 and {r['path'] for r in oldm['files']}=={p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()}-set(oldm['excluded_terminal_files']),'Prior whole299inventory')
 boundary=load(O/'REMOTE_BOUNDARY.json');need(boundary['opening']['docs']==boundary['closing']['docs']=='f5f5fb2fb18196b604d7b568e3e58ccc1bf127b3','Exact current docs boundary')
 for phase in ['start','end']:
  ref=api('remote-main-'+phase+'.json');commit=api('remote-commit-'+phase+'.json');root=api('remote-root-'+phase+'.json');docs=api('remote-docs-'+phase+'.json')
  point=boundary['opening' if phase=='start' else 'closing']
  need(ref['object']['sha']==commit['sha']==point['commit'],'Actual ref/commit')
  cb=(O/'raw'/('native-commit-'+phase+'.raw')).read_bytes();need(native('commit',cb)==point['commit'] and cb.splitlines()[0]==('tree '+point['root']).encode(),'Native commit body/root')
  need(root['sha']==commit['tree']['sha']==point['root'] and tree_sha(root['tree'])==root['sha'],'Actual native root tree')
  need(root['truncated'] is False and docs['truncated'] is False,'Remote trees complete')
  need(next(r['sha'] for r in root['tree'] if r['path']=='docs')==docs['sha']==point['docs'],'Actual root/docs chain')
  dirs={'':docs['sha']}|{r['path']:r['sha'] for r in docs['tree'] if r['type']=='tree'}
  need(len(dirs)==51,'Complete docs tree objects')
  for directory,oid in dirs.items():
   entries=[]
   for r in docs['tree']:
    p=PurePosixPath(r['path']);parent='' if str(p.parent)=='.' else str(p.parent)
    if parent==directory:entries.append(dict(r,path=p.name))
   need(tree_sha(entries)==oid,'Native recursive tree '+directory)
 need(api('remote-docs-start.json')==api('remote-docs-end.json'),'Whole closing docs equality')
 old={r['path']:r for r in load(D/'CURRENT_BLOB_BINDINGS.json')};rows=load(O/'CURRENT_BLOB_BINDINGS.json');new={r['path']:r for r in rows}
 leaves={'docs/'+r['path']:r for r in docs['tree'] if r['type']=='blob'};need(len(old)==len(new)==len(leaves)==254 and set(old)==set(new)==set(leaves),'Complete leaf sets')
 need(sum(r['original_bytes'] for r in rows)==40689089 and sum(r['bytes'] for r in rows)==40684709,'Complete body byte totals')
 representations=[]
 for r in rows:
  q=old[r['path']];ob=Path(r['original_body_path']).read_bytes();b=Path(r['current_body_path']).read_bytes()
  need(native('blob',ob)==q['blob']==r['original_blob'] and len(ob)==q['bytes']==r['original_bytes'] and sha(ob)==q['sha256']==r['original_SHA256'],'Whole original blob body')
  need(native('blob',b)==r['blob']==leaves[r['path']]['sha'] and len(b)==r['bytes'] and sha(b)==r['SHA256'],'Whole current blob body')
  rp=D/'corpus'/f"{q['blob']}.raw"
  if rp.exists():
   need(rp.read_bytes()==ob,'Original cached raw equality')
   source=O/'private/current-strict-gap.html' if r['path']=='docs/papers/strict-dirichlet-gap/index.html' else rp
   need(source.read_bytes()==b,'Current raw representation exact body');representations.append((r['path'],'raw_UTF8',str(source),source.read_text()))
   if r['path'].endswith('.html'):
    v=D/'corpus'/f"{q['blob']}.visible.txt"
    if r['path']=='docs/papers/strict-dirichlet-gap/index.html':v=O/'private/current-strict-gap.visible.txt'
    p=HTML();p.feed(source.read_text());need(v.read_text()==' '.join(p.visible),'Whole decoded HTML equality');representations.append((r['path'],'decoded_HTML',str(v),v.read_text()))
 delta=[r for r in rows if r['blob']!=r['original_blob']];need(len(delta)==1 and delta[0]['path']=='docs/papers/strict-dirichlet-gap/index.html' and delta[0]['bytes']==838 and delta[0]['SHA256']=='dedb9326ddf053603601dc22355b00c555ed1ec05a8767b6119bcec03455965c','Exact sole known delta')
 extracts=load(O/'REUSED_EXTRACT_BINDINGS.json');need(len(extracts)==76 and len({r['path'] for r in extracts})==73 and sum(r['pages'] for r in extracts)==854,'Whole reusable PDF coverage')
 for r in extracts:
  b=bound(r);need(new[r['public_path']]['blob']==r['pdf_blob'] and new[r['public_path']]['SHA256']==r['pdf_sha256'],'Exact PDF/extraction source identity');representations.append((r['public_path'],'reused_complete_PDF_text',r['path'],b.decode()))
 need(len(representations)==260,'Complete identity representations')
 results=load(O/'SEARCH_RESULTS.json')
 for name,pattern in results['queries'].items():
  actual=[]
  for path,kind,source,t in representations:
   matches=list(re.finditer(pattern,normalized(t)))
   if matches:actual.append((path,kind,source,len(matches)))
  recorded=[(r['public_path'],r['representation'],r['path'],r['occurrences']) for r in results['hits'][name]]
  need(actual==recorded and len(actual)==results['hit_representation_counts'][name],'Whole corpus search reproducibility '+name)
 for row in ['121','122','127','128']:
  for q in ['record_concept','title','distinctive']:need(results['hits'][row+'_'+q]==[],'Core identity negative')
 secondary=load(O/'PUNCTUATION_INSENSITIVE_SEARCH.json')
 for row,needles in secondary['needles'].items():
  found=[]
  for path,kind,source,t in representations:
   flat=re.sub(r'[^a-z0-9]','',normalized(t));matched=[n for n in needles if n in flat]
   if matched:found.append({'public_path':path,'representation':kind,'path':source,'matched_needles':matched})
  need(found==secondary['hits'][row]==[],'Punctuation-insensitive corpus negative')
 receipts=load(O/'WHOLEBODY_TRANSPORT_RECEIPTS.json');need(len(receipts['responses'])==9 and receipts['mutation_calls']==0,'Native read response count')
 for r in receipts['responses']:
  envelope=json.loads(bound(r['stored_actual_tool_response']));body=envelope['structuredContent']['content'].encode();need(len(body)==r['whole_native_content_bytes'] and sha(body)==r['whole_native_content_SHA256'] and envelope['isError'] is False,'Whole actual tool content receipt')
 targets=load(O/'TARGET_IDENTITIES.json');need([t['record_id'] for t in targets]==['23439582','23440389','23570763','23331295'],'Four native targets')
 for t in targets:
  j=json.loads(bound(t['config']));s=j['source_binding']['whole_original_source_ready'];rn=s['selected_actual_PDF'];pdf=bound(rn);need(pdf==Path(j['source_binding']['whole_original_source_ready']['selected_actual_PDF']['path']).read_bytes(),'Actual whole PDF identity')
  tex=s['controlling_TeX'];tp=Path(tex.get('path',tex.get('extracted_path')));need(len(tp.read_bytes())==tex['bytes'] and sha(tp.read_bytes())==tex['SHA256'],'Actual controlling TeX identity')
  record=json.loads(bound(next(q for q in s['whole_native_API_objects'] if q['role']=='record')));md=record['metadata'];need(str(record['id'])==t['record_id'] and record['doi']==j['doi']==t['fields']['doi'],'Native record/DOI identity')
  need((md['title'],md['version'],md['publication_date'])==(j['title'],j['version'],j['publication_date']),'Native actual metadata')
  need(j['canonical_url'] is None and j['AA'] is None,'Frozen literal target flags')
  for a in t['all_native_assets_in_original_order']:
   b=bound(a);k=a['original_api_file_object'];need(len(b)==k['size'] and hashlib.md5(b).hexdigest()==k['checksum'].split(':')[1],'Native asset whole MD5/size')
   need(not any(r['SHA256']==sha(b) for r in rows),'No native asset corresponding docs path')
  need(all(not x for x in t['native_asset_equal_docs_paths'].values()),'Literal target asset equality negatives')
 need(next(t for t in targets if t['record_id']=='23331295')['fields']['printed_version'] is None,'Absent printed version preserved')
 exclusions=load(O/'EXCLUSIONS.json');need(exclusions['genuine_candidate_HTML_count']==0 and len(exclusions['items'])==2 and all(r['correspondence'] is False for r in exclusions['items']),'Both full falsehit exclusions')
 verdict=load(O/'VERDICT.json');need(set(verdict['records'])=={t['record_id'] for t in targets} and verdict['redirects_written']==[],'Four dispositions and no writes')
 for r in verdict['records'].values():need(r['literal_VERDICT']=='BOUNDED_NEGATIVE_NO_GENUINE_CORRESPONDING_OLD_HTML_ARTICLE_LOCATED' and r['legacy_HTML_URL'] is None and r['proposed_redirect_target'] is None and r['redirect_authorized_now'] is False,'Literal record no-redirect verdict')
 need(verdict['science_reopened_or_checkers_run'] is False and verdict['source_site_core_Sheet_Gitref_localindex_deploy_contact_mutations'] is False,'Task mutation/execution boundary')
 if not preseal:
  s=load(O/'FINAL_SEAL.json');need(s['OWNED_MANIFEST_SHA256']==sha((O/'OWNED_MANIFEST.json').read_bytes()),'Final manifest seal')
  for name in ['REPORT.md','VERDICT.json','INPUT_MANIFEST.json','verify_custody_read_only.py']:need(s['sealed_payload_SHA256'][name]==sha((O/name).read_bytes()),'Final selected seal '+name)
 print(json.dumps({'verdict':'PASS','mode':'preseal' if preseal else 'sealed','checks':N,'owned_payloads':len(paths),'external_byte_bindings':len(inputs),'whole_original_blobs':254,'whole_current_blobs':254,'current_docs_tree':boundary['closing']['docs'],'actual_root_docs_tree_responses':4,'authenticated_docs_tree_objects_per_boundary':51,'identity_representations':260,'reused_PDF_path_occurrences':76,'reused_PDF_pages':854,'new_PDF_extractions':0,'network_requests':0,'writes':0,'subprocesses':0,'scientific_or_prior_code_executions':0},sort_keys=True))
if __name__=='__main__':
 need(sys.argv[1:] in [[],['--preseal']],'Usage: verify_custody_read_only.py [--preseal]')
 main(sys.argv[1:]==['--preseal'])
