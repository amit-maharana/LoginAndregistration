# Choose Linux OS Image
FROM ubuntu:20.04

# Update packages
RUN apt-get update -y
RUN apt-get -y install python3-pip

# Create a working directory
WORKDIR /login_and_register

# copy required files
COPY requirements.txt /login_and_register
COPY logger.py /login_and_register
COPY configuration.py /login_and_register
COPY loginandregistration.py /login_and_register

# Install requirements
RUN pip3 install -r requirements.txt

# Run
CMD ["python3","loginandregistration.py"]