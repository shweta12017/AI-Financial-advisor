## AI Financial Advisor

A modern, colorful Streamlit web application that provides personalized financial insights, risk analysis, goal planning, and AI-powered financial advice with offline fallback capabilities.

### ✨ Features

- 🎨 **Modern UI** with blue, red, green, and golden color scheme
- 📊 **Financial Dashboard** - Enter and analyze your financial data
- ⚠️ **Risk Analysis** - Understand your financial health with color-coded indicators
- 🎯 **Goal Planner** - Plan and project your financial goals
- 🤖 **Smart Chatbot** - Get AI-powered financial advice with offline fallback
- 🔄 **Offline Mode** - Works without API dependencies
- 📱 **Responsive Design** - Works on all devices

### 🚀 Live Demo

Deployed on Render: [Your Live App URL](https://your-app-url.onrender.com)

### Project structure

```text
ai-financial-advisor/
├─ app.py
├─ render.yaml
├─ requirements.txt
├─ README.md
├─ .env.example
├─ .gitignore
├─ config/
│  └─ settings.py
├─ models/
│  └─ financial_profile.py
├─ services/
│  ├─ financial_calculations.py
│  ├─ gemini_client.py
│  ├─ advice_generator.py
│  └─ fallback_chatbot.py
├─ visualization/
│  └─ charts.py
├─ ui/
│  ├─ dashboard.py
│  ├─ risk_analysis.py
│  ├─ goal_planner.py
│  └─ chatbot.py
└─ utils/
   └─ validators.py
```

### 🛠️ Local Setup

1. **Clone the repository**:
```bash
git clone https://github.com/shweta12017/AI-Financial-advisor.git
cd AI-Financial-advisor
```

2. **Create and activate a virtual environment** (PowerShell example):
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure Gemini API key**:

- Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

- Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Add it to your `.env` file:
```text
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

5. **Run the app**:
```bash
streamlit run app.py
```

Then open the URL Streamlit prints in the console (usually `http://localhost:8501`).

### 🌐 Deployment on Render

1. **Fork and push to GitHub**:
   - Fork this repository
   - Make your changes
   - Push to your GitHub repository

2. **Deploy on Render**:
   - Go to [Render.com](https://render.com)
   - Connect your GitHub account
   - Click "New +" → "Web Service"
   - Select your repository
   - Render will automatically detect the `render.yaml` configuration

3. **Set Environment Variables**:
   - In your Render dashboard, add the `GEMINI_API_KEY` environment variable
   - The app will work in offline mode even without an API key

### 🔧 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Optional | Your Google Gemini API key |
| `GEMINI_MODEL` | Optional | Gemini model to use (default: gemini-2.0-flash) |

### 🤖 Chatbot Features

The chatbot includes smart fallback functionality:
- **Online Mode**: Uses Gemini AI for responses
- **Offline Mode**: Provides rule-based financial advice
- **Automatic Switching**: Falls back when API quota is exceeded
- **Manual Control**: Toggle between modes in the sidebar

### 📊 Financial Calculations

- **Savings Rate**: Percentage of income saved
- **Debt-to-Income Ratio**: Financial health indicator
- **Emergency Fund**: 3-6 months of expenses
- **Risk Profiling**: Based on questionnaire
- **Goal Projections**: Future savings calculations

### 🎨 Color Scheme

- 🔵 **Blue**: Dashboard and primary actions
- 🔴 **Red**: Risk analysis and alerts
- 🟢 **Green**: Goal planning and success states
- 🟡 **Golden**: Chatbot and premium features

### ⚠️ Important Notes

- This app is for **educational purposes only** and does **not** replace professional financial, tax, or legal advice.
- All calculations are simplified and use configurable assumptions.
- Your API key is never committed to version control (protected by `.gitignore`).
- The app works fully in offline mode without API dependencies.

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is open source and available under the [MIT License](LICENSE).

### 🆘 Support

If you encounter any issues:
1. Check the [Issues](https://github.com/shweta12017/AI-Financial-advisor/issues) page
2. Create a new issue with detailed information
3. The app includes comprehensive error handling and fallback modes

