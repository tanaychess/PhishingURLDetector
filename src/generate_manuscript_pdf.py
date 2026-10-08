"""
High-Fidelity IEEE Two-Column Conference Manuscript PDF Generator.
Generates paper/final/Phishing_Website_XAI.pdf adhering strictly to IEEE conference formatting.
Author: Tanay Samson Pathare (Department of Computer Science, Bhonsala Military College)

Uses system TrueType fonts (LiberationSerif / DejaVuSerif) to ensure 100% vector Unicode precision
with ZERO missing glyphs, black rectangles, or encoding artifacts.
Suppresses running headers and footers on Page 1; removes all 'Page N' footers across all pages per IEEE standards.
Exact 4-page balanced IEEE conference layout containing all comprehensive text, equations, tables, figures, and 21 verified references.
"""

import os
import sys
import shutil
import zipfile
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, FrameBreak,
    Paragraph, Spacer, Image, Table, TableStyle, HRFlowable, NextPageTemplate
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def register_unicode_fonts():
    """Register system TrueType fonts for clean Unicode glyph rendering without black spot artifacts."""
    font_paths = {
        "Liberation-Regular": "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "Liberation-Bold": "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "Liberation-Italic": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        "Liberation-BoldItalic": "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf",
    }
    fallback_paths = {
        "Liberation-Regular": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "Liberation-Bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "Liberation-Italic": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
        "Liberation-BoldItalic": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-BoldItalic.ttf",
    }
    for name, path in font_paths.items():
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(name, path))
        elif os.path.exists(fallback_paths[name]):
            pdfmetrics.registerFont(TTFont(name, fallback_paths[name]))

def create_ieee_manuscript_pdf(output_pdf="paper/final/PhishingURLDetetctor.pdf"):
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    register_unicode_fonts()
    
    # Page setup: A4 dimensions in points
    page_w, page_h = A4
    margin_x = 0.5 * 72   # 36 pt (0.5 in)
    margin_y = 0.40 * 72  # 28.8 pt
    
    col_gap = 14  # 14 pt gap between columns
    col_w = (page_w - (2 * margin_x) - col_gap) / 2  # ~254.5 pt per column
    usable_h = page_h - (2 * margin_y)
    
    # Define two frames for standard 2-column layout (Pages 2+)
    frame_left = Frame(
        margin_x, margin_y, col_w, usable_h,
        id="col1", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
    )
    frame_right = Frame(
        margin_x + col_w + col_gap, margin_y, col_w, usable_h,
        id="col2", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
    )
    
    # Title / Header Frame (Page 1 full-width span)
    title_h = 115
    frame_title = Frame(
        margin_x, page_h - margin_y - title_h, page_w - (2 * margin_x), title_h,
        id="header_frame", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
    )
    frame_left_p1 = Frame(
        margin_x, margin_y, col_w, usable_h - title_h,
        id="col1_p1", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
    )
    frame_right_p1 = Frame(
        margin_x + col_w + col_gap, margin_y, col_w, usable_h - title_h,
        id="col2_p1", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
    )
    
    # Page 1: Clean canvas with NO footers and NO running header
    def on_first_page(canvas_obj, doc_obj):
        pass

    # Pages 2+: Subtle standard running header (NO page number footers per IEEE standards)
    def on_later_pages(canvas_obj, doc_obj):
        canvas_obj.saveState()
        canvas_obj.setFont("Liberation-Italic", 7.5)
        canvas_obj.drawString(margin_x, page_h - margin_y + 8, "Pathare: Explainable Machine Learning Framework for Phishing Website Detection")
        canvas_obj.restoreState()

    doc = BaseDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=margin_x,
        rightMargin=margin_x,
        topMargin=margin_y,
        bottomMargin=margin_y
    )
    
    first_page_template = PageTemplate(
        id="FirstPage",
        frames=[frame_title, frame_left_p1, frame_right_p1],
        onPage=on_first_page
    )
    two_col_template = PageTemplate(
        id="TwoCol",
        frames=[frame_left, frame_right],
        onPage=on_later_pages
    )
    
    doc.addPageTemplates([first_page_template, two_col_template])
    
    # Typography Styles - Standard IEEE Dimensions
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        "IEEE_Title",
        parent=styles["Normal"],
        fontName="Liberation-Bold",
        fontSize=14.5,
        leading=18.0,
        alignment=TA_CENTER,
        spaceAfter=4
    )
    
    author_style = ParagraphStyle(
        "IEEE_Authors",
        parent=styles["Normal"],
        fontName="Liberation-Regular",
        fontSize=8.6,
        leading=11.2,
        alignment=TA_CENTER,
        spaceAfter=4
    )
    
    abstract_text = ParagraphStyle(
        "IEEE_AbsText",
        parent=styles["Normal"],
        fontName="Liberation-Italic",
        fontSize=8.0, leading=10.0,
        alignment=TA_JUSTIFY,
        spaceAfter=3
    )
    
    keywords_style = ParagraphStyle(
        "IEEE_Keywords",
        parent=styles["Normal"],
        fontName="Liberation-Regular",
        fontSize=8.0, leading=10.0,
        alignment=TA_JUSTIFY,
        spaceAfter=3
    )
    
    sec_heading = ParagraphStyle(
        "IEEE_SecHead",
        parent=styles["Normal"],
        fontName="Liberation-Bold",
        fontSize=8.4,
        leading=10.6,
        alignment=TA_CENTER,
        spaceBefore=4.0,
        spaceAfter=1.5,
        keepWithNext=True
    )
    
    subsec_heading = ParagraphStyle(
        "IEEE_SubSecHead",
        parent=styles["Normal"],
        fontName="Liberation-Italic",
        fontSize=7.9,
        leading=10.0,
        alignment=TA_LEFT,
        spaceBefore=3.0,
        spaceAfter=1.0,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        "IEEE_Body",
        parent=styles["Normal"],
        fontName="Liberation-Regular",
        fontSize=8.0, leading=10.0,
        alignment=TA_JUSTIFY,
        firstLineIndent=8,
        spaceAfter=1.2
    )
    
    bullet_style = ParagraphStyle(
        "IEEE_Bullet",
        parent=styles["Normal"],
        fontName="Liberation-Regular",
        fontSize=8.0, leading=10.0,
        alignment=TA_JUSTIFY,
        leftIndent=10,
        firstLineIndent=-10,
        spaceAfter=0.8
    )
    
    caption_style = ParagraphStyle(
        "IEEE_Caption",
        parent=styles["Normal"],
        fontName="Liberation-Regular",
        fontSize=6.8,
        leading=8.4,
        alignment=TA_CENTER,
        spaceBefore=1.5,
        spaceAfter=1.8
    )
    
    equation_style = ParagraphStyle(
        "IEEE_Eq",
        parent=styles["Normal"],
        fontName="Liberation-Italic",
        fontSize=7.4,
        leading=9.2,
        alignment=TA_CENTER,
        spaceBefore=1.5,
        spaceAfter=1.5
    )
    
    ref_style = ParagraphStyle(
        "IEEE_Ref",
        parent=styles["Normal"],
        fontName="Liberation-Regular",
        fontSize=6.1,
        leading=7.2,
        alignment=TA_JUSTIFY,
        leftIndent=10,
        firstLineIndent=-10,
        spaceAfter=0.6
    )
    
    # Dedicated Table Styles with clean single-line font sizing
    th_style = ParagraphStyle(
        "IEEE_TH",
        parent=styles["Normal"],
        fontName="Liberation-Bold",
        fontSize=4.9,
        leading=5.9,
        alignment=TA_CENTER
    )
    tc_style = ParagraphStyle(
        "IEEE_TC",
        parent=styles["Normal"],
        fontName="Liberation-Regular",
        fontSize=4.8,
        leading=5.8,
        alignment=TA_CENTER
    )
    tc_left_style = ParagraphStyle(
        "IEEE_TC_Left",
        parent=styles["Normal"],
        fontName="Liberation-Regular",
        fontSize=4.8,
        leading=5.8,
        alignment=TA_LEFT
    )
    tc_bold_style = ParagraphStyle(
        "IEEE_TC_Bold",
        parent=styles["Normal"],
        fontName="Liberation-Bold",
        fontSize=4.8,
        leading=5.8,
        alignment=TA_CENTER
    )
    tc_left_bold_style = ParagraphStyle(
        "IEEE_TC_LeftBold",
        parent=styles["Normal"],
        fontName="Liberation-Bold",
        fontSize=4.8,
        leading=5.8,
        alignment=TA_LEFT
    )

    story = []
    
    # ----------------------------------------------------
    # HEADER FRAME: Title, Single Author
    # ----------------------------------------------------
    story.append(NextPageTemplate("TwoCol"))
    title_text = "An Explainable Machine Learning Framework for Phishing Website Detection Using URL and Network Features"
    story.append(Paragraph(title_text, title_style))
    
    author_text = """
    <b>Tanay Samson Pathare</b><br/>
    <i>Department of Computer Science, Bhonsala Military College</i><br/>
    <i>Nashik, Maharashtra, India</i><br/>
    Email: tanaypathare1@gmail.com
    """
    story.append(Paragraph(author_text, author_style))
    story.append(FrameBreak())  # Move to Left Column of Page 1
    
    # ----------------------------------------------------
    # ABSTRACT & KEYWORDS
    # ----------------------------------------------------
    abs_p = "<b><i>Abstract</i>— Phishing websites represent a pervasive cyber threat engineered to harvest credentials through deceptive web infrastructure. While machine learning enables proactive detection beyond signature blacklists, operational deployment is hindered by model opacity and the network latency of external domain inspection. This paper presents an explainable machine learning framework for phishing website detection using 111 structured URL lexical, path, query, and network resolver features on a benchmark corpus of 58,645 URLs. Evaluating five classification architectures across 11,729 held-out test instances with 5-fold cross-validation on the training set, XGBoost achieves superior discrimination, yielding a 5-seed mean of 94.74% ± 0.08% accuracy and 94.98% ± 0.08% F1-score (seed 42: 94.82% accuracy, 95.05% F1-score; seeds vary model tree subsampling on a fixed split), statistically outperforming Random Forest (p &lt; 0.001, McNemar's test). Tree-based Shapley Additive Explanations (TreeSHAP) applied strictly to training data eliminate selection leakage, demonstrating high ranking stability under model retraining (&rho;<sub>s</sub> = 0.973 ± 0.010 across 98 features, Kendall's &tau; = 0.795 within top-20, 95.0% top-20 set overlap; &rho;<sub>s</sub> = 0.9991 under explanation subsampling) and identifying directory length, domain registration age, and delimiters as primary discriminators. Feature reduction demonstrates that a compact top-20 subset—the smallest subset within about 0.2 pp of full training CV F1—matches full-model test efficacy while reducing model-only inference latency (excluding resolver lookups) to 1.67 ms per 10<sup>3</sup> queries. Furthermore, an uncertainty-gated cascade resolves 64.3% of URLs in-memory with 97.78% Tier-1 accuracy using zero-network lexical parsing, supporting a tiered design for high-throughput perimeter triage that eliminates nearly two-thirds of external network calls despite a modest increase in error rates (end-to-end FNR: 4.98% vs. 4.78%; FPR: 5.93% vs. 5.62%).</b>"
    story.append(Paragraph(abs_p, abstract_text))
    
    kw_p = "<b><i>Keywords</i>— Phishing Website Detection, Explainable Artificial Intelligence (XAI), Machine Learning, URL Features, TreeSHAP, Feature Selection, Cybersecurity.</b>"
    story.append(Paragraph(kw_p, keywords_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.gray, spaceAfter=3))
    
    # Section I: Introduction
    story.append(Paragraph("I. INTRODUCTION", sec_heading))
    story.append(Paragraph(
        "Phishing represents a pervasive threat in modern cyberspace. Attackers engineer deceptive URLs and spoofed web portals to impersonate authentic organizations, harvesting credentials and financial assets [1], [2]. Threat telemetry from the Anti-Phishing Working Group (APWG) [1] documents millions of active phishing attacks annually, while the Verizon DBIR [2] identifies credential theft as a primary breach vector across confirmed corporate breaches.",
        body_style
    ))
    story.append(Paragraph(
        "Conventional defenses rely heavily on centralized signature databases and community blacklists (e.g., Google Safe Browsing, PhishTank). While blacklists provide high precision on cataloged domains, they exhibit significant discovery delays, often requiring hours to verify zero-hour domains [3]-[6], during which zero-day attacks achieve maximum impact.",
        body_style
    ))
    story.append(Paragraph(
        "To overcome blacklist latency, machine learning (ML) has emerged as a proactive alternative, classifying domain, path, and structural indicators dynamically [7], [8]. However, operational adoption in Security Operations Centers (SOCs) faces two critical bottlenecks: (i) <i>Model Opacity</i>, where opaque tree ensembles fail to provide interpretable feature attributions for containment decisions; and (ii) <i>Page Crawling Latency</i>, where full DOM rendering introduces substantial latency and risks drive-by malware [9], [10].",
        body_style
    ))
    story.append(Paragraph(
        "To address these challenges, this paper presents an empirical benchmark and explainable ML framework for phishing detection using 111 structured URL lexical, path, file, query, and resolver metrics on 58,645 URLs [11]. We evaluate five paradigms: Logistic Regression, Decision Trees, Random Forests, Linear SVM, and XGBoost [12] across 11,729 held-out test samples with 5-fold cross-validation. To ensure transparency, we apply Tree-based Shapley Additive Explanations (TreeSHAP) [13], [14] strictly on training data, eliminating selection leakage.",
        body_style
    ))
    story.append(Paragraph("The primary contributions of this work are:", body_style))
    story.append(Paragraph("• <b>Multi-Model Benchmark & Statistical Validation:</b> We evaluate five supervised ML architectures across 11,729 test instances with 5-fold CV on training data (N=46,916), verifying that XGBoost's lead (5-seed mean: 94.74% ± 0.08% acc, 94.98% ± 0.08% F1; seed 42: 94.82% accuracy, 95.05% F1) over Random Forest is statistically significant via McNemar's test (p &lt; 0.001).", bullet_style))
    story.append(Paragraph("• <b>Train-Only Attribution & Ranking Stability:</b> We implement TreeSHAP strictly on training data to prevent selection leakage, demonstrating robust ranking stability under model retraining (&rho;<sub>s</sub> = 0.973 ± 0.010 across 98 features, Kendall's &tau; = 0.795 within top-20, 95.0% top-20 set overlap; &rho;<sub>s</sub> = 0.9991 under explanation subsampling) and identifying primary signals (directory length, domain activation age, delimiters).", bullet_style))
    story.append(Paragraph("• <b>Feature Reduction & Cascaded Triage:</b> We evaluate nested subsets, selecting k=20 via training CV which sustains full predictive performance (5-seed test mean: 94.71% ± 0.09% acc, 94.95% ± 0.08% F1). Furthermore, evaluating an uncertainty-gated cascade demonstrates that a zero-network lexical-only model (84 features) resolves 64.3% of URLs in-memory with 97.78% accuracy, preserving 94.57% overall pipeline accuracy while cutting external network queries by 64.3%.", bullet_style))
    story.append(Paragraph("• <b>Computational Profiling:</b> We measure model inference latency (mean ± std over 20 repeated runs), single-query latency (N=1), serialized model footprints, and throughput under batched execution.", bullet_style))
    
    # Section II: Related Work
    story.append(Paragraph("II. RELATED WORK", sec_heading))
    story.append(Paragraph(
        "The evolution of automated phishing detection spans four major paradigms: heuristic/blacklist methods, content-based deep learning, URL/network-based machine learning, and Explainable AI (XAI) frameworks.",
        body_style
    ))
    story.append(Paragraph("<i>A. Heuristic and Blacklist-Based Detection</i>", subsec_heading))
    story.append(Paragraph(
        "Early defenses relied on signature repositories and community blacklists [3]. While services like PhishTank and Google Safe Browsing provide authoritative verdicts for cataloged threats, studies by Hannousse and Yahiouche [5] and Marchal et al. [6] show that blacklists suffer from significant discovery latency against zero-day phishing campaigns.",
        body_style
    ))
    story.append(Paragraph("<i>B. Content-Based and Deep Learning Approaches</i>", subsec_heading))
    story.append(Paragraph(
        "To overcome blacklist delays, several studies proposed inspecting web page contents, DOM trees, and scripts. Opara et al. [9] developed HTMLPhish, employing CNN-LSTM networks to analyze raw HTML document flows. Mohammad et al. [15] investigated self-structuring neural networks on page-level features. Adebowale et al. [10] integrated convolutional and recurrent architectures, while Al-Alyan and Al-Ahmadi [16] proposed convolutional models on URL statistical features. However, content fetching incurs multi-second latency and risks drive-by exploit payload execution.",
        body_style
    ))
    story.append(Paragraph("<i>C. URL and Network-Centric Machine Learning</i>", subsec_heading))
    story.append(Paragraph(
        "To achieve high-throughput triage without page rendering, researchers turned toward feature engineering on URLs and network metadata. Sahoo et al. [3] and Rao and Pais [4] established taxonomies of URL lexical properties. Sahingoz et al. [7] evaluated tree classifiers and linear SVMs on lexical representations. Babagoli et al. [8] proposed heuristic non-linear regression strategies for phishing detection, while Chiew et al. [17] analyzed hybrid ensemble feature selection. Vrbančič et al. [11] standardized a benchmark containing 111 structured features across 58,645 URLs, capturing URL, domain, directory, file, query, and resolver metadata without page rendering.",
        body_style
    ))
    story.append(Paragraph("<i>D. Explainable Artificial Intelligence (XAI) in Cybersecurity</i>", subsec_heading))
    story.append(Paragraph(
        "Recent works have explored post-hoc interpretability in phishing detection. Al-Fayoumi et al. [18] proposed XAI-PhD, leveraging TreeSHAP with ensemble models to interpret URL classification decisions and prune features to reduce prediction overhead. Uddin et al. [19] combined gradient-boosting models with SHAP on a public Kaggle dataset. Calzarossa et al. [20] proposed an explainable machine learning procedure to identify critical phishing indicators, while Kehkashan et al. [21] evaluated random forest with SHAP on a Kaggle dataset of 11,000 URLs.",
        body_style
    ))
    story.append(Paragraph(
        "While these studies established the utility of post-hoc explanations, several methodological distinctions and gaps remain: (i) while feature selection studies such as XAI-PhD [18] perform model cross-validation, the methodological description does not explicitly state whether TreeSHAP attributions used for feature pruning were restricted to the training folds or computed across the full dataset prior to reduction, which leaves open the possibility of selection leakage; (ii) attribution ranking stability across random seeds and subsamples is often unquantified; (iii) existing feature selection methods treat all features uniformly, whereas in practice, synchronous external network lookups incur tens to hundreds of milliseconds of latency compared to microsecond in-memory lexical parsing; and (iv) computational latency reporting frequently omits repeated measurement intervals or single-query benchmarking. This paper addresses these challenges by enforcing a strict train-only TreeSHAP protocol on the standardized 58,645 URL corpus [11], verifying attribution stability across seeds, and evaluating an uncertainty-gated cascade that explicitly decouples in-memory lexical parsing from network resolver queries.",
        body_style
    ))
    
    # Section III: Proposed Methodology
    story.append(Paragraph("III. PROPOSED METHODOLOGY", sec_heading))
    story.append(Paragraph(
        "The architectural pipeline of the proposed framework operates across four stages: (i) static feature extraction and zero-variance filtering, (ii) multi-model supervised classification, (iii) leak-free TreeSHAP feature attribution on training data, and (iv) SHAP-directed feature pruning and computational profiling (Fig. 1).",
        body_style
    ))
    
    if os.path.exists("figures/fig1_system_architecture.png"):
        story.append(Image("figures/fig1_system_architecture.png", width=col_w, height=col_w * 0.38))
        story.append(Paragraph("Fig. 1. Architectural Pipeline of the Proposed Explainable Phishing Detection Framework.", caption_style))
        
    story.append(Paragraph("<i>A. Dataset Formulation and Preprocessing</i>", subsec_heading))
    story.append(Paragraph(
        "We utilize the benchmark dataset curated by Vrbančič et al. [11], containing 58,645 URLs (30,647 phishing from PhishTank/OpenPhish and 27,998 legitimate from Alexa top sites, search results, and open community directories). Table I outlines the dataset parameters, and Fig. 2 illustrates class distribution across partitions.",
        body_style
    ))
    
    if os.path.exists("figures/fig2_class_distribution.png"):
        story.append(Image("figures/fig2_class_distribution.png", width=col_w, height=col_w * 0.38))
        story.append(Paragraph("Fig. 2. Class Distribution Across Stratified Partitions.", caption_style))
    
    # Table I: Dataset
    t1_data = [
        [Paragraph("<b>Property</b>", th_style), Paragraph("<b>Specification / Value</b>", th_style)],
        [Paragraph("Dataset Provenance", tc_left_style), Paragraph("Vrbančič et al. (Data in Brief, 2020) [11]", tc_left_style)],
        [Paragraph("Feature Modality", tc_left_style), Paragraph("Static URL Lexical, Path, File, Query, Resolver", tc_left_style)],
        [Paragraph("Total URL Instances", tc_left_style), Paragraph("58,645 URLs", tc_left_style)],
        [Paragraph("Raw Feature Dimensions", tc_left_style), Paragraph("111 Numeric Features (97 Lexical / 14 Resolver; 96/15 in [11])", tc_left_style)],
        [Paragraph("Retained Dimensions", tc_left_style), Paragraph("98 Informative Features (13 Constant Delimiters Filtered)", tc_left_style)],
        [Paragraph("Class Balance", tc_left_style), Paragraph("30,647 Phishing (52.26%) / 27,998 Benign (47.74%)", tc_left_style)],
        [Paragraph("Train / Test Partition", tc_left_style), Paragraph("80% Stratified Train (46,916) / 20% Test (11,729)", tc_left_style)],
        [Paragraph("Missing / Sentinel Values", tc_left_style), Paragraph("0 NaN (Unset/unavailable metrics encoded as -1)", tc_left_style)]
    ]
    t1 = Table(t1_data, colWidths=[col_w * 0.38, col_w * 0.62])
    t1.setStyle(TableStyle([
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
        ('TOPPADDING', (0,0), (-1,-1), 0.5),
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
    ]))
    story.append(Paragraph("<b>TABLE I: DATASET SPECIFICATION AND PARTITIONING</b>", caption_style))
    story.append(t1)
    story.append(Spacer(1, 1.5))
    
    story.append(Paragraph(
        "A cross-partition feature vector audit indicates that exactly 335 test instances (2.86% of the 11,729 test set) share identical 98-feature vectors with instances in the training set. Within partitions, 906 rows in train (1.93%) and 130 rows in test (1.11%) represent internal duplicates due to discrete structural metrics on pathless root domains with default values. Crucially, 332 of the 335 cross-partition twin pairs (99.1%) share identical ground-truth labels (with only 3 label conflicts). Evaluating on the strictly de-duplicated test subset (N = 11,394), XGBoost achieves 94.71% accuracy and 95.05% F1-score, while Random Forest achieves 94.18% accuracy and 94.58% F1-score (compared to 94.82% / 95.05% and 94.30% / 94.57% on the full test set), confirming that cross-partition repetition does not inflate generalization metrics. The numeric sentinel -1 denotes 'not applicable' or 'lookup unavailable' (e.g., URLs lacking directory paths assign -1 to path metrics, and failed WHOIS lookups assign -1 to activation age). Preprocessing fits a zero-variance filter V(X_j) > 0 strictly on D_train. Thirteen constant features (all belonging to the domain structural family) are eliminated, leaving D' = 98 informative features (84 lexical/structural and 14 network/resolver metrics). For distance-based models (Logistic Regression and Linear SVM), features are standardized via z-score scaling fitted exclusively on D_train.",
        body_style
    ))
    story.append(Paragraph("<i>V(X<sub>j</sub>) = (1 / N<sub>train</sub>) &Sigma; (x<sub>ij</sub> - &mu;<sub>j</sub>)<sup>2</sup> &gt; 0 &nbsp;&nbsp;&nbsp;&nbsp; (1)</i>", equation_style))
    story.append(Paragraph("<i>z<sub>ij</sub> = (x<sub>ij</sub> - &mu;<sub>j</sub>) / &sigma;<sub>j</sub> &nbsp;&nbsp;&nbsp;&nbsp; (2)</i>", equation_style))
    
    story.append(Paragraph("<i>B. URL Feature Engineering Taxonomy</i>", subsec_heading))
    story.append(Paragraph(
        "The 111 structured metrics span six cybersecurity feature families (20 + 21 + 18 + 18 + 20 + 14 = 111 raw; 20 + 8 + 18 + 18 + 20 + 14 = 98 retained):",
        body_style
    ))
    story.append(Paragraph("1) <b>URL Lexical</b> (20/20 retained): URL length (length_url), presence flags (email_in_url), and delimiter frequencies (qty_slash_url, qty_dot_url, qty_hyphen_url, qty_equal_url, qty_and_url). Vrbančič et al. [11] counted email_in_url among 15 custom script features; because it uses purely regex-based string matching with 0 external network requests, we classify it as lexical, leaving 14 network/resolver features.", bullet_style))
    story.append(Paragraph("2) <b>Domain Structural</b> (21/8 retained): Domain length, IP indicator, authority dots (qty_dot_domain), vowels, and hyphens (13 constant delimiter counts eliminated by zero-variance filtering).", bullet_style))
    story.append(Paragraph("3) <b>Directory/Path</b> (18/18 retained): Directory length (directory_length), slash nesting count (qty_slash_directory), and path delimiters (encoded as -1 when no directory is present).", bullet_style))
    story.append(Paragraph("4) <b>File-Level</b> (18/18 retained): Filename length (file_length) and character frequencies.", bullet_style))
    story.append(Paragraph("5) <b>Query/Parameter</b> (20/20 retained): Query length (params_length), parameter count (qty_params), and argument delimiters.", bullet_style))
    story.append(Paragraph("6) <b>Resolver/Network</b> (14/14 retained): Domain activation age (time_domain_activation), expiration time (time_domain_expiration), DNS TTL (ttl_hostname), ASN (asn_ip), lookup latency (time_response), nameservers (qty_nameservers), MX records (qty_mx_servers), resolved IPs (qty_ip_resolved), TLS certificate flag (tls_ssl_certificate), SPF records (domain_spf), redirect hops (qty_redirects), full URL Google index (url_google_index), domain Google index (domain_google_index), and URL shortener lookup flag (url_shortened). Filtering 13 constant domain delimiters leaves exactly 84 purely in-memory lexical and structural features across groups 1–5 that require strictly 0 external network lookups.", bullet_style))
    
    story.append(Paragraph("<i>C. Classification Model Architectures</i>", subsec_heading))
    story.append(Paragraph(
        "We evaluate five diverse classification paradigms: (i) <b>Logistic Regression (LR)</b> with L2 regularization (C=1.0); (ii) <b>Decision Trees (DT)</b> with Gini impurity splitting (max_depth=12); (iii) <b>Random Forest (RF)</b> ensemble with 100 bagging trees (max_depth=15); (iv) <b>Linear SVM</b> with Platt calibration; and (v) <b>XGBoost</b> [12] (100 estimators, max_depth=6, eta=0.1, subsample=0.8, colsample=0.8). Table II outlines hyperparameter specifications.",
        body_style
    ))
    
    # Table II: Model Configurations
    t2_data = [
        [Paragraph("<b>Architecture</b>", th_style), Paragraph("<b>Hyperparameter Configuration</b>", th_style)],
        [Paragraph("Logistic Reg.", tc_left_style), Paragraph("L2 penalty, C=1.0, L-BFGS solver, max_iter=1000", tc_left_style)],
        [Paragraph("Decision Tree", tc_left_style), Paragraph("Gini Impurity, max_depth=12, min_samples_split=10", tc_left_style)],
        [Paragraph("Random Forest", tc_left_style), Paragraph("100 Trees, max_depth=15, min_samples_split=5", tc_left_style)],
        [Paragraph("Linear SVM", tc_left_style), Paragraph("LinearSVC (C=1.0), Platt Calibrated (3-fold CV)", tc_left_style)],
        [Paragraph("XGBoost", tc_left_style), Paragraph("100 Estimators, max_depth=6, eta=0.1, subsample=0.8, colsample=0.8", tc_left_style)]
    ]
    t2 = Table(t2_data, colWidths=[col_w * 0.32, col_w * 0.68])
    t2.setStyle(TableStyle([
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
        ('TOPPADDING', (0,0), (-1,-1), 0.5),
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
    ]))
    story.append(Paragraph("<b>TABLE II: MODEL HYPERPARAMETER CONFIGURATIONS</b>", caption_style))
    story.append(t2)
    story.append(Spacer(1, 1.5))
    
    story.append(Paragraph("<i>D. Explainable AI via TreeSHAP</i>", subsec_heading))
    story.append(Paragraph(
        "To explain model decisions, we deploy TreeSHAP [13], [14], which satisfies the additive attribution property f(x) = phi_0 + sum(phi_j(x)), where phi_0 = E[f(x)] is the expected base model output, and phi_j(x) is the Shapley attribution:",
        body_style
    ))
    story.append(Paragraph("<i>f(x) = &phi;<sub>0</sub> + &Sigma;<sub>j=1</sub><sup>D'</sup> &phi;<sub>j</sub>(x) &nbsp;&nbsp;&nbsp;&nbsp; (3)</i>", equation_style))
    story.append(Paragraph("<i>I<sub>j</sub> = (1 / |X<sub>train,exp</sub>|) &Sigma;<sub>i</sub> |&phi;<sub>j</sub>(x<sub>i</sub>)| &nbsp;&nbsp;&nbsp;&nbsp; (4)</i>", equation_style))
    story.append(Paragraph(
        "Global feature importance I_j is computed as the mean absolute SHAP value strictly over a training explanation subset X_train,exp (N=500 random samples). Deriving I_j exclusively on D_train eliminates selection leakage into feature selection. Global feature rankings demonstrate high stability across explanation subsample seeds (&rho;<sub>s</sub> = 0.9991 over all 98 features, Pearson r = 0.9995, Kendall &tau; = 0.9131 ± 0.026 within the Top-20, and 100% top-20 set overlap; &rho;<sub>s</sub> = 0.9995 between N=500 and N=1,000). When retraining the underlying model across 5 seeds, rank agreement remains robust (&rho;<sub>s</sub> = 0.973 ± 0.010 across 98 features, Kendall &tau; = 0.7948 ± 0.031 within the Top-20). Ranked features direct nested feature pruning.",
        body_style
    ))
    
    # Section IV: Experimental Setup
    story.append(Paragraph("IV. EXPERIMENTAL SETUP", sec_heading))
    story.append(Paragraph(
        "All experiments are implemented in Python 3.14 utilizing scikit-learn (v1.9.1), xgboost (v3.4.1), shap (v0.52.0), and scipy (v1.18.1). Execution was conducted on an x86_64 Linux environment equipped with an Intel Core i5-3337U processor @ 1.80 GHz (2 physical cores, 4 threads) and 4 GB RAM running Ubuntu Linux. Random seed 42 is fixed across data partitioning, cross-validation folds, and subsampling for deterministic reproducibility, with multi-seed evaluations (seeds 42, 123, 456, 789, 2024; varying model tree subsampling on fixed test split) validating variance bounds.",
        body_style
    ))
    story.append(Paragraph(
        "Generalization stability is evaluated using 5-Fold Stratified Cross-Validation on the training partition (N_train = 46,916), recording mean ± std across folds. Crucially, to prevent data leakage across validation folds, zero-variance feature filtering and standard scaling transformations are fitted strictly within each training fold pipeline rather than globally prior to cross-validation. Final model evaluation is performed on the untouched held-out test partition (N_test = 11,729). Statistical significance between classifier predictions is verified using McNemar's test with Edwards continuity correction.",
        body_style
    ))
    story.append(Paragraph(
        "Model inference latency is measured in batched vector mode over the entire held-out test matrix (N=11,729) using predict() with multi-threading enabled (n_jobs=-1). Each model executes two warm-up passes followed by 20 repeated measurement iterations (mean ± std in ms / 1,000 URLs). In addition, to account for single-threaded runtime differences across linear and tree models under unbatched stream deployment, we benchmark single-query latency (N=1, batch size 1) across 500 repeated trials (Decision Tree: 0.22 ms, Logistic Regression: 0.30 ms, XGBoost: 0.71 ms [~60× the 11.6 µs feature extraction latency], Linear SVM: 4.01 ms, Random Forest: 49.38 ms; Top-20 XGBoost: 0.46 ms median / 0.56 ms mean). Storage footprint is measured by serializing fitted model structures using joblib (compression level 3). In-memory string-based feature extraction speed is benchmarked over 10,000 raw URL string parsing operations (extracting all 84 retained lexical properties including character counts, token delimiters, and structural lengths across URL, domain authority, directory path, filename, and query parameter components in pure CPU memory without I/O), yielding an average extraction latency of 11.6 &mu;s per URL (11.6 ms per 10<sup>3</sup> URLs).",
        body_style
    ))
    
    # Section V: Results and Empirical Analysis
    story.append(Paragraph("V. RESULTS AND EMPIRICAL ANALYSIS", sec_heading))
    story.append(Paragraph("<i>A. Comparative Classifier Performance</i>", subsec_heading))
    story.append(Paragraph(
        "Table III summarizes the empirical performance of all five machine learning models on the held-out test partition (N_test = 11,729), alongside 5-fold cross-validation scores on the training set, PR-AUC (Average Precision), batched inference latency, and single-query latency.",
        body_style
    ))
    
    # Table III: Model Comparison - clean 8 columns with zero text wrapping
    t3_data = [
        [
            Paragraph("<b>Model Architecture</b>", th_style),
            Paragraph("<b>Acc (%)</b>", th_style),
            Paragraph("<b>F1 (%)</b>", th_style),
            Paragraph("<b>ROC</b>", th_style),
            Paragraph("<b>PR (AP)</b>", th_style),
            Paragraph("<b>5-Fold CV F1</b>", th_style),
            Paragraph("<b>Batch Lat (ms/1k URLs)</b>", th_style),
            Paragraph("<b>Single Lat</b>", th_style)
        ],
        [
            Paragraph("Logistic Regression", tc_left_style),
            Paragraph("89.97", tc_style),
            Paragraph("90.55", tc_style),
            Paragraph("0.9613", tc_style),
            Paragraph("0.9637", tc_style),
            Paragraph("90.48 ± 0.20", tc_style),
            Paragraph("1.41 ± 0.16", tc_style),
            Paragraph("0.30 ms", tc_style)
        ],
        [
            Paragraph("Decision Tree", tc_left_style),
            Paragraph("93.61", tc_style),
            Paragraph("93.92", tc_style),
            Paragraph("0.9668", tc_style),
            Paragraph("0.9546", tc_style),
            Paragraph("93.62 ± 0.17", tc_style),
            Paragraph("0.53 ± 0.05", tc_style),
            Paragraph("0.22 ms", tc_style)
        ],
        [
            Paragraph("Random Forest", tc_left_style),
            Paragraph("94.30", tc_style),
            Paragraph("94.57", tc_style),
            Paragraph("0.9867", tc_style),
            Paragraph("0.9880", tc_style),
            Paragraph("94.79 ± 0.11", tc_style),
            Paragraph("10.60 ± 0.31", tc_style),
            Paragraph("49.38 ms", tc_style)
        ],
        [
            Paragraph("Linear SVM", tc_left_style),
            Paragraph("89.99", tc_style),
            Paragraph("90.58", tc_style),
            Paragraph("0.9613", tc_style),
            Paragraph("0.9637", tc_style),
            Paragraph("90.45 ± 0.22", tc_style),
            Paragraph("2.85 ± 0.20", tc_style),
            Paragraph("4.01 ms", tc_style)
        ],
        [
            Paragraph("<b>XGBoost</b>", tc_left_bold_style),
            Paragraph("<b>94.82</b>", tc_bold_style),
            Paragraph("<b>95.05</b>", tc_bold_style),
            Paragraph("<b>0.9879</b>", tc_bold_style),
            Paragraph("<b>0.9889</b>", tc_bold_style),
            Paragraph("<b>95.17 ± 0.13</b>", tc_bold_style),
            Paragraph("<b>2.46 ± 0.20</b>", tc_bold_style),
            Paragraph("<b>0.71 ms</b>", tc_bold_style)
        ]
    ]
    t3 = Table(t3_data, colWidths=[
        col_w*0.22, col_w*0.09, col_w*0.09, col_w*0.11,
        col_w*0.11, col_w*0.16, col_w*0.12, col_w*0.10
    ])
    t3.setStyle(TableStyle([
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
        ('TOPPADDING', (0,0), (-1,-1), 0.5),
        ('LEFTPADDING', (0,0), (-1,-1), 1.2),
        ('RIGHTPADDING', (0,0), (-1,-1), 1.2),
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
    ]))
    story.append(Paragraph("<b>TABLE III: CLASSIFICATION PERFORMANCE & LATENCY (N=11,729)</b>", caption_style))
    story.append(t3)
    story.append(Spacer(1, 1.5))
    
    story.append(Paragraph(
        "Tree-based ensemble architectures demonstrate superior discriminative capability over linear baselines. XGBoost achieves the highest overall performance: 94.82% Accuracy, 94.88% Precision, 95.22% Recall, 95.05% F1, 0.9879 ROC-AUC, and 0.9889 PR-AUC (5-fold CV F1: 95.17% ± 0.13%) with 2.46 ± 0.20 ms batch latency per 10<sup>3</sup> URLs and 0.71 ms single-query latency (~60× the 11.6 µs feature extraction time). Random Forest attains 94.30% Accuracy, 94.57% F1, and 0.9867 ROC-AUC (CV F1: 94.79% ± 0.11%). Decision Tree achieves 93.61% Accuracy and 93.92% F1 at 0.53 ± 0.05 ms batch latency and 0.22 ms single-query latency, with Average Precision of 0.9546. Linear models (Logistic Regression and Linear SVM) attain 89.97% and 89.99% accuracy (CV F1: 90.48% and 90.45%), producing near-identical ROC-AUC (0.9613) and PR-AUC (0.9637). This occurs because both fit regularized hyperplanes on standardized features: the cosine similarity between their weight vectors is 0.8307, and the Spearman rank correlation between their test decision scores reaches &rho;<sub>s</sub> = 0.9997 (Pearson r = 0.9836), rendering their ranking-based metrics indistinguishable at four decimal places. Fig. 3 illustrates the Receiver Operating Characteristic (ROC) and Precision-Recall (PR) curves across all evaluated models.",
        body_style
    ))
    story.append(Paragraph(
        "On the test set, XGBoost identifies 5,836 True Positives out of 6,129 phishing URLs (Recall = 95.22%) and 5,285 True Negatives out of 5,600 benign URLs (Specificity = 94.38%), with FPR = 5.62% and FNR = 4.78%. McNemar's test with continuity correction yields chi2 = 13.79 (p = 2.04e-4 &lt; 0.001), confirming XGBoost's statistical superiority over Random Forest. Multi-seed evaluation across 5 random seeds (seeds 42, 123, 456, 789, 2024; varying model tree subsampling on fixed test split) confirms stability: XGBoost achieves mean accuracy of 94.74% ± 0.08% and mean F1 of 94.98% ± 0.08% versus Random Forest's 94.59% ± 0.06%.",
        body_style
    ))
    
    if os.path.exists("figures/fig5_roc_pr_curves.png"):
        story.append(Image("figures/fig5_roc_pr_curves.png", width=col_w, height=col_w * 0.38))
        story.append(Paragraph("Fig. 3. Discrimination Diagnostics: (a) ROC, and (b) PR Curves across classifiers.", caption_style))
        
    story.append(Paragraph("<i>B. Explainability and Feature Attribution Analysis</i>", subsec_heading))
    story.append(Paragraph(
        "TreeSHAP analysis was executed strictly on the training partition (N=500 random samples) to extract global feature rankings without selection leakage. Table IV details the top 10 most influential features according to mean absolute SHAP value and plausible cybersecurity semantic interpretations.",
        body_style
    ))
    
    # Table IV: Top SHAP Features - formatted with ample interpretation width
    t4_data = [
        [
            Paragraph("<b>Rank</b>", th_style),
            Paragraph("<b>Feature Identifier</b>", th_style),
            Paragraph("<b>Mod.</b>", th_style),
            Paragraph("<b>|SHAP|</b>", th_style),
            Paragraph("<b>Plausible Cybersecurity Interpretation</b>", th_style)
        ],
        [
            Paragraph("1", tc_style),
            Paragraph("directory_length", tc_left_style),
            Paragraph("Lex", tc_style),
            Paragraph("1.0811", tc_style),
            Paragraph("Path length/presence (deep nesting masks fraud; -1 = no path)", tc_left_style)
        ],
        [
            Paragraph("2", tc_style),
            Paragraph("time_domain_activation", tc_left_style),
            Paragraph("Net", tc_style),
            Paragraph("0.9912", tc_style),
            Paragraph("Domain age (new domains/failed WHOIS signal throwaways)", tc_left_style)
        ],
        [
            Paragraph("3", tc_style),
            Paragraph("qty_slash_url", tc_left_style),
            Paragraph("Lex", tc_style),
            Paragraph("0.7377", tc_style),
            Paragraph("Forward slash delimiter count across URL hierarchy", tc_left_style)
        ],
        [
            Paragraph("4", tc_style),
            Paragraph("length_url", tc_left_style),
            Paragraph("Lex", tc_style),
            Paragraph("0.7222", tc_style),
            Paragraph("Raw URL character length (used to obscure landing)", tc_left_style)
        ],
        [
            Paragraph("5", tc_style),
            Paragraph("qty_dot_domain", tc_left_style),
            Paragraph("Lex", tc_style),
            Paragraph("0.5293", tc_style),
            Paragraph("Subdomain dot count (used in multi-level brand spoofing)", tc_left_style)
        ],
        [
            Paragraph("6", tc_style),
            Paragraph("ttl_hostname", tc_left_style),
            Paragraph("Net", tc_style),
            Paragraph("0.3147", tc_style),
            Paragraph("DNS TTL metric (short TTLs reflect fast-flux evasive DNS)", tc_left_style)
        ],
        [
            Paragraph("7", tc_style),
            Paragraph("asn_ip", tc_left_style),
            Paragraph("Net", tc_style),
            Paragraph("0.2057", tc_style),
            Paragraph("Autonomous System Number (flags bulletproof/rogue ASNs)", tc_left_style)
        ],
        [
            Paragraph("8", tc_style),
            Paragraph("time_response", tc_left_style),
            Paragraph("Net", tc_style),
            Paragraph("0.1724", tc_style),
            Paragraph("HTTP lookup response latency in seconds (host variability)", tc_left_style)
        ],
        [
            Paragraph("9", tc_style),
            Paragraph("qty_hyphen_directory", tc_left_style),
            Paragraph("Lex", tc_style),
            Paragraph("0.1277", tc_style),
            Paragraph("Hyphens in path (inserted to mimic trusted brand keywords)", tc_left_style)
        ],
        [
            Paragraph("10", tc_style),
            Paragraph("qty_redirects", tc_left_style),
            Paragraph("Net", tc_style),
            Paragraph("0.1082", tc_style),
            Paragraph("HTTP redirect hop count (multi-hop chains obscure target)", tc_left_style)
        ]
    ]
    t4 = Table(t4_data, colWidths=[col_w*0.09, col_w*0.25, col_w*0.08, col_w*0.10, col_w*0.48])
    t4.setStyle(TableStyle([
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
        ('TOPPADDING', (0,0), (-1,-1), 0.5),
        ('LEFTPADDING', (0,0), (-1,-1), 1.2),
        ('RIGHTPADDING', (0,0), (-1,-1), 1.2),
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
    ]))
    story.append(Paragraph("<b>TABLE IV: TOP 10 SHAP FEATURES AND INTERPRETATIONS</b>", caption_style))
    story.append(t4)
    story.append(Spacer(1, 1.5))
    
    if os.path.exists("figures/fig7_shap_summary_beeswarm.png"):
        story.append(Image("figures/fig7_shap_summary_beeswarm.png", width=col_w, height=col_w * 0.38))
        story.append(Paragraph("Fig. 4. SHAP Summary Beeswarm Plot on Training Partition.", caption_style))
        
    story.append(Paragraph(
        "Fig. 4 illustrates directional attributions across training instances. Crucially, the interpretation of directory_length and time_domain_activation must be contextualized with -1 sentinel encoding. Because absence of directory or failed WHOIS resolution is coded as -1, tree decision boundaries split on whether a feature is positive versus <= 0, effectively encoding qualitative presence alongside quantitative magnitude within a single scalar dimension.",
        body_style
    ))
        
    story.append(Paragraph("<i>C. Feature Selection and Computational Benchmarking</i>", subsec_heading))
    story.append(Paragraph(
        "To assess whether compact feature subsets maintain classification performance, we evaluated XGBoost across nested feature subsets ranked by training set SHAP importance: Full (98 features), Top-30, Top-20, Top-10, Top-5, alongside a dedicated Lexical-Only baseline (84 features, 0 network lookups). Table V and Fig. 5 delineate performance, latency, and throughput trade-offs.",
        body_style
    ))
    
    # Table V: Feature Selection & Computational Resources - clean widths
    t5_data = [
        [
            Paragraph("<b>Configuration</b>", th_style),
            Paragraph("<b>Net/Lex</b>", th_style),
            Paragraph("<b>Acc (%)</b>", th_style),
            Paragraph("<b>F1 (%)</b>", th_style),
            Paragraph("<b>ROC</b>", th_style),
            Paragraph("<b>Lat (ms/1k)</b>", th_style),
            Paragraph("<b>Size (MB)</b>", th_style),
            Paragraph("<b>Throughput (q/s)</b>", th_style)
        ],
        [
            Paragraph("XGBoost (Full 98)", tc_left_style),
            Paragraph("14N/84L", tc_style),
            Paragraph("94.82", tc_style),
            Paragraph("95.05", tc_style),
            Paragraph("0.9879", tc_style),
            Paragraph("2.46 ± 0.20", tc_style),
            Paragraph("0.126", tc_style),
            Paragraph("406,318", tc_style)
        ],
        [
            Paragraph("XGBoost (Top-30)", tc_left_style),
            Paragraph("12N/18L", tc_style),
            Paragraph("94.74", tc_style),
            Paragraph("94.97", tc_style),
            Paragraph("0.9882", tc_style),
            Paragraph("1.83 ± 0.07", tc_style),
            Paragraph("0.134", tc_style),
            Paragraph("546,448", tc_style)
        ],
        [
            Paragraph("<b>XGBoost (Top-20)</b>", tc_left_bold_style),
            Paragraph("<b>11N/9L</b>", tc_bold_style),
            Paragraph("<b>94.82</b>", tc_bold_style),
            Paragraph("<b>95.05</b>", tc_bold_style),
            Paragraph("<b>0.9876</b>", tc_bold_style),
            Paragraph("<b>1.67 ± 0.06</b>", tc_bold_style),
            Paragraph("<b>0.130</b>", tc_bold_style),
            Paragraph("<b>600,099</b>", tc_bold_style)
        ],
        [
            Paragraph("XGBoost (Top-10)", tc_left_style),
            Paragraph("5N/5L", tc_style),
            Paragraph("94.19", tc_style),
            Paragraph("94.48", tc_style),
            Paragraph("0.9859", tc_style),
            Paragraph("1.57 ± 0.11", tc_style),
            Paragraph("0.126", tc_style),
            Paragraph("636,942", tc_style)
        ],
        [
            Paragraph("XGBoost (Top-5)", tc_left_style),
            Paragraph("1N/4L", tc_style),
            Paragraph("91.32", tc_style),
            Paragraph("91.84", tc_style),
            Paragraph("0.9723", tc_style),
            Paragraph("1.59 ± 0.12", tc_style),
            Paragraph("0.121", tc_style),
            Paragraph("628,930", tc_style)
        ],
        [
            Paragraph("<b>XGBoost (Lexical-84)</b>", tc_left_bold_style),
            Paragraph("<b>0N/84L</b>", tc_bold_style),
            Paragraph("<b>89.68</b>", tc_bold_style),
            Paragraph("<b>90.04</b>", tc_bold_style),
            Paragraph("<b>0.9627</b>", tc_bold_style),
            Paragraph("<b>3.16 ± 0.43</b>", tc_bold_style),
            Paragraph("<b>0.342</b>", tc_bold_style),
            Paragraph("<b>316,002</b>", tc_bold_style)
        ],
        [
            Paragraph("Random Forest", tc_left_style),
            Paragraph("14N/84L", tc_style),
            Paragraph("94.30", tc_style),
            Paragraph("94.57", tc_style),
            Paragraph("0.9867", tc_style),
            Paragraph("10.60 ± 0.31", tc_style),
            Paragraph("4.068", tc_style),
            Paragraph("94,369", tc_style)
        ],
        [
            Paragraph("Decision Tree", tc_left_style),
            Paragraph("14N/84L", tc_style),
            Paragraph("93.61", tc_style),
            Paragraph("93.92", tc_style),
            Paragraph("0.9668", tc_style),
            Paragraph("0.53 ± 0.05", tc_style),
            Paragraph("0.029", tc_style),
            Paragraph("1,884,868", tc_style)
        ],
        [
            Paragraph("Linear SVM", tc_left_style),
            Paragraph("14N/84L", tc_style),
            Paragraph("89.99", tc_style),
            Paragraph("90.58", tc_style),
            Paragraph("0.9613", tc_style),
            Paragraph("2.85 ± 0.20", tc_style),
            Paragraph("0.006", tc_style),
            Paragraph("350,920", tc_style)
        ],
        [
            Paragraph("Logistic Regression", tc_left_style),
            Paragraph("14N/84L", tc_style),
            Paragraph("89.97", tc_style),
            Paragraph("90.55", tc_style),
            Paragraph("0.9613", tc_style),
            Paragraph("1.41 ± 0.16", tc_style),
            Paragraph("0.004", tc_style),
            Paragraph("708,898", tc_style)
        ]
    ]
    t5 = Table(t5_data, colWidths=[
        col_w*0.25, col_w*0.12, col_w*0.09, col_w*0.09,
        col_w*0.09, col_w*0.13, col_w*0.09, col_w*0.14
    ])
    t5.setStyle(TableStyle([
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
        ('TOPPADDING', (0,0), (-1,-1), 0.5),
        ('LEFTPADDING', (0,0), (-1,-1), 1.2),
        ('RIGHTPADDING', (0,0), (-1,-1), 1.2),
        ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,6), (-1,6), 0.4, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.8, colors.black),
    ]))
    story.append(Paragraph("<b>TABLE V: FEATURE REDUCTION TRADE-OFFS AND RESOURCE PROFILES (SEED 42)</b>", caption_style))
    story.append(t5)
    story.append(Spacer(1, 1.5))
    
    story.append(Paragraph(
        "The optimal subset size k=20 was selected via 5-fold cross-validation on the training set (CV F1: k=5: 91.85%, k=10: 94.52%, k=20: 95.02%, k=30: 95.17%, k=98: 95.20%), where k=20 marks the distinct performance plateau. Pruning the feature space to the Top-20 subset (a 79.6% reduction) preserves full predictive performance: seed 42 achieves 94.82% Accuracy, 95.05% F1-score, and 0.9876 ROC-AUC, with a 5-seed test mean of 94.71% ± 0.09% accuracy, 94.95% ± 0.08% F1-score, and 0.9876 ± 0.0001 ROC-AUC. Concurrently, model inference latency decreases from 2.46 ± 0.20 ms to 1.67 ± 0.06 ms per 10<sup>3</sup> queries in batch mode (a 32.3% reduction; single-query latency falls to 0.46 ms median, 0.56 ms mean vs. 0.71 ms for Full 98), while batch throughput increases from 406,318 to 600,099 queries/s on standard CPU hardware. Crucially, the Lexical-Only model achieves 89.68% accuracy, 90.04% F1-score, and 0.9627 ROC-AUC (CV F1: 90.19% ± 0.17%) using zero network lookups.",
        body_style
    ))
    story.append(Paragraph(
        "To empirically validate a practical two-tier architecture, we evaluated an uncertainty-gated cascade: when the Tier 1 lexical model's predicted probability falls within an uncertainty band [&tau;<sub>L</sub>, &tau;<sub>H</sub>], classification is deferred to the Tier 2 Top-20 resolver model. Operating thresholds were calibrated via 5-fold cross-validation on the training set to maximize query offloading while constraining the Tier-1 out-of-fold phishing leakage rate below 2.5% (CV sweep at [0.10, 0.90]: 64.21% coverage, 97.98% accuracy, 2.35% phishing leak rate). On the held-out test partition (N=11,729), Tier 1 autonomously resolves 64.28% of instances (7,539 URLs) purely in-memory with 97.78% accuracy, eliminating external lookups for nearly two-thirds of incoming traffic. Specifically, Tier 1 classifies 3,380 URLs as legitimate (p &lt; 0.10) with 90 false negatives, yielding a test phishing leakage rate of 2.66% (slightly above the 2.5% CV design target due to test distribution variance), and 4,159 URLs as phishing (p &gt; 0.90) with 4,082 true phishing. This yields a conditional Tier-1 phishing recall of 97.84% (4,082/4,172) on the resolved subset; however, accounting for the 1,957 deferred phishing URLs and 90 Tier-1 leaks, the end-to-end cascade achieves an overall FNR of 4.98% (305/6,129) and FPR of 5.93% (332/5,600), compared to 4.78% FNR and 5.62% FPR for monolithic full-network XGBoost. Tier 1 resolves 3,051 pathless legitimate, 316 legitimate with paths, 89 pathless phishing, and 4,083 phishing with paths. Notably, of the 141 pathless phishing URLs in the test set, 88 (62.4%) are predicted legitimate at Tier 1 (p &lt; 0.10) and bypass Tier 2 entirely, highlighting an operational blind spot for root-domain phishing. The deferred 4,190 ambiguous URLs (1,908 legitimate with paths, 1,905 phishing with paths, 325 pathless legitimate, 52 pathless phishing) are evaluated by Tier 2, which achieves 88.78% accuracy on these difficult instances. Overall pipeline accuracy reaches 94.57% and F1-score reaches 94.81%—matching within 0.25 percentage points (pp) of monolithic full-network accuracy (and within 0.24 pp for F1-score) while saving 64.28% of resolver lookups. Under a narrower deferral band [0.15, 0.85] (wider decisive margin), 73.1% of queries are resolved at Tier 1 with 96.93% accuracy (94.42% overall accuracy).",
        body_style
    ))
    story.append(Paragraph(
        "As a baseline, a heuristic classifying URLs as phishing whenever a directory path exists (directory_length > -1) achieves 79.84% accuracy, 83.51% F1-score, and 97.70% recall, exploiting dataset sampling skew (97.70% of phishing vs 39.71% of legitimate URLs contain paths). On the 8,212 path-bearing test URLs, where the naive heuristic achieves only 72.92% accuracy, the full XGBoost model attains 93.59% accuracy (Recall = 96.34%, F1 = 95.64%), demonstrating genuine discriminative learning beyond path presence. On the 3,517 pathless URLs, XGBoost achieves 97.67% accuracy and 99.76% specificity (Recall = 47.52%, F1 = 62.04%). An ablation removing all 56 path, directory, file, and parameter features ('no path/file/query-group features') yielded a 28-feature URL/domain lexical model that achieves 89.17% accuracy (86.23% on path-bearing, 96.05% on pathless) and 89.58% F1-score. When deployed in Tier 1 of the cascade at [0.10, 0.90], this model resolves 62.48% of test queries (7,328 URLs) with 97.69% accuracy, sustaining 94.53% overall cascade accuracy and 94.78% F1-score, confirming that non-path lexical cues reduce reliance on explicit path tokens while still supporting a tiered design.",
        body_style
    ))
    
    if os.path.exists("figures/fig9_feature_reduction_comparison.png"):
        story.append(Image("figures/fig9_feature_reduction_comparison.png", width=col_w, height=col_w * 0.38))
        story.append(Paragraph("Fig. 5. Classification Performance vs. Dimensionality and Latency.", caption_style))
        
    # Section VI: Discussion & Limitations
    story.append(Paragraph("VI. DISCUSSION & LIMITATIONS", sec_heading))
    story.append(Paragraph("<i>A. Operational Considerations & Tiered Deployment</i>", subsec_heading))
    story.append(Paragraph(
        "A critical operational factor in ML phishing detection is distinguishing feature extraction latency from model inference latency. While model inference takes 1.67 ms per 1,000 queries (model-only), external resolver queries introduce substantial round-trip network delays—typically tens to hundreds of milliseconds for synchronous DNS resolution, WHOIS TCP queries, and TLS handshakes [5], [6]—as well as strict query rate limits, making synchronous external queries impractical for high-volume inline network inspection. In contrast, lexical URL features are parsed in-memory at 11.6 &mu;s per URL with zero external overhead. This motivates and empirically validates the evaluated two-tier perimeter defense: Tier 1 resolves 64.28% of instances with 97.78% accuracy in-memory, while Tier 2 executes only for the remaining borderline cases, sustaining 94.57% pipeline accuracy while cutting resolver load by nearly two-thirds.",
        body_style
    ))
    story.append(Paragraph("<i>B. Quantitative Error Analysis</i>", subsec_heading))
    story.append(Paragraph(
        "Analysis of 293 False Negatives (FN = 293, 4.78% of phishing test samples) and 315 False Positives (FP = 315, 5.62% of legitimate test samples) reveals distinct structural patterns influenced by -1 sentinel distributions:",
        body_style
    ))
    story.append(Paragraph("• <b>False Negatives:</b> Phishing URLs misclassified as legitimate exhibited shallow or absent directory paths (median 1.0 char, mean 6.57 vs. median 24.0, mean 29.57 in TP), shorter overall length (median 22.0 vs. 48.0 in TP), and fewer slashes (median 1.0 vs. 3.0 in TP). Crucially, 44.71% of FNs (131/293) had failed WHOIS lookups resulting in -1 sentinels for domain activation age, compared to 35.32% in TPs (2,061/5,836), a statistically significant difference (&chi;<sup>2</sup> = 10.31, <i>p</i> = 0.0013, chi-square contingency test). Including -1 sentinels, median domain age was 159.0 days for FNs vs 682.5 days for TPs, driven by the higher concentration of failed lookups. However, excluding -1 sentinels, valid FN domains averaged 3,351.66 days (median 2,702.50 days, N=162) versus valid TP domains averaging 2,313.14 days (median 1,914.00 days, N=3,775). This suggests that FNs evade detection through two mechanisms: (i) lookup failures that collapse into default -1 sentinels, and (ii) hosting on genuinely older, compromised legitimate domains or aged parked infrastructure.", bullet_style))
    story.append(Paragraph("• <b>False Positives:</b> Legitimate URLs misclassified as phishing featured elongated directory paths (median 13.0 chars, mean 18.55 vs. median -1.0, mean 3.41 in TN; 97.5% of FPs had paths vs. only 36.3% of TNs), longer URLs (median 33.0 vs. 18.0 in TN), and directory hyphens (mean 0.63 vs. -0.49 in TN; excluding -1 sentinels, FP mean was 0.67 vs. 0.41 in TN), typical of single-page apps, deep tracking links, and UTM parameter structures.", bullet_style))
    story.append(Paragraph("<i>C. Limitations and Threats to Validity</i>", subsec_heading))
    story.append(Paragraph(
        "Key limitations and threats to validity include: (1) <i>Sampling Artifacts & Row Duplication</i>: legitimate URLs originate from Alexa top domains and search indices (where 60.29% assign -1 for directory absence), while phishing URLs originate from PhishTank (97.70% contain sub-paths). An exact cross-partition audit identified 335 instances (2.86% of test) sharing identical feature vectors with training rows, 99.1% of which share identical labels. Evaluating on the strictly de-duplicated test subset (N=11,394) preserves 94.71% accuracy and 95.05% F1-score for XGBoost (94.18% / 94.58% for RF), confirming that row repetition does not alter conclusions; (2) <i>Adversarial Evasion and Root-Domain Blind Spots</i>: because Tier 1 relies heavily on lexical and path metrics, adversaries hosting phishing pages directly at root domains can evade Tier 1 triage—88 of 141 pathless phishing test URLs (62.4%) were misclassified as legitimate at Tier 1 and bypassed Tier 2. Attackers aware of path-heavy features can also craft minimal-path URLs or manipulate delimiter frequencies to manipulate SHAP attributions; (3) <i>Temporal Age & Concept Drift</i>: the dataset dates from 2020, requiring ongoing validation against modern evasion tactics (e.g. serverless proxies, IPFS gateways); (4) <i>Lookup Reliability</i>: external WHOIS/DNS queries may experience rate-limiting, collapsing metrics into -1 sentinels; and (5) <i>Hyperparameter Tuning</i>: models were evaluated on standard baseline configurations.",
        body_style
    ))
    
    # Section VII: Conclusion & Future Work
    story.append(Paragraph("VII. CONCLUSION & FUTURE WORK", sec_heading))
    story.append(Paragraph(
        "In this paper, we presented an empirical benchmark and explainable machine learning framework for phishing website detection using 111 structured URL lexical, directory path, file, query, and resolver features. Evaluated on 58,645 URLs, XGBoost achieved superior predictive performance: a 5-seed mean of 94.74% ± 0.08% accuracy and 94.98% ± 0.08% F1-score (seed 42: 94.82% Accuracy, 94.88% Precision, 95.22% Recall, 95.05% F1-score, and 0.9879 ROC-AUC on 11,729 held-out test samples; 5-fold CV F1: 95.17% ± 0.13%), demonstrating statistically significant superiority over Random Forest via McNemar's test (p &lt; 0.001).",
        body_style
    ))
    story.append(Paragraph(
        "By integrating TreeSHAP strictly on training data to eliminate selection leakage, the framework provides transparent and stable (&rho;<sub>s</sub> = 0.9991 Spearman rank correlation, Kendall &tau; = 0.9131 within Top-20; 100% top-20 set overlap) feature attributions, identifying directory length, domain age, delimiter frequency, and URL length as primary discriminative signals. Systematic feature reduction, guided by training cross-validation (elbow at k=20), revealed that pruning 79.6% of features (from 98 to 20) preserves full predictive performance (5-seed test mean: 94.71% ± 0.09% accuracy, 94.95% ± 0.08% F1; seed 42: 94.82% accuracy, 95.05% F1) while lowering model-only inference latency to 1.67 ± 0.06 ms per 1,000 queries. Furthermore, evaluating an uncertainty-gated cascade demonstrates that a zero-network lexical-only model (89.68% accuracy, 90.04% F1) resolves 64.3% of queries purely in-memory with 97.78% accuracy, preserving 94.57% overall pipeline accuracy while cutting external network queries by 64.3%, establishing an empirically validated tiered defense for high-throughput perimeter triage.",
        body_style
    ))
    story.append(Paragraph(
        "Future work will explore online adaptive learning for concept drift, character-level embeddings for IDN homograph detection, and open-source browser and DNS gateway extensions.",
        body_style
    ))
    
    # Data & Code Availability Section (Restored!)
    story.append(Paragraph("DATA AND CODE AVAILABILITY", sec_heading))
    story.append(Paragraph(
        "To ensure reproducibility and open scientific evaluation, all source code, preprocessing scripts, model training routines, feature ranking pipelines, and serialized experiment data are available in the project repository at: <font color='#0000ee'><u>https://github.com/tanaychess/PhishingURLDetetctor</u></font>.",
        body_style
    ))
    
    # Acknowledgments & References
    story.append(Paragraph("ACKNOWLEDGMENT", sec_heading))
    story.append(Paragraph(
        "The author acknowledges the Department of Computer Science, Bhonsala Military College, for providing research infrastructure and computational resources for this investigation.",
        body_style
    ))
    
    story.append(Paragraph("REFERENCES", sec_heading))
    refs = [
        "[1] Anti-Phishing Working Group (APWG), 'Phishing Activity Trends Report, 4th Quarter 2023,' APWG, Tech. Rep., 2023.",
        "[2] Verizon Business, '2024 Data Breach Investigations Report (DBIR),' Verizon, Tech. Rep., 2024.",
        "[3] D. Sahoo, C. Liu, and S. C. H. Hoi, 'Malicious URL detection using machine learning: A survey,' <i>arXiv:1701.07179</i>, 2017.",
        "[4] R. S. Rao and A. R. Pais, 'Detection of phishing websites using an efficient feature-based machine learning framework,' <i>Neural Comput. & Appl.</i>, vol. 31, no. 8, pp. 3851-3873, 2019.",
        "[5] A. Hannousse and S. Yahiouche, 'Towards benchmark datasets for machine learning based website phishing detection: An experimental study,' <i>Eng. Appl. Artif. Intell.</i>, vol. 104, p. 104347, 2021.",
        "[6] S. Marchal et al., 'Off-the-hook: An efficient and usable client-side phishing prevention application,' <i>IEEE Trans. Comput.</i>, vol. 66, no. 10, pp. 1717-1733, 2017.",
        "[7] O. K. Sahingoz, E. Buber, O. Demir, and B. Diri, 'Machine learning based phishing detection from URLs,' <i>Expert Syst. Appl.</i>, vol. 117, pp. 345-357, 2019.",
        "[8] M. Babagoli, M. P. Aghababa, and V. Solouk, 'Heuristic nonlinear regression strategy for detecting phishing websites,' <i>Soft Comput.</i>, vol. 23, pp. 4315-4327, 2019.",
        "[9] C. Opara, B. Wei, and Y. Chen, 'HTMLPhish: Enabling phishing web page detection by applying deep learning techniques on HTML analysis,' in <i>Proc. IJCNN</i>, 2020, pp. 1-8.",
        "[10] M. A. Adebowale, K. T. Lwin, and M. A. Hossain, 'Intelligent phishing detection scheme using deep learning algorithms,' <i>J. Enterp. Inf. Manag.</i>, vol. 36, no. 3, pp. 747-766, 2023.",
        "[11] G. Vrbančič, I. Fister Jr, and V. Podgorelec, 'Datasets for phishing websites detection,' <i>Data in Brief</i>, vol. 33, p. 106438, 2020.",
        "[12] T. Chen and C. Guestrin, 'XGBoost: A scalable tree boosting system,' in <i>Proc. ACM SIGKDD</i>, 2016, pp. 785-794.",
        "[13] S. M. Lundberg et al., 'From local explanations to global understanding with explainable AI for trees,' <i>Nature Mach. Intell.</i>, vol. 2, no. 1, pp. 56-67, 2020.",
        "[14] S. M. Lundberg and S.-I. Lee, 'A unified approach to interpreting model predictions,' in <i>NeurIPS</i>, vol. 30, pp. 4765-4774, 2017.",
        "[15] R. M. Mohammad, F. Thabtah, and L. McCluskey, 'Predicting phishing websites based on self-structuring neural network,' <i>Neural Comput. & Appl.</i>, vol. 25, no. 2, pp. 443-458, 2014.",
        "[16] A. Al-Alyan and S. Al-Ahmadi, 'Robust URL phishing detection based on deep learning,' <i>KSII TIIS</i>, vol. 14, no. 7, pp. 2752-2768, 2020.",
        "[17] K. L. Chiew et al., 'A new hybrid ensemble feature selection framework for machine learning-based phishing detection system,' <i>Inf. Sci.</i>, vol. 484, pp. 153-166, 2019.",
        "[18] M. Al-Fayoumi, B. Alhijawi, Q. Abu Al-Haija, and R. Armoush, 'XAI-PhD: Fortifying trust of phishing URL detection empowered by Shapley additive explanations,' <i>iJOE</i>, vol. 20, no. 11, pp. 80-101, 2024.",
        "[19] K. M. M. Uddin et al., 'Explainable machine learning for phishing site detection: A high-efficiency approach using boosting models and SHAP,' <i>J. Eng.</i>, vol. 2025, no. 1, 2025.",
        "[20] M. C. Calzarossa, P. Giudici, and R. Zieni, 'Explainable machine learning for phishing feature detection,' <i>Qual. Reliab. Eng. Int.</i>, vol. 40, no. 1, pp. 362-373, 2024.",
        "[21] T. Kehkashan et al., 'Explainable phishing website detection for secure and sustainable cyber infrastructure,' <i>Sci. Rep.</i>, vol. 15, p. 41751, 2025."
    ]
    for r in refs:
        story.append(Paragraph(r, ref_style))
        
    doc.build(story)
    print(f"Successfully generated clean IEEE manuscript PDF: {output_pdf}")
    print(f"File size: {os.path.getsize(output_pdf) / 1024:.2f} KB")
    
    # Also copy to paper/overleaf/main.pdf
    overleaf_pdf = "paper/overleaf/main.pdf"
    os.makedirs(os.path.dirname(overleaf_pdf), exist_ok=True)
    shutil.copyfile(output_pdf, overleaf_pdf)
    print(f"Copied to Overleaf distribution: {overleaf_pdf}")
    
    # Build Overleaf zip package
    zip_path = "paper/PhishingURLDetetctor_Overleaf.zip"
    overleaf_zip_path = "paper/overleaf/PhishingURLDetetctor_Overleaf.zip"
    overleaf_dir = "paper/overleaf"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(overleaf_dir):
            for file in files:
                if file.endswith(".zip"):
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, overleaf_dir)
                zipf.write(file_path, rel_path)
    shutil.copyfile(zip_path, overleaf_zip_path)
    print(f"Created Overleaf zip bundle: {zip_path} and {overleaf_zip_path}")

if __name__ == "__main__":
    create_ieee_manuscript_pdf()