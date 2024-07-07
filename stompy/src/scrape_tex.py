"""Scrapes a latex url for images and saves them to a directory."""

import arxiv
import requests
import tarfile
import os
from io import BytesIO

# Function to download a file from a URL
def download_file(url):
    response = requests.get(url)
    response.raise_for_status()
    return BytesIO(response.content)

# Function to extract images from a tar.gz file
def extract_images_from_tar(tar_data, extract_path):
    with tarfile.open(fileobj=tar_data, mode="r:gz") as tar:
        tar.extractall(path=extract_path)
        # Find all image files in the extracted content
        images = [os.path.join(extract_path, member.name) for member in tar.getmembers() if member.name.lower().endswith('.png')]
    return images

# Search for papers on arXiv
query = "quantum computing"
search = arxiv.Search(
    query=query,
    max_results=5,  # Adjust the number of results you want to process
    sort_by=arxiv.SortCriterion.SubmittedDate
)

# Directory to save the images
if not os.path.exists('images'):
    os.makedirs('images')

for result in search.results():
    paper_id = result.entry_id.split('/')[-1]
    latex_url = f"https://arxiv.org/e-print/{paper_id}"

    print(f'Downloading LaTeX source for paper {paper_id} from {latex_url}')
    
    try:
        tar_data = download_file(latex_url)
    except Exception as e:
        print(f"Failed to download LaTeX source for paper {paper_id}: {e}")
        continue
    
    extract_path = os.path.join('latex_sources', paper_id)
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    
    try:
        images = extract_images_from_tar(tar_data, extract_path)
    except Exception as e:
        print(f"Failed to extract images for paper {paper_id}: {e}")
        continue

    # Copy images to the 'images' directory with paper ID as part of the filename
    for img_path in images:
        img_filename = os.path.basename(img_path)
        dest_path = os.path.join('images', f"{paper_id}_{img_filename}")
        os.rename(img_path, dest_path)
        print(f"Extracted and saved image {dest_path}")

print("Image extraction complete.")

def main() -> None:
    