import pytest
from httpx import AsyncClient


special_key=None
reftoken=None

@pytest.mark.asyncio
async def test_login_user_admin_login_post(testing_client):
            """Test case for login_user_admin_login_post

            Login User
            """
            async with AsyncClient(app=testing_client, base_url="http://test") as client:
                login_user_model = {"password":"password","grant_type":"authorization_code","username":"Bushu","token":"none"}
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response = await client.post(
                    "/admin/login",
                    headers={},
                    json=login_user_model,
                )
               
            assert response.status_code == 500
                # uncomment below to assert the status code of the HTTP response
                # ##############################################################################
            async with AsyncClient(app=testing_client, base_url="http://test") as client:
                login_user_model = {
                        "grant_type": "authorization_code",
                        "username": "superspecial",
                        "password": "password",
                        "token": "none"
                                }
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response2 = await client.post(
                    "/admin/login",
                    headers=headers,
                    json=dict(login_user_model),
                )
            global reftoken
            global special_key
            
            reftoken=response2.json()["refresh_token"]
            special_key=response2.json()["access_token"]
                
            assert response2.status_code == 200
           
                # ####################################################################################
            async with AsyncClient(app=testing_client, base_url="http://test") as client:
                login_user_model = {
                        "grant_type": "authorization_code",
                        "username": "superspecial",
                        "password": "password3",
                        "token": "none"
                                }
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response3 = await client.post(
                    "/admin/login",
                    headers=headers,
                    json=dict(login_user_model),
                )     
            assert response3.json() == {"Message":"Invalid Password"}
            assert response3.status_code == 200
                # ####################################################################################
            async with AsyncClient(app=testing_client, base_url="http://test") as client:  
                login_user_model = {"password":"password","grant_type":"refresh_token","username":"superspecial","token":reftoken}
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response4 = await client.post(
                    "/admin/login",
                    headers=headers,
                    json=login_user_model,
                )

                # uncomment below to assert the status code of the HTTP response
            assert response4.status_code == 200
                # #################################################################################### 
                # ####################################################################################
            async with AsyncClient(app=testing_client, base_url="http://test") as client:  
                login_user_model = {"password":"password","grant_type":"refresh_token","username":"superspecial","token":'assdfasd'}
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response5 = await client.post(
                    "/admin/login",
                    headers=headers,
                    json=login_user_model,
                )

                # uncomment below to assert the status code of the HTTP response
            assert response5.status_code == 500
                # #################################################################################### 
                # ####################################################################################
            async with AsyncClient(app=testing_client, base_url="http://test") as client: 
                login_user_model = {"password":"password","grant_type":"token_decode","username":"Bushu","token":special_key}
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response6 = await client.post(
                    "/admin/login",
                    headers=headers,
                    json=login_user_model,
                )
                # # uncomment below to assert the status code of the HTTP response
            
            assert response6.status_code == 200
                # #################################################################################### 
            async with AsyncClient(app=testing_client, base_url="http://test") as client: 
                login_user_model = {"password":"password","grant_type":"token_decode","username":"Bushu","token":special_key+'asdfasdf'}
                
                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                }
                response7 = await client.post(
                    "/admin/login",
                    headers=headers,
                    json=login_user_model,
                )
                # # uncomment below to assert the status code of the HTTP response
            
            assert response7.status_code == 500
                # #################################################################################### 
@pytest.mark.asyncio
async def test_get_all_users_admin_users_all_get(testing_client):
    """Test case for get_all_users_admin_users_all_get

    Get All Users
    """
    async with AsyncClient(app=testing_client, base_url="http://test") as client:
        
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {special_key}',
                       
        }
        response = await client.get(
            "/admin/users/all",
            headers=headers,
        )
    
    print(response.json())
    assert response.status_code == 200

# def test_add_user_roles_admin_addroles_post(client: TestClient):
#     """Test case for add_user_roles_admin_addroles_post

#     Add User Roles
#     """
#     roles_users_model = {"user_id":0,"role_id":6}

#     headers = {
#         # "Authorization": "f"Bearer {special-key}"",
#          "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "POST",
#         "/admin/addroles",
#         headers=headers,
#         json=roles_users_model,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_delete_all_roles_admin_role_all_delete(client: TestClient):
#     """Test case for delete_all_roles_admin_role_all_delete

#     Delete All Roles
#     """

#     headers = {
#         "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "DELETE",
#         "/admin/role/all",
#         headers=headers,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_delete_all_user_admin_user_all_delete(client: TestClient):
#     """Test case for delete_all_user_admin_user_all_delete

#     Delete All User
#     """

#     headers = {
#         "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "DELETE",
#         "/admin/user/all",
#         headers=headers,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_delete_role_admin_role_item_id_delete(client: TestClient):
#     """Test case for delete_role_admin_role_item_id_delete

#     Delete Role
#     """

#     headers = {
#         "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "DELETE",
#         "/admin/role/{item_id}".format(item_id=56),
#         headers=headers,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_delete_user_admin_user_item_uuid_delete(client: TestClient):
#     """Test case for delete_user_admin_user_item_uuid_delete

#     Delete User
#     """

#     headers = {
#         "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "DELETE",
#         "/admin/user/{item_uuid}".format(item_uuid='item_uuid_example'),
#         headers=headers,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_delete_user_roles_admin_deleteroles_role_id_user_id_delete(client: TestClient):
#     """Test case for delete_user_roles_admin_deleteroles_role_id_user_id_delete

#     Delete User Roles
#     """

#     headers = {
#         "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "DELETE",
#         "/admin/deleteroles/{role_id}/{user_id}".format(role_id=56, user_id=56),
#         headers=headers,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_get_all_roles_admin_roles_all_get(client: TestClient):
#     """Test case for get_all_roles_admin_roles_all_get

#     Get All Roles
#     """

#     headers = {
#         "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "GET",
#         "/admin/roles/all",
#         headers=headers,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200




# def test_get_role_admin_role_item_id_get(client: TestClient):
#     """Test case for get_role_admin_role_item_id_get

#     Get Role
#     """

#     headers = {
#         "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "GET",
#         "/admin/role/{item_id}".format(item_id=56),
#         headers=headers,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_get_user_admin_user_item_uuid_get(client: TestClient):
#     """Test case for get_user_admin_user_item_uuid_get

#     Get User
#     """

#     headers = {
#         "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "GET",
#         "/admin/user/{item_uuid}".format(item_uuid='item_uuid_example'),
#         headers=headers,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_index_get(client: TestClient):
#     """Test case for index_get

#     Index
#     """

#     headers = {
#     }
#     response = client.request(
#         "GET",
#         "/",
#         headers=headers,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_login_token_admin_token_post(client: TestClient):
#     """Test case for login_token_admin_token_post

#     Login Token
#     """

#     headers = {
#     }
#     data = {
#         "grant_type": 'grant_type_example',
#         "username": 'username_example',
#         "password": 'password_example',
#         "scope": '',
#         "client_id": 'client_id_example',
#         "client_secret": 'client_secret_example'
#     }
#     response = client.request(
#         "POST",
#         "/admin/token",
#         headers=headers,
#         data=data,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_login_user_admin_login_post(client: TestClient):
#     """Test case for login_user_admin_login_post

#     Login User
#     """
#     login_user_model = {"password":"password","grant_type":"authorization_code","username":"username","token":"none"}

#     headers = {
#     }
#     response = client.request(
#         "POST",
#         "/admin/login",
#         headers=headers,
#         json=login_user_model,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     assert response.status_code == 200


# def test_register_roles_admin_role_register_post(client: TestClient):
#     """Test case for register_roles_admin_role_register_post

#     Register Roles
#     """
#     role_model = {"name":"name","description":"description"}

#     headers = {
#         "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "POST",
#         "/admin/role/register",
#         headers=headers,
#         json=role_model,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_register_user_admin_user_register_post(client: TestClient):
#     """Test case for register_user_admin_user_register_post

#     Register User
#     """
#     user_model = {"password":"password","last_name":"last_name","disabled":1,"middle_name":"middle_name","first_name":"first_name","email":"email","username":"username"}

#     headers = {
#         "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "POST",
#         "/admin/user/register",
#         headers=headers,
#         json=user_model,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_test_oauth2_admin_testoauth_get(client: TestClient):
#     """Test case for test_oauth2_admin_testoauth_get

#     Test Oauth2
#     """

#     headers = {
#         "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "GET",
#         "/admin/testoauth",
#         headers=headers,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_update_role_admin_roleupdate_item_id_put(client: TestClient):
#     """Test case for update_role_admin_roleupdate_item_id_put

#     Update Role
#     """
#     role_model_all = {"name":"name","description":"description","id":0}

#     headers = {
#         "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "PUT",
#         "/admin/roleupdate/{item_id}".format(item_id=56),
#         headers=headers,
#         json=role_model_all,
#     )

#     # uncomment below to assert the status code of the HTTP response
#     #assert response.status_code == 200


# def test_update_user_admin_userrole_item_uuid_put(client: TestClient):
#     """Test case for update_user_admin_userrole_item_uuid_put

#     Update User
#     """
#     user_model = {"password":"password","last_name":"last_name","disabled":1,"middle_name":"middle_name","first_name":"first_name","email":"email","username":"username"}

#     headers = {
#         "Authorization": f"Bearer {special_key}",
#     }
#     response = client.request(
#         "PUT",
#         "/admin/userrole/{item_uuid}".format(item_uuid='item_uuid_example'),
#         headers=headers,
#         json=user_model,
#     )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

