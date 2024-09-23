client_id = 'P1LHBKUBWJ-100'
secret_key = '4NBJQHU4BO'
redirect_uri ='https://www.google.com/'
response_type = "code"  
state = "sample_state" 
grant_type = "authorization_code"
user_name = 'YS38001'
totp_key = 'QMFSLXH7C5Z4C7HL2OZCXWX6Q75FVDVL'
pin1 = '9'
pin2 = '8'
pin3 = '4'
pin4 = '4'
url='https://www.google.com/?s=ok&code=200&auth_code=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE3MjY5OTY1NDEsImV4cCI6MTcyNzAyNjU0MSwibmJmIjoxNzI2OTk1OTQxLCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJZUzM4MDAxIiwib21zIjoiSzEiLCJoc21fa2V5IjoiZmU0OTIzNjc1MDJhOGRiNTc0ZGZkZDkzOWNiODZkMTc2MmMyNmEyYWM0MjRiMWU0MDVkNjg1YTQiLCJub25jZSI6IiIsImFwcF9pZCI6IlAxTEhCS1VCV0oiLCJ1dWlkIjoiM2Q2MTlhNDYxNzE3NDExMjk2NTY1Yjk2ODhiN2UyODgiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.Jz10Zwju4AkmmeNmJ_Qtcn7KhHkVumTEYKo-uN8nljg&state=None'
s1=url.split('auth_code=')
auth_code =s1[1].split('&state')[0]

print (auth_code)