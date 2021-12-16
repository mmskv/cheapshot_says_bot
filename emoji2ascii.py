import os
from os import listdir
from os.path import isfile, join

import emoji

emojis = [f for f in listdir(".") if isfile(join(".", f))]
for e in emojis:
    name = emoji.demojize(e).replace("_face:", ":")
    if name != e:
        os.rename(e, name)
    else:
        print(e, "is not an emoji")
