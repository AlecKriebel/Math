"""Pure current native-presentation constructor, with a separate actual-facts gate.
No backend import, API installation or file write occurs in this module.
"""
S=None
ADDED=frozenset(('CURRENT_STATUS.json','CURRENT_PROOF.md','CURRENT_PROOF_SOURCE.tex','CURRENT_SOURCE_AND_PRIORITY.json','CURRENT_PROVENANCE.json','CURRENT_RESEARCH_LOG.md','CURRENT_PUBLICATION_LEDGER.json','NATIVE_PRESENTATION_RECEIPT.json','SHA256SUMS','requirements-current.txt'))
STAGES=frozenset(('published_pending_merge','actual_merge_accepted','actual_factual_accepted_completion_pending'))


def configure(support):
    global S
    if S is not None:raise RuntimeError('Fresh native constructor required')
    S=support


def current_names():return set(S.originals()[1])|set(ADDED)


def validate_shape(stage,f):
    S.need(stage in STAGES,'Native factual stage')
    required={'schema','original_head','UTC','package_seal','publication_ready_gate','publication_receipt','tracker_receipt'}|({'merge_receipt'} if stage=='actual_merge_accepted' else {'merge_receipt','factual_receipt'} if stage=='actual_factual_accepted_completion_pending' else set())
    S.need(type(f) is dict and set(f)==required and f['schema']=='pr206-native-actual-facts-v1' and f['original_head']==S.HEAD,'Exact native actual-facts shape')
    stamp=S.datetime.datetime.fromisoformat(f['UTC']);S.need(stamp.utcoffset()==S.datetime.timedelta(0),'Native UTC timestamp')
    for name in required-{'schema','original_head','UTC'}:
        value=f[name];S.need(type(value) is dict and set(value)=={'path','bytes','sha256'},'Explicit native receipt pointer');S.rel(value['path']);S.bytepin({k:value[k] for k in ('bytes','sha256')})


def validate_facts(stage,f):
    S.authority();validate_shape(stage,f);g,p,t,context=S.operations()
    wanted={'package_seal':S.pp(g['package']+'/'+g['package_seal_file'],g['package_seal']),'publication_ready_gate':S.pp(S.PUBLICATION_GATE,context['gate_pin']),'publication_receipt':S.pp('ROOT_PUBLICATION_RECEIPT.json',S.pin(S.frozen('ROOT_PUBLICATION_RECEIPT.json'))),'tracker_receipt':S.pp('ROOT_TRACKER_RECEIPT.json',S.pin(S.frozen('ROOT_TRACKER_RECEIPT.json')))}
    for name,value in wanted.items():S.need(f[name]==value,'Exact actual native receipt binding '+name)
    for kind in (() if stage=='published_pending_merge' else ('merge',) if stage=='actual_merge_accepted' else ('merge','factual')):
        state=S.actual(kind);a=state['receipt'];S.need(a['facts']['completed'] is False and all(a['facts'][k]==v for k,v in S.BASE_COUNTS.items()),'Native predecessor remains incomplete')
        S.need(f[kind+'_receipt']==S.pp(state['directory'][len(S.CASE):]+'ACCEPTANCE.json',S.pin(S.read(state['directory']+'ACCEPTANCE.json'))),'Exact actual native predecessor receipt')
        S.need(a['facts']['actual_merge_accepted'] is True and (kind!='factual' or a['facts']['actual_factual_accepted'] is True),'Actual merge/factual predecessor facts')
    return g,p,t


def render(stage,f,old,portable,proof_source,g,p,t):
    """Pure proposed bytes. Callers must separately validate actual Root facts."""
    validate_shape(stage,f);S.need(len(old)==21 and sum(len(b) for b in old.values())==55033 and not (set(old)&set(ADDED)) and S.pin(portable)==S.PORTABLE,'Exact original21 and current portable source')
    S.need(type(proof_source) is bytes and S.pin(proof_source)==g['package_safe_files'][g['manuscript_source_file']],'Exact approved manuscript source proof copy')
    S.need(g['source_facts']==S.SOURCE_FACTS and p['doi']=='10.5281/zenodo.'+str(p['id']) and t['doi']==p['doi'],'Qualified actual native rendering facts')
    archive=S.CASE+'original_submitted_head/';merged=stage!='published_pending_merge';factual=stage=='actual_factual_accepted_completion_pending'
    current={'UTC':f['UTC'],'PR':206,'problem_id':5100062,'original_head':S.HEAD,'declared_PR_base':S.DECLARED,'authenticated_authored_range_base':S.FORK,'status':'claimed_solved','original_effort_cell':'1/5','original_author_effort_unverified':True,'original_author_commit_count':4,'author_effort':S.EFFORT,'native_stage':stage,'exact_claim':S.CLAIM,'credit_and_limits':S.CREDIT,'source_facts':S.SOURCE_FACTS,'mathematical_clearance':True,'source_contract_clearance':True,'bounded_priority_audit_complete':True,'priority_clearance_scope':'qualified_attributed_verification_note_only','theorem_novelty_cleared':False,'formula_novelty_cleared':False,'proof_method_novelty_cleared':False,'historical_firstness_independence_established':False,'independent_discovery_certified':False,'literal_simultaneity_established':False,'current_openness_established':False,'actual_publication_verified':True,'actual_tracker_row_verified':True,'actual_original_merge_accepted':merged,'actual_factual98_accepted':factual,'program_completion_accepted':False,'completed':False,'DOI':p['doi'],'record_id':p['id'],'tracker_range':t['range'],'publication_title':g['metadata']['title'],'publication_package':S.CASE+g['package'],'program_completion_authority':'Separate actual100 native acceptance plus full local-five sync and completion pointer; native factual98 never supplies completion.','extensive_AI_use':True,'unrefereed':True,'conventional_human_peer_review':False,'formal_proof_assistant_certification':False}
    provenance={name:{'path':archive+name,**S.bpin(raw)} for name,raw in old.items()}
    out={}
    for name in old:
        history={'historical_original':provenance[name],'historical_original_claims_not_current_authority':True,'current_status_file':'CURRENT_STATUS.json','current_source_and_priority_file':'CURRENT_SOURCE_AND_PRIORITY.json','current':current}
        if name.endswith('.json'):out[name]=S.enc(history)
        elif name.endswith('.md'):
            out[name]=('# Current Root-gated presentation: '+name+'\n\n'+g['metadata']['title']+'\n\n'+S.CLAIM+'\n\n'+S.CREDIT+'\n\n'+S.EFFORT+'\n\nActual research note: https://doi.org/'+p['doi']+'. Current proof copy: CURRENT_PROOF_SOURCE.tex; CURRENT_SOURCE_AND_PRIORITY.json records exact credited sources and limits. Original file remains immutable at '+provenance[name]['path']+'; its favorable labels, source declarations, current-open classifications and PASS counts are dated historical input only. Extensive AI; unrefereed; no conventional human peer review.\n').encode()
        elif name.endswith('.py'):out[name]=portable
        else:S.need(False,'Explicit original native extension required')
    S.need({'verify_triangles.py','independent_review/independent_check.py'}=={name for name in old if name.endswith('.py')},'Exactly two current executable paths')
    out['verify_triangles.py']=portable;out['independent_review/independent_check.py']=portable
    out['CURRENT_STATUS.json']=S.enc(current);out['CURRENT_SOURCE_AND_PRIORITY.json']=S.enc({**current,'historical_target':'RGK k903,a, Table10 page12, row k903,a dated10/20 (October2020); source nomenclature interpreted by exact Root source gate','RGH_delta_qualification':'Public preprint delta defect is disclosed; journal full text/typography uninspected. Corrected-plus-b4 comparison is only an exact control, not a claimed general corrected formula.','Chavez_DOI':'10.1007/s40598-020-00154-8','prior_exact_overlap':{'author':'Alper Ferudun','DOI':'10.5281/zenodo.23096994','same_target':True,'substantially_same_flag_curve_mechanism':True},'record_date_limit':'Specified GitHub/Zenodo record timestamps do not certify first public availability, repository visibility history, independence or priority.'})
    out['CURRENT_PROVENANCE.json']=S.enc({'original21_archive':provenance,'original_archive_bytes':55033,'all_original_bytes_immutable_in_audit_archive':True,'native_current_wrappers_replace_historical_claims':True,'historical_favorable_reviews_not_new_whole_package_events':True,'historical_unsafe_assertion_checkers_not_current_validation':True,'current_checker_paths':{'verify_triangles.py':S.PORTABLE,'independent_review/independent_check.py':S.PORTABLE},'current_finite_limits':'Four explicit genuine convex primitive polygons only; finite exact controls do not prove all odd periods/stars or novelty. Radical sign guards fail closed after4096bits.','source_gate':S.pp('ROOT_MATHEMATICAL_SOURCE_GATE_01.json',S.FIXED_GATES['ROOT_MATHEMATICAL_SOURCE_GATE_01.json']),'priority_gate':S.pp('ROOT_PRIORITY_EDITORIAL_GATE_01.json',S.FIXED_GATES['ROOT_PRIORITY_EDITORIAL_GATE_01.json']),'current_verifier_adoption':S.pp('ROOT_CURRENT_VERIFIER_ADOPTION_01.json',S.FIXED_GATES['ROOT_CURRENT_VERIFIER_ADOPTION_01.json'])})
    out['CURRENT_PROOF_SOURCE.tex']=proof_source
    out['CURRENT_PROOF.md']=('# Current attributed proof source\n\n'+S.CLAIM+'\n\n'+S.CREDIT+'\n\nThe exact Root-reviewed manuscript source is copied byte-for-byte to CURRENT_PROOF_SOURCE.tex. The matching reviewed PDF/source are '+S.CASE+g['package']+'/'+g['manuscript_pdf_file']+' and '+g['manuscript_source_file']+'. DOI https://doi.org/'+p['doi']+'. The original CANDIDATE.md is preserved in the immutable audit archive and is not the current bibliography/priority authority.\n').encode()
    out['README.md']=('# '+g['metadata']['title']+'\n\n'+S.CLAIM+'\n\n'+S.CREDIT+'\n\n'+S.EFFORT+'\n\nDOI https://doi.org/'+p['doi']+'; tracker '+t['range']+'. Extensive AI assistance; unrefereed; no conventional human peer review or formal proof-assistant certificate. Current scientific/source/priority scope: CURRENT_STATUS.json, CURRENT_PROOF_SOURCE.tex, CURRENT_SOURCE_AND_PRIORITY.json. CURRENT_PROVENANCE.json authenticates every original archive leaf and labels original reviews and PASS counts historical.\n\nBoth current executable paths verify_triangles.py and independent_review/independent_check.py are the same exact Root-accepted dependency-free source. Run python3 -E -S -B -P verify_triangles.py or python3 -E -S -B -P -O independent_review/independent_check.py. These exact controls cover four specified convex primitive polygons only and fail closed at4096-bit radical sign bounds; they do not computationally prove arbitrary odd periods/stars or priority. Original assertion-dependent programs remain unchanged in the21-file audit archive.\n\nActual publication/tracker and already-accepted predecessor facts only are listed in CURRENT_PUBLICATION_LEDGER.json. Even factual98 remains incomplete; program completion requires the separate actual100 full acceptance/local-five sync/pointer. No native wrapper authorizes207 intake.\n').encode()
    out['CURRENT_RESEARCH_LOG.md']=(f['UTC']+' — '+stage+'. '+S.CLAIM+' '+S.CREDIT+' '+S.EFFORT+' Archived21/55033 immutable; current two executable paths exact21804 dependency-free finite source; no claimed current openness or novel theorem/method. Factual98 is incomplete; actual100 authority is separate.\n').encode()
    out['CURRENT_PUBLICATION_LEDGER.json']=S.enc({'current':current,'actual_receipt_bindings':f,'package_seal':f['package_seal'],'actual_publication_receipt':f['publication_receipt'],'actual_tracker_receipt':f['tracker_receipt'],'future_program_completion_fact_omitted':True})
    out['NATIVE_PRESENTATION_RECEIPT.json']=S.enc({'UTC':f['UTC'],'stage':stage,'original21':provenance,'native_current_paths':sorted(set(old)|set(ADDED)),'current_checker_source':S.PORTABLE,'proof_source_copy':S.pp(g['package']+'/'+g['manuscript_source_file'],S.pin(proof_source)),'facts':f,'program_completion_accepted':False})
    out['requirements-current.txt']=b'Python 3.11 or newer; Python standard library only. No third-party dependency installation required.\n'
    out['FROZEN_MANIFEST.json']=S.enc({'scope':'Current native presentation; original manifest remains unchanged in audit archive.','original_manifest':provenance['FROZEN_MANIFEST.json'],'files':{name:S.bpin(raw) for name,raw in sorted(out.items()) if name not in ('FROZEN_MANIFEST.json','SHA256SUMS')}})
    out['SHA256SUMS']=''.join(S.hashlib.sha256(raw).hexdigest()+'  '+name+'\n' for name,raw in sorted(out.items()) if name!='SHA256SUMS').encode()
    S.need(set(out)==set(old)|set(ADDED) and len(out)==31 and out['verify_triangles.py']==out['independent_review/independent_check.py']==portable,'Exact31 native path/current-checker set')
    return {S.NATIVE+name:raw for name,raw in out.items()}


def construct(stage,facts):
    g,p,t=validate_facts(stage,facts);old=S.originals()[1]
    portable=S.frozen(g['package']+'/'+g['portable_source_file'],S.PORTABLE);proof=S.frozen(g['package']+'/'+g['manuscript_source_file'],g['package_safe_files'][g['manuscript_source_file']])
    return render(stage,facts,old,portable,proof,g,p,t)
