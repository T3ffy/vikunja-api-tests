# Manual requests
## Create user
- curl.exe -i -X POST "http://localhost:3456/api/v1/register" -H "Content-Type: application/json" -d '{\"email\":\"u2@example.com\",\"is_admin\":false,\"language\":\"ru-RU\",\"name\":\"u2\",\"password\":\"u2password\",\"skip_email_confirm\":true,\"username\":\"u2username\"}'

## Login 
- curl.exe -i -X POST "http://localhost:3456/api/v1/login" -H "Content-Type: application/json"  -d '{\"username\":\"u1username\",\"password\":\"u1password\"}'

## Create project
- curl.exe -i -X PUT "http://localhost:3456/api/v1/projects" -H "Content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3OTA4NTU5ODcsImlkIjoxLCJpc19hZG1pbiI6ZmFsc2UsImp0aSI6ImE2MDgwOGRmLTE3YzktNDhhMi1hY2I2LWFjY2YxYTAzN2RiMiIsInNpZCI6IjQ4ODZkZThiLWM0ZjUtNGVlZS1iNjJjLTFmMjAyNTMzYWZmMSIsInR5cGUiOjEsInVzZXJuYW1lIjoidTF1c2VybmFtZSJ9.ZAD6H5ZPlsxjZPIaeilmklS6mnPn4dzPK84s6a63w_M" -d '{\"title\":\"New_Project\"}'

##  Create task
- curl.exe -i -X PUT "http://localhost:3456/api/v1/projects/3/tasks" -H "Content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3OTA4NTU5ODcsImlkIjoxLCJpc19hZG1pbiI6ZmFsc2UsImp0aSI6ImE2MDgwOGRmLTE3YzktNDhhMi1hY2I2LWFjY2YxYTAzN2RiMiIsInNpZCI6IjQ4ODZkZThiLWM0ZjUtNGVlZS1iNjJjLTFmMjAyNTMzYWZmMSIsInR5cGUiOjEsInVzZXJuYW1lIjoidTF1c2VybmFtZSJ9.ZAD6H5ZPlsxjZPIaeilmklS6mnPn4dzPK84s6a63w_M" -d '{\"title\":\"NEW_TASK\"}'

## Edit task
- curl.exe -i -X POST "http://localhost:3456/api/v1/tasks/1" -H "Content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3OTA4NTY2NDEsImlkIjoxLCJpc19hZG1pbiI6ZmFsc2UsImp0aSI6ImVjM2ZhNmRhLTlkOTYtNGY1Zi1iZjM2LTc3MzkxN2RhNTk4MyIsInNpZCI6Ijk4ZGI0YzU0LWQ2NzItNDk0NS05NDE3LWNlMDQzYTkzNDQyMCIsInR5cGUiOjEsInVzZXJuYW1lIjoidTF1c2VybmFtZSJ9.t5BlFcTpILEPfD0pueXk0rbtkE5bCLqA6FLCWdCOAt0" -d '{\"title\":\"NEW-NEW_TASK\"}'

## Delete task
- curl.exe -i -X DELETE "http://localhost:3456/api/v1/tasks/1" -H "Content-type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3OTA4NTY2NDEsImlkIjoxLCJpc19hZG1pbiI6ZmFsc2UsImp0aSI6ImVjM2ZhNmRhLTlkOTYtNGY1Zi1iZjM2LTc3MzkxN2RhNTk4MyIsInNpZCI6Ijk4ZGI0YzU0LWQ2NzItNDk0NS05NDE3LWNlMDQzYTkzNDQyMCIsInR5cGUiOjEsInVzZXJuYW1lIjoidTF1c2VybmFtZSJ9.t5BlFcTpILEPfD0pueXk0rbtkE5bCLqA6FLCWdCOAt0" -d '{\"title\":\"NEW-NEW_TASK\"}'
