input = #paste that long output from secret file

list = input.split('.') #split the input into dashes-only sequences
bignum = 0
for s in list:
    if len(s) > 0:
        bignum += (1 << (len(s) - 1)) #length of dash sequence indicates the value in array b

out = ""
print(bignum)
while bignum > 0:
    out += chr(bignum % 256) #take last 8 bytes and turn them into char
    bignum = bignum // 256

print(out[::-1]) #we have to reverse the output