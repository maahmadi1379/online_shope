from typing import Dict

from django.db.models import QuerySet

from apps.users.models import User
from apps.shopping.models import Review, Product


class ReviewService:
    @classmethod
    def add(cls, user_obj: User, product_obj: Product, rating: int, description: str) -> Review:
        review_obj = Review.objects.create(
            user=user_obj,
            product=product_obj,
            rating=rating,
            description=description,
        )

        return review_obj

    @classmethod
    def list(cls, parameters: Dict = None) -> QuerySet[Review]:
        if parameters is None:
            parameters = {}

        reviews_objs = Review.objects.filter(**parameters).order_by('-created')

        return reviews_objs
