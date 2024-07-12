# Airrived

I have created 4 REST endpoints:

1) fangPDF: To extract IOCs from PDF files.
2) fangURL: To extract IOCs from webpages.
3) tactic: To get techniques and subtechniques in it.
4) technique: To get the tactic it belongs to along with it's sub techniques.

# STEPS to implement:

1) Clone the repository
2) Install dependancies
3) Install postman on local pc
4) Run server.py
5) Copy the url and paste in Postman which looks like http://127.0.0.1:5000/rest_service?rest_service=input
Eg: http://127.0.0.1:5000/tactic?tactic=Initial Access
Eg: http://127.0.0.1:5000/fangURL?url='Link'
Eg: http://127.0.0.1:5000/fangPdf?file=uploadfile

# ACCESSING ENDPOINTS

1) fangPDF CURL_Request-
curl --location 'http://127.0.0.1:5000/fangPdf' \
--form 'file=@"/Users/rush/Downloads/Shining a Light on DARKSIDE Ransomware Operations _ Google Cloud Blog.pdf"' \

2) fangURL CURL_Request-
curl --location 'http://127.0.0.1:5000/fangURL?url=https%3A%2F%2Fcloud.google.com%2Fblog%2Ftopics%2Fthreat-intelligence%2Fshining-a-light-on-darkside-ransomware-operations%2F' \

3) tactic CURL_Request-
curl --location --request POST 'http://127.0.0.1:5000/tactic?tactic=Initial%20Access'

4) technique CURL_Request-
curl --location --request POST 'http://127.0.0.1:5000/technique?technique=Active%20Scanning'



