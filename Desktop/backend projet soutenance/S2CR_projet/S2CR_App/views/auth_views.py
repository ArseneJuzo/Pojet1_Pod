from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from ..models import Client, Technicien, Administrateur
from ..decorators import auth_required

def authenticate_user(email, password, user_type):
    
    try:
        if user_type == 'client':
            user = Client.objects.get(email=email, est_actif=True)
            # Vérifier le mot de passe avec check_password (hashé)
            if user.check_password(password):
                return user
        elif user_type == 'technicien':
            user = Technicien.objects.get(email=email, est_actif=True)
            if user.check_password(password):
                return user
        elif user_type == 'administrateur':
            user = Administrateur.objects.get(email=email, is_active=True)
            if user.check_password(password):
                return user
    except (Client.DoesNotExist, Technicien.DoesNotExist, Administrateur.DoesNotExist):
        pass
    
    return None  # Authentification échouée

def connexion_view(request):
    # Si déjà connecté, rediriger
    if request.session.get('user_id'):
        user_type = request.session.get('user_type')
        if user_type == 'client':
            return redirect('gestion_pannes:client_dashboard')
        elif user_type == 'technicien':
            return redirect('gestion_pannes:tech_dashboard')
        else:
            return redirect('gestion_pannes:admin_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user_type = request.POST.get('user_type', '')
        
        # VALIDATION BASIQUE
        if not all([email, password, user_type]):
            messages.error(request, 'Tous les champs sont obligatoires')
            return render(request, 'auth/login.html')
        
        if user_type not in ['client', 'technicien', 'administrateur']:
            messages.error(request, 'Type d\'utilisateur invalide')
            return render(request, 'auth/login.html')
        
        # TENTATIVE D'AUTHENTIFICATION
        user = authenticate_user(email, password, user_type)
        if user:
            # CRÉER LA SESSION
            request.session['user_id'] = user.pk
            request.session['user_type'] = user_type
            request.session['user_email'] = user.email
            
            # REDIRECTION SELON LE RÔLE
            messages.success(request, f'Bienvenue {user.get_full_name()}!')
            if user_type == 'client':
                return redirect('S2CR_App:client_dashboard')
            elif user_type == 'technicien':
                return redirect('S2CR_App:tech_dashboard')
            else:
                return redirect('S2CR_App:admin_dashboard')
        else:
            messages.error(request, 'Email, mot de passe ou type d\'utilisateur incorrect')
    
    return render(request, 'auth/login.html')

def inscription_view(request):
    
    if request.method == 'POST':
        # RÉCUPÉRER TOUTES LES DONNÉES
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        mobile = request.POST.get('mobile', '').strip()
        adresse = request.POST.get('adresse', '').strip()
        
        # VALIDATIONS
        errors = []
        
        if not all([nom, prenom, email, password, password_confirm]):
            errors.append('Tous les champs marqués * sont obligatoires')
        
        if password != password_confirm:
            errors.append('Les mots de passe ne correspondent pas')
            
        if len(password) < 8:
            errors.append('Le mot de passe doit contenir au moins 8 caractères')
        
        # Validation email
        try:
            validate_email(email)
        except ValidationError:
            errors.append('Format d\'email invalide')
        
        # Vérifier unicité email
        if Client.objects.filter(email=email).exists():
            errors.append('Cette adresse email est déjà utilisée')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'auth/register_client.html',{
                'form_data': request.POST

            })
        
        # CRÉER LE CLIENT
        try:
            # Récupérer un admin par défaut (obligatoire dans notre modèle)
            admin_default = Administrateur.objects.first()
            if not admin_default:
                messages.error(request, 'Erreur système : aucun administrateur trouvé')
                return render(request, 'auth/register_client.html')
            
            # Utiliser le manager personnalisé
            client = Client.objects.create_user(
                email=email,
                password=password,  # Sera hashé automatiquement
                nom=nom,
                prenom=prenom,
                mobile=mobile,
                adresse=adresse,
                id_admin=admin_default
            )
            
            messages.success(request, 'Inscription réussie ! Vous pouvez maintenant vous connecter.')
            return redirect('S2CR_App:login')
            
        except Exception as e:
            messages.error(request, f'Erreur lors de l\'inscription : {str(e)}')
    
    return render(request, 'auth/register_client.html')

def deconnexion_view(request):
    request.session.flush()  # Vider toute la session
    messages.success(request, 'Vous avez été déconnecté avec succès')
    return redirect('gestion_pannes:login')