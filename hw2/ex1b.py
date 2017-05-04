import numpy

data = numpy.loadtxt("Data/docword.kos.txt", skiprows=3)


def jaccard(a, b):
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


array = []
sett = set()
for line in range(0, len(data)):
    sett.add(data[line, 1])
    if data[line, 0] != data[line - 1, 0] and line > 1:
        array.append(sett)
        sett = set()
    if line == (len(data) - 1):
        array.append(sett)
text = open("output.txt", "w")
count = 0
for i in range(0, 3430):
    for j in range(i + 1, 3430):
        result = jaccard(array[i], array[j])
        text.write(str(result))
    text.write("\n")
text.close

wordset = set(array)
print(len(wordset))
# c_mat=numpy.empty([6906,3430])
# for i in range(0,6906):
# for j in range(0,3430):
# if list(array)[i] in array[j]:
# c_mat[i,j]=1
# else:
# c_mat[i,j]=0
