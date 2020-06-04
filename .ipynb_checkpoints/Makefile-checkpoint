# assuming `make` is run from this directory
PWD = $(shell pwd)

build:
	docker build -t brand-translator:latest .

run: build
	docker run \
	-it \
	brand-translator:latest $(script)

run-enter: build
	docker run \
	-it \
	-entrypoint '/bin/sh' \
	brand-translator:latest

run-categorize: build
	docker run \
	-it \
	-v $(PWD)/data:/home/data \
	brand-translator:latest src/dataset/companies.py

run-download: build
	docker run \
	-it \
	-v $(PWD)/data:/home/data \
	brand-translator:latest src/dataset/wikipedia.py download ./data/companies/industries/$(industry) ./data/wikipedia/content/$(industry)

run-parse: build
	docker run \
	-it \
	-v $(PWD)/data:/home/data \
	brand-translator:latest src/dataset/wikipedia.py parse ./data/wikipedia/content/$(industry) ./data/wikipedia/textcontent/$(industry)

run-gen-dsc: build
	docker run \
	-it \
	-v $(PWD)/data:/home/data \
	brand-translator:latest src/dataset/descriptors.py ./data/wikipedia/textcontent/$(industry) ./data/unaided-awareness/$(industry)

run-train: build
	docker run \
	-it \
	-v $(PWD)/data:/home/data \
	brand-translator:latest src/unaided-awareness/brand-translator.py ./data/unaided-awareness/$(industry)

# --entrypoint '/bin/sh' \
# brand-translator:latest