from datetime import date


from django.db.models import IntegerField, CharField, DateField, TimeField, BooleanField

from django.test import TestCase
from django.contrib.auth.models import User
from charity.models import Category, Institution, Donation


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
        category = Category.objects.first()
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        category = Category.objects.first()
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 256)

    def test_object_str_name(self):
        category = Category.objects.first()
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
        institution = Institution.objects.first()
        field_label = institution._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Nazwa')

    def test_name_max_length(self):
        institution = Institution.objects.first()
        max_length = institution._meta.get_field('name').max_length
        self.assertEquals(max_length, 256)

    def test_object_str_name(self):
        institution = Institution.objects.first()
        expected_object_name = f'{institution.name}'
        self.assertEquals(expected_object_name, str(institution))

    def test_description_label(self):
        institution = Institution.objects.first()
        field_label = institution._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Opis działalnosci')

    def test_description_max_length(self):
        institution = Institution.objects.first()
        max_length = institution._meta.get_field('description').max_length
        self.assertEquals(max_length, 516)

    def test_type_label(self):
        institution = Institution.objects.first()
        field_label = institution._meta.get_field('type').verbose_name
        self.assertEquals(field_label, 'typ')

    def test_type_max_length(self):
        institution = Institution.objects.first()
        max_length = institution._meta.get_field('type').max_length
        self.assertEquals(max_length, 20)

    def test_type_default(self):
        institution = Institution.objects.first()
        institution_type = institution.type
        self.assertEquals(institution_type, 'Fundacja')

    def test_categories_label(self):
        institution = Institution.objects.first()
        field_label = institution._meta.get_field('categories').verbose_name
        self.assertEquals(field_label, 'Kategorie darów')

    def test_institution_categories_fields(self):
        institution = Institution.objects.first()
        categories = institution.categories.all()
        test_category_1 = Category.objects.get(name='test_category_1')
        test_category_2 = Category.objects.get(name='test_category_2')
        self.assertEquals(categories[0], test_category_1)
        self.assertEquals(categories[1], test_category_2)
        self.assertEquals(institution.categories.get(pk=test_category_1.pk), test_category_1)
        self.assertEquals(institution.categories.get(pk=test_category_2.pk), test_category_2)
        self.assertQuerysetEqual(categories, [repr(test_category_1), repr(test_category_2)], ordered=False)

    def test_institution_get_categories(self):
        institution = Institution.objects.first()
        get_categories = institution.get_categories()
        self.assertEquals(get_categories, ", ".join([c.name for c in institution.categories.all()]))

    def test_institution_label(self):
        institution = Institution.objects.first()
        model_label = institution._meta.verbose_name
        self.assertEquals(model_label, 'Instytucja')

    def test_institutions_label(self):
        institution = Institution.objects.first()
        model_label_plural = institution._meta.verbose_name_plural
        self.assertEquals(model_label_plural, 'Instytucje')


class DonationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_category_1 = Category.objects.create(name='test_category_1')
        test_category_2 = Category.objects.create(name='test_category_2')
        institution = Institution.objects.create(name='test_institution', description='institution for test purpose')
        institution.categories.add(test_category_1, test_category_2)
        user = User.objects.create(first_name='user', last_name='user', username='user', email='user@email.com',
                                   password='top_secret')
        donation = Donation.objects.create(quantity=1, address='test_address', phone_number='1111', city='test_city',
                                           zip_code='11-000', pick_up_date='2020-06-22', pick_up_time='00:00',
                                           pick_up_comment='test_comment',
                                           user=user, institution=institution)
        donation.categories.add(test_category_1, test_category_2)

    def test_get_object(self):
        donation = Donation.objects.all()
        self.assertEquals(len(donation), 1)
        self.assertEquals(Donation.objects.filter(institution__name='test_institution').count(), 1)
        user = User.objects.first()
        self.assertEquals(Donation.objects.filter(user=user).count(), 1)

    def test_object_str_name(self):
        donation = Donation.objects.first()
        expected_object_name = f'{donation.institution}'
        self.assertEquals(expected_object_name, str(donation))

    def test_quantity_label(self):
        donation = Donation.objects.first()
        field_label = donation._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'Ilość')

    def test_quantity_instance(self):
        field = Donation._meta.get_field('quantity')
        self.assertTrue(isinstance(field, IntegerField))

    def test_categories_label(self):
        donation = Donation.objects.first()
        field_label = donation._meta.get_field('categories').verbose_name
        self.assertEquals(field_label, 'Kategorie darów')

    def test_donation_get_categories(self):
        donation = Donation.objects.first()
        get_categories = donation.get_categories()
        self.assertEquals(get_categories, ", ".join([c.name for c in donation.categories.all()]))

    def test_donation_categories_fields(self):
        donation = Donation.objects.first()
        categories = donation.categories.all()
        test_category_1 = Category.objects.get(name='test_category_1')
        test_category_2 = Category.objects.get(name='test_category_2')
        self.assertEquals(categories[0], test_category_1)
        self.assertEquals(categories[1], test_category_2)
        self.assertEquals(donation.categories.get(pk=test_category_1.pk), test_category_1)
        self.assertEquals(donation.categories.get(pk=test_category_2.pk), test_category_2)
        self.assertQuerysetEqual(categories, [repr(test_category_1), repr(test_category_2)], ordered=False)

    def test_institution_label(self):
        donation = Donation.objects.first()
        field_label = donation._meta.get_field('institution').verbose_name
        self.assertEquals(field_label, 'Instytucja')

    def test_institution_object(self):
        donation = Donation.objects.first()
        institution = Institution.objects.get(name='test_institution')
        self.assertEquals(donation.institution, institution)

    def test_address_label(self):
        donation = Donation.objects.first()
        field_label = donation._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'Adres')

    def test_address_instance(self):
        field = Donation._meta.get_field('address')
        self.assertTrue(isinstance(field, CharField))

    def test_address_max_length(self):
        donation = Donation.objects.first()
        max_length = donation._meta.get_field('address').max_length
        self.assertEquals(max_length, 256)

    def test_phone_number_label(self):
        donation = Donation.objects.first()
        field_label = donation._meta.get_field('phone_number').verbose_name
        self.assertEquals(field_label, 'Numer telefonu')

    def test_phone_number_instance(self):
        field = Donation._meta.get_field('phone_number')
        self.assertTrue(isinstance(field, CharField))

    def test_phone_number_max_length(self):
        donation = Donation.objects.first()
        max_length = donation._meta.get_field('phone_number').max_length
        self.assertEquals(max_length, 12)

    def test_city_label(self):
        donation = Donation.objects.first()
        field_label = donation._meta.get_field('city').verbose_name
        self.assertEquals(field_label, 'Miasto')

    def test_city_instance(self):
        field = Donation._meta.get_field('city')
        self.assertTrue(isinstance(field, CharField))

    def test_city_max_length(self):
        donation = Donation.objects.first()
        max_length = donation._meta.get_field('city').max_length
        self.assertEquals(max_length, 126)

    def test_zip_code_label(self):
        donation = Donation.objects.first()
        field_label = donation._meta.get_field('zip_code').verbose_name
        self.assertEquals(field_label, 'Kod pocztowy')

    def test_zip_code_instance(self):
        field = Donation._meta.get_field('zip_code')
        self.assertTrue(isinstance(field, CharField))

    def test_zip_code_max_length(self):
        donation = Donation.objects.first()
        max_length = donation._meta.get_field('zip_code').max_length
        self.assertEquals(max_length, 6)

    def test_pick_up_date_label(self):
        donation = Donation.objects.first()
        field_label = donation._meta.get_field('pick_up_date').verbose_name
        self.assertEquals(field_label, 'Data odbioru')

    def test_pick_up_date_instance(self):
        field = Donation._meta.get_field('pick_up_date')
        self.assertTrue(isinstance(field, DateField))

    def test_pick_up_time_label(self):
        donation = Donation.objects.first()
        field_label = donation._meta.get_field('pick_up_time').verbose_name
        self.assertEquals(field_label, 'Godzina odbioru')

    def test_pick_up_time_instance(self):
        field = Donation._meta.get_field('pick_up_time')
        self.assertTrue(isinstance(field, TimeField))

    def test_pick_up_comment_label(self):
        donation = Donation.objects.first()
        field_label = donation._meta.get_field('pick_up_comment').verbose_name
        self.assertEquals(field_label, 'Dodatkowe informacje')

    def test_pick_up_comment_instance(self):
        field = Donation._meta.get_field('pick_up_comment')
        self.assertTrue(isinstance(field, CharField))

    def test_pick_up_comment_max_length(self):
        donation = Donation.objects.first()
        max_length = donation._meta.get_field('pick_up_comment').max_length
        self.assertEquals(max_length, 256)

    def test_user_label(self):
        donation = Donation.objects.first()
        field_label = donation._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Użytkownik')

    def test_user_object(self):
        donation = Donation.objects.first()
        user = User.objects.get(username='user')
        self.assertEquals(donation.user, user)

    def test_status_label(self):
        donation = Donation.objects.first()
        field_label = donation._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'Czy dary odebrane?')

    def test_status_instance(self):
        field = Donation._meta.get_field('status')
        self.assertTrue(isinstance(field, BooleanField))

    def test_status_default(self):
        donation = Donation.objects.get(id=1)
        donation_status = donation.status
        self.assertEquals(donation_status, False)

    def test_update_date_label(self):
        donation = Donation.objects.get(id=1)
        field_label = donation._meta.get_field('update_date').verbose_name
        self.assertEquals(field_label, 'Data aktualizacji statusu')

    def test_update_date_instance(self):
        field = Donation._meta.get_field('update_date')
        self.assertTrue(isinstance(field, DateField))

    def test_update_date_default(self):
        donation = Donation.objects.first()
        donation_update_date = donation.update_date
        self.assertEquals(donation_update_date, date.today())

    def test_donation_label(self):
        donation = Donation.objects.first()
        model_label = donation._meta.verbose_name
        self.assertEquals(model_label, 'Dary')

    def test_donations_label(self):
        donation = Donation.objects.first()
        model_label_plural = donation._meta.verbose_name_plural
        self.assertEquals(model_label_plural, 'Dary')


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(first_name='user', last_name='user', username='user', email='user@email.com',
                                   password='top_secret')

    def test_get_object(self):
        test_user = User.objects.all()
        self.assertEquals(len(test_user), 1)
        self.assertEquals('user', test_user[0].username)
        self.assertEquals(User.objects.filter(username='user').count(), 1)