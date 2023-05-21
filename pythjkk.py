using System;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace ManageSubscriptions
{
    class Program
    {
        static void Main(string[] args)
        {
            string tenantId = "<Enter your tenant ID>"; //Enter your tenant ID here
            string clientId = "<Enter your client ID>"; //Enter your client ID here
            string clientSecret = "<Enter your client secret>"; //Enter your client secret here
            string subscriptionId = "<Enter the subscription ID>"; //Enter your subscription ID here

            string authority = "https://login.microsoftonline.com/" + tenantId;
            string context = "https://management.azure.com/";
            string resource = "https://management.core.windows.net/";

            // Build authentication context and get token
            AuthenticationContext authenticationContext = new AuthenticationContext(authority);
            ClientCredential clientCredential = new ClientCredential(clientId, clientSecret);

            AuthenticationResult authenticationResult = authenticationContext.AcquireTokenAsync(resource, clientCredential).Result;
            string accessToken = authenticationResult.AccessToken;

            // Set the request URL
            string url = string.Format("{0}subscriptions/{1}/providers/Microsoft.Commerce/enableAutomaticRenewal?api-version=2015-06-01-preview", context, subscriptionId);

            // Make the HTTP request
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
            request.Method = "POST";
            request.Headers.Add("Authorization", "Bearer " + accessToken);

            try
            {
                HttpWebResponse response = (HttpWebResponse)request.GetResponse();
                Console.WriteLine("Subscription automatic renewal has been enabled.");
            }
            catch (WebException ex)
            {
                HttpWebResponse response = (HttpWebResponse)ex.Response;
                Console.WriteLine("Failed to enable subscription automatic renewal.");
                Console.WriteLine("Error message: " + response.StatusDescription);
            }

            Console.ReadKey();
        }
    }
}
