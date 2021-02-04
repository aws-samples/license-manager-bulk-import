import boto3
from botocore.config import Config
from amis import windows_amis, sql_amis

config = Config(
   retries = {
      'max_attempts': 10,
      'mode': 'adaptive'
   }
)
license_manager = boto3.client('license-manager', config = config)

def register_license(product_name, count_type, count, ami_arn, rules = None):
    response = license_manager.create_license_configuration(
        Name=product_name,
        LicenseCountingType=count_type,
        LicenseCount=count,
        LicenseCountHardLimit=True,
        LicenseRules=rules,
        DisassociateWhenNotFound=True
    )
    if ami_arn is not None:
        license_manager.update_license_specifications_for_resource(
            ResourceArn=ami_arn,
            AddLicenseSpecifications=[
                {
                    'LicenseConfigurationArn': response['LicenseConfigurationArn'],
                    'AmiAssociationScope': 'cross-account'
                }
            ]
        )

def register_windows_server_standard(family, version, quantity):
  product_name = 'Windows Server Standard {}'.format(version)
  print ('Registering ' + product_name)
  register_license(
      product_name, 
      'Core', 
      quantity,
      windows_amis['Windows Server Standard'].get(version),
      [
          '#allowedTenancy=EC2-DedicatedHost', 
          '#licenseAffinityToHost=90'
      ])

def register_windows_server_datacenter_2_proc(family, version, quantity):
  product_name = 'Windows Server Datacenter {}'.format(version)
  register_license(
      product_name, 
      'Core', 
      quantity, 
      windows_amis['Windows Server Datacenter'].get(version),
      [
          '#allowedTenancy=EC2-DedicatedHost', 
          '#licenseAffinityToHost=90'
      ])

def register_windows_server_datacenter(family, version, quantity):
  product_name = 'Windows Server Datacenter {}'.format(version)
  register_license(
      product_name, 
      'Core', 
      quantity,
      windows_amis['Windows Server Datacenter'].get(version),
      [
          '#allowedTenancy=EC2-DedicatedHost', 
          '#licenseAffinityToHost=90'
      ])

def register_sql_server_standard(family, version, quantity):
  product_name = 'SQL Server - Standard {} (vCPU)'.format(version)
  register_license(
      product_name, 
      'vCPU', 
      quantity,
      sql_amis['SQL Server Standard'].get(version),
      [ '#honorVcpuOptimization=True' ])

def register_sql_server_enterprise(family, version, quantity):
  product_name = 'SQL Server Enterprise {} (Core)'.format(version)
  register_license(
      product_name,
      'Core',
      quantity,
      sql_amis['SQL Server Enterprise'].get(version))

# The products we know how to register
product_registrars = {
        'Windows Server - Standard': register_windows_server_standard,
        'Windows Server Datacenter - 2 Proc': register_windows_server_datacenter_2_proc,
        'Windows Server - Datacenter': register_windows_server_datacenter,
        'SQL Server - Standard': register_sql_server_standard,
        'SQL Server Enterprise Core': register_sql_server_enterprise
    }