# CILeek
A simple tool to fetch CI Build logs from Travis CI for a certain organisation. 
The tool works by providing it the Organisation name (ex:github) and your Travis Access Token.
In case you need one you can get it from registering here https://travis-ci.org/.

## Prerequisites:
1. Python 2.7
2. python requests module (pip install requests)

## Usage:
python CILeek.py -token 'mytoken' -org 'myorg'
