#!/bin/bash
# GitHub Setup Script for AI Digest Generator

echo "🚀 Setting up AI Digest Generator for GitHub Actions"
echo ""

# Check if .env exists and warn about not committing it
if [ -f ".env" ]; then
    echo "⚠️  WARNING: .env file found!"
    echo "   Make sure to add it to .gitignore and NEVER commit API keys!"
    echo "   Set up repository secrets in GitHub instead."
    echo ""
fi

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
    git add .
    git reset .env  # Make sure .env is not staged
    git commit -m "Initial commit: AI Digest Generator with GitHub Actions"
    echo "✅ Git repository initialized"
    echo ""
else
    echo "📝 Git repository already exists"
    echo ""
fi

echo "📋 Next steps:"
echo "1. Create a new repository on GitHub"
echo "2. Push this code: git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
echo "3. Push: git push -u origin main"
echo "4. Go to GitHub repo → Settings → Secrets and variables → Actions"
echo "5. Add these secrets:"
echo "   - EXA_API_KEY"
echo "   - OPENROUTER_API_KEY"
echo "   - EMAIL_USERNAME (your Gmail)"
echo "   - EMAIL_PASSWORD (Gmail app password)"
echo "   - EMAIL_RECIPIENT (where to send emails)"
echo ""
echo "🎯 The workflow will run every Monday at 9 AM UTC automatically!"
echo "   You can also trigger it manually from the Actions tab."