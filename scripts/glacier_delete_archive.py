#!/usr/bin/env python3

import sys
import logging
import boto3
from botocore.exceptions import ClientError
from optparse import OptionParser

# Usage: python3 glacier_delete_archive.py -v PalmerLab -a archive_id -o out_file

def delete_archive(account_id, archive_id, glacier_vault, out_file):
	client = boto3.client('glacier')
	try:
		response = client.delete_archive(accountId=account_id,
										 vaultName=glacier_vault,
										 archiveId=archive_id)
	except ClientError as e:
		logging.error(e)
		sys.exit()

	print("Delete archive " + archive_id + " on Glacier vault " + glacier_vault)
	print(response)

	with open(out_file, "w") as file:
		file.write(str(response))

def help():
	print("====== Delete an archive =====")
	print("Delete an archive on the AWS Glacier")
	print("-u <account id>     the account that owns the vault")
	print("-a <archive id>                      the archive id")
	print("-v <vault name>               the name of the vault")
	print("-o <output file>               the output file name")
	sys.exit()

if __name__=="__main__":
	usage = "usage: %prog [options]"
	parser = OptionParser(usage)
	parser.add_option('-u', type="string", nargs=1, dest="account_id", help="<account id>")
	parser.add_option('-a', type="string", nargs=1, dest="archive_id", help="<archive id>")
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
	if options.archive_id != None:
		archive_id = options.archive_id
	else:
		raise "Please provide a archive id"
	if options.glacier_vault != None:
		glacier_vault = options.glacier_vault
	else:
		raise "Please provide a vault name"
	if options.out_file != None:
		out_file = options.out_file
	else:
		raise "Please provide an output filename"

	delete_archive(account_id, archive_id, glacier_vault, out_file)
