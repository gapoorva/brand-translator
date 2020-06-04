import word_augmentation
import os
import random
import sys

def get_company_name(filename):
    return filename.replace('_', ' ')

class DescriptorsDataset():
    def __init__(self, textcontentdir, classifydir):
        self.textcontentdir = textcontentdir
        self.classifydir = classifydir
        self.text_contents = {}
        self.co_ex_n = 20
        self.dsc_ex_n = 80
        self.dsc_ex_len = 3
        self.augmentation = word_augmentation.Augmentation()



    def generate_descriptors(self):
        for root, dirs, files in os.walk(self.textcontentdir):
            for filename in files:
                filepath = os.path.join(root, filename)

                descriptors = open(filepath, 'r').read().split()
                company_name = get_company_name(filename).split()
                descriptors.extend(company_name)

                for i in range(self.co_ex_n):
                    example = company_name.copy()
                    example = [ self.augmentation.augment(w) for w in example ]

                    examplefilename = os.path.join(self.classifydir, filename, str(i).zfill(4) + '.txt')
                    os.makedirs(os.path.dirname(examplefilename), exist_ok=True)
                    f = open(examplefilename, 'w')
                    f.write(' '.join(example))
                    f.close()

                for j in range(self.co_ex_n, self.co_ex_n + self.dsc_ex_n):
                    example = random.choices(descriptors.copy(), k=self.dsc_ex_len)
                    example = [ self.augmentation.augment(w) for w in example ]

                    examplefilename = os.path.join(self.classifydir, filename, str(j).zfill(4) + '.txt')
                    os.makedirs(os.path.dirname(examplefilename), exist_ok=True)
                    f = open(examplefilename, 'w')
                    f.write(' '.join(example))
                    f.close()


if __name__ == "__main__":
    generator = DescriptorsDataset(sys.argv[1], sys.argv[2])
    generator.generate_descriptors()