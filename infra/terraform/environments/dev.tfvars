environment              = "dev"
location                 = "eastus"
project_name             = "aksdevsecops"
aks_node_count           = 1
postgres_sku             = "B_Standard_B1ms"
enable_zone_redundant_ha = false

tags = {
  Environment = "dev"
  CostCenter  = "CC-DEV-001"
  Owner       = "platform-engineering"
  ManagedBy   = "terraform"
}
