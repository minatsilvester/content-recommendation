lists = [1,2,3,4]
if type(lists) is list:
    print("yes")
dict = locals()
d = 0
for d in dict:
    if "list" in d:
        print("yes")
# print(dict)
# required = dict['lists']
# print(required)
