#!/usr/bin/env python3
"""Fresh reviewer05 actual-function tests; synthetic services, no real mutations."""
import argparse,copy,hashlib,json,socket,subprocess,sys,types
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
A=Path(__file__).resolve().parents[2];P=A.parents[1]/'private/pr0399_package05'
def require(v,m):
    if not v:raise RuntimeError(m)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();out=args.output
    require(out.is_absolute() and out.is_relative_to(P),'owned absolute private output');out.mkdir(parents=True,exist_ok=False)
    names=['ops_binding','prepublication_check','publication_live_gates','repository_integration','verify_published_files','publication_lifecycle','record_publication_ledger'];mods=[]
    for name in names:
        m=types.ModuleType(name);m.__file__=str(A/(name+'.py'));sys.modules[name]=m;exec(compile((A/(name+'.py')).read_bytes(),m.__file__,'exec'),m.__dict__);mods.append(m)
    B,C,G,I,V,Y,L=mods;meta,selected=B.manifest();identifier=29999991;doi='10.5281/zenodo.'+str(identifier);url='https://zenodo.org/records/'+str(identifier)
    metadata=copy.deepcopy(meta);metadata.pop('upload_type');metadata.pop('publication_type');metadata.update(resource_type={'type':'publication','subtype':'preprint','title':'Preprint'},license={'id':meta['license']})
    public={'id':identifier,'doi':doi,'metadata':metadata,'files':[{'key':e['name'],'size':e['size'],'checksum':'md5:'+e['md5']} for e in selected]}
    downloads={e['name']:((B.PUBLICATION/e['name']).read_bytes(),200,url+'/files/'+e['name']) for e in selected};cases=[];attempts=[]
    def forbidden(*a,**k):attempts.append('forbidden');raise RuntimeError('REAL PROVIDER TRAPPED')
    def pipeline(label,resolved=url,status=200,bypass=False,proof='correct',idempotent=False,corrupt_readback=False,expect='reject'):
        work=out/('case'+str(len(cases)));work.mkdir();(work/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json').write_text(json.dumps({'ledger_leads':[]}))
        rows=[B.HEADERS.copy()]+([L.desired_row(identifier)] if idempotent else []);counts={'gate':0,'read':0,'append':0}
        inspect={'id':identifier,'state':'published','doi':doi,'doi_url':'https://doi.org/'+doi,'doi_resolution':{'http_status':status,'resolved_url':resolved}}
        def fetch(u):
            if u=='https://zenodo.org/api/records/'+str(identifier):return json.dumps(public).encode(),200,u
            for n,value in downloads.items():
                if '/files/'+n in u:return value
            raise RuntimeError('Unexpected synthetic fetch')
        def collect(*a,**k):counts['gate']+=1;return {'started_utc':B.stamp(),'ledger_sha256':B.digest(rows),'expected_identity_record_ids':[identifier],'receipt':'synthetic'},{}
        def gws(action,params,body=None):
            if action=='get':
                counts['read']+=1;value=copy.deepcopy(rows)
                if corrupt_readback and counts['read']>1:value.append(['','','https://zenodo.org:443/record/'+str(identifier)+'/',''])
                return {'values':value}
            require(action=='append','only append permitted');require((work/'LEDGER_APPEND_INTENT.json').is_file(),'durable intent before append');require(body['values']==[L.desired_row(identifier)],'literal row');counts['append']+=1;rows.extend(copy.deepcopy(body['values']));return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':body['values']}}}
        with ExitStack() as patches:
            for m,n,value in [(V,'AUDIT',work),(V,'PRIVATE',work),(L,'AUDIT',work),(L,'PRIVATE',work),(V,'require_release_clearance',lambda:None),(L,'require_release_clearance',lambda:None),(V.zenodo,'run',lambda *a,**k:copy.deepcopy(inspect)),(V,'fetch',fetch),(L,'collect',collect),(L,'gws',gws)]:patches.enter_context(patch.object(m,n,value))
            if bypass:
                evidence={'policy':'pr399-exact-https-record-v1','record':identifier,'status':200,'resolved_url':url}
                if proof!='correct':evidence=proof
                result={'record':identifier,'release_manifest_sha256':B.RELEASE_SHA,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':status,'resolved_url':resolved,'destination_verified':evidence}}
                (work/'ZENODO_PUBLIC_FILE_VERIFICATION.json').write_text(json.dumps(result));patches.enter_context(patch.object(L,'verify_live',lambda *a:copy.deepcopy(result)))
            try:r=L.append_verified('0'*40,identifier);verdict='accept';reason=None
            except (RuntimeError,ValueError,KeyError,TypeError,B.zenodo.DepositError) as e:verdict='reject';reason=str(e)
        require(verdict==expect,label+' unexpected '+verdict+': '+str(reason))
        if expect=='accept':require(counts['append']==(0 if idempotent else 1) and r['unique_target_and_DOI'] and r['read_back_exact'],'successful real logic')
        elif not corrupt_readback:require(counts=={'gate':0,'read':0,'append':0},'destination failure precedes gate/read/append')
        require(not (work/'LEDGER_PUBLICATION_VERIFICATION.json').exists() or expect=='accept','no false success receipt')
        cases.append({'label':label,'verdict':verdict,'counts':counts,'reason':reason})
    bad=[None,'',url+'/',url+'?x=1',url+'#x',url.replace('https:','http:'),url.replace('zenodo.org','zenodo.org:443'),url.replace('zenodo.org','ZENODO.ORG'),url.replace('zenodo.org','www.zenodo.org'),url.replace('/records/','/record/'),url.replace('/records/','/records/../records/'),url.replace('29999991','29999990'),'https://example.org/records/29999991',url.replace('29999991','29999992'),url.replace('29999991','029999991'),url.replace('29999991','%322999991'),url+'\x00',url+'\n',200,{},['https://zenodo.org/records/29999991']]
    with ExitStack() as traps:
        traps.enter_context(patch.object(socket,'socket',forbidden));traps.enter_context(patch.object(subprocess,'run',forbidden));traps.enter_context(patch.object(V,'urlopen',forbidden))
        for n in ['request','get','create','upload','update','publish']:traps.enter_context(patch.object(B.zenodo.ZenodoClient,n,forbidden))
        for j,resolved in enumerate(bad):
            pipeline('actual full wrong destination '+str(j),resolved=resolved)
            pipeline('forged upstream positive wrong destination '+str(j),resolved=resolved,bypass=True)
        for status in [200.0,'200',True,False,201,302,404,None]:pipeline('exact status '+repr(status),status=status,bypass=True)
        for evidence in [None,{},True,{'policy':'pr399-exact-https-record-v1','record':float(identifier),'status':200,'resolved_url':url},{'policy':'pr399-exact-https-record-v1','record':identifier,'status':200.0,'resolved_url':url},{'policy':'pr399-exact-https-record-v1','record':identifier,'status':200,'resolved_url':url,'extra':None}]:pipeline('independent proof '+repr(evidence),bypass=True,proof=evidence)
        pipeline('canonical actual pipeline',expect='accept');pipeline('canonical exact-row idempotence',idempotent=True,expect='accept');pipeline('canonical independent proof',bypass=True,expect='accept');pipeline('late target alias must break readback',corrupt_readback=True)
        # No first-cell/model shortcut may conceal a later unresolved alias.
        for cells in [['tensor core','','','10/abc'],['10.5281/zenodo.29999991','','','https://zenodo.org/unknown']]:
            try:B.row_identity_names(cells)
            except RuntimeError:cases.append({'label':'all cells evaluated','verdict':'reject'})
            else:raise RuntimeError('later ambiguity hidden')
    require(not attempts,'zero real provider attempts')
    result={'optimization':sys.flags.optimize,'all_passed':True,'controls':len(cases),'actual_provider_attempts':len(attempts),'cases':cases,'helpers':[{'path':n+'.py','sha256':hashlib.sha256((A/(n+'.py')).read_bytes()).hexdigest()} for n in names],'scope':'Actual functions with synthetic services and simulated clearance; no publication permission'}
    (out/'INDEPENDENT_OPERATIONS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in {'cases','helpers'}},indent=2))
if __name__=='__main__':main()
