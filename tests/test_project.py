from django.test import TestCase
from tuneldjango.apps.main.models import Project
from tuneldjango.apps.users.models import User, Group


class ProjectTestCase(TestCase):
    def setUp(self):
        """Do creation of models here"""
        user = User.objects.create(username="dinosaur")
        group = Group.objects.create(name="Dinosaur Group")
        Project.objects.create(
            name="Dinosaur Project",
            description="This is a project for dinosaurs",
            contact=user,
            group=group,
        )

    def test_projects(self):
        """Write tests for your project hers."""
        project = Project.objects.get(name="Dinosaur Project")
        self.assertEqual(project.get_label(), "project")
        self.assertEqual(project.contact.username, "dinosaur")
        self.assertEqual(project.group.uuid, "dinosaur-group")
