"http://34.123.28.173:5052/

Invoke-WebRequest -Uri "http://34.123.28.173:5052/time?city=Ottawa" -Headers @{ Authorization = "Bearer secret-token-123" }
