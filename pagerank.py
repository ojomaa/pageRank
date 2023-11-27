import os
import random
import re
import sys
from collections import Counter

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    ranks
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Initialize PageRank with 1 - Damping Factor as default
    dictionary_keys= corpus.keys()
    keys_length = len(dictionary_keys)
    PageRank = {key : (1 / keys_length * (1 - damping_factor)) for key in corpus}

    # Probabilities for damping_factor
    if page in corpus: 
        value = corpus[page]
        value_length = len(value)
        for val in value:
            probability = (1 / value_length) * (damping_factor)
            PageRank[val] += probability

        # If theres no outgoing links, equal random probability for all pages
        if not value:
            for key in corpus:
                PageRank[key] += damping_factor / keys_length
    
    # Return PageRank
    return PageRank


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Create the initial sample & its probability distribution
    data = []
    keys = [key for key in corpus.keys()]
    sample = random.choice(keys)
    data.append(sample)
    prob = transition_model(corpus, sample, damping_factor)

    # Based on probability, choose a page
    for i in range(n-1):
        prob = transition_model(corpus, sample, damping_factor)
        sample = random.choices(list(prob.keys()), list(prob.values()))[0]
        data.append(sample)

    # Normalize the data
    counter = Counter(data)
    normalized_pagerank = {page: count / n for page, count in counter.items()}

    # Return the PageRank
    print('Total Samples: ', sum(counter.values()))
    return normalized_pagerank

    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Assign each page a rank of 1/N. N being number of pages in corpus
    count = corpus.items()
    PageRank = {key : (1 / len(corpus)) for key, value in count}

    iterations = 0
    while True:
        new_PageRank = {}
        iterations += 1

        # PR(p) = (1-d/N) + d(sum(PR(i)/NumLinks(i)))
        for key, value in corpus.items():
            first_value = (1 - damping_factor) / len(corpus)
            new_PageRank[key] = first_value
            
            for ke, val in corpus.items():
                if key in val:
                    second_value = damping_factor * (PageRank[ke] / len(val))
                    new_PageRank[key] += second_value

            # Pages with no outgoing links
            if not corpus[key]:
                new_PageRank[key] += damping_factor / len(corpus)
        
        # If no PageRank values change by more than 0.001, break
        if all(abs(new_PageRank[key] - PageRank[key]) < 0.001 for key in corpus):
            break
        
        PageRank = new_PageRank

    print('iterations: ', iterations)

    # Return PageRank
    return PageRank


if __name__ == "__main__":
    main()
