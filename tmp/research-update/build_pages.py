from pathlib import Path
import html
import json
import re

root = Path(__file__).resolve().parents[2]
template = (root / 'research/sinmuli.html').read_text(encoding='utf-8')
header = template[template.index('    <header'):template.index('    <main')]
footer = template[template.index('    <footer'):]

def external(url, label, cls=''):
    return f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener"' + (f' class="{cls}"' if cls else '') + f'>{label} ↗</a>'

def panel(id, label, title, content):
    return f'''<article class="research-panel reveal" id="{id}">
          <p class="case-type">{label}</p><h2>{title}</h2>
          {content}
        </article>'''

def flow(steps):
    return '<ol class="research-flow">'+''.join(f'<li>{s}</li>' for s in steps)+'</ol>'

def two(a,b):
    return f'<div class="research-two-col"><div>{a}</div><div>{b}</div></div>'

def make_page(slug, name, title, description, kicker, authors, date, record, status, doi, paper, bib, panels, extra_links=(), schema_extra=None):
    article = {'@context':'https://schema.org','@type':'ScholarlyArticle','headline':title,
        'datePublished':date,'identifier':doi,'url':paper,
        'author':[{'@type':'Person','name':a} for a in authors],
        'sameAs':[f'https://doi.org/{doi}']}
    if schema_extra: article.update(schema_extra)
    jump = ''.join(f'<a href="#{id}">{label}</a>' for id,label,_ in panels)
    body = '\n        '.join(p for _,_,p in panels)
    links = ''.join(external(u,l,'button button-outline') for u,l in extra_links)
    page = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <meta name="description" content="{html.escape(description, quote=True)}" />
    <meta name="theme-color" content="#08111f" />
    <link rel="icon" href="../img/branding/favicon.svg?v=5" type="image/svg+xml" />
    <title>{name} — Research by Sayan Mondal</title>
    <link rel="canonical" href="https://sayanmondal2098.github.io/research/{slug}.html" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&amp;family=Manrope:wght@600;700;800&amp;display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="../css/site.css" />
    <link rel="stylesheet" href="../css/research.css" />
    <link rel="stylesheet" href="../css/projects.css" />
    <link rel="stylesheet" href="../css/research-projects.css" />
    <script defer src="../js/site.js"></script>
    <script defer src="../js/citations.js"></script>
    <script type="application/ld+json">{json.dumps(article, ensure_ascii=False, indent=2)}</script>
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
{header}    <main id="main">
      <section class="page-hero wrap reveal">
        <a class="text-link" href="./">← All publications</a>
        <p class="kicker">{kicker}</p>
        <h1>{title}</h1>
        <p>{description}</p>
        <div class="profile-actions">
          {external(paper, 'Read the paper', 'button')}
          <a class="button button-outline" href="citations/{bib}.bib" download>Download BibTeX</a>
          <button class="button button-outline citation-copy" type="button" data-copy-citation="{slug}" data-title="{name}">Copy citation</button>
          {links}
        </div>
      </section>
      <section class="research-project-summary wrap reveal" aria-label="Publication details">
        <div><strong>Record</strong><span>{record}</span></div>
        <div><strong>Published</strong><span>{date}</span></div>
        <div><strong>Status</strong><span>{status}</span></div>
        <p>Authors: {', '.join(authors)}.</p>
      </section>
      <nav class="research-jump wrap" aria-label="On this page">{jump}</nav>
      <section class="section wrap research-project-body">
        {body}
        <article class="research-panel reveal">
          <p class="case-type">Continue exploring</p>
          <h2>Related research</h2>
          <div class="paper-links">
            <a href="cyberhull.html">CyberHull</a><a href="sinmuli.html">SiNMULI</a>
            <a href="astria.html">ASTriA</a><a href="entrourl.html">EntroURL-Bench</a>
            <a href="carbon-loss.html">Carbon-loss estimation</a><a href="./">Full publication archive →</a>
          </div>
        </article>
        <div id="citation-status" class="citation-toast" role="status" aria-live="polite" aria-atomic="true"></div>
      </section>
    </main>
{footer}'''
    (root/f'research/{slug}.html').write_text(page, encoding='utf-8')

cyber_source = 'https://arxiv.org/html/2610.27675v2'
cyber_repo = 'https://github.com/AniketGhosal/CyberHull-URL-Detection'
cyber_panels = [
 ('overview','Overview',panel('overview','Research question','Can geometric boundaries make URL decisions inspectable?',two(
    '<strong>The problem</strong><p>Phishing infrastructure changes faster than static blacklists. CyberHull studies whether explicit boundaries around observed legitimate web behaviour can identify suspicious URLs without a deep neural classifier.</p>',
    '<strong>The contribution</strong><p>The framework projects content, language, and link features into several geometric spaces called vaults. Each vault encloses legitimate examples in a convex hull. A request is accepted by the model only when its projected features satisfy every selected boundary.</p>'))),
 ('method','Method',panel('method','Methodology','From web features to a geometric decision.',
    flow(['Extract web features','Rank feature pairs','Construct convex hulls','Project an unseen URL','Check each boundary','Return a URL label'])+two(
    '<strong>Offline construction</strong><ul><li>Extract 91 features from the enriched benchmark.</li><li>Rank candidate pairs using the difference between class means divided by the sum of class standard deviations.</li><li>The study evaluates 4,095 pairs and retains 46 vaults; its explanation highlights three complementary feature domains.</li><li>Use QuickHull to enclose the legitimate training points in each selected space.</li></ul>',
    '<strong>Inference</strong><p>Project an incoming URL into the same feature spaces and apply containment tests. Falling outside a selected hull produces a malicious classification. This is a deterministic decision rule over measured features; being inside a hull is not proof that a website is safe.</p>'))),
 ('features','Feature spaces',panel('features','Feature design','Three complementary views of a website.',
    '<div class="research-table-wrap" role="region" aria-label="CyberHull feature spaces" tabindex="0"><table class="research-table"><caption>Feature domains described in the preprint</caption><thead><tr><th scope="col">Domain</th><th scope="col">Signals</th><th scope="col">Purpose</th></tr></thead><tbody><tr><th scope="row">Structural entropy</th><td>Shannon entropy and internal-page entropy</td><td>Describe content variability and repetition.</td></tr><tr><th scope="row">Semantic content</th><td>TF-IDF distributions of informational and urgency-related tokens</td><td>Represent language and page intent.</td></tr><tr><th scope="row">Hyperlink topology</th><td>Internal link density and outbound link ratios</td><td>Describe site connectivity.</td></tr></tbody></table></div>')),
 ('evaluation','Evaluation',panel('evaluation','Reported evaluation','92% accuracy in the paper’s benchmark.',
    '<p>The revised preprint describes an 80/20 stratified split and reports averaged results from stratified five-fold cross-validation. Table 3 compares methods on the same feature representation. These are author-reported experimental results, not independently reproduced measurements.</p>'+
    '<div class="research-table-wrap" role="region" aria-label="CyberHull benchmark results" tabindex="0"><table class="research-table"><caption>Reported results · arXiv v2, Table 3</caption><thead><tr><th scope="col">Method</th><th scope="col">Accuracy</th><th scope="col">Precision</th><th scope="col">Recall</th><th scope="col">F1</th><th scope="col">False-positive rate</th></tr></thead><tbody>'+''.join(f'<tr{chr(32)+"class="+chr(34)+"result-highlight"+chr(34) if row[0]=="CyberHull" else ""}><th scope="row">{row[0]}</th>'+''.join(f'<td>{v}</td>' for v in row[1:])+'</tr>' for row in [('PCA','32%','0.28','0.31','0.29','0.41'),('SVM','81%','0.79','0.76','0.77','0.14'),('Random Forest','88%','0.86','0.84','0.85','0.09'),('XGBoost','90%','0.89','0.87','0.88','0.07'),('CyberHull','92%','0.93','0.91','0.92','0.03')])+'</tbody></table></div>'+
    '<p class="research-source">Source: '+external(cyber_source+'#S4.T3','CyberHull v2, Table 3')+'. The separate count of 1,314 intercepted attacks out of 1,470 in Table 2 is not the same statistic as the cross-validation accuracy above.</p>'+
    '<p>The implementation uses Python 3.12, NumPy, Pandas, and SciPy Spatial. The paper describes CPU experiments on an Intel Core i7 with 16 GB RAM, with scikit-learn and XGBoost baselines.</p>')),
 ('limits','Scope & limitations',panel('limits','Scope and future work','Boundary quality depends on the data behind it.',two(
    '<strong>Current boundaries</strong><ul><li>Contaminated legitimate training data can distort the learned hulls.</li><li>Strict feature extraction removes unusable samples and limits the diversity represented in the evaluation.</li><li>Changes in legitimate websites can produce false positives unless boundaries are refreshed.</li><li>Results from this benchmark should not be directly ranked against SiNMULI or ASTriA results from different evaluations.</li></ul>',
    '<strong>Future directions</strong><p>The authors propose adaptive perimeter updates, broader validation on changing traffic, and federated feedback between edge nodes. These are research directions rather than established deployment capabilities.</p>'))),
 ('resources','Paper & code',panel('resources','Open artifacts','Read, inspect, and cite the work.',
    '<p>First submitted 20 October 2026; revised 23 October 2026 (v2). This page follows v2. Status: arXiv preprint.</p><div class="paper-links">'+external('https://arxiv.org/abs/2610.27675','arXiv record')+external(cyber_source,'Full text (v2)')+external('https://arxiv.org/pdf/2610.27675v2','PDF (v2)')+external(cyber_repo,'Author-linked code & data')+external('https://doi.org/10.48550/arXiv.2610.27675','DOI')+'</div><p class="research-source">Summary based on the authors’ CC BY 4.0 preprint. Source checked 27 October 2026.</p>'))
]
make_page('cyberhull','CyberHull','CyberHull: Deterministic Malicious URL Isolation via Convex Hull',
    'Geometric threat detection using explicit convex boundaries over content entropy, semantic features, and hyperlink structure.',
    'Latest research · arXiv preprint · October 2026',
    ['Avijit Gayen','Aniket Ghosal','Durba Chakraborty','Sayan Mondal','Md Abdul Aziz Al Aman','Angshuman Jana'],
    '2026-10-20','arXiv:2610.27675v2','Preprint · revised 23 Oct 2026','10.48550/arXiv.2610.27675',
    'https://arxiv.org/abs/2610.27675','gayen2026cyberhull',cyber_panels,[(cyber_repo,'Code & data')],
    {'dateModified':'2026-10-23','isAccessibleForFree':True,'license':'https://creativecommons.org/licenses/by/4.0/'})

astria_doi='https://doi.org/10.1109/TENSYMP68909.2026.11704039'
astria_panels=[
 ('overview','Overview',panel('overview','Research question','Learn from URLs when labels are scarce.',two(
    '<strong>Motivation</strong><p>Maintaining a large, current collection of labeled malicious URLs is expensive. Blacklists struggle with newly generated addresses, while purely unsupervised detection can flag harmless URLs without reliable supervision.</p>',
    '<strong>Research contribution</strong><p>ASTriA investigates adaptive semi-supervised tri-learning: multiple learners help assign reliable pseudo-labels to unlabeled samples, expanding a smaller labeled training set over successive iterations.</p>'))),
 ('method','Method',panel('method','Methodology','Iteratively expand the labeled training set.',
    flow(['Labeled seed URLs','Unlabeled URL pool','Lexical & host features','Collaborative pseudo-labels','Expand training set','Repeat & classify'])+two(
    '<strong>Inputs and representation</strong><p>A limited labeled collection anchors learning, while a larger unlabeled pool supplies additional examples. Lightweight lexical and host-based features keep the representation practical for URL classification.</p>',
    '<strong>Learning workflow</strong><p>The published abstract describes iterative high-confidence pseudo-labeling with interpretable classifiers including Random Forest and k-Nearest Neighbors. The tri-learning design uses collaboration among learners to reduce dependence on manually supplied labels.</p>'))),
 ('scope','Evidence & scope',panel('scope','Evidence and interpretation','A documented method with a clear publication record.',two(
    '<strong>Verified evidence</strong><p>The IEEE publication record confirms the title, five authors, TENSYMP venue, and pages 1–5. The public abstract supports the labeled/unlabeled workflow, pseudo-labeling approach, feature families, and named classifiers.</p><p>Numerical accuracy, dataset sizes, learner configurations, and confidence thresholds are not reproduced here because those details were not available in the accessible abstract.</p>',
    '<strong>Evaluation considerations</strong><p>When applying this method, inspect how pseudo-label errors propagate, how confidence is calibrated, and how performance changes as URL distributions evolve. These are practical considerations for interpreting semi-supervised systems, not additional experimental claims about ASTriA.</p>'))),
 ('context','Research context',panel('context','Connected research','Different routes to trustworthy URL detection.',
    '<p>ASTriA focuses on learning from partially labeled data. <a href="sinmuli.html">SiNMULI</a> studies signed hyperlink relationships; <a href="cyberhull.html">CyberHull</a> studies geometric feature boundaries; <a href="entrourl.html">EntroURL-Bench</a> supplies a separate line of work on richer, reproducible URL datasets. These projects explore complementary questions; this comparison does not imply that they share an evaluation protocol.</p>')),
 ('resources','Publication & citation',panel('resources','Publication record','IEEE Region 10 Symposium, 2026.',
    '<p><strong>Authors:</strong> Avijit Gayen, Sayan Mondal, Bhanu Bariar, Khokan Mondal, and Angshuman Jana.</p><p><strong>Venue:</strong> 2026 IEEE Region 10 Symposium (TENSYMP), Penang, Malaysia, 29 June–1 July 2026, pp. 1–5. The conference program lists the presentation on 30 June.</p><div class="paper-links">'+external(astria_doi,'DOI')+external('https://ieeexplore.ieee.org/document/11704039/','IEEE Xplore')+external('https://ieeemy.org/tensymp2026/day-2-30-6-2026-tuesday/','Conference program')+external('https://scholar.google.com/citations?view_op=view_citation&hl=en&user=dwLadG8AAAAJ&citation_for_view=dwLadG8AAAAJ:Y0pCki6q_DkC','Scholar abstract')+'</div><p class="research-source">Metadata checked against IEEE’s Crossref deposit and the official conference program on 27 October 2026.</p>'))
]
make_page('astria','ASTriA','ASTriA: Adaptive Semi-Supervised Tri-Learning Approach for Scalable Malicious URL Detection',
    'A lightweight semi-supervised approach that expands limited labeled URL data through collaborative, high-confidence pseudo-labeling.',
    'Cybersecurity & machine learning · IEEE TENSYMP 2026',
    ['Avijit Gayen','Sayan Mondal','Bhanu Bariar','Khokan Mondal','Angshuman Jana'],
    '2026-06','IEEE TENSYMP · pp. 1–5','Conference paper','10.1109/TENSYMP68909.2026.11704039',astria_doi,
    'gayen2026astria',astria_panels,schema_extra={'pagination':'1–5','publisher':{'@type':'Organization','name':'IEEE'}})

carbon_paper='https://ijarcce.com/papers/carbon-loss-estimation-a-case-study-of-little-andaman-development-plan/'
carbon_pdf='https://ijarcce.com/wp-content/uploads/2022/04/IJARCCE.2022.11336.pdf'
carbon_panels=[
 ('overview','Overview',panel('overview','Research question','Estimate the carbon implications of land-use change.',two(
    '<strong>Study context</strong><p>The paper examines the Little Andaman development proposal discussed at the time of publication in 2022. It asks how forest clearing within the proposed development area could affect stored carbon.</p>',
    '<strong>Contribution</strong><p>The study combines satellite-derived land-cover areas with published forest carbon inventories in QGIS. It provides a secondary-data estimation workflow to support environmental assessment, rather than a direct field measurement of emissions.</p>'))),
 ('data','Data sources',panel('data','Data and tools','Connect land cover with forest carbon inventories.',
    '<div class="research-table-wrap" role="region" aria-label="Carbon study data sources" tabindex="0"><table class="research-table"><caption>Inputs documented in the 2022 paper</caption><thead><tr><th scope="col">Input</th><th scope="col">Reference period</th><th scope="col">Use</th></tr></thead><tbody><tr><th scope="row">Bhuvan land use / land cover</th><td>2015–16</td><td>Resourcesat-2 LISS-III thematic data at 1:50,000 scale.</td></tr><tr><th scope="row">India State of Forest Report</th><td>2019</td><td>Forest-type and density-based carbon inventories for the Andaman and Nicobar Islands.</td></tr><tr><th scope="row">QGIS</th><td>Study workflow</td><td>Spatial processing and estimation of forest-class areas.</td></tr></tbody></table></div>')),
 ('method','Method',panel('method','Methodology','Translate mapped forest areas into carbon-pool estimates.',
    flow(['Select areas of interest','Extract land-cover classes','Estimate class areas','Match carbon inventories','Scale each carbon pool','Aggregate stock estimates'])+two(
    '<strong>Land-cover grouping</strong><p>Four sampled areas inform estimates for evergreen/semi-evergreen forest, deciduous forest, swamp/mangrove, and plantation. The method maps their proportions onto the study area.</p>',
    '<strong>Carbon accounting</strong><p>For each forest class, the regional inventory is scaled by the estimated class area. The five pools are above-ground biomass, below-ground biomass, dead wood, litter, and soil organic carbon; their contributions are then summed.</p>'))),
 ('findings','Findings & interpretation',panel('findings','Reported findings','Soil and evergreen forests dominate the estimate.',
    '<p>The paper’s tables identify soil organic carbon as the largest pool and evergreen/semi-evergreen forest as the largest forest-class contribution. This highlights why an assessment of forest conversion needs to consider below-ground carbon as well as standing vegetation.</p>'+
    '<p>The results section reports a total of 2,996.286 tonnes. That number is reproduced as a reported value, with an important qualification: the source inventory uses thousands of tonnes, while later tables use tonnes, and study-area references alternate between 210 and 240 km². Those units and area assumptions need reconciliation before the total is reused for planning or comparison.</p>'+
    '<p class="research-source">Source: '+external(carbon_pdf,'Published paper, Tables 1–3 and Results section')+'. The qualification above follows from the labels and area values printed in the paper.</p>')),
 ('limits','Scope & future work',panel('limits','Scope and limitations','A historical estimation study.',two(
    '<strong>Interpretation</strong><p>The work uses historical imagery and regional inventory averages. It estimates carbon stock potentially affected under a development scenario; it does not measure when or how much of that carbon would reach the atmosphere, and it does not establish the current status of the development plan.</p>',
    '<strong>Further work</strong><p>The authors suggest improving the estimate with alternative satellite datasets and machine-learning tools in GIS. Updated imagery, explicit unit checks, a consistent study boundary, and field validation would strengthen reuse of the workflow.</p>'))),
 ('resources','Publication & citation',panel('resources','Publication record','IJARCCE · March 2022.',
    '<p><strong>Authors:</strong> Sujit Raha, Avijit Chakraborty, Purbita Chatterjee, Tanmoy Chakraborty, and Sayan Mondal.</p><p>International Journal of Advanced Research in Computer and Communication Engineering, volume 11, issue 3, pp. 196–203. DOI: 10.17148/IJARCCE.2022.11336.</p><div class="paper-links">'+external(carbon_paper,'Publisher record')+external(carbon_pdf,'Open-access PDF')+external('https://doi.org/10.17148/IJARCCE.2022.11336','DOI')+'</div><p class="research-source">Summary based on the CC BY 4.0 paper, verified against the publisher and the author’s Scholar profile on 27 October 2026.</p>'))
]
make_page('carbon-loss','Carbon-loss estimation','Carbon loss estimation: a case study of Little Andaman development plan',
    'A geospatial study combining Bhuvan land-cover data and forest carbon inventories to estimate carbon stock affected by a development scenario.',
    'Environmental computing · Journal article · March 2022',
    ['Sujit Raha','Avijit Chakraborty','Purbita Chatterjee','Tanmoy Chakraborty','Sayan Mondal'],
    '2022-03','IJARCCE 11(3) · pp. 196–203','Journal article','10.17148/IJARCCE.2022.11336',carbon_paper,
    'raha2022carbon',carbon_panels,[(carbon_pdf,'Open PDF')],{'isAccessibleForFree':True,'license':'https://creativecommons.org/licenses/by/4.0/','pagination':'196–203'})
print('Created CyberHull, ASTriA, and carbon-loss research pages.')
