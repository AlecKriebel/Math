#!/usr/bin/env python3
"""Exact preserved-input local three-helper destination repair installation."""
from pathlib import Path
import datetime as dt,difflib,hashlib,json,os
H=Path(__file__).resolve().parent;A=H.parent;O=H/'pre_destination_binding'
HELPERS=['ops_binding.py','prepublication_check.py','publication_live_gates.py','repository_integration.py','verify_published_files.py','publication_lifecycle.py','record_publication_ledger.py']
FUNCTION='''

def doi_destination_evidence(identifier, status, resolved_url):
    """Authenticated DOI outcome policy; independent of lexical ledger leads.

    Accept only literal HTTPS zenodo.org /records/{exact positive ASCII ID}.
    Explicit ports (including443), userinfo, host aliases/case variations,
    trailing slash, query, fragment, encoding and route variants all reject.
    Root may review a new policy separately; never infer identity from them.
    """
    if type(identifier) is not int or identifier<=0:
        raise RuntimeError('Exact positive intended record ID required')
    expected='https://zenodo.org/records/'+str(identifier)
    if type(status) is not int or status!=200 or not isinstance(resolved_url,str) or resolved_url!=expected:
        raise RuntimeError('DOI final destination is not the exact intended HTTPS Zenodo record')
    return {'policy':'pr399-exact-https-record-v1','record':identifier,
            'status':200,'resolved_url':expected}
'''

def main():
 before=json.loads((H/'INPUT_PRESERVATION.json').read_bytes());changes=[];diff=[]
 for e in before['complete_context_files']:
  for root in [O,A]:
   b=(root/e['path']).read_bytes()
   if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise RuntimeError('Preserved input changed '+e['path'])
 proposal=H/'proposed_helpers';proposal.mkdir(exist_ok=False)
 for name in HELPERS:
  old=(O/name).read_text();new=old
  if name=='ops_binding.py':new+=FUNCTION
  elif name=='verify_published_files.py':
   oldline="    # Compare every intended field on the public record as well as authenticated\n"
   newline="    destination=doi_destination_evidence(identifier,inspection['doi_resolution'].get('http_status'),\n                                         inspection['doi_resolution'].get('resolved_url'))\n"+oldline
   if new.count(oldline)!=1:raise RuntimeError('Verifier shape')
   new=new.replace(oldline,newline)
   oldline="'resolved_url':inspection['doi_resolution']['resolved_url']}"
   newline="'resolved_url':inspection['doi_resolution']['resolved_url'],\n                          'destination_verified':destination}"
   if new.count(oldline)!=1:raise RuntimeError('Receipt shape')
   new=new.replace(oldline,newline)
  elif name=='record_publication_ledger.py':
   oldline="    gate,acceptance=collect('before_ledger',expected_head,identifier,allow_target_row=True)"
   newline="""    resolution=public['doi_resolution']
    destination=doi_destination_evidence(identifier,resolution.get('status'),resolution.get('resolved_url'))
    evidence=resolution.get('destination_verified')
    if (not isinstance(evidence,dict) or evidence!=destination
            or type(evidence.get('record')) is not int or type(evidence.get('status')) is not int):
        raise RuntimeError('Fresh exact DOI destination evidence absent or inconsistent')
"""+oldline
   if new.count(oldline)!=1:raise RuntimeError('Appender shape')
   new=new.replace(oldline,newline)
  compile(new,str(A/name),'exec');(proposal/name).write_text(new)
  changes.append({'path':name,'before_sha256':hashlib.sha256(old.encode()).hexdigest(),'after_sha256':hashlib.sha256(new.encode()).hexdigest(),'changed':old!=new})
  diff.extend(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile='preserved356/'+name,tofile='canonical399/'+name))
 if {e['path'] for e in changes if e['changed']}!={'ops_binding.py','verify_published_files.py','record_publication_ledger.py'}:raise RuntimeError('Repair scope')
 for e in changes:
  if e['changed']:
   temp=H/(e['path']+'.install.tmp')
   with temp.open('xb') as stream:stream.write((proposal/e['path']).read_bytes());stream.flush();os.fsync(stream.fileno())
   os.replace(temp,A/e['path'])
 (H/'REPAIR.diff').write_text(''.join(diff));(H/'CANONICAL_INSTALLATION.json').write_text(json.dumps({'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'files':changes,'context631_preserved_before_install':True,'provider_calls':0,'publication_ready':False},indent=2)+'\n')
 print(json.dumps({'changed_helpers':3,'context_preserved':len(before['complete_context_files']),'publication_ready':False}))
if __name__=='__main__':main()
