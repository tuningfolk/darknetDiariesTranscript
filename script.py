from bs4 import BeautifulSoup
import requests
import sys
def extract_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        soup = BeautifulSoup(response.text, 'html.parser')
        all_paragraphs = soup.find_all('p')
        recording_started = False
        extracted_content = []
        
        for p in all_paragraphs:
            text = p.get_text(strip=True)
            
            # Check for start marker
            if "[START OF RECORDING]" in text:
                recording_started = True
            if recording_started:
                extracted_content.append(text)
            if "[END OF RECORDING]" in text:
                break
        return "\n".join(extracted_content)
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching the webpage: {e}"
if len(sys.argv)==1:
    print("Usage: python3 script.py <episode no.>")
    exit(1)
url = "https://darknetdiaries.com/transcript/"+sys.argv[1]
result = extract_content(url)

if result:
    print("Extracted Content:\n")
    print(result)
else:
    print("No content found between the markers.")

