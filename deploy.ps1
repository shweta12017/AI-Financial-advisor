# AI Financial Advisor Deployment Script (PowerShell)
# This script helps you deploy to GitHub and Render

Write-Host "🚀 AI Financial Advisor Deployment Script" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "app.py")) {
    Write-Host "❌ Error: app.py not found. Please run this script from the project root." -ForegroundColor Red
    exit 1
}

# Initialize git repository if not already done
if (-not (Test-Path ".git")) {
    Write-Host "📁 Initializing Git repository..." -ForegroundColor Blue
    git init
    git branch -M main
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

# Add all files
Write-Host "📦 Adding files to Git..." -ForegroundColor Blue
git add .

# Commit changes
Write-Host "💾 Committing changes..." -ForegroundColor Blue
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
$remoteExists = git remote get-url origin 2>$null
if (-not $remoteExists) {
    Write-Host "🔗 Adding remote repository..." -ForegroundColor Blue
    git remote add origin https://github.com/shweta12017/AI-Financial-advisor.git
} else {
    Write-Host "✅ Remote repository already configured" -ForegroundColor Green
}

# Push to GitHub
Write-Host "📤 Pushing to GitHub..." -ForegroundColor Blue
git push -u origin main

Write-Host ""
Write-Host "✅ Deployment files ready!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Next Steps for Render Deployment:" -ForegroundColor Cyan
Write-Host "1. Go to https://render.com"
Write-Host "2. Connect your GitHub account"
Write-Host "3. Click 'New +' → 'Web Service'"
Write-Host "4. Select your repository: shweta12017/AI-Financial-advisor"
Write-Host "5. Render will auto-detect render.yaml"
Write-Host "6. Add GEMINI_API_KEY environment variable (optional)"
Write-Host "7. Click 'Create Web Service'"
Write-Host ""
Write-Host "🎉 Your app will be live at: https://your-app-name.onrender.com" -ForegroundColor Yellow
Write-Host ""
Write-Host "📝 Don't forget to add your API key in Render dashboard!" -ForegroundColor Magenta
Write-Host "   The app works in offline mode even without it." -ForegroundColor Magenta

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
