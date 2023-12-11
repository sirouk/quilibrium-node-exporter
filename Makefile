SHELL=/usr/bin/env bash

ifndef GIT_ORG
GIT_ORG = sirouk
endif

ifndef GIT_REPO
GIT_REPO = quilibrium-node-exporter
endif

ifndef SOURCE_PATH
SOURCE_PATH=~/quilibrium-node-exporter
endif

ifndef REPO_PATH
REPO_PATH=~/${GIT_REPO}
endif



check:
	cd ${SOURCE_PATH}
	ls 
	curl 127.0.0.1:8380/metrics 


install:
	cd ${SOURCE_PATH}
	sudo apt install -y python3 python3-pip jq
	python3 -m pip install flask
	python3 -m pip install base58

	@if [ ! -d ${REPO_PATH} ]; then \
		mkdir -p ${REPO_PATH} && cd ${REPO_PATH} && git clone https://github.com/${GIT_ORG}/${GIT_REPO} .; \
	elif [ -d ${REPO_PATH}/.git ]; then \
		cd ${REPO_PATH}; \
	else \
		echo "Directory exists but is not a git repository. Please handle manually."; \
	fi


update: install
	cd ${REPO_PATH}
	git pull


start-exporter:
	cd ${SOURCE_PATH} && python3 quilibrium-node-exporter.py


start-cron:
	@cd ${REPO_PATH}; \
	ps aux | grep "python3 quilibrium-node-exporter.py" | grep -v "grep" > /dev/null; \
	ps_exit_status=$$?; \
	if [ $$ps_exit_status -ne 0 ]; then \
		echo "Starting Quilibrium Node Exporter..."; \
		cd ${REPO_PATH} && make start-exporter >> ${REPO_PATH}/exporter.log 2>&1 & \
	else \
		echo "Quilibrium Node Exporter is already running"; \
	fi


stop-cron:
	@cd ${REPO_PATH}; \
	ps aux | grep "python3 quilibrium-node-exporter.py" | grep -v "grep" > /dev/null; \
	ps_exit_status=$$?; \
	if [ $$ps_exit_status -ne 0 ]; then \
		echo "Quilibrium Node Exporter is not running!"; \
		cd ${REPO_PATH} && make start-exporter >> ${REPO_PATH}/exporter.log 2>&1 & \
	else \
		echo "Stopping Quilibrium Node Exporter..."; \
		pkill -f "python3 quilibrium-node-exporter.py"; \
	fi
