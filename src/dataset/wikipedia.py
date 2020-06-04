from wikipedia_client import WikipediaClient
from sys import argv
from time import sleep
from random import randint
from os import walk, path, makedirs
from content_processing import ContentProcessor

class WikipediaDataset():
    def __init__(self, infile, outdir):
        self.companies_filename = infile
        self.client = WikipediaClient()
        self.downloads_path = outdir
        self.cp = ContentProcessor()


        # self.load()

    def load(self):
        f = open(self.companies_filename, 'r')
        self.companies = f.read().splitlines()
        f.close()

    def download(self):
        for name in self.companies:
            content = self.client.retrieve_page_content(name)

            outfilename = path.join(self.downloads_path, name.replace(' ', '_'))
            makedirs(path.dirname(outfilename), exist_ok=True)

            f = open(outfilename, 'w')
            f.write(content)
            f.close()
            sleep(5 + randint(-2, 2))

    def parse(self, contentdir):
        for root, _, files in walk(contentdir):
            for filename in files:
                contentfile = open(path.join(root, filename), 'r')
                content = contentfile.read()
                contentfile.close()
                self.cp.add_document(filename, content)
                print('processed', filename)

        docs = self.cp.tfidf_scoring()
        for filename, content in docs.items():
            outfilename = path.join(self.downloads_path, filename)
            makedirs(path.dirname(outfilename), exist_ok=True)
            outfile = open(outfilename, 'w')
            outfile.write(content)
            outfile.close()



if __name__ == "__main__":
    if argv[1] == 'download':
        dataset = WikipediaDataset(argv[2], argv[3])
        dataset.load()
        dataset.download()
    elif argv[1] == 'parse':
        dataset = WikipediaDataset('', argv[3])
        dataset.parse(argv[2])


