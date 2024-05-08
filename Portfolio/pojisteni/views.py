from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Insurance, Insured, InsuranceEvent, UserRole, Statistics
from .forms import InsuredForm
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class InsuredIndex(generic.ListView):

    template_name = "pojisteni/insured_index.html"  
    context_object_name = "insureds"  

    def get_queryset(self):
        return Insured.objects.all()
    
    
class InsuranceIndex(generic.ListView):
    template_name = "pojisteni/insurance_index.html"
    context_object_name = "insurances"

    def get_queryset(self):
        return Insurance.objects.all()    
    
class CurrentInsured(generic.DetailView):

    model = Insured
    template_name = "pojisteni/insured_detail.html"    
    
class CreateInsured(generic.edit.CreateView):
    form_class = InsuredForm  
    template_name = "pojisteni/create_insured.html"

   
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        
        return render(request, self.template_name, {"form": form})  
    
class About(generic.TemplateView):
    template_name = "pojisteni/about.html"    
    
class EventsIndex(generic.ListView):  # přidáno
    template_name = "pojisteni/events_index.html"
    context_object_name = "events"

    def get_queryset(self):
        return InsuranceEvent.objects.all()    
    
class HomeView(TemplateView):
    template_name = 'pojisteni/home.html'    
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Přesměrování na domovskou stránku po přihlášení
    else:
        form = AuthenticationForm()
    return render(request, 'pojisteni/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Přesměrování na domovskou stránku po odhlášení

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Přesměrování na domovskou stránku po registraci
    else:
        form = UserCreationForm()
    return render(request, 'pojisteni/register.html', {'form': form})    

def edit_insured(request, pk):
    # Získání pojištěnce podle jeho primárního klíče (pk)
    insured = get_object_or_404(Insured, pk=pk)

    if request.method == 'POST':
        # Pokud je požadavek typu POST, zpracování formuláře
        form = InsuredForm(request.POST, instance=insured)
        if form.is_valid():
            form.save()
            return redirect('insured_index')  # Přesměrování na seznam pojištěnců po úspěšné editaci
    else:
        # Pokud je požadavek typu GET, zobrazíme formulář s aktuálními údaji pojištěnce
        form = InsuredForm(instance=insured)

    return render(request, 'edit_insured.html', {'form': form})

def delete_insured(request, pk):
    # Získání pojištěnce podle jeho primárního klíče (pk)
    insured = get_object_or_404(Insured, pk=pk)

    if request.method == 'POST':
        # Pokud je požadavek typu POST, provede se smazání pojištěnce
        insured.delete()
        return redirect('insured_index')  # Přesměrování na seznam pojištěnců po úspěšném smazání

    return render(request, 'delete_insured.html', {'insured': insured})