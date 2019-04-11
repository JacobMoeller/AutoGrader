from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from personal.models import Courses
from http.cookies import SimpleCookie
from personal.models import Courses, Invite, Takes
from django.contrib.auth.models import Group, Permission


class InstructorHomePageViewTest(TestCase):
    fixtures = ['init_data.json', 'test_data1_auth.json',
        'test_data1.json', ]

    @classmethod
    def setUpTestData(cls):

        # Create two users
        # cls.test_group1 = Group.objects.create(name='Instructor')
        # cls.test_group1 = Group.objects.create(name='Student')
        # cls.test_group1 = Group.objects.create(name='Grader')
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
                course_title=f'CIS_201 {course_id}',
                course_number=405, id=course_id+200,
                course_crn=12346+course_id,
                instructor_username=cls.test_user1,
            )
            cls.course.save()

        cls.invite = Invite.objects.create(
                id=4000,
                sender_username=User.objects.get(username='testuser1'),
                rec_username=User.objects.get(username='testuser2'),
                course_id=Courses.objects.get(id=1),
                user_level="Student"
            )
        cls.invite.save()


    # Tests to see if the url is correct
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    # Tests to see if the url name is accessible
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('homepage'), follow=True)
        self.assertEqual(response.status_code, 200)

    # Tests to see if the correct template is being used; not signed in
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('homepage'), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(response.status_code, 200)

    # Tests to see if the correct template is being used; signed in
    def test_view_uses_homepage_template(self):
        self.client.force_login(self.test_user1)
        response = self.client.get(reverse('homepage'), follow=True)
        self.assertTemplateUsed(response, 'personal/homepage.html')
        self.assertEqual(response.status_code, 200)

    # Tests to see if the 4 courses are being shown
    def test_view_all_courses(self):
        login = self.client.login(username='testuser1', password='password')

        # check that user has four courses
        course_count = Courses.objects.filter(
            instructor_username=self.test_user1).count()
        self.assertEqual(course_count, 4)

        # see if four courses are displayed on instructor's homepage
        response = self.client.get(reverse('homepage'), follow=True)
        course_count_displayed = len(response.context['course_list'])
        self.assertEqual(course_count_displayed, 4)

    def test_can_set_and_flush_cookie(self):
        session = self.client.session
        session['test_cookie'] = 'True'
        session.save()

        self.assertEqual(session['test_cookie'], 'True')
        session.flush()
        self.assertTrue(not session.__contains__('test_cookie'))

    def test_logout_timeout(self):
        login = self.client.login(username='testuser1', password='password')
        response = self.client.get(reverse('homepage'), follow=True)
        session = self.client.session

        # view should check cookies and redirect to logout
        session.flush()
        response = self.client.get(reverse('homepage'), follow=True)
        self.assertTemplateUsed(response, 'registration/login.html')

    # Tests to see if the url is correct
    def test_view_url_redirects_at_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    # Tests to see if the url name is accessible
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('homepage'), follow=True)
        self.assertEqual(response.status_code, 200)


# Tests for the Email view.
class EmailPageTest(TestCase):

    # Tests to see if the url is correct
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/email/')
        self.assertEqual(response.status_code, 200)

    # Tests to see if the url name is accessible
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('email'))
        self.assertEqual(response.status_code, 200)

    # Tests to see if the correct template is being used
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('email'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personal/email_form.html')

# Tests for sending emails
from django.core import mail
class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail('Test Email', 'This is a test email.',
                       'potsdamautograder@gmail.com', ['malonejc200@potsdam.edu'],
                       fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test Email')
