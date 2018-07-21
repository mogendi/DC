# from django.db.models.signals import post_save
import os
from django.conf import settings
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, LogoutView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post, CustomUser, AvailClasses, Resources, Assignments, AssignmentsHandedIn
from django.shortcuts import Http404, render, redirect
from django.template import loader
from .forms import UserForm, CustomUserForm, PostForm, ClassForm, ResourceForm, AssignmentForm, HandInForm
from django.template.defaultfilters import slugify
from django_ajax.decorators import ajax


class Logout(LogoutView):
    next_page = "/DC/signup.html"


class PasswordReset(PasswordResetView):
    template_name = "admin/registration/password_reset_form.html"


class Landing(generic.TemplateView):
    template_name = "DC/landing.html"


@ajax
def detail(request, post_id):
    author = False
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404("Post doesn't exist")
    if post.author.id == request.user.id:
        author = True
    return render(request, 'DC/detail.html', {'post': post, 'author': author})


@ajax
def resource_detail(request, slug):
    owner = False
    try:
        rscs = Resources.objects.get(slug=slug)
    except Resources.DoesNotExist:
        raise Http404("Resource does not exist")
    if rscs.owner.id == request.user.id:
        owner = True
    return render(request, 'DC/resouce_details.html', {'rscs': rscs, 'owner': owner})


@login_required
def home(request):
    user_classes = AvailClasses.objects.filter(students=request.user.id)
    user_posts_default = Post.objects.filter(author=request.user)
    user_resources_default = Resources.objects.filter(owner=request.user)
    loaded = True
    context = {
        'user_resources_default': user_resources_default,
        'user_posts_default': user_posts_default,
        'user_classes': user_classes,
        'loaded': loaded,
    }
    return render(request, 'DC/experiment.html', context)


@login_required
def home_in_context(request, class_id):
    creator = False
    current_class = AvailClasses.objects.get(pk=class_id)
    user_classes = AvailClasses.objects.filter(students=request.user.id)
    assignments = Assignments.objects.filter(class_related=current_class)
    template = loader.get_template('DC/experiment.html')
    if current_class.class_creator.id == request.user.id:
        creator = True
    if request.GET.get('search'):
        result_resources = Resources.objects.filter(name__contains=request.GET.get('search')) \
            .filter(class_related=class_id)
        result_posts = Post.objects.filter(title__contains=request.GET.get('search')).filter(class_related=class_id)
        assignments = Assignments.objects.filter(title__contains=request.GET.get('search')).filter(class_related=class_id)
        context = {
            'creator': creator,
            'current_class': current_class,
            'result_resources': result_resources,
            'result_posts': result_posts,
            'class_id': class_id,
            'user_classes': user_classes,
            'assignments': assignments
        }
    else:
        class_posts = Post.objects.filter(class_related=current_class)
        class_resources = Resources.objects.filter(class_related=current_class)
        context = {
            'current_class': current_class,
            'class_resources': class_resources,
            'class_id': class_id,
            'user_classes': user_classes,
            'class_posts': class_posts,
            'creator': creator,
            'assignments': assignments
        }
    return HttpResponse(template.render(context, request))


@ajax
@login_required
def parallel_home(request, class_id):
    creator = False
    current_class = AvailClasses.objects.get(pk=class_id)
    users_enrolled = current_class.students.all().count()
    user_classes = AvailClasses.objects.filter(students=request.user.id)
    if current_class.class_creator.id == request.user.id:
        creator = True
    if request.GET.get('search'):
        result_resources = Resources.objects.filter(name__contains=request.GET.get('search')) \
            .filter(class_related=class_id)
        result_posts = Post.objects.filter(title__contains=request.GET.get('search')).filter(class_related=class_id)
        context = {
            'creator': creator,
            'current_class': current_class,
            'result_resources': result_resources,
            'result_posts': result_posts,
            'class_id': class_id,
            'user_classes': user_classes,
            'users_enrolled': users_enrolled
        }
    else:
        class_posts = Post.objects.filter(class_related=current_class)
        class_resources = Resources.objects.filter(class_related=current_class)
        context = {
            'current_class': current_class,
            'class_resources': class_resources,
            'class_id': class_id,
            'user_classes': user_classes,
            'class_posts': class_posts,
            'creator': creator,
            'users_enrolled': users_enrolled
        }
    return render(request, 'DC/detail.html', context)


@login_required
def class_details(request, class_id):
    creator = False
    current_class = AvailClasses.objects.get(pk=class_id)
    users_enrolled = current_class.students.all().count()
    user_classes = AvailClasses.objects.filter(students=request.user.id)
    assignments = Assignments.objects.filter(class_related=current_class)
    if current_class.class_creator.id == request.user.id:
        creator = True
    if request.GET.get('search'):
        result_resources = Resources.objects.filter(name__contains=request.GET.get('search')) \
            .filter(class_related=class_id)
        result_posts = Post.objects.filter(title__contains=request.GET.get('search')).filter(class_related=class_id)
        context = {
            'creator': creator,
            'current_class': current_class,
            'result_resources': result_resources,
            'result_posts': result_posts,
            'class_id': class_id,
            'user_classes': user_classes,
            'users_enrolled': users_enrolled
        }
    else:
        class_posts = Post.objects.filter(class_related=current_class)
        class_resources = Resources.objects.filter(class_related=current_class)
        context = {
            'current_class': current_class,
            'class_resources': class_resources,
            'class_id': class_id,
            'user_classes': user_classes,
            'class_posts': class_posts,
            'creator': creator,
            'users_enrolled': users_enrolled,
            'assignments': assignments
        }
    return render(request, 'DC/home.html', context)


@ajax
@login_required
def home_body(request, view_id, class_id):
    current_class = AvailClasses.objects.get(pk=class_id)
    users_enrolled = current_class.students.all().count()
    class_posts = Post.objects.filter(class_related=class_id).count()
    class_resources = Resources.objects.filter(class_related=class_id).count()
    if view_id == 1:
        context = {
            'class_posts': class_posts,
            'class_resources': class_resources,
        }
    if view_id == 2:
        context = {
            'users_enrolled': users_enrolled,
        }
    return render(request, 'DC/landing.html', context)


@ajax
@login_required
def def_user(request):
    current_user = request.user
    user_posts = Post.objects.filter(author=current_user)
    user_files = Resources.objects.filter(owner=current_user)
    user_classes = AvailClasses.objects.filter(students=current_user.id)
    ass_handed_in = AssignmentsHandedIn.objects.filter(user_hand_in=current_user)
    user_posts_no = user_posts.count()
    user_files_no = user_files.count()
    user_classes_no = user_classes.count()
    context = {
        'user_posts': user_posts,
        'user_files': user_files,
        'user_classes': user_classes,
        'ass_handed_in': ass_handed_in,
        'user_posts_no': user_posts_no,
        'user_files_no': user_files_no,
        'user_classes_no': user_classes_no
    }
    return render(request, 'DC/userinfo.html', context)


class ResourceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Resources
    form_class = ResourceForm
    login_url = '/login/'
    template_name = 'DC/new_file.html'

    def file_type(self, name):
        types = {"image": ['jpg', 'gif', 'jpeg', 'png', 'tiff', 'bmp'],
                 "video": ['webm', 'mpeg4', '3gpp', 'mov', 'avi', 'mpegps', 'wmv', 'flv'],
                 "document": ['doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt', 'pdf'],
                 "code": ['c', 'cpp', 'py', 'java', 'html', 'css']}
        extension = name.split(".")[1].lower()
        for key in types:
            if extension in types[key]:
                return key

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.name = self.request.FILES['file'].name
        class_relate = AvailClasses.objects.get(pk=self.kwargs['class_id'])
        form.instance.class_related = class_relate
        form.instance.slug = slugify(form.instance.name)
        form.instance.file_type = self.file_type(form.instance.name)
        if self.kwargs['ass_id']>0:
            form.instance.assignments = AssignmentsHandedIn.objects.get(pk=self.kwargs['ass_id'])
        else:
            pass
        return super().form_valid(form)


class FileView(LoginRequiredMixin, generic.DetailView):
    model = Resources
    login_url = '/login/'
    form_class = ResourceForm
    template_name = 'DC/resource_details'


class ResourceListView(LoginRequiredMixin, generic.ListView):
    model = Resources
    login_url = '/login/'
    template_name = 'DC/userinfo'


class AssignmentListView(LoginRequiredMixin, generic.ListView):
    model = Assignments
    login_url = '/login/'
    template_name = 'DC/userinfo'


def create_user(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        user_profile = CustomUserForm(data=request.POST)

        if user_form.is_valid() and user_profile.is_valid():
            user = user_form.save()
            user.set_password(user.password)  # Hashing the password
            user.save()
            profile = user_profile.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
            return redirect('/login')
        else:
            print(user_form.errors, user_profile.errors)
    else:
        user_form = UserForm()
        user_profile = CustomUserForm()

    return render(request, 'registration/signup.html', {'user_form': user_form,
                                                        'user_profile': user_profile,
                                                        'registered': registered})


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = '/login/'
    redirect_field_name = '/DC/detail.html'
    form_class = PostForm
    model = Post
    template_name = "DC/new_post.html"

    def form_valid(self, form):
        class_id = self.kwargs['class_id']
        class_inst = AvailClasses.objects.get(pk=class_id)
        form.instance.author = self.request.user
        form.instance.class_related = class_inst
        return super().form_valid(form)

   # def post_valid(self, form):
    #    if form.is_valid():
     #      if self.request.user.link.type_field == 'STD':
      #          post = form.save(commit=False)
       #         post.save()
        #        return redirect("/DC/home.html")


class ClassCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = '/login/'
    model = AvailClasses
    form_class = ClassForm
    template_name = "DC/create_class.html"

    def form_valid(self, form):
        form.instance.class_creator = self.request.user
        return super().form_valid(form)


class ClassEnrollView(LoginRequiredMixin, generic.TemplateView):
    login_url = '/login/'
    template_name = "DC/enroll.html"

    def post(self, form):
        chosen_class = AvailClasses.objects.get(className=form.POST.get('chosen'))
        chosen_class.students.add(self.request.user)
        return redirect("/home/{}".format(chosen_class.id))


class AssignmentCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = '/login/'
    model = Assignments
    form_class = AssignmentForm
    template_name = "DC/new_assignment.html"

    def form_valid(self, form):
        class_id = self.kwargs['class_id']
        form.instance.class_related = AvailClasses.objects.get(pk=class_id)
        return super().form_valid(form)


class AssignmentHandIn(LoginRequiredMixin, generic.CreateView):
    model = AssignmentsHandedIn
    form_class = HandInForm
    login_url = 'login'
    template_name = "DC/handin.html"

    def form_valid(self, form):
        form.instance.user_hand_in = self.request.user
        return super().form_valid(form)


@ajax
@login_required
def class_list(request, class_id):
    current_class = AvailClasses.objects.get(pk=class_id)
    std_list = current_class.students.all()
    user_posts_no = Post.objects.filter(author=request.user).count()
    user_files_no = Resources.objects.filter(owner=request.user).count()
    user_classes_no = AvailClasses.objects.filter(students=request.user).count()
    context = {
        "std_list": std_list,
        'user_posts_no': user_posts_no,
        'user_files_no': user_files_no,
        'user_classes_no': user_classes_no
    }
    return render(request, "DC/resouce_details.html", context)


@login_required
def delete_post(request, post_id):
    post_context = Post.objects.get(pk=post_id)
    class_rel = post_context.class_related
    post_context.delete()
    return redirect('/home/%d' % class_rel.id)


@login_required
def delete_resource(request, slug):
    resources = Resources.objects.get(slug=slug)
    class_rel = resources.class_related
    resources.delete()
    return redirect('/home/%d' % class_rel.id)


@login_required
def delete_class(request, class_id):
    class_inst = Resources.objects.get(pk=class_id)
    class_inst.delete()
    return redirect('/home/')


@login_required
def delete_resource(request, slug):
    resource = Resources.objects.get(slug=slug)
    class_rel = resource.class_related
    resource.delete()
    return redirect('/home/%d' % class_rel.id)


@login_required
def middle(request):
    return render(request, "DC/middle.html", context={})


@ajax
def all_classes(request):
    return render(request, "DC/classes.html", context={'classes': AvailClasses.objects.all()})
