# LUXBIN - Hugging Face Deployment Instructions

## 📋 Complete Deployment Guide

Follow these steps to deploy your LUXBIN demo to Hugging Face Spaces.

---

## Prerequisites

1. **Hugging Face Account**: Create one at [huggingface.co](https://huggingface.co)
2. **Git Installed**: For uploading files (or use the web interface)

---

## Method 1: Web Upload (Easiest)

### Step 1: Create New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in:
   - **Space name**: `luxbin-demo` (or your preferred name)
   - **License**: `mit` or `apache-2.0`
   - **SDK**: Select **Gradio**
   - **Space hardware**: `CPU basic` (free tier works fine)
4. Click **"Create Space"**

### Step 2: Upload Files

You'll see an empty repository. Upload these 3 files:

**File 1: `app.py`**
- Click **"Files and versions"** → **"Add file"** → **"Upload files"**
- Upload: `/Users/nicholechristie/Documents/Unreal Projects/WWYD 5.7/LUXBIN_HF_DEMO/app.py`

**File 2: `requirements.txt`**
- Click **"Add file"** → **"Upload files"** again
- Upload: `/Users/nicholechristie/Documents/Unreal Projects/WWYD 5.7/LUXBIN_HF_DEMO/requirements.txt`

**File 3: `README.md`**
- The README.md is auto-created, but replace it with:
- Click on `README.md` → **"Edit"**
- Copy contents from `/Users/nicholechristie/Documents/Unreal Projects/WWYD 5.7/LUXBIN_HF_DEMO/README.md`
- Click **"Commit changes to main"**

### Step 3: Wait for Build

- Hugging Face will automatically build your Space
- Watch the build logs at the top of the page
- Should take 1-2 minutes
- When you see **"Running"** status, it's live!

### Step 4: Test

1. Visit your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/luxbin-demo`
2. Try the encoder with "HELLO WORLD"
3. Test different grammar settings
4. View the alphabet wheel and grammar guide

---

## Method 2: Git Upload (Advanced)

### Step 1: Create Space

Same as Method 1 - create the Space on Hugging Face website first.

### Step 2: Clone Repository

```bash
cd ~/Desktop
git clone https://huggingface.co/spaces/YOUR_USERNAME/luxbin-demo
cd luxbin-demo
```

### Step 3: Copy Files

```bash
cp "/Users/nicholechristie/Documents/Unreal Projects/WWYD 5.7/LUXBIN_HF_DEMO/app.py" .
cp "/Users/nicholechristie/Documents/Unreal Projects/WWYD 5.7/LUXBIN_HF_DEMO/requirements.txt" .
cp "/Users/nicholechristie/Documents/Unreal Projects/WWYD 5.7/LUXBIN_HF_DEMO/README.md" .
```

### Step 4: Push to Hugging Face

```bash
git add .
git commit -m "Initial LUXBIN demo"
git push
```

### Step 5: Verify

Visit your Space URL and test the app.

---

## Troubleshooting

### Build Fails with Gradio Import Error

**Error**: `ImportError: cannot import name 'HfFolder' from 'huggingface_hub'`

**Fix**: Make sure `requirements.txt` has:
```txt
gradio>=5.9.1
huggingface-hub>=1.2.0
```

**NOT**:
```txt
gradio==4.44.1  ❌ (too old)
```

### Font Not Found Warnings

**Warning**: `Cannot open font resource`

**Impact**: Letters on hue wheel may not display perfectly, but app still works

**Fix** (optional): Add to `requirements.txt`:
```txt
matplotlib>=3.7.0
```

And update font path in `app.py`:
```python
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 16)
except:
    font = ImageFont.load_default()
```

### Space Shows "Building" Forever

1. Check build logs for errors
2. Most common: requirements.txt syntax error
3. Fix: Make sure each package is on its own line, no trailing spaces

---

## Updating Your Space

### Web Method:
1. Go to your Space
2. Click **"Files and versions"**
3. Click on the file you want to edit
4. Make changes
5. Click **"Commit changes to main"**

### Git Method:
```bash
cd luxbin-demo
# Make your changes to app.py or other files
git add .
git commit -m "Updated encoder logic"
git push
```

Space will automatically rebuild!

---

## Making Your Space Public

By default, Spaces are public. To change visibility:

1. Go to your Space settings
2. Scroll to **"Visibility"**
3. Choose **"Public"** or **"Private"**

---

## Sharing Your Space

Your Space URL is:
```
https://huggingface.co/spaces/YOUR_USERNAME/luxbin-demo
```

Share this link! People can:
- Use the encoder without signing in
- See your README documentation
- Fork your Space to make their own version

---

## Next Steps

1. **Customize**: Add more LUXBIN features (decoder, animations, sound)
2. **Document**: Add examples and tutorials to README
3. **Share**: Post on social media, forums, etc.
4. **Improve**: Add temporal encoding visualization, sentence structure, etc.

---

## Support

- **Hugging Face Docs**: [huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)
- **Gradio Docs**: [gradio.app/docs](https://www.gradio.app/docs)
- **LUXBIN Spec**: See `README.md` in this demo

---

**Your LUXBIN demo is ready to deploy!** 🚀

Choose Method 1 (web upload) for simplicity, or Method 2 (git) if you're comfortable with command line.
