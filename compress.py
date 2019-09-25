from __future__ import print_function
from distutils.dir_util import copy_tree
from botocore.vendored import requests
from jinja2 import Template
import os,subprocess,json,boto3,logging,jinja2,urllib,re
def handler(event,context):
	r='/';q='git %s %s';p=' && ';o='/tmp/template-environment-configuration';n='-rf';m='rm';l='eu-central-1';k='ssm';j='Value';T='application/';S='\n';R=True;Q='/tmp/id_rsa';P='RequestType';O='ResourceProperties';F=context;A=event;C=logging.getLogger();C.setLevel(logging.INFO);C.info('Received event: {}'.format(json.dumps(A)));B=A[O]['Name'];print(B);K=A[O][j];print(K);U=A[O]['Test'];print(U);G={}
	try:L=boto3.client(k)
	except Exception as V:C.info('boto3.client failure: {}'.format(V));send(A,F,FAILED,G)
	if A[P]=='Create':
		W='1234567890';s='0987654321';X='test';D=l;t='demo';u='https://jenkins.com';v='https://proxy.com';w='vpc-123456';Y='https://github.com/kentrikos/template-environment-configuration.git';Z=K;a='clone --depth 1 -b jinja_templating --single-branch';b='remote add origin';subprocess.run([m,n,o]);subprocess.run([m,n,Q]);os.environ['GIT_SSH_COMMAND']='ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /tmp/id_rsa';L=boto3.client(k);c=L.get_parameter(Name='/my/securestring/data',WithDecryption=R);E=c['Parameter'][j];d=re.search('^(-----BEGIN ([^-]+)-----)',E).group(0);e=re.search('(-----END ([^-]+)-----)',E).group(0);H=re.sub('^\\s*(?:\\-+(?:.*?)\\-+)?\\s*((?:[A-Za-z0-9\\+\\/]\\s?)+={0,2})\\s*(?:\\-+(?:.*?)\\-+)?\\s*$','\\g<1>',E);H=H.replace(' ',S);E=d+S+H+S+e+'\n ';M=open(Q,'w+');M.write(E);M.close();subprocess.run(['chmod','700',Q]);x=subprocess.check_output(p.join(['git config --global --add user.email "example@example.com"','git config --global --add user.name "example"','cd /tmp',q%(a,Y)]),stderr=subprocess.STDOUT,shell=R).decode();os.chdir(o);y=os.getcwd();D=l;I='operations/region';J='operations/'+D+r;copy_tree(I,J);I='application/region';J=T+D+r;copy_tree(I,J);f=T+D+'/terraform.template.tfvars'
		with open(f)as g:h=Template(g.read())
		i=h.render(application_aws_account_number=W,environment_type=X);N=open(T+D+'/terraform.tfvars','w');N.write(i);N.close();z=subprocess.check_output(p.join(['cd /tmp/template-environment-configuration','rm -rf .git','git init',q%(b,Z),'git add .','git commit -m initial','git push --force -u origin master']),stderr=subprocess.STDOUT,shell=R).decode();C.info('Successfully retrieved parameter {}'.format(B));send(A,F,SUCCESS,G,B)
	if A[P]=='Update':C.info('Successfully updated parameter {}'.format(B));send(A,F,SUCCESS,G,B)
	elif A[P]=='Delete':C.info('Successfully deleted parameter: {}'.format(B));send(A,F,SUCCESS,None,B)
SUCCESS='SUCCESS'
FAILED='FAILED'
def send(event,context,responseStatus,responseData,physicalResourceId=None,noEcho=False):
	K='LogicalResourceId';J='RequestId';I='StackId';D=context;B=event;E=B['ResponseURL'];print(E);A={};A['Status']=responseStatus;A['Reason']='See the details in CloudWatch Log Stream: '+D.log_stream_name;A['PhysicalResourceId']=physicalResourceId or D.log_stream_name;A[I]=B[I];A[J]=B[J];A[K]=B[K];A['NoEcho']=noEcho;A['Data']=responseData;C=json.dumps(A);print('Response body:\n'+C);F={'content-type':'','content-length':str(len(C))}
	try:G=requests.put(E,data=C,headers=F);print('Status code: '+G.reason)
	except Exception as H:print('send(..) failed executing requests.put(..): '+str(H))