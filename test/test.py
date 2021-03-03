import requests
import sys

port=sys.argv[1]

url="172.17.0.1"

register_buyer_url = "http://"+url+":"+port+"/buyer/1/test?Buyer_country=india&Buyer_shipping_address=test%20adress&Buyer_shipping_city=test%20city&Buyer_shipping_zip_code=246715&Buyer_email_address=shukla.ajiyresg%40gmail.com&Buyer_phone_number=2345678900"
delete_url = "http://"+url+":"+port+"/buyer/1"
get_credit_url = "http://"+url+":"+port+"/credit_score/1/test?Buyer_country=india"
get_buyer_url = "http://"+url+":"+port+"/buyer/1"
update_url = "http://"+url+":"+port+"/buyer/1?Buyer_shipping_city=updated"
generate_invoice_url = "http://"+url+":"+port+"/invoice/1/test?Product_price=10&Number_of_pieces=10&Send_mail=true&Status=paid"
list_invoices = "http://"+url+":"+port+"/invoices"
update_invoice_url = "http://"+url+":"+port+"/invoice/1?Resend_mail=false&Product_name=pen"

payload = {}
headers= {}

post_response = requests.request("POST", register_buyer_url, headers=headers, data = payload)
assert post_response.status_code == 200

post_response = requests.request("POST", generate_invoice_url, headers=headers, data = payload)
assert post_response.status_code == 200

get_response = requests.request("GET", get_buyer_url, headers=headers, data = payload)
assert get_response.status_code == 200

get_response = requests.request("GET", get_credit_url, headers=headers, data = payload)
assert get_response.status_code == 200

get_response = requests.request("GET", list_invoices, headers=headers, data = payload)
assert get_response.status_code == 200

update_response = requests.request("PATCH", update_url, headers=headers, data = payload)
assert update_response.status_code == 200

update_response = requests.request("PATCH", update_invoice_url, headers=headers, data = payload)
assert update_response.status_code == 200


delete_response = requests.request("DELETE", delete_url, headers=headers, data = payload)
assert delete_response.status_code == 200

print("all test cases passed")



