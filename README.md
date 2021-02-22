# AWS_S3_glacier
Python3 scripts for operations on AWS S3 Glacier

## Documentation
### Before You Begin
What you need: AWS CLI, Boto3  
1. Install AWS CLI version 2:  
https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html  

2. Configure AWS CLI:  
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config  

3. Install Boto3 package (python3):  
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation  

4. Create a AWS S3 Glacier Vault  
Instruction to create a vault on AWS web console window:  
https://docs.aws.amazon.com/amazonglacier/latest/dev/getting-started-create-vault.html  


### Upload an archive using multipart upload
(Recommended for file > 100 MB)  
(For file < 100MB, you can use this instruction: https://docs.aws.amazon.com/code-samples/latest/catalog/python-glacier-upload_archive.py.html)  
1. Initiate, upload and complete the upload ()  
```
python3 glacier_multipart_upload.py -u account_id -v vault_name -f file_name -s chunk_size -o out_file
```
```
Change the arguments based on your needs.  
-u <account id>             the account that owns the vault (optional)  
-s <chunk size>             the size of each part for parallel upload (end with MB or GB)  
-f <file name>              the file you want to upload  
-v <vault name>             the name of the vault  
-o <output file>            the output file name  
** The chunk size must be a megabyte (1024 KB) multiplied by a power of 2  
** If you don’t use -u flag or use -u -, it will set the account id you used to configure the AWS CLI as default account id  
** Number of chunks must be < 10000, total size must be < 5 TB  
```

2. Check if upload is completed (the multipart upload may take up to 24 hrs to finish) (optional)  
```
python3 glacier_list_jobs.py -u account_id -v vault_name -o out_file
```
```
Change the arguments based on your needs.
-u <account id>             the account that owns the vault (optional)
-v <vault name>             the name of the vault
-o <output file>            the output file name
** If you don’t use -u flag or use -u -, it will set the account id you used to configure the AWS CLI as default account id
** You can also go on AWS S3 Glacier console to check if the archive appears there
```


### Retrieve an archive  
1. Initiate archive inventory retrieval to see what archives you have on the Glacier vault  
```
python3 glacier_retrieve_inventory_initiate.py -u account_id -v vault_name -o out_file
```
```
Change the arguments based on your needs.
-u <account id>            the account that owns the vault (optional)
-v <vault name>            the name of the vault
-o <output file>           the output file name
** If you don’t use -u flag or use -u -, it will set the account id you used to configure the AWS CLI as default account id
```

2. Check if archive inventory retrieval initiation is completed (the initiation may take up to 24 hrs to finish) (optional)  
```
python3 glacier_list_jobs.py -u account_id -v vault_name -o out_file
```
```
Change the arguments based on your needs.
-u <account id>             the account that owns the vault (optional)
-v <vault name>             the name of the vault
-o <output file>            the output file name
** If you don’t use -u flag or use -u -, it will set the account id you used to configure the AWS CLI as default account id
```

3. Retrieve the archive inventory to see what archives you have on the Glacier vault  
```
python3 glacier_get_job_output.py -u account_id -v vault_name -j job_id -o out_file
```
```
Change the arguments based on your needs.
-u <account id>             the account that owns the vault (optional)
-j <job id>                 the job id
-v <vault name>             the name of the vault
-o <output file>            the output file name
** Get the job id from the output of the previous step
** If you don’t use -u flag or use -u -, it will set the account id you used to configure the AWS CLI as default account id
```

4. Initiate archive retrieval  
```
python3 glacier_retrieve_archive_initiate.py -u account_id -v vault_name -a archive_id -o out_file
```
```
Change the arguments based on your needs.
-u <account id>             the account that owns the vault (optional)
-a <archive id>             the archive id
-v <vault name>             the name of the vault
-o <output file>            the output file name
** Get the archive id from the output of the previous step
** If you don’t use -u flag or use -u -, it will set the account id you used to configure the AWS CLI as default account id
```

5. Check if archive archive retrieval initiation is completed (the initiation may take up to 24 hrs to finish)  
```
python3 glacier_list_jobs.py -u account_id -v vault_name -o out_file
```
```
Change the arguments based on your needs.
-u <account id>             the account that owns the vault (optional)
-v <vault name>             the name of the vault
-o <output file>            the output file name
** If you don’t use -u flag or use -u -, it will set the account id you used to configure the AWS CLI as default account id
```

6. Retrieve the archive  
```
python3 glacier_retrieve_archive.py -u account_id -s chunk_size -S archive_size -j job_id -v vault_name -o out_file
```
```
Change the arguments based on your needs.
-u <account id>             the account that owns the vault (optional)
-s <chunk size>             the size of each part for parallel upload (end with MB or GB)
-S <archive size> (int)     the size of the archive (integer that indicates the size in bytes)
-j <job id>                 the id of the initiated job
-v <vault name>             the name of the vault
-o <output file>            the output file name
** Get the job id and archive size from the output of the previous step
** If you don’t use -u flag or use -u -, it will set the account id you used to configure the AWS CLI as default account id
```


### Delete an archive
1. Initiate archive inventory retrieval to see what archives you have on the Glacier vault  
```
python3 glacier_retrieve_inventory_initiate.py -u account_id -v vault_name -o out_file
```
```
Change the arguments based on your needs.
-u <account id>             the account that owns the vault (optional)
-v <vault name>             the name of the vault
-o <output file>            the output file name
** If you don’t use -u flag or use -u -, it will set the account id you used to configure the AWS CLI as default account id
```

2. Check if archive inventory retrieval initiation is completed (the initiation may take up to 24 hrs to finish) (optional)  
```
python3 glacier_list_jobs.py -u account_id -v vault_name -o out_file
```
```
Change the arguments based on your needs.
-u <account id>             the account that owns the vault (optional)
-v <vault name>             the name of the vault
-o <output file>            the output file name
** If you don’t use -u flag or use -u -, it will set the account id you used to configure the AWS CLI as default account id
```

3. Retrieve the archive inventory to see what archives you have on the Glacier vault  
```
python3 glacier_get_job_output.py -u account_id -v vault_name -j job_id -o out_file
```
```
Change the arguments based on your needs.
-u <account id>             the account that owns the vault (optional)
-j <job id>                 the job id
-v <vault name>             the name of the vault
-o <output file>            the output file name
** Get the job id from the output of the previous step
** If you don’t use -u flag or use -u -, it will set the account id you used to configure the AWS CLI as default account id
```

4. Delete an archive  
```
python3 glacier_delete _archive.py -u account_id -v vault_name -a archive_id -o out_file
```
```
Change the arguments based on your needs.
-u <account id>             the account that owns the vault (optional)
-a <archive id>             the archive id
-v <vault name>             the name of the vault
-o <output file>            the output file name
** Get the archive id from the output of the previous step
** If you don’t use -u flag or use -u -, it will set the account id you used to configure the AWS CLI as default account id
```