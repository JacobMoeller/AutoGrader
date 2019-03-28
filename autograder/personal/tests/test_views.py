from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from personal.models import Courses
from django.contrib.auth.models import Group, Permission


class InstructorHomePageViewTest(TestCase):
    #fixtures = ['initial_data.json', ]

    @classmethod
    def setUpTestData(cls):

        # Create two users
        cls.test_group1 = Group.objects.create(name='Instructor')
        cls.test_group1 = Group.objects.create(name='Student')
        cls.test_group1 = Group.objects.create(name='Grader')
        # Create two users
        cls.test_user1 = User.objects.create_user(
            username='testuser1',
            password='password')
        cls.test_user2 = User.objects.create_user(
            username='testuser2',
            password='password')
        cls.test_user1.save()

        # Add test_user1 to Instructor group
        group = Group.objects.get(name="Instructor")
        group.user_set.add(cls.test_user1)

        cls.test_user2.save()

        # Add test_user2 to Student group
        group = Group.objects.get(name="Student")
        group.user_set.add(cls.test_user2)

        # Create 4 courses
        number_of_courses = 4
        for course_id in range(number_of_courses):
            cls.course = Courses.objects.create(
                course_title = f'CIS_201 {course_id}',
                course_number=405, id=course_id,
                course_crn=12345+course_id,
                instructor_username=cls.test_user1,
            )
            cls.course.save()


    # Tests to see if the url is correct
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    ## Tests to see if the url name is accessible
    def test_view_url_accessible_by_name(self):
         response = self.client.get(reverse('homepage'), follow=True)
         self.assertEqual(response.status_code, 200)
