import random, sys
text = "Player:4:5\n"
addtext = "Sequence:"
sequence_length = random.randint(3, 10)
seq_opt = ["j", "a", "d"]
seq = ["j", "a", "d"]

for x in range(sequence_length - 1):
    seq.append(random.choice(seq_opt))
random.shuffle(seq)
print (seq)

for x in range(len(seq)):
    if x == len(seq) - 1:
        addtext += seq[x]

    else:
        addtext += seq[x] + ":"

text += addtext + "\nDistance:10000\n"
dist = 600
choices = ["Pebble:", "Enemy:4:", "2Peb", "Bird:4:"]

while True:
    sprite = random.choice(choices)

    if sprite == "2Peb":
        text += "Pebble:" + str(dist) + "\n"
        dist += 100
        text += "Pebble:" + str(dist) + "\n"

    else:
        text += sprite + str(dist) + "\n"

    if dist >= 9000:
        break

    dist += 600
print (text)
input("Are you sure? press enter for this file name: " + sys.argv[1])

try:
    with open(sys.argv[1], "w") as fh:
        fh.write(text)
        
except Exception as err:
    print (err)
