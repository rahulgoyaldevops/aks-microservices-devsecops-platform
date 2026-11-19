variable "environment" {
  description = "Deployment environment (e.g., dev, prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "location" {
  description = "Azure region for all resources"
  type        = string
  default     = "eastus"
}

variable "project_name" {
  description = "Base project name used for resource naming"
  type        = string
  default     = "aks-devsecops"
}

variable "aks_node_count" {
  description = "Number of nodes in the default AKS system node pool"
  type        = number
  default     = 2
}

variable "postgres_sku" {
  description = "SKU name for Azure Database for PostgreSQL Flexible Server"
  type        = string
  default     = "B_Standard_B1ms"
}

variable "enable_zone_redundant_ha" {
  description = "Enable ZoneRedundant high availability for PostgreSQL Flexible Server"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Mandatory FinOps and governance tags applied to all resources"
  type        = map(string)

  validation {
    condition     = contains(keys(var.tags), "Environment") && contains(keys(var.tags), "CostCenter") && contains(keys(var.tags), "Owner")
    error_message = "FinOps tags must include Environment, CostCenter, and Owner."
  }
}
