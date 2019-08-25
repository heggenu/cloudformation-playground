from __future__ import print_function
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
    
    logger.info('Received event: {}'.format(json.dumps(event)))
    
    # The Git repository to clone
    remote_repository = 'https://github.com/heggenu/cloudformation-playground.git'
    new_remote_repository = 'git@github.com:heggenu/lambda-git-push.git'
    git_command = 'clone --depth 1'
    git_command_add_origin = 'remote add origin'
    
    subprocess.run(["rm","-rf", "/tmp/cloudformation-playground"])
    subprocess.run(["rm","-rf", "/tmp/id_rsa"])

    os.environ["GIT_SSH_COMMAND"] = "ssh -o UserKnownHostsFile=/tmp/known_hosts -i /tmp/id_rsa"

    newFile = open('/tmp/known_hosts','w+')
    newFile.write('github.com,140.82.118.3,140.82.118.4  ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==')
    newFile.close()

    keyFile = open('/tmp/id_rsa','w+')
    keyFile.write(f'''-----BEGIN OPENSSH PRIVATE KEY-----
    ...
-----END OPENSSH PRIVATE KEY-----
    ''')
    keyFile.close()

    subprocess.run(["chmod","400", "/tmp/id_rsa"])


        
    # Clone the remote Git repository
    output=subprocess.check_output(
        ' && '.join([
            #'rm -rf /tmp/*',
            'cd /tmp',
            'git %s %s' % (git_command, remote_repository),
            'cd /tmp/cloudformation-playground',
            'rm -rf .git',
            'git init',
            'git %s %s' % (git_command_add_origin, new_remote_repository),
            'git add .',
            'git commit -m "initial commit"',
            'git push -u origin master'
        ]),
        stderr=subprocess.STDOUT,
        shell=True).decode()
    
    print(output.split('\n'))

lambda_handler('empty','empty')
