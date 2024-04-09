from django.shortcuts import render
from .models import Profile,Skill,About,Service,Project,Category,Blog
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
def home(request):
    profile = Profile.objects.last()
    skills = Skill.objects.order_by('order')
    about = About.objects.last()
    offers = Service.objects.order_by('order')

    projects = Project.objects.all()
    categories = Category.objects.all()
    blogs = Blog.objects.all()

    return render(request, 'index.html',
                   {'profile': profile, 
                    'skills': skills, 
                    'about':about, 
                    'offers':offers, 
                    'projects':projects,
                    'categories':categories,
                    'blogs': blogs
                    })

def project_detail(request,pk):
    project=get_object_or_404(Project, id=pk)
    return render(request, "portfolio-details.html",{'project':project})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, id = pk)
    blog.view_count += 1
    blog.save()
    return render(request, "single-blog.html",{'blog':blog,
                                               })

def about_me(request):
    about = About.objects.last()

    return render(request, 'about-us.html',
                   {
                    'about':about
                    })

def portfolio(request):
    projects = Project.objects.all()

    return render(request, 'portfolio.html',
                   {
                    'projects':projects
                    })

def blog(request):
    blogs = Blog.objects.all()
    popular_posts =Blog.objects.order_by('-view_count')[:4]

    if request.method == 'POST':
        search = request.POST.get('search')
        blogs = Blog.objects.filter(title__icontains = search)
        print(search)

    p = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    try:
        page_objects = p.get_page(page_number)
    except PageNotAnInteger:
        page_objects = p.page(1)
    except EmptyPage:
        page_objects =p.page(p.num_pages)
    return render(request, 'blog.html',
                   {
                    'blogs':page_objects,
                    'popular_posts':popular_posts
                    })
