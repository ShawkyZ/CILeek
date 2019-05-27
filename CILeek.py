#!/usr/bin/env python

import json
import requests
import sys
import argparse
import codecs

parser = argparse.ArgumentParser(description='Fetch log files from Travis CI')
parser.add_argument('-token', type=str,
                    help='Travis CI Access Token')
parser.add_argument('-org',  type=str,
                    help='Travis CI Orginisation Name ex: microsoft')
parser.add_argument('--dir', type=str, nargs='?',
                    help='Directory to save the fetched log files')

args = parser.parse_args()
print(args)
if args.token:
    token = args.token
if args.org:
    org = args.org
if args.dir:
    saveDir = args.saveDir
    if not saveDir.endsWith("/"):
        saveDir += "/"
else:
    saveDir = ""
header = {
    "Travis-API-Version" : "3",
    "User-Agent" : "API Tester",
    "Authorization" : "token "+token,
}
endpoint = "https://api.travis-ci.org"

def getRepositories():
    return requests.get(endpoint + "/owner/"+org+"/repos", headers= header).json()

def getLog(jobId):
    return requests.get(endpoint + "/v3/job/"+str(jobId)+"/log.txt", headers= header).text

def createLogFile(jobId, repoName, content):
    fileName = saveDir+str(jobId)+"_"+repoName+"_log.txt"
    f = codecs.open(fileName, "a+",  encoding='utf8')
    f.write(content)
    f.close()
    print(fileName+" Created")

for repo in getRepositories()['repositories']:
    try:
        buildsEndpoint = endpoint + "/repo/"+str(repo['id'])+"/builds"
        builds = requests.get(buildsEndpoint, headers= header).json()
        joblist = [job for build in builds['builds'] for job in build['jobs']]
        for job in joblist:
            logContent = getLog(job['id'])
            createLogFile(job['id'], repo['name'], logContent)
    except Exception as e:
        print(type(e))
        print(str(e))
        pass