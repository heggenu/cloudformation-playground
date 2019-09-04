from __future__ import print_function
from distutils.dir_util import copy_tree
from botocore.vendored import requests
from jinja2 import Template
import os,subprocess,json,boto3,logging,jinja2,urllib,re
def handler(event,context):
	n='/';m='git %s %s';l=' && ';k='/tmp/template-environment-configuration';j='-rf';i='rm';h='eu-central-1';g='ssm';R='application/';Q='\n';P=True;O='/tmp/id_rsa';N='RequestType';F=context;A=event;B=logging.getLogger();B.setLevel(logging.INFO);B.info('Received event: {}'.format(json.dumps(A)));C=A['ResourceProperties']['Name'];G={}
	try:K=boto3.client(g)
	except Exception as S:B.info('boto3.client failure: {}'.format(S));send(A,F,FAILED,G)
	if A[N]=='Create':
		T='1234567890';o='0987654321';U='test';D=h;p='demo';q='https://jenkins.com';r='https://proxy.com';s='vpc-123456';V='https://github.com/kentrikos/template-environment-configuration.git';W='git@github.com:heggenu/lambda-git-push.git';X='clone --depth 1 -b jinja_templating --single-branch';Y='remote add origin';subprocess.run([i,j,k]);subprocess.run([i,j,O]);os.environ['GIT_SSH_COMMAND']='ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /tmp/id_rsa';K=boto3.client(g);Z=K.get_parameter(Name='/my/securestring/data',WithDecryption=P);E=Z['Parameter']['Value'];a=re.search('^(-----BEGIN ([^-]+)-----)',E).group(0);b=re.search('(-----END ([^-]+)-----)',E).group(0);H=re.sub('^\\s*(?:\\-+(?:.*?)\\-+)?\\s*((?:[A-Za-z0-9\\+\\/]\\s?)+={0,2})\\s*(?:\\-+(?:.*?)\\-+)?\\s*$','\\g<1>',E);H=H.replace(' ',Q);E=a+Q+H+Q+b+'\n ';L=open(O,'w+');L.write(E);L.close();subprocess.run(['chmod','700',O]);t=subprocess.check_output(l.join(['git config --global --add user.email "example@example.com"','git config --global --add user.name "example"','cd /tmp',m%(X,V)]),stderr=subprocess.STDOUT,shell=P).decode();os.chdir(k);u=os.getcwd();D=h;I='operations/region';J='operations/'+D+n;copy_tree(I,J);I='application/region';J=R+D+n;copy_tree(I,J);c=R+D+'/terraform.template.tfvars'
		with open(c)as d:e=Template(d.read())
		f=e.render(application_aws_account_number=T,environment_type=U);M=open(R+D+'/terraform.tfvars','w');M.write(f);M.close();v=subprocess.check_output(l.join(['cd /tmp/template-environment-configuration','rm -rf .git','git init',m%(Y,W),'git add .','git commit -m initial']),stderr=subprocess.STDOUT,shell=P).decode();B.info('Successfully retrieved parameter {}'.format(C));send(A,F,SUCCESS,G,C)
	if A[N]=='Update':B.info('Successfully updated parameter {}'.format(C));send(A,F,SUCCESS,G,C)
	elif A[N]=='Delete':B.info('Successfully deleted parameter: {}'.format(C));send(A,F,SUCCESS,None,C)
SUCCESS='SUCCESS'
FAILED='FAILED'
def send(event,context,responseStatus,responseData,physicalResourceId=None,noEcho=False):
	K='LogicalResourceId';J='RequestId';I='StackId';D=context;B=event;E=B['ResponseURL'];print(E);A={};A['Status']=responseStatus;A['Reason']='See the details in CloudWatch Log Stream: '+D.log_stream_name;A['PhysicalResourceId']=physicalResourceId or D.log_stream_name;A[I]=B[I];A[J]=B[J];A[K]=B[K];A['NoEcho']=noEcho;A['Data']=responseData;C=json.dumps(A);print('Response body:\n'+C);F={'content-type':'','content-length':str(len(C))}
	try:G=requests.put(E,data=C,headers=F);print('Status code: '+G.reason)
	except Exception as H:print('send(..) failed executing requests.put(..): '+str(H))