def review_check(specs,freeze,freeze_pin,context):
    need(type(specs) is list and len(specs)>=2,'at least2 NEW whole-package reviews')
    need(all(type(s) is str and re.fullmatch(f'{i:02d}:[0-9a-f]{{64}}',s) for i,s in enumerate(specs,1)),'consecutive externally pinned review rounds')
    folder=A/'reviews'
    actual={'full_package_'+s.split(':')[0] for s in specs}
    need(actual=={'full_package_'+s.split(':')[0] for s in specs},'all numbered adverse/unfinished reviews must be supplied')
    prior=set();reviewers=set();last_end=None;rows=[];current_clean=[]
    mandatory={'RESULT.json','FULL_AUDIT.md','RESEARCH_LOG.md','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json'}
    originals=original_check();inherited=inherited_findings(freeze)
    for index,spec in enumerate(specs,1):
        number,pin=spec.split(':');base=folder/('full_package_'+number)
        raw=read_regular(base/'MANIFEST.json');need(sha(raw)==pin,'external complete review manifest')
        doc=strict_json(raw);records=doc.get('files');allowed=doc.get('explicit_public_allowlist')
        need(type(records) is dict and mandatory<=set(records) and type(allowed) is list and len(allowed)==len(set(allowed)) and set(allowed)==set(records) and 'MANIFEST.json' not in records,'sealed explicit review allowlist')
        captured={n:read_regular(base/n,pin=v) for n,v in records.items() if safe(n)}
        need(len(captured)==len(records) and all(captured[n].strip() for n in mandatory),'review paths/nonempty mandatory artifacts')
        result=strict_json(captured['RESULT.json']);complete=result_schema(result)
        rid=result['reviewer_agent_id'];need(rid not in reviewers,'distinct independent reviewers');reviewers.add(rid)
        start,end=utc(result['started_utc']),utc(result['completed_utc'])
        need(start<end and (last_end is None or last_end<start),'sequential NEW review chronology');last_end=end
        pins=result['candidate_pins'];review_base=D;review_freeze=freeze
        if pins['freeze']!=freeze_pin:
            review_base=D/'reviewed_candidates'/('candidate'+str(result['candidate_revision']).zfill(2))
            review_freeze=freeze_check(read_regular(review_base/'FREEZE.json'),pins['freeze'],context,review_base,historical=True)
        need(result['candidate_revision']==review_freeze['revision_candidate'] and pins['manifest']==review_freeze['package_manifest_sha256'] and pins['pdf']==review_freeze['files'][PDF]['sha256'],'entire scientific/operational candidate identity')
        inspected=result['inspected_helper_hashes'];expected=review_freeze['future_helpers']
        need(set(inspected)<=set(expected) and all(exact(value,expected[name]) for name,value in inspected.items()),'partial inspected helper pins must bind exact candidate')
        if complete:need(exact(inspected,expected),'completed review entire inspected helper inventory')
        a_start,t_start=review_authentication(strict_json(captured['AUTHENTICATION_START.json']),pins,review_freeze,originals)
        a_end,t_end=review_authentication(strict_json(captured['AUTHENTICATION_END.json']),pins,review_freeze,originals)
        need(start<=t_start<=t_end<=end,'before/after review timestamps')
        cold_pass,t_cold=review_cold(strict_json(captured['COLD_REPLAY.json']),pins,review_freeze,review_base)
        need(t_start<=t_cold<=t_end,'cold observation outside authentication bracket')
        full_evidence=a_start and a_end and cold_pass
        if not complete or not full_evidence:
            need(result.get('nonclean_history') is not None and result['clean_for_preprint'] is False,'incomplete/failed evidence requires honest nonclean RESULT')
        for issues in (result['required_issues'],result['optional_issues']):
            need(all(type(x) is dict and type(x.get('id')) is str and x['id'] for x in issues),'every required/optional finding ID')
        def verified(mapping,key):
            value=mapping.get(key)
            return type(value) is dict and value.get('verified') is True and type(value.get('evidence')) is str and bool(value['evidence'].strip())
        clean_current=(pins['freeze']==freeze_pin and complete and full_evidence and result['clean_for_preprint'] is True and result.get('nonclean_history') is None)
        if clean_current:
            need(all(verified(result['prior_issue_resolution'],key) for key in prior),'all earlier required AND optional findings independently dispositioned')
            need(all(verified(result['inherited_finding_dispositions'],key) for key in inherited),'fresh reviewers verify all50 inherited dispositions')
            need(utc(freeze['created_utc'])<=start,'current review starts after freeze')
            current_clean.append(index)
        else:current_clean=[]
        prior.update(x['id'] for x in result['required_issues']+result['optional_issues'])
        rows.append({'round':index,'manifest_sha256':pin,'completed_utc':result['completed_utc'],'candidate_freeze_sha256':pins['freeze'],'required_issues':result['required_issues'],'optional_issues':result['optional_issues'],'completion_flags':{k:result[k] for k in ('clean_context','full_reproducer_completed','entire_package_review')},'evidence_statuses':{k:strict_json(captured[k])['status'] for k in ('AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json')},'nonclean_history':result.get('nonclean_history'),'eligible_clean_current':clean_current})
    need(len(current_clean)>=2 and current_clean[-1]==len(specs),'at least TWO fresh clean ENTIRE current-package reviews after every fix')
    return rows,result
