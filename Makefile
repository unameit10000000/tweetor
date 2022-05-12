up:
	docker run --rm -it -p 5500:5500 --env-file .localtest tweetor/web

bash:
	docker run --rm -it -p 5500:5500 --env-file .localtest tweetor/web bash

build:
	docker build -t tweetor/web .

push: build
	docker tag tweetor/web <dckr_username>/<image-tag:version>
	docker push <dckr_username>/<image-tag:version>
