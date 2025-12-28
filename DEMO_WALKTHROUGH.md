# Demo Walkthrough Guide

This guide helps you walk through the live demo during the workshop. Follow these steps in order.

---

## Pre-Demo Checklist (Do before the workshop)

- [ ] Run `az login` and verify you're logged in
- [ ] Test that `az account show` returns your subscription
- [ ] Have VS Code or terminal ready with this folder open
- [ ] Have browser ready to show Azure Portal (optional)
- [ ] Install dependencies: `uv sync`
- [ ] Download sample images: `uv run python download_samples.py`
- [ ] Have some fun images ready on your desktop to upload

---

## DEMO PART 1: Azure Resource Setup (~5 min)

### What to say:
> "First, let's create the Azure resources we need. We'll use Azure CLI to do this, which is great for automation and reproducibility."

### Commands to run (copy from commands.md):

```bash
# 1. Show we're logged in
az account show

# 2. Create resource group
az group create --name rg-vision-workshop --location eastus

# 3. Create the AI Vision resource (explain F0 is free tier)
az cognitiveservices account create \
  --name vision-workshop-resource \
  --resource-group rg-vision-workshop \
  --kind ComputerVision \
  --sku F0 \
  --location eastus \
  --yes

# 4. Get the endpoint
az cognitiveservices account show \
  --name vision-workshop-resource \
  --resource-group rg-vision-workshop \
  --query "properties.endpoint" \
  --output tsv

# 5. Get the API key
az cognitiveservices account keys list \
  --name vision-workshop-resource \
  --resource-group rg-vision-workshop

# 6. Create .env file (show this manually)
```

### Talking points:
- Explain what a resource group is (logical container)
- Mention F0 is free tier (20 calls/min, 5K calls/month)
- Show that we get an endpoint URL and API key
- Emphasize NEVER commit API keys to Git

---

## DEMO PART 2: Python Environment Setup (~2 min)

### What to say:
> "Now let's set up our Python environment. We're using uv - a super fast Python package manager from Astral."

### Commands to run:

```bash
# 1. Sync dependencies (uv creates venv automatically!)
uv sync

# 2. Create .env file with credentials
# Copy the endpoint and key from previous step
```

### Talking points:
- uv is 10-100x faster than pip
- Automatically creates virtual environment
- Uses pyproject.toml (modern Python standard)
- No need to activate venv manually!

### Show the .env file:
```bash
cat .env
```

---

## DEMO PART 3: Code Walkthrough (~5 min)

### What to say:
> "Let's look at the code and understand how it works."

### Open app.py and highlight these sections:

#### 1. Configuration (lines 20-30)
```python
# Load environment variables
load_dotenv()

# Azure AI Vision configuration
ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT", "").rstrip("/")
API_KEY = os.getenv("AZURE_VISION_KEY", "")
```
> "We load credentials from environment variables - never hardcode secrets!"

#### 2. API Call Function (lines 33-60)
```python
def analyze_image(image_data: bytes, features: list[str]) -> dict:
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Content-Type": "application/octet-stream"
    }
    params = {
        "api-version": API_VERSION,
        "features": ",".join(features)
    }
    response = requests.post(ANALYZE_URL, headers=headers, params=params, data=image_data)
```
> "This is the core - we send the image to Azure and get back JSON with all the analysis results."

#### 3. Feature Selection (sidebar)
> "The API supports multiple features - you choose what you need and pay only for what you use."

#### 4. Results Display
> "We parse the JSON response and display it in a user-friendly way."

---

## DEMO PART 4: Run the App (~3 min)

### What to say:
> "Let's run the app and see it in action!"

### Command:
```bash
uv run streamlit run app.py
```

### Show:
1. The app opens in browser
2. Green checkmark showing connected to Azure
3. Sidebar with feature options
4. Three tabs for input methods

---

## DEMO PART 5: Test Different Images (~8 min)

### Test 1: Sample Image - Office Scene
> "Let's start with a sample image from Microsoft."

1. Click "Sample Images" tab
2. Click "Office Scene"
3. Enable: Caption, Tags, Objects, OCR
4. Click "Analyze Image"
5. **Show and explain each result:**
   - Caption: AI-generated description
   - Tags: Keywords identified
   - Objects: With bounding boxes!
   - OCR: Text extracted from the presentation

### Test 2: Handwritten Text
> "Now let's try handwritten text - this is impressive!"

1. Click "Handwritten Text" sample
2. Enable only OCR
3. Click "Analyze"
4. **Show:** It can read handwriting!

### Test 3: Upload Your Own Image
> "Let's try something more interesting - upload your own image!"

1. Switch to "Upload Image" tab
2. Upload an image (have something fun ready)
3. Enable all features
4. Click "Analyze"
5. **Discuss the results**

### Test 4: Image URL
> "You can also analyze images from URLs."

1. Switch to "Image URL" tab
2. Paste any image URL
3. Analyze and show results

### Test 5: Dense Captions (if time permits)
> "Dense captions generate descriptions for different regions of the image."

1. Enable "Dense Captions" in sidebar
2. Analyze an image with multiple objects
3. Show multiple captions for different areas

---

## DEMO PART 6: Show Raw JSON (~2 min)

### What to say:
> "For developers, you can see the raw API response."

1. Expand "View Raw JSON Response"
2. Walk through the structure
3. Explain how you'd use this in a real application

---

## DEMO PART 7: Cleanup (~2 min)

### What to say:
> "Important: Let's clean up our resources so we don't get charged."

### Commands:
```bash
# Delete the resource group (deletes everything inside)
az group delete --name rg-vision-workshop --yes --no-wait
```

> "The --no-wait flag means it runs in the background. It'll take a few minutes to fully delete."

---

## Backup Plan

### If Azure CLI fails:
- Have a pre-created resource ready in another resource group
- Copy the endpoint and key from Azure Portal

### If API returns errors:
- Check if .env file is correct
- Verify the endpoint doesn't have trailing slash issues
- Check Azure Portal for any quota issues

### If Streamlit won't start:
- Run `uv sync` again
- Check Python version (need 3.10+)
- Try `uv run python -m streamlit run app.py`

---

## Key Messages to Reinforce

1. **Azure AI Vision is easy to use** - Just REST API calls
2. **Free tier available** - Great for learning and prototyping
3. **Multiple features** - Caption, tags, objects, OCR, and more
4. **Production ready** - Same APIs used in real Microsoft products
5. **Microsoft Learn** - Free learning path to go deeper

---

## Time Management

| Section | Target Time | Running Total |
|---------|-------------|---------------|
| Azure Setup | 5 min | 5 min |
| Python Setup | 2 min | 7 min |
| Code Walkthrough | 5 min | 12 min |
| Run App | 3 min | 15 min |
| Test Images | 8 min | 23 min |
| Raw JSON | 2 min | 25 min |
| Cleanup | 2 min | 27 min |
| **Buffer** | 3 min | 30 min |

---

## Transition to Q&A

> "That's the demo! As you can see, Azure AI Vision makes it really easy to add powerful image analysis to your applications. Any questions?"
