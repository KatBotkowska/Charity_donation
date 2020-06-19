from django.test import TestCase
from charity.models import Category, Institution, Donation, InstitutionChoices


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='test_category')

    def test_get_object(self):
        test_category = Category.objects.all()
        self.assertEquals(len(test_category), 1)
        self.assertEquals('test_category', test_category[0].name)
        self.assertEquals(Category.objects.filter(name='test_category').count(), 1)

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 256)

    def test_object_str_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = f'{category.name}'
        self.assertEquals(expected_object_name, str(category))


class IstitutionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_category = Category.objects.create(name='test_category')
        Institution.objects.create(name='test_institution', description='institution for test purpose',
                                   categories=test_category)
