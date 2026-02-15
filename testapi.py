"""
Test script for Movie Recommender API
Run this after starting the API server with: uvicorn app:app --reload
"""

import requests
import json
from typing import List, Dict

# API base URL
BASE_URL = "http://localhost:8000"

def print_response(title: str, response: requests.Response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response:\n{json.dumps(data, indent=2)}")
    except:
        print(f"Response: {response.text}")
    
    print(f"{'='*60}\n")

def test_health_check():
    """Test 1: Health check endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print_response("Test 1: Health Check", response)
    return response.status_code == 200

def test_submit_ratings_new_user():
    """Test 2: Submit ratings for a new user"""
    payload = {
        "user_id": 99999,  # New user ID
        "ratings": [
            {"movie_id": 1, "rating": 5.0},
            {"movie_id": 2, "rating": 4.5},
            {"movie_id": 3, "rating": 3.0},
        ]
    }
    
    response = requests.post(f"{BASE_URL}/rate", json=payload)
    print_response("Test 2: Submit Ratings (New User)", response)
    return response.status_code == 200

def test_submit_ratings_update():
    """Test 3: Update existing ratings"""
    payload = {
        "user_id": 99999,
        "ratings": [
            {"movie_id": 1, "rating": 4.0},  # Update from 5.0 to 4.0
            {"movie_id": 50, "rating": 5.0},  # New movie
        ]
    }
    
    response = requests.post(f"{BASE_URL}/rate", json=payload)
    print_response("Test 3: Update Existing Ratings", response)
    return response.status_code == 200

def test_invalid_rating():
    """Test 4: Submit invalid rating (should fail)"""
    payload = {
        "user_id": 99999,
        "ratings": [
            {"movie_id": 1, "rating": 6.0},  # Invalid: > 5.0
        ]
    }
    
    response = requests.post(f"{BASE_URL}/rate", json=payload)
    print_response("Test 4: Invalid Rating (Should Fail)", response)
    return response.status_code == 422  # Validation error

def test_invalid_movie_id():
    """Test 5: Submit rating for non-existent movie (should fail)"""
    payload = {
        "user_id": 99999,
        "ratings": [
            {"movie_id": 9999999, "rating": 4.0},  # Non-existent movie
        ]
    }
    
    response = requests.post(f"{BASE_URL}/rate", json=payload)
    print_response("Test 5: Invalid Movie ID (Should Fail)", response)
    return response.status_code == 400

def test_recommendations_cold_start():
    """Test 6: Get recommendations for new user (cold start)"""
    response = requests.get(f"{BASE_URL}/recommend?user_id=88888&n=5")
    print_response("Test 6: Recommendations - Cold Start", response)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Got {len(data['recommendations'])} recommendations")
        print(f"✓ Source: {data['source']}")
        return True
    return False

def test_recommendations_personalized():
    """Test 7: Get personalized recommendations (user with ratings)"""
    # First submit enough ratings
    payload = {
        "user_id": 77777,
        "ratings": [
            {"movie_id": i, "rating": 4.0} 
            for i in range(1, 11)  # Rate 10 movies
        ]
    }
    requests.post(f"{BASE_URL}/rate", json=payload)
    
    # Now get recommendations
    response = requests.get(f"{BASE_URL}/recommend?user_id=77777&n=10")
    print_response("Test 7: Recommendations - Personalized", response)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Got {len(data['recommendations'])} recommendations")
        print(f"✓ Source: {data['source']}")
        
        # Print first 3 recommendations
        print("\n📽️ Top 3 Recommendations:")
        for i, rec in enumerate(data['recommendations'][:3], 1):
            rating_str = f" (predicted: {rec['predicted_rating']})" if rec.get('predicted_rating') else ""
            print(f"  {i}. {rec['title']}{rating_str}")
        
        return True
    return False

def test_user_stats():
    """Test 8: Get user statistics"""
    response = requests.get(f"{BASE_URL}/user/77777/stats")
    print_response("Test 8: User Statistics", response)
    return response.status_code == 200

def test_recommendations_invalid_n():
    """Test 9: Request invalid number of recommendations (should fail)"""
    response = requests.get(f"{BASE_URL}/recommend?user_id=1&n=100")  # n > 50
    print_response("Test 9: Invalid n Parameter (Should Fail)", response)
    return response.status_code == 400

def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "🎬"*30)
    print("MOVIE RECOMMENDER API TEST SUITE")
    print("🎬"*30 + "\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Submit Ratings (New User)", test_submit_ratings_new_user),
        ("Update Ratings", test_submit_ratings_update),
        ("Invalid Rating", test_invalid_rating),
        ("Invalid Movie ID", test_invalid_movie_id),
        ("Recommendations (Cold Start)", test_recommendations_cold_start),
        ("Recommendations (Personalized)", test_recommendations_personalized),
        ("User Statistics", test_user_stats),
        ("Invalid n Parameter", test_recommendations_invalid_n),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("Make sure the server is running with:")
        print("  uvicorn app:app --reload")