"""Focused actual parsed12 publication/public/append and late-boundary controls."""
from pathlib import Path
engine=Path(__file__).with_name('ENGINE17.py')
exec(compile(engine.read_bytes(),str(engine),'exec',dont_inherit=True,optimize=0),globals())
need(MS=='623a85eca963527260367dd192bb0373f6a81972179633fa6f219c72a6237803','Final12 source anchor');need(BS=='5a60e8743ab5dd72e113a75f9af370974a0895bdabd8e68321d58701c947ae94','Final12 bootstrap anchor')
def outcome(label,w,ok,a,e,before,delta,details=None):
    record(label,w,ok,a,e,before,delta,details);need(checks[-1]['status']=='PASS','Parsed12 counterexample '+label)
def full(w):
    with w.installed():
        for action in ['resume-stage','publish','verify-public','ledger']:
            a,e=run(w,action);need(e is None,'Positive phase '+action+': '+str(e))
    return a,e
for style in ['actual','old']:
    label='full_actual_publication_and_public_aliases_'+style;w=setup(label);w.append_reply_style=style;a,e=full(w)
    response=json.loads((m.RUNTIME/'LEDGER_APPEND_RESPONSE.json').read_bytes())
    need((('commentUpdateState'in response)==(style=='actual')) and(m.RUNTIME/'LEDGER_APPEND_ACKNOWLEDGED.json').exists(),'Observed reply/acknowledged append not exercised')
    outcome(label,w,True,a,e,(0,0),{'native':5,'append':1},{'append_reply_keys':sorted(response),'actual_publication_profile':True})
w=setup('public_alias_negative_group','ledger');proper=w.native.public
for label,mutate in [
 ('ledger_rejects_wrong_recid',lambda p:p.__setitem__('recid','999')),
 ('ledger_rejects_wrong_file_UUID',lambda p:p['files'][0].__setitem__('id','00000000-0000-0000-0000-000000009999')),
 ('ledger_rejects_wrong_content_route',lambda p:p['files'][0]['links'].__setitem__('self','https://zenodo.org/api/records/999/files/foreign.pdf/content')),
 ('ledger_rejects_wrong_duplicate_title',lambda p:p.__setitem__('title','Foreign title'))]:
    def corrupted():p=proper();mutate(p);return p
    w.native.public=corrupted;before=(len(w.native.calls),w.appends)
    with w.installed():a,e=run(w,'ledger')
    need(not(m.RUNTIME/'LEDGER_APPEND_INTENT.json').exists()and not(m.RUNTIME/'LEDGER_VERIFIED.json').exists(),'Contrary public alias reached ledger write/certification')
    outcome(label,w,False,a,e,before,{'native':0,'append':0},{'fixed_binary_downloads_remain_correct':not w.bytes_bad})
w.native.public=proper
for label,mutate in [
 ('ledger_rejects_conflicting_legacy_key',lambda e:e.__setitem__('key','a-different-paper.pdf')),
 ('ledger_rejects_conflicting_legacy_size',lambda e:e.__setitem__('size',0)),
 ('ledger_rejects_conflicting_legacy_file_id',lambda e:e.__setitem__('file_id','00000000-0000-0000-0000-000000009999')),
 ('ledger_rejects_conflicting_legacy_content',lambda e:e['links'].__setitem__('content','https://zenodo.org/api/records/999/files/foreign.pdf/content'))]:
    w.native.fault=lambda l,n,f:mutate(l['files'][0]);before=(len(w.native.calls),w.appends)
    with w.installed():a,e=run(w,'ledger')
    need(not(m.RUNTIME/'LEDGER_APPEND_INTENT.json').exists()and not(m.RUNTIME/'LEDGER_VERIFIED.json').exists(),'Contrary legacy alias reached append/certification')
    outcome(label,w,False,a,e,before,{'native':0,'append':0},{'primary_legacy_native_finalized_public_bytes_remain_correct':True})
for label,mutate in [
 ('ledger_rejects_residual12_legacy_root_title',lambda l:l.__setitem__('title','Contradictory supplied legacy title')),
 ('ledger_rejects_legacy_root_title_bool',lambda l:l.__setitem__('title',True)),
 ('ledger_rejects_legacy_root_record_id',lambda l:l.__setitem__('record_id',999)),
 ('ledger_rejects_legacy_root_concept',lambda l:l.__setitem__('conceptrecid','999')),
 ('ledger_rejects_legacy_root_owner_bool',lambda l:l.__setitem__('owner',True)),
 ('ledger_rejects_legacy_root_state',lambda l:l.__setitem__('state','unsubmitted')),
 ('ledger_rejects_legacy_root_DOI_URL',lambda l:l.__setitem__('doi_url','https://doi.org/10.5281/zenodo.999')),
 ('ledger_rejects_legacy_root_self_link',lambda l:l['links'].__setitem__('self','https://zenodo.org/api/records/999')),
 ('ledger_rejects_legacy_unknown_root',lambda l:l.__setitem__('unreviewed_identity',{'id':999})),
 ('ledger_rejects_legacy_root_modified',lambda l:l.__setitem__('modified','2000-01-01T00:00:00+00:00')),
 ('ledger_rejects_unsupported_legacy_status',lambda l:l.__setitem__('status','published'))]:
    w.native.fault=lambda l,n,f:mutate(l);before=(len(w.native.calls),w.appends)
    with w.installed():a,e=run(w,'ledger')
    need(not(m.RUNTIME/'LEDGER_APPEND_INTENT.json').exists()and not(m.RUNTIME/'LEDGER_VERIFIED.json').exists(),'Contrary legacy root reached append/certification')
    outcome(label,w,False,a,e,before,{'native':0,'append':0},{'raw_primary_metadata_native_finalized_public_intended_correct':True})
w.native.fault=None
(DEST/'public_alias_negative_group.json').write_text(json.dumps({'completed_cases':19,'all_rejected_before_append':True})+'\n')
w=setup('postpublish_wrong_derived_source','publish')
w.native.after=lambda l,n,f:next(iter(n['media_files']['entries'].values()))['processor'].__setitem__('source_file_id','00000000-0000-0000-0000-000000009999')
before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'publish')
need(not(m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists()and json.loads((m.RUNTIME/'PUBLISH_FAILURE.json').read_bytes())['id']==777,'Posteffect publication failure lost known ID')
outcome('postpublish_wrong_derived_source',w,False,a,e,before,{'native':1,'append':0})
with w.installed():
    before=(len(w.native.calls),w.appends);a,e=run(w,'publish')
outcome('postpublish_failure_no_retry',w,False,a,e,before,{'native':0,'append':0})
w=setup('late_checked_source_after_fsynced_publish_intent','publish');writer=c.durable;hit=[]
def source_change(path,value):
    writer(path,value)
    if path.name=='WRITE_publish_publish_INTENT.json':
        hit.append(True);p=m.CONTEXT['source_root']/'sheet17.py';p.write_bytes(p.read_bytes()+b'\n# inert case source corruption\n')
before=(len(w.native.calls),w.appends)
with model.patch((c,'durable',source_change)),w.installed():a,e=run(w,'publish')
need(hit,'Actual source fsync boundary missed');outcome('late_checked_source_after_fsynced_publish_intent',w,False,a,e,before,{'native':0,'append':0})
w=setup('late_canonical_competitor_unknown_field','publish');writer=c.durable;changed={}
def state_change(path,value):
    writer(path,value)
    if path.name=='WRITE_publish_publish_INTENT.json':
        target=c.zenodo.state_path(pub.MANIFEST.resolve(),'production');v=json.loads(target.read_bytes());v['concurrent_unknown']={'flag':True,'integer':1};changed['raw']=(json.dumps(v,indent=1)+'\n').encode();target.write_bytes(changed['raw'])
before=(len(w.native.calls),w.appends)
with model.patch((c,'durable',state_change)),w.installed():a,e=run(w,'publish')
need(c.zenodo.state_path(pub.MANIFEST.resolve(),'production').read_bytes()==changed['raw'],'Concurrent canonical bytes overwritten')
outcome('late_canonical_competitor_unknown_field',w,False,a,e,before,{'native':0,'append':0})
w=setup('intent_drift_after_long_fresh_target_read','publish');native=modules['native_policy'];writer=native.durable;hit=[]
def late_intent(path,value):
    writer(path,value);intent=m.RUNTIME/'WRITE_publish_publish_INTENT.json'
    if path.name=='verified.json'and intent.exists()and not hit:
        hit.append(True);v=json.loads(intent.read_bytes());v['known_id']=999;intent.write_text(json.dumps(v)+'\n')
before=(len(w.native.calls),w.appends)
with model.patch((native,'durable',late_intent)),w.installed():a,e=run(w,'publish')
need(hit,'Long target-read intention hook missed');outcome('intent_drift_after_long_fresh_target_read',w,False,a,e,before,{'native':0,'append':0})
w=setup('server_append_preserves_concurrent_writer','ledger');command=w.command;foreign=['Another concurrent paper','10.5281/zenodo.99999999','https://zenodo.org/records/99999999','PR #1329'];foreign_calls=[];old_rows=copy.deepcopy(w.rows)
def competing_append(argv,body=None):
    if argv[:4]==['gws','sheets','spreadsheets','batchUpdate']:
        payload=json.loads(argv[argv.index('--json')+1]);need(set(payload['requests'][0])=={'appendCells'},'Writer used addressed update')
        request=payload['requests'][0]['appendCells'];need(set(request)=={'sheetId','rows','fields'},'Writer supplies client row/range/table address')
        # A separate server-side append lands after the actor's final read and
        # before its own AppendCells application. Neither writer owns an index.
        w.rows.append(copy.deepcopy(foreign));foreign_calls.append({'operation':'appendCells','values':foreign})
    return command(argv,body)
before=(len(w.native.calls),w.appends)
with model.patch((w,'command',competing_append)),w.installed():a,e=run(w,'ledger')
own=pub.draft_row(777)
need(len(foreign_calls)==1 and w.rows==old_rows+[foreign,own]and w.appends==1,'One writer overwrote the other append')
need((m.RUNTIME/'LEDGER_APPEND_ACKNOWLEDGED.json').exists()and not(m.RUNTIME/'LEDGER_VERIFIED.json').exists(),'Concurrent append effect not retained or falsely certified')
(w.place/'BOTH_APPEND_EFFECTS.json').write_text(json.dumps({'foreign':foreign,'own':own,'suffix':w.rows[-2:],'own_appends':w.appends,'foreign_appends':len(foreign_calls)},indent=2)+'\n')
outcome('server_append_preserves_concurrent_writer',w,False,a,e,before,{'native':0,'append':1},{'foreign_append_effects':1,'both_writer_rows_preserved':True,'no_fake_last_row_precondition':True})
with w.installed():
    before=(len(w.native.calls),w.appends);a,e=run(w,'ledger')
need(w.rows==old_rows+[foreign,own],'GET-only reconciliation altered rows')
outcome('concurrent_append_GET_only_no_retry',w,False,a,e,before,{'native':0,'append':0})
w=setup('bad_comment_reply_after_one_append','ledger');w.final_response_fault=lambda response:response.__setitem__('commentUpdateState','UPDATED');before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'ledger')
need(not(m.RUNTIME/'LEDGER_VERIFIED.json').exists()and not(m.RUNTIME/'LEDGER_APPEND_ACKNOWLEDGED.json').exists(),'Unreviewed reply accepted')
outcome('bad_comment_reply_after_one_append',w,False,a,e,before,{'native':0,'append':1})
w=setup('old_history_change_after_final_certificate_fsync','ledger');sync=os.fsync;hit=[]
def after_sync(fd):
    result=sync(fd)
    if(m.RUNTIME/'LEDGER_VERIFIED.json').exists()and not hit:
        st=os.fstat(fd)
        if stat.S_ISDIR(st.st_mode):
            hit.append(True);p=m.PRIOR_RUNTIME/'INTEGRATE_INTENT.json';v=json.loads(p.read_bytes());v['inert_concurrent_history']=True;p.write_text(json.dumps(v)+'\n')
    return result
before=(len(w.native.calls),w.appends)
with model.patch((os,'fsync',after_sync)),w.installed():a,e=run(w,'ledger')
need(hit and a is None and e is not None,'Postcertificate history drift returned success')
outcome('old_history_change_after_final_certificate_fsync',w,False,a,e,before,{'native':0,'append':1},{'certificate_leaf_may_exist':(m.RUNTIME/'LEDGER_VERIFIED.json').exists(),'receipt_presence_is_not_success':True})
w=setup('exclusive_initial_state_competitor');link=os.link;sentinel={}
def state_race(src,dst,*args,**kwargs):
    place=c.zenodo.state_path(pub.MANIFEST.resolve(),'production')
    if dst==place.name:
        sentinel['raw']=(json.dumps({'manifest':str(pub.MANIFEST.resolve()),'environment':'production','id':999,'marker':[True,1]},indent=1)+'\n').encode();place.write_bytes(sentinel['raw'])
    return link(src,dst,*args,**kwargs)
with model.patch((os,'link',state_race)),w.installed():a,e=run(w,'resume-stage')
need(c.zenodo.state_path(pub.MANIFEST.resolve(),'production').read_bytes()==sentinel['raw'],'Initial state competitor bytes overwritten')
need(json.loads((m.RUNTIME/'CREATE_RETURNED_KNOWN_ID.json').read_bytes())['id']==777,'Known created ID lost')
outcome('exclusive_initial_state_competitor',w,False,a,e,(0,0),{'native':1,'append':0})
for label,change in [
 ('late_afterintent_native_false_totalbytes',lambda l,n,f:n['media_files'].__setitem__('total_bytes',False)),
 ('late_afterintent_native_other_family',lambda l,n,f:n['parent'].__setitem__('id','999'))]:
 w=setup(label,'publish');writer=c.durable;hit=[]
 def drift(path,value):
  writer(path,value)
  if path.name=='WRITE_publish_publish_INTENT.json':hit.append(True);w.native.fault=change
 before=(len(w.native.calls),w.appends)
 with model.patch((c,'durable',drift)),w.installed():a,e=run(w,'publish')
 need(hit and not(m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists(),'Durable native boundary missing')
 outcome(label,w,False,a,e,before,{'native':0,'append':0})
w=setup('postappend_FORMULA_change','ledger');w.formula_after=True;before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'ledger')
need((m.RUNTIME/'LEDGER_APPEND_RESPONSE.json').exists()and not(m.RUNTIME/'LEDGER_VERIFIED.json').exists(),'Formula postwrite failure not retained')
outcome('postappend_FORMULA_change',w,False,a,e,before,{'native':0,'append':1})
w=setup('capacity_exhausted_no_append','ledger');book=w.book;command=w.command;capacity=len(w.rows)
def capped_book():
    value=book();value['sheets'][0]['properties']['gridProperties']['rowCount']=capacity;return value
w.book=capped_book
def capped_command(argv,body=None):
    response=command(argv,body)
    if argv[:5]==['gws','sheets','spreadsheets','values','batchGetByDataFilter']:response['valueRanges'][0]['valueRange']['range']="'Math Puzzles'!A1:AQ"+str(capacity)
    return response
with model.patch((w,'command',capped_command)),w.installed():
    before=(len(w.native.calls),w.appends);a,e=run(w,'ledger')
need(e and 'No allocated row capacity'in e['message']and not(m.RUNTIME/'LEDGER_APPEND_INTENT.json').exists(),'Capacity edge was not exercised')
outcome('capacity_exhausted_no_append',w,False,a,e,before,{'native':0,'append':0})
w=setup('lost_append_response_then_GET_only','ledger');w.append_mode='lost';before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'ledger')
need((m.RUNTIME/'LEDGER_APPEND_INTENT.json').exists()and not(m.RUNTIME/'LEDGER_VERIFIED.json').exists()and w.rows[-1]==pub.draft_row(777),'Lost response did not preserve known append')
outcome('lost_append_response_then_GET_only',w,False,a,e,before,{'native':0,'append':1})
w.append_mode=None;before=(len(w.native.calls),w.appends)
with w.installed():a,e=run(w,'ledger')
need(w.appends==1,'GET reconciliation retried append')
record('lost_append_GET_only_reconciliation',w,e is None,a,e,before,{'native':0,'append':0},
       {'reentry_result_observed_not_presupposed':True,'row_preserved':w.rows[-1]==pub.draft_row(777)})
need(checks[-1]['status']=='PASS','GET-only write delta incorrect')
# Newly authored original-response-only cases; provider later views remain
# correct except the explicitly labeled single late-native-context control.
import inspect
for label,phase,kind,expected in [
 ('original14_create_title','stage','create',1),
 ('original14_publish_size','publish','publish',1),
 ('original14_get_title','publish','get',0),
 ('original14_update_title','stage','update',4),
 ('original14_upload_ack_size','stage','upload',2),
 ('original14_upload_context_get_title','stage','upload_context',2),
 ('original14_get_false_published_shortcut','publish','get_submitted',0),
 ('original14_postpublish_context_DepositError','publish','context',1),
 ('original14_publish_lost_response','publish','lost_publish',1)]:
 w=setup(label,phase);changed=[];before=(len(w.native.calls),w.appends)
 if kind in {'create','publish','update','upload'}:
  original=getattr(w.native,kind)
  def altered(*args):
   value=original(*args)
   if not changed:
    if kind in {'create','update'}:value['title']='CONTRADICTORY ORIGINAL '+kind.upper()+' RESPONSE TITLE'
    elif kind=='publish':value['files'][0]['size']=0
    else:value['size']=0
    changed.append(copy.deepcopy(value))
   return value
  setattr(w.native,kind,altered)
 elif kind in {'get','get_submitted','upload_context'}:
  original=w.native.get
  def altered_get(i):
   value=original(i);caller=inspect.currentframe().f_back.f_code
   selected=caller is(m.EdgeDelegate.mutation.__code__ if kind=='upload_context'else m.EdgeDelegate.get.__code__)
   if selected and not changed:
    if kind=='get_submitted':value['submitted']=True
    else:value['title']='CONTRADICTORY SINGLE ORIGINAL GET TITLE'
    changed.append(copy.deepcopy(value))
   return value
  w.native.get=altered_get
 elif kind=='context':
  original=w.native.native_get
  def altered_context(i,draft=False):
   value=original(i,draft)
   if w.native.published and inspect.currentframe().f_back.f_code is m.EdgeDelegate.native_get.__code__ and not changed:
    value['parent']['id']='999';changed.append(copy.deepcopy(value))
   return value
  w.native.native_get=altered_context
 else:w.native.lost=True
 action='resume-stage'if phase=='stage'else'publish'
 with w.installed():a,e=run(w,action)
 need(e is not None and e['type']=='ConsumedResponseError','Rejected original body reached SDK recovery/success')
 need((m.RUNTIME/'CREATE_RETURNED_KNOWN_ID.json').exists(),'Known created ID lost')
 if kind in {'publish','context'}:
  need((m.RUNTIME/'PUBLISH_RETURNED_SERVICE_FACT.json').exists()and w.native.published,'Known returned publish fact lost')
 if kind=='lost_publish':need(w.native.published and not(m.RUNTIME/'PUBLISH_RETURNED_SERVICE_FACT.json').exists(),'Unknown POST response misrepresented')
 need((not changed)if kind=='lost_publish'else len(changed)==1,'Not exactly one original/context change')
 need(list(m.RUNTIME.glob('CONSUMED_RESPONSE17_HOLD_*')),'Missing durable response HOLD')
 need(not(m.RUNTIME/'ZENODO_PUBLISH_VERIFIED.json').exists()and not(m.RUNTIME/'LEDGER_VERIFIED.json').exists()
      and not list(m.RUNTIME.glob('PRIVATE_PUBLICATION_STATE_*')),'Response rejection certified or saved a private publication summary')
 originals=[json.loads(path.read_bytes())for path in m.PRIVATE.glob('service_original_*.json')]
 need(originals,'Original consumed bodies not physically retained')
 if phase=='stage':need(not(m.RUNTIME/'ZENODO_STAGE_VERIFIED.json').exists(),'Contrary stage response certified')
 (w.place/'ONE_CHANGED_ORIGINAL_OR_CONTEXT.json').write_text(json.dumps(changed,indent=2)+'\n')
 (w.place/'CORRECT_LATER_PROVIDER_VIEWS.json').write_text(json.dumps(w.native.records(),indent=2)+'\n')
 outcome(label,w,False,a,e,before,{'native':expected,'append':0},
         {'one_changed_parsed_original_or_context':len(changed),'original_files_physical':len(originals),
          'original_response_kind':kind,'private_publication_summary_absent':True,'known_id_preserved':777})
 before=(len(w.native.calls),w.appends)
 with w.installed():a,e=run(w,action)
 need(e is not None and not list(m.RUNTIME.glob('PRIVATE_PUBLICATION_STATE_*')),'Held action resumed into success')
 outcome(label+'_no_retry',w,False,a,e,before,{'native':0,'append':0})
archive_completed();need(not model.ATTEMPTS,'Real escape attempt')
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':MS,'bootstrap_sha256':BS,'case_count':len(checks),'parsed_invocations_including_setups':len(CLI_INVOCATIONS),'results':checks,'real_escape_attempts':model.ATTEMPTS,'actual_requests_or_mutations':0,'publication_ready':False,'allocated_bytes':allocated()}
(DEST/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='results'},indent=2))
