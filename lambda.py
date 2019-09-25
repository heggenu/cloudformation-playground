from __future__ import print_function
from distutils.dir_util import copy_tree
from botocore.vendored import requests
from jinja2 import Template

import os
import subprocess
import json
import boto3
import logging
import jinja2
import urllib
import re
      
def handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    logger.info('Received event: {}'.format(json.dumps(event)))

    name = event["ResourceProperties"]["Name"]
    print(name)
    gitrepo=event["ResourceProperties"]["Value"]
    print(gitrepo)
    bobba=event["ResourceProperties"]["Test"]
    print(bobba)

    # initialize our response
    response_data = {}

    try:
      ssm=boto3.client('ssm')
    except Exception as e:
      logger.info('boto3.client failure: {}'.format(e))
      send(event, context, FAILED, response_data)
    
    if event['RequestType'] == 'Create':

      #DEFAULT VALUES
      aws_account = '1234567890'
      aws_opp_account =  '0987654321'
      environment_type =  'test'
      region =  'eu-central-1'
      product_domain_name = 'demo'
      jenkins_config_url = 'https://jenkins.com'
      http_proxy = "https://proxy.com"
      vpc_id = "vpc-123456"
      
      # The Git repository to clone
      remote_repository = 'https://github.com/kentrikos/template-environment-configuration.git'
      new_remote_repository = gitrepo
      git_command = 'clone --depth 1 -b jinja_templating --single-branch'
      git_command_add_origin = 'remote add origin'
      
      subprocess.run(["rm","-rf", "/tmp/template-environment-configuration"])
      subprocess.run(["rm","-rf", "/tmp/id_rsa"])

      os.environ["GIT_SSH_COMMAND"] = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /tmp/id_rsa"

      #newFile = open('/tmp/known_hosts','w+')
      #newFile.write('github.com,140.82.118.3,140.82.118.4  ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==')
      #newFile.close()
      
      ssm=boto3.client('ssm')
      privateSSHKeyParameter=ssm.get_parameter(
                    Name='/my/securestring/data',
                    WithDecryption=True
                  )

      privateSSHKey=privateSSHKeyParameter['Parameter']['Value']

      privateSSHKeyBegin = re.search(r'^(-----BEGIN ([^-]+)-----)',privateSSHKey).group(0)
      privateSSHKeyEnd = re.search(r'(-----END ([^-]+)-----)',privateSSHKey).group(0)
      privateSSHKeyBase64 = re.sub(r'^\s*(?:\-+(?:.*?)\-+)?\s*((?:[A-Za-z0-9\+\/]\s?)+={0,2})\s*(?:\-+(?:.*?)\-+)?\s*$', '\g<1>', privateSSHKey)
      privateSSHKeyBase64=privateSSHKeyBase64.replace(' ','\n')

      privateSSHKey=privateSSHKeyBegin+'\n'+privateSSHKeyBase64+'\n'+privateSSHKeyEnd+'\n '

      keyFile = open('/tmp/id_rsa','w+')
      keyFile.write(privateSSHKey)
      keyFile.close()

      subprocess.run(["chmod","700", "/tmp/id_rsa"])

      # Clone the remote Git repository
      clone=subprocess.check_output(
          ' && '.join([
              'git config --global --add user.email "example@example.com"',
              'git config --global --add user.name "example"',
              'cd /tmp',
              'git %s %s' % (git_command, remote_repository)
          ]),
          stderr=subprocess.STDOUT,
          shell=True).decode()
      
      os.chdir('/tmp/template-environment-configuration')
      cwd = os.getcwd()
      region='eu-central-1'
      
      # copy new folder structure
      fromDirectory = "operations/region"
      toDirectory = "operations/" + region + "/"
      copy_tree(fromDirectory, toDirectory)
      
      fromDirectory = "application/region"
      toDirectory = "application/" + region + "/"
      copy_tree(fromDirectory, toDirectory)
      
      TEMPLATE_FILE = "application/" + region + "/terraform.template.tfvars"
      with open(TEMPLATE_FILE) as file_:
          template = Template(file_.read())
      #add value from top section here if newly added    
      rendered_file = template.render(application_aws_account_number=aws_account,environment_type=environment_type)
      f = open("application/" + region + "/terraform.tfvars" , "w")
      f.write(rendered_file)
      f.close()
          
      # Clone the remote Git repository
      push=subprocess.check_output(
          ' && '.join([
              'cd /tmp/template-environment-configuration',
              'rm -rf .git',
              'git init',
              'git %s %s' % (git_command_add_origin, new_remote_repository),
              'git add .',
              'git commit -m initial',
              #'git push --force -u origin master'
          ]),
          stderr=subprocess.STDOUT,
          shell=True).decode()
      
      result = subprocess.run(["git push -u origin master"], cwd='/tmp/template-environment-configuration',
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          check=False)
      print(result)

      logger.info("Successfully retrieved parameter {}".format(name))
      send(event, context, SUCCESS, response_data, name)

    if event['RequestType'] == 'Update':

      # Potentially support updating config repo from CloudFormation.

      logger.info("Successfully updated parameter {}".format(name))
      send(event, context, SUCCESS, response_data, name)

    elif event['RequestType'] == 'Delete':
      
      logger.info("Successfully deleted parameter: {}".format(name))
      send(event, context, SUCCESS, None, name)

#  Copyright 2016 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
#  This file is licensed to you under the AWS Customer Agreement (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at http://aws.amazon.com/agreement/ .
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied.
#  See the License for the specific language governing permissions and limitations under the License.

SUCCESS = "SUCCESS"
FAILED = "FAILED"

def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData

    json_responseBody = json.dumps(responseBody)

    print("Response body:\n" + json_responseBody)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))