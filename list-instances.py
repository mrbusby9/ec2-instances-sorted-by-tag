#!/usr/bin/env python

import sys
import boto3

#set user params
if len(sys.argv) > 1:
    aws_profile = sys.argv[1]
else:
    print "Please pass AWS profile as an arguement.\nExample: python list-instances.py MY_AWS_PROFILE"
    sys.exit()

#set boto aws profile
boto3.setup_default_session(profile_name=aws_profile)
ec2 = boto3.resource('ec2')

#set dictionary
dictionary = dict()

#Loop through instances and create dictonary with owner as key and object as value
for i in ec2.instances.all():
    ownername = "Unknown"
    if i.tags:
        for tag in i.tags:
            if 'Owner'in tag['Key']:
                ownername = tag['Value']
            #Future addition: logic to compare user supplied key/value pair
            #if UserKey and UserValue found in tags, add to dict, otherwise pass
    key = ownername + "-" + i.id
    dictionary[key] = i

#sort dictionary by key, loop through dictionary and print out data
for key in sorted(dictionary.iterkeys()):
    #Future addition: Allow user to supply list of ec2 attributes to display
    print "%s,%s,%s,%s" % (dictionary[key].id,key.replace("-" + dictionary[key].id,""),dictionary[key].instance_type, dictionary[key].launch_time)
