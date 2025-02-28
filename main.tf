provider "aws" {
  region = "eu-central-1"
}

# Creating a VPC
resource "aws_vpc" "dev-vpc" {
  cidr_block = "10.0.0.0/16"
}

# Creating a private subnet
resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.dev-vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-central-1"
  map_public_ip_on_launch = false
}

# Creating an Internet Gateway
resource "aws_internet_gateway" "dev-gw" {
  vpc_id = aws_vpc.dev-vpc.id
}

# Creating a route table
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.dev-vpc.id
}

# Associating the route table with the subnet
resource "aws_route_table_association" "dev-rt" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

# Creating an EC2 instance
resource "aws_instance" "devskiller-ec2" {
  ami           = "ami-0be656e75e69af1a9" 
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.private.id
  private_ip = "10.0.10.250"

  tags = {
    Name = "devskiller-ec2-instance"
  }
}

# Allocating an Elastic IP
resource "aws_eip" "ip" {
  domain = "vpc"
  instance = aws_instance.devskiller-ec2.id
}

# Create an EBS volume
resource "aws_ebs_volume" "devskiller-ec2" {
  availability_zone = "eu-central-1"
  size              = 10
}

# Attach the EBS volume to the instance
resource "aws_volume_attachment" "devskiller-ec2" {
  device_name = "/dev/sdc"
  volume_id   = aws_ebs_volume.devskiller-ec2.id
  instance_id = aws_instance.devskiller-ec2.id
}