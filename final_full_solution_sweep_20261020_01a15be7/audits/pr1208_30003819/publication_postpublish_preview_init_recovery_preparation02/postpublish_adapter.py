"""Inherits core07 gates/Journal/append and recovery01 cold capture semantics."""
ALLOWED=['reconcile','verify-public','ledger']
RECORD=23578142
CONCEPT=23578141
def need(ok,message):
 if not ok:raise RuntimeError(message)
def provider_class(base):
 class PostPublishedProvider(base):
  def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self._ledger_delegate_allowed=False
  def client(self):
   client=super().client()
   if not getattr(client,'_postpublish02_get_only',False):
    original=client.request
    def get_only(method,url,*args,**kwargs):
     need(method=='GET','Postpublish02 blocks every Zenodo mutation, including a second publish');return original(method,url,*args,**kwargs)
    client.request=get_only;client._postpublish02_get_only=True
   return client
  def append_row(self,row):
   need(self._ledger_delegate_allowed,'Ledger delegate requires inherited once/edge guards');return super().append_row(row)
  def git_write(self,*a,**kw):raise RuntimeError('Postpublish02 forbids Git effects')
  def ready(self,*a,**kw):raise RuntimeError('Postpublish02 forbids readiness effects')
  def install_state_absent(self,*a,**kw):raise RuntimeError('Postpublish02 forbids shared cursor effects')
  def bind_state(self,*a,**kw):raise RuntimeError('Postpublish02 forbids cursor binding')
  def private_state_receipt(self,*a,**kw):raise RuntimeError('Postpublish02 forbids publication summary cursor writes')
  def tool_context(self,*a,**kw):raise RuntimeError('Postpublish02 forbids stage/publish tool context')
 return PostPublishedProvider

def engine_class(life,checker,binding):
 Base=life.Engine
 class PostPublishedEngine(Base):
  def __init__(self,*args,**kwargs):
   super().__init__(*args,**kwargs)
   need(self.action in ALLOWED and type(self.identifier) is int and self.identifier==RECORD,'Only fixed sameCASE postpublish actions permitted')
   if self.action=='ledger':need(not self.j.exists('LEDGER_ROW_INTENT'),'Prior ledger intent: reconcile GET-only; never append again')
   self.recover_original_publish()
  def recheck(self):
   super().recheck();checker(self)
   need(self.action in ALLOWED,'Postpublish02 action forbidden')
   need(self.identifier is None or type(self.identifier) is int and self.identifier==RECORD,'Postpublish02 target switched')
  def start(self,key,request):
   need(key=='LEDGER' and self.action=='ledger','No new publication/Git phase under postpublish02');return super().start(key,request)
  def mutate(self,key,request,call,before):
   need(self.action=='ledger' and key=='LEDGER_ROW','Only the first inherited ledger append is effect-capable')
   need(not self.j.exists('LEDGER_ROW_INTENT'),'Ledger request already attempted')
   def delegate():
    need(not self.p._ledger_delegate_allowed,'Nested ledger delegation forbidden');self.p._ledger_delegate_allowed=True
    try:return call()
    finally:self.p._ledger_delegate_allowed=False
   return super().mutate(key,request,delegate,before)
  def recover_original_publish(self):
   self.recheck();need(self.j.exists('ZENODO_PUBLISH_RESPONSE'),'Original successful publish POST absent')
   need(not self.j.exists('ZENODO_PUBLISH_UNKNOWN'),'Original publication outcome has unresolved uncertainty')
   phase=self.j.read('PUBLISH_PHASE_INTENT');intent=self.j.read('ZENODO_PUBLISH_INTENT');original=self.j.read('ZENODO_PUBLISH_RESPONSE')
   need(phase['operation']=='PUBLISH' and phase['action']=='publish' and life.typed_equal(phase['request'],{'id':RECORD}) and intent['operation']=='ZENODO_PUBLISH' and intent['action']=='publish' and life.typed_equal(intent['request'],{'id':RECORD}),'Original publish request/phase identity differs')
   need(life.pin(self.j.expected['ZENODO_PUBLISH_RESPONSE'])==binding['original_publish_response'] and life.pin(self.j.expected['ZENODO_PUBLISH_INTENT'])==binding['original_publish_intent'] and life.pin(self.j.expected['PUBLISH_PHASE_INTENT'])==binding['original_publish_phase_intent'],'Original POST/intent bytes differ from authority')
   self.require_merged();g=self.gate(merged=True,row=life.draft_row(RECORD))
   _,post=self.observe(True,{life.PDF,life.ZIP},legacy_response=original['response']);self.family(g,post)
   _,current=self.observe(True,{life.PDF,life.ZIP});self.family(g,current)
   for key in ['record','concept','owner','doi','native_metadata','files']:
    need(life.typed_equal(post[key],current[key]),'Original successful POST/fresh GET infrastructure differs')
   need(current['record']==RECORD and current['concept']==CONCEPT,'Original published target family differs')
   proof={'id':RECORD,'concept':CONCEPT,'doi':current['doi'],'state':'published','evidence':'Original fsynced publish POST validated against fresh native/finalized and independent legacy GET; no publication request repeated','original_publish_response':binding['original_publish_response'],'additive_authorization':binding['additive_authorization']}
   self.receipt('POSTPUBLISH02_ORIGINAL_POST_VERIFIED',proof)
   self.receipt('PUBLISH_VERIFIED',{'id':RECORD,'doi':current['doi'],'state':'published'})
 return PostPublishedEngine
