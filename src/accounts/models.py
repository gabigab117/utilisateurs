from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


# permet de rajouter des champs par exemple
# class CustomUser(AbstractUser):
#       zip_code = models.CharField(blank=True, max_length=5)


# il faut créer un manager lorsqu'on hérite de AbstractBaseUser ! ! !  !
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, zip_code=None, genre=None):
        if not email:
            raise ValueError("Vous devez entrer un email")
        if not zip_code.isdigit():
            raise ValueError("Des chiffres voyons !")

        user = self.model(email=self.normalize_email(email), zip_code=zip_code, genre=genre)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, zip_code=None, genre=None):
        user = self.create_user(email=email, password=password, zip_code=zip_code, genre=genre)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user


# permet de modifier la façon dont vont s'authentifier les utilisateurs et ajouter des champs
# avec AbstractBaseUser on n'a que password et last_login de défini
class CustomUser(AbstractBaseUser):
    HOMME = "HO"
    FEMME = "FE"

    GENRES = [
        (HOMME, "Homme"),
        (FEMME, "Femme")
    ]
    # unique obligatoire car si se connecte avec le mail on ne peut pas avoir 2 fois le mm
    email = models.EmailField(unique=True, max_length=255, blank=False)
    # champ nécessaire pour que l'admin fonctionne
    # ici pour savoir s'il est actif ou non
    is_active = models.BooleanField(default=True)
    # est-ce qu'il a accès à l'admin ?
    is_staff = models.BooleanField(default=False)
    # est-ce qu'il a des droits d'admin ?
    is_admin = models.BooleanField(default=False)
    # je peux aussi ajouter les champs que je veux
    zip_code = models.CharField(max_length=5)
    genre = models.CharField(max_length=5, choices=GENRES, null=True)

    # je veux utiliser le champ email pour se connecter
    USERNAME_FIELD = "email"
    # si je veux qu'un champ soit obligatoire
    REQUIRED_FIELDS = ["zip_code"]

    # on relie class au modele avec attribut objects
    objects = MyUserManager()

    # il faut penser à rajouter deux méthodes :
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "Utilisateur"
