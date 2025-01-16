from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    """
    Extended user model with profile fields.
    Inherits from AbstractUser for authentication features.
    """
    # Tuple for immutability and better performance
    USER_TYPE_CHOICES = (
        ('staff', 'Staff'),
        ('tutor', 'Tutor'),
    )
    
    # Basic user fields with clear constraints
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='tutor'
    )
    phone = models.CharField(max_length=20)
    address = models.TextField()
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,  # Optional in forms
        null=True    # Optional in database
    )

    class Meta:
        # Optimize common queries with indexes
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['user_type']),
            models.Index(fields=['email']),
        ]

    # Type hints for better IDE support and code clarity
    def is_staff_member(self) -> bool:
        return self.user_type == 'staff'
    
    def is_tutor(self) -> bool:
        return self.user_type == 'tutor'

class VetSkills(models.Model):
    skills = models.CharField(max_length=100)

    def __str__(self):
        return self.skills
    
    class Meta:
        ordering=['skills']

class StaffProfile(models.Model):
    """
    Staff member profile with position and skills.
    Handles different staff roles and their permissions.
    """
    # Constants to avoid magic strings and improve maintainability
    POSITION_ADMIN = 'admin'
    POSITION_MANAGER = 'manager'
    POSITION_GROOMER = 'groomer'
    POSITION_VET = 'vet'
    POSITION_ASSISTANT = 'assistant'
    
    # Use constants in choices for consistency
    STAFF_TYPE_CHOICES = (
        (POSITION_ADMIN, 'Administrador'),
        (POSITION_MANAGER, 'Gerente'),
        (POSITION_GROOMER, 'Groomer'),
        (POSITION_VET, 'Veterinário'),
        (POSITION_ASSISTANT, 'Assistente'),
    )
    
    # Relationships with clear related_names for reverse access
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='staff_profile'
    )
    position = models.CharField(
        max_length=20,
        choices=STAFF_TYPE_CHOICES,
        default=POSITION_ASSISTANT
    )
    # Use string reference to avoid circular imports
    skills = models.ManyToManyField(
        'VetSkills',
        blank=True,
        related_name='staff_members'
    )

    class Meta:
        # Optimize position-based queries
        ordering = ['position', 'user__first_name']
        indexes = [models.Index(fields=['position'])]

    def clean(self) -> None:
        """
        Validation method to ensure skills are only assigned
        to vet or groomer positions
        """
        if not self.pk:
            return
            
        allowed_positions = [self.POSITION_VET, self.POSITION_GROOMER]
        if self.position not in allowed_positions:
            self.skills.clear()

    # Permission methods using constants for clarity
    def has_management_access(self) -> bool:
        return self.position in [self.POSITION_ADMIN, self.POSITION_MANAGER]
    
    def has_medical_access(self) -> bool:
        return self.position in [self.POSITION_VET, self.POSITION_ADMIN]
    
    def has_grooming_access(self) -> bool:
        return self.position in [
            self.POSITION_GROOMER,
            self.POSITION_ADMIN,
            self.POSITION_MANAGER
        ]

class Pet(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    age = models.IntegerField()
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='pets',
    )

class TutorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='tutor_profile',
    )

    def clean(self):
        if self.user.user_type != 'tutor':
            raise ValidationError('Apenas tutores podem ter um perfil de tutor.')

    def __str__(self):
        return f'Perfil de {self.user.get_full_name()}'
    
    # Método helper para acessar os pets do tutor
    def get_pets(self):
        return self.user.pets.all()

    class Meta:
        ordering = ['user__first_name']