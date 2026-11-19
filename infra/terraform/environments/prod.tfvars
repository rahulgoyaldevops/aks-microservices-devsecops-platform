environment              = "prod"
location                 = "eastus"
project_name             = "aksdevsecops"
aks_node_count           = 3
postgres_sku             = "GP_Standard_D4s_v3"
enable_zone_redundant_ha = true

tags = {
  Environment = "prod"
  CostCenter  = "CC-PROD-001"
  Owner       = "platform-engineering"
  ManagedBy   = "terraform"
}
