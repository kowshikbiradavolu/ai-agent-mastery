"""
Exercise 1: Weather Fetcher
=============================
Difficulty: Beginner | Time: 1.5 hours

Task:
Create a function that takes a city name, calls the wttr.in API,
and returns a dictionary with temperature and conditions.
Handle errors gracefully.

Instructions:
1. Complete the fetch_weather() function below
2. Handle edge cases: empty city, API timeout, invalid city
3. Test with at least 3 different cities
4. Bonus: Add wind speed and humidity to the output

Run: python exercise_01_weather_fetcher.py
"""

import json
import requests


def fetch_weather(city: str) -> dict:
    """Fetch weather data for a given city.

    Args:
        city: Name of the city

    Returns:
        Dictionary with keys: city, temperature_c, conditions
        (Bonus: wind_kmh, humidity_percent when available)

    Raises:
        ValueError: If city is empty or API call fails
    """
    if not city or not city.strip():
        raise ValueError("City name cannot be empty")
    
    city = city.strip()
    url = f"https://wttr.in/{city}?format=j1"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        raise ValueError("Request timed out")
    except requests.RequestException as e:
        raise ValueError(f"API request failed: {e}")
    
    try:
        data = response.json()
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response")
    
    current = data.get("current_condition")
    if not current:
        raise ValueError("No current weather data available")
    
    cc = current[0]
    temperature_c = cc.get("temp_C")
    if temperature_c is None:
        raise ValueError("Temperature data not available")
    
    weather_desc = cc.get("weatherDesc", [])
    conditions = weather_desc[0]["value"] if weather_desc else "Unknown"
    
    result = {
        "city": city,
        "temperature_c": temperature_c,
        "conditions": conditions
    }
    
    # Bonus fields
    wind_kmh = cc.get("windspeedKmph")
    if wind_kmh is not None:
        result["wind_kmh"] = wind_kmh
    
    humidity = cc.get("humidity")
    if humidity is not None:
        result["humidity_percent"] = humidity
    
    return result


# === Test your implementation ===
if __name__ == "__main__":
    # Test 1: Valid city
    print("Test 1: London")
    result = fetch_weather("London")
    print(result)

    # Test 2: Another valid city
    print("\nTest 2: Tokyo")
    result = fetch_weather("Tokyo")
    print(result)

    # Test 3: Third city
    print("\nTest 3: New York")
    result = fetch_weather("New York")
    print(result)

    # Test 4: Error handling - empty city
    print("\nTest 4: Empty city (should raise ValueError)")
    try:
        fetch_weather("")
    except ValueError as e:
        print(f"Caught error: {e}")

    # Test 5: City with special characters (API will handle gracefully)
    print("\nTest 5: City with special characters")
    result = fetch_weather("São Paulo")
    print(result)

    # Test 3: Error handling - empty city
    print("Test 3: Empty city (should raise ValueError)")
    # try:
    #     result = fetch_weather("")
    # except ValueError as e:
    #     print(f"Caught error: {e}")
