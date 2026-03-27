#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import threading
from queue import Queue
from urllib3.exceptions import InsecureRequestWarning

# --- UMBRA_CHI SHADOW CRAWLER PRO v1.2 ---
# "Mapping the shadows before the strike."

# THE SHADOW SILENCER: Suppress SSL warnings for a clean terminal
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class ShadowCrawler:
    def __init__(self, target_url, threads=10):
        self.target_url = target_url
        self.target_domain = urlparse(target_url).netloc
        self.threads = threads
        self.queue = Queue()
        self.queue.put(target_url)
        self.visited = set()

        # PRO TOUCH: User-Agent Spoofing (Looks like a real Chrome browser)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def extract_links(self, url):
        try:
            # BYPASS PART: verify=False allows us to crawl HTTPS even in labs
            response = requests.get(url, headers=self.headers, timeout=5, verify=False)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    full_url = urljoin(url, href)

                    # Logic: Only crawl links that belong to the target domain
                    if urlparse(full_url).netloc == self.target_domain and full_url not in self.visited:
                        self.visited.add(full_url)
                        self.queue.put(full_url)
                        print(f"[+] Discovered: {full_url}")

                        # Auto-save results to a text file
                        with open("targets_found.txt", "a") as f:
                            f.write(full_url + "\n")
        except Exception:
            # Silent fail for broken links to keep the terminal clean
            pass

    def worker(self):
        while not self.queue.empty():
            url = self.queue.get()
            self.extract_links(url)
            self.queue.task_done()

    def run(self):
        print(f"[*] Umbra_Chi beginning reconnaissance on {self.target_url}")
        print(f"[*] Using {self.threads} threads for maximum speed...")

        # Start the thread workers
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

        self.queue.join()
        print(f"[*] Recon Complete. Links saved to targets_found.txt")


if __name__ == "__main__":
    # Ensure the output file is fresh for each run
    open("targets_found.txt", "w").close()

    target = input("Enter target (e.g., https://tutorialspoint.com): ")
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target

    crawler = ShadowCrawler(target)
    crawler.run()