"""PR206 custody10 -> ready90. Root configures support; no project loader/CLI."""
S=None


def configure(support):
    global S
    if S is not None:raise RuntimeError('Fresh ready module required')
    S=support
    S.register('ready',{'inputs':inputs,'overlay':overlay,'parents':lambda parent:[parent],'original':original,'queue_before':lambda data:S.queue_rows()[1],'queue_after':lambda data:S.queue_rows()[1],'facts':facts,'mutable':lambda data:set(S.VIEWS)})


def inputs(gate_pin):
    g,files=S.gate(gate_pin);S.baseline_custody()
    return {'gate_pin':S.bytepin(gate_pin),'gate':g,'files':files,'package':g['package'],'package_seal':g['package_seal'],'whole_package_reviews_completed':len(g['whole_package_review_events'])}


def original(h,data,after=False,candidate=None):
    raw=S.frozen('ORIGINAL_PR_METADATA.json',S.ORIGINAL_METADATA);old=S.decode(raw);p=S.api(h,'pulls/206')
    S.need(p['head']['sha']==S.HEAD and p['head']['ref']=='dot/math-5100062' and p['base']['ref']=='main' and p['state']=='open' and p['draft'] is True and p['merged'] is False,'Original open/draft HEAD at actual90')
    for key in ('title','body','created_at','updated_at','commits','changed_files'):S.need(p[key]==old[key],'Original pre-update metadata unchanged '+key)
    return p


def facts(data,actual=False):
    return {'case_percent':90,'Root_publication_gate_pin':data['gate_pin'],'package':data['package'],'package_seal':data['package_seal'],'publication_ready':True,'NEW_whole_package_reviews_completed':data['whole_package_reviews_completed'],'whole_package_review_loop_complete':True,'mathematical_clearance':True,'source_contract_clearance':True,'priority_clearance':True,'priority_clearance_scope':'qualified_attributed_note_only','bounded_priority_audit_complete':True,'qualified_attributed_note_editorially_cleared':True,'priority_novelty_clearance':False,'historical_firstness_independence_established':False,'actual_publication_verified':False,'actual_tracker_row_verified':False,'actual_original_PR_merged':False,'actual_merge_accepted':False,'actual_factual_accepted':False,'completed':False,'DOI':None,'record_id':None,'tracker_range':None,**S.BASE_COUNTS}


def overlay(h,parent,stamp,data,name):
    out={S.CASE+path:S.frozen(path,p) for path,p in data['files'].items()};out.update(S.views_overlay(h,parent,stamp,'ready',data))
    S.need(S.Q not in out and not any(path.startswith(S.ALL_NATIVE) for path in out),'Ready90 no QUEUE/native attempts')
    return out


def bind(name,gate_pin):return S.bind('ready',name,gate_pin)
def prepare(name):return S.prepare('ready',name)
def verify(name):return S.verify('ready',name)
def accept(name):return S.accept('ready',name)
def sync(name):return S.sync('ready',name)
def pointer(name):return S.pointer('ready',name)
