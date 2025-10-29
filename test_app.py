#!/usr/bin/env python3
"""
Simple test script to verify the Flask app functionality
"""

import os
import sys
from unittest.mock import patch, MagicMock

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_counties_list():
    """Test that counties list is properly loaded"""
    from app import COUNTIES
    assert len(COUNTIES) == 22, f"Expected 22 counties, got {len(COUNTIES)}"
    assert "臺北市" in COUNTIES, "臺北市 should be in counties list"
    assert "高雄市" in COUNTIES, "高雄市 should be in counties list"
    print("✓ Counties list test passed")

def test_cache_functions():
    """Test cache functionality"""
    from app import get_cached_forecast, cache_forecast
    
    # Test cache miss
    result = get_cached_forecast("test_location")
    assert result is None, "Cache should be empty initially"
    
    # Test cache store and hit
    test_data = {"test": "data"}
    cache_forecast("test_location", test_data)
    result = get_cached_forecast("test_location")
    assert result == test_data, "Cached data should match stored data"
    print("✓ Cache functions test passed")

def test_process_forecast_data():
    """Test forecast data processing"""
    from app import process_forecast_data
    
    # Mock CWA API response structure
    mock_location_data = {
        "locationName": "臺北市",
        "weatherElement": [
            {
                "elementName": "Wx",
                "time": [
                    {
                        "startTime": "2024-01-01 06:00:00",
                        "endTime": "2024-01-01 18:00:00",
                        "parameter": {
                            "parameterName": "多雲",
                            "parameterValue": "03"
                        }
                    },
                    {
                        "startTime": "2024-01-01 18:00:00",
                        "endTime": "2024-01-02 06:00:00",
                        "parameter": {
                            "parameterName": "陰天",
                            "parameterValue": "04"
                        }
                    }
                ]
            },
            {
                "elementName": "PoP",
                "time": [
                    {
                        "startTime": "2024-01-01 06:00:00",
                        "endTime": "2024-01-01 18:00:00",
                        "parameter": {
                            "parameterName": "20"
                        }
                    },
                    {
                        "startTime": "2024-01-01 18:00:00",
                        "endTime": "2024-01-02 06:00:00",
                        "parameter": {
                            "parameterName": "30"
                        }
                    }
                ]
            },
            {
                "elementName": "MinT",
                "time": [
                    {
                        "startTime": "2024-01-01 06:00:00",
                        "endTime": "2024-01-01 18:00:00",
                        "parameter": {
                            "parameterName": "15"
                        }
                    },
                    {
                        "startTime": "2024-01-01 18:00:00",
                        "endTime": "2024-01-02 06:00:00",
                        "parameter": {
                            "parameterName": "12"
                        }
                    }
                ]
            },
            {
                "elementName": "MaxT",
                "time": [
                    {
                        "startTime": "2024-01-01 06:00:00",
                        "endTime": "2024-01-01 18:00:00",
                        "parameter": {
                            "parameterName": "25"
                        }
                    },
                    {
                        "startTime": "2024-01-01 18:00:00",
                        "endTime": "2024-01-02 06:00:00",
                        "parameter": {
                            "parameterName": "20"
                        }
                    }
                ]
            },
            {
                "elementName": "CI",
                "time": [
                    {
                        "startTime": "2024-01-01 06:00:00",
                        "endTime": "2024-01-01 18:00:00",
                        "parameter": {
                            "parameterName": "舒適"
                        }
                    },
                    {
                        "startTime": "2024-01-01 18:00:00",
                        "endTime": "2024-01-02 06:00:00",
                        "parameter": {
                            "parameterName": "寒冷"
                        }
                    }
                ]
            }
        ]
    }
    
    result = process_forecast_data(mock_location_data)
    
    assert result["location"] == "臺北市", "Location name should be preserved"
    assert len(result["time_slots"]) == 2, "Should have 2 time slots"
    
    first_slot = result["time_slots"][0]
    assert first_slot["weather"] == "多雲", "Weather should be extracted correctly"
    assert first_slot["pop"] == "20", "PoP should be extracted correctly"
    assert first_slot["min_temp"] == "15", "MinT should be extracted correctly"
    assert first_slot["max_temp"] == "25", "MaxT should be extracted correctly"
    assert first_slot["comfort"] == "舒適", "CI should be extracted correctly"
    
    print("✓ Forecast data processing test passed")

def test_app_import():
    """Test that Flask app can be imported and initialized"""
    from app import app
    assert app is not None, "Flask app should be created"
    assert app.name == "app", "App name should be 'app'"
    print("✓ Flask app import test passed")

if __name__ == "__main__":
    print("Running Flask weather app tests...\n")
    
    try:
        test_counties_list()
        test_cache_functions()
        test_process_forecast_data()
        test_app_import()
        
        print("\n🎉 All tests passed! The Flask weather app is ready to use.")
        print("\nTo run the app:")
        print("1. Set your CWA_API_KEY in .env file")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
