# 👁️ Azure AI Vision Workshop Demo

A Streamlit-based web application that demonstrates the capabilities of Microsoft Azure AI Vision API. Built for Microsoft Student Ambassador workshops.

![Azure AI Vision](https://img.shields.io/badge/Azure-AI%20Vision-0078D4?style=flat-square&logo=microsoft-azure)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)

## 🌟 Features

- **📝 Image Captioning** - Generate human-readable descriptions of images
- **🏷️ Smart Tags** - Automatically identify and tag image content
- **📦 Object Detection** - Detect objects with bounding boxes and confidence scores
- **📄 OCR (Optical Character Recognition)** - Extract printed and handwritten text
- **🔍 Dense Captions** - Generate detailed captions for multiple regions within an image
- **👥 People Detection** - Identify and locate people in images
- **✂️ Smart Crops** - Get AI-suggested crop regions for better framing

## 📸 Demo

The app provides three ways to analyze images:
1. **Upload** - Upload images from your local device
2. **URL** - Analyze images from public URLs
3. **Samples** - Try pre-loaded sample images

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Azure account with an active subscription ([Create free account](https://azure.microsoft.com/free/))
- Azure CLI installed ([Installation guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
- UV package manager ([Install UV](https://github.com/astral-sh/uv))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd msa-q4-25
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up Azure AI Vision**

   Login to Azure:
   ```bash
   az login
   ```

   Create a resource group:
   ```bash
   az group create --name rg-vision-workshop --location eastus
   ```

   Create AI Vision resource:
   ```bash
   az cognitiveservices account create \
     --name vision-workshop-resource \
     --resource-group rg-vision-workshop \
     --kind ComputerVision \
     --sku F0 \
     --location eastus \
     --yes
   ```

4. **Get your credentials**

   Get endpoint:
   ```bash
   az cognitiveservices account show \
     --name vision-workshop-resource \
     --resource-group rg-vision-workshop \
     --query "properties.endpoint" \
     --output tsv
   ```

   Get API key:
   ```bash
   az cognitiveservices account keys list \
     --name vision-workshop-resource \
     --resource-group rg-vision-workshop \
     --query "key1" \
     --output tsv
   ```

5. **Create `.env` file**

   Create a `.env` file in the project root:
   ```bash
   AZURE_VISION_ENDPOINT=https://eastus.api.cognitive.microsoft.com/
   AZURE_VISION_KEY=your-key-here
   ```

   Replace with your actual endpoint and key from step 4.

6. **Run the application**
   ```bash
   uv run streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`

## 🎮 Usage

1. **Select features** - Choose which analysis features to enable from the sidebar
2. **Choose input method**:
   - Upload an image file
   - Enter a public image URL
   - Select a sample image
3. **Click "Analyze Image"** - View comprehensive results including captions, tags, detected objects, and extracted text
4. **Explore results** - View visualizations with bounding boxes and confidence scores

## 📁 Project Structure

```
msa-q4-25/
├── app.py                    # Main Streamlit application
├── pyproject.toml           # Project dependencies and metadata
├── .env                     # Environment variables (create this)
├── commands.md              # Detailed Azure CLI command reference
├── DEMO_WALKTHROUGH.md      # Workshop presentation guide
├── README.md                # This file
├── sample_images/           # Sample images for testing
├── analyze_template.py      # Template for custom analysis
├── download_samples.py      # Script to download sample images
├── generate_ppt.py          # Generate presentation slides
└── presentation.md          # Presentation content
```

## 🔑 Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
AZURE_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_VISION_KEY=your-api-key-here
```

⚠️ **Important**: Never commit your `.env` file to version control!

## 💰 Pricing

- **F0 (Free Tier)**: 20 calls/minute, 5,000 calls/month
- **S1 (Standard Tier)**: ~$1 per 1,000 transactions

See [Azure AI Vision Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/computer-vision/) for details.

## 🧹 Cleanup

After you're done, delete the Azure resources to avoid charges:

```bash
az group delete --name rg-vision-workshop --yes --no-wait
```

## 🛠️ Development

### Running in Development Mode

```bash
uv run streamlit run app.py --server.runOnSave true
```

This enables auto-reload when you save changes to the code.

### Project Dependencies

- **streamlit** - Web framework for the UI
- **requests** - HTTP library for API calls
- **Pillow** - Image processing and manipulation
- **python-dotenv** - Load environment variables from .env file

## 📚 Resources

- [Azure AI Vision Documentation](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/)
- [Microsoft Learn Path - Computer Vision](https://learn.microsoft.com/en-us/training/paths/create-computer-vision-solutions-azure-ai/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Azure CLI Reference](https://docs.microsoft.com/en-us/cli/azure/)

## 🤝 Contributing

This project is designed for educational purposes as part of Microsoft Student Ambassador workshops. Feel free to fork and adapt for your own workshops!

## 📝 License

MIT License - See LICENSE file for details

## 🎓 Workshop Information

This demo is part of the Microsoft Student Ambassador workshop series on Azure AI Services. It's designed to be:
- **Interactive** - Hands-on experience with real Azure APIs
- **Educational** - Learn cloud AI concepts practically
- **Accessible** - Free tier available for all students

## 🐛 Troubleshooting

### "Azure credentials not found" Error
- Ensure your `.env` file exists in the project root
- Verify the environment variables are correctly formatted (no spaces around `=`)
- Check that your endpoint URL ends with a `/`

### "API Error: 401" 
- Your API key may be incorrect
- Run the key retrieval command again to get a fresh key

### "API Error: 429"
- You've exceeded the rate limit (20 calls/minute on F0 tier)
- Wait a minute or upgrade to S1 tier

### Free Tier Already Used
- If you get "F0 SKU already exists" error, use `--sku S1` instead
- Or delete your existing F0 resource from another region

## 👨‍💻 Author

Built with ❤️ by Microsoft Student Ambassadors

---

**Happy Coding! 🚀**
