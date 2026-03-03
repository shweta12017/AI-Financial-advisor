#!/bin/bash

# AI Financial Advisor Deployment Script
# This script helps you deploy to GitHub and Render

echo "🚀 AI Financial Advisor Deployment Script"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the project root."
    exit 1
fi

# Initialize git repository if not already done
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git branch -M main
else
    echo "✅ Git repository already exists"
fi

# Add all files
echo "📦 Adding files to Git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "🎨 Add AI Financial Advisor with modern UI and offline chatbot

Features:
- Modern blue, red, green, and golden color scheme
- Financial dashboard with risk analysis
- Goal planning and projections
- Smart chatbot with offline fallback
- Render deployment configuration
- Comprehensive documentation

🔐 API keys protected by .gitignore
🚀 Ready for deployment on Render"

# Check if remote exists
if ! git remote get-url origin 2>/dev/null; then
    echo "🔗 Adding remote repository..."
    git remote add origin https://github.com/shweta12017/AI-Financial-advisor.git
else
    echo "✅ Remote repository already configured"
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Deployment files ready!"
echo ""
echo "🌐 Next Steps for Render Deployment:"
echo "1. Go to https://render.com"
echo "2. Connect your GitHub account"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select your repository: shweta12017/AI-Financial-advisor"
echo "5. Render will auto-detect render.yaml"
echo "6. Add GEMINI_API_KEY environment variable (optional)"
echo "7. Click 'Create Web Service'"
echo ""
echo "🎉 Your app will be live at: https://your-app-name.onrender.com"
echo ""
echo "📝 Don't forget to add your API key in Render dashboard!"
echo "   The app works in offline mode even without it."
