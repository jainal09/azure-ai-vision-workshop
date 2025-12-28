"""
Generate Azure AI Vision Workshop PowerPoint from template.

This script takes the Microsoft Student Ambassadors branded template
and populates it with the workshop content.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt


# Template and output paths
TEMPLATE_PATH = "/Users/jainal09/Downloads/MS_SA_Template_Final.pptx"
OUTPUT_PATH = "/Users/jainal09/msa-q4-25/Azure_AI_Vision_Workshop.pptx"

# Workshop content
WORKSHOP_CONTENT = {
    "title": "Build an AI-Powered Image Analyzer",
    "subtitle": "Azure AI Vision Workshop",
    "presenter": "Jainal Gosaliya",
    "date": "",  # Update this!
    "slides": [
        {
            "layout": "title",  # Will use Walkin 4 (index 3)
            "title": "Build an AI-Powered Image Analyzer",
            "subtitle": "Azure AI Vision Workshop",
        },
        {
            "layout": "content",
            "title": "About Me",
            "content": """Jainal Gosaliya

Beta Microsoft Learn Student Ambassador

Pursuing Masters of Software Engineering Systems
at Northeastern University

Loves Python, AI, and Azure!

Connect with me:
linkedin.com/in/jainal-gosaliya
github.com/jainal09""",
        },
        {
            "layout": "content",  # Title & Non-bulleted text (index 6)
            "title": "Agenda",
            "content": """What We'll Cover Today

- Introduction to Azure AI Vision (5 min)
- Key Features & Use Cases (3 min)
- Live Demo: Build an Image Analyzer (20 min)
- Q&A (2 min)

By the end, you'll be able to:
- Set up Azure AI Vision from scratch
- Build a working image analyzer app
- Extract text, detect objects, and generate captions""",
        },
        {
            "layout": "content",
            "title": "What is Azure AI Vision?",
            "content": """Cloud-based AI service that analyzes images and extracts information

Part of: Microsoft Foundry Tools (Azure AI Services)

Key Capabilities:
- Read and extract text from images (OCR)
- Detect and identify objects in photos
- Generate human-like image descriptions
- Analyze image content and metadata

Pricing: Free tier available!
- 20 calls/minute
- 5,000 calls/month

learn.microsoft.com/azure/ai-services/computer-vision/""",
        },
        {
            "layout": "content",
            "title": "Key Features",
            "content": """OCR (Read)
Extract printed & handwritten text - scan receipts, documents, signs

Image Captions
Generate natural language descriptions - "A dog playing in the park"

Object Detection
Identify objects with bounding boxes - find all cars in a parking lot

Smart Tags
Label images with keywords - ["outdoor", "nature", "sunny"]

Dense Captions
Multiple captions for different regions of an image

People Detection
Detect people and their positions in photos""",
        },
        {
            "layout": "content",
            "title": "Real-World Use Cases",
            "content": """Accessibility
- Screen readers describing images for visually impaired users
- Alt-text generation for websites

Retail & E-commerce
- Product image tagging
- Visual search ("find similar items")

Document Processing
- Digitize paper documents
- Extract data from forms and receipts

Security & Surveillance
- Object detection in security feeds
- License plate recognition

Social Media
- Content moderation
- Auto-tagging photos""",
        },
        {
            "layout": "content",
            "title": "What We'll Build",
            "content": """A Streamlit web app that:

1. Accepts image upload or URL
2. Sends image to Azure AI Vision API
3. Displays results:
   - Generated caption
   - Detected objects with bounding boxes
   - Extracted text (OCR)
   - Smart tags

Tech Stack:
- Python 3.10+
- Streamlit (Web UI)
- Azure AI Vision SDK
- ~50 lines of code!""",
        },
        {
            "layout": "demo",  # Demo slide (index 19)
            "title": "Demo",
            "subtitle": "Let's build it live!",
        },
        {
            "layout": "content",
            "title": "Resources & Next Steps",
            "content": """Official Documentation
learn.microsoft.com/azure/ai-services/computer-vision/

Microsoft Learn Path
learn.microsoft.com/training/paths/create-computer-vision-solutions-azure-ai/

Certifications
- AI-102: Azure AI Engineer Associate
- AI-900: Azure AI Fundamentals

Code from Today
github.com/jainal09/azure-ai-vision-workshop

Questions? Let's connect!
linkedin.com/in/jainal-gosaliya""",
        },
        {
            "layout": "section",  # Section Title (index 21)
            "title": "Q&A",
        },
        {
            "layout": "closing",  # Closing slide (index 28)
            "title": "Thank You!",
        },
    ],
}


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
        "title": 3,  # Walkin 4 - title slide
        "content": 6,  # Title & Non-bulleted text
        "content_bullets": 9,  # Title and Content (with bullets)
        "two_column": 11,  # Two Column Non-bulleted text
        "demo": 19,  # Demo slide
        "video": 20,  # Video slide
        "section": 21,  # Section Title
        "code": 27,  # Developer Code Layout
        "closing": 28,  # Closing logo slide_1
    }
    return layout_map.get(layout_type, 6)


def add_slide(prs: Presentation, slide_data: dict) -> None:
    """Add a slide with the specified layout and content."""
    layout_idx = get_layout_index(slide_data["layout"])
    layout = prs.slide_layouts[layout_idx]
    slide = prs.slides.add_slide(layout)

    # Set title
    if slide.shapes.title:
        slide.shapes.title.text = slide_data.get("title", "")

    # Set content based on layout type
    if slide_data["layout"] in ["content", "content_bullets", "code"]:
        # Find the body placeholder
        for shape in slide.placeholders:
            if shape.placeholder_format.type == 2:  # BODY type
                shape.text = slide_data.get("content", "")
                # Adjust font size for readability
                for paragraph in shape.text_frame.paragraphs:
                    paragraph.font.size = Pt(18)
                break

    elif slide_data["layout"] == "demo":
        # Demo slide has subtitle
        for shape in slide.placeholders:
            if shape.placeholder_format.type == 2:  # BODY type
                shape.text = slide_data.get("subtitle", "")
                break

    elif slide_data["layout"] == "title":
        # Title slide has subtitle
        for shape in slide.placeholders:
            if shape.placeholder_format.type == 2:  # BODY type
                shape.text = slide_data.get("subtitle", "")
                break


def generate_presentation() -> None:
    """Generate the workshop presentation from template."""
    print(f"Loading template: {TEMPLATE_PATH}")

    # Copy template to output
    shutil.copy(TEMPLATE_PATH, OUTPUT_PATH)

    # Open the copy
    prs = Presentation(OUTPUT_PATH)

    print(f"Template has {len(prs.slides)} existing slides")

    # Clear all slides except the first walk-in slide
    clear_slides(prs, keep_first_n=1)
    print(f"Cleared slides, keeping first 1. Now have {len(prs.slides)} slides")

    # Add our workshop slides
    for i, slide_data in enumerate(WORKSHOP_CONTENT["slides"]):
        print(f"Adding slide {i + 2}: {slide_data.get('title', 'Untitled')} ({slide_data['layout']})")
        add_slide(prs, slide_data)

    # Save
    prs.save(OUTPUT_PATH)
    print(f"\nPresentation saved to: {OUTPUT_PATH}")
    print(f"Total slides: {len(prs.slides)}")


if __name__ == "__main__":
    generate_presentation()
