#Download Python from DockerHub and use it
FROM python:latest

#Set the working directory in the Docker container
WORKDIR /playlist-genius

#Copy the dependencies file to the working directory
COPY requirements.txt .

#Install the dependencies
RUN pip install -r requirements.txt

#Copy the Flask app code to the working directory
COPY . .

#Run the container
CMD [ "python", "./app.py" ]