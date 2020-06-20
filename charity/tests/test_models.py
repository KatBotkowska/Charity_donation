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


class InstitutionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_category_1 = Category.objects.create(name='test_category_1')
        test_category_2 = Category.objects.create(name='test_category_2')
        institution = Institution.objects.create(name='test_institution', description='institution for test purpose')
        institution.categories.add(test_category_1, test_category_2)


    def test_get_object(self):
        institution = Institution.objects.all()
        self.assertEquals(len(institution), 1)
        self.assertEquals('test_institution', institution[0].name)
        self.assertEquals(Institution.objects.filter(name='test_institution').count(), 1)

    def test_name_label(self):
        institution = Institution.objects.get(id=1)
        field_label = institution._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Nazwa')

    def test_name_max_length(self):
        institution = Institution.objects.get(id=1)
        max_length = institution._meta.get_field('name').max_length
        self.assertEquals(max_length, 256)

    def test_object_str_name(self):
        institution = Institution.objects.get(id=1)
        expected_object_name = f'{institution.name}'
        self.assertEquals(expected_object_name, str(institution))

    def test_description_label(self):
        institution = Institution.objects.get(id=1)
        field_label = institution._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Opis działalnosci')

    def test_description_max_length(self):
        institution = Institution.objects.get(id=1)
        max_length = institution._meta.get_field('description').max_length
        self.assertEquals(max_length, 516)

    def test_type_label(self):
        institution = Institution.objects.get(id=1)
        field_label = institution._meta.get_field('type').verbose_name
        self.assertEquals(field_label, 'typ')

    def test_type_max_length(self):
        institution = Institution.objects.get(id=1)
        max_length = institution._meta.get_field('type').max_length
        self.assertEquals(max_length, 20)

    def test_type_default(self):
        institution = Institution.objects.get(id=1)
        institution_type = institution.type
        self.assertEquals(institution_type, 'Fundacja')

    def test_categories_label(self):
        institution = Institution.objects.get(id=1)
        field_label = institution._meta.get_field('categories').verbose_name
        self.assertEquals(field_label, 'Kategorie darów')

    def test_institution_categories_fields(self):
        institution = Institution.objects.get(id=1)
        categories = institution.categories.all()
        test_category_1 = Category.objects.get(name='test_category_1')
        test_category_2 = Category.objects.get(name='test_category_2')
        self.assertEquals(categories[0], test_category_1)
        self.assertEquals(categories[1], test_category_2)
        self.assertEquals(institution.categories.get(pk=test_category_1.pk), test_category_1)
        self.assertEquals(institution.categories.get(pk=test_category_2.pk), test_category_2)
        self.assertQuerysetEqual(categories, [repr(test_category_1), repr(test_category_2)], ordered=False)

    def test_institution_get_categories(self):
        institution = Institution.objects.get(id=1)
        get_categories = institution.get_categories()
        self.assertEquals(get_categories, ", ".join([c.name for c in institution.categories.all()]))

    def test_institution_label(self):
        institution = Institution.objects.get(id=1)
        model_label = institution._meta.verbose_name
        self.assertEquals(model_label, 'Instytucja')

    def test_institutions_label(self):
        institution = Institution.objects.get(id=1)
        model_label_plural = institution._meta.verbose_name_plural
        self.assertEquals(model_label_plural, 'Instytucje')

