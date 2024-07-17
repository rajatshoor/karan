provider "google" {
  credentials = file("~/ica1-429000-82d557a68848.json")
  project     = "ica1-429000"
  region      = "us-central1"
  zone        = "us-central1-a"
}

# Data source to fetch access token
data "google_client_config" "default" {}

provider "kubernetes" {
  host                   = "https://${google_container_cluster.primary.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(google_container_cluster.primary.master_auth[0].cluster_ca_certificate)
}

# Create GKE Cluster
resource "google_container_cluster" "primary" {
  name     = "iac2"
  location = "us-central1-a"

  initial_node_count = 1

  node_config {
    machine_type = "e2-medium"
  } # <- This closing brace was missing

  # Disable deletion protection
  deletion_protection = false
}

#Create Kubernetes Namespaces
resource "kubernetes_namespace" "backend" {
  metadata {
    name = "backend"
  }
}

resource "kubernetes_namespace" "frontend" {
  metadata {
    name = "frontend"
  }
}
