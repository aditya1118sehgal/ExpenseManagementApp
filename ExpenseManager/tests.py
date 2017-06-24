from django.test import TestCase
from django.contrib.auth.models import User
from ExpenseManager.models import Expense, Profile

class ProfileModelTest(TestCase):
    def setUp(self):
        self.userA = User.objects.create_user(username='testuserA', password='12345')
        self.userR = User.objects.create_user(username='testuserR', password='12345')
        self.roleA = 'A'
        self.roleR = 'R'
        self.profileA = Profile(user=self.userA, role=self.roleA)
        self.profileR = Profile(user=self.userR, role=self.roleR)

    def test_user(self):
        self.assertEqual(self.userA, self.profileA.user)
        self.assertEqual(self.userR, self.profileR.user)

    def test_role(self):
        self.assertEqual(self.profileA.role, self.roleA)
        self.assertEqual(self.profileR.role, self.roleR)

    def test_admin(self):
        self.assertFalse(self.profileR.is_admin())
        self.assertTrue(self.profileA.is_admin())
        notAdminRole = 'X'
        self.assertFalse((Profile(self.userA, notAdminRole).is_admin()))


class ExpenseModelTest(TestCase):
    def setUp(self):
        self.amount = 21.49
        self.text = 'some text'
        self.title = 'test expense'
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.expense = Expense(author=self.user, title=self.title, text=self.text, amount=self.amount)

    def test_stringRepresentation(self):
        self.assertEqual(str(self.expense), self.expense.title)

    def test_amount(self):
        self.assertEqual(self.amount, self.expense.amount)

    def test_user(self):
        self.assertEqual(self.user, self.expense.author)

    def test_text(self):
        self.assertEqual(self.text, self.expense.text)

    def test_title(self):
        self.assertEqual(self.title, self.expense.title)

    def test_created_date(self):
        self.assertFalse(self.expense.created_date is None)
