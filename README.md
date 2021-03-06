# INTODUCTION 
This is a RESTAPI for managing payment system for sellers.
The API is dockerized using docker compose and execution is managed by MAKEFILE 


# HOW TO RUN
In the config directory there are 3 files with different port numbers.
- qa which is default file with value 8080
- prod with port no. 8000
- stg with port no. 5000

1: Move to directory
2: Run 'make run ENV=filename' command and it will build the docker image and create corresponding container. 
for example, we can move to the directory and run following commands for qa environment
- make run ENV=qa

3: After that you can open following link for requests
http://127.0.0.1:{port}/docs
for interactive API
     or 
http://127.0.0.1:{port}/redoc 
for alternate interactive API

4: There are some of the tabs available namely-
- Buyer Credit: You can click on the tab and fill the parameters to get the credit score of the buyer

- Register Buyer: This tab is to register buyer. If it is already present it will return "Buyer is already registered"

- Get Buyer Details: This tab is to get the Buyer's detail from the database. Returns 404 if the buyer is not present.

- Delete Buyer: This tab is delete the Buyer's detail from the database. Returns 404 if the buyer is not present.
 
- Patch Buyer: This tab is to patch details in  buyer's database. Returns 404 if the buyer is not present.

- Generate invoice: This tab is to generate the invoice of the purchase , prerequisite is buyer should be registered.The pdf will be created inside the docker container to get it you can use 
"docker cp {container_name}:/tmp/invoice_{vat_id}.pdf ."

- List invoices: This tab will return list of all invoices generated till now.

- Get invoice: This tab will return particular invoice of the buyer.

- Update Invoice: This tab will do update operation in the invoices.

# Testing
To test the project move to directory and run 'make test'. It will create and run the API and then test it using requests and assert. Testing will be done inside another docker container.

# STRUCTURE OF PROJECT
# core: 
It contains the source code with 3 layers, namely 
- Controller Layer
- Service Layer 
- Repository Layer
Controller layer is the outermost layer of the API which takes the request.
Service layer is the medium which transfer the API call to repository layer
Repository layer is the layer which connects with the database.

# config:
It contains dependencies of source code
There are 3 files with different port numbers and a env file for postgreSQL data.
- qa with port no. 8080
- prod with port no. 8000
- stg with port no. 5000

# Build:
It contains the build related things such as docker compose file , DockerFile and requirement.txt file

# Scripts:
It contains the script for testing purpose.

# Test:
it contains the source code for testing API.

# Data Models used inside the project.

There are three Datamodels used:

1.Credit_base with following fields:
- Buyer_business_VAT_ID
- Buyer_business_name
- Buyer_country
1(a).This pydantic datamodel stores data in table "Buyer credit" as :
- Buyer_business_VAT_ID = Column(String, primary_key=True)
- Buyer_business_name = Column(String)
- Buyer_country = Column(String)
- Buyer_credit_score= Column(Integer), It is automatically generated

2.Buyer_base with following fields:
- Buyer_business_VAT_ID
- Buyer_business_name
- Buyer_country
- Buyer_shipping_address
- Buyer_shipping_city
- Buyer_shipping_zip_code
- Buyer_email_address
- Buyer_phone_number
2(a).This pydantic datamodel stores data in table "Buyer" as :
- Buyer_business_VAT_ID= Column(String, primary_key=True)
- Buyer_business_name = Column(String)
- Buyer_country = Column(String)
- Buyer_shipping_address = Column(String)
- Buyer_shipping_city = Column(String)
- Buyer_shipping_zip_code = Column(String)
- Buyer_email_address = Column(String)
- Buyer_phone_number = Column(String)

3.Invoice with follwing fields:
- Buyer_business_VAT_ID
- Product_name
- Product_price
- Number_of_pieces
- Status
- Send_mail
3(a).This pydantic datamodel stores data in table "Invoice" as:
- Buyer_business_VAT_ID= Column(String,primary_key=True,index=False)
- Product_name= Column(String)
- Product_price= Column(Integer)
- Number_of_pieces= Column(Integer)
- Status= Column(String)

# Request's Response:

1. 200 for successfull response
2. 400 for bad request
3. 404 for non found
4. 500 for internal error 