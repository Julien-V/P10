from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError


# Create your models here.
class Categorie(models.Model):
    category_name = models.TextField()


class Product(models.Model):
    product_name = models.TextField()
    brands = models.TextField(null=True)
    code = models.BigIntegerField()
    categories = models.TextField()
    nutrition_grades = models.CharField(max_length=1)
    stores = models.TextField(null=True)
    url = models.TextField()
    image_url = models.TextField()
    req100 = models.TextField()
    added_timestamp = models.BigIntegerField()
    updated_timestamp = models.BigIntegerField(null=True)

    def clean(self):
        # [var, type, null, (min_len, max_len)]
        requirements = {
            "product_name": [
                self.product_name, str, False,
                (0, None)],
            "brands": [
                self.brands, str, True,
                (0, None)],
            "code": [
                self.code, int, False,
                (0, None)],
            "categories": [
                self.categories, str, False,
                (0, None)],
            "nutrition_grades": [
                self.nutrition_grades, str, False,
                (0, 1)],
            "stores": [
                self.stores, str, True,
                (0, None)],
            "url": [
                self.url, str, False,
                (0, None)],
            "image_url": [
                self.image_url, str, False,
                (0, None)],
            "req100": [
                self.req100, str, False,
                (0, None)],
            "added_timestamp": [
                self.added_timestamp, int, False,
                (0, None)],
            "updated_timestamp": [
                self.updated_timestamp, int, True,
                (0, None)]
        }
        for key in requirements:
            r = requirements[key]
            value = r[0]
            typ = r[1]
            nullable = r[2]
            (minLen, maxLen) = r[3]
            # nullable
            if not nullable:
                # type
                if not isinstance(value, typ):
                    raise ValidationError(
                        f"'{key}' should be a {typ} not {type(value)}")
                if isinstance(value, int):
                    length = value
                else:
                    length = len(value)
                if maxLen is None:
                    # minLen without maxLen
                    if length <= minLen:
                        raise ValidationError(
                            f"'{key}': {value} should be > {minLen}")
                else:
                    # minLen and maxLen
                    if length <= minLen:
                        raise ValidationError(
                            f"'{key}': {value} should be > {minLen}")
                    elif length > maxLen:
                        raise ValidationError(
                            f"'{key}': {value} should be <= {maxLen}")


class Favorite(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    updated_timestamp = models.BigIntegerField()


class CategoriesProducts(models.Model):
    category = models.ForeignKey(
        Categorie, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)


class Translation(models.Model):
    tag = models.TextField(unique=True)
    fr_FR = models.TextField()
    en_GB = models.TextField(null=True)
