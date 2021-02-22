#!/usr/bin/env python3

import sys
import math
import logging
import boto3
from botocore.exceptions import ClientError
from optparse import OptionParser

# Usage: python3 glacier_retrieve_archive.py -v glacier_vault -j job_id -s chunk_size -S archive_size -o out_file

def retrieve_archive(account_id, archive_size, job_id, chunk_size, glacier_vault, out_file):
	client = boto3.client('glacier')
	# retrieve archive
	parts = math.ceil(archive_size / chunk_size)
	try:
		with open(out_file, "wb") as file:
			for p in range(parts):
				print(str(p))
				lower = p * chunk_size
				upper = lower + chunk_size - 1
				if upper > archive_size:
					upper = archive_size - 1
				response = client.get_job_output(accountId=account_id,
										vaultName=glacier_vault, jobId=job_id,
										range='bytes={}-{}'.format(lower, upper))
				file.write(response['body'].read())
	except ClientError as e:
		logging.error(e)
		sys.exit()

	print("Get job output for job " + job_id + " on Glacier vault " + glacier_vault)

def help():
	print("====== Retrieve archive data =====")
	print("Retrieve archive data from the AWS Glacier")
	print("-u <account id>             the account that owns the vault")
	print("-s <chunk size>   the size of each part for parallel upload")
	print("-S <archive size> (int)             the size of the archive")
	print("-j <job id>                     the id of the initiated job")
	print("-v <vault name>                       the name of the vault")
	print("-o <output file>                       the output file name")
	sys.exit()

if __name__=="__main__":
	usage = "usage: %prog [options]"
	parser = OptionParser(usage)
	parser.add_option('-u', type="string", nargs=1, dest="account_id", help="<account id>")
	parser.add_option('-s', type="string", nargs=1, dest="chunk_size", help="<chunk size>")
	parser.add_option('-S', type="int", nargs=1, dest="archive_size", help="<archive size>")
	parser.add_option('-j', type="string", nargs=1, dest="job_id", help="<job id>")
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
	if options.archive_size != None:
		archive_size = options.archive_size
	else:
		raise "Please provide the archive size in integer (bytes)"
	if options.chunk_size != None:
		if options.chunk_size[-2:].upper() == "GB":
			chunk_size = int(options.chunk_size[:-2]) * (2 ** 30) # GB to bytes
		elif  options.chunk_size[-2:].upper() == "MB":
			chunk_size = int(options.chunk_size[:-2]) * (2 ** 20) # MB to bytes
		else:
			logging.error("please enter the chunk size in MB or GB")
			sys.exit()
	else:
		chunk_size = archive_size
	if options.job_id != None:
		job_id = options.job_id
	else:
		raise "Please provide a job id"
	if options.glacier_vault != None:
		glacier_vault = options.glacier_vault
	else:
		raise "Please provide a vault name"
	if options.out_file != None:
		out_file = options.out_file
	else:
		raise "Please provide an output filename"

	retrieve_archive(account_id, archive_size, job_id, chunk_size, glacier_vault, out_file)
