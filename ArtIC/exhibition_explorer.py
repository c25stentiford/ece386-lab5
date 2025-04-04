import requests
import json
from typing import List, Dict, Any, Optional

def search_exhibitions(term: str) -> List[Dict[str, Any]]:
    '''Make a request to exhibitions/search for the search term,
    using Elasticsearch `exists` option to only return results where the `artwork_titles` field is not empty.
    Process the result and return a list of exhibitions with their IDs and titles.
    '''
    base_url = "https://api.artic.edu/api/v1/exhibitions/search"
    
    # Build query to find exhibitions matching the term AND having artwork_titles
    query = {
        "q": term,
        "query": {
            "bool": {
                "must": [
                    {"exists": {"field": "artwork_titles"}}
                ]
            }
        },
        "limit": 50  # Return up to 50 results
    }
    
    # URL encode the JSON query
    params = {"params": json.dumps(query)}
    
    # Make the request
    print(f"Making request to: {base_url} with params: {params}")
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        print(f"Error: API returned status code {response.status_code}")
        return []
    
    # Parse the response
    results = response.json()
    
    # Extract the exhibitions data
    exhibitions = results.get("data", [])
    
    # For debugging, print number of results
    print(f"Found {len(exhibitions)} exhibitions matching '{term}' with artwork titles")
    
    return exhibitions

def get_exhibition_details(exhibition_id: int) -> Optional[Dict[str, Any]]:
    '''Retrieve detailed information about a specific exhibition, including artwork titles.'''
    url = f"https://api.artic.edu/api/v1/exhibitions/{exhibition_id}"
    params = {"fields": "id,title,artwork_titles"}
    
    print(f"Making request to: {url} with params: {params}")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error: API returned status code {response.status_code}")
        return None
    
    return response.json().get("data")

def display_artwork_titles(exhibition: Dict[str, Any]) -> None:
    '''Display the artwork titles for a given exhibition.'''
    print(f"\nArtwork titles for exhibition: {exhibition['title']}")
    print("-" * 60)
    
    artwork_titles = exhibition.get("artwork_titles", [])
    if not artwork_titles:
        print("No artwork titles available for this exhibition.")
        return
    
    for i, title in enumerate(artwork_titles, 1):
        print(f"{i}. {title}")

def main() -> None:
    '''Main function that repeatedly prompts the user and calls search functions.'''
    print("Art Institute of Chicago Exhibition Search")
    print("----------------------------------------")
    
    while True:
        # Get search term from user
        search_term = input("\nEnter a search term for exhibitions (or 'exit' to quit): ")
        if search_term.lower() == 'exit':
            break
        
        # Search for exhibitions
        exhibitions = search_exhibitions(search_term)
        
        if not exhibitions:
            print("No exhibitions found matching your search term with artwork titles.")
            continue
        
        # Display the list of exhibitions
        print("\nFound exhibitions:")
        for i, exhibition in enumerate(exhibitions, 1):
            print(f"{i}. {exhibition['title']}")
        
        # Ask user how many exhibitions they want to view
        while True:
            try:
                selection = input("\nEnter the number of the exhibition you'd like to view (or '0' to search again): ")
                if selection == '0':
                    break
                
                selection = int(selection)
                if 1 <= selection <= len(exhibitions):
                    # Get the selected exhibition
                    selected_exhibition = exhibitions[selection - 1]
                    
                    # Get detailed information about the exhibition
                    exhibition_details = get_exhibition_details(selected_exhibition['id'])
                    
                    if exhibition_details:
                        display_artwork_titles(exhibition_details)
                    else:
                        print("Could not retrieve details for this exhibition.")
                else:
                    print(f"Please enter a number between 1 and {len(exhibitions)}")
            except ValueError:
                print("Please enter a valid number")
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    print("\nThank you for using the Art Institute of Chicago Exhibition Search!")

if __name__ == "__main__":
    main()
