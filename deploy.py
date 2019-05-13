#!/usr/bin/python3

import sys
import subprocess

def main():
    bucket_name = input("Please enter s3 bucket name: ")
    response = input("Sync s3 bucket from jekyll build? (y/n)")
    if 'y' in response:
        run_shell_command("cd ./src/ && jekyll build")
        output = run_shell_command(f"aws s3 sync ./src/_site/ s3://{bucket_name}")
        print(f"Output of command: {output}\n-----")
    response = input("Invalidate Cloudfront? (y/n) ")
    if 'y' in response:
        from _cloudfront_mappings import cloudfront_mappings
        output = run_shell_command(
            f"aws cloudfront create-invalidation " + \
            f"--distribution-id {cloudfront_mappings[bucket_name]} " + \
            f"--paths '/*'")
        print(f"output of command: {output}\n-----")
        return 0
    return 0

def run_shell_command(cmd):
    try:
        print("Currently running command '{}'".format(cmd))
        byte_output = subprocess.check_output(cmd,
                                          stderr=subprocess.STDOUT,
                                          shell=True)
        str_output = byte_output.decode("utf-8")
        #log.debug(str_output)
        return str_output
    except subprocess.CalledProcessError as e:
        print("cmd failed, returned non-zero code. Output:\n"\
                 "{}".format(e.output.decode("utf-8")))
        raise e

if __name__ == "__main__":
    sys.exit(main())
