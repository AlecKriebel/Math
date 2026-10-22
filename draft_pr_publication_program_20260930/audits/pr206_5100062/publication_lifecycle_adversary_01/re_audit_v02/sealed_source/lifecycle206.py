"""PR206 ready90 -> safe merge95 -> incomplete actual factual98 -> actual100.
Root configures modules explicitly. No project loading or service/ref CLI.
"""
S=R=N=None


def configure(support,ready,native):
    global S,R,N
    if S is not None:raise RuntimeError('Fresh lifecycle module required')
    S,R,N=support,ready,native
    for phase in ('merge','factual','completion'):
        S.register(phase,{'inputs':lambda argument,p=phase:inputs(p,argument),'overlay':lambda h,parent,stamp,data,name,p=phase:overlay(p,h,parent,stamp,data,name),'parents':lambda parent,p=phase:parents(p,parent),'original':lambda h,data,after,candidate,p=phase:original(p,h,data,after,candidate),'queue_before':lambda data,p=phase:S.queue_rows()[1] if p=='merge' else S.published_row(data['DOI']),'queue_after':lambda data:S.published_row(data['DOI']),'facts':lambda data,actual,p=phase:facts(p,data,actual),'mutable':lambda data:set(S.VIEWS)|{S.NATIVE+n for n in N.current_names()}|{S.Q}})


def inputs(phase,ack_pin):
    S.need(phase in ('merge','factual','completion'),'Lifecycle phase');S.metadata_ack(ack_pin);g,p,t,context=S.operations();state=S.actual(S.PHASES[phase][2]);a=state['receipt']
    S.need(a['facts']['completed'] is False and all(a['facts'][key]==value for key,value in S.BASE_COUNTS.items()),'Actual incomplete predecessor counters')
    if phase=='merge':S.need(a['case_percent']==90 and a['facts']['publication_ready'] is True and a['facts']['actual_publication_verified'] is False,'Actual ready90 prerequisite')
    else:S.need(a['facts']['actual_merge_accepted'] is True and a['facts']['actual_publication_verified'] is True and a['facts']['actual_tracker_row_verified'] is True,'Actual published/tracked merged predecessor')
    if phase=='completion':S.need(a['case_percent']==98 and a['facts']['actual_factual_accepted'] is True and a['facts']['completed'] is False,'Actual factual98 is incomplete, not a completion receipt')
    return {'gate_pin':context['gate_pin'],'gate':g,'package':g['package'],'package_seal':g['package_seal'],'whole_package_reviews_completed':len(g['whole_package_review_events']),'metadata_ack':ack_pin,'publication_receipt_pin':S.pin(S.frozen('ROOT_PUBLICATION_RECEIPT.json')),'tracker_receipt_pin':S.pin(S.frozen('ROOT_TRACKER_RECEIPT.json')),'DOI':p['doi'],'record_id':p['id'],'tracker_range':t['range'],'predecessor':{'phase':S.PHASES[phase][2],'directory':state['directory'],'acceptance_pin':S.pin(S.read(state['directory']+'ACCEPTANCE.json')),'pointer_pin':S.pin(S.read(S.POINTER[S.PHASES[phase][2]]))}}


def parents(phase,parent):
    S.need(phase in ('merge','factual','completion') and S.re.fullmatch('[0-9a-f]{40}',parent) is not None,'Exact phase parents')
    return [parent,S.HEAD] if phase=='merge' else [parent]


def facts(phase,data,actual=False):
    S.need(phase in ('merge','factual','completion') and type(actual) is bool,'Phase/actual selector')
    result=R.facts(data,actual);merged=phase!='merge' or actual;factual=phase=='completion' or (phase=='factual' and actual)
    result.update(case_percent=S.PHASES[phase][1],actual_publication_verified=True,actual_tracker_row_verified=True,actual_original_PR_merged=merged,actual_merge_accepted=merged,actual_factual_accepted=factual,completed=phase=='completion' and actual,DOI=data['DOI'],record_id=data['record_id'],tracker_range=data['tracker_range'])
    result.update(S.counts(phase,actual));return result


def original(phase,h,data,after=False,candidate=None):
    ack=S.metadata_ack(data['metadata_ack']);p=S.api(h,'pulls/206')
    S.need(p['head']['sha']==S.HEAD and p['head']['ref']=='dot/math-5100062' and p['base']['ref']==ack['expected_base_ref'] and p['title']==ack['expected_title'] and S.pin((p['body'] or '').encode())==ack['expected_body_pin'],'Exact original HEAD and Root-acknowledged actual final metadata')
    if phase=='merge' and not after:S.need(p['state']=='open' and p['draft'] is False and p['merged'] is False,'Open nondraft original before95')
    else:
        expected=candidate if phase=='merge' else S.actual('merge')['receipt']['checkpoint_commit']
        S.need(p['state']=='closed' and p['draft'] is False and p['merged'] is True and p['merge_commit_sha']==expected,'Actual original-HEAD-safe merge readback')
    return p


def native_facts(phase,stamp,data):
    g=data['gate'];f={'schema':'pr206-native-actual-facts-v1','original_head':S.HEAD,'UTC':stamp,'package_seal':S.pp(g['package']+'/'+g['package_seal_file'],g['package_seal']),'publication_ready_gate':S.pp(S.PUBLICATION_GATE,data['gate_pin']),'publication_receipt':S.pp('ROOT_PUBLICATION_RECEIPT.json',data['publication_receipt_pin']),'tracker_receipt':S.pp('ROOT_TRACKER_RECEIPT.json',data['tracker_receipt_pin'])}
    for kind in (() if phase=='merge' else ('merge',) if phase=='factual' else ('merge','factual')):
        state=S.actual(kind);f[kind+'_receipt']=S.pp(state['directory'][len(S.CASE):]+'ACCEPTANCE.json',S.pin(S.read(state['directory']+'ACCEPTANCE.json')))
    return f


def overlay(phase,h,parent,stamp,data,name):
    stage={'merge':'published_pending_merge','factual':'actual_merge_accepted','completion':'actual_factual_accepted_completion_pending'}[phase]
    out=N.construct(stage,native_facts(phase,stamp,data));out.update(S.views_overlay(h,parent,stamp,phase,data))
    for filename in ('ROOT_PUBLICATION_RECEIPT.json','ROOT_TRACKER_RECEIPT.json',data['metadata_ack']['path'],S.SOURCE_ADOPTION):out[S.CASE+filename]=S.frozen(filename)
    prior=data['predecessor'];out[S.POINTER[prior['phase']]]=S.read(S.POINTER[prior['phase']])
    for filename in ('ACCEPTANCE.json','LOCAL_GLOBAL_FIVE_SYNC.json','ROOT_PRE_MOVE_VERIFICATION.json','FOREIGN_QUEUE_RECONCILIATION.json'):out[prior['directory']+filename]=S.read(prior['directory']+filename)
    if phase=='merge':
        pt=S.api(h,'git/commits/'+parent)['tree']['sha'];S.need(S.native_leaves(h,pt,S.NATIVE)=={},'Owned original native directory must be absent before95')
        out[S.Q]=S.replace_queue(S.body(h,S.Q,parent),data['DOI'])
    return out


def bind(phase,name,metadata_ack_pin):return S.bind(phase,name,metadata_ack_pin)
def prepare(phase,name):return S.prepare(phase,name)
def verify(phase,name):return S.verify(phase,name)
def accept(phase,name):return S.accept(phase,name)
def sync(phase,name):return S.sync(phase,name)
def pointer(phase,name):return S.pointer(phase,name)
