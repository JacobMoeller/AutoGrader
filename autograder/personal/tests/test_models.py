from django.test import TestCase

# Create your tests here.
from personal.models import Courses, Invite, Assignment, Takes, Submission
from django.contrib.auth.models import User, Group


class InviteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user1 = User.objects(username='Ryan Murphy', password='password')
        Courses.objects.create(
            course_id=1, course_title='Software Engineering',
            instructor_username=test_user1)
        Invite.objects.create(
            invite_id=1, course_id=Courses.objects.get(course_id=1),
            sender_username='durhams199',
            rec_username='rwilliam122',
            level_of_invite='instructor')

    def test_sender_username_label(self):
        invite = Invite.objects.get(invite_id=1)
        field_label = invite._meta.get_field('sender_username').verbose_name
        self.assertEquals(field_label, 'sender username')

    def test_rec_username_label(self):
        invite = Invite.objects.get(invite_id=1)
        field_label = invite._meta.get_field('rec_username').verbose_name
        self.assertEquals(field_label, 'rec username')

    def test_level_of_invite_label(self):
        invite = Invite.objects.get(invite_id=1)
        field_label = invite._meta.get_field('level_of_invite').verbose_name
        self.assertEquals(field_label, 'level of invite')

    def test_sender_username_max_length(self):
        invite = Invite.objects.get(invite_id=1)
        max_length = invite._meta.get_field('sender_username').max_length
        self.assertEquals(max_length, 20)

    def test_rec_username_max_length(self):
        invite = Invite.objects.get(invite_id=1)
        max_length = invite._meta.get_field('rec_username').max_length
        self.assertEquals(max_length, 20)

    def test_level_of_invite_max_length(self):
        invite = Invite.objects.get(invite_id=1)
        max_length = invite._meta.get_field('level_of_invite').max_length
        self.assertEquals(max_length, 10)

    def test_course_id_references_class(self):
        invite = Invite.objects.get(invite_id=1)
        course_test = Courses.objects.get(course_id=1)
        self.assertEquals(invite.course_id, course_test)


class CoursesModelTest(TestCase):
    # Set up non-modified objects used by all test methods
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects(username='Ryan Murphy', password='password')
        Courses.objects.create(
            course_id=1, course_title='Software Engineering',
            instructor_username=test_user1)

    def test_course_title_label(self):
        course_test = Courses.objects.get(course_id=1)
        field_label = course_test._meta.get_field('course_title').verbose_name
        self.assertEquals(field_label, 'course title')

    def test_instructor_username_label(self):
        course_test = Courses.objects.get(course_id=1)
        field_label = course_test._meta.get_field(
            'instructor_username').verbose_name
        self.assertEquals(field_label, 'instructor username')

    def test_course_title_max_length(self):
        course = Courses.objects.get(course_id=1)
        max_length = course._meta.get_field('course_title').max_length
        self.assertEquals(max_length, 30)

    def test_instructor_username_max_length(self):
        course = Courses.objects.get(course_id=1)
        max_length = course._meta.get_field('instructor_username').max_length
        self.assertEquals(max_length, 20)


class AssignmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user1 = User.objects(username='Ryan Murphy', password='password')
        Courses.objects.create(
            course_id=1, course_title='Software Engineering',
            instructor_username=test_user1)
        Assignment.objects.create(
            assignment_id=1, course_id=Courses.objects.get(course_id=1),
            assignment_description="Finish your sprint for the week",
            acceptance_criteria='Fits your definition of done',
            testing_criteria='Run their tests')

    def test_assignment_description_label(self):
        assignment_test = Assignment.objects.get(assignment_id=1)
        field_label = assignment_test._meta.get_field(
            'assignment_description').verbose_name
        self.assertEquals(field_label, 'assignment description')

    def test_optional_notes_label(self):
        assignment_test = Assignment.objects.get(assignment_id=1)
        field_label = assignment_test._meta.get_field(
            'optional_notes').verbose_name
        self.assertEquals(field_label, 'optional notes')

    def test_acceptance_criteria_label(self):
        assignment_test = Assignment.objects.get(assignment_id=1)
        field_label = assignment_test._meta.get_field(
            'acceptance_criteria').verbose_name
        self.assertEquals(field_label, 'acceptance criteria')

    def test_testing_criteria_label(self):
        assignment_test = Assignment.objects.get(assignment_id=1)
        field_label = assignment_test._meta.get_field(
            'testing_criteria').verbose_name
        self.assertEquals(field_label, 'testing criteria')

    def test_assignment_description_max_length(self):
        assignment_test = Assignment.objects.get(assignment_id=1)
        max_length = assignment_test._meta.get_field(
            'assignment_description').max_length
        self.assertEquals(max_length, 200)

    def test_optional_notes_max_length(self):
        assignment_test = Assignment.objects.get(assignment_id=1)
        max_length = assignment_test._meta.get_field(
            'optional_notes').max_length
        self.assertEquals(max_length, 200)

    def test_acceptance_criteria_max_length(self):
        assignment_test = Assignment.objects.get(assignment_id=1)
        max_length = assignment_test._meta.get_field(
            'acceptance_criteria').max_length
        self.assertEquals(max_length, 200)

    def test_testing_criteria_max_length(self):
        assignment_test = Assignment.objects.get(assignment_id=1)
        max_length = assignment_test._meta.get_field(
            'testing_criteria').max_length
        self.assertEquals(max_length, 200)

    def test_course_id_references_class(self):
        assignment_test = Assignment.objects.get(assignment_id=1)
        course_test = Courses.objects.get(course_id=1)
        self.assertEquals(assignment_test.course_id, course_test)


class SubmissionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user1 = User.objects(username='Ryan Murphy', password='password')
        Courses.objects.create(
            course_id=1, course_title='Software Engineering',
            instructor_username=test_user1)
        Assignment.objects.create(
            assignment_id=1,
            course_id=Courses.objects.get(course_id=1))
        Submission.objects.create(
            submission_id=1,
            assignment_id=Assignment.objects.get(assignment_id=1),
            submitted_user='durhams199')

    def test_submitted_user_label(self):
        submission_test = Submission.objects.get(submission_id=1)
        field_label = submission_test._meta.get_field(
            'submitted_user').verbose_name
        self.assertEquals(field_label, 'submitted user')

    def test_submitted_user_max_length(self):
        submission_test = Submission.objects.get(submission_id=1)
        max_length = submission_test._meta.get_field(
            'submitted_user').max_length
        self.assertEquals(max_length, 20)


class TakesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Courses.objects.create(
            course_id=1,
            course_title='Software Engineering',
            instructor_username='Ryan Murphy')
        Takes.objects.create(
            student_username='matthewsr199',
            course_id=Courses.objects.get(course_id=1))

    def test_course_id_references_course(self):
        takes_test = Takes.objects.get(student_username='matthewsr199')
        test_user1 = User.objects(username='Ryan Murphy', password='password')
        Courses.objects.create(
            course_id=1, course_title='Software Engineering',
            instructor_username=test_user1)
        Takes.objects.create(
            takes_id=1,
            course_id=Courses.objects.get(course_id=1),
            student_username='matthewsr199')

    def test_course_id_references_course(self):
        takes_test = Takes.objects.get(takes_id=1)
        course_test = Courses.objects.get(course_id=1)
        self.assertEquals(takes_test.course_id, course_test)

    def test_student_username_max_length(self):
#        takes_test = Takes.objects.get(student_username = 'matthewsr199')
        takes_test = Takes.objects.get(takes_id=1)
        max_length = takes_test._meta.get_field('student_username').max_length
        self.assertEquals(max_length, 20)
