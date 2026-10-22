#!/usr/bin/env python3
"""Actual DOI-status -> live verifier -> independent appender; zero providers."""
import argparse,copy,hashlib,json,socket,subprocess,sys,types
from pathlib import Path
from unittest.mock import patch
from contextlib import ExitStack
H=Path(__file__).resolve().parent;A=H.parent

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args();output=args.output
 if not output.is_absolute() or not output.is_relative_to(A.parents[1]/'private'):raise RuntimeError('New private output required')
 # Exact reviewer04 first55 controls, before its old-finding assumptions.
 source=H/'pre_destination_binding/reviews/package_adversary_04/operations_checks.py';body=source.read_text()
 if hashlib.sha256(source.read_bytes()).hexdigest()!='08991cecd52cf1907d3b4bcd680e4f66de8cf207d6c70ba2d9c3aeee4201b936':raise RuntimeError('Review04 source changed')
 prefix=body.split(' doi_findings=[]\n',1)[0]+'\n';module=types.ModuleType('review04_nonfinding');module.__file__=str(A/'reviews/package_adversary_04/operations_checks.py');prior=sys.argv;sys.argv=[str(source),'--output',str(output)]
 try:exec(compile(prefix,str(source),'exec'),module.__dict__)
 finally:sys.argv=prior
 B,C,G,I,V,Y,D=module.mods;metadata=module.meta;selected=module.selected;public=module.public;inspection=module.inspection;downloads=module.downloads;identifier=module.id;canonical='https://zenodo.org/records/'+str(identifier);cases=[];attempts=module.attempts
 def require(v,message):
  if not v:raise RuntimeError('CONTROL FAILED: '+message)
 def forbidden(*a,**k):attempts.append(True);raise RuntimeError('REAL PROVIDER FORBIDDEN')
 def direct(resolution):
  value=copy.deepcopy(inspection);value['doi_resolution']=resolution
  return V.verify_public_record(identifier,metadata,selected,value,public,downloads,200)
 def status_result(status,url):
  class Response:
   def __init__(self):self.status=status;self.url=url
   def __enter__(self):return self
   def __exit__(self,*a):return False
  class Opener:
   def open(self,*a,**k):return Response()
  with patch.object(B.zenodo,'build_opener',lambda *a:Opener()):return B.zenodo.doi_status('10.5281/zenodo.'+str(identifier))
 def pipeline(resolution,bypass=False,proof_override=None,idempotent=False,omit_proof=False):
  work=output/('case_'+str(len(cases)));work.mkdir();(work/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').write_text(json.dumps({'ledger_leads':[]}));rows=[B.HEADERS.copy()];counts={'gate':0,'read':0,'append':0}
  if idempotent:rows.append(D.desired_row(identifier))
  inspected=copy.deepcopy(inspection);inspected['doi_resolution']=copy.deepcopy(resolution)
  def fetch(url):
   if url=='https://zenodo.org/api/records/'+str(identifier):return json.dumps(public).encode(),200,url
   for e in selected:
    if '/files/'+e['name'] in url:return downloads[e['name']]
   raise RuntimeError('Unexpected synthetic download')
  def collect(*a,**k):counts['gate']+=1;return {'expected_identity_record_ids':[identifier],'ledger_sha256':B.digest(rows),'started_utc':B.stamp(),'receipt':'synthetic-only'},{}
  def gws(action,params,body=None):
   if action=='get':counts['read']+=1;return {'values':copy.deepcopy(rows)}
   require(action=='append','only intended synthetic append');require((work/'LEDGER_APPEND_INTENT.json').exists(),'exclusive intent precedes append');require(body['values']==[D.desired_row(identifier)],'literal desired row');counts['append']+=1;rows.append(copy.deepcopy(body['values'][0]));return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':body['values']}}}
  with ExitStack() as guards:
   for m,n,v in [(V,'AUDIT',work),(V,'PRIVATE',work),(D,'AUDIT',work),(D,'PRIVATE',work),(V,'require_release_clearance',lambda:None),(D,'require_release_clearance',lambda:None),(V.zenodo,'run',lambda *a,**k:copy.deepcopy(inspected)),(V,'fetch',fetch),(D,'collect',collect),(D,'gws',gws)]:guards.enter_context(patch.object(m,n,v))
   if bypass:
    proof={'policy':'pr399-exact-https-record-v1','record':identifier,'status':200,'resolved_url':canonical}
    if proof_override is not None:proof=copy.deepcopy(proof_override)
    stub={'record':identifier,'all_public_file_bytes_match_reviewed':True,'release_manifest_sha256':B.RELEASE_SHA,'doi_resolution':{'status':resolution.get('http_status'),'resolved_url':resolution.get('resolved_url'),'destination_verified':proof}}
    if omit_proof:stub['doi_resolution'].pop('destination_verified')
    (work/'ZENODO_PUBLIC_FILE_VERIFICATION.json').write_text(json.dumps(stub))
    guards.enter_context(patch.object(D,'verify_live',lambda *a:stub))
   try:result=D.append_verified('0'*40,identifier);verdict='accept'
   except (RuntimeError,ValueError,KeyError,TypeError,B.zenodo.DepositError) as error:result=str(error);verdict='reject'
  if verdict=='reject':require(not counts['append'] and not counts['gate'] and not counts['read'],'reject before gate/read/append');require(not (work/'LEDGER_PUBLICATION_VERIFICATION.json').exists(),'no false success receipt')
  else:require(result['unique_target_and_DOI'] and result['read_back_exact'] and counts['append']==(0 if idempotent else 1),'actual intended success/unique readback')
  return {'reason':result if verdict=='reject' else None,'verdict':verdict,'boundary_counts':counts,'bypass_public_verifier':bypass,'idempotent':idempotent}
 def run_pipeline(label,resolution,expected,**kwargs):
  result=pipeline(resolution,**kwargs);require(result['verdict']==expected,label+repr(result));cases.append({'case':label,**result})
 bad_urls=[canonical[:-1]+'0','https://zenodo.org/records/29999989','https://zenodo.org/records/29999992','https://example.org/unrelated','https://zenodo.org.evil.example/records/'+str(identifier),'https://sub.zenodo.org/records/'+str(identifier),'https://user@zenodo.org/records/'+str(identifier),canonical.replace('zenodo.org','ZENODO.ORG'),canonical.replace('zenodo.org','www.zenodo.org'),canonical.replace('zenodo.org','zenodo.org.'),canonical.replace('https:','http:'),canonical.replace('https:','ftp:'),canonical.removeprefix('https:'),canonical.removeprefix('https://'),canonical.replace('zenodo.org','zenodo.org:443'),canonical.replace('zenodo.org','zenodo.org:0443'),canonical.replace('zenodo.org','zenodo.org:80'),canonical.replace('zenodo.org','zenodo.org:65536'),canonical.replace('zenodo.org','zenodo.org:'),canonical.replace('zenodo.org','zenodo.org:abc'),canonical.replace('/records/','/record/'),canonical.replace('/records/','/api/records/'),canonical+'/',canonical+'/export/json',canonical+'?download=1',canonical+'#metadata',canonical.replace('/records/','/records/./'),canonical.replace('/records/','//records/'),canonical.replace(str(identifier),'0'+str(identifier)),canonical.replace(str(identifier),'%32'+str(identifier)[1:]),canonical.replace('zenodo.org','z%65nodo.org'),canonical.replace('/records/','/records%2F'),canonical.replace('/records/','/records%252F'),None,'',42,[], ' '+canonical,canonical+' ',canonical+'\n',canonical+'\t',canonical.replace('zenodo.org','zenodo.orℊ')]
 resolutions=[{'http_status':200,'resolved_url':url} for url in bad_urls]
 resolutions += [{'http_status':code,'resolved_url':canonical} for code in [404,302,'200',True,None,200.0]]+[{'http_status':200},{'resolved_url':canonical},{}]
 with ExitStack() as guards:
  guards.enter_context(patch.object(socket,'socket',forbidden));guards.enter_context(patch.object(subprocess,'run',forbidden));guards.enter_context(patch.object(V,'urlopen',forbidden))
  for n in ['request','get','create','upload','update','publish']:guards.enter_context(patch.object(B.zenodo.ZenodoClient,n,forbidden))
  for index,resolution in enumerate(resolutions):
   try:direct(resolution)
   except (RuntimeError,ValueError,KeyError,TypeError):cases.append({'case':'direct_reject_'+str(index),'verdict':'reject'})
   else:raise RuntimeError('Direct accepted wrong destination '+repr(resolution))
   run_pipeline('actual_verify_live_append_reject_'+str(index),resolution,'reject')
   run_pipeline('independent_upstream_bypass_reject_'+str(index),resolution,'reject',bypass=True)
  for url in [canonical,canonical[:-1]+'0','https://example.org/unrelated']:
   observed=status_result(200,url);require(observed['http_status']==200 and observed['resolved_url']==url,'actual doi_status synthetic final outcome');run_pipeline('actual_doi_status_to_verifier_to_append_'+url,observed,'accept' if url==canonical else 'reject')
  result=direct({'http_status':200,'resolved_url':canonical});require(result['doi_resolution']['destination_verified']==B.doi_destination_evidence(identifier,200,canonical),'direct exact evidence');cases.append({'case':'direct_exact_destination_evidence','verdict':'accept'})
  run_pipeline('actual_canonical_idempotence',{'http_status':200,'resolved_url':canonical},'accept',idempotent=True)
  run_pipeline('independent_correct_proof',{'http_status':200,'resolved_url':canonical},'accept',bypass=True)
  run_pipeline('independent_boolean_only_missing_proof',{'http_status':200,'resolved_url':canonical},'reject',bypass=True,omit_proof=True)
  for number,proof in enumerate([{}, {'policy':'wrong','record':identifier,'status':200,'resolved_url':canonical},{'policy':'pr399-exact-https-record-v1','record':identifier-1,'status':200,'resolved_url':canonical},{'policy':'pr399-exact-https-record-v1','record':identifier,'status':200.0,'resolved_url':canonical},{'policy':'pr399-exact-https-record-v1','record':identifier,'status':200,'resolved_url':canonical,'extra':True}]):run_pipeline('forged_or_absent_evidence_'+str(number),{'http_status':200,'resolved_url':canonical},'reject',bypass=True,proof_override=proof)
  for bad_id in [0,-1,True,str(identifier),None]:
   try:B.doi_destination_evidence(bad_id,200,canonical)
   except RuntimeError:cases.append({'case':'exact_identifier_type_'+repr(bad_id),'verdict':'reject'})
   else:raise RuntimeError('Invalid exact identifier accepted')
 require(not attempts,'zero actual provider attempts');require(len(module.results)==55,'all reviewer nonfinding controls preserved')
 out={'optimization':sys.flags.optimize,'new_destination_controls':len(cases),'review04_other_controls':len(module.results),'total':len(cases)+len(module.results),'all_passed':True,'actual_provider_attempts':len(attempts),'helper_bindings':[{'path':n+'.py','sha256':hashlib.sha256((A/(n+'.py')).read_bytes()).hexdigest()} for n in module.NAMES],'cases':cases,'other_controls':module.results,'policy':'Exact literal HTTPS zenodo.org /records/{expectedID}; no ports/aliases/query/fragment/trailing path. Conservative lexical lead recognizer is not used.'}
 (output/'DESTINATION_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in {'cases','other_controls','helper_bindings'}},indent=2))
if __name__=='__main__':main()
