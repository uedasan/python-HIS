from pathlib import Path
import numpy as np
from tqdm import tqdm

class HISReader():

    def __init__(self, path):
        self.fd = open(path, "rb")
        header,comment = self.__read_header()
        self.length = header[7]
        self.count = 0
        self.fd.seek(0)

    def __len__(self):
        return self.length

    def __iter__(self):
        return self

    def __next__(self):
        image = self.read_next_image()
        if image is None:
            raise StopIteration()
        return image

    def read_next_image(self):
        if self.count == self.length:
            return None
        self.header, self.comment = self.__read_header()
        if lsef.header[6]!=2:
            raise NotImplementedError("only 16bit type is supported")
        width, height = self.header[2:4]
        image = np.fromfile(self.fd, f"{width}H", height)
        self.count += 1
        return image

    def __read_header(self):
        fmt = "2a,H,H,H,H,H,H,i4,H,H,d,i4,30b"
        self.header = tuple(np.fromfile(self.fd, fmt, 1)[0])
        assert(self.header[0] == b"IM")
        self.comment = np.fromfile(self.fd, f"a{self.header[1]}", 1)[0]
        return self.header, self.comment


def main():
    reader = HISReader("a.HIS")
    for i, image in enumerate(tqdm(reader)):
        pass


if __name__=="__main__":
    main()
