import csv
import os

class Stylus:

    def __init__(self, filename):
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write('0')

        self.file = open(filename, 'r+', newline='')            # opens file for both reading and writing. Pointer placed at the beginning. Does not create. Allows subsequent overwrite.
        
        self.reader = csv.reader(self.file, delimiter=',')
        self.writer = csv.writer(self.file)


    def readCell(self, index):
        self.file.seek(0, os.SEEK_SET)          # reset pointer
        
        content = [row for row in self.reader]

        try:
            data = content[index[0]][index[1]]
        except IndexError:
            return None
        else:
            return data


    def writeCell(self, data, index):
        self.file.seek(0, os.SEEK_SET)          # reset pointer

        content = [row for row in self.reader]

        # pad cols
        for row in content:         # pad cols
            pad = index[1] - (len(row)-1)
            row.extend([None for x in range(pad)])
    
        # pad rows
        pad = index[0] - (len(content)-1)
        content.extend([[None for x in range(len(content[0]))] for x in range(pad)])

        # write
        content[index[0]][index[1]] = data
        self.file.seek(0, os.SEEK_SET)
        self.writer.writerows(content)
        


if __name__ == '__main__':
    stylus = Stylus('test.csv')
    stylus.writeCell('x', [5,3])
    print(stylus.readCell([2,2]))
    
    
