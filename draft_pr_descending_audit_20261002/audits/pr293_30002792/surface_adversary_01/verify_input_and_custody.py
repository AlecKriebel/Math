from pathlib import Path
from html.parser import HTMLParser
import datetime,gzip,hashlib,json,os,re,sys
W=Path(__file__).resolve().parent
A=W.parent
MANIFEST=A/'snapshot_manifest.json'
EXCLUDE_NATIVE=sys.argv[1] if len(sys.argv)>1 else None
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes()
 return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'observed_mode':p.stat().st_mode&0o777}
def sha(b):return hashlib.sha256(b).hexdigest()
def write(name,data): (W/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
assert MANIFEST.stat().st_size==17475
assert sha(MANIFEST.read_bytes())=='8fe845421a5802daed352e99b4903797eb7ac98c1bc88592ac639d8f20fb0d1a'
m=json.loads(MANIFEST.read_bytes())
assert m['head']=='6e717193f93c8a321cce1ce35a00eed1ecfb56e7'
assert m['original_submitted_status']=='claimed_solved' and m['original_author_budget']=='2/5'
original=[]
for f in m['files']:
 p=Path(f['snapshot']['path'])
 b=p.read_bytes()
 assert p.is_relative_to(A/'snapshot')
 assert len(b)==f['snapshot']['bytes'] and sha(b)==f['snapshot']['sha256']
 blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert blob==f['git_blob']
 assert (p.stat().st_mode&0o777)==f['snapshot']['mode']==0o444
 original.append({'repository_path':f['path'],'pin':pin(p),'computed_git_blob':blob,'full_body_read_for_byte_authentication':True})
assert len(original)==19
native=[]
raw_source=[]
for d in sorted((W/'native').iterdir()):
 if d.name==EXCLUDE_NATIVE:continue
 r=json.loads((d/'request.json').read_bytes())
 start=json.loads((d/'started.json').read_bytes())
 e=json.loads((d/'execution.json').read_bytes())
 assert e['actual_child_PID']==start['actual_child_PID'] and e['actual_recorder_PID']==start['actual_recorder_PID']==r['actual_recorder_PID']
 assert e['parent_reaped_child'] is True and e['timed_out'] is False and e['exception'] is None
 assert datetime.datetime.fromisoformat(e['end_UTC'])>=datetime.datetime.fromisoformat(start['UTC'])>=datetime.datetime.fromisoformat(r['UTC'])
 expected=23 if int(d.name.split('_')[0])<=8 else 0
 assert e['exit_code']==expected
 src=gzip.decompress((d/'recorder_prelaunch.py.gz').read_bytes())
 assert len(src)==r['recorder_source']['bytes'] and sha(src)==r['recorder_source']['sha256']
 assert src==Path(r['recorder_source']['path']).read_bytes()
 for cs in r.get('child_sources',[]):
  b=gzip.decompress(Path(cs['prelaunch']['path']).read_bytes())
  assert len(b)==cs['source']['bytes'] and sha(b)==cs['source']['sha256']
  assert b==Path(cs['source']['path']).read_bytes()
 for stream in ('stdout','stderr'):
  p=d/(stream+'.bin'); b=p.read_bytes()
  assert len(b)==e[stream]['bytes'] and sha(b)==e[stream]['sha256']
 row={'directory':d.name,'request':r,'start':start,'execution':e,'runtime_file_modes_are_capture_time_not_final_freeze_modes':True,
      'envelope_files':[pin(p) for p in sorted(d.iterdir()) if p.is_file()]}
 native.append(row)
 argv=r['argv']
 if argv[0]=='/usr/bin/curl' and expected==0:
  out=Path(argv[argv.index('--output')+1]); hdr=Path(argv[argv.index('--dump-header')+1])
  assert out.is_relative_to(W/'private_sources') and hdr.is_relative_to(W/'private_sources')
  b=out.read_bytes(); hb=hdr.read_bytes()
  statuses=re.findall(rb'^HTTP/\S+\s+(\d+)',hb,re.M)
  assert statuses and statuses[-1]==b'200'
  if out.suffix=='.pdf':assert b.startswith(b'%PDF-') and b'%%EOF' in b[-2048:]
  if out.suffix=='.html':assert b and (b'<html' in b[:4096].lower() or b'<!doctype' in b[:4096].lower())
  raw_source.append({'url':argv[-1],'response_body':pin(out),'headers':pin(hdr),'native_capture':d.name,'HTTP_statuses':[int(x) for x in statuses],'private_archive_only':True})
assert len(native)==32 and len(raw_source)==13
class TextParser(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
derived=[]
for h in sorted((W/'private_sources').glob('*.html')):
 p=TextParser();p.feed(h.read_text()); fresh=''.join(p.parts)
 t=h.with_suffix('.txt'); existing=t.read_text()
 assert re.sub(r'\s+','',fresh)==re.sub(r'\s+','',existing)
 derived.append({'raw_html':pin(h),'derived_text':pin(t),'verification':'all non-whitespace characters exactly match fresh HTMLParser data extraction omitting script/style; original whitespace layout is not claimed byte-replayed'})
pages={
 'liedtke.txt':([1,13,14],'Picard/Albanese and H^2 obstruction consequence; relevant full pages'),
 'kleiman_picard.txt':([46,47],'Proposition 5.19 and entire proof'),
 'kleiman_hodge.txt':([75,76,77,78,79],'B.15-B.16 intersection projection formula; B.26 RR; B.27 and complete proof; B.28'),
 'milne_jacobians.txt':([1,5,6,19,20],'edition/correction statement; Jacobian dimension; Proposition 6.1 complete proof'),
 'milne_abelian.txt':([4,5,6,12,13,19,20],'genus-zero/dense-curves argument; isogenies; Poincare reducibility'),
 'janssen.txt':([1,8],'actual arbitrary-characteristic field convention and Question 3.1; scope, not priority'),
 'conrad_quotient.txt':([1],'Exercise 1 quotient construction; remainder of one-page sheet incidentally read, not relied upon')}
excerpt=W/'semantic_excerpts';excerpt.mkdir(exist_ok=False)
readscope=[]
for name,(chosen,purpose) in pages.items():
 path=W/'private_sources'/name;b=path.read_bytes();blocks=b.split(b'\f');offset=0;cuts=[]
 for i,block in enumerate(blocks):
  if i+1 in chosen:
   pp=excerpt/(name.replace('.txt','')+'_page_'+str(i+1)+'.txt')
   pp.write_bytes(block)
   cuts.append({'PDF_page':i+1,'source_text_byte_interval_half_open':[offset,offset+len(block)],'excerpt':pin(pp)})
  offset+=len(block)+1
 assert len(cuts)==len(chosen)
 readscope.append({'source_text':pin(path),'source_pdf':pin(path.with_suffix('.pdf')),'complete_text_PDF_page_count':b.count(b'\f'),
 'semantic_full_PDF_read_claimed':len(chosen)==b.count(b'\f'),'purpose':purpose,'full_selected_pages':cuts,
 'visual_full_pages_viewed':{'liedtke.txt':[13,14],'kleiman_hodge.txt':[78,79],'milne_jacobians.txt':[19,20],'janssen.txt':[1]}.get(name,[])})
def htmlcut(name,start,end,purpose):
 path=W/'private_sources'/(name+'.txt');s=path.read_text()
 i=s.index(start);j=s.index(end,i+len(start)) if end else len(s)
 raw=s[i:j].encode()
 out=excerpt/(name+'_'+str(len(readscope))+'.txt');out.write_bytes(raw)
 readscope.append({'source_text':pin(path),'raw_HTML':pin(path.with_suffix('.html')),'source_text_UTF8_byte_interval_half_open':[len(s[:i].encode()),len(s[:j].encode())],
                  'excerpt':pin(out),'purpose':purpose,'semantic_full_HTML_document_read_claimed':False})
htmlcut('stacks_resolution','Definition 54.14.1.','Comments','surface resolution definitions; Theorem 54.14.5 with its complete proof and preceding local resolution results')
htmlcut('stacks_bertini_irreducibility','Lemma 37.32.3.','Comments','irreducible Bertini assumptions and complete proof')
htmlcut('stacks_bertini_smooth','Lemma 33.47.3.','Comments','smooth Bertini assumptions and complete proof; applied to S_reg immersion')
htmlcut('stacks_dualizing_CM','Lemma 48.27.5.','Comments','proper Cohen-Macaulay Serre duality and canonical module properties; entire lemma and proof')
htmlcut('stacks_reflexive','Definition 31.13.1.','Comments','full reflexive-module section including Lemmas 31.13.12-13 and proofs')
htmlcut('kollar_dao_conductor','Lemma 18.','Corollary 19.','condition (18.2) of finite canonical duality')
htmlcut('kollar_dao_conductor','Proposition 32.','Corollary 33.','finite duality under (18.2) and complete proof')
htmlcut('kollar_dao_conductor','Definition 46.','Lemma 50.','Definitions 46-47, section 48 equation (48.1), Lemma 49 complete proof')
authorpath=A/'snapshot/unsolved_math_prioritization/attempts/30002792'
authorsemantic=[pin(authorpath/n) for n in ['PUBLIC_TURN_2.md','source_record.json','SOURCES.md']]
ind=pin(W/'INDEPENDENT_INITIAL_DERIVATION.md')
assert ind['bytes']==3019 and ind['sha256']=='1f649f16509b8fd963f3d3525f47ffc85148bf336694ddbbe8f02b0c0220c224'
write('READ_SCOPE.json',{'UTC':now(),'initial_independence':ind,'initial_record':json.loads((W/'INDEPENDENCE_RECORD.json').read_text()),
 'author_files_read_entire_body_for_semantic_scope':authorsemantic,'prior_reviewer_proof_semantically_read':False,
 'snapshot_all19_full_bytes_read_for_authentication_only':True,
 'source_body_full_bytes_read_for_custody_not_all_PDF_pages_semantically_read':True,
 'primary_selected_mathematical_read_scope':readscope,
 'visual_renders':[pin(p) for p in sorted((W/'private_sources/renders').glob('*.png'))],
 'source_transformation_verification':derived,
 'no_priority_audit':True,'no_other_family_convergence':True})
write('INPUT_AND_SOURCE_CUSTODY.json',{'UTC':now(),'actual_verifier_PID':os.getpid(),'verifier_source':pin(Path(__file__)),
 'original_manifest':pin(MANIFEST),'original_PR_head':m['head'],'original_status':m['original_submitted_status'],'original_budget':m['original_author_budget'],
 'all_19_original_bodies_authenticated':original,
 'complete_finished_native_capture_count':len(native),'captures':native,
 'first_eight_failures_retained':{'expected_exit':23,'reason':'private_sources destination did not exist; headers/output could not be opened','not_reclassified_as_success':True},
 'successful_whole_primary_body_count':len(raw_source),'raw_primary_sources':raw_source,
 'all_private_source_files_full_bytes_read_and_pinned':[pin(p) for p in sorted((W/'private_sources').rglob('*')) if p.is_file()],
 'source_html_data_replay_nonwhitespace_exact':derived,
 'semantic_read_scope_file':'READ_SCOPE.json',
 'current_verifier_capture_excluded_while_running':EXCLUDE_NATIVE,
 'runtime_observed_modes_are_not_final_immutable_modes':True,
 'no_claim_to_have_executed_other_family_or_author_3888_controls':True})
print(json.dumps({'status':'PASS_FULL_BODY_AUTHENTICATION_AND_NATIVE_CUSTODY','UTC':now(),'actual_PID':os.getpid(),
 'original_bodies':len(original),'finished_native_captures':len(native),'successful_public_primary_bodies':len(raw_source),
 'failed_captures_preserved':8,'semantic_scope_records':len(readscope)},indent=2))
