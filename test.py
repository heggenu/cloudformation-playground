from __future__ import print_function
from distutils.dir_util import copy_tree

import os
import subprocess
import json
import boto3
import logging
import jinja2
import urllib
      
def lambda_handler(event, context):
    from jinja2 import Template
    template = Template('Hello {{ name }}!')
    
    print(template.render(name='John Doe'))

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    #logger.info('Received event: {}'.format(json.dumps(event)))
    
    #DEFAULT VALUES
    default_aws_account = '1234567890'
    default_opp_account = '0987654321'
    default_environment_type = 'test'
    default_role_name = 'AssumeKopsCrossAccount'
    default_region = 'us-east-1'
    default_product_domain_name = 'demo'
    default_jenkins_config_url = 'https://jenkins.com'
    default_http_proxy = "https://proxy.com"
    default_vpc_id = "vpc-123456"
    default_subnet1_id = "subnet-12345"
    default_subnet2_id = "subnet-23456"
    default_subnet3_id = "subnet-34567"
    default_private_hosted_zone_id = "AAAAAAAAA"
    default_private_hosted_zone_alias_jenkins = "Jenkins"
    default_jxDomainAliasPrefix = "JX"
    default_gitBitbucketServer = "https://bitbucket.com"
    default_gitProviderUrl = "https://github.com"
    default_gitApiToken = "jf982j3498fj349j"
    default_gitUsername = "gitman"
    
    #replaces values into the templated file, to add a value add curly braces: ex - {{value}}
    aws_account = default_aws_account
    aws_opp_account =  default_opp_account
    environment_type =  default_environment_type
    region =  default_region
    product_domain_name = default_product_domain_name
    jenkins_config_url = default_jenkins_config_url
    http_proxy = default_http_proxy
    vpc_id = default_vpc_id
    
    #Jenkins-Core configuration
    private_hosted_zone_id = default_private_hosted_zone_id
    private_hosted_zone_alias_jenkins = default_private_hosted_zone_alias_jenkins

    
    # The Git repository to clone
    remote_repository = 'https://github.com/kentrikos/template-environment-configuration.git'
    new_remote_repository = 'git@github.com:heggenu/lambda-git-push.git'
    git_command = 'clone --depth 1 -b jinja_templating --single-branch'
    git_command_add_origin = 'remote add origin'
    
    subprocess.run(["rm","-rf", "/tmp/template-environment-configuration"])
    subprocess.run(["rm","-rf", "/tmp/id_rsa"])

    os.environ["GIT_SSH_COMMAND"] = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /tmp/id_rsa"

    newFile = open('/tmp/known_hosts','w+')
    newFile.write('github.com,140.82.118.3,140.82.118.4  ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==')
    newFile.close()
    
    ssm=boto3.client('ssm')
    privateSSHKey=ssm.get_parameter(
                  Name='/securestring/data',
                  WithDecryption=True
                )

    keyFile = open('/tmp/id_rsa','w+')
    keyFile.write(privateSSHKey['Parameter']['Value'])
    keyFile.close()


    subprocess.run(["chmod","700", "/tmp/id_rsa"])

    # Clone the remote Git repository
    clone=subprocess.check_output(
        ' && '.join([
            #'rm -rf /tmp/*',
            'git config --global --add user.email "example@example.com"',
            'git config --global --add user.name "example"',
            'cd /tmp',
            'git %s %s' % (git_command, remote_repository)
        ]),
        stderr=subprocess.STDOUT,
        shell=True).decode()
    
    os.chdir('/tmp/template-environment-configuration')
    
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
            'ls -la',
            'git %s %s' % (git_command_add_origin, new_remote_repository),
            'git add .',
            'git commit -m initial',
            'git push --force -u origin master'
        ]),
        stderr=subprocess.STDOUT,
        shell=True).decode()
    
    #result = subprocess.run(["git push -u origin master"], cwd='/tmp/cloudformation-playground',
    #                    shell=True,
    #                    stdout=subprocess.PIPE,
    #                    stderr=subprocess.PIPE,
    #                    check=False)
    #print(result)
    
    print(clone.split('\n'))
