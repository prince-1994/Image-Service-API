## Image Service API

An Image processing API to edit images and convert them into other formats. 

The API currently supports adjusting brightness, contrast, color balance, sharpness as well as flipping vertically, mirroring and rotating input images. The project uses the Pillow library to handle image editing and format conversion tasks. The project uses FastAPI to implement the API server.

The project also has a CI/CD pipeline to release latest changes on the server when commits are pushed to the master branch . The CI/CD pipeline checks out code on a self hosted runner, run tests, run linting, creates a docker image and pushes to dockerhub. Then it logs into the deployment server, pulls the latest docker image which was recently pushed and runs the service using docker. After that it updates the nginx-conf file.


#### Running the project
Make sure you are in the root folder of the project and then run the following.
```
> touch ./.env.dev && docker compose up
```
This will run the service on 8000 port. You can use the following curl command to rotate an image by 45 degrees, flip the image upside down, increase the color contrast by a magnitude of 2 and convert to png format using the service.
```
> curl -X POST --data-binary "@tests/test-image-1-scenery.jpeg" http://localhost:8000/images/edit?rotate=-45&flip=1&con=2&format=png -o test_image.png
```
The following query params are currently supported
```
bri, con, col, sharp: -Inf to Inf
flip(vertical), mirror(horizontal): 0 or 1
rotate(in degrees): -Inf to Inf
```

#### Running tests
```
> pip install -r requirements.txt && pip install -r requirements.dev.txt
> pytest -s tests
```