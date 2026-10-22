"""Externally adopted full-carrier and exact source contracts; no generic exemptions."""
from ops_core import require,sha,canonical,typed_equal,recursive_identity_hits
def validate_gate(plan,gate):
    items={i['pr']:i for i in plan['items']}
    require(type(gate)is dict and gate.get('plan_canonical_sha256')==sha(canonical(plan)),'Canonical plan gate binding')
    require(type(gate.get('semantic_decisions'))is list and type(gate.get('intrabatch'))is list and type(gate.get('cross_batch_eleven'))is list,'Complete semantic packet required')
    expected={(a,b)for a in items for b in items if a!=b}
    require({(d['pr'],d['other_pr'])for d in gate['intrabatch']}==expected and len(gate['intrabatch'])==1122,'Exact1122 intra-batch scope proofs')
    context={i['pr']:i for i in plan['separate_eleven_context']};eleven=gate['separate_eleven_prs'];require(type(eleven)is list and len(eleven)==11 and len(set(eleven))==11 and 1224 in eleven and set(eleven)==set(context),'Separate eleven inventory')
    require({(d['pr'],d['other_pr'])for d in gate['cross_batch_eleven']}=={(a,b)for a in items for b in eleven}and len(gate['cross_batch_eleven'])==374,'Every34-by11 exact cross-result comparison required')
    for d in gate['semantic_decisions']+gate['intrabatch']+gate['cross_batch_eleven']:
        require(d['pr']in items and d['target_four_cells_sha256']==items[d['pr']]['row_sha256']and type(d.get('scientific_reason'))is str and bool(d['scientific_reason']),'Exact target and individual scientific explanation')
        require(d.get('root_adopted')is False and d.get('classification')in ['DISTINCT_EXACT_RESULT','SAME_SELECTED_EXISTING_PUBLICATION_NOT_LEDGER_COVERAGE','SAME_AUDITED_CANDIDATE_SOURCE_NOT_LEDGER_COVERAGE'],'Only separately adopted proposed exact scope roles')
    for d in gate['intrabatch']:require(d['other_row_sha256']==items[d['other_pr']]['row_sha256'],'Other intra-batch literal scope drift')
    for d in gate['cross_batch_eleven']:require(d['other_row_sha256']==context[d['other_pr']]['row_sha256'],'Other eleven literal scope drift')
    require(gate.get('unresolved')==[],'Unresolved dated semantic objects cannot authorize an action')
    requests=gate['public_requests'];require(type(requests)is list and bool(requests)and len({r['key']for r in requests})==len(requests),'Unique complete publication requests')
    for r in requests:
        if r.get('body_policy')=='QUALIFIED_DOI_ROUTE_ONLY':require(r['role']=='doi'and r.get('stream_hash_only')is True and type(r.get('qualification'))is str and bool(r['qualification']),'Route-only policy restricted to explicitly qualified DOI redirects')
        else:require(r.get('body_policy','EXACT_COMPLETE_BODY')=='EXACT_COMPLETE_BODY','Unknown publication body policy')
    for i in plan['items']:
        roles={r['role']for r in requests if i['pr']in r['target_prs']}
        require('pr' in roles,'Every candidate needs current PR binding')
        require({'registry','doi'}.issubset(roles)if i['row'][2]else'source' in roles,'Every selected DOI or intentional source-only role must be observed')
        prs=[r for r in requests if i['pr']in r['target_prs']and r['role']=='pr']
        require(sorted(r['pr']for r in prs)==sorted(i['associated_prs']),'All35 exact associated PR observations required')
        require(all(r['url']=='https://api.github.com/repos/AlecKriebel/Math/pulls/'+str(r['pr'])for r in prs),'Wrong PR route')
        if i['row'][2]:
            doi=[r for r in requests if i['pr']in r['target_prs']and r['role']=='doi'];require(len(doi)==1 and doi[0]['url']==i['row'][2],'Exact selected DOI route required')
        else:require(any(r['role']=='source'and i['pr']in r['target_prs']and r['url']in i['row'][3]for r in requests),'Source-only URL must occur in the adopted qualified row')
    return True
def publication_gate(gate,observed):
    expected={r['key']:r for r in gate['public_requests']};require(type(observed)is dict and set(observed)==set(expected),'Missing/extra publication source role')
    for key,r in expected.items():
        v=observed[key]
        require(type(v)is dict and type(v.get('status'))is int and v['status']==r['status']and v.get('final_url')==r['final_url'],'Exact DOI/source/PR route status or destination changed')
        require(v.get('complete')is True and type(v.get('bytes'))is int and v['bytes']>=0 and type(v.get('sha256'))is str and len(v['sha256'])==64,'Complete source/redirect hash receipt required')
        if r.get('body_policy')=='QUALIFIED_DOI_ROUTE_ONLY':
            require(r['role']=='doi'and r.get('stream_hash_only')is True,'DOI policy cannot project scientific metadata');continue
        require(type(v.get('bytes'))is int and v['bytes']==r['bytes']and v.get('sha256')==r['sha256']and v.get('complete')is True,'Complete publication body changed')
        if 'body' in v:require(sha(canonical(v['body']))==r['canonical_body_sha256'],'Full typed publication body changed')
def semantic_gate(plan,gate,observed,account,publication):
    allowed={}
    for d in gate['semantic_decisions']:
        key=(d['pr'],d['kind'],d['body_sha256']);require(key not in allowed,'Duplicate exact semantic decision');allowed[key]=d
    witnessed=set();context={sha(canonical(i['row'])):i for i in plan['separate_eleven_context']};cross={(d['pr'],d['other_pr']):d for d in gate['cross_batch_eleven']}
    carriers=[('sheet',r)for r in observed['values'][1:]]+[('owned',r)for r in account['passes'][1]['records'].values()]+[('local',r)for r in account['local']]
    carriers +=[('public',v['body'])for v in publication['responses'].values()if'body'in v]
    for kind,body in carriers:
        if kind=='sheet'and any(typed_equal(body,i['row'])for i in plan['items']):continue
        for i in plan['items']:
            hits=recursive_identity_hits(body,i)
            if hits:
                digest=sha(canonical(body))
                if kind=='sheet'and digest in context:
                    d=cross[(i['pr'],context[digest]['pr'])];require(d['other_row_sha256']==digest,'Exact separate eleven vector changed');continue
                key=(i['pr'],kind,digest);require(key in allowed,'New/changed complete matching '+kind+' carrier forPR'+str(i['pr']))
                require(typed_equal(hits,allowed[key]['matched']),'Complete matching aliases changed')
                witnessed.add(key)
    require(witnessed==set(allowed),'Previously reviewed matching carrier disappeared; fresh individual rebind required')
