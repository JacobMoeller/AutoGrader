from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from personal.models import Courses, Takes


class InstructorHomePageViewTest(TestCase):
    fixtures = ['init_data.json', 'test_data_auth.json',
        'test_data.json', ]

    @classmethod
    def setUpTestData(cls):

        # Create two users
        cls.test_user1 = User.objects.create_user(
            username='testuser1',
            password='password')
        cls.test_user1.save()

        # Add test_user1 to Instructor group
        group = Group.objects.get(name="Instructor")
        group.user_set.add(cls.test_user1)

        # Add test_user2 to Student group
        cls.test_user2 = User.objects.create_user(
            username='testuser2',
            password='password')
        cls.test_user2.save()
        group = Group.objects.get(name="Student")
        group.user_set.add(cls.test_user2)

        # Create 2 courses
        cls.course1 = Courses.objects.create(
            course_title = f'CIS_201',
            course_number=201, id=111,
            course_crn=5454,
            instructor_username=cls.test_user1,
        )
        cls.course1.save()

        cls.course2 = Courses.objects.create(
            course_title = f'CIS_203',
            course_number=203, id=112,
            course_crn=5455,
            instructor_username=cls.test_user1,
        )
        cls.course2.save()

        cls.course3 = Courses.objects.create(
            course_title = f'CIS_405',
            course_number=405, id=113,
            course_crn=5456,
            instructor_username=cls.test_user2,
        )
        cls.course2.save()

    # Tests to see if correct template is used for course detail page
    def test_detail_view_template(self):
        login = self.client.force_login(self.test_user1)
        response = self.client.get(
            reverse('course_detail', kwargs={'pk': 111}), follow=True)
        self.assertTemplateUsed(response, 'personal/course_detail.html')
        self.assertEqual(response.status_code, 200)

    # Tests to see if 404 is thrown for course detail page
    def test_detail_404_template(self):
        login = self.client.login(username='testuser1', password='password')
        response = self.client.get(reverse(
            'course_detail', kwargs={'pk': 500}), follow=True)
        self.assertTemplateUsed(response, '404.html')
        self.assertEqual(response.status_code, 404)

    # Tests to see if student can see course-detail page if in course
    def test_detail_student_allowed_template(self):
        login = self.client.force_login(self.test_user2)
        # Add student to CIS 201 (id: 111)
        Takes.objects.create(
            course_id=self.course1,
            student_username=self.test_user2,
            is_grader_in_course=False
        ).save()
        self.assertTrue(self.test_user2==Takes.objects.get(
            course_id=self.course1).student_username)
        response = self.client.get(reverse(
            'course_detail', kwargs={'pk': self.course1.id}), follow=True)
        self.assertTemplateUsed(response, 'personal/course_detail.html')
        self.assertEqual(response.status_code, 200)

    # Tests to see if permission denied for course-detail page if not in course
    def test_detail_permission_denied_template(self):
        login = self.client.force_login(self.test_user2)
        with self.assertRaises(Takes.DoesNotExist):
            Takes.objects.get(course_id=self.course2,
            student_username=self.test_user2)
        response = self.client.get(reverse(
            'course_detail', kwargs={'pk': self.course2.id}), follow=True)
        self.assertTemplateUsed(response, '403.html')
        self.assertEqual(response.status_code, 403)

    # Tests to see if permission allowed for course if current instructor
    def test_detail_permission_allowed_course_pages(self):
        # testuser1 is instructor of id=111 but not 113
        login = self.client.force_login(self.test_user1)
        self.assertTrue(self.test_user1 == self.course1.instructor_username)
        response = self.client.get(reverse(
            'course_detail', kwargs={'pk': self.course1.id}), follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse(
            'course_update', kwargs={'pk': self.course1.id}), follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse(
            'course_delete', kwargs={'pk': self.course1.id}), follow=True)
        self.assertEqual(response.status_code, 200)

    # Tests to see if permission denied for course if not current instructor
    def test_detail_permission_denied_course_pages(self):
        # testuser1 is instructor of id=111 but not 113
        login = self.client.force_login(self.test_user1)

        self.assertTrue(self.test_user1 != self.course3.instructor_username)
        response = self.client.get(reverse(
            'course_detail', kwargs={'pk': self.course3.id}), follow=True)
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse(
            'course_update', kwargs={'pk': self.course3.id}), follow=True)
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse(
            'course_delete', kwargs={'pk': self.course3.id}), follow=True)
        self.assertEqual(response.status_code, 403)

    # Test the create course form.
    def test_create_course_form(self):
        self.client.force_login(self.test_user1)
        response = self.client.post(
            reverse('course_create'),
            {
                'course_crn': 66666,
                'course_title': 'Bread Making',
                'course_number': 469,
                'instructor_username': self.test_user1
            }, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('homepage'), follow=True)
        self.assertContains(response, "Bread Making")
        self.assertTrue(Courses.objects.get(course_number="469"))

    # Test the delete course form through the course_delete page.
    def test_delete_course_form(self):
        self.client.force_login(self.test_user1)
        response = self.client.post(
            reverse('course_delete', kwargs={
                'pk': self.course1.id,
                }), follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('homepage'), follow=True)
        self.assertNotContains(response, self.course1.course_title)
        with self.assertRaises(Courses.DoesNotExist):
            Courses.objects.get(course_number=self.course1.course_number)

    # Test the edit course form through the course_update page.
    def test_edit_course_form(self):
        self.client.force_login(self.test_user1)
        response = self.client.post(
            reverse('course_update', kwargs={'pk': self.course1.id}), {
                    'course_title': 'Bread Making',
                    'course_number': 469,
                    'course_crn': 7399,
                }, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('homepage'), follow=True)
        self.assertContains(response, 'Bread Making')
        self.assertNotContains(response, 'CIS_201')
