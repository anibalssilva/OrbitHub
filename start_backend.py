import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Test the import
try:
    from app.data_access import filter_satellites
    result = filter_satellites(limit=1)
    print(f"✓ Backend loaded successfully!")
    print(f"✓ Data access working: {len(result)} satellite(s) loaded")
    if result:
        print(f"✓ Fields available: {list(result[0].keys())}")
        print(f"✓ Sample data: {result[0]}")
except Exception as e:
    print(f"✗ Error loading backend: {e}")
    sys.exit(1)

# Start uvicorn
print("\n🚀 Starting Uvicorn server...")
os.chdir('backend')
os.system('python -m uvicorn app.main:app --port 8000 --reload')

