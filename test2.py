import sys
from rapidocr import RapidOCR

engine = RapidOCR()

result = engine(sys.argv[1])

line1 = result.txts[-2]
line2 = result.txts[-1]

print(line1)
print(line2)