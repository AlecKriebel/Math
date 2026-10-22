from pathlib import Path
OWN=Path(__file__).resolve().parent;p=OWN/'build_log_tests.py';s=p.read_text()
# Extend the template's proof hook only; services remain inert.
s=s.replace("which=cfg.pop('concurrent_change');value=rd(which);value.update(concurrent_marker='PRESERVE NEW WRITER') if type(value) is dict else value[-1].update(concurrent_marker='PRESERVE NEW WRITER');wr(which,value)","which=cfg.pop('concurrent_change')\n    if which in ('project_log','audit_log'):\n     path=(pr if which=='project_log' else audit)/'RESEARCH_LOG.md';path.write_bytes(path.read_bytes()+b'CONCURRENT UNRELATED BYTES\\\\n')\n    else:\n     value=rd(which);value.update(concurrent_marker='PRESERVE NEW WRITER') if type(value) is dict else value[-1].update(concurrent_marker='PRESERVE NEW WRITER');wr(which,value)") if False else s
# The source template is read unchanged, so apply this additional adaptation.
pos=s.index("pos=s.index(' # Independently reconstruct')")
transform='''s=s.replace("which=cfg.pop('concurrent_change');value=rd(which);value.update(concurrent_marker='PRESERVE NEW WRITER') if type(value) is dict else value[-1].update(concurrent_marker='PRESERVE NEW WRITER');wr(which,value)", "which=cfg.pop('concurrent_change')\\n    if which in ('project_log','audit_log'):\\n     path=(pr if which=='project_log' else audit)/'RESEARCH_LOG.md';path.write_bytes(path.read_bytes()+b'CONCURRENT UNRELATED BYTES\\\\n')\\n    else:\\n     value=rd(which);value.update(concurrent_marker='PRESERVE NEW WRITER') if type(value) is dict else value[-1].update(concurrent_marker='PRESERVE NEW WRITER');wr(which,value)")
'''
s=s[:pos]+transform+s[pos:]
pos=s.index(' # Completion record and all four final bytes')
extra=''' # Fresh-input checks also protect both raw log prefixes from stale overwrite.
 for role in ['project_log','audit_log']:
  setup();cfg['concurrent_change']=role
  try:call()
  except RuntimeError as e:need(any(x in str(e) for x in ['fingerprint','changed','nonregular or oversized']),'wrong stale-log guard')
  else:raise RuntimeError('stale log snapshot accepted')
  path=(pr if role=='project_log' else audit)/'RESEARCH_LOG.md';before=path.read_bytes();need(b'CONCURRENT UNRELATED BYTES' in before,'owned log change absent');call();logs_consistent();need(path.read_bytes().startswith(before),'fresh retry lost concurrent unrelated bytes');EVENTS.append({'test':'stale_log_input_reject_then_fresh_prefix_preserved_'+role,'status':'PASS'})
 for role in ['project','audit']:
  for damage in ['missing','symlink','hardlink']:
   setup();path=(pr if role=='project' else audit)/'RESEARCH_LOG.md';unrelated=path.parent/'unrelated-log-anchor';unrelated.write_bytes(b'UNRELATED ANCHOR');path.unlink()
   if damage=='symlink':path.symlink_to(unrelated.name)
   if damage=='hardlink':os.link(unrelated,path)
   before=required_raw()[:2]
   try:call()
   except (RuntimeError,OSError) as e:
    need(unrelated.read_bytes()==b'UNRELATED ANCHOR','unrelated linked target overwritten')
    if damage in ('missing','symlink'):need(required_raw()[:2]==before,'missing/symlink log changed state before validation')
   else:raise RuntimeError('unsafe/missing required log accepted')
   if path.exists() or path.is_symlink():path.unlink()
   path.write_bytes(b'UNRELATED LOG\\\\n');call();logs_consistent();unrelated.unlink();EVENTS.append({'test':'required_log_'+damage+'_reject_and_owned_repair_'+role,'status':'PASS'})
'''
s=s[:pos]+extra+s[pos:]
# required_raw() reads missing files; state/inventory-only snapshots use direct reads.
s=s.replace("before=required_raw()[:2]\n   try:call()", "before=[(pr/name).read_bytes() for name in ['CURRENT_STATE.json','inventory.json']]\n   try:call()")
s=s.replace("need(required_raw()[:2]==before,'missing/symlink", "need([(pr/name).read_bytes() for name in ['CURRENT_STATE.json','inventory.json']]==before,'missing/symlink")
p.write_text(s)
