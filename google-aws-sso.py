#!/usr/bin/python3
# TODO:
# Remove GAM and use Google API Calls
import argparse
import os
import re
gamdh="python /Users/miguel.mingorance/repos/gamdh/gam.py"
parser = argparse.ArgumentParser(description='Manage AWS SSO configurations for GSuite.')
parser.add_argument('username', metavar='name', help='The username to manage')
parser.add_argument('awsid', nargs='+', help='A list of AWS account IDs')
parser.add_argument('-r', metavar='role', default='sso-administrator', help='The role to assume. Defaults to sso-administrator if not specified.')

args = parser.parse_args()

newAccounts=args.awsid
username=args.username
newRole=args.r

userAWSAccountList = {}
gaminfocommand = gamdh + " info user " + username
os.system(gaminfocommand + "> /tmp/" + username + "_info")
tempFile = "/tmp/" + username + "_info"

with open(tempFile, "rt") as in_file:
	for line in in_file:
		if "arn" in line:
			accountNumber = re.search('[0-9][^:]*', line)
			accountAccess = re.search('sso-[^,]*', line)
			userAWSAccountList[accountNumber.group(0)] = accountAccess.group(0)

if os.path.exists(tempFile):
	os.remove(tempFile)
else:
	print("The file does not exists\nProbably something went wrong when GAM tried to get the info of the user")
	exit(1)

commandline = gamdh + " update user " + username + " AWS_SAML.SessionDuration 28800"

for newAccount in newAccounts:
	commandNewAccounts = " AWS_SAML.IAM_Role value arn:aws:iam::{0}:role/sso/{1},arn:aws:iam::{0}:saml-provider/google".format(newAccount,newRole)

commandOldAccounts = ""
for existingAccount, existingRole in userAWSAccountList.items():
	existingAccount = existingAccount
	existingRole = existingRole
	if existingAccount not in newAccounts:
		commandOldAccounts = commandOldAccounts + (" AWS_SAML.IAM_Role value arn:aws:iam::{0}:role/sso/{1},arn:aws:iam::{0}:saml-provider/google".format(existingAccount,existingRole))
	else:
		continue

commandline = commandline + commandOldAccounts + commandNewAccounts

print("The command that would be run is:")
print(commandline)
print()
print("To run this command, type 'yes' below:")
if input() == "yes":
	os.system(commandline)
else:
	print("No command was run.")
