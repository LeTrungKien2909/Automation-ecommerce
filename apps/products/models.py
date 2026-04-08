from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Tên danh mục')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name='Mô tả')
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='Hình ảnh')
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=300, verbose_name='Tên sản phẩm')
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name='Danh mục'
    )
    description = models.TextField(verbose_name='Mô tả')
    specifications = models.TextField(blank=True, verbose_name='Thông số kỹ thuật')
    price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='Giá')
    discount_price = models.DecimalField(
        max_digits=15, decimal_places=0, null=True, blank=True, verbose_name='Giá khuyến mãi'
    )
    stock = models.PositiveIntegerField(default=0, verbose_name='Tồn kho')
    main_image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Hình ảnh chính')
    is_active = models.BooleanField(default=True, verbose_name='Đang bán')
    is_featured = models.BooleanField(default=False, verbose_name='Nổi bật')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0

    class Meta:
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'
        ordering = ['-created_at']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', verbose_name='Hình ảnh')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='Mô tả hình')

    def __str__(self):
        return f'Image for {self.product.name}'

    class Meta:
        verbose_name = 'Hình ảnh sản phẩm'


class ProductReview(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Người dùng')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Đánh giá')
    comment = models.TextField(verbose_name='Nhận xét')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.name}'

    class Meta:
        verbose_name = 'Đánh giá sản phẩm'
        verbose_name_plural = 'Đánh giá sản phẩm'
        unique_together = ['product', 'user']
