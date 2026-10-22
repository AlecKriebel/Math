"""Offline replay and active omission/DOI-policy falsification. No service operations."""
from pathlib import Path
import json,gzip,hashlib,types,copy
O=Path(__file__).resolve().parent
def gz(p):return json.loads(gzip.decompress(p.read_bytes()))
def load():
    ns={'__file__':str(O/'source/bootstrap.py'),'__name__':'_unit_captured_bootstrap'};exec(compile((O/'source/bootstrap.py').read_bytes(),ns['__file__'],'exec',optimize=0),ns)
    source=hashlib.sha256((O/'source/SOURCE_MANIFEST.json').read_bytes()).hexdigest();m,v=ns['load_verified'](source);return m,v,source
def replay():
    M,verify,source=load();C=M['ops_core'];G=M['gates'];plan=json.loads((O/'PROPOSAL.json').read_bytes());gate=gz(O/'private/REVIEWED_GATE_PROPOSED.json.gz');G.validate_gate(plan,gate);obs=json.loads((O/'INITIAL_READONLY_COLLECTION.json').read_bytes());numeric=gz(O/obs['numeric']['path']);records=gz(O/obs['owned_complete'][0]['path'])['records'];local=gz(O/obs['local']['path']);pub=gz(O/'private/PUBLIC_INITIAL_COMPLETE.json.gz')['results'];pub['1253_registry_0']=gz(O/'private/PUBLIC_1253_FOLLOWUP.json.gz')['result'];account={'passes':[{'records':records},{'records':records}],'local':local};publication={'responses':pub};G.publication_gate(gate,pub);G.semantic_gate(plan,gate,numeric,account,publication)
    results=[{'name':'actual_dated3340_complete_carrier_and_source_gate','pass':True}]
    def rejects(name,fn,expected):
        try:fn()
        except Exception as e:
            assert expected in str(e),(name,repr(e));results.append({'name':name,'pass':True,'error':repr(e)});return
        raise AssertionError(name+' accepted')
    candidate=next(d for d in gate['semantic_decisions']if d['kind']=='owned');remove=next(k for k,b in records.items()if C.sha(C.canonical(b))==candidate['body_sha256']);omitted={k:v for k,v in records.items()if k!=remove};a={'passes':[{'records':omitted},{'records':omitted}],'local':local};rejects('previous_complete_matching_carrier_omission',lambda:G.semantic_gate(plan,gate,numeric,a,publication),'Previously reviewed matching carrier disappeared')
    context=copy.deepcopy(numeric);context['values'] +=[i['row']for i in plan['separate_eleven_context']];G.semantic_gate(plan,gate,context,account,publication);results.append({'name':'exact_separate_eleven_vectors_use374_scope_comparisons_without_adding_rows','pass':True})
    r={'key':'fixture','role':'doi','stream_hash_only':True,'body_policy':'QUALIFIED_DOI_ROUTE_ONLY','status':403,'final_url':'https://publisher.invalid/exact-doi','bytes':1,'sha256':'a'*64,'qualification':'Synthetic explicitly qualified redirect, not a scientific source.'};v={'fixture':{'status':403,'final_url':r['final_url'],'bytes':2,'sha256':'b'*64,'complete':True}};G.publication_gate({'public_requests':[r]},v);results.append({'name':'explicit_DOI_route_policy_retains_actual_hash_receipt_without_freezing_anti_bot_HTML','pass':True})
    wrong=copy.deepcopy(v);wrong['fixture']['status']=200;rejects('DOI_policy_cannot_change_actual_status',lambda:G.publication_gate({'public_requests':[r]},wrong),'route status or destination changed')
    wrong=copy.deepcopy(v);wrong['fixture']['final_url']='https://publisher.invalid/unrelated';rejects('DOI_policy_cannot_change_final_target',lambda:G.publication_gate({'public_requests':[r]},wrong),'route status or destination changed')
    wrong=copy.deepcopy(gate);wrong['public_requests'][0]['body_policy']='QUALIFIED_DOI_ROUTE_ONLY';rejects('DOI_policy_cannot_apply_to_PR_or_scientific_metadata',lambda:G.validate_gate(plan,wrong),'restricted to explicitly qualified DOI redirects')
    strict={**r,'body_policy':'EXACT_COMPLETE_BODY'};rejects('default_body_policy_remains_exact',lambda:G.publication_gate({'public_requests':[strict]},v),'Complete publication body changed')
    closing=gz(O/'private/CLOSING_NUMERIC_COMPLETE_AND_RAW.json.gz')['numeric'];rejects('actual_later_row240_matching_carrier_requires_fresh_individual_adoption',lambda:G.semantic_gate(plan,gate,closing,account,publication),'New/changed complete matching sheet carrier forPR1257')
    verify();return {'source_manifest_sha256':source,'results':results,'all_passed':all(x['pass']for x in results),'production_effects':0,'root_action_adoption':False}
if __name__=='__main__':
    out=replay();(O/'SEMANTIC_AND_POLICY_UNIT_RESULTS.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps(out))
