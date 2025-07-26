import requests


def test_station_search(station_name: str):
    url = "https://indian-railway-irctc.p.rapidapi.com/api/trains-search/v1/suggest-station"
    
    querystring = {
        "q": station_name,
        "isH5": "true",
        "client": "web"
    }
    
    headers = {
        "x-rapidapi-key": "f95b3738c0msh3c3d40199299a6cp1097f3jsn304050bd7f51",
        "x-rapidapi-host": "indian-railway-irctc.p.rapidapi.com",
        "x-rapid-api": "rapid-api-database"
    }
    
    try:
        print(f"\nSearching for stations matching '{station_name}'...")
        response = requests.get(url, headers=headers, params=querystring)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "body" in data and data["body"]:
                stations = data["body"]
                print(f"\nFound {len(stations)} matching stations:")
                for station in stations:
                    print(f"• {station.get('name', 'N/A')} ({station.get('code', 'N/A')})")
                    if "state" in station:
                        print(f"  State: {station['state']}")
            else:
                print("No stations found.")
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Error occurred: {e}")

def test_train(train_number: str):
    url = f"https://indian-railway-irctc.p.rapidapi.com/api/trains-search/v1/train/{train_number}"
    
    querystring = {"isH5":"true","client":"web"}
    
    headers = {
        "x-rapidapi-key": "f95b3738c0msh3c3d40199299a6cp1097f3jsn304050bd7f51",
        "x-rapidapi-host": "indian-railway-irctc.p.rapidapi.com",
        "x-rapid-api": "rapid-api-database"
    }
    
    try:
        print(f"\nGetting information for train {train_number}...")
        response = requests.get(url, headers=headers, params=querystring)
        print(f"Status code: {response.status_code}")
        
        print(response.json())
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Test station search
    print("\nTesting Station Search:")
    stations_to_search = ["Mumbai", "Delhi", "Bangalore"]
    for station in stations_to_search:
        test_station_search(station)
    
    # Test train info
    print("\nTesting Train Information:")
    trains_to_test = ["12051", "12952"]  # Janshatabdi, Rajdhani
    for train_number in trains_to_test:
        test_train(train_number) 