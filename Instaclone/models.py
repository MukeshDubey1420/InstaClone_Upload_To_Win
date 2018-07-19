from django.db import models
import uuid
# Create your models here.
# class User(models.Model):
#     name = models.CharField(max_length=255)
#     phone = models.CharField(max_length=30)
#     age = models.IntegerField(default=0)
#     has_verified_mobile = models.BooleanField(default=False)
#     created_on = models.DateTimeField(auto_now_add=True)


class UserModel(models.Model):
	email = models.EmailField()
	name = models.CharField(max_length=120)
	username = models.CharField(max_length=120)
	password = models.CharField(max_length=40)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.name + " Has Username:-  " + str(self.username)


class SessionToken(models.Model):
	user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING,)
	session_token = models.CharField(max_length=255)
	created_on = models.DateTimeField(auto_now_add=True)
	is_valid = models.BooleanField(default=True)


	def create_token(self):
		self.session_token = uuid.uuid4()
	def __str__(self):
		return self.user.username + " Logged in at " + str(self.created_on)


class PostModel(models.Model):
	user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING,)
	image = models.FileField(upload_to='user_images')
	image_url = models.CharField(max_length=255)
	caption = models.CharField(max_length=240)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	has_liked = False

	@property
	def like_count(self):
		return len(LikeModel.objects.filter(post=self))

	@property
	def comments_count(self):
		return len(CommentModel.objects.filter(post=self))

	@property
	def comments(self):
		return CommentModel.objects.filter(post=self).order_by('-created_on')


	def __str__(self):
		return self.user.username + " Posted " + self.image_url


class LikeModel(models.Model):
	user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING,)
	post = models.ForeignKey(PostModel, on_delete=models.DO_NOTHING,)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username + " Liked " + str(self.post)


class CommentModel(models.Model):
	user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING,)
	post = models.ForeignKey(PostModel, on_delete=models.DO_NOTHING,)
	comment_text = models.CharField(max_length=555)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username + " Commented " + self.comment_text


class CategoryModel(models.Model):
		post = models.ForeignKey(PostModel, on_delete=models.DO_NOTHING,)
		category_text = models.CharField(max_length=200)
		def __str__(self):
			return self.user.username + " categoriesd " + self.category_text