# Trigger lifecycle patch v2
from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""      setTimeout(() => {
        document.getElementById('splash').classList.add('hidden');
        document.getElementById('mainContent').classList.add('show');
      }, 2000);"""
new="""      setTimeout(() => {
        document.getElementById('splash')?.classList.add('hidden');
        document.getElementById('mainContent')?.classList.add('show');
      }, 2000);"""
if old in s:
    s=s.replace(old,new,1)
elif new not in s:
    raise SystemExit('EXPECTED_LIFECYCLE_BLOCK_NOT_FOUND')
if 'Tenho dificuldade em manter o foco em conversas longas.' not in s:
    raise SystemExit('QUESTION_SENTINEL_MISSING')
p.write_text(s,encoding='utf-8')
