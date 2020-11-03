to_skip = ("bad", "naughty","\x01", u'\u0001', b'\x01', b'\x001')
out_handle = open("testout", "w")


with open("testin.txt", "r") as handle:
    for line in handle:
        print('type', type(line), line)
        if line.contains(r'[^\x00-\x7F]+'):
            print('contain special character')
        else:
            print("no it does not contain")



#         if set(line.split(" ")).intersection(to_skip):
#             continue
#         out_handle.write(line)
# out_handle.close()


# import re

# to_skip = ("bad", "naughty","\x01", u'\u0001', b'\x01', b'\x001')
# out_handle = open("testout", "w")

# with open("testin.txt", "r") as handle:
#     # regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
#     regex = re.compile('x[0-9]+')

#     for line in handle:
#         # if set(line.split(" ")).intersection(to_skip):
#         if(regex.search(line) == None):
#             continue
#         out_handle.write(line)
# out_handle.close()





# import re

# to_skip = ("bad", "naughty","\x01", u'\u0001', b'\x01', b'\x001')
# out_handle = open("testout", "w")




# with open("testin.txt", "r") as handle:
#     regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

#     for line in handle:
#         # if set(line.split(" ")).intersection(to_skip):
#         if(regex.search(line) != None):
#             continue
#         out_handle.write(line)
# out_handle.close()







# to_skip = ("bad", "naughty","\x01", u'\u0001', b'\x01', b'\x001')
# out_handle = open("testout", "w")

# with open("testin.txt", "r") as handle:
#     for line in handle:
#         if set(line.split(" ")).intersection(to_skip):
#             continue
#         out_handle.write(line)
# out_handle.close()


# def ascii_lines(iterable):
#     for line in iterable:
#         if all(ord(ch) < 128 for ch in line):
#             yield line

# f = open('testin.txt', encoding="ascii")
# for line in ascii_lines(f):
#     print(line)



# cat testin.txt | tr -cd '[:alnum:]\n\r~!@#$%^&*()-_=+{}\|;:<>,./?"`' | sed '/^$/d' > testout



# to_skip = ("bad", "naughty","\x01", u'\u0001', r'\x001')
# out_handle = open("testout", "w")

# with open("testin.txt", "r") as handle:
#     for line in handle:
#         if set(line.split(" ")).intersection(to_skip):
#             continue
#         print(line)
#         out_handle.write(line)
# out_handle.close()






