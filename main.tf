provider "google" {
  project = "sincere-quasar-346017"
  region  = "us-west4"
}

resource "google_storage_bucket" "app_bucket" {
  name = "pouroverlabs-django-jwt-auth-test-bucket"
  location = "us-west4"
}

# Upload app files and docker-compose file to the storage bucket
resource "google_storage_bucket_object" "app_files" {
  bucket = "${google_storage_bucket.app_bucket.name}"
  name   = "app_files.zip"
  source = "./app_files.zip"
}

# Create a VM instance template from the custom image
resource "google_compute_instance" "app" {
  name        = "app-template"
  machine_type = "n1-standard-1"
  zone         = "us-west4-a"
  
  boot_disk {
    initialize_params {
      image = "ubuntu-1804-bionic-v20221201"
    }
  }

  metadata_startup_script = <<EOF
#!/bin/bash

# Install unzip
sudo apt update
sudo apt install -y unzip

# Download app files and docker-compose file from the storage bucket
gsutil cp gs://${google_storage_bucket.app_bucket.name}/app_files.zip app_files.zip

# Extract app files and docker-compose file
unzip app_files.zip

# Run docker-compose
docker-compose up -d
EOF

  network_interface {
    network = "default"
    access_config {
      // Use the firewall rule created above
      network_tier = "PREMIUM"
      nat_ip       = "${google_compute_address.my_address.address}"
    }
  }
}

resource "google_compute_firewall" "allow_internet_access" {
  name    = "allow-internet-access"
  network = "default"


  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "443", "3000", "8000"]
  }

  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_network" "my_network" {
  name                    = "my-network"
}

# Create a subnetwork in the custom network
# resource "google_compute_subnetwork" "my_subnetwork" {
#   name          = "my-subnetwork"
#   network       = "${google_compute_network.my_network.self_link}"
#   ip_cidr_range = "10.0.0.0/16"
# }

resource "google_compute_address" "my_address" {
  name = "my-address"
  region = "us-west4"
}

