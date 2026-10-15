import datetime,hashlib,json,os,pathlib,stat

root=pathlib.Path(__file__).resolve().parent
package=pathlib.Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr140_5100023/publication_package_v1')
def sha(body):return hashlib.sha256(body).hexdigest()
def check(ok,message):
    if not ok:raise RuntimeError(message)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
start=json.loads((root/'START_SEALS.json').read_text())
rows=[dict(path=str(p.relative_to(package)),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in sorted(package.rglob('*')) if p.is_file()]
check(rows==start['files'],'candidate changed during review')
end=dict(utc=now,candidate=str(package),files=rows,start_end_complete_bytes_equal=True)
(root/'END_SEALS.json').write_text(json.dumps(end,indent=2)+'\n')
custody=[]
for p in sorted(root.glob('*_child.json')):
    r=json.loads(p.read_text())
    try:os.killpg(r['pid'],0);empty=False
    except ProcessLookupError:empty=True
    check(r['exit_code']==0 and r['reaped'] and r['process_group_empty'] and not r['timed_out'] and empty,'owned child custody '+p.name)
    custody.append(dict(receipt=p.name,pid=r['pid'],reaped=r['reaped'],process_group_absent_at_close=empty))
reproduction=json.loads((root/'fresh_reproduction/REPRODUCTION.json').read_text())
for r in reproduction['runs']:
    try:os.killpg(r['actual_PID'],0);empty=False
    except ProcessLookupError:empty=True
    check(r['child_reaped'] and r['process_group_empty'] and not r['timed_out'] and empty,'reproduction child custody')
    custody.append(dict(case=r['case'],mode=r['mode'],pid=r['actual_PID'],reaped=r['child_reaped'],process_group_absent_at_close=empty))
(root/'OWN_CHILD_CUSTODY.json').write_text(json.dumps(dict(utc=now,all_absent=True,children=custody),indent=2)+'\n')
for name in ['PACKAGE_AUDIT.json','PROVENANCE_AUDIT.json','own_symbolic_result.json','own_rational_attack_result.json','own_highprecision_attack_result.json']:
    check(json.loads((root/name).read_text())['status']=='PASS','evidence failed '+name)
seals={p['path']:dict(bytes=p['bytes'],sha256=p['sha256']) for p in rows}
result=dict(schema='pr140-fresh-whole-publication-package-adversary-r2/v1',utc=now,actual_closer_pid=os.getpid(),
            reviewer='/root/pr140_whole_publication_package_adversary_r2_20261007',status='PASS',review_completion_percent=100,
            mandatory_findings=[],optional_findings=[],candidate=str(package),candidate_start_end_equal=True,
            package_manifest=seals['PACKAGE_MANIFEST.json'],pdf=seals['antipedal_centroids.pdf'],zip=seals['antipedal_centroids_support.zip'],
            pdf_pages=5,all_five_current_pages_visually_inspected_clean=True,zip_members=26,verification_files=17,
            mathematical_scope='Original full-line unweighted antipedal vertex mean; a>b>0; 0<lambda<b²; even least period>=4; primitive stars and either orientation; circle separate.',
            own_math_before_predecessor_verdicts=True,
            independent_rational_cases=223,independent_focal_line_systems=892,independent_rotation_cases=4080,
            independent_highprecision_orbit_phases=45,independent_highprecision_decimal_digits=85,
            independent_max_centroid_residual='7.528685314365615066e-66',independent_symbolic_zero_residuals=5,
            low_precision_diagnostic='Initial absolute centroid threshold1e-7 failed at3.93755e-7 near endpoint; 85-digit direct-tangent repeat closed conditioning concern. Low-precision output is not a centroid pass.',
            portable_reproduction=dict(runner_pid=84381,positive_runs=6,negative_rejections=8,counts_per_mode=[686292,12846,19],python='3.14.6',SymPy='1.14.0'),
            exact_overlap_credit='Ferudun DOI10.5281/zenodo.23092466: theorem/coefficient/pair-and-moment mechanism identical in common scope; algebraically checked.',
            documented_PR_created_at='2026-09-30T11:31:05Z',documented_specific_Zenodo_created_at='2026-10-01T23:58:07.321420Z',
            original_proof_fresh_git_read_sha256='8d13afb77521c9eb8705f494aeba989a5052143e19641534411b8cfec1829754',
            package_R2_readback_sha256='1b8867adc1200a3da2e8d5313c953e8bd41340c20548cf2e1f0700d05cb11d88',
            no_concrete_earlier_complete_lead_identified=True,absolute_priority=False,exclusive_novelty=False,independent_discovery='UNESTABLISHED',
            conventional_human_peer_review=False,third_party_papers_exported=False,all_owned_children_reaped_and_absent=True,
            ENOSPC=False,no_package_Git_provider_PR_tracker_mutation=True,no_individual_contact=True,
            limitations=['Classical Poncelet closure is invoked; no proof-assistant or conventional human verification.',
                         'Finite rational, parity and high-precision cases supplement the analytical all-period proof.',
                         'Least period is an explicit theorem restriction; source does not formally define it; repeated odd even-list extension is false.',
                         'Hyperbolic, endpoint and two-bounce caustics excluded; circle handled without evaluating c^-2 formula.',
                         'Only existing CPython3.14.6/SymPy1.14.0 environment tested; no fresh installation or other-platform claim.',
                         'Bounded literature audit; all historical originals not reread by R2; Veselov and M’Clelland originals remain unread as disclosed.',
                         'DOI/Zenodo web-tool access failed; authenticated cached primary metadata and checksum-matched full paper inspected; arXiv PDF and PR page freshly accessible.',
                         'Specific public record dates do not establish absolute priority, independence, copying or collaboration.'],
            review_supports_parent_clean_publication_gate=True,provider_action_performed=False,operational_publication_authorization_not_decided_here=True,
            parent_overall_goal_complete=False)
(root/'RESULT.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
log=root/'research_log.md'
log.write_text(log.read_text()+'\n'+now+' — Final checkpoint, 100% complete for this bounded R2 assignment. PASS; no mandatory or optional finding. Complete candidate29 bytes equal start; current PDF5/ZIP26/nestedverification17 and intended metadata/files verified. Own rational, symbolic and 85-digit normal/optimized attacks pass. Fresh portable6positive/8negative counts pass. All owned children reaped and groups checked absent at closure. Publication package supports the parent clean-review gate; no provider/Git/tracker/person action or overall-goal completion occurred.\n')
members=[]
for p in sorted(root.rglob('*')):
    if not p.is_file() or p.name=='FINAL_MANIFEST.json':continue
    members.append(dict(relative=str(p.relative_to(root)),bytes=p.stat().st_size,mode=stat.S_IMODE(p.stat().st_mode),sha256=sha(p.read_bytes())))
manifest=dict(schema='pr140-whole-package-r2-closed-manifest/v1',utc=now,actual_closer_pid=os.getpid(),self_excluded='FINAL_MANIFEST.json',status='CLOSED_PASS',
              member_count=len(members),members=members,no_third_party_primary_bodies=True,candidate_manifest_sha256=seals['PACKAGE_MANIFEST.json']['sha256'])
(root/'FINAL_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
for row in members:
    body=(root/row['relative']).read_bytes()
    check(len(body)==row['bytes'] and sha(body)==row['sha256'],'own closed manifest readback')
print(json.dumps(dict(status=result['status'],completion_percent=100,own_manifest_members=len(members),
                     RESULT_sha256=sha((root/'RESULT.json').read_bytes()),REPORT_sha256=sha((root/'REPORT.md').read_bytes()),
                     FINAL_MANIFEST_sha256=sha((root/'FINAL_MANIFEST.json').read_bytes()),candidate_seals=result['package_manifest'],
                     pdf=result['pdf'],zip=result['zip'],all_children_absent=True),indent=2))
