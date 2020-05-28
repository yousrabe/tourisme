from django.shortcuts import render, redirect , get_object_or_404, redirect
from art.forms import RegisterForm, RegisterFormUpdate, AddAddress, LoginForm, IssuesForm
from django.contrib.auth import authenticate, login, logout
from art.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

@csrf_exempt
def savePanier(request):
    i = 0
    print(request.user.username)
    if not request.user.username:
        return redirect('art:error')
    user = User.objects.get(id=request.user.id)
    d = request.POST
    di = []
    for key, value in d.items():
        temp = [key,value]
        di.append(temp)
        q = 0 
        c = CartLine()
        print(key)
        if key.startswith('quantity_'):
            q = value
        if key.startswith('item_name_'):
            i += 1
            #c.client = Client.objects.get(user=user)
            c.client = Client.objects.get(user=user)
            c.product  = Product.objects.get(name=value)
            c.quantity = d['quantity_'+ key[-1]]
            c.save()
    return redirect('art:index')

def facture(request):
    u = request.user
    print(u.id)
    user = User.objects.get(id=u.id)

    idd = Client.objects.get(id=u.id-1)

    list_commande = CartLine.objects.filter(client=idd)

    return render(request, 'facture.html' , {'lc' : list_commande})


def index(request):
    # statistique
    data = json.load(open("data.json"))
    data["nb"] = data["nb"] + 1
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
        
    products = Product.objects.select_related('vat').order_by('-id')[:8]
    form = RegisterForm()
    form2 = LoginForm()
    form3 = IssuesForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.phone = form.cleaned_data['telephone']
            client.zip = form.cleaned_data['code_post']
            client.adress = form.cleaned_data['adress']
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            #__move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html', {'products' : products})
        else:
            print('oki2')
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                #if user.is_active:
                client = Client.objects.filter(user_id=user.id).first()
                #__move_session_cart_to_database_cart(request, client.id)
                login(request, user)
                return render(request, 'index.html' , {'products' : products})
            else:
                return redirect('art:error')

    return render(request, 'index.html', {'form': form, 'form2' : form2, 'products' : products})

def __move_session_cart_to_database_cart(request, client_id):
    if 'cart' in request.session:
        for product_id, qty in request.session['cart'].iteritems():
            if CartLine.objects.filter(product_id=product_id, client_id=client_id).exists():
                cart_line = CartLine.objects.get(product_id=product_id, client_id=client_id)
                cart_line.quantity += int(qty)
            else:
                cart_line = CartLine(product_id=product_id, client_id=client_id, quantity=qty)
            cart_line.save()
        del request.session['cart']
    return

def error(request):
    return render(request, 'error.html')

def logout_view(request):
    logout(request)
    return redirect('art:index')

def produits_view(request):
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')
    products = Product.objects.select_related('vat').order_by('-id')[:8]
    return render(request, 'produit.html', {'products': products ,'form': form, 'form2' : form2, 'form3' : form })

def contact_view(request):
    form = RegisterForm()
    form2 = LoginForm()
    form3 = IssuesForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')

    return render(request, 'contact.html', {'form': form, 'form2' : form2, 'form3' : form3})

def tunisie_view(request):
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')

    return render(request, 'tunisie.html', {'form': form, 'form2' : form2})

def about_view(request):
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')

    return render(request, 'about.html', {'form': form, 'form2' : form2})

def event_view(request):
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')

    return render(request, 'event.html', {'form': form, 'form2' : form2})

def single_view(request, id):
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')

    product = Product.objects.get(id=id)
    pictures = Photo.objects.filter(product__pk=product.id)
    return render(request, 'single.html', {'product': product, 'pictures': pictures , 'form': form, 'form2' : form2})

def cat_view_tapis(request):
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')
    cat = Category.objects.filter(name='tapis')
    product = Product.objects.filter(category=cat[0])
    #product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product, 'form' : form , 'form2' : form2})


def cat_view_habits(request):
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')

    cat = Category.objects.filter(name='habits')
    print(cat)
    product = Product.objects.filter(category=cat[0])
    #product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product, 'form': form, 'form2' : form2})

def cat_view_poterie(request):
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')

    cat = Category.objects.filter(name='poterie')
    product = Product.objects.filter(category=cat[0])
    #product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product, 'form': form, 'form2' : form2})

def cat_view_mosaique(request):
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')

    cat = Category.objects.filter(name='mosaique')
    product = Product.objects.filter(category=cat[0])
    #product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product, 'form': form, 'form2' : form2})

def cat_view_bijoux(request):
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')

    cat = Category.objects.filter(name='bijoux')
    product = Product.objects.filter(category=cat[0])
    #product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product, 'form': form, 'form2' : form2})

def cat_view_cuivre(request):
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')

    cat = Category.objects.filter(name='cuivre')
    product = Product.objects.filter(category=cat[0])
    #product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product, 'form': form, 'form2' : form2})

def cat_view_ceramique(request):
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')

    cat = Category.objects.filter(name='ceramique')
    product = Product.objects.filter(category=cat[0])
    #product =Product.objects.filter(category=cat)
    return render(request, 'produit.html', {'product': product, 'form': form, 'form2' : form2})

def produits_view(request):
    form = RegisterForm()
    form2 = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        form2 = LoginForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le client
            user = User(username=form.cleaned_data['username'], email=form.cleaned_data['email'],
                        first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            client = Client(user_id=user.id)
            client.save()

            # On connecte le client
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            __move_session_cart_to_database_cart(request, client.id)
            login(request, user)
            return render(request, 'index.html')
        elif form2.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    client = Client.objects.filter(user_id=user.id).first()
                    __move_session_cart_to_database_cart(request, client.id)
                    login(request, user)
                return render(request, 'index.html')
            else:
                return redirect('art:error')

    products = Product.objects.all()
    return render(request, 'produit.html', {'products': products, 'form': form, 'form2' : form2})



def reclamation(request):
    if request.method == 'POST':
        form = IssuesForm(request.POST)
        if form.is_valid():
            # On cree l utilisateur et le clie
            issues = Issues()
            issues.name = form.cleaned_data['name']
            issues.desc = form.cleaned_data['desc']
            issues.save()
    return redirect('art:index')

