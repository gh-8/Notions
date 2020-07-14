from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from .models import Notion
# Create your tests here.
User = get_user_model()

class NotionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',password='somepw')
        Notion.objects.create(content="my first notion", user=self.user)
        Notion.objects.create(content="my second notion", user=self.user)
        Notion.objects.create(content="my third notion", user=self.user)
        self.currentCount = Notion.objects.all().count()


    def test_notion_created(self):
        notion_obj = Notion.objects.create(content="my second notion", user=self.user)
        self.assertEqual(notion_obj.id,4)
        self.assertEqual(notion_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepw')
        return client

    def test_notion_list(self):
        client = self.get_client()
        response = client.get("/api/notions/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()),1)

    def test_notion_list(self):
        client = self.get_client()
        response = client.get("/api/notions/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()),3)
    
    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/notions/action/", {"id":1 ,"action":"like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)
        print(response.json())
    
    def test_action_unlike(self):
        #like first then unlike
        client = self.get_client()
        response = client.post("/api/notions/action/", {"id":2 ,"action":"like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/notions/action/", {"id":2 ,"action":"unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)
    
    def test_action_share(self):
        #share a post then count number of posts
        client = self.get_client()
        response = client.post("/api/notions/action/", {"id":2 ,"action":"share"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_notion_id = data.get("id")
        self.assertNotEqual(2,new_notion_id)
        self.assertEqual(self.currentCount +1, new_notion_id)
    
    def test_notion_create_api(self):
        request_data = {"content": "This is my test notion"}
        client = self.get_client()
        response = client.post("/api/notions/create/",request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_notion_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_notion_id)
    
    def test_notion_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/notions/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)