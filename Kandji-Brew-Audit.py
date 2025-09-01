import requests
import os


kandji_api_token = os.environ.get("kandji_api_token")
kandji_domain=os.environ.get("kandji_domain")
authorisation_value = str('Bearer ') + kandji_api_token

### Brew Audit Library Item ID is: b5d21f9e-9d41-4463-b2b5-c292b3c2ccad
### You can get from the full URL in Kandji : https://domain.kandji.io/library/custom-scripts/b5d21f9e-9d41-4463-b2b5-c292b3c2ccad/status

url = "https://"+kandji_domain+".api.kandji.io/api/v1/library/library-items/b5d21f9e-9d41-4463-b2b5-c292b3c2ccad/status"

payload = {}
headers = {
  'Authorization': authorisation_value
}

while url:  # keep looping until 'next' is None
  response = requests.request("GET", url, headers=headers, data=payload)
  json_response = response.json()

  for value in range(len(json_response["results"])):
    log_lines = json_response["results"][value]["log"]
    ## Avoid any errors in case there is a Null result (Script hasn't run yet)
    if log_lines:
      # Only process logs that contain "Script results:" (actual package data)
      # Skip computers with error messages
      if ("Script results:" in log_lines and 
          "Homebrew is not installed or not in PATH" not in log_lines and
          "Error: Could not determine local user directory" not in log_lines and
          "sudo: /opt/homebrew/bin/brew: command not found" not in log_lines):
        script_results = log_lines.split("Script results:")[1].strip()
        # Split by newlines and print each package line
        for line in script_results.split('\n'):
          if line.strip() and not line.startswith("Exit code:"):  # Only print non-empty lines and skip exit codes
            print(f'{json_response["results"][value]["computer"]["name"]},{line.strip()}')
      # If no "Script results:" found or contains errors, skip this computer entirely
  
  # ✅ assign url to the next page, if any
  url = json_response.get("next")


## Typical JSON Response
#    "count": 380,
#     "next": "https://xxx.api.kandji.io/api/v1/library/library-items/b5d21f9e-9d41-4463-b2b5-c292b3c2ccad/status?limit=300&offset=300",
#     "previous": null,