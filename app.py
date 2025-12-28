"""
Azure AI Vision Workshop Demo
=============================
A Streamlit application that demonstrates Azure AI Vision capabilities.

Features:
- Image captioning
- Object detection with bounding boxes
- OCR (text extraction)
- Smart tags
- Dense captions

Author: Microsoft Student Ambassador Workshop
"""

from __future__ import annotations

import io
import os
from typing import Any

import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image, ImageDraw

# Load environment variables
load_dotenv()

# Azure AI Vision configuration
ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT", "").rstrip("/")
API_KEY = os.getenv("AZURE_VISION_KEY", "")

# API version and URL
API_VERSION = "2024-02-01"
ANALYZE_URL = f"{ENDPOINT}/computervision/imageanalysis:analyze"


def analyze_image(image_data: bytes, features: list[str]) -> dict[str, Any]:
    """
    Send image to Azure AI Vision API for analysis.

    Args:
        image_data: Image bytes
        features: List of features to analyze (caption, tags, objects, read, denseCaptions)

    Returns:
        API response as dictionary
    """
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Content-Type": "application/octet-stream"
    }

    params = {
        "api-version": API_VERSION,
        "features": ",".join(features)
    }

    response = requests.post(
        ANALYZE_URL,
        headers=headers,
        params=params,
        data=image_data,
        timeout=30
    )

    if response.status_code != 200:
        st.error(f"API Error: {response.status_code} - {response.text}")
        return {}

    return response.json()


def analyze_image_url(image_url: str, features: list[str]) -> dict[str, Any]:
    """
    Analyze image from URL using Azure AI Vision API.

    Args:
        image_url: URL of the image
        features: List of features to analyze

    Returns:
        API response as dictionary
    """
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Content-Type": "application/json"
    }

    params = {
        "api-version": API_VERSION,
        "features": ",".join(features)
    }

    body = {"url": image_url}

    response = requests.post(
        ANALYZE_URL,
        headers=headers,
        params=params,
        json=body,
        timeout=30
    )

    if response.status_code != 200:
        st.error(f"API Error: {response.status_code} - {response.text}")
        return {}

    return response.json()


def draw_bounding_boxes(image: Image.Image, objects: list[dict[str, Any]]) -> Image.Image:
    """
    Draw bounding boxes around detected objects.

    Args:
        image: PIL Image object
        objects: List of detected objects with bounding box coordinates

    Returns:
        Image with bounding boxes drawn
    """
    draw = ImageDraw.Draw(image)

    # Colors for different objects
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8"]

    for i, obj in enumerate(objects):
        bbox = obj.get("boundingBox", {})
        label = obj.get("tags", [{}])[0].get("name", "object") if obj.get("tags") else "object"
        confidence = obj.get("tags", [{}])[0].get("confidence", 0) if obj.get("tags") else 0

        x = bbox.get("x", 0)
        y = bbox.get("y", 0)
        w = bbox.get("w", 0)
        h = bbox.get("h", 0)

        color = colors[i % len(colors)]

        # Draw rectangle
        draw.rectangle(
            [(x, y), (x + w, y + h)],
            outline=color,
            width=3
        )

        # Draw label background
        label_text = f"{label} ({confidence:.0%})"
        text_bbox = draw.textbbox((x, y - 20), label_text)
        draw.rectangle(text_bbox, fill=color)
        draw.text((x, y - 20), label_text, fill="white")

    return image


def draw_ocr_boxes(image: Image.Image, read_result: dict[str, Any]) -> Image.Image:
    """
    Draw bounding boxes around detected text.

    Args:
        image: PIL Image object
        read_result: OCR result from API

    Returns:
        Image with text bounding boxes drawn
    """
    draw = ImageDraw.Draw(image)

    blocks = read_result.get("blocks", [])

    for block in blocks:
        for line in block.get("lines", []):
            polygon = line.get("boundingPolygon", [])
            if len(polygon) >= 4:
                points = [(p["x"], p["y"]) for p in polygon]
                draw.polygon(points, outline="#00FF00", width=2)

    return image


def main() -> None:
    """Main Streamlit application."""

    # Page configuration
    st.set_page_config(
        page_title="Azure AI Vision Demo",
        page_icon="👁️",
        layout="wide"
    )

    # Header
    st.title("👁️ Azure AI Vision Demo")
    st.markdown("*Analyze images using Microsoft Azure AI Vision*")

    # Check for API credentials
    if not ENDPOINT or not API_KEY:
        st.error("⚠️ Azure credentials not found!")
        st.info("""
        Please set up your `.env` file with:
        ```
        AZURE_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
        AZURE_VISION_KEY=your-api-key
        ```

        Run the commands in `commands.md` to create your Azure resource.
        """)
        st.stop()

    st.success(f"✅ Connected to: `{ENDPOINT}`")

    # Sidebar - Feature selection
    st.sidebar.header("🎛️ Analysis Options")

    features_to_analyze = []

    if st.sidebar.checkbox("📝 Caption", value=True, help="Generate a description of the image"):
        features_to_analyze.append("caption")

    if st.sidebar.checkbox("🏷️ Tags", value=True, help="Identify tags/keywords in the image"):
        features_to_analyze.append("tags")

    if st.sidebar.checkbox("📦 Object Detection", value=True, help="Detect objects with bounding boxes"):
        features_to_analyze.append("objects")

    if st.sidebar.checkbox("📄 OCR (Read Text)", value=True, help="Extract text from the image"):
        features_to_analyze.append("read")

    if st.sidebar.checkbox("🔍 Dense Captions", value=False, help="Generate captions for multiple regions"):
        features_to_analyze.append("denseCaptions")

    if st.sidebar.checkbox("👥 People Detection", value=False, help="Detect people in the image"):
        features_to_analyze.append("people")

    if st.sidebar.checkbox("✂️ Smart Crops", value=False, help="Suggest crop regions"):
        features_to_analyze.append("smartCrops")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 Resources")
    st.sidebar.markdown("[Azure AI Vision Docs](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/)")
    st.sidebar.markdown("[Microsoft Learn Path](https://learn.microsoft.com/en-us/training/paths/create-computer-vision-solutions-azure-ai/)")

    # Main content - Image input
    st.header("📸 Upload or Enter Image")

    tab1, tab2, tab3 = st.tabs(["📁 Upload Image", "🔗 Image URL", "🖼️ Sample Images"])

    image_data = None
    image_url = None
    display_image = None

    with tab1:
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["jpg", "jpeg", "png", "gif", "bmp", "webp"],
            help="Upload an image to analyze"
        )

        if uploaded_file:
            image_data = uploaded_file.getvalue()
            display_image = Image.open(io.BytesIO(image_data))

    with tab2:
        image_url = st.text_input(
            "Enter image URL",
            placeholder="https://example.com/image.jpg",
            help="Enter a publicly accessible image URL"
        )

        if image_url:
            try:
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    display_image = Image.open(io.BytesIO(response.content))
                else:
                    st.error("Failed to load image from URL")
            except Exception as e:
                st.error(f"Error loading image: {e}")

    with tab3:
        st.markdown("**Try these sample images:**")

        sample_images = {
            "Office Scene": "https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/media/quickstarts/presentation.png",
            "Street View": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg",
            "Handwritten Text": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/handwritten_text.jpg",
            "Printed Text": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/printed_text.jpg",
        }

        cols = st.columns(len(sample_images))

        for i, (name, url) in enumerate(sample_images.items()):
            with cols[i]:
                if st.button(f"📷 {name}", key=f"sample_{i}"):
                    image_url = url
                    try:
                        response = requests.get(url, timeout=10)
                        if response.status_code == 200:
                            display_image = Image.open(io.BytesIO(response.content))
                    except Exception as e:
                        st.error(f"Error loading sample: {e}")

    # Display image and analyze button
    if display_image:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("🖼️ Original Image")
            st.image(display_image, use_container_width=True)

        # Analyze button
        if st.button("🔍 Analyze Image", type="primary", use_container_width=True):
            if not features_to_analyze:
                st.warning("Please select at least one analysis feature from the sidebar.")
            else:
                with st.spinner("🔄 Analyzing image with Azure AI Vision..."):
                    # Call API
                    if image_data:
                        result = analyze_image(image_data, features_to_analyze)
                    elif image_url:
                        result = analyze_image_url(image_url, features_to_analyze)
                    else:
                        st.error("No image to analyze")
                        result = {}

                if result:
                    st.header("📊 Analysis Results")

                    # Create result columns
                    result_col1, result_col2 = st.columns([1, 1])

                    with result_col1:
                        # Caption
                        if "captionResult" in result:
                            st.subheader("📝 Caption")
                            caption = result["captionResult"]
                            st.info(f"**{caption.get('text', 'N/A')}**")
                            st.caption(f"Confidence: {caption.get('confidence', 0):.1%}")

                        # Tags
                        if "tagsResult" in result:
                            st.subheader("🏷️ Tags")
                            tags = result["tagsResult"].get("values", [])
                            if tags:
                                tag_html = " ".join([
                                    f'<span style="background-color: #4ECDC4; color: white; padding: 4px 8px; border-radius: 4px; margin: 2px; display: inline-block;">{tag["name"]} ({tag["confidence"]:.0%})</span>'
                                    for tag in tags[:15]
                                ])
                                st.markdown(tag_html, unsafe_allow_html=True)
                            else:
                                st.write("No tags detected")

                        # Dense Captions
                        if "denseCaptionsResult" in result:
                            st.subheader("🔍 Dense Captions")
                            dense_captions = result["denseCaptionsResult"].get("values", [])
                            for dc in dense_captions[:5]:
                                st.write(f"• {dc.get('text', 'N/A')} ({dc.get('confidence', 0):.0%})")

                    with result_col2:
                        # OCR Results
                        if "readResult" in result:
                            st.subheader("📄 Extracted Text (OCR)")
                            read_result = result["readResult"]
                            blocks = read_result.get("blocks", [])

                            all_text = []
                            for block in blocks:
                                for line in block.get("lines", []):
                                    all_text.append(line.get("text", ""))

                            if all_text:
                                st.text_area(
                                    "Detected Text:",
                                    "\n".join(all_text),
                                    height=200
                                )
                            else:
                                st.write("No text detected in image")

                        # Object Detection
                        if "objectsResult" in result:
                            st.subheader("📦 Detected Objects")
                            objects = result["objectsResult"].get("values", [])

                            if objects:
                                # Draw bounding boxes on image
                                img_with_boxes = display_image.copy()
                                img_with_boxes = draw_bounding_boxes(img_with_boxes, objects)
                                st.image(img_with_boxes, caption="Objects with bounding boxes", use_container_width=True)

                                # List objects
                                for obj in objects:
                                    tags = obj.get("tags", [])
                                    if tags:
                                        st.write(f"• {tags[0]['name']} ({tags[0]['confidence']:.0%})")
                            else:
                                st.write("No objects detected")

                        # People Detection
                        if "peopleResult" in result:
                            st.subheader("👥 People Detected")
                            people = result["peopleResult"].get("values", [])
                            st.write(f"Found {len(people)} person(s) in the image")

                    # Raw JSON (expandable)
                    with st.expander("📋 View Raw JSON Response"):
                        st.json(result)

    else:
        st.info("👆 Upload an image, enter a URL, or select a sample image to get started!")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        Built with ❤️ using Azure AI Vision & Streamlit |
        <a href='https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/'>Documentation</a>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
