from rollic_backend.models import User
from rest_framework import status
from rest_framework.test import APITestCase

class PutReqTestCase(APITestCase):

    def setUp(self) -> None:

        self.wrong_req_body = {"name": '',"email": "", "password": "" }
        self.missed_req_body = {"name": '', "password": "" }
        self.valid_req_body = {"name": 'temp_user',"email": "temp_user@gmail.com", "password": "pass" }
        
    def testcase_wrong_request(self):
        response = self.client.put("/users", self.missed_req_body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def testcase_missed_req_body(self):
        response = self.client.put("/users", self.wrong_req_body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def testcase_valid_req_body(self):
        response = self.client.put("/users", self.valid_req_body, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testcase_twice_same_req(self):
        self.client.put("/users", self.valid_req_body, format="json")
        response = self.client.put("/users", self.valid_req_body, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PatchReqTestCase(APITestCase):

    def setUp(self) -> None:

        self.wrong_req_body = {"name": 12 , "password": "" }
        self.missed_req_body = {"name": ''}
        self.valid_req_body = {"name": 'temp_user',"email": "temp_user@gmail.com", "password": "pass" }
        self.valid_new_req_body = {"name": 'new__', "password": "new__" }
        self.client.put("/users", self.valid_req_body, format="json")
    
    def testcase_req2invalid_user_id(self):
        response = self.client.patch("/users/24", self.valid_new_req_body, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def testcase_wrong_request(self):
        response = self.client.patch("/users/1", self.missed_req_body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def testcase_missed_req_body(self):
        response = self.client.patch("/users/1", self.wrong_req_body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def testcase_valid_req_body(self):
        response = self.client.patch("/users/1", self.valid_new_req_body, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetReqTestCase(APITestCase):
    def setUp(self) -> None:
        self.valid_req_body = {"name": 'temp_user',"email": "temp_user@gmail.com", "password": "pass" }
        self.client.put("/users", self.valid_req_body, format="json")

    def testcase_req2invalid_user_id(self):
        response = self.client.get("/users/10000", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def testcase_valid_req_body(self):
        response = self.client.get("/users/1", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(response.json()['name'], self.valid_req_body['name'])

class GetsReqTestCase(APITestCase):
    def setUp(self) -> None:
        self.wrong_req_body = {"name": "sz" , "password": "as" }
        self.valid_req_body = {"name": 'temp_user',"email": "temp_user@gmail.com", "password": "pass" }
        self.valid_req_body_2 = {"name": 'temp_user_2',"email": "temp_user_2@gmail.com", "password": "pass" }
    
    def testcase_server_error(self):
        response = self.client.post("/users", format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED) 

    def testcase_get_empty_db(self):
        response = self.client.get("/users", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND) 

    def testcase_valid_req_body(self):
        self.client.put("/users", self.valid_req_body, format="json")
        self.client.put("/users", self.valid_req_body_2, format="json")

        response = self.client.get("/users", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(len(response.json()), 2)

class DelReqTestCase(APITestCase):
    def setUp(self) -> None:
        self.wrong_req_body = {"name": "sz" , "password": "as" }
        self.valid_req_body = {"name": 'temp_user',"email": "temp_user@gmail.com", "password": "pass" }
        self.client.put("/users", self.valid_req_body, format="json")
    
    def testcase_valid_req_body(self):
        response = self.client.delete("/users/1", format="json")
        response_2 = self.client.delete("/users/1", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)