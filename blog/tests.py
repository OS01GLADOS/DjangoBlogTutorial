from django.test import TestCase, Client
from django.contrib.auth.models import User
from blog.models import Post


class BlogPostTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='teiko', password='mirai')
        user = User.objects.create_user(username='user2', password='none')
        Post.objects.create(author_id=user.id, title='test', content='testsd')
        self.client.login(username='user2', password='none')

    def testUpdate(self):
        new_title = 'changed title'
        new_content = 'changed content'
        res = self.client.post('/post/1/update', {'content': new_content, 'title': new_title})
        post = Post.objects.all().first()
        self.assertEqual(new_title, post.title)
        self.assertEqual(new_content, post.content)

    def testDelete(self):
        res = self.client.post('/post/1/delete')
        post = Post.objects.all().first()
        self.assertIsNone(post)


# Create your tests here.
class BlogTestCase(TestCase):

    def test_404(self):
        response = self.client.get('/something/weird')
        self.assertEqual(response.status_code, 404)

    def test_403(self):
        User.objects.create_user(username='teiko', password='mirai')
        user = User.objects.create_user(username='user2', password='none')
        Post.objects.create(author_id=user.id, title='test', content='testsd')
        self.client.login(username='teiko', password='mirai')
        result = self.client.get('/post/1/update')
        self.assertEqual(result.status_code, 403)
        self.client.logout()
        self.client.login(username='user2', password='none')
        result = self.client.get('/post/1/update')
        self.assertEqual(result.status_code, 200)
