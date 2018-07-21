# from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


def upload_folder(instance, filename):
    return 'user/{0}/{1}'.format(instance.owner, filename)


class Comment(models.Model):
    postrelated = models.ForeignKey('DC.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.CharField(max_length=5000)
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("blog/post_list")

    def __str__(self):
        return self.text


class AvailClasses(models.Model):
    class_creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    className = models.TextField(max_length=200)
    # class_posts = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    # class_resources = models.ForeignKey(Resources, on_delete=models.CASCADE, blank=True, null=True)
    students = models.ManyToManyField(User, related_name="student", blank=True, null=True)

    def get_absolute_url(self):
        return u'/class/enrollclass/'

    def __str__(self):
        return self.className


class Enroll(models.Model):
    class_name = models.ForeignKey(AvailClasses, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    class_related = models.ForeignKey(AvailClasses, on_delete=models.CASCADE, blank=False, null=False,
                                      related_name="posts")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return u'/home/%d/' % self.class_related.id

    def __str__(self):
        return self.title


class Assignments(models.Model):
    title = models.CharField(max_length=256)
    due_date = models.DateTimeField()
    class_related = models.ForeignKey(AvailClasses, on_delete=models.CASCADE, blank=False, null=False,
                                      related_name="assignments")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return u'/home/%d/' % self.class_related.id


class AssignmentsHandedIn(models.Model):
    assignment = models.ForeignKey(Assignments, blank=False, null=False, on_delete=models.CASCADE, related_name="handin")
    hand_in_date = models.DateTimeField(auto_now_add=True)
    user_hand_in = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.assignment.title + '_' + self.user_hand_in.username

    def get_absolute_url(self):
        return '/files/newfile/{0}/{1}/'.format(self.assignment.class_related.id, self.id)


class Resources(models.Model):
    """Model definition for File."""
    # class_related = models.ForeignKey(AvailClasses, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_folder)
    shared_with = models.ManyToManyField(
        User, related_name='shared_with_me', blank=True)
    slug = models.SlugField(max_length=256, unique=True)
    file_type = models.CharField(max_length=20)
    name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(
        auto_now=True, blank=True, null=True, editable=True)
    class_related = models.ForeignKey(AvailClasses, on_delete=models.CASCADE, blank=False, null=False,
                                      related_name="resources")
    assignments = models.ForeignKey(AssignmentsHandedIn, on_delete=models.CASCADE, related_name="resource", blank=True,
                                    null=True)
    description = models.CharField(max_length=450, null=True, blank=True)

    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'

    def __str__(self):
        """Unicode representation of File."""
        return self.name

    def get_absolute_url(self):
        return u'/home/%d/' % self.class_related.id


class CustomUser(models.Model):
    type = (
        ('STD', 'Student'),
        ('TCH', 'Teacher')
    )
    type_field = models.CharField(max_length=3, verbose_name="Type", choices=type)
    profile_pic = models.ImageField(upload_to="profile_pics", default='static/download.jpg', blank=True)
    classes = models.ForeignKey(AvailClasses, on_delete=models.CASCADE, blank=True, null=True)
    link = models.OneToOneField(User, on_delete=models.CASCADE, related_name='link')  # extension of default user field
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    resources = models.ManyToManyField(Resources, related_name="cust_user_resource", blank=True)

    def __str__(self):
        return self.link.username

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
    # if created:
        # CustomUser.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
    # instance.profile.save()

# class Teacher(models.Model):
    # link = models.OneToOneField(User, on_delete=models.CASCADE)
    # link2class = models.ForeignKey(AvailClasses, on_delete=models.CASCADE)
    # posts = models.ForeignKey(Post, on_delete=models.CASCADE)

