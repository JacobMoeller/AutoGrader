from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from personal.models import Courses
class InstructorHomePageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        '''
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='password')
        test_user2 = User.objects.create_user(username='testuser2', password='password')
        
        test_user1.save()
        test_user2.save()
        '''
        
        #Create 4 courses
        number_of_courses = 4
        for course_id in range(number_of_courses):
            Courses.objects.create(
                course_title = f'CIS_201 {course_id}',
            )

    #Tests to see if the url is correct
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    #Tests to see if the url name is accessible
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    #Tests to see if the correct template is being used
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personal/homepage.html')

    #Tests to see if the 4 courses are being shown
    def test_view_all_courses(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['course_list']) == 4)

