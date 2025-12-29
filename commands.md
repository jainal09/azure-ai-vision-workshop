# Azure AI Vision Workshop - Command Reference

## Prerequisites Checklist

Before starting, ensure you have:
- [ ] Azure CLI installed (`az --version`)
- [ ] Logged in to Azure (`az login`)
- [ ] Python 3.10+ installed (`python --version`)
- [ ] uv installed (`uv --version`) - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`

---

# LIVE DEMO FLOW (Copy-Paste Ready)

> **Use this section during your live demo. Each step is numbered and ready to copy-paste.**

---

## STEP 1: Verify Login

```bash
az account show
```

**What to look for:** Your subscription name and email should appear.

---

## STEP 2: Create Resource Group

```bash
az group create --name rg-vision-workshop --location eastus
```

**What to look for:** `"provisioningState": "Succeeded"`

---

## STEP 3: Create AI Vision Resource

```bash
az cognitiveservices account create \
  --name vision-workshop-resource \
  --resource-group rg-vision-workshop \
  --kind ComputerVision \
  --sku F0 \
  --location eastus \
  --yes
```

**What to look for:** `"provisioningState": "Succeeded"` and `"sku": { "name": "F0" }`

> **If you get "F0 already exists" error**, use `--sku S1` instead (paid tier, ~$1/1000 calls)

---

## STEP 4: Get Endpoint

```bash
az cognitiveservices account show \
  --name vision-workshop-resource \
  --resource-group rg-vision-workshop \
  --query "properties.endpoint" \
  --output tsv
```

**OUTPUT EXAMPLE:**
```
https://eastus.api.cognitive.microsoft.com/
```

> **ACTION:** Copy the entire URL output (including https://)
> You'll paste this as `AZURE_VISION_ENDPOINT` in Step 6

---

## STEP 5: Get API Key

```bash
az cognitiveservices account keys list \
  --name vision-workshop-resource \
  --resource-group rg-vision-workshop \
  --query "key1" \
  --output tsv
```

**OUTPUT EXAMPLE:**
```
49d47589b1d144109a1b1d5acf278c23
```

> **ACTION:** Copy the key string (32 characters, no quotes)
> You'll paste this as `AZURE_VISION_KEY` in Step 6

---

## STEP 6: Create .env File

### Option A: Manual (Recommended for demo - more visual)

```bash
nano .env
```

Then type these two lines (paste your values from Steps 4 & 5):

```
AZURE_VISION_ENDPOINT=https://eastus.api.cognitive.microsoft.com/
AZURE_VISION_KEY=your-key-from-step-5
```

Save: `Ctrl+X`, then `Y`, then `Enter`

### Option B: One-liner (automated)

```bash
ENDPOINT=$(az cognitiveservices account show --name vision-workshop-resource --resource-group rg-vision-workshop --query "properties.endpoint" -o tsv) && \
KEY=$(az cognitiveservices account keys list --name vision-workshop-resource --resource-group rg-vision-workshop --query "key1" -o tsv) && \
echo "AZURE_VISION_ENDPOINT=$ENDPOINT" > .env && \
echo "AZURE_VISION_KEY=$KEY" >> .env
```

### Verify .env was created correctly:

```bash
cat .env
```

**Expected output:**
```
AZURE_VISION_ENDPOINT=https://eastus.api.cognitive.microsoft.com/
AZURE_VISION_KEY=49d47589b1d144109a1b1d5acf278c23
```

> **IMPORTANT:** Make sure there are NO spaces around the `=` signs!

---

## STEP 7: Install Python Dependencies

```bash
uv sync
```

**What to look for:** `Installed XX packages` message

---

## STEP 8: Run the App

```bash
uv run streamlit run app.py
```

**What to look for:**
```
Local URL: http://localhost:8501
```

> **ACTION:** Browser should open automatically. If not, click the URL or open http://localhost:8501

---

## STEP 9: Test the App

In the browser:
1. Check for green "Connected to:" message
2. Go to "Image URL" tab
3. Paste this test URL:
   ```
   https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/media/quickstarts/presentation.png
   ```
4. Click "Analyze Image"
5. Show the results: Caption, Tags, OCR text, Objects

---

## STEP 10: Cleanup (After Demo)

```bash
az group delete --name rg-vision-workshop --yes --no-wait
```

> This deletes everything in the background. No need to wait.

---

# DETAILED REFERENCE

## Resource Naming

| Resource | Name | Notes |
|----------|------|-------|
| Resource Group | `rg-vision-workshop` | Container for all resources |
| AI Vision | `vision-workshop-resource` | The actual AI service |
| SKU | `F0` (free) or `S1` (paid) | Free: 20 calls/min, 5K/month |
| Region | `eastus` | Good availability |

---

## .env File Format

The `.env` file must look EXACTLY like this:

```
AZURE_VISION_ENDPOINT=https://eastus.api.cognitive.microsoft.com/
AZURE_VISION_KEY=your-32-character-key-here
```

**Common mistakes:**
- Spaces around `=` (wrong: `AZURE_VISION_KEY = abc`)
- Missing `https://` in endpoint
- Extra quotes (wrong: `AZURE_VISION_KEY="abc"`)
- Trailing spaces after the key

---

## Troubleshooting

### "F0 SKU is not available" or "CanNotCreateMultipleFreeAccounts"

You already have a free tier resource (or a soft-deleted one blocking it). Options:

**Option A: Use paid tier instead**
```bash
az cognitiveservices account create \
  --name vision-workshop-resource \
  --resource-group rg-vision-workshop \
  --kind ComputerVision \
  --sku S1 \
  --location eastus \
  --yes
```
Cost: ~$1 per 1,000 API calls

**Option B: Find and delete the existing F0 resource**
```bash
# List active ComputerVision resources
az cognitiveservices account list --query "[?kind=='ComputerVision']" --output table

# If found, delete it
az cognitiveservices account delete --name <resource-name> --resource-group <resource-group>
```

**Option C: Purge soft-deleted resources (most common issue!)**
```bash
# List soft-deleted resources
az cognitiveservices account list-deleted --output table

# Purge the soft-deleted resource
az cognitiveservices account purge \
  --name vision-workshop-resource \
  --location eastus \
  --resource-group rg-vision-workshop

# Then retry creating the F0 resource
az cognitiveservices account create \
  --name vision-workshop-resource \
  --resource-group rg-vision-workshop \
  --kind ComputerVision \
  --sku F0 \
  --location eastus \
  --yes
```

### "Resource provider not registered"

```bash
az provider register --namespace Microsoft.CognitiveServices
# Wait 1-2 minutes, then retry
```

### App shows "Azure credentials not found"

Your `.env` file is missing or malformed. Check:
```bash
cat .env
```

Make sure both lines exist and have correct values.

### App shows "API Error: 401"

Invalid API key. Regenerate:
```bash
az cognitiveservices account keys regenerate \
  --name vision-workshop-resource \
  --resource-group rg-vision-workshop \
  --key-name key1
```

Then update `.env` with the new key.

### App shows "API Error: 404"

Wrong endpoint URL. Get it again:
```bash
az cognitiveservices account show \
  --name vision-workshop-resource \
  --resource-group rg-vision-workshop \
  --query "properties.endpoint" \
  --output tsv
```

---

## Quick Reference Card

| Action | Command |
|--------|---------|
| Login | `az login` |
| Create Resource Group | `az group create --name rg-vision-workshop --location eastus` |
| Create Vision Resource | `az cognitiveservices account create --name vision-workshop-resource --resource-group rg-vision-workshop --kind ComputerVision --sku F0 --location eastus --yes` |
| Get Endpoint | `az cognitiveservices account show --name vision-workshop-resource --resource-group rg-vision-workshop --query "properties.endpoint" -o tsv` |
| Get Key | `az cognitiveservices account keys list --name vision-workshop-resource --resource-group rg-vision-workshop --query "key1" -o tsv` |
| Install Deps | `uv sync` |
| Run App | `uv run streamlit run app.py` |
| Type Check | `uv run ty check` |
| Cleanup | `az group delete --name rg-vision-workshop --yes --no-wait` |

---

## Sample Image URLs for Testing

Copy-paste these during your demo:

**Office Scene (good for all features):**
```
https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/media/quickstarts/presentation.png
```

**Handwritten Text (impressive OCR demo):**
```
https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/handwritten_text.jpg
```

**Printed Text:**
```
https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/printed_text.jpg
```

**Street/Landmark:**
```
https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/landmark.jpg
```

---

## Timing Guide

| Step | Time | Running Total |
|------|------|---------------|
| Steps 1-3 (Azure setup) | 3 min | 3 min |
| Steps 4-6 (Get creds + .env) | 2 min | 5 min |
| Step 7 (uv sync) | 1 min | 6 min |
| Step 8 (Run app) | 1 min | 7 min |
| Step 9 (Demo testing) | 10 min | 17 min |
| Code walkthrough | 5 min | 22 min |
| Step 10 (Cleanup) | 1 min | 23 min |
| Buffer/Q&A | 7 min | 30 min |
