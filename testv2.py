import boto3
import json
import schedule
import time

def job():
	iam = boto3.client('iam')
#List policies on AWS account
	cp = iam.list_policies(
	Scope = 'Local' # 'AWS'|'Local'|'All'
	)
	groups=iam.list_groups()
	c=[]
	for ig in groups['Groups']:
		d=ig['GroupName']
		c.append(str(d))
		
	if 'SMB_Nub8_Security' not in c:
		create_group_response = iam.create_group(GroupName = 'SMB_Nub8_Security')
#Check current policies on the AWS accounts
	a=[] #Auxiliar variable for a list of current policies
	for user in cp['Policies']:
		b=user['PolicyName']
		a.append(str(b))
	my_managed_policy = {
    	"Version":"2012-10-17",
    	"Statement":[{
        "Effect":"Allow",
        "Action":[        
            "cloudformation:*",
            "iam:*"
        ],
        "Resource":"*"
    	},
    	{
        "Effect":"Deny",
        "Action":[        
            "cloudformation:*"		
        ],
        "Resource":"arn:aws:cloudformation:us-east-1:992039636206:stack/S*"
    	},
{
        "Effect":"Deny",
        "Action":[        
            "iam:DeleteUser",
	    "iam:DeleteAccessKey",
	    "iam:ListAccessKey",
	    "iam:CreateAccessKey",
	    "iam:UpdateAccessKey",			
        ],
        "Resource":"arn:aws:iam::992039636206:user/smb_security11"
    	},
{
        "Effect":"Deny",
        "Action":[        
            "iam:DeletePolicy",		
	    "iam:CreatePolicyVersion",
	    "iam:DeletePolicyVersion",
	    "iam:DeleteRolePolicy",
	    "iam:DeleteUserPolicy",
	    "iam:DeleteGroupPolicy",
	    "iam:DetachRolePolicy",
	    "iam:DetachUserPolicy",
	    "iam:DetachGroupPolicy",
        ],
        "Resource":"arn:aws:iam::992039636206:policy/SMB_Tomcat_Policy"
    	},
{
        "Effect":"Deny",
        "Action":[        
            "iam:DeletePolicy",		
	    "iam:CreatePolicyVersion",
	    "iam:DeletePolicyVersion",
	    "iam:DeleteRolePolicy",
	    "iam:DeleteUserPolicy",
	    "iam:DeleteGroupPolicy",
	    "iam:DetachRolePolicy",
	    "iam:DetachUserPolicy",
	    "iam:DetachGroupPolicy",



        ],
        "Resource":"arn:aws:iam::992039636206:policy/Sentek5801"
    	},
{
        "Effect":"Deny",
        "Action":[        
	    "iam:DetachRolePolicy",
	    "iam:DetachUserPolicy",
	    "iam:DetachGroupPolicy"
        ],
 "Resource": [
      "arn:aws:iam::992039636206:group/*",
      "arn:aws:iam::992039636206:role/*",
      "arn:aws:iam::992039636206:user/*",
    ],
    "Condition": {"ArnLike": 
      {"iam:PolicyARN": "arn:aws:iam::992039636206:policy/Sentek5801"}
    }
    	},
{
        "Effect":"Deny",
        "Action":[        
	    "iam:DetachRolePolicy",
	    "iam:DetachUserPolicy",
	    "iam:DetachGroupPolicy"
        ],
 "Resource": [
      "arn:aws:iam::992039636206:group/*",
      "arn:aws:iam::992039636206:role/*",
      "arn:aws:iam::992039636206:user/*",
    ],
    "Condition": {"ArnLike": 
      {"iam:PolicyARN": "arn:aws:iam::992039636206:policy/SMB_Tomcat_Policy"}
    }
    	}]
	}

	if 'Sentek5801' not in a:
		iam.create_policy(
	 	PolicyName='Sentek5801',
	 	PolicyDocument=json.dumps(my_managed_policy)
	 	)

	pages = iam.get_paginator('list_users')
	for page in pages.paginate():
		for user in page['Users']:
			usertogroup=iam.add_user_to_group(
			UserName = user['UserName'], #Name of user
			GroupName = 'SMB_Nub8_Security'
			)
	#		response = iam.attach_user_policy(
	#		UserName = user['UserName'], #Name of user
	#		PolicyArn = 'arn:aws:iam::992039636206:policy/Sentek5801'
			# Policy ARN which you want to asign to user
	#		)
			#print(response)
			#print("Arn: {0}\nCreateDate: {1}\n"
			#.format(user['Arn'], user['CreateDate']))
	pages1 = iam.get_paginator('list_groups')
	for page in pages1.paginate():
		for user in page['Groups']:
			response = iam.attach_group_policy(
			GroupName=user['GroupName'],
			PolicyArn='arn:aws:iam::992039636206:policy/Sentek5801')
			#print("Arn: {0}\nCreateDate: {1}\n"
			#.format(user['GroupName'], user['CreateDate']))
	pages2 = iam.get_paginator('list_roles')
	path="/aws-service-role"
	for page in pages2.paginate():
		for user in page['Roles']:
			if path not in user['Path']:
				response = iam.attach_role_policy(
				RoleName=user['RoleName'],
				PolicyArn='arn:aws:iam::992039636206:policy/Sentek5801')
			#print(user)
	print("Done")
schedule.every(2).seconds.do(job)
while 1:
    schedule.run_pending()
    time.sleep(1)
