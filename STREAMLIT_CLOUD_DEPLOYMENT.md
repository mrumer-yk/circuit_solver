# 🚀 Streamlit Cloud Deployment Guide

## ⚠️ **IMPORTANT: Fix for "Error installing requirements"**

If you're getting the "Error installing requirements" error, follow these steps:

### Step 1: Use the Correct Requirements File
**For Streamlit Cloud deployment, use:**
```
requirements_cloud.txt
```

**NOT:**
```
requirements.txt
```

### Step 2: Streamlit Cloud Configuration
1. **Main file path**: `app.py`
2. **Requirements file**: `requirements_cloud.txt`
3. **Python version**: 3.9 (recommended)

### Step 3: Add Environment Variables
In Streamlit Cloud app settings, add these secrets:
```toml
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```

## 🔧 **Why This Fixes the Issue**

The original `requirements.txt` had:
- ❌ **Fixed versions** that may not be compatible with Streamlit Cloud
- ❌ **OpenCV with GUI dependencies** that fail in cloud environment

The new `requirements_cloud.txt` has:
- ✅ **Flexible version ranges** for better compatibility
- ✅ **OpenCV headless version** (no GUI dependencies)
- ✅ **Streamlined dependencies** for cloud deployment

## 📋 **Deployment Steps**

1. **Go to**: [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with GitHub
3. **Click "New app"**
4. **Repository**: `mrumer-yk/new_solver_circuit`
5. **Branch**: `master`
6. **Main file path**: `app.py`
7. **Requirements file**: `requirements_cloud.txt`
8. **Add secrets**: Your Gemini API key
9. **Click "Deploy!"**

## 🚨 **Troubleshooting**

### If still getting requirements error:
1. **Check Python version**: Use Python 3.9
2. **Clear cache**: Delete and recreate the app
3. **Check logs**: Look at the terminal output for specific errors

### Common issues:
- **OpenCV**: Use `opencv-python-headless` instead of `opencv-python`
- **Version conflicts**: Use flexible version ranges (`>=` instead of `==`)
- **System dependencies**: The `packages.txt` file handles this

## ✅ **Expected Result**

After successful deployment, you should see:
- ✅ **No "Error installing requirements" message**
- ✅ **Circuit Solving Agent interface loads**
- ✅ **Image upload functionality works**
- ✅ **Gemini API integration functional**

## 🔄 **Local vs Cloud**

- **Local development**: Use `requirements.txt` + `config_local.toml`
- **Streamlit Cloud**: Use `requirements_cloud.txt` + `config_cloud.toml`

This separation ensures both environments work optimally!
