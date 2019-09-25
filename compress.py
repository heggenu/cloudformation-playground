from __future__ import print_function
_A=False
from distutils.dir_util import copy_tree
from botocore.vendored import requests
from jinja2 import Template
import os,subprocess,json,boto3,logging,jinja2,urllib,re
def handler(event,context):
	s='/';r='git %s %s';q=' && ';p='-rf';o='rm';n='eu-central-1';m='ssm';l='Value';U='application/';T='\n';S='/tmp/id_rsa';R='/tmp/template-environment-configuration';Q='RequestType';P='ResourceProperties';K=True;F=context;A=event;C=logging.getLogger();C.setLevel(logging.INFO);C.info('Received event: {}'.format(json.dumps(A)));B=A[P]['Name'];print(B);L=A[P][l];print(L);V=A[P]['Test'];print(V);G={}
	try:M=boto3.client(m)
	except Exception as W:C.info('boto3.client failure: {}'.format(W));send(A,F,FAILED,G)
	if A[Q]=='Create':
		X='1234567890';t='0987654321';Y='test';D=n;u='demo';v='https://jenkins.com';w='https://proxy.com';x='vpc-123456';Z='https://github.com/kentrikos/template-environment-configuration.git';a=L;b='clone --depth 1 -b jinja_templating --single-branch';c='remote add origin';subprocess.run([o,p,R]);subprocess.run([o,p,S]);os.environ['GIT_SSH_COMMAND']='ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /tmp/id_rsa';M=boto3.client(m);d=M.get_parameter(Name='/my/securestring/data',WithDecryption=K);E=d['Parameter'][l];e=re.search('^(-----BEGIN ([^-]+)-----)',E).group(0);f=re.search('(-----END ([^-]+)-----)',E).group(0);H=re.sub('^\\s*(?:\\-+(?:.*?)\\-+)?\\s*((?:[A-Za-z0-9\\+\\/]\\s?)+={0,2})\\s*(?:\\-+(?:.*?)\\-+)?\\s*$','\\g<1>',E);H=H.replace(' ',T);E=e+T+H+T+f+'\n ';N=open(S,'w+');N.write(E);N.close();subprocess.run(['chmod','700',S]);y=subprocess.check_output(q.join(['git config --global --add user.email "example@example.com"','git config --global --add user.name "example"','cd /tmp',r%(b,Z)]),stderr=subprocess.STDOUT,shell=K).decode();os.chdir(R);z=os.getcwd();D=n;I='operations/region';J='operations/'+D+s;copy_tree(I,J);I='application/region';J=U+D+s;copy_tree(I,J);g=U+D+'/terraform.template.tfvars'
		with open(g)as h:i=Template(h.read())
		j=i.render(application_aws_account_number=X,environment_type=Y);O=open(U+D+'/terraform.tfvars','w');O.write(j);O.close();A0=subprocess.check_output(q.join(['cd /tmp/template-environment-configuration','rm -rf .git','git init',r%(c,a),'git add .','git commit -m initial']),stderr=subprocess.STDOUT,shell=K).decode();k=subprocess.run(['git push -u origin master'],cwd=R,shell=K,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=_A);print(k);C.info('Successfully retrieved parameter {}'.format(B));send(A,F,SUCCESS,G,B)
	if A[Q]=='Update':C.info('Successfully updated parameter {}'.format(B));send(A,F,SUCCESS,G,B)
	elif A[Q]=='Delete':C.info('Successfully deleted parameter: {}'.format(B));send(A,F,SUCCESS,None,B)
SUCCESS='SUCCESS'
FAILED='FAILED'
def send(event,context,responseStatus,responseData,physicalResourceId=None,noEcho=_A):
	K='LogicalResourceId';J='RequestId';I='StackId';D=context;B=event;E=B['ResponseURL'];print(E);A={};A['Status']=responseStatus;A['Reason']='See the details in CloudWatch Log Stream: '+D.log_stream_name;A['PhysicalResourceId']=physicalResourceId or D.log_stream_name;A[I]=B[I];A[J]=B[J];A[K]=B[K];A['NoEcho']=noEcho;A['Data']=responseData;C=json.dumps(A);print('Response body:\n'+C);F={'content-type':'','content-length':str(len(C))}
	try:G=requests.put(E,data=C,headers=F);print('Status code: '+G.reason)
	except Exception as H:print('send(..) failed executing requests.put(..): '+str(H))