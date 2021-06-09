resource "kubernetes_namespace" "sofin_dev" {
  metadata {
    annotations = {
      name = "This namespace is for development"
    }

    labels = {
      mylabel = "dev"
    }

    name = "development"
  }
}

resource "kubernetes_namespace" "sofin_prod" {
  metadata {
    annotations = {
      name = "This namespace is for productive env"
    }

    labels = {
      mylabel = "prod"
    }

    name = "production"
  }
}

