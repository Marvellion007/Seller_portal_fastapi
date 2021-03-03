ENV := qa
FILE_CONFIG := ./config/${ENV}.config
CONFIG :=$(shell cat $(FILE_CONFIG))
port = $(word 2,$(CONFIG))

.PHONY: build
.PHONY: test

build:	
	port=${port} docker-compose -f ./build/docker-compose.yml build
	
run: build
	port=${port} docker-compose -f ./build/docker-compose.yml up 
	
stop: 		
	port=${port} docker-compose -f ./build/docker-compose.yml down 

test:
	port=${port} docker-compose -f ./build/docker-compose.yml build  && \
	port=${port} docker-compose -f ./build/docker-compose.yml up -d && \
	cd ${CURDIR}/scripts && \
	chmod +x script.sh && \
	bash script.sh ${port}&& \
	cd ${CURDIR} && \
	port=${port} docker-compose -f ./build/Docker_Test/docker-compose.yml build && \
	port=${port} docker-compose -f ./build/docker-compose.yml down && \
	docker image remove docker_test_testing 
	

