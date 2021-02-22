#!/usr/bin/env python3

import os
import sys
import math
import logging
import boto3
from botocore.exceptions import ClientError
from botocore.utils import calculate_tree_hash
from optparse import OptionParser

# Usage: python3 glacier_upload.py -v PalmerLab -f file_name -s 1GB -o out_file

def multipart_upload(account_id, chunk_size, file_name, glacier_vault, out_file):
	file_size = os.path.getsize(file_name)
	parts = math.ceil(file_size / chunk_size)

	client = boto3.client('glacier')
	try:
		# initiate initiate_multipart_upload
		upload_obj = client.initiate_multipart_upload(accountId=account_id,
												vaultName=glacier_vault,
												archiveDescription=file_name,
												partSize=str(chunk_size))
		print(upload_obj)
		# upload file in chunks
		with open(file_name, 'rb') as upload:
			for p in range(parts):
				lower = p * chunk_size
				upper = lower + chunk_size - 1
				if upper > file_size:
					upper = file_size - 1
				file_part = upload.read(chunk_size)

				up_part = client.upload_multipart_part(accountId=account_id,
									vaultName=glacier_vault,
									uploadId=upload_obj['uploadId'],
									range='bytes {}-{}/*'.format(lower, upper),
									body=file_part)
		# complete the upload
		checksum = calculate_tree_hash(open(file_name, 'rb'))
		complete_upload = client.complete_multipart_upload(accountId=account_id,
												vaultName=glacier_vault,
												uploadId=upload_obj['uploadId'],
												archiveSize=str(file_size),
												checksum=checksum)
	except ClientError as e:
		logging.error(e)
		sys.exit()

	print("complete archiving " + file_name + " in Glacier vault " + glacier_vault)
	print(complete_upload)

	with open(out_file, "w") as file:
		file.write(str(complete_upload))

def help():
	print("====== Multipart upload =====")
	print("Initiate, upload and complete the upload to AWS Glacier")
	print("-u <account id>             the account that owns the vault")
	print("-s <chunk size>   the size of each part for parallel upload")
	print("-f <file name>                  the file you want to upload")
	print("-v <vault name>                       the name of the vault")
	print("-o <output file>                       the output file name")
	print("number of chunks must be < 10000, total size must be < 5 TB")
	sys.exit()

if __name__=="__main__":
	usage = "usage: %prog [options]"
	parser = OptionParser(usage)
	parser.add_option('-u', type="string", nargs=1, dest="account_id", help="<account id>")
	parser.add_option('-s', type="string", nargs=1, dest="chunk_size", help="<chunk size>")
	parser.add_option('-f', type="string", nargs=1, dest="file_name", help="<file name>")
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
	if options.chunk_size != None:
		if options.chunk_size[-2:].upper() == "GB":
			chunk_size = int(options.chunk_size[:-2]) * (2 ** 30) # GB to bytes
		elif  options.chunk_size[-2:].upper() == "MB":
			chunk_size = int(options.chunk_size[:-2]) * (2 ** 20) # MB to bytes
		else:
			logging.error("please enter the chunk size in MB or GB")
			sys.exit()
	else:
		raise "Please provide a chunk size"
	if options.file_name != None:
		file_name = options.file_name
	else:
		raise "Please provide a file name"
	if options.glacier_vault != None:
		glacier_vault = options.glacier_vault
	else:
		raise "Please provide a vault name"
	if options.out_file != None:
		out_file = options.out_file
	else:
		raise "Please provide an output filename"

	multipart_upload(account_id, chunk_size, file_name, glacier_vault, out_file)
