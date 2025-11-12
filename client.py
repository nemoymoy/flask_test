import requests

# response = requests.post(
#     url='http://127.0.0.1:5000/users',
#     json={'login': 'user_2', 'password':'simple password'},
#
# )
# print(response.status_code)
# print(response.text)

# response = requests.get(
#     url='http://127.0.0.1:5000/users/3',
#
# )
# print(response.status_code)
# print(response.text)

# response = requests.patch(
#     url='http://127.0.0.1:5000/users/3',
# json={'login': 'user_2_up',},
# )
# print(response.status_code)
# print(response.text)
#
# response = requests.get(
#     url='http://127.0.0.1:5000/users/3',
#
# )
# print(response.status_code)
# print(response.text)

response = requests.delete(
    url='http://127.0.0.1:5000/users/3',

)
print(response.status_code)
print(response.text)

response = requests.get(
    url='http://127.0.0.1:5000/users/3',

)
print(response.status_code)
print(response.text)