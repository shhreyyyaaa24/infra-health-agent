#!/usr/bin/env python3
"""
Create mock screenshots for testing
"""

import os
from PIL import Image, ImageDraw, ImageFont
import sys

def create_mock_screenshot(env_name, output_dir="screenshots"):
    """Create a mock screenshot for an environment"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create a simple image
    width, height = 1200, 800
    image = Image.new('RGB', (width, height), color='#f0f8ff')
    draw = ImageDraw.Draw(image)
    
    # Draw header
    draw.rectangle([0, 0, width, 80], fill='#2c3e50')
    draw.text((20, 25), f"{env_name.upper()} DASHBOARD", fill='white')
    
    # Draw mock dashboard content
    draw.rectangle([20, 100, width-20, height-20], fill='white', outline='#ddd')
    
    # Add some mock metrics
    metrics = [
        ("CPU Usage", "65%", "#28a745"),
        ("Memory", "82%", "#ffc107"),
        ("Disk", "45%", "#28a745"),
        ("Network", "23%", "#28a745")
    ]
    
    y_pos = 120
    for metric, value, color in metrics:
        draw.text((50, y_pos), f"{metric}: {value}", fill=color)
        y_pos += 40
    
    # Add timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((width-200, height-40), timestamp, fill='#666')
    
    # Save the image
    filename = f"{env_name.lower()}_dashboard.png"
    filepath = os.path.join(output_dir, filename)
    image.save(filepath)
    print(f"Created mock screenshot: {filepath}")
    return filepath

if __name__ == "__main__":
    # Create mock screenshots for testing
    environments = ["gcp", "aws", "azure"]
    
    for env in environments:
        create_mock_screenshot(env)
    
    print("✅ Mock screenshots created successfully!")
