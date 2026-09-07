from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
original = s

qmatch = re.search(r'(\s*const questions = \{.*?\n\s*\};)', s, re.S)
assert qmatch, 'questions object not found'
questions_before = qmatch.group(1)

meta_replacements = {
    '<title>EIR-TDAH-A – Escala Integrada de Rastreio para TDAH</title>': '<title>Atenção, organização e impulsividade no dia a dia</title>',
    '<meta name="description" content="EIR-TDAH-A: Escala Integrada de Rastreio clínica para TDAH baseada em DSM-5-TR e CID-11.">': '<meta name="description" content="Rastreio clínico sobre atenção, organização, impulsividade e impacto funcional no dia a dia.">',
    '<meta property="og:site_name" content="EIR-TDAH-A">': '<meta property="og:site_name" content="Plataforma Terapêutica Richelmy Murta">',
    '<meta property="og:title" content="EIR-TDAH-A – Escala Integrada de Rastreio para TDAH">': '<meta property="og:title" content="Atenção, organização e impulsividade no dia a dia">',
    '<meta property="og:description" content="EIR-TDAH-A: Escala Integrada de Rastreio clínica para TDAH baseada em DSM-5-TR e CID-11.">': '<meta property="og:description" content="Rastreio clínico sobre atenção, organização, impulsividade e impacto funcional no dia a dia.">',
    '<meta property="og:image:alt" content="Banner EIR-TDAH-A – Escala Integrada de Rastreio para TDAH">': '<meta property="og:image:alt" content="Imagem de apoio ao rastreio clínico">',
    '<meta name="twitter:title" content="EIR-TDAH-A – Escala Integrada de Rastreio para TDAH">': '<meta name="twitter:title" content="Atenção, organização e impulsividade no dia a dia">',
    '<meta name="twitter:description" content="EIR-TDAH-A: Escala Integrada de Rastreio clínica para TDAH baseada em DSM-5-TR e CID-11.">': '<meta name="twitter:description" content="Rastreio clínico sobre atenção, organização, impulsividade e impacto funcional no dia a dia.">',
    '<section class="hero" aria-label="Banner EIR-TDAH-A">': '<section class="hero" aria-label="Imagem de apoio ao rastreio">',
    '<img src="https://i.pinimg.com/736x/57/56/e0/5756e082e6578f470c72d23a323ed61e.jpg" alt="Banner EIR-TDAH-A – Escala Integrada de Rastreio para TDAH">': '<img src="https://i.pinimg.com/736x/57/56/e0/5756e082e6578f470c72d23a323ed61e.jpg" alt="Imagem de apoio ao rastreio de atenção e organização">',
    '<p>Este formulário de autorrelato avalia sintomas de TDAH em adultos, baseado em critérios do DSM-5-TR e CID-11. Leia cada afirmação e selecione a resposta que melhor descreve sua experiência nos últimos 6 meses.</p>': '<p>Leia cada afirmação e selecione a resposta que melhor descreve sua experiência real nos últimos 6 meses. Não há respostas certas ou erradas; o conjunto será analisado clinicamente pelo psicólogo responsável.</p>',
    '<section class="block" id="block1"><h3>1. Desatenção Atual</h3><div id="q1"></div></section>': '<section class="block" id="block1"><h3>Bloco 1</h3><div id="q1"></div></section>',
    '<section class="block" id="block2"><h3>2. Hiperatividade e Impulsividade</h3><div id="q2"></div></section>': '<section class="block" id="block2"><h3>Bloco 2</h3><div id="q2"></div></section>',
    '<section class="block" id="block3"><h3>3. Desregulação Emocional</h3><div id="q3"></div></section>': '<section class="block" id="block3"><h3>Bloco 3</h3><div id="q3"></div></section>',
    '<section class="block" id="block4"><h3>4. Funções Executivas</h3><div id="q4"></div></section>': '<section class="block" id="block4"><h3>Bloco 4</h3><div id="q4"></div></section>',
    '<section class="block" id="block5"><h3>5. Impacto Funcional</h3><div id="q5"></div></section>': '<section class="block" id="block5"><h3>Bloco 5</h3><div id="q5"></div></section>',
    '<section class="block" id="block6"><h3>6. Retroatividade Infantil</h3><div id="q6"></div></section>': '<section class="block" id="block6"><h3>Bloco 6</h3><div id="q6"></div></section>',
    '<section class="block" id="block7"><h3>7. Diagnóstico Diferencial</h3><div id="q7"></div></section>': '<section class="block" id="block7"><h3>Bloco 7</h3><div id="q7"></div></section>',
    '<section class="block" id="block8"><h3>8. Autorregulação e Comportamentos Gerais</h3><div id="q8"></div></section>': '<section class="block" id="block8"><h3>Bloco 8</h3><div id="q8"></div></section>',
    '<div class="actions"><button type="button" id="submit">Corrigir</button></div>': '<div class="actions"><button type="button" id="submit">Concluir rastreio</button></div>',
}
for old, new in meta_replacements.items():
    if old in s:
        s = s.replace(old, new, 1)

# Remove result-only CSS.
s = re.sub(r'\n\s*/\* Cards \*/.*?\nfooter\s*\{', '\nfooter{', s, count=1, flags=re.S)

# Remove patient results section.
s, n = re.subn(r'\n\s*<!-- Resultados -->\s*<section id="results".*?</section>', '', s, count=1, flags=re.S)
assert n == 1, 'patient result section not found exactly once'

# Replace everything after the preserved questions object with render-only runtime.
qmatch_now = re.search(r'(\s*const questions = \{.*?\n\s*\};)', s, re.S)
assert qmatch_now, 'questions object lost before runtime replacement'
start = qmatch_now.end()
script_end = s.find('\n  </script>', start)
assert script_end > start, 'module script end not found'
render_runtime = r'''

    const renderQuestions = () => {
      Object.entries(questions).forEach(([key, arr]) => {
        const container = document.getElementById(key);
        container.innerHTML = arr.map((q,i) => `
          <div class="question">
            <p>${i+1}. ${q}</p>
            <div class="options">
              ${[0,1,2,3,4].map(v => `<label><input required name="${key}_${i}" type="radio" value="${v}">${v}</label>`).join('')}
            </div>
          </div>`).join('');
      });
    };

    document.addEventListener('DOMContentLoaded', () => {
      renderQuestions();
      document.getElementById('darkModeToggle').addEventListener('click', () =>
        document.body.classList.toggle('dark')
      );
    });'''
s = s[:start] + render_runtime + s[script_end:]

qmatch_after = re.search(r'(\s*const questions = \{.*?\n\s*\};)', s, re.S)
assert qmatch_after and qmatch_after.group(1) == questions_before, 'clinical question bank changed'

for token in (
    'const maxScores',
    'const severity',
    'DSM_INATT',
    'DSM_HIIMP',
    'function dsmCount',
    'Regra DSM-like',
    'Triagem compatível com critérios DSM',
    'Risco dimensional baixo',
    'Indicação dimensional grave',
    'id="results"',
    'thermometer-fill',
    "getElementById('splash')",
):
    assert token not in s, f'legacy scorer/result token remains: {token}'

assert 'Concluir rastreio' in s
assert 'últimos 6 meses' in s
assert 'screening-uniformity-v1.js' in s
assert s != original
p.write_text(s, encoding='utf-8')
