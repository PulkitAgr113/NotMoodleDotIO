s = '<div class="b" id="wordDiv'
f = open('skribbl.txt').read().split('\n')
words = []
x = ""
for val in f:
    if s in val:
        val = val.replace('<','>')
        z = val.split('>')
        words.append(z[2])
        x += z[2] + "\n"
print(len(words))
with open('words.txt', 'w') as f:
    f.write(x)