from pathlib import Path
import re
import difflib
import sys

sys.stdout.reconfigure(encoding='utf-8')
patches = []

root = Path(__file__).resolve().parents[2]

def read(name): return (root/name).read_text(encoding='utf-8')
def write(name,text):
    lines = list(difflib.unified_diff(read(name).splitlines(), text.splitlines(), n=3))[2:]
    patches.append('*** Update File: '+name+'\n'+'\n'.join('@@' if line.startswith('@@') else line for line in lines))
def replace(text, old, new):
    assert old in text, old[:100]
    return text.replace(old,new)

def card(id,year,venue,title,authors,summary,details,bib,links,status,featured=False):
    return f'''        <article class="paper-card{' paper-featured' if featured else ''} reveal" id="{id}">
          <div class="paper-year">{year}</div>
          <div>
            <p class="venue">{venue}</p>
            <h2>{title}</h2>
            <p class="paper-meta">{authors}</p>
            <p class="paper-abstract">{summary}</p>
            <div class="paper-details">{''.join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a,b in details)}</div>
            <div class="citation-actions">
              <span>Cite this work</span>
              <a href="citations/{bib}.bib" download>Download BibTeX ↓</a>
              <button class="citation-copy" type="button" data-copy-citation="{id}" data-title="{title.split(':')[0]}">Copy citation</button>
            </div>
            <div class="paper-links">
              <a href="{id}.html">View research page →</a>
              {''.join(f'<a href="{url}" target="_blank" rel="noopener">{label} ↗</a>' for url,label in links)}
            </div>
          </div>
          <span class="paper-type">{status}</span>
        </article>

'''

cyber_title='CyberHull: Deterministic Malicious URL Isolation via Convex Hull'
carbon_title='Carbon loss estimation: a case study of Little Andaman development plan'
cyber = card('cyberhull',2026,'arXiv preprint · Submitted 20 October 2026 · Revised 23 October 2026 · arXiv:2610.27675v2',
    cyber_title,'Avijit Gayen · Aniket Ghosal · Durba Chakraborty · <strong>Sayan Mondal</strong> · Md Abdul Aziz Al Aman · Angshuman Jana',
    'CyberHull builds convex boundaries around legitimate web behaviour using content entropy, semantic features, and hyperlink topology. Deterministic containment tests identify URLs that fall outside the learned regions.',
    [('Problem','Detect evolving malicious URLs with inspectable, computationally lightweight decisions.'),('Approach','QuickHull-based geometric vaults across complementary feature spaces.'),('Reported result','92% accuracy and 0.92 F1 in the v2 preprint’s benchmark; broader traffic validation remains future work.')],
    'gayen2026cyberhull',[('https://arxiv.org/abs/2610.27675','arXiv'),('https://arxiv.org/pdf/2610.27675v2','PDF (v2)'),('https://doi.org/10.48550/arXiv.2610.27675','DOI'),('https://github.com/AniketGhosal/CyberHull-URL-Detection','Code &amp; data')],'arXiv preprint',True)
carbon = card('carbon-loss',2022,'IJARCCE · Volume 11, issue 3 · March 2022 · pp. 196–203 · DOI 10.17148/IJARCCE.2022.11336',
    carbon_title,'Sujit Raha · Avijit Chakraborty · Purbita Chatterjee · Tanmoy Chakraborty · <strong>Sayan Mondal</strong>',
    'A geospatial estimation study connecting Bhuvan land-cover data with forest carbon inventories to assess carbon stock potentially affected by the Little Andaman development scenario described in 2022.',
    [('Data','Resourcesat-2 LISS-III land-cover data from 2015–16 and the India State of Forest Report 2019.'),('Method','QGIS processing and forest-class area estimates across five carbon pools.'),('Interpretation','A historical stock-loss estimate; the detailed page explains the source’s unit and study-area inconsistencies.')],
    'raha2022carbon',[('https://doi.org/10.17148/IJARCCE.2022.11336','DOI'),('https://ijarcce.com/papers/carbon-loss-estimation-a-case-study-of-little-andaman-development-plan/','Publisher'),('https://ijarcce.com/wp-content/uploads/2022/04/IJARCCE.2022.11336.pdf','Full text')],'Journal article')

s=read('research/index.html')
s=replace(s,'Research publications by Sayan Mondal in cybersecurity, trustworthy machine learning, NLP, and intelligent systems.','Research publications by Sayan Mondal in cybersecurity, trustworthy machine learning, geospatial carbon estimation, NLP, and intelligent systems.')
s=replace(s,'Research spanning signed-network security, causal cyber defense,\n          trustworthy machine learning, natural language processing, transport\n          safety, and intelligent public infrastructure.','Research spanning geometric and signed-network security, causal cyber\n          defense, semi-supervised learning, geospatial carbon estimation,\n          natural language processing, and intelligent infrastructure.')
s=replace(s,'<a class="button" href="sinmuli.html">SiNMULI project</a','<a class="button" href="cyberhull.html">CyberHull project</a\n          ><a class="button button-outline" href="astria.html">ASTriA project</a\n          ><a class="button button-outline" href="carbon-loss.html">Carbon-loss study</a\n          ><a class="button button-outline" href="sinmuli.html">SiNMULI project</a')
start=s.index('        <div><strong>7</strong><span>publications</span></div>')
end=s.index('      </section>',start)
s=s[:start]+'''        <div><strong>9</strong><span>archived works</span></div>
        <div><strong>10</strong><span>Scholar citations</span></div>
        <div><strong>1</strong><span>Scholar h-index</span></div>
        <p>
          Scholar snapshot: <time datetime="2026-10-27">27 October 2026</time>.
          Seven indexed articles; i10-index: 0. This archive also includes two
          earlier reports/preprints. <a href="https://scholar.google.com/citations?user=dwLadG8AAAAJ&amp;hl=en" target="_blank" rel="noopener">View live Scholar metrics ↗</a>
        </p>
'''+s[end:]
s=replace(s,'><span>Intelligent infrastructure</span>','><span>Intelligent infrastructure</span><span>Geometric threat detection</span\n            ><span>Geospatial carbon estimation</span>')
s=replace(s,'        <article class="paper-card paper-featured reveal">',cyber+'        <article class="paper-card reveal" id="sinmuli">')
pos=s.index('        <article class="paper-card reveal">\n          <div class="paper-year">2020</div>')
s=s[:pos]+carbon+s[pos:]
start=s.index('<article class="paper-card reveal" id="astria">')
pos=s.index('            <div class="paper-links">',start)+len('            <div class="paper-links">')
s=s[:pos]+'\n              <a href="astria.html">View research page →</a>'+s[pos:]
s=replace(s,'Every publication above now includes a verified BibTeX download and','Every publication above includes a BibTeX download and')
write('research/index.html',s)

s=read('index.html')
s=replace(s,'I investigate how semi-supervised learning, signed networks,\n              causal reasoning, trustworthy machine learning, language\n              technologies, and intelligent infrastructure can make digital and\n              physical systems safer, more explainable, and more adaptive.','I investigate geometric and signed-network threat detection,\n              semi-supervised learning, causal cyber defense, and trustworthy\n              machine learning, alongside work in language technologies,\n              geospatial carbon estimation, and intelligent infrastructure.')
s=replace(s,'<h3>SiNMULI</h3>\n              <p>\n                Signed-network reasoning for interpretable malicious URL\n                identification.\n              </p>\n              <a href="research/sinmuli.html">View research page →</a>',
    '<h3>CyberHull</h3>\n              <p>\n                Deterministic malicious URL detection using convex boundaries\n                across content, semantic, and hyperlink features.\n              </p>\n              <a href="research/cyberhull.html">View research page →</a>')
s=replace(s,'Latest · arXiv 2026','Latest · arXiv preprint · Oct 2026')
s=replace(s,'href="research/#astria">View publication →','href="research/astria.html">View research page →')
s=replace(s,'<div><strong>7</strong><span>Publications</span></div>\n              <div><strong>6</strong><span>Research themes</span></div>\n              <div><strong>6</strong><span>DOI records</span></div>',
    '<div><strong>9</strong><span>Archived works</span></div>\n              <div><strong>10</strong><span>Scholar citations</span></div>\n              <div><strong>1</strong><span>h-index</span></div>\n              <p class="research-snapshot">Scholar metrics · <time datetime="2026-10-27">27 Oct 2026</time></p>')
marker='        </div>\n        <div class="projects-more reveal">'
new='''          <article class="project-preview-card reveal">
            <div><span class="project-count">06</span><p>Geometric security</p></div>
            <h3>CyberHull URL isolation</h3>
            <span>Convex hulls and interpretable threat boundaries</span>
            <a href="research/cyberhull.html">View research page →</a>
          </article>
          <article class="project-preview-card reveal">
            <div><span class="project-count">07</span><p>Environmental computing</p></div>
            <h3>Little Andaman carbon study</h3>
            <span>Land-cover analysis and forest carbon estimation</span>
            <a href="research/carbon-loss.html">View research page →</a>
          </article>
'''
s=replace(s,marker,new+marker)
write('index.html',s)

def case(slug,kicker,title,description,problem,stack,method,limits,steps,outcome):
    return f'''          <article class="case-study reveal" id="{slug}">
            <div class="case-study-head"><p class="case-type">{kicker}</p><h2>{title}</h2><p>{description}</p></div>
            <div class="case-grid"><div><strong>Research problem</strong><p>{problem}</p></div>
              <div><strong>Technology stack</strong><div class="tech-list">{''.join(f'<span>{v}</span>' for v in stack)}</div></div></div>
            <div class="case-grid"><div><strong>Method</strong><p>{method}</p></div>
              <div><strong>Scope and limitations</strong><p>{limits}</p></div></div>
            <div class="system-diagram" aria-label="{title} workflow">{''.join(f'<span>{v}</span>' for v in steps)}</div>
            <div class="case-footer"><p><strong>Outcome:</strong> {outcome}</p><a href="../research/{slug}.html">View research page →</a></div>
          </article>

'''
s=read('pages/projects.html')
s=replace(s,'><a class="button button-outline" href="#sinmuli">SiNMULI</a','><a class="button button-outline" href="#cyberhull">CyberHull</a\n          ><a class="button button-outline" href="#carbon-loss">Carbon-loss study</a\n          ><a class="button button-outline" href="#sinmuli">SiNMULI</a')
s=replace(s,'<strong>6</strong><span>case studies','<strong>8</strong><span>case studies')
s=replace(s,'<strong>4</strong><span>research cases','<strong>6</strong><span>research cases')
s=replace(s,'Latest cybersecurity research · arXiv 2026','Signed-network research · arXiv 2026')
newcase=case('cyberhull','Latest research · arXiv preprint · October 2026',cyber_title,
    'Explores inspectable URL classification through geometric boundaries learned from legitimate web features.',
    'Changing phishing infrastructure can evade static lists. The study investigates a CPU-based detection approach with explicit decision boundaries.',
    ['Python','SciPy Spatial','NumPy','Pandas','Computational geometry'],
    'Extract content, semantic, and hyperlink features; rank feature pairs; construct QuickHull vaults; classify new URLs using containment tests.',
    'Boundary quality depends on clean baseline data and complete feature extraction. Legitimate website changes require recalibration, and broader traffic validation remains future work.',
    ['Web features','Feature-pair selection','Convex hull vaults','Containment checks','URL decision'],
    'v2 preprint reports 92% accuracy and 0.92 F1 in its benchmark. Public paper and author-linked implementation are available.')
s=replace(s,'          <article class="case-study reveal" id="sinmuli">',newcase+'          <article class="case-study reveal" id="sinmuli">')
start=s.index('<article class="case-study reveal" id="astria">')
pos=s.index('              <a\n                href="https://doi.org/',start)
s=s[:pos]+'              <a href="../research/astria.html">View research page →</a>\n'+s[pos:]
newcase=case('carbon-loss','Environmental computing · IJARCCE 2022',carbon_title,
    'Combines satellite land-cover observations and forest inventory data to estimate carbon stock affected by a historical development scenario.',
    'Estimate the carbon implications of forest conversion in the Little Andaman proposal examined in the 2022 paper.',
    ['QGIS','Bhuvan','Remote sensing','Land-cover analysis','Carbon accounting'],
    'Map four forest classes from sampled land-cover areas, scale regional carbon densities to the study area, and aggregate five carbon pools.',
    'The source contains inconsistent area and unit labels. The detailed page records these limits; the result is not a measurement of present-day emissions.',
    ['Land-cover data','Forest classes','Carbon inventories','Area scaling','Stock estimate'],
    'journal article, volume 11(3), pp. 196–203, with an open-access paper and DOI.')
pos=s.index('        </div>\n      </section>',s.index('id="entrourl"'))
s=s[:pos]+newcase+s[pos:]
write('pages/projects.html',s)

s=read('pages/resume.html')
new=f'''        <article>
          <time>2026</time>
          <div><h3><a href="../research/cyberhull.html">{cyber_title}</a></h3>
            <p>arXiv:2610.27675 · Preprint · Revised 23 October 2026</p></div>
        </article>
'''
s=replace(s,'        <h2>Selected Publications</h2>','        <h2>Selected Publications</h2>\n'+new)
s=replace(s,'              ASTriA: Adaptive Semi-Supervised Tri-Learning Approach for\n              Scalable Malicious URL Detection',
    '              <a href="../research/astria.html">ASTriA: Adaptive Semi-Supervised Tri-Learning Approach for\n              Scalable Malicious URL Detection</a>')
pos=s.index('        <article>\n          <time>2020</time>',s.index('class="publications"'))
s=s[:pos]+f'''        <article>
          <time>2022</time>
          <div><h3><a href="../research/carbon-loss.html">{carbon_title}</a></h3>
            <p>IJARCCE 11(3), 196–203 · DOI: 10.17148/IJARCCE.2022.11336</p></div>
        </article>
'''+s[pos:]
s=replace(s,'Seven publications in total. Full list:','Nine works in the research archive. Full list:')
write('pages/resume.html',s)
s=read('research/sinmuli.html').replace('Latest research · 2026','Signed-network research · 2026')
write('research/sinmuli.html',s)
print('*** Begin Patch\n'+'\n'.join(patches)+'\n*** End Patch')
