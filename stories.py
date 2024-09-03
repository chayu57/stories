import http.server
import socketserver
import urllib.request

PORT = 8000


def scrape_time_stories():
    try:
        url = "https://time.com"
        response = urllib.request.urlopen(url)
        web_content = response.read().decode('utf-8')
        
       
        print("Fetched HTML content from Time.com")


        stories = []

        
        start_index = web_content.find('LATEST STORIES')
        if start_index == -1:
            print("Could not find 'LATEST STORIES' section.")
            return "[]"

        end_index = web_content.find('</ul>', start_index)
        latest_stories_section = web_content[start_index:end_index]

        print("Extracted 'LATEST STORIES' section.")

       
        while '<a href="' in latest_stories_section:
            link_start = latest_stories_section.find('<a href="') + len('<a href="')
            link_end = latest_stories_section.find('"', link_start)
            link = latest_stories_section[link_start:link_end]
            
            title_start = latest_stories_section.find('">', link_end) + len('">')
            title_end = latest_stories_section.find('</a>', title_start)
            title = latest_stories_section[title_start:title_end]
            
            stories.append({"title": title, "link": url + link})
            
            
            latest_stories_section = latest_stories_section[title_end:]

     
        print("Extracted stories:", stories[:6])

        
        return str(stories[:6]).replace("'", '"')
    except Exception as e:
        print("Error during scraping:", e)
        return "[]"


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/getTimeStories':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                stories_json = scrape_time_stories()
                self.wfile.write(stories_json.encode())
                print("Response sent successfully.")
            except Exception as e:
                print("Error in handling request:", e)
                self.send_response(500)
                self.end_headers()


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()

