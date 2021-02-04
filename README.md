# AWS Sample: Bulk Import Licenses into License Manager

Welcome! This repository contains code that demonstrates how a customer could use the AWS License Manager APIs to perform a bulk import of their licenses from a license statement. In this example, we're assuming that the source document containing the list of product licenses is a Microsoft Excel spreadsheet with a Worksheet named "License Summary." In addition, we're also assuming that the first line containing product information is line 5 of your spreadsheet. You can change both of these things in main.py.

You will need to create a file named amis.py that maps products to AMI IDs created by importing your server images. A template file (named, fittingly, amis.py.template) has been provided as an example; simply copy this file to a new file named amis.py and replace the fake IDs in the template with your actual AMI IDs.

License configurations are created and registered using functions defined in registrars.py. A few examples that match the list from our sample spreadsheet have been provided, but you can add your own by adding a new function and registering the function in the `product_registrars` variable.

Finally, this sample assumes that you have pre-configured your environment with IAM credentials, either in a credentials file or using an EC2 instance profile. However you provide credentials, the user/role will at least need permission to invoke license-manager:CreateLicense and license-manager:UpdateLicenseSpecificationsForResource.