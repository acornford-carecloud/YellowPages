#import json
#import pycurl


group_assoc = {}
with open('/etc/group','r') as group_file:
    for group in group_file:
        import code; code.interact(local=locals())
        group_data =  group.split(":")
        group_assoc[group_data[2]] = group_data[0]
user_dict = {}
with open('/etc/passwd','r') as user_file:
    for user in user_file:
        import code; code.interact(local=locals())
        user_data = user.split(":")
        user_dict[user[0]] = { "group": group_assoc[user_data[3]], "sudo": False}

print user_dict
