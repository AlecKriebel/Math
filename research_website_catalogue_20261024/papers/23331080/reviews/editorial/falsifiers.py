#!/usr/bin/env python3
"""Private in-memory semantic/visibility/state/native-object fault controls."""
import copy,json,sys
sys.dont_write_bytecode=True
from verify_read_only import E,Q,load,semantic
html=(Q/'page.html').read_text();cfg=load(Q/'promotion.json');snap=load(E/'LITERAL_INPUT_SNAPSHOT.json')
positive=semantic(html,cfg,snap);cases=[]
def h(name,old,new,why):
 if html.count(old)!=1:raise RuntimeError('nonunique copy fault '+name)
 cases.append((name,html.replace(old,new),copy.deepcopy(cfg),copy.deepcopy(snap),why))
def c(name,keys,value,why):
 a=copy.deepcopy(cfg);p=a
 for k in keys[:-1]:p=p[k]
 p[keys[-1]]=value;cases.append((name,html,a,copy.deepcopy(snap),why))
def n(name,keys,value,why):
 a=copy.deepcopy(snap);p=a
 for k in keys[:-1]:p=p[k]
 p[keys[-1]]=value;cases.append((name,html,copy.deepcopy(cfg),a,why))
h('truncated full abstract','The argument uses the exact evolution of a second base derivative along a stationary central fiber and an explicit global positivity certificate.</p>','</p>','full original abstract')
h('all-finite-time quantifier narrowed','every finite t ≥ 0','only t = t*','required scientific')
h('wrong negative witness','At t* = (log 2)/2 this coefficient is −1/96.','At t* = (log 2)/2 this coefficient is +1/96.','exact quantitative')
h('wrong initial polynomial','+ δ p x².','+ δ p x³.','exact quantitative')
h('classical PDE input erased','Classical smooth finite-time parabolic existence and parameter regularity','Computation alone','required scientific')
h('mean normalization omitted','− ∫<sub>ℙ¹</sub> w μ_F','', 'exact quantitative')
h('wrong source defining equation','defining equation (13)','defining equation (12)','required scientific')
h('prior normalized negativity removed','Remark 4.11 already gives normalized anticanonical negativity','Remark 4.11 gives no relevant prior result','required scientific')
h('habilitation overlap invented','its overlap is unknown','its overlap is fully settled','required scientific')
h('hidden article attribute','<article>','<article hidden>','unexpected/hidden')
h('outer template wrapper','<body>','<body><template>','document parent grammar')
h('hidden stylesheet','body { margin: 0;','body { display: none; margin: 0;','approved visible')
h('premature canonical HTML','<head>','<head><link rel="canonical" href="https://aleckriebel.com/research/premature/">','document parent grammar')
h('invented public MIT license','as stated by the Zenodo record.','as stated by the Zenodo record. Original software: MIT.','invented separate MIT')
h('firstness promotion','<footer>','<footer><p>This is the first positivity loss example.</p>','inflated firstness')
h('unrendered secondary hidden style','</style>','</style><style>article{display:none}</style>','approved visible')
h('admissible positive root removed','square-root metric, with weight φ₀/2','an unspecified metric','required scientific')
c('public deployment invented',['state','site_deployed'],True,'all public flags false')
c('AA assigned before adoption',['state','AA'],cfg['proposed']['page_url'],'canonical and native AA null')
c('root editorial adoption fabricated',['state','root_editorial_adoption'],True,'root editorial adoption pending')
c('unsupported follow-up added',['science','follow_up'],{'question':'What else can be extended?'},'exact root-cleared scope')
c('human review invented',['copy','human_peer_review_claimed'],True,'review type not promoted')
c('PDF page count inherited incorrectly',['source','PDF','pages'],5,'actual four-page')
c('embedded PDF invented',['source','ZIP','embedded_PDFs'],1,'actual four-page')
c('native asset order reversed',['source','native_public_asset_order'],['verification_package.zip','positivity_loss.pdf'],'native original file order')
c('separate software license invented',['source','separate_code_license'],'MIT','exact source license')
c('root scientific clearance substituted',['science','root_clearance_SHA256'],'0'*64,'actual root scientific clearance')
c('canonical proposal promoted',['state','canonical_url'],cfg['proposed']['page_url'],'canonical and native AA null')
c('configuration all-time quantifier narrowed',['science','full_counterexample','all_finite_t_geq_zero'],'At t=log(2)/2 only','full all-finite-time')
n('literal custom verdict coerced to PASS',['literal_three_custom_verdicts','scope','literal_custom_verdict'],'PASS','whole literal custom verdict')
n('historical unread flag rewritten',['source_ready_original','target_manuscript_scientifically_read'],True,'whole original native object')
n('one native endpoint omitted',['five_whole_transport_objects_in_native_order'],snap['five_whole_transport_objects_in_native_order'][:-1],'whole original native object')
out=[]
for name,a,b,c,why in cases:
 try:semantic(a,b,c)
 except RuntimeError as ex:
  if why not in str(ex):raise RuntimeError('unexpected rejection '+name+': '+str(ex))
  out.append({'fault':name,'rejection':str(ex)})
 else:raise RuntimeError('fault accepted '+name)
print(json.dumps({'literal_status':'ALL_PRIVATE_EDITORIAL_SEMANTIC_VISIBILITY_STATE_AND_LITERAL_OBJECT_FAULTS_REJECTED','optimized':bool(sys.flags.optimize),'positive_custom_status':positive['literal_status'],'faults':len(out),'records':out,'source_programs_replayed':False,'files_mutated':False,'publication_authority':False},indent=2,sort_keys=True))
