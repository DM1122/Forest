import csv
import os
import progress.bar

class CSVProcessor:
    def __init__(self, inpath, outpath, delim=','):
        self.inpath = inpath
        self.outpath = outpath

        with open(self.inpath, 'r') as fobj:
            reader = csv.reader(fobj, delimiter=delim)
            self.data = [row for row in reader]


    def __str__(self):
        info_str = 'CSV File {} | Size: {}\n'.format(
            hex(id(self.data)),
            len(self.data))

        if len(self.data) <= 10:
            data_str = ''.join(self.data)
            for row in self.data:
                print(row)
        else:
            for row in self.data[:5]:
                print(row)

            print('...')
            
            for row in self.data[len(self.data)-5:]:
                print(row)
        
        output_str = info_str+data_str
        reutur


    def replaceAll(self, query, string):
        for idx, row in enumerate(self.data):
            for idy, col in enumerate(row):
                self.data[idx][idy] = col.replace(query, string)


    def insertChar(self, char, key, after=True):
        '''
        Inserts char at index following first occurence of key in strings fields.
        Useful for configuring delimeters.
        '''

        for idx, row in enumerate(self.data):
            for idy, col in enumerate(row):
                index = col.find(key)
                if after:
                    self.data[idx][idy] = col[:index+1] + char + col[index+1:]
                else:
                    self.data[idx][idy] = col[:index] + char + col[index:]


    def export(self):
        with open(self.outpath, 'w', newline='') as fobj:
            writer = csv.writer(fobj)
            writer.writerows(self.data)


    def removeSpace(self):
        for idx, row in enumerate(self.data):
            for idy, col in enumerate(row):
                self.data[idx][idy] = col.strip()


    def dropEmptyRows(self):
        for idx, row in enumerate(self.data):
            if row == []:
                del self.data[idx]


    def dropEmptyFields(self):
        for idx, row in enumerate(self.data):
            for idy, col in enumerate(row):
                if col == '':
                    del self.data[idx][idy]


    def stringsToNum(self):     # WIP
        for idx, row in enumerate(self.data):
            for idy, col in enumerate(row):
                if col.isdigit() or col.isdecimal():
                    try:
                        self.data[idx][idy] = int(col)
                    except ValueError:
                        self.data[idx][idy] = float(col)


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


def mergeCSV(inpath, outpath):
    filenames = os.listdir(inpath)

    data = []

    bar = progress.bar.Bar('Merging CSV files', max=len(filenames))
    for filename in filenames:
        with open(inpath+filename, 'r') as fobj:
            reader = csv.reader(fobj)
            data.extend([row for row in reader])
        bar.next()
    bar.finish()
    
    # export
    with open(outpath, 'w', newline='') as fobj:
        writer = csv.writer(fobj)
        writer.writerows(data)


if __name__ == '__main__':
    CSVProc = CSVProcessor('data/out2.csv','data/out3.csv', delim='@')
    CSVProc.removeSpace()
    CSVProc.export()

    
    
