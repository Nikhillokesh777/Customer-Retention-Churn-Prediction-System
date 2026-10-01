"""
Generate a comprehensive, beautiful, interview-ready PDF guide for the
Customer Retention & Churn Prediction System (Retentio.AI).
Written in simple, clear, plain English without confusing jargon.
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
    PageBreak
)
from reportlab.pdfgen import canvas

# ============================================================
# Numbered Canvas for Running Header & Footer
# ============================================================

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header (pages after cover page)
        if self._pageNumber > 1:
            self.drawString(54, 11 * 72 - 36, "RETENTIO.AI  |  Enterprise Churn Intelligence & Interview Playbook")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.drawString(54, 30, "AI-Powered Customer Retention System  •  Comprehensive Project & Interview Guide")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 30, page_str)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 40, 8.5 * 72 - 54, 40)

        self.restoreState()


# ============================================================
# Build Document Story
# ============================================================

def build_pdf(output_path="Customer_Retention_Churn_System_Interview_Guide.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "SubSectionHeading",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#334155"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    bold_body = ParagraphStyle(
        "BoldBody",
        parent=body_style,
        fontName="Helvetica-Bold"
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        parent=body_style,
        fontName="Helvetica-Oblique",
        textColor=colors.HexColor("#1E1B4B"),
        fontSize=8.5,
        leading=12
    )

    q_style = ParagraphStyle(
        "QuestionStyle",
        parent=body_style,
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    a_style = ParagraphStyle(
        "AnswerStyle",
        parent=body_style,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8
    )

    story = []

    # ---------------------------------------------------------
    # COVER / HEADER
    # ---------------------------------------------------------
    story.append(Paragraph("AI-Powered Customer Retention & Churn System", title_style))
    story.append(Paragraph("Complete Project Architecture, UI Encyclopedia & Interview Preparation Guide", subtitle_style))

    # Badge ribbon table
    badge_data = [[
        Paragraph("<b>Active Model:</b> XGBoost v2.1", body_style),
        Paragraph("<b>Churn Capture (Recall):</b> 72.5%", body_style),
        Paragraph("<b>ROC-AUC Score:</b> 0.846", body_style),
        Paragraph("<b>Status:</b> Production Ready", body_style)
    ]]
    badge_table = Table(badge_data, colWidths=[126, 130, 118, 130])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # SECTION 1: WHAT IS THIS PROJECT?
    # ---------------------------------------------------------
    story.append(Paragraph("1. Executive Summary & Business Problem", h1_style))
    story.append(Paragraph(
        "<b>What is Customer Churn?</b> In any subscription business (like telecom, internet, Netflix, or cloud software), "
        "<b>churn</b> happens when an existing customer cancels their contract or stops paying and goes to a competitor.<br/>"
        "<b>Why is this a big problem?</b> Acquiring a brand-new customer costs <b>5 to 7 times more money</b> in marketing, ads, and sales "
        "than keeping an existing happy customer. If a company loses 25% of its customers every year, it is losing millions of dollars.<br/>"
        "<b>What does this project do?</b> It takes raw telecom account data, runs it through an automated Machine Learning pipeline, "
        "and immediately flags customers who are at high risk of leaving <i>before they actually cancel</i>. It then gives the customer success team "
        "a specific retention playbook (like offering a discount, free tech support, or an annual plan) to convince them to stay.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 2: TOOLS & TECHNOLOGIES USED
    # ---------------------------------------------------------
    story.append(Paragraph("2. Technologies, Tools & Libraries Used", h1_style))
    story.append(Paragraph(
        "Here are all the programming tools and libraries used in this project, explained in plain English:", body_style
    ))

    tools_data = [
        [Paragraph("<b>Tool / Library</b>", bold_body), Paragraph("<b>What it is</b>", bold_body), Paragraph("<b>Why we used it in this project</b>", bold_body)],
        [
            Paragraph("<b>Python 3.9+</b>", body_style),
            Paragraph("Core programming language", body_style),
            Paragraph("Simple, clean syntax with the best ecosystem for data science and AI.", body_style)
        ],
        [
            Paragraph("<b>Pandas</b>", body_style),
            Paragraph("Data manipulation library", body_style),
            Paragraph("Loads the CSV dataset, handles missing numbers, and structures data into clean tables.", body_style)
        ],
        [
            Paragraph("<b>NumPy</b>", body_style),
            Paragraph("Numerical math library", body_style),
            Paragraph("Fast calculations, rounding numbers, and handling arrays of probabilities.", body_style)
        ],
        [
            Paragraph("<b>Scikit-learn</b>", body_style),
            Paragraph("Machine learning toolkit", body_style),
            Paragraph("Provides preprocessors (StandardScaler, OneHotEncoder, SimpleImputer) and creates the unified Pipeline.", body_style)
        ],
        [
            Paragraph("<b>XGBoost</b>", body_style),
            Paragraph("Gradient boosted tree library", body_style),
            Paragraph("Our champion classification algorithm. Delivers high accuracy and handles non-linear customer patterns.", body_style)
        ],
        [
            Paragraph("<b>Streamlit</b>", body_style),
            Paragraph("Web application framework", body_style),
            Paragraph("Builds a clean, real-time web dashboard entirely in Python without needing React or complex frontend code.", body_style)
        ],
        [
            Paragraph("<b>Plotly</b>", body_style),
            Paragraph("Interactive visualization engine", body_style),
            Paragraph("Draws interactive circular risk dials, probability bar charts, and pie charts with clean dark-mode visuals.", body_style)
        ],
        [
            Paragraph("<b>Joblib</b>", body_style),
            Paragraph("Object serialization tool", body_style),
            Paragraph("Saves the fully trained model to a file (churn_pipeline.pkl) so we can load and use it in milliseconds.", body_style)
        ],
        [
            Paragraph("<b>Pytest</b>", body_style),
            Paragraph("Automated testing framework", body_style),
            Paragraph("Runs automated unit tests to guarantee that input shapes, risk thresholds, and pipeline functions work without bugs.", body_style)
        ]
    ]
    tools_table = Table(tools_data, colWidths=[100, 130, 274])
    tools_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tools_table)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # SECTION 3: MACHINE LEARNING MODELS & COMPARISON
    # ---------------------------------------------------------
    story.append(Paragraph("3. Machine Learning Models Used & Why We Picked XGBoost", h1_style))
    story.append(Paragraph(
        "During model experimentation, three different machine learning classifiers were evaluated on the IBM Telco dataset "
        "using an 80/20 stratified train-test split:", body_style
    ))

    models_data = [
        [Paragraph("<b>Model Name</b>", bold_body), Paragraph("<b>How it Works</b>", bold_body), Paragraph("<b>Accuracy</b>", bold_body), Paragraph("<b>Churn Recall</b>", bold_body), Paragraph("<b>Role in Project</b>", bold_body)],
        [
            Paragraph("<b>1. Logistic Regression</b>", body_style),
            Paragraph("Draws a straight linear decision boundary between staying and leaving.", body_style),
            Paragraph("~80%", body_style),
            Paragraph("~55%", body_style),
            Paragraph("Baseline model to test minimum performance.", body_style)
        ],
        [
            Paragraph("<b>2. Random Forest</b>", body_style),
            Paragraph("Builds a forest of 100 decision trees and votes on the final outcome.", body_style),
            Paragraph("~79%", body_style),
            Paragraph("~48%", body_style),
            Paragraph("Ensemble model; suffered from low recall without class weighting.", body_style)
        ],
        [
            Paragraph("<b>3. Tuned XGBoost (Winner)</b>", body_style),
            Paragraph("Gradient boosted trees that train sequentially, each tree correcting the errors of earlier trees. Uses positive class weighting.", body_style),
            Paragraph("<b>76.9%</b>", body_style),
            Paragraph("<b>72.5%</b>", body_style),
            Paragraph("<b>Active Production Pipeline.</b> Catches almost 3 out of 4 churners.", body_style)
        ]
    ]
    models_table = Table(models_data, colWidths=[100, 154, 60, 75, 115])
    models_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(models_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Important Concept — Why is Recall more important than Accuracy here?</b><br/>"
        "In this dataset, ~73% of customers stay and ~27% churn. If a lazy model simply predicted <i>'Nobody will ever leave'</i>, "
        "its accuracy would be 73%! But it would catch <b>zero</b> churning customers and the company would lose all its revenue.<br/>"
        "<b>Recall (Churn Capture Rate)</b> measures: <i>'Out of all customers who actually left, how many did our AI find in advance?'</i> "
        "By setting <code>scale_pos_weight=2.0</code> in XGBoost, we boosted churn recall from <b>48% to 72.5%</b>, saving millions in business value.",
        body_style
    ))
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # SECTION 4: COMPLETE VISUAL INTERFACE ENCYCLOPEDIA
    # ---------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("4. Interface Encyclopedia: Every Single Item Explained", h1_style))
    story.append(Paragraph(
        "Here is a complete, plain-English reference explaining every single label, button, and slider visible in the Retentio.AI interface:",
        body_style
    ))

    ui_data = [
        [Paragraph("<b>Interface Item</b>", bold_body), Paragraph("<b>Category</b>", bold_body), Paragraph("<b>Simple Plain-English Meaning & Business Importance</b>", bold_body)],
        
        # Header items
        [
            Paragraph("<b>RETENTIO.AI Platform</b>", body_style),
            Paragraph("Header Banner", body_style),
            Paragraph("The brand title of our enterprise churn intelligence system.", body_style)
        ],
        [
            Paragraph("<b>Production XGBoost v2.1</b>", body_style),
            Paragraph("System Badge", body_style),
            Paragraph("Displays the current active ML model powering real-time inference.", body_style)
        ],
        [
            Paragraph("<b>72.5% Churn Recall</b>", body_style),
            Paragraph("System Metric", body_style),
            Paragraph("Tells executive leaders that the model catches ~73% of all at-risk customers.", body_style)
        ],
        [
            Paragraph("<b>Automated Counterfactual Optimization</b>", body_style),
            Paragraph("Feature Tag", body_style),
            Paragraph("Indicates that the system can test 'what-if' solutions to lower customer risk.", body_style)
        ],
        [
            Paragraph("<b>AUC: 0.846</b>", body_style),
            Paragraph("Quality Metric", body_style),
            Paragraph("Area Under ROC Curve. A score from 0.5 to 1.0 showing how well the model separates churners from loyal users. 0.846 is excellent.", body_style)
        ],

        # 4 Main Tabs
        [
            Paragraph("<b>👤 Subscriber Risk Diagnostic</b>", body_style),
            Paragraph("Main Tab 1", body_style),
            Paragraph("Analyzes 1 single customer account right now. Shows their risk dial, root causes for leaving, and a custom action plan.", body_style)
        ],
        [
            Paragraph("<b>🔮 What-If Retention Simulator</b>", body_style),
            Paragraph("Main Tab 2", body_style),
            Paragraph("Lets you simulate changes (like giving them a 1-year contract or tech support) and shows how much their churn risk drops.", body_style)
        ],
        [
            Paragraph("<b>📁 Batch Portfolio Intelligence</b>", body_style),
            Paragraph("Main Tab 3", body_style),
            Paragraph("Upload a CSV file containing 5,000+ customers at once. Scores everyone in seconds and exports a prioritized call list.", body_style)
        ],
        [
            Paragraph("<b>💰 Strategic ROI & ARR Preserved</b>", body_style),
            Paragraph("Main Tab 4", body_style),
            Paragraph("A financial calculator that converts AI predictions into dollar amounts of revenue saved and return on campaign spend.", body_style)
        ],

        # Demographic Inputs
        [
            Paragraph("<b>Gender</b> (Male / Female)", body_style),
            Paragraph("Demographics", body_style),
            Paragraph("Customer gender. Kept in IBM dataset for demographic fairness evaluation.", body_style)
        ],
        [
            Paragraph("<b>Senior Citizen</b> (Yes / No)", body_style),
            Paragraph("Demographics", body_style),
            Paragraph("Customers age 65+. Often on fixed pensions or require simpler, clearer technology.", body_style)
        ],
        [
            Paragraph("<b>Partner on Account</b> (Yes / No)", body_style),
            Paragraph("Demographics", body_style),
            Paragraph("Whether the customer has a spouse/partner. Accounts with partners have higher stickiness and churn less.", body_style)
        ],
        [
            Paragraph("<b>Dependents Covered</b> (Yes / No)", body_style),
            Paragraph("Demographics", body_style),
            Paragraph("Whether children or family are on the plan. Family accounts are much harder to cancel, lowering churn.", body_style)
        ],

        # Contract & Financials
        [
            Paragraph("<b>Account Tenure (months)</b>", body_style),
            Paragraph("Contract", body_style),
            Paragraph("How many months the customer has been with the company. First 6 months are highest risk; customers past 24 months are loyal.", body_style)
        ],
        [
            Paragraph("<b>Contract Commitment</b>", body_style),
            Paragraph("Contract", body_style),
            Paragraph("<b>Month-to-month:</b> Highest churn (no lock-in).<br/><b>One year / Two year:</b> Low churn (customer committed for discount).", body_style)
        ],
        [
            Paragraph("<b>Paperless Billing</b> (Yes / No)", body_style),
            Paragraph("Billing", body_style),
            Paragraph("Customers receiving email/app bills versus traditional printed paper letters.", body_style)
        ],
        [
            Paragraph("<b>Billing Channel</b>", body_style),
            Paragraph("Payment", body_style),
            Paragraph("<b>Electronic check:</b> High friction & highest churn.<br/><b>Bank transfer / Credit card auto-pay:</b> Automated, hands-off, lowest churn.", body_style)
        ],
        [
            Paragraph("<b>Monthly ARPU ($)</b>", body_style),
            Paragraph("Financials", body_style),
            Paragraph("Average Revenue Per User per month. High monthly spend with month-to-month contracts makes customers look for cheaper competitors.", body_style)
        ],
        [
            Paragraph("<b>Lifetime Total Charges ($)</b>", body_style),
            Paragraph("Financials", body_style),
            Paragraph("Total revenue collected over customer lifespan (roughly Tenure multiplied by Monthly Spend).", body_style)
        ],

        # Services
        [
            Paragraph("<b>Voice Service</b> (Yes / No)", body_style),
            Paragraph("Service", body_style),
            Paragraph("Traditional telephone dial tone connection.", body_style)
        ],
        [
            Paragraph("<b>Multi-Line Option</b>", body_style),
            Paragraph("Service", body_style),
            Paragraph("Multiple telephone numbers on the same account for household members.", body_style)
        ],
        [
            Paragraph("<b>Broadband Tier</b>", body_style),
            Paragraph("Internet", body_style),
            Paragraph("<b>Fiber optic:</b> High speed, high cost (high churn if unsupported).<br/><b>DSL:</b> Copper wire, lower speed.<br/><b>No:</b> Phone only.", body_style)
        ],
        [
            Paragraph("<b>Cybersecurity Defense</b>", body_style),
            Paragraph("Value-Add Service", body_style),
            Paragraph("Antivirus, firewalls, and spam protection. Adds stickiness when enabled.", body_style)
        ],
        [
            Paragraph("<b>Cloud Backup</b>", body_style),
            Paragraph("Value-Add Service", body_style),
            Paragraph("Online cloud storage for customer photos and personal files.", body_style)
        ],
        [
            Paragraph("<b>Hardware Protection</b>", body_style),
            Paragraph("Value-Add Service", body_style),
            Paragraph("Insurance warranty covering damaged Wi-Fi routers and cable set-top boxes.", body_style)
        ],
        [
            Paragraph("<b>VIP Tech Concierge</b>", body_style),
            Paragraph("Support", body_style),
            Paragraph("Dedicated premium tech support line. <b>Massive churn protector:</b> Customers without tech support leave when things break!", body_style)
        ],
        [
            Paragraph("<b>IPTV & Movie Streaming</b>", body_style),
            Paragraph("Entertainment", body_style),
            Paragraph("Internet television packages and on-demand video entertainment streaming.", body_style)
        ]
    ]

    ui_table = Table(ui_data, colWidths=[130, 94, 280])
    ui_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(ui_table)
    story.append(Spacer(1, 14))

    # ---------------------------------------------------------
    # SECTION 5: TOP 15 INTERVIEW QUESTIONS & ANSWERS
    # ---------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("5. Top 15 Must-Know Interview Questions & Answers", h1_style))
    story.append(Paragraph(
        "These questions cover machine learning, data engineering, product design, and business value. "
        "Answers are written in confident, straightforward language that interviewers love to hear.",
        body_style
    ))

    qa_list = [
        (
            "Q1: Can you give a 60-second elevator pitch of your customer churn project?",
            "<b>Answer:</b> I built an end-to-end, class-balanced machine learning system called <b>Retentio.AI</b>. "
            "It predicts customer churn for subscription telecom providers. In telecom, acquiring a customer costs 5 to 7 times more "
            "than keeping one. My system uses a tuned XGBoost pipeline with positive-class weighting that achieves a <b>72.5% churn recall</b> "
            "and <b>0.846 ROC-AUC</b>. Instead of just giving a black-box probability, the system diagnoses customer-specific risk drivers "
            "(like month-to-month contracts or lack of tech support), features a counterfactual 'What-If' simulator to test retention offers in real time, "
            "and calculates net annual recurring revenue saved."
        ),
        (
            "Q2: Why did you choose the IBM Telco Customer Churn dataset?",
            "<b>Answer:</b> It is the industry-standard benchmark for subscription attrition modeling. It contains 7,043 real-world customer records "
            "spanning demographics, contract terms, billing channels, and subscribed digital services. It has realistic real-world challenges: "
            "an imbalanced class distribution (~26.5% churners), missing blank values in TotalCharges, and mixed numeric/categorical data types."
        ),
        (
            "Q3: What was the class imbalance problem in this dataset, and how did you resolve it?",
            "<b>Answer:</b> In the dataset, only ~27% of customers churn while ~73% stay. A standard baseline model will easily achieve 79% accuracy "
            "simply by predicting that everyone stays, but its churn recall is terrible (~48%)—meaning it misses more than half the leaving customers. "
            "I solved this by applying positive class weighting (<code>scale_pos_weight=2.0</code>) in XGBoost. This penalizes the model twice as heavily "
            "for missing a churner, lifting churn capture rate to <b>72.5%</b>."
        ),
        (
            "Q4: Why is Recall more important than Accuracy for churn prediction?",
            "<b>Answer:</b> Because the business cost of a <b>False Negative</b> (a customer leaves without us knowing, losing thousands in lifetime value) "
            "is drastically higher than a <b>False Positive</b> (we reach out to a loyal customer and offer them a small discount or perk). "
            "Maximizing Recall ensures we capture as many at-risk dollars as possible."
        ),
        (
            "Q5: Why did you select XGBoost over Random Forest or Logistic Regression?",
            "<b>Answer:</b> Logistic Regression is too simple to capture non-linear interactions (like high monthly spend combined with lack of tech support). "
            "Random Forest was solid, but its serialized file size was massive (19.5 MB) and its recall remained under 50%. "
            "Tuned XGBoost gave us higher ROC-AUC (0.846), higher F1-score (0.624), 72.5% recall, and serialized into a lightweight 150 KB file."
        ),
        (
            "Q6: How did you prevent data leakage during preprocessing?",
            "<b>Answer:</b> I built a strict scikit-learn <code>ColumnTransformer</code> inside an end-to-end <code>Pipeline</code>. "
            "Imputation (median filling for TotalCharges) and StandardScaling are calculated <i>strictly on the training split</i> and only applied "
            "to test/production splits. Categorical one-hot encoding uses <code>handle_unknown='ignore'</code> to prevent unseen production categories from crashing the app."
        ),
        (
            "Q7: What are the top 3 drivers of customer churn according to your model?",
            "<b>Answer:</b> 1) <b>Contract Type:</b> Month-to-month customers churn at 5x the rate of 1-year or 2-year contracted users.<br/>"
            "2) <b>Tenure:</b> Customers in their first 6 months have the highest attrition velocity.<br/>"
            "3) <b>Payment Channel:</b> Customers paying with manual Electronic Checks churn far more than those on automated Credit Card or Bank Auto-Pay."
        ),
        (
            "Q8: Did you find any silent data bugs when integrating the model into the frontend?",
            "<b>Answer:</b> Yes! In the raw CSV dataset, <code>SeniorCitizen</code> is stored as integers <code>0</code> or <code>1</code>. "
            "Initially, the UI was passing strings <code>'Yes'</code> or <code>'No'</code>. Because the OneHotEncoder was fitted on <code>[0, 1]</code>, "
            "it treated <code>'Yes'</code> as an unknown category and silently zeroed out the feature during inference! I caught this through inspection "
            "and fixed the frontend to strictly pass integers <code>1</code> and <code>0</code>."
        ),
        (
            "Q9: What is the 'What-If Retention Simulator' tab, and why is it valuable?",
            "<b>Answer:</b> It implements <b>Counterfactual Inference</b>. Most AI tools only tell you what is broken; this tool lets customer success reps "
            "simulate the solution. A rep can select: <i>'What if we switch this month-to-month user to a 1-year plan and add free tech support?'</i> "
            "The model immediately re-scores the customer, showing a drop from 92% risk to 60% risk. This guides the exact concession to offer."
        ),
        (
            "Q10: How does your recommendation engine work?",
            "<b>Answer:</b> It couples risk classification with customer-specific feature analysis. If a high-risk user is on Month-to-Month, it suggests "
            "an annual contract 15% discount. If they lack tech support on fiber optic, it suggests complimentary 3-month VIP support. If they use electronic checks, "
            "it suggests a $10 bill credit for auto-pay enrollment."
        ),
        (
            "Q11: How does the Batch Portfolio Scoring feature work?",
            "<b>Answer:</b> In production, companies have thousands of customers. This tab allows uploading a CSV with 5,000+ accounts. "
            "The pipeline vectorizes and scores the entire cohort simultaneously, tallies total Annual Recurring Revenue (ARR) at risk, "
            "and generates an exported CSV ranked by highest churn probability for outbound call campaigns."
        ),
        (
            "Q12: How do you measure business ROI from this machine learning model?",
            "<b>Answer:</b> I built a Strategic ROI calculator in the app. If a company has 7,000 subscribers with a 26.5% baseline churn rate "
            "and our retention campaign successfully rescues 25% of predicted churners, the company preserves <b>~$350,000 in gross annual revenue</b>. "
            "Even after paying $30 per retention incentive, the net benefit is over <b>$330,000</b>, delivering an <b>8x+ ROI</b>."
        ),
        (
            "Q13: How did you ensure software quality and reliability?",
            "<b>Answer:</b> I added an automated test suite with <code>pytest</code> covering pipeline loading, probability boundary checks [0.0, 1.0], "
            "proper integer encoding for SeniorCitizen, and recommendation threshold logic. All 6 tests pass cleanly."
        ),
        (
            "Q14: How would you deploy this system into an enterprise cloud architecture?",
            "<b>Answer:</b> I would wrap the <code>churn_pipeline.pkl</code> inside a <b>FastAPI</b> REST service containerized with <b>Docker</b>. "
            "It would be deployed on AWS ECS or Google Cloud Run behind an API Gateway. The Streamlit dashboard or React frontend would call <code>POST /predict</code> "
            "for real-time scoring and <code>POST /batch-predict</code> triggered by Apache Airflow for nightly batch scoring."
        ),
        (
            "Q15: How would you monitor this model once it is live in production?",
            "<b>Answer:</b> I would monitor two key things: 1) <b>Data Drift:</b> Check if customer feature distributions change over time (e.g. inflation causing price jumps) "
            "using Kolmogorov-Smirnov tests or Evidently AI. 2) <b>Concept Drift:</b> Compare predicted churn probability distributions against actual churn rates "
            "every quarter to trigger automated pipeline retraining."
        )
    ]

    for q, a in qa_list:
        story.append(Paragraph(q, q_style))
        story.append(Paragraph(a, a_style))

    # ---------------------------------------------------------
    # BUILD PDF
    # ---------------------------------------------------------
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {output_path}")


if __name__ == "__main__":
    out_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "Customer_Retention_Churn_System_Interview_Guide.pdf"
    )
    build_pdf(out_file)
