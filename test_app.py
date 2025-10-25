#!/usr/bin/env python3
"""Test script to verify Finglish application works"""

import os
import sys

# Set environment variable
os.environ['forvo_key'] = 'demo_key'

try:
    # Test imports
    from server import app
    from model import connect_to_db, Word, User, Vocabulary
    print("✅ All imports successful")
    
    # Connect to database
    connect_to_db(app)
    print("✅ Database connection successful")
    
    # Test database queries
    with app.app_context():
        word_count = Word.query.count()
        print(f"✅ Database has {word_count} words")
        
        # Test a simple query
        first_word = Word.query.first()
        if first_word:
            print(f"✅ Sample word: {first_word.english} -> {first_word.farsi}")
        
    print("\n🎉 SUCCESS: Your Finglish application is working!")
    print("\nTo start the server, run:")
    print("export forvo_key='your_actual_forvo_key'")
    print("python3 server.py")
    print("\nThen visit: http://localhost:5000")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)
