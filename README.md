# ⚡ Circuit Solving Agent

An AI-powered circuit analysis and problem-solving application built with Streamlit and Google Gemini AI.

## 🚀 Quick Deploy

### Deploy to Streamlit Cloud (Recommended)
1. **Fork this repository** or push your code to GitHub
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Sign in with GitHub** and click "New app"
4. **Select your repository** and set main file to `app.py`
5. **Add your Gemini API key** in the app settings
6. **Deploy!** 🎉

### Local Development
```bash
# Clone and setup
git clone <your-repo-url>
cd new_chain_of_thoughts

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py --server.port 8501
```

## ✨ Features

### 🔌 Core Circuit Analysis
- **AI-Powered Analysis**: Uses Gemini Pro Vision for circuit understanding
- **Multi-Format Support**: JPG, PNG, BMP, TIFF images
- **Smart Processing**: Handles blurry and handwritten circuits
- **Confidence Scoring**: AI confidence assessment with validation

### 🔧 Smart Image Enhancement
- **Auto-Enhancement**: Automatically improves image quality
- **Blurry Photo Correction**: Advanced algorithms for unclear images
- **Handwritten Recognition**: Specialized for hand-drawn circuits
- **Before/After Comparison**: Visual quality improvement display

### 📊 Comprehensive Results
- **Circuit Identification**: Type and component analysis
- **Mathematical Calculations**: Step-by-step circuit solutions
- **Validation Engine**: Multi-layer result verification
- **Downloadable Reports**: Complete analysis in text format

## 🏗️ Architecture

```
new_chain_of_thoughts/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .streamlit/                 # Streamlit configuration
│   ├── config.toml            # App settings
│   └── secrets.toml           # API keys (local)
├── config/                     # Configuration management
│   └── settings.py            # App settings and prompts
├── models/                     # Data models
│   └── circuit_analysis.py    # Pydantic models
├── services/                   # External services
│   └── gemini_service.py      # Gemini API integration
├── chain/                      # Analysis workflow
│   └── circuit_analysis_chain.py  # Main analysis chain
├── utils/                      # Utility functions
│   ├── image_utils.py         # Basic image processing
│   ├── image_enhancement.py   # Advanced image enhancement
│   └── validation_engine.py   # Result validation
└── DEPLOYMENT.md              # Deployment guide
```

## 🔑 Configuration

### Required Environment Variables
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### Streamlit Cloud Secrets
```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

## 📱 Usage

1. **Upload Circuit Image**: Drag & drop or select circuit image
2. **Add Context**: Optional additional information or questions
3. **Choose Analysis Depth**: Basic, detailed, or comprehensive
4. **Analyze**: Click "Analyze Circuit" for AI-powered analysis
5. **Review Results**: Comprehensive analysis with confidence scoring
6. **Download Report**: Get complete analysis in text format

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Engine**: Google Gemini Pro Vision API
- **Image Processing**: OpenCV, Pillow (PIL)
- **Data Validation**: Pydantic models
- **Architecture**: Modular, chain-of-thought design

## 🔒 Security & Performance

- ✅ **API Key Protection**: Secure storage in Streamlit secrets
- ✅ **Input Validation**: File format and size restrictions
- ✅ **Error Handling**: Graceful failure with user feedback
- ✅ **Async Processing**: Non-blocking API calls
- ✅ **Image Optimization**: Automatic size and quality management

## 🚨 Troubleshooting

### Common Issues
1. **Connection Failed**: Check API key and Gemini API quota
2. **Image Upload Error**: Verify format (JPG/PNG/BMP/TIFF) and size (<10MB)
3. **Analysis Failed**: Ensure circuit is clearly visible in image

### Support
- Check Streamlit Cloud logs for errors
- Verify all dependencies in requirements.txt
- Test locally before deploying

## 📈 Future Enhancements

- [ ] User authentication and accounts
- [ ] Circuit library and history
- [ ] Advanced validation rules
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Real-time collaboration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using Streamlit and Gemini AI**

For deployment help, see [DEPLOYMENT.md](DEPLOYMENT.md)
