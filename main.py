import requests
import hashlib

def login(name:str, pwd:str) -> tuple:
	password_md5 = hashlib.md5(pwd.encode(encoding='utf-8')).hexdigest()
	url = 'https://auac-sso.yzw.cn/api/auac/sso/v1/web/login'  #登陆链接
	headers = {"Content-Type": "application/json"}
	data = {
		"appKey": "jc_v2_purchase",
		"loginName": name,
		"password": password_md5,
		"loginType": 10,
		"isRememberMe": False,
		"agreementFlag": 1
	}
	r = s.post(url, headers=headers, json=data)
	# print("登陆返回值：",r.json())
	return r.json()['data']['ssoUser']['orgCode'],r.json()['data']['ssoUser']['orgName']

def pingfen(orgCode:str, orgName:str, pjProjectCode:int, pjProjectName:str, categoryCode:str, categoryFullName:str, pjSupplierCode:int, pjSupplierName:str):
	url = 'https://crp.yzw.cn/api/requisition/assess/assessRequisition'  #
	headers = {"Content-Type": 'application/json'}
	data = {
		"businessType": 2,
		"ruleType": 12,
		"categoryCode": categoryCode,
		"categoryName": categoryFullName,
		"contractOrgCode": orgCode,
		"contractOrgName": orgName,
		"areaCode": None,
		"areaName": None,
		"projectCode": pjProjectCode,
		"projectName": pjProjectName,
		"assessRuleList": [{
			"ruleId": 1,#专业分包1706，劳务分包2445
			"ruleAttrs": [{
				"ruleId": 1,
				"attrValueKey": "environment_qualify_type",
				"attrValueInput": "environment_qualify_type_two"
			}],
			"engineOutputScore": "0",
			"score": 0
		}],
		"supplierCode": pjSupplierCode,
		"supplierName": pjSupplierName,
		"type": 2,
		"assessRuleScore": 0,
		"organizationCode": orgCode,
		"organizationName": orgName,
		"patchData": False
	}
	r = s.post(url,headers=headers, json=data)
	# print("评价数据：",r.json())

def get_dict(orgCode:str) -> dict:
	url = 'https://crp.yzw.cn/api/assess/appointTarget/supplierPageList'
	headers = {"Content-Type": "application/json"}
	data = {"param":{"containSub":True,"organizationCode":orgCode,"ruleType":12,"assessInputTab":10,"perf":1,"projectStatus":"1","myProject":True},"pageNum":1,"pageSize":100}	# 待评价
	# data = {"param":{"containSub":True,"organizationCode":orgCode,"ruleType":12,"assessInputTab":30,"myProject":True},"pageNum":1,"pageSize":1}	# 已评价
	# data = {"param":{"containSub":True,"organizationCode":orgCode,"ruleType":12,"assessInputTab":50,"myProject":True},"pageNum":1,"pageSize":1}	# 全部可评价
	r = s.post(url, headers=headers, json=data)
	# print("获取评价列表：",r.json())
	return r.json()

if __name__ == '__main__':
	s = requests.session()
  
	# 填入用户名及密码
	name = ""
	pwd = ""
	orgCode,orgName = login(name, pwd)
	for list in get_dict(orgCode)["data"]["list"]:
		pjProjectCode = int(list['pjProjectCode'])
		pjProjectName = str(list['pjProjectName'])
		categoryCode = str(list['categoryCode'])
		categoryFullName = str(list['categoryFullName'])
		pjSupplierCode = list['pjSupplierCode']
		pjSupplierName = str(list['pjSupplierName'])
		pingfen(orgCode, orgName, pjProjectCode, pjProjectName, categoryCode,categoryFullName,pjSupplierCode,pjSupplierName)
