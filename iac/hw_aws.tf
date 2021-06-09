provider "aws" {
  profile	= "default"
  region	= var.region
}

data "aws_availability_zones" "available" {}

locals {
  cluster_name = "sofin-eks"
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "2.66.0"
  name                 = "sofin-vpc"
  cidr                 = "10.0.0.0/16"
  azs                  = data.aws_availability_zones.available.names
  public_subnets     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]

  enable_nat_gateway   = true
  enable_dns_hostnames = true

}

data "aws_subnet_ids" "sofin-net-ids" {
  depends_on = [
    module.vpc
  ]
  vpc_id =  module.vpc.vpc_id
}

resource "aws_db_subnet_group" "sofin-net-gr" {
  name       = "main"
  subnet_ids = data.aws_subnet_ids.sofin-net-ids.ids
}

