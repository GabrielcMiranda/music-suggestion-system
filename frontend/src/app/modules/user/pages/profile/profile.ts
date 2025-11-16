import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { UserService, ProfileData, OtherProfileData } from '../../../../core/services/user.service';
import { AuthService } from '../../../../core/services/auth.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './profile.html',
  styleUrl: './profile.scss'
})
export class Profile implements OnInit {
  
  currentUserProfile: ProfileData | null = null;

  searchInput = '';
  
  searchedProfile: ProfileData | OtherProfileData | null = null;
  

  isLoadingProfile = true;
  isSearching = false;
  errorMessage = '';
  searchErrorMessage = '';
  
  currentUsername = '';
  
  isEditingProfilePicture = false;
  selectedFile: File | null = null;
  previewUrl: string | null = null;
  isDragging = false;
  isUploadingPicture = false;
  uploadErrorMessage = '';
  
  constructor(
    private router: Router,
    private authService: AuthService,
    private userService: UserService,
  ) {}
  
  ngOnInit(): void {
    this.loadCurrentUserProfile();
  }
  
  loadCurrentUserProfile(): void {
    this.isLoadingProfile = true;
    this.errorMessage = '';
    
    const token = this.authService.getToken();
    
    if (!token) {
      this.errorMessage = 'Token não encontrado. Faça login novamente.';
      this.isLoadingProfile = false;
      this.router.navigate(['/auth/login']);
      return;
    }
    
    try {
      
      const payload = JSON.parse(atob(token.split('.')[1]));
      this.currentUsername = payload.username;
      
   
      
      if (!this.currentUsername) {
        throw new Error('Username não encontrado no token');
      }
      

      this.userService.getProfile(this.currentUsername).subscribe({
        next: (profile) => {
          this.currentUserProfile = profile as ProfileData;
          this.isLoadingProfile = false;
   
        },
        error: (error) => {
  
          this.errorMessage = error.error?.detail || 'Erro ao carregar perfil';
          this.isLoadingProfile = false;
        }
      });
      
    } catch (error) {

      this.errorMessage = 'Token inválido. Faça login novamente.';
      this.isLoadingProfile = false;
      this.authService.removeToken();
      this.router.navigate(['/auth/login']);
    }
  }
  
  searchUser(): void {
    if (!this.searchInput.trim()) {
      this.searchErrorMessage = 'Digite um username para buscar';
      return;
    }
    
    if (this.searchInput.toLowerCase() === this.currentUsername.toLowerCase()) {
      this.searchErrorMessage = 'Este é o seu próprio perfil';
      this.searchedProfile = null;
      return;
    }
    
    this.isSearching = true;
    this.searchErrorMessage = '';
    this.searchedProfile = null;
    
    this.userService.getProfile(this.searchInput).subscribe({
      next: (profile) => {
        this.searchedProfile = profile;
        this.isSearching = false;
      },
      error: (error) => {
        this.searchErrorMessage = error.error?.detail || 'Usuário não encontrado';
        this.searchedProfile = null;
        this.isSearching = false;
      }
    });
  }
  
  clearSearch(): void {
    this.searchInput = '';
    this.searchedProfile = null;
    this.searchErrorMessage = '';
  }
  
  isOwnProfile(profile: ProfileData | OtherProfileData | null): profile is ProfileData {
    return profile !== null && 'email' in profile;
  }
  
  logout(){
    this.authService.removeToken();
    this.router.navigate(['/auth/login']);
  }
  
  enableEditMode(): void {
    this.isEditingProfilePicture = true;
    this.selectedFile = null;
    this.previewUrl = null;
    this.uploadErrorMessage = '';
  }
  
  cancelEditMode(): void {
    this.isEditingProfilePicture = false;
    this.selectedFile = null;
    this.previewUrl = null;
    this.uploadErrorMessage = '';
  }
  
  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      this.handleFile(input.files[0]);
    }
  }
  
  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = true;
  }
  
  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
  }
  
  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
    
    if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
      this.handleFile(event.dataTransfer.files[0]);
    }
  }
  
  handleFile(file: File): void {
    if (!file.type.startsWith('image/')) {
      this.uploadErrorMessage = 'Por favor, selecione uma imagem válida';
      return;
    }
    
    if (file.size > 5 * 1024 * 1024) {
      this.uploadErrorMessage = 'A imagem deve ter no máximo 5MB';
      return;
    }
    
    this.selectedFile = file;
    this.uploadErrorMessage = '';
    
    const reader = new FileReader();
    reader.onload = (e) => {
      this.previewUrl = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }
  
  uploadProfilePicture(): void {
    if (!this.selectedFile) {
      this.uploadErrorMessage = 'Selecione uma imagem primeiro';
      return;
    }
    
    this.isUploadingPicture = true;
    this.uploadErrorMessage = '';
    
    const formData = new FormData();
    formData.append('file', this.selectedFile);
    
    this.userService.updateProfilePicture(formData).subscribe({
      next: () => {
        this.isUploadingPicture = false;
        this.isEditingProfilePicture = false;
        this.selectedFile = null;
        this.previewUrl = null;
        this.loadCurrentUserProfile();
      },
      error: (error) => {
        this.uploadErrorMessage = error.error?.detail || 'Erro ao atualizar foto de perfil';
        this.isUploadingPicture = false;
      }
    });
  }
}