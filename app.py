import os
import sys
import json
from lxml import etree


# Save as a file
def save_file(text, filename):
	if type(text) != 'str':
		text = str(text)
	file = open(filename, "w", encoding="utf-8")
	file.write(text)
	file.close()


# Read file
def read_file(filename):
    with open(filename, 'rb') as f: #, encoding="utf-8")
        text = f.read()
    return text


# Save as json file
def save_json_file(json_value, file_path):
    with open(file_path, "w") as file:
        # Write the JSON data to the file
        json.dump(json_value, file, indent=4)
    

# Check arguments.
if len(sys.argv) < 2:
    print(f"Usage: python {os.path.basename(sys.argv[0])} <xml-path>")
    sys.exit(1)
else:
    if not os.path.isfile(sys.argv[1]):
        print(f"Can't find: {sys.argv[1]}")
        sys.exit(1)


# Read xml file
root = etree.fromstring(read_file(sys.argv[1]))

# Iterate through all XML elements
for elem in root.getiterator():
    # Skip comments and processing instructions,
    # because they do not have names
    if not (
        isinstance(elem, etree._Comment)
        or isinstance(elem, etree._ProcessingInstruction)
    ):
        # Remove a namespace URI in the element's name
        elem.tag = etree.QName(elem).localname

# Remove unused namespace declarations
etree.cleanup_namespaces(root)
# print(etree.tostring(root).decode())

# Make output data
data = {}
data['analysts'] = '' # ?
data['asset_class'] = root.find(".//AssetClass").get("assetClass") if root.find(".//AssetClass") != None else ""
data['asset_type'] = root.find(".//AssetType").get("assetType") if root.find(".//AssetType") != None else ""
data['bank'] = '' # ?
data['focus_value'] = 'SectorIndustry' # ?
data['mime_type'] = root.find(".//MIMEType").text if root.find(".//MIMEType") != None else ""

data['org_details'] = {}
data['org_details']['OrganizationName'] = root.find(".//OrganizationName").text if root.find(".//OrganizationName") != None else ""
data['org_details']['OrganizationType'] = root.find(".//Organization").get("type") if root.find(".//Organization") != None else ""

data['org_details']['People'] = []
for one in root.findall('.//Person'):
    org = {
        "CountryCode": "",
        "Email": "",
        "FamilyName": "",
        "GivenName": "",
        "JobRole": "",
        "PersonID": "",
        "PhoneNumber": "",
    }
    org['CountryCode'] = one.find(".//CountryCode").text.replace("+", "") if one.find(".//CountryCode") != None else ""
    org['Email'] = one.find(".//Email").text if one.find(".//Email") != None else ""
    org['FamilyName'] = one.find("FamilyName").text if one.find("FamilyName") != None else ""
    org['GivenName'] = one.find("GivenName").text if one.find("GivenName") != None else ""
    org['PhoneNumber'] = one.find(".//Number").text if one.find(".//Number") != None else ""
    org['JobRole'] = one.find("JobTitle").text if one.find("JobTitle") != None else ""
    org['PersonID'] = one.get("personID")
    data['org_details']['People'].append(org)


data['primary_analyst'] = '' # ?
data['primary_analyst_email'] = '' # ?
data['primary_region'] = root.find(".//Region").get("regionType") if root.find(".//Region") != None else ""
data['product_category_value'] = root.find(".//ProductCategory").get("productCategory") if root.find(".//ProductCategory") != None else ""
data['publication_datetime'] = root.find(".//ProductDetails").get("publicationDateTime") if root.find(".//ProductDetails") != None else ""

data['region_data'] = []
region_data = {"primaryIndicator": "", "regionType": ""}
region_data['primaryIndicator'] = root.find(".//Region").get("primaryIndicator") if root.find(".//Region") != None else ""
region_data['regionType'] = root.find(".//Region").get("regionType") if root.find(".//Region") != None else ""
data['region_data'].append(region_data)

data['regions'] = []
region_data = {"regionType": "", "primaryIndicator": ""}
region_data['primaryIndicator'] = root.find(".//Region").get("primaryIndicator") if root.find(".//Region") != None else ""
region_data['regionType'] = root.find(".//Region").get("regionType") if root.find(".//Region") != None else ""
data['regions'].append(region_data)

data['sector_data'] = []
for one in root.findall('.//SectorIndustry'):
    org = {
        "classificationType": "",
        "code": "",
        "focusLevel": "",
        "level": "",
        "name": "",
        "primaryIndicator": "",
    }
    org['classificationType'] = one.get("classificationType")
    org['code'] = one.get("code")
    org['focusLevel'] = one.get("focusLevel")
    org['level'] = one.get("level")
    org['primaryIndicator'] = one.get("primaryIndicator")
    org['name'] = one.find(".//Name").text if one.find(".//Name") != None else ""
    data['sector_data'].append(org)

data['sector_id'] = "" # ?
data['securities'] = []
for one in root.findall('.//SecurityType'):
    org = {
    }
    org['SecurityType'] = one.get("securityType")
    org['PublisherDefinedValue'] = one.get("publisherDefinedValue")
    data['securities'].append(org)

data['subject'] = root.find(".//Subject").get("publisherDefinedValue") if root.find(".//Subject") != None else "" # ?
data['synopsis'] = root.find(".//Synopsis").text if root.find(".//Synopsis") != None else ""
data['title'] = root.find(".//Title").text if root.find(".//Title") != None else ""
data['url'] = root.find(".//URL").text if root.find(".//URL") != None else ""

# Save 
out = sys.argv[1].replace(".xml", "_output.txt")
save_json_file(data, out)
print("Result:", out)