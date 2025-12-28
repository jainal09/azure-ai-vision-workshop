"""
Generate Azure AI Vision Workshop PowerPoint from template.
"""

from __future__ import annotations

import shutil

from pptx import Presentation
from pptx.util import Pt


TEMPLATE_PATH = "/Users/jainal09/Downloads/MS_SA_Template_Final.pptx"
OUTPUT_PATH = "/Users/jainal09/msa-q4-25/Azure_AI_Vision_Workshop.pptx"


def clear_slides(prs: Presentation, keep_first_n: int = 0) -> None:
    """Remove all slides except the first n."""
    slide_ids = [slide.slide_id for slide in prs.slides]
    for i, slide_id in enumerate(slide_ids):
        if i >= keep_first_n:
            rId = prs.slides._sldIdLst[keep_first_n].rId
            prs.part.drop_rel(rId)
            del prs.slides._sldIdLst[keep_first_n]


def get_layout_index(layout_type: str) -> int:
    """Map layout type to template layout index."""
    layout_map = {
        "title": 3,
        "content": 6,
        "content_alt": 7,
        "content_alt2": 8,
        "demo": 19,
        "section": 21,
        "closing": 28,
    }
    return layout_map.get(layout_type, 6)


def format_text_frame(text_frame, content: str) -> None:
    """Format text frame with proper styling - MAX 6 lines."""
    text_frame.clear()
    lines = content.strip().split("\n")

    for i, line in enumerate(lines):
        if i == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()

        stripped = line.strip()

        if not stripped:
            p.text = ""
            p.space_after = Pt(8)
            continue

        is_section_header = stripped.endswith(":") and len(stripped) < 50
        is_bullet = stripped.startswith("-") or stripped.startswith("•")

        if is_bullet:
            p.text = "• " + stripped.lstrip("-•· ")
            p.font.size = Pt(20)
            p.space_before = Pt(4)
            p.space_after = Pt(4)
        elif is_section_header:
            p.text = stripped
            p.font.bold = True
            p.font.size = Pt(22)
            p.space_before = Pt(12)
            p.space_after = Pt(4)
        else:
            p.text = stripped
            p.font.size = Pt(20)
            p.space_before = Pt(4)
            p.space_after = Pt(4)


def add_slide(prs: Presentation, slide_data: dict) -> None:
    """Add a slide with the specified layout and content."""
    layout_idx = get_layout_index(slide_data["layout"])
    layout = prs.slide_layouts[layout_idx]
    slide = prs.slides.add_slide(layout)

    if slide.shapes.title:
        slide.shapes.title.text = slide_data.get("title", "")

    if slide_data["layout"] in ["content", "content_alt", "content_alt2"]:
        for shape in slide.placeholders:
            if shape.placeholder_format.type == 2:
                format_text_frame(shape.text_frame, slide_data.get("content", ""))
                break

    elif slide_data["layout"] == "demo":
        for shape in slide.placeholders:
            if shape.placeholder_format.type == 2:
                shape.text = slide_data.get("subtitle", "")
                for p in shape.text_frame.paragraphs:
                    p.font.size = Pt(28)
                break

    elif slide_data["layout"] == "title":
        for shape in slide.placeholders:
            if shape.placeholder_format.type == 2:
                shape.text = slide_data.get("subtitle", "")
                for p in shape.text_frame.paragraphs:
                    p.font.size = Pt(28)
                break


def generate_presentation() -> None:
    """Generate the workshop presentation from template."""
    print(f"Loading template: {TEMPLATE_PATH}")
    shutil.copy(TEMPLATE_PATH, OUTPUT_PATH)
    prs = Presentation(OUTPUT_PATH)

    print(f"Template has {len(prs.slides)} existing slides")
    clear_slides(prs, keep_first_n=1)

    # SLIDES - Keep each slide to MAX 5-6 bullet points
    slides = [
        {
            "layout": "title",
            "title": "Build an AI-Powered Image Analyzer",
            "subtitle": "Azure AI Vision Workshop",
        },
        {
            "layout": "content",
            "title": "About Me",
            "content": """Jainal Gosaliya

Beta Microsoft Learn Student Ambassador

Masters in Software Engineering Systems
Northeastern University

Passionate about Python, AI & Azure!""",
        },
        {
            "layout": "content_alt",
            "title": "Agenda",
            "content": """Today's Plan:
- What is Azure AI Vision?
- Key Features
- Real-World Use Cases
- Live Demo
- Q&A""",
        },
        {
            "layout": "content",
            "title": "What is Azure AI Vision?",
            "content": """Cloud-based AI for image analysis

Part of Microsoft Azure AI Services

Capabilities:
- Extract text from images (OCR)
- Detect objects in photos
- Generate image descriptions
- Analyze image content""",
        },
        {
            "layout": "content_alt",
            "title": "Pricing",
            "content": """Free Tier Available!

- 20 API calls per minute
- 5,000 calls per month
- No credit card required

Perfect for learning & prototyping""",
        },
        {
            "layout": "content",
            "title": "Key Features",
            "content": """OCR (Read):
- Extract printed & handwritten text

Image Captions:
- "A dog playing in the park"

Object Detection:
- Identify objects with bounding boxes

Smart Tags:
- Auto-label images with keywords""",
        },
        {
            "layout": "content_alt",
            "title": "Use Cases: Accessibility",
            "content": """Helping visually impaired users:

- Screen readers describing images
- Auto-generate alt-text for websites
- Make content accessible to everyone""",
        },
        {
            "layout": "content",
            "title": "Use Cases: Business",
            "content": """Retail & E-commerce:
- Product image tagging
- Visual search

Document Processing:
- Digitize paper documents
- Extract data from receipts""",
        },
        {
            "layout": "content_alt",
            "title": "What We'll Build",
            "content": """A Streamlit web app:

1. Upload image or paste URL
2. Send to Azure AI Vision API
3. Display results:
   - Caption
   - Objects detected
   - Extracted text (OCR)""",
        },
        {
            "layout": "content",
            "title": "Tech Stack",
            "content": """Simple & Powerful:

- Python 3.10+
- Streamlit (Web UI)
- Azure AI Vision REST API
- About 50 lines of code!""",
        },
        {
            "layout": "demo",
            "title": "Demo Time!",
            "subtitle": "Let's build it live!",
        },
        {
            "layout": "content",
            "title": "Resources",
            "content": """Documentation:
- learn.microsoft.com/azure/ai-services/computer-vision/

Microsoft Learn Path:
- Azure AI Vision learning path

Code from Today:
- github.com/jainal09/azure-ai-vision-workshop""",
        },
        {
            "layout": "content_alt",
            "title": "Certifications",
            "content": """Continue your journey:

- AI-900: Azure AI Fundamentals
- AI-102: Azure AI Engineer Associate

Free learning resources on Microsoft Learn!""",
        },
        {
            "layout": "section",
            "title": "Q&A",
        },
        {
            "layout": "content",
            "title": "Connect With Me",
            "content": """Jainal Gosaliya

LinkedIn:
- linkedin.com/in/jainal-gosaliya

GitHub:
- github.com/jainal09""",
        },
        {
            "layout": "closing",
            "title": "Thank You!",
        },
    ]

    for i, slide_data in enumerate(slides):
        print(f"Adding slide {i + 2}: {slide_data.get('title', 'Untitled')}")
        add_slide(prs, slide_data)

    prs.save(OUTPUT_PATH)
    print(f"\nSaved: {OUTPUT_PATH}")
    print(f"Total slides: {len(prs.slides)}")


if __name__ == "__main__":
    generate_presentation()
