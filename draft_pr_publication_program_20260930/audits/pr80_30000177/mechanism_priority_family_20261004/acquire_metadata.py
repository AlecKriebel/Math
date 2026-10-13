from pathlib import Path
from capture import capture
p=Path(__file__).resolve().parent
items=[
 ('pradhan','https://arxiv.org/abs/0705.1917'),
 ('winter','https://arxiv.org/abs/quant-ph/9807019'),
 ('das','https://arxiv.org/abs/1412.6247'),
 ('nonmarkov','https://arxiv.org/abs/2211.13057'),
 ('singh','https://arxiv.org/abs/1502.05130'),
 ('horodecki_piani','https://arxiv.org/abs/quant-ph/0701134'),
 ('huang','https://arxiv.org/abs/quant-ph/9911120'),
 ('allahverdyan','https://arxiv.org/abs/quant-ph/9712034'),
 ('hayashi','https://arxiv.org/abs/2109.12518'),
 ('sen','https://arxiv.org/abs/0909.0580'),
 ('secure','https://arxiv.org/abs/1106.3956'),
 ('shukla','https://arxiv.org/abs/1204.4573'),
 ('agrawal','https://arxiv.org/abs/quant-ph/0610001'),
 ('roy','https://arxiv.org/abs/1707.02449'),
 ('wang_yan','https://cpb.iphy.ac.cn/en/article/doi/10.1088/1674-1056/20/12/120309'),
]
for name,url in items:
 r,out,err=capture('metadata_'+name,['/usr/bin/curl','-L','--fail','--max-time','30',url],cwd=str(p))
 print(name,'childexit',r['exit_code'],'bytes',len(out),flush=True)
 if r['exit_code'] == 0:(p/'private'/(name+'_metadata.html')).write_bytes(out)
