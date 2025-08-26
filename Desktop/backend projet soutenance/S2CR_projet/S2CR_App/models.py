from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal


class AdministrateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class Administrateur(AbstractBaseUser):
    id_admin = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=254, null=True, blank=True)
    prenom = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    mobile = models.CharField(max_length=254, null=True, blank=True)
    password_admin = models.CharField(max_length=254)
    adresse = models.CharField(max_length=254, null=True, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = AdministrateurManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'administrateur'
        verbose_name = 'Administrateur'
        verbose_name_plural = 'Administrateurs'

    def set_password(self, raw_password):
        self.password_admin = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_admin)

    def __str__(self):
        return f"{self.prenom} {self.nom}" if self.prenom and self.nom else self.email


class CategoriePanne(models.Model):
    id_categorie = models.AutoField(primary_key=True)
    id_admin = models.ForeignKey(Administrateur, on_delete=models.RESTRICT)
    libelle = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    date_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'categorie_panne'
        verbose_name = 'Catégorie de panne'
        verbose_name_plural = 'Catégories de pannes'

    def __str__(self):
        return self.libelle


class ClientManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Client(AbstractBaseUser):
    id_client = models.AutoField(primary_key=True)
    id_admin = models.ForeignKey(Administrateur, on_delete=models.RESTRICT)
    nom = models.CharField(max_length=254)
    prenom = models.CharField(max_length=254)
    email = models.EmailField(max_length=254, unique=True)
    adresse = models.CharField(max_length=254, null=True, blank=True)
    ville = models.CharField(max_length=254, null=True, blank=True)
    mobile = models.CharField(max_length=254, null=True, blank=True)
    password_client = models.CharField(max_length=254)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = ClientManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    class Meta:
        db_table = 'client'
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def set_password(self, raw_password):
        self.password_client = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_client)

    @property
    def is_active(self):
        return self.est_actif

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class TechnicienManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Technicien(AbstractBaseUser):
    id_technicien = models.AutoField(primary_key=True)
    id_categorie = models.ForeignKey(CategoriePanne, on_delete=models.RESTRICT)
    id_admin = models.ForeignKey(Administrateur, on_delete=models.RESTRICT)
    nom = models.CharField(max_length=254)
    prenom = models.CharField(max_length=254)
    email = models.EmailField(max_length=254, unique=True)
    adresse = models.CharField(max_length=254, null=True, blank=True)
    mobile = models.CharField(max_length=254, null=True, blank=True)
    ville = models.CharField(max_length=254, null=True, blank=True)
    password_tech = models.CharField(max_length=254)
    specialite = models.CharField(max_length=254, null=True, blank=True)
    est_actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = TechnicienManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    class Meta:
        db_table = 'technicien'
        verbose_name = 'Technicien'
        verbose_name_plural = 'Techniciens'

    def set_password(self, raw_password):
        self.password_tech = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_tech)

    @property
    def is_active(self):
        return self.est_actif

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Disponibilite(models.Model):
    id_disponibilite = models.AutoField(primary_key=True)
    id_technicien = models.ForeignKey(Technicien, on_delete=models.CASCADE)
    periode = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    statut = models.CharField(
        max_length=50, 
        default='disponible',
        choices=[
            ('disponible', 'Disponible'),
            ('occupe', 'Occupé'),
            ('indisponible', 'Indisponible'),
        ]
    )
    date_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'disponibilite'
        verbose_name = 'Disponibilité'
        verbose_name_plural = 'Disponibilités'

    def __str__(self):
        return f"{self.id_technicien} - {self.periode} ({self.heure_debut}-{self.heure_fin})"


class Signalement(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('assigne', 'Assigné'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]

    id_signalement = models.AutoField(primary_key=True)
    id_client = models.ForeignKey(Client, on_delete=models.RESTRICT)
    id_categorie = models.ForeignKey(CategoriePanne, on_delete=models.RESTRICT)
    id_admin = models.ForeignKey(Administrateur, on_delete=models.RESTRICT)
    description = models.TextField()
    photo = models.CharField(max_length=500, null=True, blank=True)
    date_signalement = models.DateTimeField(default=timezone.now)
    diagnostic = models.TextField(null=True, blank=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')

    class Meta:
        db_table = 'signalement'
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'

    def __str__(self):
        return f"Signalement #{self.id_signalement} - {self.id_client}"


class Intervention(models.Model):
    STATUT_CHOICES = [
        ('programmee', 'Programmée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]

    id_intervention = models.AutoField(primary_key=True)
    id_signalement = models.ForeignKey(Signalement, on_delete=models.RESTRICT)
    id_technicien = models.ForeignKey(Technicien, on_delete=models.RESTRICT)
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    note = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[
            MinValueValidator(Decimal('0.00')),
            MaxValueValidator(Decimal('5.00'))
        ]
    )
    commentaire = models.TextField(null=True, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='programmee')
    date_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'intervention'
        verbose_name = 'Intervention'
        verbose_name_plural = 'Interventions'

    def __str__(self):
        return f"Intervention #{self.id_intervention} - {self.id_technicien}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Avertissement'),
        ('error', 'Erreur'),
        ('success', 'Succès'),
    ]

    id_notification = models.AutoField(primary_key=True)
    id_technicien = models.ForeignKey(Technicien, on_delete=models.CASCADE, null=True, blank=True)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)
    lue = models.BooleanField(default=False)
    type_notification = models.CharField(max_length=50, choices=TYPE_CHOICES, default='info')

    class Meta:
        db_table = 'notification'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.id_technicien and not self.id_client:
            raise ValidationError('Une notification doit être associée soit à un technicien soit à un client')
        if self.id_technicien and self.id_client:
            raise ValidationError('Une notification ne peut pas être associée à la fois à un technicien et à un client')

    def __str__(self):
        destinataire = self.id_technicien or self.id_client
        return f"Notification pour {destinataire} - {self.message[:50]}"


class Historique(models.Model):
    TYPE_ACTION_CHOICES = [
        ('create', 'Création'),
        ('update', 'Modification'),
        ('delete', 'Suppression'),
    ]

    id_historique = models.AutoField(primary_key=True)
    id_client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    id_technicien = models.ForeignKey(Technicien, on_delete=models.SET_NULL, null=True, blank=True)
    table_concernee = models.CharField(max_length=100)
    id_entite = models.IntegerField()
    type_action = models.CharField(max_length=50, choices=TYPE_ACTION_CHOICES)
    date_action = models.DateTimeField(default=timezone.now)
    ancienne_valeur = models.TextField(null=True, blank=True)
    nouvelle_valeur = models.TextField(null=True, blank=True)
    champ_modifie = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'historique'
        verbose_name = 'Historique'
        verbose_name_plural = 'Historiques'
        ordering = ['-date_action']

    def __str__(self):
        return f"{self.type_action} sur {self.table_concernee} #{self.id_entite}"


# Fonctions d'authentification personnalisées
def authenticate_user(email, password, user_type='client'):
    """
    Authentifie un utilisateur selon son type
    
    Args:
        email (str): Email de l'utilisateur
        password (str): Mot de passe en clair
        user_type (str): 'client', 'technicien' ou 'administrateur'
    
    Returns:
        User object si authentification réussie, None sinon
    """
    try:
        if user_type == 'client':
            user = Client.objects.get(email=email, est_actif=True)
            if user.check_password(password):
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                return user
        elif user_type == 'technicien':
            user = Technicien.objects.get(email=email, est_actif=True)
            if user.check_password(password):
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                return user
        elif user_type == 'administrateur':
            user = Administrateur.objects.get(email=email, is_active=True)
            if user.check_password(password):
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                return user
    except (Client.DoesNotExist, Technicien.DoesNotExist, Administrateur.DoesNotExist):
        pass
    
    return None


def get_user_by_email(email):
    """
    Récupère un utilisateur par son email, quel que soit son type
    
    Returns:
        Tuple (user_object, user_type) ou (None, None) si non trouvé
    """
    # Essayer Client
    try:
        user = Client.objects.get(email=email)
        return user, 'client'
    except Client.DoesNotExist:
        pass
    
    # Essayer Technicien
    try:
        user = Technicien.objects.get(email=email)
        return user, 'technicien'
    except Technicien.DoesNotExist:
        pass
    
    # Essayer Administrateur
    try:
        user = Administrateur.objects.get(email=email)
        return user, 'administrateur'
    except Administrateur.DoesNotExist:
        pass
    
    return None, None
