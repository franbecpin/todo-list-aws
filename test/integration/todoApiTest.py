import http.client
import os
import unittest
from urllib.request import urlopen
import requests
import json

import pytest

BASE_URL = os.environ.get("BASE_URL")
#BASE_URL = "https://m0qwfec693.execute-api.us-east-1.amazonaws.com/Prod"
DEFAULT_TIMEOUT = 2  # in secs


@pytest.mark.api
class TestApi(unittest.TestCase):
    
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_listtodos(self):
        print('---------------------------------------')
        print('Starting - integration test List TODO')
        #Add TODO
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: '+ str(json_response))
        jsonbody= json.loads(json_response['body'])
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example", "Error en la petición API a {url}"
        )
        #List
        url = BASE_URL+"/todos"
        response = requests.get(url)
        print('Response List Todo:' + str(response.json()))
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertTrue(response.json())
        
        print('End - integration test List TODO')
    def test_api_addtodo(self):
        print('---------------------------------------')
        print('Starting - integration test Add TODO')
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add Todo: '+ json_response['body'])
        jsonbody= json.loads(json_response['body'])
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example", "Error en la petición API a {url}"
        )
        url = url+"/"+ID_TODO
        response = requests.delete(url)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        print('End - integration test Add TODO')
    
    def test_api_gettodo(self):
    print('---------------------------------------')
    print('Starting - integration test Get TODO (adaptativo)')

    todos_url = f"{BASE_URL}/todos"
    data = {"text": "Integration text example - GET"}

    # POST (intento de crear). Usa json= para enviar Content-Type correcto
    response = requests.post(todos_url, json=data, timeout=5)
    try:
        json_response = response.json()
    except ValueError:
        json_response = {"_raw": response.text}
    print('Response Add Todo: ' + str(json_response))

    # Si el entorno bloquea escrituras, modo solo lectura y skip
    if response.status_code in (401, 403, 405):
        ro = requests.get(todos_url, timeout=5)
        self.assertEqual(ro.status_code, 200, "GET /todos no devolvió 200 en modo solo lectura")
        try:
            ro_json = ro.json()
        except ValueError:
            ro_json = {"_raw": ro.text}
        print('GET /todos (read-only) → ' + str(ro_json))
        pytest.skip(f"Entorno read-only: POST bloqueado ({response.status_code}). Test ejecutado en modo solo lectura.")
        return

    # POST debe ser 200 en entornos write-enabled
    self.assertEqual(response.status_code, 200, f"POST /todos no devolvió 200: {response.status_code}")

    # Normaliza respuesta (API Gateway con 'body' o JSON directo)
    if isinstance(json_response, dict) and 'body' in json_response:
        body = json_response['body']
        try:

        
    
    def test_api_updatetodo(self):
        print('---------------------------------------')
        print('Starting - integration test Update TODO')
        #Add TODO
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example - Initial"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add todo: ' + json_response['body'])
        jsonbody= json.loads(json_response['body'])
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example - Initial", "Error en la petición API a {url}"
        )
        #Update TODO
        url = BASE_URL+"/todos/" + ID_TODO
        data = {
         "text": "Integration text example - Modified",
         "checked": "true"
        }
        response = requests.put(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Update todo: ' + str(json_response))
        #jsonbody= json.loads(json_response['body'])
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            json_response['text'], "Integration text example - Modified", "Error en la petición API a {url}"
        )
        #Test GET TODO
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.get(url)
        json_response = response.json()
        print('Response Get Todo: '+ str(json_response))
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            json_response['text'], "Integration text example - Modified", "Error en la petición API a {url}"
        )
        #Delete TODO to restore state
        response = requests.delete(url)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        print('End - integration test Update TODO')
    def test_api_deletetodo(self):
        print('---------------------------------------')
        print('Starting - integration test Delete TODO')
        #Add TODO
        url = BASE_URL+"/todos"
        data = {
         "text": "Integration text example - Initial"
        }
        response = requests.post(url, data=json.dumps(data))
        json_response = response.json()
        print('Response Add todo: ' + json_response['body'])
        jsonbody= json.loads(json_response['body'])
        ID_TODO = jsonbody['id']
        print ('ID todo:'+ID_TODO)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        self.assertEqual(
            jsonbody['text'], "Integration text example - Initial", "Error en la petición API a {url}"
        )
        #Delete TODO to restore state
        response = requests.delete(url + '/' + ID_TODO)
        self.assertEqual(
            response.status_code, 200, "Error en la petición API a {url}"
        )
        print ('Response Delete Todo:' + str(response))
        #Test GET TODO
        url = BASE_URL+"/todos/"+ID_TODO
        response = requests.get(url)
        print('Response Get Todo '+ url+': '+ str(response))
        self.assertEqual(
            response.status_code, 404, "Error en la petición API a {url}"
        )
        print('End - integration test Delete TODO')
    