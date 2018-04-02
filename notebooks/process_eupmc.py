import re



def get_paper_subdirectories(matching_papers):
    """
    Return a list of subdirectory names returned by getpapers
    For each line in the index file of matching_papers, strip the
    start of the line (http://europepmc.org/articles/)
    """

    eupmc_header = "http://europepmc.org/articles/"
    subdirs = []

    with open(matching_papers, 'r') as f:
        for line in f:
            if line.startswith(eupmc_header):
                terms = line.split("/")
                subdirs.append(terms[-1].rstrip())

    return subdirs
