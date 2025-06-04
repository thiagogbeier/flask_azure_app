_Before Proceeding, make sure you have coreved the following:_

- Entra App information (Unique - One per each Application you're about to deploy: App ID, Tenant ID, Secret)

_Click Here to Deploy Web Apps to Azure_

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fthiagogbeier%2Fflask_azure_app%2Fmain%2Fazuredeploy.json)

Make sure to validate if you are creating New Resource Group (click on Create New) or select existing.

![Alt text](webappservice-image2.png "Azure Teamplate Wizard")

_When Web App is up and running check the following:_

- Web App main URL

_Alternate deployment_

az deployment group create --resource-group <resource-group-name> --template-uri https://raw.githubusercontent.com/thiagogbeier/flask_azure_app/main/azuredeploy.json --parameters siteName=myuniquesite123 clientId=xxxxx clientSecret=xxxxx tenantId=xxxxx

_Web App expected outcome_

![Alt text](webappservice-image1.png "Azure web apps when completed")
