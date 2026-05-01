import requests
from bs4 import BeautifulSoup
import sqlite3

# Function to fetch photonics startups from a webpage
def get_photonics_startups(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Find startup names in a specific HTML structure
        startups = []
        for item in soup.find_all('div', class_='startup-name'):  # Adjust the tag and class
            startups.append(item.get_text(strip=True))

        return startups

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Function to save startups to an SQLite database
def save_to_database(startups, db_name="startups.db"):
    try:
        # Connect to SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create a table for startups if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS photonics_startups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        ''')

        # Insert startups into the table
        for startup in startups:
            try:
                cursor.execute('INSERT INTO photonics_startups (name) VALUES (?)', (startup,))
            except sqlite3.IntegrityError:
                # Skip duplicates
                pass

        # Commit changes and close the connection
        conn.commit()
        conn.close()
        print(f"Saved {len(startups)} startups to the database.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

# Example usage
if __name__ == "__main__":
    url = "https://example.com/photonics-startups"  # Replace with a real URL
    startups = get_photonics_startups(url)
    if startups:
        save_to_database(startups)
        print("Photonics Startups:")
        for startup in startups:
            print(startup)