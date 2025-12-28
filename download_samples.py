"""
Download sample images for the Azure AI Vision workshop demo.
Run this script before the workshop to have local sample images ready.
"""

from __future__ import annotations

import os

import requests

SAMPLE_IMAGES: dict[str, str] = {
    "office_presentation.png": "https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/media/quickstarts/presentation.png",
    "landmark.jpg": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg",
    "handwritten_text.jpg": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/handwritten_text.jpg",
    "printed_text.jpg": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/printed_text.jpg",
    "objects.jpg": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/objects.jpg",
    "faces.jpg": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/faces.jpg",
}

OUTPUT_DIR = "sample_images"


def download_images() -> None:
    """Download all sample images."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Downloading sample images for Azure AI Vision workshop...")
    print("-" * 50)

    for filename, url in SAMPLE_IMAGES.items():
        filepath = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(filepath):
            print(f"[SKIP] {filename} already exists")
            continue

        try:
            print(f"[DOWNLOADING] {filename}...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"[OK] {filename} saved ({len(response.content) / 1024:.1f} KB)")

        except Exception as e:
            print(f"[ERROR] Failed to download {filename}: {e}")

    print("-" * 50)
    print(f"Done! Images saved to '{OUTPUT_DIR}/' directory")


if __name__ == "__main__":
    download_images()
