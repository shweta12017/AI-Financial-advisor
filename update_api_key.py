#!/usr/bin/env python3
"""
Script to update the Gemini API key in .env file
"""

import os
import sys

def update_api_key(new_api_key):
    """Update the API key in .env file"""
    env_file = ".env"
    
    if not os.path.exists(env_file):
        print("Error: .env file not found!")
        return False
    
    # Read current content
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Replace the API key
    lines = content.split('\n')
    updated_lines = []
    
    for line in lines:
        if line.startswith('GEMINI_API_KEY='):
            updated_lines.append(f'GEMINI_API_KEY={new_api_key}')
        else:
            updated_lines.append(line)
    
    # Write back to file
    with open(env_file, 'w') as f:
        f.write('\n'.join(updated_lines))
    
    print("API key updated successfully!")
    return True

if __name__ == "__main__":
    print("Update Gemini API Key")
    print("=" * 30)
    print("1. Go to: https://aistudio.google.com/app/apikey")
    print("2. Create a new API key")
    print("3. Copy the key")
    print("4. Paste it below")
    print()
    
    new_key = input("Enter your new API key: ").strip()
    
    if new_key and len(new_key) > 20:  # Basic validation
        update_api_key(new_key)
        print("\nYour chatbot should now work!")
        print("Restart your Streamlit app to apply changes.")
    else:
        print("Invalid API key. Please check and try again.")
