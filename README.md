# Emory Researchers Info Scraper

This repository contains code and resources for scraping information about researchers affiliated with Emory University. The primary objective is to automate the discovery of researcher profiles, extract relevant details (e.g., email, research interests, biography), and identify valid headshot images. This pipeline integrates web scraping, HTML parsing, image classification, and prompt-based field extraction using language models.

---

## Repository Structure

- **data/**: Contains metadata and URLs generated from Google Custom Search queries.
  
- **images/**: Stores raw images retrieved from the scraped webpages. Post-processing step filters images, retaining only those that appear to be researcher headshots.

- **info/**: Contains the cleaned and structured researcher information in JSON format.

- **model/**: Contains the CV model used for headshot classification. Used to filter out non-researcher images (e.g., logos, diagrams).

- **prompt/**: Stores prompt templates for the OpenAI agents.

- `*.py` files: Python scripts that run the scraping and processing tasks. Each script’s usage is defined within the file itself.

---

## Workflow Overview

1. **Initial Query Generation:**  
   Given a list of researcher names, we construct queries in the form of `"first_name + last_name + emory"`. These queries are sent to the Google Custom Search API to retrieve relevant webpages.  
   - The top ranked result is saved to `data/queried_urls.json`.

2. **Web Scraping & Data Retrieval:**  
   Using libraries like **BeautifulSoup** and **Selenium**, we fetch and parse the HTML of the identified webpages.  
   - Text and images from the identified page are saved temporarily for further processing.

3. **Text Processing & Field Extraction:**  
   1. **Identify Relevant Sections:**  
      Extract webpage containers likely to contain researcher info (e.g., `<div class="personal-information">`).  
      
   2. **GPT-4o Extraction Agent:**  
      Pass the selected text sections into a GPT-4o model agent using a prompt defined in `prompt/`. This agent extracts key fields such as `email`, `research_interests`, `bio`, and more.
   
   3. **GPT-4omini Mapping Agent:**  
      The extracted fields are then refined and mapped to the designated schema using a second agent, GPT-4omini. The mapping prompt is also provided in the `prompt/` directory.
   
   4. **Result Storage:**  
      The final cleaned and structured JSON (per researcher) is saved in `info/firstname_lastname.json`.

4. **Image Processing & Classification:**  
   1. **Image Retrieval:**  
      All images from the webpage are initially saved to `images/`.

   2. **Image Filtering (CV model):**  
      A local CV model (stored in `model/`) filters out non-headshot images. This removes logos, icons, and irrelevant images, leaving only what appears to be a researcher headshot.

5. **Final Result:**
   - The final scraped results are correspondingly saved in `info\` and `images\` folders. The merged excel file is saved in `complete list.xlsx`.
