# Azure AI Vision Workshop
## Build an AI-Powered Image Analyzer

---

# SLIDE 1: Title Slide

**Title:** Build an AI-Powered Image Analyzer with Azure AI Vision

**Subtitle:** Hands-on Workshop | Microsoft Student Ambassadors

**Presenter:** [Your Name]

**Date:** [Event Date]

> [IMAGE PLACEHOLDER: Azure AI Vision logo + futuristic image analysis graphic]

---

# SLIDE 2: Agenda

**What We'll Cover Today**

| Time | Section |
|------|---------|
| 5 min | Introduction to Azure AI Vision |
| 3 min | Key Features & Use Cases |
| 20 min | Live Demo: Build an Image Analyzer |
| 2 min | Q&A |

**By the end, you'll be able to:**
- Understand what Azure AI Vision can do
- Set up Azure AI Vision resource from scratch
- Build a working image analyzer application
- Extract text, detect objects, and generate captions from images

---

# SLIDE 3: What is Azure AI Vision?

**Azure AI Vision** is a cloud-based AI service that analyzes images and extracts valuable information.

**Part of:** Microsoft Foundry Tools (formerly Azure AI Services)

**Key Capabilities:**
- Read and extract text from images (OCR)
- Detect and identify objects in photos
- Generate human-like image descriptions
- Analyze image content and metadata

**Pricing:** Free tier available (20 calls/min, 5K calls/month)

> [IMAGE PLACEHOLDER: Azure AI Vision service icon with connected capabilities diagram]

**Microsoft Learn:** https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/

---

# SLIDE 4: Key Features

| Feature | What It Does | Example |
|---------|--------------|---------|
| **OCR (Read)** | Extracts printed & handwritten text | Scan receipts, documents, signs |
| **Image Captions** | Generates natural language descriptions | "A dog playing in the park" |
| **Dense Captions** | Multiple captions for different regions | Describe each part of an image |
| **Object Detection** | Identifies objects with bounding boxes | Find all cars in a parking lot |
| **Smart Tags** | Labels images with relevant keywords | ["outdoor", "nature", "sunny"] |
| **People Detection** | Detects people and their positions | Count people in a room |

> [IMAGE PLACEHOLDER: Grid showing each feature with a sample image and its output]

---

# SLIDE 5: Real-World Use Cases

**1. Accessibility**
- Screen readers describing images for visually impaired users
- Alt-text generation for websites

**2. Retail & E-commerce**
- Product image tagging
- Visual search ("find similar items")

**3. Document Processing**
- Digitize paper documents
- Extract data from forms and receipts

**4. Security & Surveillance**
- Object detection in security feeds
- License plate recognition

**5. Social Media**
- Content moderation
- Auto-tagging photos

> [IMAGE PLACEHOLDER: 4-panel grid showing each use case with icons]

---

# SLIDE 6: Architecture Overview

```
┌──────────────┐     ┌─────────────────────┐     ┌──────────────────┐
│              │     │                     │     │                  │
│  Your App    │────▶│  Azure AI Vision    │────▶│  JSON Response   │
│  (Python)    │     │  REST API           │     │  (Results)       │
│              │     │                     │     │                  │
└──────────────┘     └─────────────────────┘     └──────────────────┘
       │                      │
       │                      │
       ▼                      ▼
┌──────────────┐     ┌─────────────────────┐
│ Image Input  │     │ Features:           │
│ - URL        │     │ - Caption           │
│ - File       │     │ - Tags              │
│ - Base64     │     │ - Objects           │
└──────────────┘     │ - OCR Text          │
                     │ - Dense Captions    │
                     └─────────────────────┘
```

**What you need:**
1. Azure Subscription (free tier works!)
2. Azure AI Vision Resource
3. API Key + Endpoint
4. Python + Azure SDK

> [IMAGE PLACEHOLDER: Clean architecture diagram with Azure icons]

---

# SLIDE 7: Demo Time!

**What We'll Build:**

A Streamlit web app that:
1. Accepts image upload or URL
2. Sends image to Azure AI Vision API
3. Displays:
   - Generated caption
   - Detected objects with bounding boxes
   - Extracted text (OCR)
   - Smart tags

**Tech Stack:**
- Python 3.10+
- Streamlit (Web UI)
- Azure AI Vision SDK
- Pillow (Image processing)

> [IMAGE PLACEHOLDER: Screenshot of the final app UI]

---

# SLIDE 8: Let's Code!

**Step-by-step:**

1. Create Azure AI Vision resource (Azure CLI)
2. Install dependencies
3. Write the Python code
4. Build the Streamlit UI
5. Test with sample images
6. Clean up resources

**Follow along:** [Your GitHub repo or live share link]

---

# SLIDE 9: Resources & Next Steps

**Official Documentation:**
- Azure AI Vision: https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/
- Quickstart: https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40

**Microsoft Learn Path:**
- Develop computer vision solutions: https://learn.microsoft.com/en-us/training/paths/create-computer-vision-solutions-azure-ai/

**Certifications:**
- AI-102: Azure AI Engineer Associate
- AI-900: Azure AI Fundamentals

**Code from today:** [Your GitHub repo link]

> [IMAGE PLACEHOLDER: QR code linking to resources]

---

# SLIDE 10: Q&A

**Questions?**

**Connect with me:**
- LinkedIn: [Your LinkedIn]
- GitHub: [Your GitHub]
- Twitter/X: [Your Handle]

**Thank you for attending!**

> [IMAGE PLACEHOLDER: Thank you graphic with contact info]

---

# APPENDIX: Image Suggestions

| Slide | Suggested Image |
|-------|-----------------|
| 1 | Azure AI Vision hero image from Microsoft docs |
| 3 | Azure Cognitive Services family diagram |
| 4 | Feature comparison grid (create in PowerPoint) |
| 5 | Use case icons (accessibility, retail, document, security) |
| 6 | Architecture diagram (draw in PowerPoint or use draw.io) |
| 7 | Screenshot of your completed demo app |
| 9 | QR code generator: https://www.qr-code-generator.com/ |
| 10 | Professional thank you slide background |

**Recommended sources for images:**
- Microsoft Design: https://developer.microsoft.com/en-us/fabric#/resources
- Azure Icons: https://learn.microsoft.com/en-us/azure/architecture/icons/
- Unsplash (free stock): https://unsplash.com/
