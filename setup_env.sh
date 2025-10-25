#!/bin/bash
# Setup script for Finglish application

# Set the Forvo API key (you'll need to get this from forvo.com)
export forvo_key="demo_key_placeholder"

# Create the database and run the seed script
python3 seed.py

echo "Setup complete! You can now run: python3 server.py"
