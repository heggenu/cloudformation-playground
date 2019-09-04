import re

privateSSHKey="-----BEGIN OPENSSH PRIVATE KEY----- abc def ghi jkl mno pqr stu vxy== -----END OPENSSH PRIVATE KEY----- "

privateSSHKeyBegin = re.search(r'^(-----BEGIN ([^-]+)-----)',privateSSHKey).group(0)
privateSSHKeyEnd = re.search(r'(-----END ([^-]+)-----)',privateSSHKey).group(0)
privateSSHKeyBase64 = re.sub(r'^\s*(?:\-+(?:.*?)\-+)?\s*((?:[A-Za-z0-9\+\/]\s?)+={0,2})\s*(?:\-+(?:.*?)\-+)?\s*$', '\g<1>', privateSSHKey)
privateSSHKeyBase64=privateSSHKeyBase64.replace(' ','\n')


privateSSHKey=privateSSHKeyBegin+'\n'+privateSSHKeyBase64+'\n'+privateSSHKeyEnd+'\n '
print(privateSSHKey)