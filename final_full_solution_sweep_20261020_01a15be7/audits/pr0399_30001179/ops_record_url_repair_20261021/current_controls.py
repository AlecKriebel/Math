#!/usr/bin/env python3
"""Actual complete/independent route identity controls, synthetic providers only."""
import copy,json,socket,subprocess,sys,tempfile
from pathlib import Path
from contextlib import ExitStack
from unittest.mock import patch
from controls_support import HERE,implementation
KIND='canonical' if '--canonical' in sys.argv else 'proposed'
B,P,G,I,V,L,D=implementation(KIND)
CASES=[];PROVIDERS=[]
OBSERVED=['https://zenodo.org/record/999/','https://zenodo.org:443/records/999','https://zenodo.org/records/./999','https://zenodo.org/records/999/export/json','https://ZENODO.ORG:443/record/999/?download=1#details','https://zenodo.org:443/records/./999?download=1#files','https://zenodo.org:443/records/999/export/json?x=1#metadata','https://zenodo.org/record/999/#files','https://zenodo.org/records/999/export/json#metadata']
ADDITIONAL=['https://zenodo.org:000443//records///999/','HTTP://ZENODO.ORG:080/record/999','https://www.zenodo.org:0443/API/RECORDS/./999/EXPORT/JSON?x#y','//zenodo.org/records/999','//ZENODO.ORG:0443/record/999/','zenodo.org/records/999','ZENODO.ORG:0443/records/999/export/json','www.zenodo.org:00443/records/999/files/paper.pdf','https://zenodo.org/records/000999','https://zenodo.org/records/%39%39%39','https://zenodo.org/%72ecords/999','https://zenodo.org/records/%2e/999','https://zenodo.org/path/../records/999','https://zenodo.org/records/999/../999','https://zenodo.org/records/999/files/dir/file.pdf','https://zenodo.org/api/records/999/draft','https://zenodo.org/records/999/versions/latest']
AMBIGUOUS=['https://zenodo.org./records/999','https://zenodo.org../records/999','https://zenodo.org:444/records/999','https://zenodo.org:/records/999','https://zenodo.org:abc/records/999','https://zenodo.org:65536/records/999','https://user:pass@zenodo.org/records/999','https://zenodo.org@evil.example/records/999','ftp://zenodo.org/records/999','https:/zenodo.org/records/999','https//zenodo.org/records/999','https:///zenodo.org/records/999','https://zenodo.org\\evil/records/999','https://zenodo.org/%ZZ/999','https://zenodo.org/records%2F999','https://zenodo.org/records%252F999','https://zenodo.org/unknown/999','https://zenodo.org/records/','https://zenodo.org/records/999abc','https://zenodo.org/records/９９９','https://zenodo.org/records/0','https://zenodo.org/records/-999','https://zenodo.org/records/999/unknown','https://zenodo.org/records/999/export','https://zenodo.org/records/999/export/json/extra','https://zenodo.org/../records/999','https://z%65nodo.org/records/999','zenodo.org:80/records/999','https://zenodo.org/records/'+('9'*129),'https://zenodo.org/records/999/files/'+('a'*16400),'zenodo.org\\records\\999','//zenodo.org\\records\\999','user@zenodo.org/records/999','user:pass@zenodo.org/records/999','https:user@zenodo.org/records/999',('u'*400)+'@zenodo.org/records/999']
DISTINCT=['10.5281/zenodo.0999','10.5281/zenodo.9990','10.5281/zenodo.1999','10.5281/zenodo.999abc','10.5281/zenodo.999/extra','https://zenodo.org/records/9990','https://zenodo.org:443/records/1999','https://zenodo.org/record/9990/export/json','https://zenodo.org/records/999/../1999','https://zenodo.org.evil/records/999','https://evilzenodo.org/records/999','https://evil.example/path/zenodo.org/records/999','https://evil.example/?url=https://zenodo.org/records/999','https://evil.example/#//zenodo.org/records/999','https://zenodo.orℊ/records/999','https://ＺＥＮＯＤＯ.ＯＲＧ/records/999','xzenodo.org/records/999','zenodo.orgfoo/records/999','www.zenodo.orgfoo/records/999','zenodo.orgℊ/records/999','zenodo.org.evil/records/999']

def check(value,message):
    if not value:raise RuntimeError('CONTROL CHECK FAILED: '+message)

def forbidden(*a,**k):
    PROVIDERS.append(True);raise RuntimeError('ACTUAL PROVIDER FORBIDDEN')

def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False)+'\n')

def pipeline(root,rows,exempt=False,bypass=False,after=None,before_allocation=False,family=False):
    root.mkdir();repo=root/'repo';repo.mkdir();(root/'private').mkdir();current=[B.HEADERS]+copy.deepcopy(rows);desired=D.desired_row(999);calls=[];reads=[]
    write(root/'raw/pr0399/ledger_live.json',{'values':[B.HEADERS]})
    exemption_rows=copy.deepcopy(rows)+(copy.deepcopy(after[1:]) if after and exempt else [])
    unique={B.digest(row):row for row in exemption_rows}
    write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',{'pr':399,'root_identity_reconciliation_complete':True,'unresolved_leads':[],'release_manifest_sha256':B.RELEASE_SHA,'account_leads':[],'ledger_leads':[{'values_sha256':key,'disposition':'distinct_non_target'} for key in unique] if exempt else [],'unrelated_local_state_exemptions':[]})
    write(root/'ZENODO_PUBLIC_FILE_VERIFICATION.json',{'synthetic':True})
    record={'id':999,'metadata':{'title':B.TITLE},'files':[]}
    if family:record.update(conceptrecid='888',conceptdoi='10.5281/zenodo.888')
    class Client:
        base='https://offline.invalid'
        def request(self,method,url):
            from urllib.parse import parse_qs,urlsplit
            check(method=='GET','synthetic account reads only')
            q=parse_qs(urlsplit(url).query).get('q',[''])[0]
            records=[{'id':23174283,'metadata':{'title':'Fibonacci'},'files':[]}] if q=='Fibonacci' else [record]
            return {'hits':{'total':len(records),'hits':copy.deepcopy(records)},'links':{}}
    def command(args):
        if args[0]=='gws':return {'values':copy.deepcopy(current)}
        if args[-1].endswith('/pulls/399'):
            return {'number':399,'state':'open' if before_allocation else 'closed','merged':not before_allocation,'draft':before_allocation,'head':{'sha':B.ORIGINAL if before_allocation else 'a'*40,'ref':B.BRANCH,'repo':{'full_name':'AlecKriebel/Math'}},'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}
        return {'object':{'sha':'b'*40}}
    def gws(action,params,body=None):
        if action=='get':
            reads.append(True)
            if after is not None and len(reads)==2:current[:]=copy.deepcopy(after)
            return {'values':copy.deepcopy(current)}
        check(action=='append' and (root/'LEDGER_APPEND_INTENT.json').is_file(),'durable intent before exactly intended synthetic append')
        check(body['values']==[desired],'exact intended row');calls.append(copy.deepcopy(body));current.append(copy.deepcopy(desired))
        return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':[desired]}}}
    result={'status':None,'append_calls':0,'reason':None,'matching_rows':None,'bypassed_upstream':bypass}
    public={'record':999,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':200},'release_manifest_sha256':B.RELEASE_SHA}
    with ExitStack() as guards:
        for module,key,value in [(P,'ROOT',root),(P,'PRIVATE',root/'private'),(P,'REPO',repo),(P,'verify_destination',lambda:None),(P,'read_command',command),(P.zenodo,'ZenodoClient',lambda *a:Client()),(P.zenodo,'token_for',lambda *a:'unused'),(G,'AUDIT',root),(D,'AUDIT',root),(D,'PRIVATE',root/'private'),(D,'require_release_clearance',lambda:None),(D,'verify_live',lambda *a:public),(D,'gws',gws)]:guards.enter_context(patch.object(module,key,value))
        if bypass:
            gate={'started_utc':B.stamp(),'receipt':'synthetic','ledger_sha256':B.digest(current),'expected_identity_record_ids':[888,999] if family else [999]};acceptance={}
        else:
            try:gate=P.gather('before_integration' if before_allocation else 'before_ledger',B.ORIGINAL if before_allocation else 'a'*40,None if before_allocation else 999)
            except RuntimeError as ex:result.update(status='collector_rejected',reason=str(ex));return result
            result['matching_rows']=len(gate['ledger_matches'])
            if before_allocation:result['status']='collector_accepted';return result
            try:acceptance=G.reconcile(gate,'before_ledger','a'*40,999,True)
            except RuntimeError as ex:result.update(status='gate_rejected',reason=str(ex));return result
        with patch.object(D,'collect',lambda *a,**k:(gate,acceptance)):
            try:receipt=D.append_verified('a'*40,999)
            except RuntimeError as ex:result.update(status='append_rejected',reason=str(ex))
            else:result.update(status='verified',returned_unique=receipt['unique_target_and_DOI'])
        result['append_calls']=len(calls)
        if result['status']!='verified':check(not (root/'LEDGER_PUBLICATION_VERIFICATION.json').exists(),'no false uniqueness receipt')
    return result


def run_case(work,name,rows,expected_status,expected_calls=0,**kwargs):
    root=work/str(len(CASES));result=pipeline(root,rows,**kwargs)
    check(result['status']==expected_status and result['append_calls']==expected_calls,name+' '+repr(result))
    CASES.append({'case':name,**result})


def main():
    with ExitStack() as guards:
        guards.enter_context(patch.object(socket,'socket',forbidden));guards.enter_context(patch.object(subprocess,'run',forbidden));guards.enter_context(patch.object(V,'urlopen',forbidden))
        for name in ['request','create','upload','update','publish','get']:guards.enter_context(patch.object(B.zenodo.ZenodoClient,name,forbidden))
        with tempfile.TemporaryDirectory(prefix='route_controls_',dir=HERE) as tmp:
            work=Path(tmp)
            for index,alias in enumerate(OBSERVED+ADDITIONAL):
                for column in range(4):
                    row=['','','',''];row[column]=alias
                    for exempt in [False,True]:
                        run_case(work,'complete_alias_'+str(index)+'_'+str(column)+'_'+str(exempt),[row],'gate_rejected',exempt=exempt)
                        run_case(work,'independent_append_alias_'+str(index)+'_'+str(column)+'_'+str(exempt),[row],'append_rejected',bypass=True,exempt=exempt)
                alias_row=['','','',alias]
                after=[B.HEADERS,D.desired_row(999),alias_row]
                run_case(work,'idempotent_readback_introduced_alias_'+str(index),[D.desired_row(999)],'append_rejected',after=after)
            for index,alias in enumerate(AMBIGUOUS):
                for column in range(4):
                    row=['ordinal lead','','10.5281/zenodo.999',''];row[column]=alias
                    run_case(work,'unknown_before_allocation_'+str(index)+'_'+str(column),[row],'collector_rejected',before_allocation=True)
                    run_case(work,'unknown_independent_append_'+str(index)+'_'+str(column),[row],'append_rejected',bypass=True,exempt=True)
                run_case(work,'unknown_introduced_readback_'+str(index),[D.desired_row(999)],'append_rejected',after=[B.HEADERS,D.desired_row(999),['','','',alias]])
            for index,value in enumerate(DISTINCT):
                run_case(work,'nearby_distinct_identity_'+str(index),[['','','',value]],'verified',1)
            run_case(work,'literal_desired_row_idempotent',[D.desired_row(999)],'verified')
            run_case(work,'genuine_absence_one_append',[],'verified',1)
            run_case(work,'canonical_and_alias_combined',[D.desired_row(999),['','','',OBSERVED[0]]],'gate_rejected',exempt=True)
            run_case(work,'multiple_aliases_combined',[['',OBSERVED[1],OBSERVED[2],OBSERVED[3]]],'gate_rejected',exempt=True)
            run_case(work,'family_route_target_precedence',[['','','','https://zenodo.org:443/records/888/export/json']],'gate_rejected',family=True,exempt=True)
            citation='OWR 10/2016 pp.479–481. https://doi.org/10.4171/OWR/2016/10'
            ordinary=[citation,citation.replace('–','-'),citation.replace('OWR','owr'),'Date: 10/21/2026',r'Fraction: \frac{10}{2016}', 'The fraction (10)/(2016) is rational.']
            for number,text in enumerate(ordinary):
                run_case(work,'ordinary_bibliography_fraction_date_'+str(number),[[text,'','','']],'verified',1)
            for number,text in enumerate([citation.replace('/2016/10','/2015/10'),citation.replace('/2016/10','/2016/100'),citation.replace('/2016/10','/2016/10.other'),citation.replace('479–481','481–479'),'OWR 10/2016 pp.479–481.','10/2016','DOI: 10/2016',citation+' https://doi.org/10/2016',citation+' 10/abc']):
                run_case(work,'unresolved_numeric_or_other_shortdoi_'+str(number),[[text,'','','']],'collector_rejected',before_allocation=True)
                run_case(work,'independent_unresolved_numeric_or_shortdoi_'+str(number),[[text,'','','']],'append_rejected',bypass=True,exempt=True)
            run_case(work,'bibliography_never_hides_target',[[citation,'','',OBSERVED[0]]],'gate_rejected',exempt=True)
            # The standalone matches function also may not skip an ambiguous
            # later cell merely because an earlier cell contains a model term.
            try:D.matches([B.HEADERS,['ordinal','','10.5281/zenodo.999',AMBIGUOUS[0]]],999)
            except RuntimeError:CASES.append({'case':'matches_no_model_shortcut','status':'matches_rejected','append_calls':0})
            else:raise RuntimeError('matches hid a later unresolved official URL')
    check(not PROVIDERS,'zero actual provider attempts')
    result={'implementation':KIND,'optimization':sys.flags.optimize,'controls':len(CASES),'all_controls_passed':True,'actual_provider_attempts':len(PROVIDERS),'observed_9x4x2_pipeline_cases':72,'cases':CASES,'scope':'Actual collector/account pagination/reconcile/independent append/readback. Only service interfaces and clearance/publication prerequisites are synthetic. Conservative URL review leads, not HTTP equivalence or theorem identity.'}
    name=('CURRENT_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'CURRENT_CONTROLS.json') if KIND=='canonical' else ('PROPOSED_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'PROPOSED_CONTROLS.json');write(HERE/name,result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
