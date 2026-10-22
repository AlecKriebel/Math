#!/usr/bin/env python3
"""Actual doi_status -> verify_live -> append; all HTTP/provider boundaries synthetic."""
from contextlib import ExitStack
import copy
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import types
from unittest.mock import patch
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent
sys.path.insert(0,str(AUDIT))
import ops_binding as B
import verify_published_files as V
import record_publication_ledger as D
CASES=[];ATTEMPTS=[]
GOOD=['https://zenodo.org/records/999','https://ZENODO.ORG:443/records/999','HTTPS://zenodo.org/records/999']
BAD=['https://zenodo.org/records/998','https://zenodo.org/records/9990','https://zenodo.org/records/1999',
 'https://foreign.invalid/records/999','https://zenodo.org.evil.invalid/records/999','https://evilzenodo.org/records/999',
 'http://zenodo.org/records/999','https://user@zenodo.org/records/999','https://user:pass@zenodo.org/records/999',
 'https://zenodo.org@foreign.invalid/records/999','https://zenodo.org:8443/records/999','https://zenodo.org:bad/records/999',
 'https://zenodo.org/','https://zenodo.org/api/records/999','https://zenodo.org/record/999','https://zenodo.org/records/999/',
 'https://zenodo.org/records/0999','https://zenodo.org/records/９９９','https://zenodo.org/records/%39%39%39',
 'https://zenodo.org/records/./999','https://zenodo.org//records/999','https:///zenodo.org/records/999',
 'https://zenodo.org/records/999?download=1','https://zenodo.org/records/999?record=1000',
 'https://zenodo.org/records/999?','https://zenodo.org/records/999#metadata','https://zenodo.org/records/999#',
 'https://zenodo.org./records/999','https://www.zenodo.org/records/999','https://zenodo.org:0443/records/999',
 ' https://zenodo.org/records/999','https://zenodo.org/records/999\n','//zenodo.org/records/999',None,'',999]


def ck(v,m):
    if not v:raise RuntimeError('DOI DESTINATION CONTROL FAILED: '+m)
def forbidden(*args,**kwargs):ATTEMPTS.append(True);raise RuntimeError('ACTUAL PROVIDER FORBIDDEN')
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def record_fixture():
    metadata,selected=B.manifest();files=[{'key':e['name'],'size':e['size'],'checksum':'md5:'+e['md5']} for e in selected]
    publicmeta=copy.deepcopy(metadata);publicmeta.pop('upload_type');publicmeta.pop('publication_type')
    publicmeta['resource_type']={'type':'publication','subtype':'preprint','title':'Preprint'};publicmeta['license']={'id':'cc-by-4.0'}
    return metadata,selected,{'id':999,'doi':'10.5281/zenodo.999','metadata':publicmeta,'files':files}


def pipeline(root,destination,forged=False):
    root.mkdir();metadata,selected,public=record_fixture();appends=[];gates=[];doi_heads=[]
    before=[B.HEADERS];desired=D.desired_row(999);reads=iter([before,before+[desired]])
    write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',{'ledger_leads':[]})
    class Response:
        status=200;url=destination
        def __enter__(self):return self
        def __exit__(self,*args):pass
    class Opener:
        def open(self,request,timeout):
            ck(request.get_method()=='HEAD' and request.full_url=='https://doi.org/10.5281/zenodo.999','actual doi_status HEAD request')
            ck(not request.has_header('Authorization'),'no authenticated header sent to DOI resolver');doi_heads.append(True)
            return Response()
    def inspect(args):
        ck(args.command=='inspect' and args.check_doi,'GET-only inspection fixture')
        return {'id':999,'state':'published','doi':'10.5281/zenodo.999','doi_url':'https://doi.org/10.5281/zenodo.999',
                'doi_resolution':B.zenodo.doi_status('10.5281/zenodo.999')}
    def fetch(url):
        if url=='https://zenodo.org/api/records/999':return json.dumps(public).encode(),200,url
        for entry in selected:
            if '/files/'+entry['name']+'?' in url:return entry['path'].read_bytes(),200,url
        raise RuntimeError('Unknown synthetic public URL')
    def gate(*args,**kwargs):gates.append(True);return {'started_utc':B.stamp(),'ledger_sha256':B.digest(before),'receipt':str(root/'gate.json')},{}
    def append(action,params,body):
        appends.append(True);ck((root/'LEDGER_APPEND_INTENT.json').exists(),'ledger intent before synthetic append')
        return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':[desired]}}}
    fake={'record':999,'all_public_file_bytes_match_reviewed':True,'release_manifest_sha256':B.RELEASE_SHA,
          'doi_resolution':{'status':200,'resolved_url':destination,'exact_expected_record_destination_verified':True}}
    if forged=='missing_url':fake['doi_resolution'].pop('resolved_url')
    if forged=='missing_resolution':fake.pop('doi_resolution')
    if forged:write(root/'ZENODO_PUBLIC_FILE_VERIFICATION.json',fake)
    with ExitStack() as stack:
        for module in [V,D]:stack.enter_context(patch.object(module,'AUDIT',root));stack.enter_context(patch.object(module,'require_release_clearance',lambda:True))
        stack.enter_context(patch.object(V,'PRIVATE',root/'private'));stack.enter_context(patch.object(V,'fetch',fetch))
        stack.enter_context(patch.object(B.zenodo,'run',inspect));stack.enter_context(patch.object(B.zenodo,'build_opener',lambda *a:Opener()))
        stack.enter_context(patch.object(D,'verify_live',(lambda identifier:copy.deepcopy(fake)) if forged else V.verify_live))
        stack.enter_context(patch.object(D,'collect',gate));stack.enter_context(patch.object(D,'read',lambda *a:next(reads)))
        stack.enter_context(patch.object(D,'gws',append))
        try:result=D.append_verified('a'*40,999)
        except RuntimeError as error:accepted=False;reason=str(error)
        else:accepted=result['status']=='verified';reason=None
    return {'accepted':accepted,'synthetic_appends':len(appends),'synthetic_upstream_gates':len(gates),
            'actual_doi_status_heads_synthetic':len(doi_heads),'reason':reason}


def main():
    metadata,selected,public=record_fixture();downloads={e['name']:(e['path'].read_bytes(),200,'synthetic') for e in selected}
    old=types.ModuleType('old_public_verifier');old.__file__=str(AUDIT/'verify_published_files.py')
    source=HERE/'before/verify_published_files.py';exec(compile(source.read_bytes(),str(source),'exec'),old.__dict__)
    old_failures=[]
    for url in ['https://zenodo.org/records/998','https://foreign.invalid/records/999']:
        inspection={'id':999,'state':'published','doi':'10.5281/zenodo.999','doi_url':'https://doi.org/10.5281/zenodo.999',
                    'doi_resolution':{'http_status':200,'resolved_url':url}}
        result=old.verify_public_record(999,metadata,selected,inspection,public,downloads,200)
        ck(result['all_public_file_bytes_match_reviewed'],'old status-only failure reproduced')
        old_failures.append({'resolved_url':url,'old_verifier_accepted':True})
    with ExitStack() as guards:
        guards.enter_context(patch.object(subprocess,'run',forbidden));guards.enter_context(patch.object(socket,'socket',forbidden))
        guards.enter_context(patch.object(V,'urlopen',forbidden))
        for method in ['request','create','upload','update','publish','get']:guards.enter_context(patch.object(B.zenodo.ZenodoClient,method,forbidden))
        with tempfile.TemporaryDirectory(dir=HERE,prefix='doi_synthetic_') as temp:
            root=Path(temp)
            for url in GOOD+BAD:
                valid=url in GOOD
                try:V.verify_doi_destination(999,{'http_status':200,'resolved_url':url})
                except RuntimeError:ck(not valid,'valid canonical DOI destination rejected')
                else:ck(valid,'unsafe DOI destination accepted')
                CASES.append({'case':'strict_destination','value':url,'expected':'accept' if valid else 'reject','pass':True})
                for forged in [False,True]:
                    result=pipeline(root/str(len(CASES)),url,forged)
                    ck(result['accepted']==valid and result['synthetic_appends']==int(valid),'actual verifier/independent append destination guard')
                    if not valid:ck(result['synthetic_upstream_gates']==0,'unsafe destination rejected independently before gate')
                    if not forged:ck(result['actual_doi_status_heads_synthetic']==1,'actual doi_status body exercised')
                    CASES.append({'case':'forged_upstream_booleans' if forged else 'doi_status_verify_live_append','value':url,**result})
            for missing in ['missing_url','missing_resolution']:
                result=pipeline(root/str(len(CASES)),GOOD[0],missing)
                ck(not result['accepted'] and result['synthetic_appends']==0 and result['synthetic_upstream_gates']==0,'missing exact destination evidence stops independently')
                CASES.append({'case':missing,**result})
            for status in [None,200.0,True,201,301,404]:
                try:V.verify_doi_destination(999,{'http_status':status,'resolved_url':GOOD[0]})
                except RuntimeError:pass
                else:raise RuntimeError('Nonexact successful DOI status accepted')
                CASES.append({'case':'invalid_status','value':status,'expected':'reject','pass':True})
    ck(not ATTEMPTS,'zero actual providers')
    result={'timestamp':B.stamp(),'optimization':sys.flags.optimize,'controls':len(CASES),'all_passed':True,'actual_provider_attempts':0,
      'old_verifier_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'old_wrong_destination_reproductions':old_failures,
      'current_verifier_sha256':hashlib.sha256((AUDIT/'verify_published_files.py').read_bytes()).hexdigest(),
      'current_appender_sha256':hashlib.sha256((AUDIT/'record_publication_ledger.py').read_bytes()).hexdigest(),'cases':CASES}
    write(HERE/('DOI_DESTINATION_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'DOI_DESTINATION_CONTROLS.json'),result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
