SHELL = /bin/bash

.PHONY: help
## help: shows this help message
help:
	@ echo "Usage: make [target]"
	@ sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'

.PHONY: run
## run: runs the application
run:
	@ docker-compose up && docker-compose rm -fsv
# @ docker-compose up
	

.PHONY: cleanup
## cleanup: removes MongoDB and associated volumes
cleanup:
	@ docker-compose down
	@ docker volume rm $$(docker volume ls -q)

.PHONY: test
## test: runs unit tests
test:
	@ pytest tests