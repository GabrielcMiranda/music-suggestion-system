import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../../core/services/auth.service';
import { MusicService } from '../../../../core/services/music.service';
import { ShareService } from '../../../../core/services/share.service';

export interface MusicRecommendation {
  title: string;
  artist: string;
  genre: string;
  album: string;
}

@Component({
  selector: 'app-recommendation',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './recommendation.html',
  styleUrl: './recommendation.scss'
})
export class Recommendation {
  musicInput = '';
  recommendations: MusicRecommendation[] = [];
  errorMessage = '';
  isLoading = false;
  hasSearched = false;
  
  sharingMusic: MusicRecommendation | null = null;
  shareEmail = '';
  isSharing = false;
  shareErrorMessage = '';
  shareSuccessMessage = '';

  constructor(
    private router: Router,
    private authService: AuthService,
    private musicService: MusicService,
    private shareService: ShareService
  ) {}

  onSubmit() {
    if (!this.musicInput.trim()) {
      this.errorMessage = 'Por favor, digite o nome de uma música';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.hasSearched = true;

    this.musicService.generateRecommendation(this.musicInput).subscribe({
      next: (response) => {
        this.recommendations = response.recommendations;
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = error.error?.detail || 'Erro ao buscar recomendações';
        this.recommendations = [];
        this.isLoading = false;
      }
    });
  }

  logout() {
    this.authService.removeToken();
    this.router.navigate(['/auth/login']);
  }
  
  openShareModal(music: MusicRecommendation): void {
    this.sharingMusic = music;
    this.shareEmail = '';
    this.shareErrorMessage = '';
    this.shareSuccessMessage = '';
  }
  
  closeShareModal(): void {
    this.sharingMusic = null;
    this.shareEmail = '';
    this.shareErrorMessage = '';
    this.shareSuccessMessage = '';
  }
  
  shareMusic(): void {
    if (!this.shareEmail.trim()) {
      this.shareErrorMessage = 'Por favor, insira um email';
      return;
    }
    
    if (!this.sharingMusic) {
      return;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.shareEmail)) {
      this.shareErrorMessage = 'Por favor, insira um email válido';
      return;
    }
    
    this.isSharing = true;
    this.shareErrorMessage = '';
    this.shareSuccessMessage = '';
    
    this.shareService.shareSong(this.sharingMusic, this.shareEmail).subscribe({
      next: () => {
        this.shareSuccessMessage = 'Música compartilhada com sucesso!';
        this.isSharing = false;
        
        setTimeout(() => {
          this.closeShareModal();
        }, 2000);
      },
      error: (error) => {
        this.shareErrorMessage = error.error?.detail || 'Erro ao compartilhar música';
        this.isSharing = false;
      }
    });
  }
}
