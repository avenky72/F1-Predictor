"""
Test script to verify everything is set up correctly.
Run this first to make sure your environment works!
"""

import sys
from pathlib import Path

def test_imports():
    """Test that all required packages are installed."""
    print("Testing package imports...")
    
    packages = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'requests': 'requests',
        'fastf1': 'fastf1',
        'dotenv': 'dotenv',
        'tqdm': 'tqdm'
    }
    
    failed = []
    for name, import_name in packages.items():
        try:
            __import__(import_name)
            print(f"✓ {name} imported successfully")
        except ImportError:
            print(f"✗ {name} import failed")
            failed.append(name)
    
    return len(failed) == 0

def test_directories():
    """Test that required directories exist."""
    print("\nTesting directory structure...")
    
    dirs = [
        'data',
        'data/raw',
        'data/processed',
        'notebooks',
        'src',
        'config'
    ]
    
    for dir_path in dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✓ {dir_path}/ exists")
        else:
            print(f"✗ {dir_path}/ missing - creating it")
            path.mkdir(parents=True, exist_ok=True)
    
    return True

def test_environment():
    """Test that .env file exists and is readable."""
    print("\nTesting environment setup...")
    
    if Path('.env').exists():
        print("✓ .env file exists")
        
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        # Check for expected variables
        expected_vars = ['DATA_DIR', 'RAW_DATA_DIR', 'PROCESSED_DATA_DIR']
        for var in expected_vars:
            value = os.getenv(var)
            if value:
                print(f"✓ {var} is set to: {value}")
            else:
                print(f"⚠ {var} is not set")
        
        return True
    else:
        print("✗ .env file missing - create it from .env.example")
        return False

def test_fastf1_connection():
    """Test that we can connect to FastF1."""
    print("\nTesting FastF1 connection...")
    
    try:
        import fastf1
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        cache_dir = os.getenv('FASTF1_CACHE', './data/raw/fastf1_cache')
        
        # Enable cache
        fastf1.Cache.enable_cache(cache_dir)
        print(f"✓ FastF1 cache enabled at: {cache_dir}")
        
        # Try to get a recent session
        print("  Testing data download (this may take a moment)...")
        session = fastf1.get_session(2023, 1, 'FP1')
        print(f"✓ Successfully connected to FastF1")
        print(f"  Test session: {session.event['EventName']} - {session.name}")
        
        return True
    except Exception as e:
        print(f"✗ FastF1 connection failed: {e}")
        return False

def main():
    """Run all tests."""
    print("F1 Prediction System - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("Directory Structure", test_directories),
        ("Environment Setup", test_environment),
        ("FastF1 Connection", test_fastf1_connection)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! Your environment is ready.")
        print("\nNext steps:")
        print("1. Run the first data collection script")
        print("2. Explore the data in a Jupyter notebook")
        print("3. Start building features")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Run: pip install -r requirements.txt")
        print("- Create .env file with required variables")
        print("- Check your internet connection")

if __name__ == "__main__":
    main()