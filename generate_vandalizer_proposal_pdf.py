from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT_FILE = "Vandalizer_Project_Proposal.pdf"


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="Vandalizer Project Proposal",
        author="Zeyad Yousef Mohamed Abd Elfadeil Shaban",
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CenterSmall",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontName="Helvetica",
            fontSize=10,
            leading=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CenterTitle",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=14,
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubSection",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=12.5,
            spaceBefore=5,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyIndent",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            leftIndent=10,
            spaceAfter=3,
        )
    )

    def p(text, style="Body"):
        return Paragraph(text, styles[style])

    def tp(text, bold=False):
        if bold:
            return Paragraph(f"<b>{text}</b>", styles["Body"])
        return Paragraph(text, styles["Body"])

    story = []

    story.append(p("College of Engineering and Technology", "CenterSmall"))
    story.append(p("Arab Academy for Science, Technology and Maritime Transport", "CenterSmall"))
    story.append(p("Computer Engineering Department", "CenterSmall"))
    story.append(Spacer(1, 8))
    story.append(p("PROJECT PROPOSAL", "CenterTitle"))
    story.append(p("Web Engineering", "CenterSmall"))
    story.append(Spacer(1, 6))
    story.append(p("Vandalizer", "CenterTitle"))
    story.append(Spacer(1, 2))
    story.append(p("<b>Supervised By</b>", "CenterSmall"))
    story.append(p("Dr. Amr Fahmy", "CenterSmall"))
    story.append(Spacer(1, 2))
    story.append(p("<b>Course</b>", "CenterSmall"))
    story.append(p("Web Engineering", "CenterSmall"))
    story.append(Spacer(1, 2))
    story.append(p("<b>Semester</b>", "CenterSmall"))
    story.append(p("Semester 8", "CenterSmall"))
    story.append(Spacer(1, 10))

    story.append(p("1. Project Team", "Section"))
    team_data = [
        ["Team Members", "Full Name", "College ID"],
        ["Member 1", "Zeyad Yousef Mohamed Abd Elfadeil Shaban", "221004741"],
        ["Member 2", "Ahmed Tamer Mohamed Amin Shaaban", "221005802"],
    ]
    team_table = Table(
        [[tp(cell, bold=(r == 0)) for cell in row] for r, row in enumerate(team_data)],
        colWidths=[28 * mm, 110 * mm, 36 * mm],
        hAlign="LEFT",
    )
    team_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9E2F3")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("GRID", (0, 0), (-1, -1), 0.6, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FC")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(team_table)

    story.append(p("2. Introduction & Problem Statement", "Section"))
    story.append(p("2.1 Background", "SubSection"))
    story.append(
        p(
            "Image editing has become an essential part of social media, marketing, design, and everyday digital communication. "
            "However, most professional editing tools are still complex for non-expert users. Simple tasks such as removing an "
            "object, replacing part of an image, or editing based on a text prompt often require manual selection, masks, layers, "
            "and technical knowledge.",
        )
    )
    story.append(
        p(
            "Vandalizer is an AI-based image editing web application designed to simplify this process. Instead of hiding the "
            "editing workflow behind a single opaque action, the system exposes the major AI stages so the user can understand "
            "how an image is detected, segmented, and edited.",
        )
    )

    story.append(p("2.2 Problem Statement", "SubSection"))
    story.append(
        p(
            "Many users want to quickly edit an image using natural language, but existing tools are either too manual or too abstract. "
            "This project addresses how to provide a simple web interface that allows a user to describe an edit in text while the system "
            "automatically detects the target object, segments it, and replaces it using AI-powered inpainting.",
        )
    )

    story.append(p("2.3 Motivation", "SubSection"))
    story.append(
        p(
            "The motivation behind Vandalizer is to make AI image editing easier for regular users and more understandable for students and "
            "beginners. The project also has educational value because it demonstrates how modern vision-language models, segmentation models, "
            "and diffusion models work together in a practical web application.",
        )
    )

    story.append(p("3. Objectives", "Section"))
    story.append(p("By the end of this project, the team will have achieved the following measurable goals:", "Body"))
    objectives = [
        "Build a web application that accepts an image and a text prompt for editing.",
        "Automatically detect the object described in the prompt inside the uploaded image.",
        "Segment the detected object accurately using an AI segmentation model.",
        "Replace or edit the selected region using a diffusion-based inpainting model.",
        "Present the editing pipeline in a clear and understandable frontend for simple users.",
    ]
    story.append(
        ListFlowable(
            [ListItem(Paragraph(obj, styles["Body"])) for obj in objectives],
            bulletType="bullet",
            start=None,
            leftIndent=14,
        )
    )

    story.append(p("4. Literature Review", "Section"))
    story.append(
        p(
            "This project is based on several important ideas in modern computer vision and generative AI."
        )
    )
    lit_points = [
        "<b>Grounded object detection:</b> Models such as Grounding DINO and OWL-V2 connect text descriptions to image regions and help locate objects using language.",
        "<b>Segmentation:</b> SAM and MobileSAM are used to separate the selected object from the background with pixel-level precision.",
        "<b>Transformer architectures:</b> Transformer-based models are important for combining visual and textual information.",
        "<b>Diffusion-based inpainting:</b> Stable Diffusion XL Inpaint and similar models generate realistic replacements in masked areas.",
        "<b>Image restoration methods:</b> LaMa-style inpainting methods provide useful background for understanding image completion and reconstruction.",
    ]
    story.append(
        ListFlowable(
            [ListItem(Paragraph(item, styles["Body"])) for item in lit_points],
            bulletType="bullet",
            leftIndent=14,
        )
    )

    story.append(p("5. Proposed Methodology", "Section"))
    story.append(p("5.1 System Overview", "SubSection"))
    story.append(
        p(
            "Vandalizer is a client-server web application. The user uploads an image through the React frontend and enters a text prompt describing "
            "the object to edit. The FastAPI backend receives the image, creates a job ID, and stores the file on the server. A Celery worker connected "
            "to Redis runs the AI pipeline asynchronously."
        )
    )
    story.append(
        p(
            "The pipeline works in three main stages: object detection from the text prompt, segmentation of the detected object, and inpainting or "
            "replacement of the segmented area. The frontend polls the server and displays the detection boxes, segmentation mask, and final edited image."
        )
    )

    story.append(p("5.2 Application Components", "SubSection"))
    comp_data = [
        ["Component", "Description"],
        ["React Frontend", "User interface for upload, prompt entry, status polling, and result display."],
        ["FastAPI Backend", "Handles upload, job creation, status checking, and process endpoints."],
        ["Celery Worker", "Executes model inference asynchronously so the interface remains responsive."],
        ["Redis", "Acts as the message broker and result backend for Celery."],
        ["Object Detection Model", "Text-grounded detector that finds the target object in the image."],
        ["Segmentation Model", "MobileSAM or SAM used to generate a precise object mask."],
        ["Inpainting Model", "Stable Diffusion XL Inpaint used to generate the edited output."],
    ]
    comp_table = Table(
        [[tp(cell, bold=(r == 0)) for cell in row] for r, row in enumerate(comp_data)],
        colWidths=[42 * mm, 132 * mm],
        hAlign="LEFT",
    )
    comp_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAD3")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.6, colors.black),
                ("FONTSIZE", (0, 0), (-1, -1), 9.2),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FC")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(comp_table)

    story.append(p("5.3 Software Architecture", "SubSection"))
    story.append(
        p(
            "The software uses a modular architecture with a separate frontend and backend. The frontend is built with React and Vite, while the "
            "backend is built with FastAPI and Celery. Redis supports asynchronous task execution. The AI models are loaded through a service layer "
            "so they can be reused efficiently across requests."
        )
    )
    story.append(
        p(
            "This architecture is suitable for separating user interaction from heavy model inference, which improves maintainability and keeps the "
            "application responsive."
        )
    )

    story.append(p("5.4 System Flow", "SubSection"))
    flow_points = [
        "The user uploads an image through the frontend.",
        "The backend saves the image and generates a job ID.",
        "The user enters a text prompt describing the object to edit.",
        "The detector identifies the object region using text-guided detection.",
        "The segmentation model creates a mask for the detected object.",
        "The inpainting model replaces the masked region using the prompt.",
        "The frontend polls the server and displays the result when processing is complete.",
    ]
    story.append(
        ListFlowable(
            [ListItem(Paragraph(point, styles["Body"])) for point in flow_points],
            bulletType="bullet",
            leftIndent=14,
        )
    )

    story.append(p("6. Development Timeline", "Section"))
    story.append(
        p(
            "The project will be completed over 6 to 7 weeks according to the following plan:"
        )
    )
    timeline_data = [
        ["Week", "Phase / Task", "Deliverable"],
        ["9", "Prepare or train the AI model pipeline and test initial inference", "Working detection / segmentation / inpainting base"],
        ["10", "Set up the backend with FastAPI, Redis, and Celery", "Functional backend APIs and async processing"],
        ["11", "Set up the frontend with React and connect the upload flow", "Basic user interface for uploading images and prompts"],
        ["12", "Ensure seamless frontend-backend integration and fine-tune the model pipeline", "End-to-end working system"],
        ["13", "Improve the frontend design and make the interface clean and user-friendly", "Polished UI"],
        ["14", "Deploy the application and prepare production settings", "Deployed version"],
        ["15", "Final testing, bug fixing, and presentation preparation", "Final submission"],
    ]
    timeline_table = Table(
        [
            [tp(cell, bold=(r == 0)) for cell in row]
            for r, row in enumerate(timeline_data)
        ],
        colWidths=[16 * mm, 90 * mm, 68 * mm],
        hAlign="LEFT",
    )
    timeline_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#FCE4D6")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.6, colors.black),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("LEADING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FC")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(timeline_table)

    def draw_footer(canvas, doc):
        canvas.saveState()
        width, height = A4
        canvas.setStrokeColor(colors.HexColor("#808080"))
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, 12 * mm, width - doc.rightMargin, 12 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawRightString(width - doc.rightMargin, 8 * mm, f"Page {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT_FILE)
