Before Proceeding, make sure you have coreved the following:

- Entra App information (Unique - One per each Application you're about to deploy: App ID, Tenant ID, Secret)

Click Here to Deploy Web Apps to Azure

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fthiagogbeier%2Fflask_azure_app%2Fmain%2Fazuredeploy.json)

When Web App is up and running check the following:

- Web App main URL

Alternate deployment

az deployment group create --resource-group <resource-group-name> --template-uri https://raw.githubusercontent.com/thiagogbeier/flask_azure_app/main/azuredeploy.json --parameters siteName=myuniquesite123 clientId=xxxxx clientSecret=xxxxx tenantId=xxxxx

Web App expected outcome

![Alt text](webappservice-image1.png "This is the image title")
