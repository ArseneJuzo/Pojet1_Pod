from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import Client, Technicien, Administrateur

def auth_required(allowed_roles=None):
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Récupérer les données de session
            user_id = request.session.get('user_id')
            user_type = request.session.get('user_type')  
            
            # VÉRIFIER SI L'UTILISATEUR EST CONNECTÉ
            if not user_id or not user_type:
                messages.warning(request, 'Veuillez vous connecter')
                return redirect('gestion_pannes:login')
            
            # VÉRIFIER SI LE RÔLE EST AUTORISÉ
            if allowed_roles and user_type not in allowed_roles:
                messages.error(request, f'Accès refusé. Page réservée aux {", ".join(allowed_roles)}')
                return redirect('gestion_pannes:login')
            
            # VÉRIFIER QUE L'UTILISATEUR EXISTE ENCORE EN BASE
            try:
                if user_type == 'client':
                    user = Client.objects.get(id_client=user_id, est_actif=True)
                elif user_type == 'technicien':
                    user = Technicien.objects.get(id_technicien=user_id, est_actif=True)
                elif user_type == 'administrateur':
                    user = Administrateur.objects.get(id_admin=user_id, is_active=True)
                else:
                    raise ValueError('Type utilisateur invalide')
                
                # AJOUTER L'UTILISATEUR À LA REQUEST
                request.current_user = user    # Utilisateur connecté
                request.user_type = user_type 
                
            except (Client.DoesNotExist, Technicien.DoesNotExist, Administrateur.DoesNotExist):
                messages.error(request, 'Session expirée')
                request.session.flush()  # Vider la session
                return redirect('gestion_pannes:login')
            
            # TOUT EST OK, EXÉCUTER LA VUE
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator