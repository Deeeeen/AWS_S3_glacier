#!/usr/bin/env python3

import sys
import logging
import boto3
from botocore.exceptions import ClientError
from optparse import OptionParser

# Usage: python3 glacier_list_jobs.py -v PalmerLab -o out_file

def list_jobs(account_id, glacier_vault, out_file):
	client = boto3.client('glacier')
	# initiate retrieve_inventory
	try:
		response = client.list_jobs(accountId=account_id,
									vaultName=glacier_vault)
	except ClientError as e:
		logging.error(e)
		sys.exit()

	print("List jobs for Glacier vault " + glacier_vault)
	print(response)

	with open(out_file, "w") as file:
		file.write(str(response))

def help():
	print("====== List jobs =====")
	print("List jobs for an AWS Glacier vault")
	print("-u <account id>     the account that owns the vault")
	print("-v <vault name>               the name of the vault")
	print("-o <output file>               the output file name")
	sys.exit()

if __name__=="__main__":
	usage = "usage: %prog [options]"
	parser = OptionParser(usage)
	parser.add_option('-u', type="string", nargs=1, dest="account_id", help="<account id>")
	parser.add_option('-v', type="string", nargs=1, dest="glacier_vault", help="<vault name>")
	parser.add_option('-o', type="string", nargs=1, dest="out_file", help="<output file>")
	parser.add_option('-H', action="store_true", dest="help", help="Displays help screen")
	options, args = parser.parse_args()
	if len(sys.argv) == 1 or options.help != None:
		help()
	if options.account_id != None:
		account_id = options.account_id
	else:
		account_id = "-"
	if options.glacier_vault != None:
		glacier_vault = options.glacier_vault
	else:
		raise "Please provide a vault name"
	if options.out_file != None:
		out_file = options.out_file
	else:
		raise "Please provide an output filename"

	list_jobs(account_id, glacier_vault, out_file)
