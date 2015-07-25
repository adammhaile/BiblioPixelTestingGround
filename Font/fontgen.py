font_base = """
FONT = [
%FONT_DATA%
]
"""
import sys
def getChar(c):
    if c < 32:
        return "SPECIAL"
    elif c == 32:
        return "Space"
    else:
        return chr(c)

font = open(sys.argv[1])

default = int(font.readline())
print "Default Char: %d" % default

chars = {}
widths = {}
offsets = {}
offset = 0

while True:
    id = font.readline()

    if id.startswith("EOF"):
        break;
    split = id.split('-')

    code = int(split[0])
    width = int(split[1])
    char = [0]*3
    print code
    print char
    for y in range(6):
        line = font.readline()

        c = 0
        for x in range(len(line)):
            if line[x] == '0':
                char[x] |= (1 << y)
    chars[code] = char
    widths[code] = width
    offset += width
    offsets[code] = offset

char_count = len(chars)
print "Total Chars: %d" % char_count

count = 0
index_list = ""
offset_list = ""
width_list = ""
char_list = ""
offset = 0

for i in range(255):

    if not chars.has_key(i):
        i = default
    char_list += "    [%s], # %s\n" % ((','.join('0x%02x' % x for x in chars[i])), getChar(i))

output = font_base.replace("%FONT_DATA%", char_list)
outfile = open("font.py", mode = 'w+')
outfile.write(output)
outfile.close()

print "Completed writing font"
