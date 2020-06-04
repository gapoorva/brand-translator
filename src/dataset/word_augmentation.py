import random
import statistics

# Taken from https://stackoverflow.com/questions/48978610/is-it-possible-to-get-immediate-neighbours-of-a-key-on-keyboard
def get_keys_around(key):
    lines = ['`1234567890-=`', 'qwertyuiop[]', 'asdfghjkl;\'', 'zxcvbnm,./']
    line_index, index = [(i, l.find(key)) for i, l in enumerate(lines) if key in l][0]
    lines = lines[line_index-1: line_index+2] if line_index else lines[0: 2]
    return [
        line[index + i] for line in lines for i in [-1, 0, 1]
        if len(line) > index + i and line[index + i] != key and index + i >= 0]

keys = '`1234567890-=qwertyuiop[]asdfghjkl;\'zxcvbnm,./'
keys_around = { k: get_keys_around(k) for k in keys }

def transform_del(w):
    if len(w) < 3:
        return w

    del_at = random.randint(0, len(w) - 1)
    return w[0:del_at] + w[del_at+1:]

def transform_add(w):
    add_at = random.randint(0, len(w) - 1)
    add_candidates = keys_around[w[add_at]]
    add_ch = add_candidates[random.randint(0, len(add_candidates) - 1)]
    return w[0:add_at] + add_ch + w[add_at:]

def transform_swap(w):
    if len(w) < 3:
        return w

    pos = random.randint(0, len(w) - 2)
    a = w[pos]
    b = w[pos+1]
    return w[0:pos] + b + a + w[pos+2:]

def transform_replace(w):
    pos = random.randint(0, len(w) - 1)
    rpl_candidates = keys_around[w[pos]]
    rpl_ch = rpl_candidates[random.randint(0, len(rpl_candidates) - 1)]
    return w[0:pos] + rpl_ch + w[pos+1:]

class Augmentation():
    def __init__(self):
        self.max_transforms = 3
        self.augmentation_prob = 0.15
        self.transforms = [
            transform_del,
            transform_add,
            transform_swap,
            transform_replace,
        ]
        self.augmentations = 0

    def augment(self, w):
        if random.random() < self.augmentation_prob:
            n = random.randint(0, self.max_transforms)
            self.augmentations += 1
            for i in range(n):
                pick = random.randint(0, len(self.transforms) - 1)
                w = self.transforms[pick](w)
        return w

    def stats(self):
        print('total augmentations', self.augmentations)
